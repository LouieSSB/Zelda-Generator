import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random

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

class Enemy():
    def __init__(self, x, y, type, room):
        self.x = x
        self.y = y
        #self.x = 5
        #self.y = 5
        self.type = type
        self.sprite = None
        if self.type == STALFOS:
            self.sprite = arcade.Sprite("stalfos_01.png")
        elif self.type == DARKNUT:
            self.sprite = arcade.Sprite("darknut_01.png")
        
        self.path = []
        
        self.room = room
        self.timer = 0

        self.sprite.left = (x)*TILE
        self.sprite.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE

    def move(self):
        self.timer += 1
        if self.timer >= 60:
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

        self.sprite.left = (self.x)*TILE
        self.sprite.bottom = SCREEN_HEIGHT -(5*TILE) - self.y*TILE

        return
    
    def validMove(self, x, y):
        newX = self.x + x
        newY = self.y + y
        if newX < 15 and newX > 0 and newY < 10 and newY > 1:
            if self.room.map[newY][newX] == 0:
                return True

        return False