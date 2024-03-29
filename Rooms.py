### IMPORTS ###
import math
import random
import arcade
import numpy as np
import copy
import enemy as enemy

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
STALFOS = 0
DARKNUT = 1

### ROOM ###
class Room:
    def __init__(self, location):
        ### INIT ###
        self.background = None
        self.wallList = None
        self.floor = None
        self.doors = None
        self.rupees = None
        self.triforce = None
        self.enemies = []
        self.enemySprites = None
        self.distance = 0

        self.quadrant = 0

        self.location = location
        self.x = location[0]
        self.y = location[1]
        self.neighbours = []

        ### FILLED TILES ###
        self.filled = np.full([MAP_WIDTH, MAP_HEIGHT], False)

        ### CONNECTIONS ###
        self.north = None
        self.south = None
        self.east = None
        self.west = None

        ### FINAL ROOM ###
        self.final = False

        ### CHECKED NEIGHBOURS ###
        self.checkedDoors = np.full((4), True, dtype=bool)

        ### IF VISITED ###
        self.visited = False

        

    ### ADD NEIGHBOURS ###
    def addNeighbour(self, b, direction):
        ### Add b as a neighbour to a ###
        if direction == NORTH:
            self.north = b
            self.checkedDoors[0] = False
        elif direction == SOUTH:
            self.south = b
            self.checkedDoors[1] = False
        elif direction == EAST:
            self.east = b
            self.checkedDoors[2] = False
        elif direction == WEST:
            self.west = b
            self.checkedDoors[3] = False
        self.neighbours.append(b)
    
    ### ROOM LAYOUT ###
    def setTemplate(self, i):
        self.map = copy.deepcopy(TEMPLATES[i])
        
### CONSTRUCT ROOM ###
def makeRoom(room, rupee_density, enemy_density):
    ### SPRITE LISTS ###
    room.wallList = arcade.SpriteList()
    room.floor = arcade.SpriteList()
    room.doors = arcade.SpriteList()
    room.rupees = arcade.SpriteList()
    room.triforce = arcade.SpriteList()
    room.enemySprites = arcade.SpriteList()

    ### CONSTRUCT FINAL ROOM ###
    makeTriforce(room)

    ### CUT OUR DOORS ###
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

    ### ADD TILES ###
    for x in range (MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if room.map[y][x] == 1:
                wall = arcade.Sprite("graphics/block_01.png")
                wall.left = x*TILE
                wall.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE
                room.wallList.append(wall)
            elif room.map[y][x] == 0:
                floor = arcade.Sprite("graphics/floor_01.png")
                floor.left = x*TILE
                floor.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE
                room.floor.append(floor)
            elif room.map[y][x] == 2:
                door = arcade.Sprite("graphics/floor_02.png")
                door.left = x*TILE
                door.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE
                room.doors.append(door)

    ### ADD RUPEES ###
    for x in range (MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if room.map[y][x] == 0:
                temp = random.random()
                if temp <= rupee_density:
                    rupee = arcade.Sprite("graphics/rupee_01.png")
                    rupee.left = x*TILE + TILE/4
                    rupee.bottom = SCREEN_HEIGHT -(5*TILE) - y*TILE
                    room.rupees.append(rupee)
                    room.filled[x,y] = True
    
    ### ADD ENEMIES ###
    for x in range (MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            if room.map[y][x] == 0 and room.filled[x,y] == False:
                num = random.random()
                if enemy_density >= num:
                    foe = enemy.Enemy(x,y, STALFOS, room)
                    room.enemies.append(foe)
                    room.enemySprites.append(foe.sprite)

    return room

### CREATE FINAL ROOM ###
def makeTriforce(room):
    ### ADD TRIFORCE ###
    if room.map == TEMPLATES[TRIFORCE]:
        triforce = arcade.Sprite("graphics/triforce_01.png")
        triforce.left = 7*TILE + 22
        triforce.bottom = SCREEN_HEIGHT -(5*TILE) - 4*TILE
        room.triforce.append(triforce)

### PAIR ROOMS ###
def pairRooms(a, b, direction):
    a.addNeighbour(b, direction)
    b.addNeighbour(a, -direction)


### TEMPLATE CONSTANTS ###
EMPTY = 0
TWINS = 1
DIAMOND = 2
LATTICE = 3
CROSSROADS = 4
MAGNET = 5
EYEBALL = 6
DIAGONAL = 7
SPIRAL = 8
BIGMAC = 9
RINGROAD = 10
SNAKE = 11
MESS = 12
TRIFORCE = 13

### TEMPLATE LAYOUTS ###
TEMPLATES = []
for i in range(TRIFORCE + 1):
    TEMPLATES.append(0)
TEMPLATES[EMPTY] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[TWINS] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1],
            [1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1],
            [1,1,0,0,1,1,0,0,0,0,1,1,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[DIAMOND] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1],
            [1,1,0,0,0,1,1,1,1,1,1,0,0,0,1,1],
            [1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[LATTICE] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,0,1,0,1,1,0,1,0,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[CROSSROADS] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[MAGNET] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[EYEBALL] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,0,0,0,0,1,1,1,0,1,1],
            [1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1],
            [1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,1,1,1,0,0,0,0,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[DIAGONAL] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,1,0,0,0,0,0,0,0,0,1,1,1],
            [1,1,0,1,0,0,0,1,0,0,0,0,1,0,1,1],
            [1,1,0,0,0,0,1,0,0,0,0,1,0,0,1,1],
            [1,1,0,0,0,1,0,0,0,0,1,0,0,0,1,1],
            [1,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1],
            [1,1,0,1,0,0,0,0,1,0,0,0,1,0,1,1],
            [1,1,1,0,0,0,0,0,0,0,0,1,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[SPIRAL] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,0,1,0,1,1],
            [1,1,0,1,0,0,0,0,0,0,1,0,1,0,1,1],
            [1,1,0,1,0,0,0,1,1,1,1,0,1,0,1,1],
            [1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[TRIFORCE] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,1,0,0,1,0,0,1,0,0,1,0,1,1],
            [1,1,0,1,0,1,0,0,0,0,1,0,1,0,1,1],
            [1,1,0,1,0,0,0,0,0,0,0,0,1,0,1,1],
            [1,1,0,1,1,1,1,0,0,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[BIGMAC] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[RINGROAD] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[SNAKE] = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1],
            [1,1,1,0,0,0,1,0,0,0,0,1,0,1,1,1],
            [1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,1],
            [1,1,0,0,1,0,1,0,0,1,0,1,0,0,1,1],
            [1,1,1,0,1,0,1,1,0,1,0,1,0,1,1,1],
            [1,1,1,0,1,0,0,0,0,1,0,0,0,1,1,1],
            [1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        ]
TEMPLATES[MESS] = [
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
