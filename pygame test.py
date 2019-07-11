import pygame
import random
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

rect_x = 50
rect_y = 50

rect_change_x = 2
rect_change_y = 2
# -- Blank Screen
size = (720,480)
screen = pygame.display.set_mode(size)
# -- Title of new window/screen
pygame.display.set_caption("DVD Screen saver test")
# -- Exit game flag set to false
done = False 
# -- Manages how fast screen refreshes

snow_list = []


# Loop 50 times and add a snow flake in a random x,y position
for i in range(50):
    x = random.randrange(0, 400)
    y = random.randrange(0, 400)
    snow_list.append([x, y])
clock = pygame.time.Clock()
### -- Game Loop
while not done:
# -- User input and controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
#End If
 #Next event
# -- Game logic goes after this comment
    rect_x += rect_change_x
    rect_y += rect_change_y
    if rect_y > 450 or rect_y < 0:
        rect_change_y = rect_change_y * -1
    if rect_x > 650 or rect_x < 0:
        rect_change_x = rect_change_x * -1
    for i in range(len(snow_list)):
            snow_list[i][1] += 1
            if snow_list[i][1] > 400:
                    # Reset it just above the top
                    y = random.randrange(-50, -10)
                    snow_list[i][1] = y
                    # Give it a new x position
                    x = random.randrange(0, 400)
                    snow_list[i][0] = x
    pos = pygame.mouse.get_pos()
    print(pos)
    x = pos[0]
    y = pos[1]
# -- Screen background is BLUE
    screen.fill (GREY)
    # -- Draw here
    pygame.draw.rect(screen, NAVY, [rect_x, rect_y, 50, 50])
    pygame.draw.rect(screen, RED, [rect_x + 10, rect_y + 10 ,30, 30])
    pygame.draw.circle(screen, WHITE, snow_list[i], 5)
    draw_stick_figure(screen,x,y)  
# -- flip display to reveal new position of objects
    pygame.display.flip()
 # - The clock ticks over
    clock.tick(60)
#End While - End of game loop
pygame.quit()

