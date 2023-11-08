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

# Functions ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def fourier(limit : int, scale : int, sine : bool, cosine : bool) :
        
        # 1/pi * (-pi -> pi)int{f(x)sin(nx)dx} for odd
        # 1/pi * (-pi -> pi)int{f(x)cos(nx)dx} for even
        
        cos_coeffs = []
        sin_coeffs = []
        cos_frequenciesrequencies = []
        sin_frequenciesrequencies = []
        
        for n in range(1,limit+1) :
            
            # cos(2n*x) * 1/(4n^2-1)    +   sin(n*x) * 1/n
            
            cos_frequenciesrequencies.append(360*2*
                                             n)
            
            sin_frequenciesrequencies.append(360*
                                             n # series
                )
            
            cos_coeffs.append(scale * 
                              1/(4*n**2-1) # series
                              )
            sin_coeffs.append(scale * 
                              (-1)* ((-1)**n)/n # series
                              )
            
        if sine and cosine :
            data = [
            [sin_coeffs,cos_coeffs],
            [sin_frequenciesrequencies,cos_frequenciesrequencies],
            [[0]*limit,[np.pi/2]*limit]
            ]
        
        if sine and not cosine: 
            data = [
            [sin_coeffs,[0]*limit],
            [sin_frequenciesrequencies,[0]*limit],
            [[0]*limit,[np.pi/2]*limit]
            ]
            
        if cosine and not sine: 
            data = [
            [[0]*limit,cos_coeffs],
            [[0]*limit,cos_frequenciesrequencies],
            [[0]*limit,[np.pi/2]*limit]
            ]
        
        return data


# Classes -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
class line () :
    
    circles = [] # init array for each corresponding circle that matches with the vector line
    points = [] # init array for each point that hits the drawing line
    trace = []
    slowing = 3
    
    def __init__(self,position : list, coefficients : list, frequencies : list, theta : list) :
        self.position = position
    
        self.sin_coefficients = coefficients[0]
        self.cos_coefficients = coefficients[1]
        
        self.sin_frequencies = frequencies[0]
        self.cos_frequencies = frequencies[1]
        
        self.sin_thetas = theta[0]
        self.cos_thetas = theta[1]
        
        # shift start location MOVE TO FUNCTION ASAP
        for i,v in enumerate(self.sin_frequencies) :
            self.sin_thetas[i] = self.sin_thetas[i] + self.sin_frequencies[i] * 2
            self.cos_thetas[i] = self.cos_thetas[i] + self.cos_frequencies[i] * 2
              
        
    def draw(self,tracing) -> None  : 
        
        starting_position = self.position # Start the path at the passed start position
        
        for i,r in enumerate(self.sin_coefficients) : 
            
            RE = (self.sin_coefficients[i]*np.cos(self.sin_thetas[i]) + self.cos_coefficients[i] * np.cos(self.cos_thetas[i])) * (-1)
            IM = (self.sin_coefficients[i]*np.sin(self.sin_thetas[i]) + self.cos_coefficients[i] * np.sin(self.cos_thetas[i])) * (-1)
            
            line.circles.append(circle(starting_position,np.sqrt((RE)**2+(IM)**2))) # create the circle for the vector line i of length len(coefficients)
            
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
        
        line.trace.append([starting_position[0]+WIDTH/4,starting_position[1]])
        
        if tracing and len(line.trace) > 1:
            pygame.draw.lines(WINDOW,RED,False,line.trace)
        
        if old_length != len(line.points) : # shift all drawing points by pi/4 rad
            for i in range(len(line.points)) :
                line.points[i][0] = line.points[i][0] + 180 * np.pi/(180*line.slowing)

        if len(line.points) >= 2: # gatekeep lines as it requires multiple points before drawing
            pygame.draw.lines(WINDOW,PURPLE,False,line.points)

        if len(line.points) > 500 : # remove first drawn points as they will be off screen and sucking performance
            _, *line.points = line.points
    
    def move(self) -> None :

        for i,theta in enumerate(self.sin_thetas) :
            
            #self.theta[i] = self.theta[i] - ((self.frequencies[i]) * np.pi/(180*FPS*line.slowing)) # 
            self.sin_thetas[i] = self.sin_thetas[i] - ((self.sin_frequencies[i]) * np.pi/(180*FPS*line.slowing))
            self.cos_thetas[i] = self.cos_thetas[i] - ((self.cos_frequencies[i]) * np.pi/(180*FPS*line.slowing))
        # Ae^{iw}

class circle() :
    
    def __init__(self,position : list, radius : int) :
        self.position = position
        self.radius = radius
    
    def draw(self) -> None :
        try : 
            pygame.gfxdraw.aacircle(
                WINDOW,
                int(self.position[0]),
                int(self.position[1]),
                int(self.radius),
                PURPLE
            )
        except : 
            pass

class text() : 
    
    texts = []
    images = []
    
    def __init__(self,position : list, size : float, padding : int, message : str, color : tuple) :
        self.position = [position[0]+padding,position[1]+padding]
        self.message = message
        self.img = font.render(self.message, True, PURPLE)
        self.size = size
        self.padding = 10
        
    def draw(self,surface) : 
        surface.blit(self.img,self.position)
    
# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def main() :

    running = True
    tracing = False

    data = fourier(1000,50,True,False)
    
    obj = line([WIDTH/4,HEIGHT/2],
               data[0],
               data[1],
               data[2]
               )

    while running :

        CLOCK.tick(FPS)

        mouse_position = pygame.mouse.get_pos()
        print(mouse_position)

        for event in pygame.event.get() :
            
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False      
                if event.key == pygame.K_r :
                    running = False
                    main()                
                if event.key == pygame.K_t :
                    if tracing :
                        tracing = False
                    else :
                        tracing = True            

        # Update   
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        obj.move()
        pygame.display.update()
        
        # Render
        WINDOW.fill(DIM_GRAY)

        # Fourier 
        pygame.draw.aaline(WINDOW,PURPLE,(WIDTH/2,0),(WIDTH/2,HEIGHT))

        obj.draw(tracing)
        
        # Texts
        t2 = text([0,0],10,20,current_time,PURPLE)
        t2.draw(WINDOW)
        
        # Buttons
        
        
        # Sliders
        
    
    return 0

if __name__ == '__main__' :
    main()