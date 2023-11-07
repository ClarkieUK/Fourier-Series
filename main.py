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
intermediate_surface = pygame.Surface(WINDOW.get_size())

pygame.display.set_caption('Fourier Series')
pygame.font.init()
font = pygame.font.SysFont('didot.ttc', 72)
CLOCK = pygame.time.Clock()



# Classes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class line () :
    
    circles = [] # init array for each corresponding circle that matches with the vector line
    points = [] # init array for each point that hits the drawing line
    slowing = 3
    
    def __init__(self,position : list, radius_list : list, starting_angles : list , frequencies : list) :
        self.frequencies = frequencies
        self.starting_angles = starting_angles
        self.position = position
        #self.end_positon = []
        self.radius_list = radius_list
        
        self.sin_rad = radius_list[0]
        self.cos_rad = radius_list[1]
        
        self.sin_f = frequencies[0]
        self.cos_f = frequencies[1]
        
        self.sin_starting_angles = starting_angles[0]
        self.cos_starting_angles = starting_angles[1]
        
        # shift start location MOVE TO FUNCTION ASAP
        for i,v in enumerate(self.sin_f) :
            self.sin_starting_angles[i] = self.sin_starting_angles[i] + self.sin_f[i] * 2
            self.cos_starting_angles[i] = self.cos_starting_angles[i] + self.cos_f[i] * 2
              
        
    def draw(self) -> None  : 
        
        starting_position = self.position # Start the path at the passed start position
        
        for i,r in enumerate(self.sin_rad) : 
            
            RE = (self.sin_rad[i]*np.cos(self.sin_starting_angles[i]) + self.cos_rad[i] * np.cos(self.cos_starting_angles[i])) * (-1)
            IM = (self.sin_rad[i]*np.sin(self.sin_starting_angles[i]) + self.cos_rad[i] * np.sin(self.cos_starting_angles[i])) * (-1)
            
            line.circles.append(circle(starting_position,np.sqrt((RE)**2+(IM)**2))) # create the circle for the vector line i of length len(radius_list)
            
            for c in line.circles :
                c.draw() # draw each circle for each vector line
            
            pygame.draw.aaline(WINDOW,PURPLE,starting_position,(starting_position[0] + RE,starting_position[1] + IM))
            
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
                line.points[i][0] = line.points[i][0] + 180 * np.pi/(180*line.slowing)

            
        if len(line.points) >= 2: # gatekeep lines as it requires multiple points before drawing
            pygame.draw.lines(WINDOW,PURPLE,False,line.points)

        if len(line.points) > 500 : # remove first drawn points as they will be off screen and sucking performance
            _, *line.points = line.points
        
    def move(self) -> None :

        for i,angle in enumerate(self.sin_starting_angles) :
            
            #self.starting_angles[i] = self.starting_angles[i] - ((self.frequencies[i]) * np.pi/(180*FPS*line.slowing)) # 
            self.sin_starting_angles[i] = self.sin_starting_angles[i] - ((self.sin_f[i]) * np.pi/(180*FPS*line.slowing))
            self.cos_starting_angles[i] = self.cos_starting_angles[i] - ((self.cos_f[i]) * np.pi/(180*FPS*line.slowing))
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
    LIMIT = 100
    running = True

    box_theta = [360] * LIMIT
    box_theta = [x * (2*(n+1)-1) for n,x in enumerate(box_theta)]
    
    box_radius = [4/np.pi] * LIMIT
    box_radius = [SCALE/2 * x * 1/(2*(n+1)-1) for n,x in enumerate(box_radius)]
    """
    obj = line([WIDTH/4,HEIGHT/2],
               box_radius,
               [np.pi]*int(LIMIT),
               box_theta
               )
               
    """
    sin_theta = [360] * LIMIT
    cos_theta = [360] * LIMIT
    
    sin_theta = [x * ((n+1))  for n,x in enumerate(sin_theta)]
    cos_theta = [x * (2*(n+1)) for n,x in enumerate(cos_theta)]
    
    thetas = [sin_theta,cos_theta]
    #thetas = [sin_theta,[0]*LIMIT]
    
    sin_rad = [1] * LIMIT
    sin_rad = [SCALE* x * 1/(n+1) for n,x in enumerate(sin_rad)]
    
    cos_rad = [1] * LIMIT
    cos_rad = [SCALE * x * 1/(4*(n+1)**2-1) for n,x in enumerate(cos_rad)]

    radii = [sin_rad,cos_rad]
    #radii = [sin_rad,[0]*LIMIT]

    starting_angles = [[0]*LIMIT,[np.pi/2]*LIMIT]
    
    obj = line([WIDTH/4,HEIGHT/2],
               radii,
               starting_angles,
               thetas
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
                if event.key == pygame.K_r :
                    running = False
                    main()

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
        
        
        #WINDOW.blit(pygame.transform.flip(WINDOW, 0, True), (0,0))
        
        
    return 0

if __name__ == '__main__' :
    main()