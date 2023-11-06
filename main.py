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
            
            RE = r * np.cos(self.starting_angles[i])
            IM = r * np.sin(self.starting_angles[i])
            
            pygame.draw.aaline(WINDOW,PURPLE,starting_position,(starting_position[0]+RE,starting_position[1]+IM))
            
            for c in line.circles :
                line.circles.pop() # pop the first drawn circles to stop overlap
            
            starting_position = [starting_position[0] + RE, starting_position[1] + IM]
            
            # update the start position along the 'journey' of radii through till the i'th vectorline , after the first iteration the new start position is essentially the tip of 
            # first circle, then on the second it would be the tip of the second circle, etc...
        
        
        difference = WIDTH/2 - starting_position[0] # calculate the difference between the endpoint and the middle line for drawing
        
        pygame.draw.aaline(
            WINDOW,
            PURPLE,
            starting_position,
            (starting_position[0]+difference,starting_position[1])
            ) # draw that connection line to the mid point
        
        old_length = len(line.points) # get how many points are inside the array ready for drawing
        
        line.points.append([starting_position[0]+difference,starting_position[1]]) # append each drawing point
        
        if old_length != len(line.points) : # shift all drawing points by pi/4 rad
            for i in range(len(line.points)) :
                line.points[i][0] = line.points[i][0] + 360 * np.pi/(180*2*line.slowing)
            
        if len(line.points) >= 2: # gatekeep lines as it requires multiple points before drawing
            pygame.draw.lines(WINDOW,PURPLE,False,line.points)

        if len(line.points) > 500 : # remove first drawn points as they will be off screen and sucking performance
            _, *line.points = line.points
        
    def move(self) -> None :

        for i,angle in enumerate(self.starting_angles) :
            
            self.starting_angles[i] = self.starting_angles[i] - ((self.frequencies[i]) * np.pi/(180*FPS*line.slowing)) # 
        # Ae^{iw}
        
class circle() :
    
    def __init__(self,position : list, radius : int) :
        self.position = position
        self.radius = radius
    
    def draw(self) -> None :

        pygame.gfxdraw.aacircle(
            WINDOW,
            int(self.position[0]),
            int(self.position[1]),
            int(self.radius),
            PURPLE
        )

    
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
    
# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def main() :

    SCALE = 80
    LIMIT = 10
    running = True

    box_theta = [360] * LIMIT
    box_theta = [x * (2*(n+1)-1) for n,x in enumerate(box_theta)]
    
    box_radius = [4/np.pi] * LIMIT
    box_radius = [SCALE/2 * x * 1/(2*(n+1)-1) for n,x in enumerate(box_radius)]
    
    obj = line([WIDTH/4,HEIGHT/2],
               box_radius,
               [np.pi/2]*int(LIMIT),
               box_theta
               )

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
        t2.draw()
        obj.draw()
        
    return 0

if __name__ == '__main__' :
    main()