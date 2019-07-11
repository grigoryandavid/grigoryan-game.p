import pygame
import random
import math

# -- Global Constants
# -- Colours
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (50,50,255)
YELLOW = (255,255,0)
RED = (255,0,0)
BLUEGREEN = (141,238,238)
DARKBLUE = (16,78,139)
GREY = (99,99,99)
GREEN = (124,252,0)
VIOLET = (238,0,238)
NAVY = (0,0,128)

def draw_stick_figure(screen,x,y):
    # Head
    pygame.draw.ellipse(screen, BLACK, [1+x,y,10,10], 0)
 
    # Legs
    pygame.draw.line(screen, BLACK ,[5+x,17+y], [10+x,27+y], 2)
    pygame.draw.line(screen, BLACK, [5+x,17+y], [x,27+y], 2)
 
    # Body
    pygame.draw.line(screen, RED, [5+x,17+y], [5+x,7+y], 2)
 
    # Arms
    pygame.draw.line(screen, RED, [5+x,7+y], [9+x,17+y], 2)
    pygame.draw.line(screen, RED, [5+x,7+y], [1+x,17+y], 2)

# -- Initialise PyGame
pygame.init()
# -- Blank Screen
size = (640,480)

screen = pygame.display.set_mode(size)
# -- Title of new window/screen
pygame.display.set_caption("My Window")
# -- Exit game flag set to false
done = False
# -- Manages how fast screen refreshes
clock = pygame.time.Clock()
#player 1 
x_speed = 0
y_speed = 0

x_coord = 10
y_coord = 10

#player 2

x1_speed = 0
y1_speed = 0

x1_coord = 10
y1_coord = 10

### -- Game Loop

while not done:
# -- User input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_LEFT:
                x_speed = -3
            elif event.key == pygame.K_RIGHT:
                x_speed = 3
            elif event.key == pygame.K_UP:
                y_speed = -3
            elif event.key == pygame.K_DOWN:
                y_speed = 3
 
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_speed = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                y_speed = 0
      

# other player controls

        elif event.type == pygame.KEYDOWN:
            # Figure out if it was an arrow key. If so
            # adjust speed.
            if event.key == pygame.K_a:
                x_speed = -3
            elif event.key == pygame.K_d:
                x_speed = 3
            elif event.key == pygame.K_w:
                y_speed = -3
            elif event.key == pygame.K_s:
                y_speed = 3
 
        # User let up on a key
        elif event.type == pygame.KEYUP:
            # If it is an arrow key, reset vector back to zero
            if event.key == pygame.K_a or event.key == pygame.K_d:
                x_speed = 0
            elif event.key == pygame.w or event.key == pygame.K_s:
                y_speed = 0
        



#End If

 #Next event
# -- Game logic goes after this comment
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed

    x1_coord = x1_coord + x1_speed
    y1_coord = y1_coord + y1_speed 
    # -- Screen background is BLACK
    screen.fill (WHITE)
    # -- Draw here
    draw_stick_figure(screen,x_coord,y_coord)
    draw_stick_figure(screen,x_coord,y_coord)
    # -- flip display to reveal new position of objects
    pygame.display.flip()
     # - The clock ticks over
    clock.tick(60)
    #End While - End of game loop
pygame.quit()

