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
RUPEE_DENSITY = 0.0

class Map():
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.rooms = np.empty([width, height], rooms.Room)
        self.goal = None
        for x in range(width):
            for y in range(height):
                self.rooms[x,y] = rooms.Room((x,y))
        self.visited = np.full([width,height], False, dtype=bool)
        self.tilelist = arcade.SpriteList()

        self.generateMaze()
        highest = 0
        for i in range (width):
            for j in range(height):
                if self.rooms[i,j].distance >= highest:
                    self.goal = self.rooms[i,j]
                    highest = self.rooms[i,j].distance
        for i in range (width):
            for j in range(height):
                if self.rooms[i,j] == self.goal:
                    self.goal.setTemplate(13)
                    rooms.makeRoom(self.rooms[i,j], 0)
                else:
                    temp = random.randint(0, 12)
                    self.rooms[i,j].setTemplate(temp)
                    rooms.makeRoom(self.rooms[i,j], RUPEE_DENSITY)
                
                
        self.makeMinimap()

    


    def generateMaze(self):
        x = random.randrange(0, self.width)
        y = random.randrange(0,self.height)
        stack = []
        x = 0
        y = 0

        room = self.rooms[x,y]
        room.distance = 0
        stack.append(room)
        self.visited[room.location] = True
        
        while len(stack) > 0:

            neighbours = self.getAvNeighbours(room.location[0], room.location[1])
            while len(neighbours) == 0 and len(stack) > 0:
                room = stack.pop()
                neighbours = self.getAvNeighbours(room.location[0], room.location[1])
            if len(neighbours) == 0:
                break


            if len(neighbours) > 0:
                stack.append(room)
                next = neighbours[random.randrange(0, len(neighbours))]
            

            diff = tuple(map(lambda i, j: i - j, next.location, room.location))
            if diff == (0,1):
                rooms.pairRooms(room, next, NORTH)
            elif diff == (0,-1):
                rooms.pairRooms(room, next, SOUTH)
            elif diff == (1,0):
                rooms.pairRooms(room, next, EAST)
            elif diff == (-1,0):
                rooms.pairRooms(room, next, WEST)
                
            next.distance = room.distance + 1
            room = next
            
            self.goal = room
            
            if self.visited[room.location] == False or 1 == 1:
                stack.append(room)
                self.visited[room.location] = True
                

        
        return
    def makeMinimap(self):
        for i in range (self.width):
            for (j) in range(self.height):
                if self.rooms[i,j] != None:
                    maptile = arcade.Sprite("room_01.png")
                    maptile.left = i*(TILE/2) + 100
                    maptile.bottom = 13*TILE + (8*j) - 8
                    self.tilelist.append(maptile)


    def getNeighbours(self, x, y):
        neighbours = []
        if (x - 1) >= 0:
            neighbours.append(self.rooms[x-1, y])
        if (x + 1) <= self.width - 1:
            neighbours.append(self.rooms[x+1, y])
        if (y - 1) >= 0:
            neighbours.append(self.rooms[x, y-1])
        if (y + 1) <= self.height - 1:
            neighbours.append(self.rooms[x, y+1])
    

        return neighbours
    
    def getAvNeighbours(self,x,y):
        neighbours = self.getNeighbours(x,y)
        options = []
        for neighbour in neighbours:
            if self.visited[neighbour.location] == False:
                options.append(neighbour)
        
        return options

    
