### IMPORTS ###
import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random

### CONSTANTS ###
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 480
TILE = 32
MAP_WIDTH = 16
MAP_HEIGHT = 11
NORTH = 1
SOUTH = -1
EAST = 2
WEST = -2
FLOOR = 0
WALL = 1
DOOR = 2
SPEED = 1
STALFOS = 0
DARKNUT = 1

### ENEMY ###
class Enemy():
    def __init__(self, x, y, type, room):
        ### INIT ###
        self.x = x
        self.y = y
        self.room = room
        self.timer = 0
        
        ### SPRITE ###
        self.type = type
        self.sprite = None
        if self.type == STALFOS:
            self.sprite = arcade.Sprite("graphics/stalfos_01.png")
        elif self.type == DARKNUT:
            self.sprite = arcade.Sprite("graphics/darknut_01.png")
        
        ### LOCATION ###
        self.sprite.left = (x)*TILE
        self.sprite.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE

    def move(self):
        ### MOVE TIMER ##
        self.timer += 1
        
        ### RANDOM MOVEMENT ###
        if self.timer >= 5:
            num = random.randrange(0,4)
            if num == 0:
                if self.validMove(0, 1):
                    self.y += 1
            if num == 1:
                if self.validMove(0, -1):
                    self.y -= 1
            if num == 2:
                if self.validMove(1, 0):
                    self.x += 1
            if num == 3:
                if self.validMove(-1, 0):
                    self.x -= 1
            self.timer = 0

        ### RECALCULATE POSITION ###
        self.sprite.left = (self.x)*TILE
        self.sprite.bottom = SCREEN_HEIGHT -(5*TILE) - self.y*TILE

        return
    
    def validMove(self, x, y):
        ### COLLISION DETECTION ###
        newX = self.x + x
        newY = self.y + y
        if newX < 15 and newX > 0 and newY < 10 and newY > 1:
            if self.room.map[newY][newX] == 0:
                return True

        return False