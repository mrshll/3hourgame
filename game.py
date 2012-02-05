import sys
import random
import math
import os
import getopt
import pygame
from socket import *


class Cursor:

    img = pygame.image.load("data/cursor.png")
    rect = img.get_rect()
    grid_x = 0
    grid_y = 0

    def draw(self, visible):
        if visible:
            screen.blit(self.img, [self.grid_x * grid_size, self.grid_y * grid_size])

    def update(self, d_x, d_y):
        if self.grid_x <= 0 and d_x < 0:
            self.grid_x = num_grids_h-1
        elif self.grid_x >= num_grids_h-1 and d_x > 0:
            self.grid_x = 0
        elif self.grid_y <= 0 and d_y < 0:
            self.grid_y = num_grids_v-1
        elif self.grid_y >= num_grids_v and d_y > 0:
            self.grid_y = 0
        else:
            self.grid_x += d_x
            self.grid_y += d_y

class Team:

    def build_lab(self, x, y):
        if self.money >= 150:
            self.money -= 150
            self.buildings['labs'].append(Lab(self.id, x, y))
            print(self.money)

    def build_factory(self, x, y):
        if self.money >= 150:
            self.money -= 150
            self.buildings['factories'].append(Factory(self.id, x, y))
            print(self.money)

    def train_unit(self, x, y):
        if self.money >= 100:
            self.money -= 100
            self.units.append("")

    def __init__(self, id):
        self.id = id
        self.money = 1000
        self.buildings=dict({'base':Base(self.id),'factories':[],'labs':[]})
        self.units=[]


class Base:

    used = False

    def __init__(self, team_id):
        self.type = 'base'
        self.team_id = team_id
        self.img = pygame.image.load("data/base_" + str(self.team_id) + ".png")
        if self.team_id == 1:
            self.grid_x = num_grids_h - 1
            self.grid_y = 0
        else:
            self.grid_x = 0
            self.grid_y = num_grids_v - 1

    def draw(self, visible):
        if visible:
            screen.blit(self.img, [self.grid_x * grid_size, self.grid_y * grid_size])

class Lab(Base):

    used = False

    def __init__(self, team_id, g_x, g_y):
        self.type = 'lab'
        self.team_id = team_id
        self.img = pygame.image.load("data/lab_" + str(self.team_id) + ".png")
        self.grid_x = g_x
        self.grid_y = g_y

class Factory(Base):

    used = False

    def __init__(self, team_id, g_x, g_y):
        self.type = 'factory'
        self.team_id = team_id
        self.img = pygame.image.load("data/factory_" + str(self.team_id) + ".png")
        self.grid_x = g_x
        self.grid_y = g_y


def draw_board(num_grids_h, num_grids_v):
    for i in range(num_grids_h):
        for j in range(num_grids_v):
            screen.blit(bg_img, (i * grid_size, j * grid_size))
            if grid[i][j]['flag'] is True:
                screen.blit(flag_img, (i * grid_size, j * grid_size - grid_size/2))

def draw_menu():
    font = pygame.font.SysFont("Courier New", 40)
    height_sum = 200
    text=["Action Menu"]
    for x in range (max(0,c.grid_x-1),min(num_grids_h,c.grid_x+2)):
        for y in range (max(0,c.grid_y-1),min(num_grids_v,c.grid_y+2)):
            if grid[x][y]['base']:
                text.append("Build Factory")
                text.append("Build Lab")
            elif grid[x][y]['unit']:
                text.append("Attack")
            elif grid[x][y]['lab']:
                text.append("Build Unit")
    text.append("Cancel")
    for i in range(len(text)):
        t = str(i) + ". " + text[i]
        screen.blit(font.render(t, 0, (0,0,255), (200,200,200)),
            (width/2-font.size(t)[0]/2,height_sum))
        height_sum+=font.get_linesize()

def update_grid():
    for row in grid:
        for c in row:
            c['base']=False
            c['factory']=False
            c['lab']=False
            c['unit']=False
    for p in Players:
        grid[p.buildings['base'].grid_x][p.buildings['base'].grid_y]['base']=True
        for f in p.buildings['factories']:
            grid[f.grid_x][f.grid_y][f.type]=True
        for l in p.buildings['labs']:
            grid[f.grid_x][f.grid_y][f.type]=True

pygame.init()
size = width, height = 840, 840
grid_size = 40
num_grids_h = width / grid_size
num_grids_v = height / grid_size

bg_img = pygame.image.load("data/grass_3.png")
flag_img = pygame.image.load("data/flag_3.png")

grid = []
flag_position = random.randint(3, 6), random.randint(3, 6)
# initialize grid
for i in range(num_grids_h):
    grid.append([])
    for j in range(num_grids_v):
        flag = False
        if i == num_grids_h / 2 + flag_position[0] and j == num_grids_v / 2 + flag_position[1]:
            flag = True
        if i == num_grids_h / 2 - flag_position[0] and j == num_grids_v / 2 - flag_position[1]:
            flag = True
        if i == num_grids_h / 2  and j == num_grids_v / 2 :
            flag = True
        grid[i].append(dict({'base': False, 'factory': False, 'lab':False, 'unit': False, 'flag': flag}))

screen = pygame.display.set_mode(size)

c = Cursor()
Players = [Team(1), Team(2)]

turn_keeper = 1
done = False
menu_disp = False

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        elif event.type == KEYDOWN:
            if event.key == K_UP:
                menu_disp = False
                c.update(0, -1)
            elif event.key == K_DOWN:
                menu_disp = False
                c.update(0, 1)
            elif event.key == K_RIGHT:
                menu_disp = False
                c.update(1, 0)
            elif event.key == K_LEFT:
                menu_disp = False
                c.update(-1, 0)
            elif event.key == K_SPACE:
                menu_disp = True
            elif event.key == K_1 and menu_disp and ~Players[turn_keeper].buildings['base'].used:
                for x in range (max(0,c.grid_x-1),min(num_grids_h,c.grid_x+2)):
                    for y in range (max(0,c.grid_y-1),min(num_grids_v,c.grid_y+2)):
                        if grid[x][y]['base']:
                            Players[turn_keeper].build_factory(c.grid_x,c.grid_y)
                            Players[turn_keeper].buildings['base'].used=True
                menu_disp=False

            elif event.key == K_RETURN:
                done=True


        update_grid()

        draw_board(num_grids_h, num_grids_v)
        c.draw(True)
        for p in Players:
            p.buildings['base'].draw(True)
            for f in p.buildings['factories']:
                f.draw(True)
            for l in p.buildings['labs']:
                l.draw(True)
        if menu_disp:
            draw_menu()
        pygame.display.flip()

        if done and turn_keeper is 1:
            turn_keeper = 2
            done = False
        if done and turn_keeper is 2:
            turn_keeper = 1
            done = False

