import pygame
from pygame import gfxdraw
import numpy as np
from datetime import datetime

# Setup Constants ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
LIGHT_BLUE = [173,216,230]
YELLOW = [255,255,0]
PURPLE = [203, 195, 227]
GRAY = [169,169,169]
DIM_GRAY = [16,16,16]
ORANGE = [255,165,0]
BROWN = [222,184,135]

WIDTH = 1080
HEIGHT = 720
PADDING = 10
FPS = 60

X_AXIS = np.array([1,0,0])
Y_AXIS = np.array([0,1,0])
Z_AXIS = np.array([0,0,1])

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Fourier Series')
pygame.font.init()
font = pygame.font.SysFont('didot.ttc', 72)
CLOCK = pygame.time.Clock()

# Classes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class line () :
    
    circles = [] # init array for each corresponding circle that matches with the vector line
    points = [] # init array for each point that hits the drawing line
    slowing = 1
    
    def __init__(self,position : list, radius_list : list, starting_angles : list , frequencies : list) :
        self.frequencies = frequencies
        self.starting_angles = starting_angles
        self.position = position
        self.end_positon = []
        self.radius_list = radius_list
        
        
    def draw(self) -> None  : 
        
        starting_position = self.position # Start the path at the passed start position
        
        for i,r in enumerate(self.radius_list) : 
            
            line.circles.append(circle(starting_position,r)) # create the circle for the vector line i of length len(radius_list)
            
            for c in line.circles :
                c.draw() # draw each circle for each vector line
            
            pygame.draw.aaline(WINDOW,PURPLE,starting_position,(starting_position[0]+r*np.cos(self.starting_angles[i]),starting_position[1]+r*np.sin(self.starting_angles[i])))
            # draw the vector line from the recurrant start position to the end position, which calculated through start_recurring = r_i * cos(theta_i)
            
            for c in line.circles :
                line.circles.pop() # pop the first drawn circles to stop overlap
        
            starting_position = [starting_position[0] + r * np.cos(self.starting_angles[i]), starting_position[1] + r * np.sin(self.starting_angles[i])]
            # update the start position along the 'journey' of radii through till the i'th vectorline , after the first iteration the new start position is essentially the tip of 
            # first circle, then on the second it would be the tip of the second circle, etc...
        
        difference = WIDTH/2 - starting_position[0] # calculate the difference between the endpoint and the middle line for drawing
        
        pygame.draw.aaline(WINDOW,PURPLE,starting_position,(starting_position[0]+difference,starting_position[1])) # draw that connection line to the mid point
        
        old_length = len(line.points) # get how many points are inside the array ready for drawing
        
        line.points.append([starting_position[0]+difference,starting_position[1]]) # append each drawing point
        
        if old_length != len(line.points) : # shift all drawing points by pi/4 rad
            for i in range(len(line.points)) :
                line.points[i][0] = line.points[i][0] + 90 * np.pi/(180*line.slowing)
            

        if len(line.points) >= 2: # gatekeep lines as it requires multiple points before drawing
            pygame.draw.lines(WINDOW,PURPLE,False,line.points)

        if len(line.points) > 500 : # remove first drawn points as they will be off screen and sucking performance
            _, *line.points = line.points
        
        
        
        #self.end_positon = [self.position[0] + self.radius * np.cos(self.starting_angles),self.position[1] + self.radius * np.sin(self.starting_angles)] 
        
        #pygame.draw.aaline(WINDOW,PURPLE,self.position,self.end_positon)
        
    def move(self) -> None :
        
        for i,angle in enumerate(self.starting_angles) :
            
            self.starting_angles[i] = self.starting_angles[i] - self.frequencies[i] * np.pi/(180*60*line.slowing) # 
            
            #self.starting_angles[i] = [angle - self.frequencies[i] * np.pi/(180*60) for angle in self.starting_angles]
        
class circle() :
    def __init__(self,position : list, radius : int) :
        self.position = position
        self.radius = radius
    
    def draw(self) -> None :
        pygame.gfxdraw.aacircle(WINDOW,int(self.position[0]),int(self.position[1]),int(self.radius),PURPLE)
        pass
    
class text() :
    
    texts = []
    images = []
    
    def __init__(self,position : list, size : float, padding : int, message : str) :
        self.position = position
        self.message = message
        self.img = font.render(self.message, True, PURPLE)
        self.size = size
        self.padding = 10
        
    def draw(self) : 
        WINDOW.blit(self.img,self.position)
        
    def clock(self,time) :
        pass
        


# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def main() :
    
    x = 0 
    SCALE = 80
    LIMIT = 250
    SPEED=1
    running = True
    
    t1 = text([40,40],10,10,'test')

    a_theta = [360] * LIMIT
    a_theta = [(x * ((2*i)+1))/SPEED for i,x in enumerate(a_theta)]
    
    a_radius = [4*SCALE/np.pi] * LIMIT
    a_radius = [x*1/((2*i)+1) for i,x in enumerate(a_radius)]

    
    # sin waves cover a cycle in 1 second, meaning 360/60 6 degrees per frame.
    
    #obj = line([WIDTH/4,HEIGHT/2],a_radius,[0]*LIMIT,a_theta)
    obj = line([WIDTH/4,HEIGHT/2],[25,10,5,2],[0]*4,[360,720,45,90])
    
    while running :

        CLOCK.tick(FPS)

        mousex,mousey = pygame.mouse.get_pos()

        for event in pygame.event.get() :
            
            if event.type == pygame.QUIT :
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False   

        # Update   
        now = datetime.now()
        obj.move()
        pygame.display.update()
        
        # Render
        WINDOW.fill(DIM_GRAY)
        pygame.draw.aaline(WINDOW,PURPLE,(WIDTH/2,0),(WIDTH/2,HEIGHT))
        current_time = now.strftime("%H:%M:%S")
        t2 = text([40,40],10,10,current_time)
        obj.draw()
        t2.draw()
        
            

    return 0


if __name__ == '__main__' :
    main()