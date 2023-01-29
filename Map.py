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

class Map():
    def __init__(self, x, y):
        self.rooms = np.empty([x,y], rooms.Room)

    def makeMinimap(self):
        for i in range (5):
            for (j) in range(5):
                if self.rooms[i,j] != None:
                    maptile = arcade.Sprite("room_01.png")
                    maptile.left = i*(TILE/2) + 100
                    maptile.bottom = 13*TILE + (8*j) - 8
                    self.mapList.append(maptile)
