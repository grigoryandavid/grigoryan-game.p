#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame
import random
import time
import json

# -- Global Constants
# -- Colours

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUEGREEN = (141, 238, 238)
DARKBLUE = (16, 78, 139)
GREY = (99, 99, 99)
GREEN = (124, 252, 0)
VIOLET = (238, 0, 238)
NAVY = (0, 0, 128)

# screen definition

size = (W, H) = (800, 600)
LEVELS_COUNT = 2
screen = pygame.display.set_mode(size)

# -- Title of new window/screen

pygame.display.set_caption('footballers')

# -- Exit game flag set to false

done = False

# -- Manages how fast screen refreshes

clock = pygame.time.Clock()

# -- Initialise PyGame

pygame.init()

font = pygame.font.SysFont(None, 25)

# -- the message to screen functions renders and draws text.
def message_to_screen(
    msg,
    color,
    x=None,
    y=None,
    ):
    screen_text = font.render(msg, True, color)
    if not x or not y:
        screentext_w = screen_text.get_width()
        x = (W - screentext_w) / 2
        y = H / 2
    screen.blit(screen_text, [x, y])


#-- this is the class for the green chest in the game, the random number
   # generation is done in the maze class
class Chest:

    def __init__ (self, color, x_coord, y_coord):
        self.color = color
        self. x_coord =  x_coord
        self. y_coord = y_coord
        self.number = random.randint(0, 9)
        self.chest_rect = None 
    def draw(self):
        self.chest_rect = pygame.draw.rect( screen, self.color, [self.x_coord, self.y_coord, 20, 20])

    def detect(self, player_rect):
        if self.chest_rect and self.chest_rect.colliderect(player_rect):
            print("chest detect")
            message_to_screen(str(self.number), RED, self.x_coord, self.y_coord)




    
    # this class is called two times for the different levels and also does collision detection.


class Maze:

    def __init__(self, color,level):
        global screen
        global size
        global W
        global H
        self.color = color

        # top, left, w, h
        filename = "level" + str(level) + ".json"
        level_file = open(filename)
        self.LEVELINFO = json.load(level_file)
        self.walls = []
        self.winning_area = None
        size = (W, H) = self.LEVELINFO['screen_size']
        screen = pygame.display.set_mode(size)
        chest_coords = self.LEVELINFO['chest_coords']
        self.chest = []
        for ch in chest_coords:
            self.chest.append(Chest( GREEN, ch[0],ch[1]))
        self.maze_key = ""
        for chest in self.chest:
            self.maze_key += str(chest.number)
        self.maze_key = "".join(sorted(self.maze_key))
        hyperloop_params = self.LEVELINFO['hyperloop_params']
        self.hyperloops = []
        # example of params [[in_x,in_y,x_speed,y_speed], [out_x,out_y,x_speed,y_speed]],
        for hl in hyperloop_params:
            self.hyperloops.append(Hyperloop(GREY, hl[0], hl[1],15,15))
            
    def draw(self):
        walls = self.LEVELINFO['walls']
        winning_area = self.LEVELINFO['winning_area']

        self.walls = []
        for wall in walls:
            self.walls.append(pygame.draw.rect(screen, self.color,
                              wall))
        for chest in self.chest:
            chest.draw()

        for hl in self.hyperloops:
            hl.draw()
                
        self.winning_area = pygame.draw.rect(screen, BLUE, winning_area)

    def chest_collision(self, player_rect):
        for chest in self.chest:
            chest.detect(player_rect)

# a for loop is used to draw a the walls a the system 


    def hyperoop_collision(self,player_rect):
        for hl in self.hyperloops:
            collision = hl.detect(player_rect)
            if collision:
                return collision
        return None
        

    def detect_collision(self, player_rect):
        for wall in self.walls:
            if wall.colliderect(player_rect):
                return True
        return False

    def detect_win(self, player_rect):
        if self.winning_area and self.winning_area.colliderect(player_rect):
            screen.fill(BLACK)
            message_to_screen("please type in the passcode in a acending order", RED)
            pygame.display.update()
            passcode = ""
            while len(passcode)< len(self.maze_key):
                print(passcode,self.maze_key)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            return 1
                        if event.key in [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]:
                            passcode += event.unicode
            if passcode == self.maze_key:
                return 2
            else:
                return 1
        return 0

# draws the player and defines the movement 
class Player:

    def __init__(
        self,
        color,
        x,
        y,
        width,
        height,
        lifes,
        ):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.figure = self.draw()
        self.lifes = lifes

    def draw(self):
        self.figure = pygame.draw.ellipse(screen, self.color, [self.x,
                self.y, self.width, self.height], 0)

    def move(self, x_speed, y_speed):
        self.x += x_speed
        self.y += y_speed

