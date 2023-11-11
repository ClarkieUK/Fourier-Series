import pygame
from pygame import gfxdraw
import numpy as np
from datetime import datetime
import scipy.integrate as spi
from numpy import pi
from numpy import cos
from numpy import sin

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
RESOLUTION = 1000
SCALE = 75

X_AXIS = np.array([1,0,0])
Y_AXIS = np.array([0,1,0])
Z_AXIS = np.array([0,0,1])

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
intermediate_surface = pygame.Surface(WINDOW.get_size())

pygame.display.set_caption('Fourier Series')
pygame.font.init()
font = pygame.font.SysFont('didot.ttc', 36)
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
            """
            cos_frequenciesrequencies.append(360*
                                             (2*n-1))
            
            sin_frequenciesrequencies.append(360*
                                             n # series
                )
            
            cos_coeffs.append(scale * 
                              1/(2*n-1)# series
                              )
            sin_coeffs.append(scale * 
                              -(-1)**n/(n)# series
                              )
            """
            cos_frequenciesrequencies.append(360*
                                             n)
            
            sin_frequenciesrequencies.append(360*
                                             (n) # series
                )
            
            cos_coeffs.append(scale * 
                              1/(4*n**2-1)# series
                              )
            sin_coeffs.append(scale * 
                              -(-1)**n/(n)# series
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

def init_series(resolution : int,scale : float,sines : bool,cosines :bool) :
    global obj
    
    data = fourier(resolution,scale,sines,cosines)
    
    obj = line([WIDTH/4,HEIGHT/2],
            data[0], # coeffs
            data[1], # freqs
            data[2] # starting angles
            )
   
def button_sinx() :
    init_series(RESOLUTION,SCALE,True,False)
    
def button_both() :
    init_series(RESOLUTION,SCALE,True,True)
    
def button_cosx() :
    init_series(RESOLUTION,SCALE,False,True)
    
    

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
        
        line.trace.append([starting_position[0],starting_position[1]])
        
        # + WIDTH / 4
        if tracing and len(line.trace) > 1:
            pygame.draw.aalines(WINDOW,RED,False,line.trace)
        
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
        self.padding = padding
        
    def draw(self,surface) : 
        surface.blit(self.img,self.position)
    
# make array of buttons that measures length from top right to easily add new buttons
    
class Button() :
    
    buttons = []
    padding = 10
    ## NEED TO FINISH PADDING LOGIC - GOOD LUCK SOLDIER!
    i = 0
    def __init__(self,text,color : list,width,height,pos,depth,function : callable) :
        # Logic
        Button.buttons.append(self)
        self.clicked = False
        self.logged_click_position = False
        self.depth = depth
        self.color = color
        self.width = width
        self.function = function
        
        total_x_distance = 0
        
        for i in range(len(Button.buttons)) :
            total_x_distance -= (Button.buttons[i].width + (1) * Button.padding)
            
        pos[0] += total_x_distance  
        pos[1] += Button.padding    
        
        self.origin = pos
        self.loose_origin = pos
        
        # Top Rectangle
        self.top_rectangle = pygame.Rect((self.loose_origin),(width,height))
        self.top_color = color
        
        # Bottom Rectangle
        self.bottom_rectangle = pygame.Rect((pos[0],pos[1]+self.depth),(width,height))
        self.bottom_color = [x - 10 for x in color]
    
        # Text
        self.text_surface = font.render(text,1,'#FFFFFF')
        self.text_rectangle = self.text_surface.get_rect(center = self.top_rectangle.center)
        
    def draw(self,surface) :
        
        pygame.draw.rect(surface,self.bottom_color,self.bottom_rectangle,border_radius=12)
        pygame.draw.rect(surface,self.top_color,self.top_rectangle,border_radius=12)
        surface.blit(self.text_surface,self.text_rectangle)
        
    def update(self) :
        
        mouse_position = pygame.mouse.get_pos()
        
        if self.top_rectangle.collidepoint(mouse_position) :
            self.top_color = [x + 20 for x in self.color]
        else :
            self.top_color = self.color
            x,y = self.origin
            self.top_rectangle[1] = y 
            self.text_rectangle = self.text_surface.get_rect(center = self.top_rectangle.center)
        
        if pygame.mouse.get_pressed()[0] :
            if not self.logged_click_position :
                self.clicked_initial_position = pygame.mouse.get_pos()
                self.logged_click_position = True

            if self.top_rectangle.collidepoint(mouse_position) and self.top_rectangle.collidepoint(self.clicked_initial_position) :      
                
                if pygame.mouse.get_pressed()[0] and self.clicked == False : 
                    self.clicked = True
                    self.top_rectangle[1] += (self.depth)/2
                    self.text_rectangle[1] += (self.depth)/2
                    # Do operation
                    self.function()
                    
        if not pygame.mouse.get_pressed()[0] :
            self.logged_click_position = False 
            self.clicked = False   
            self.top_rectangle[1] = self.origin[1]
            self.text_rectangle = self.text_surface.get_rect(center = self.top_rectangle.center)
       
        
        
        
# Main --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def main() :
    global resolution,scale
    
    running = True
    tracing = False
    
    init_series(RESOLUTION,SCALE,True,True)
    
    sine_button = Button('sin(x)',[134, 91, 235],80,40,[WIDTH,0],6,button_sinx)
    both_button = Button('both!',[134, 91, 235],80,40,[WIDTH,0],6,button_both)
    cosine_button = Button('cos(x)',[134, 91, 235],80,40,[WIDTH,0],6,button_cosx)

    while running :

        CLOCK.tick(FPS)

        for event in pygame.event.get() :
            
            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False      
                if event.key == pygame.K_r :
                    running = False
                    Button.buttons = []
                    line.trace = []
                    line.points = []
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
        for button in Button.buttons :
            button.update()
        
        # Render
        WINDOW.fill(DIM_GRAY)

        # Fourier 
        pygame.draw.aaline(WINDOW,PURPLE,(WIDTH/2,0),(WIDTH/2,HEIGHT))
        obj.draw(tracing)
        
        # Texts
        t2 = text([0,0],10,10,current_time,PURPLE)
        t2.draw(WINDOW)
        
        # Buttons
        for button in Button.buttons :
            button.draw(WINDOW) 
        
        # Sliders
        
    
    return 0

if __name__ == '__main__' :
    main()