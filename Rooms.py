import math
import random
import arcade
import numpy as np

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 480
TILE = 32
MAP_WIDTH = 16
MAP_HEIGHT = 11
NORTH = 1
SOUTH = -1
EAST = 2
WEST = -2

class Room:
    def __init__(self, location):
        # You may want many lists. Lists for coins, monsters, etc.
        self.wallList = None
        self.floor = None
        self.doors = None
        self.map = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,1,1,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,0,1,0,0,0,1,1],
            [1,1,0,0,0,1,1,1,1,0,1,0,1,1,1,1],
            [1,1,0,1,1,1,1,1,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]

        self.location = location
        #self.neighbours = np.empty([4], Room)
        self.neighbours = []

        self.north = None
        self.south = None
        self.east = None
        self.west = None

        self.checkedDoors = np.full((4), True, dtype=bool)

        # This holds the background images. If you don't want changing
        # background images, you can delete this part.
        self.background = None

    ### Add b as a neighbour to a ###
    def addNeighbour(self, b, direction):
        if direction == NORTH:
            self.north = b
            self.checkedDoors[0] = False
            #self.neighbours[0] = b
        elif direction == SOUTH:
            self.south = b
            self.checkedDoors[1] = False
            #self.neighbours[1] = b
        elif direction == EAST:
            self.east = b
            self.checkedDoors[2] = False
            #self.neighbours[2] = b
        elif direction == WEST:
            self.west = b
            self.checkedDoors[3] = False
            #self.neighbours[3] = b
        self.neighbours.append(b)
        

def makeRoom(room):
    
    room.wallList = arcade.SpriteList()
    room.floor = arcade.SpriteList()
    room.doors = arcade.SpriteList()

    ### Cut out the walls ###
    if room.north != None:
        room.map[0][8] = 2
        room.map[1][8] = 0
        room.map[0][7] = 2
        room.map[1][7] = 0
    if room.south != None:
        room.map[9][8] = 0
        room.map[10][8] = 2
        room.map[9][7] = 0
        room.map[10][7] = 2
    if room.west != None:
        room.map[5][0] = 2
        room.map[5][1] = 0
    if room.east != None:
        room.map[5][15] = 2
        room.map[5][14] = 0

    ### Add Sprites ###
    for x in range (MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if room.map[y][x] == 1:
                wall = arcade.Sprite("block_01.png")
                wall.left = x*TILE
                wall.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE
                room.wallList.append(wall)
            elif room.map[y][x] == 0:
                floor = arcade.Sprite("floor_01.png")
                floor.left = x*TILE
                floor.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE
                room.floor.append(floor)
            elif room.map[y][x] == 2:
                door = arcade.Sprite("floor_02.png")
                door.left = x*TILE
                door.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE
                room.doors.append(door)


    return room

def pairRooms(a, b, direction):
    a.addNeighbour(b, direction)
    b.addNeighbour(a, -direction)