# -- this class creates the hyperloop system(draws) and also manages the logic
# -- the draw function is called in the maze class as the orantation chages as the levels change 
class Hyperloop:

    def __init__(
        self,
        color,
        IN,
        OUT,
        width,
        height,
        ):
        self.In_coord = IN[:2]
        self.In_speed = IN[2:]
        self.Out_coord = OUT[:2]
        self.Out_speed = OUT[2:]
        self.color = color
        self.width = width
        self.height = height
        self.In_rect = None
        self.Out_rect = None

    def draw(self):
        global W
        global H
        self.In_rect = pygame.draw.rect(screen, self.color,
                self.In_coord + [self.width, self.height])
        self.Out_rect = pygame.draw.rect(screen, self.color,
                self.Out_coord + [self.width, self.height])
        self.In_coord = [(self.In_coord[0] + self.In_speed[0]) % W,
                         (self.In_coord[1] + self.In_speed[1]) % H]
        self.Out_coord = [(self.Out_coord[0] + self.Out_speed[0]) % W,
                          (self.Out_coord[1] + self.Out_speed[1]) % H]

    def detect(self, player_rect):
        if self.In_rect and self.In_rect.colliderect(player_rect): # detects player colision
            return self.Out_coord
        return None

# this class is called with the mazes to display the level and lives left 
class Game_info:

    def __init__(
        self,
        lifes,
        level,
        color,
        coord,
        ):
        self.lifes = lifes
        self.level = level
        self.color = color
        self.coord = coord

    def draw(self):
        level_text = 'Level ' + str(self.level)
        lifes_text = 'Lifes ' + str(self.lifes)
        (x, y) = self.coord
        message_to_screen(level_text, self.color, x, y)
        message_to_screen(lifes_text, self.color, x, y + 20)

## -- this function is called to display the messages for the different outcomes in the game 
def mid_game(state):
    if state == 'pass_level':
        color = WHITE
        msg = 'Level won, press P to enter the next level or Q to quit'
    elif state == 'game_over':
        color = BLACK
        msg = 'Game over,press C to play again or Q to quit'
    elif state == 'game_won':
        color = GREEN
        msg = 'Game won, TALK TO THE GAME MASTER'
    elif state == 'replay_level':
        return 'replay'
    screen.fill(color)
    message_to_screen(msg, RED)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return 'quit'
                elif event.key == pygame.K_p and state == 'pass_level':
                    return 'next_level'
                elif event.key == pygame.K_c and state == 'game_over':
                    return 'replay'


def gameLoop(level=1, lifes=3):
    global done
    global screen
    gameOver = False
    maze = Maze(WHITE,level)

    # player definitions

    player_size = max([W / 100, H / 100, 10])
    player1 = Player(
        RED,
        20,
        40,
        player_size,
        player_size,
        lifes,
        )
    game_info = Game_info(lifes, level, RED, [W - 80, 20])

    player_step = 10

    # ## -- Game Loop

    while not done:

        # -- User input and controls

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:

                # Figure out if it was an arrow key. If so
                # adjust speed.

                if event.key == pygame.K_LEFT:
                    player1.move(-player_step, 0)
                elif event.key == pygame.K_RIGHT:
                    player1.move(player_step, 0)
                elif event.key == pygame.K_UP:

                    player1.move(0, -player_step)
                elif event.key == pygame.K_DOWN:

                    player1.move(0, player_step)

        # colision detection

        collision = maze.detect_collision(player1.figure)
        if collision:
            player1.lifes -= 1
        if player1.lifes == 0:
            gameOver = True
        levelwon = maze.detect_win(player1.figure)
        a = maze.hyperoop_collision(player1.figure)
        if a:
            player1.x = a[0]
            player1.y = a[1]
        # returns the mouse position for testing 
        pos = pygame.mouse.get_pos()
        print(pos)

        if levelwon == 2:

            if level == LEVELS_COUNT:
                return 'game_won'
            else:
                return 'pass_level'
        elif levelwon == 1:
            gameOver = True

        # restart game

        if gameOver:
            return 'game_over'
        elif collision:
            return 'replay_level'

        # -- Screen background is BLACK

        screen.fill(BLACK)

        # -- Draw here

        maze.draw()
        player1.draw()
        game_info.draw()
        maze.chest_collision(player1.figure)

        # hyperloop1.draw()
        # -- flip display to reveal new position of objects

        pygame.display.flip()

        # - The clock ticks over

        clock.tick(60)

        # End While - End of game loop

    pygame.quit()


def game_control():
    level = 1
    lifes = 3
    result = gameLoop()
    action = mid_game(result)
    while action != 'quit':
        if action == 'next_level':
            level += 1

            # lifes = 3

        if action == 'replay':
            lifes -= 1
        if lifes == 0:
            lifes = 3
        result = gameLoop(level, lifes)
        action = mid_game(result)
    pygame.quit()

game_control()  
