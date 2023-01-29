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

class Player():
    def __init__(self, x, y, sprite, current_room):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.current_room = current_room
        self.last_room = None
        self.path = []
        self.graph = None
        self.timer = 0
        
        
    def choose(self):

        self.move()

        


        return

    def depthFirst(self, graph, start, visited=None):
        if visited is None:
            visited = []
        visited.append(start)
        #print(start)
        for next in graph[start] - visited:
            self.depthFirst(graph, next, visited)
        return visited


    def move(self):
        self.timer += 1;
        if len(self.path) > 0 and self.timer >= 1:
            self.sprite.center_x = (self.path[0].x * TILE) + 16
            self.sprite.center_y = (self.path[0].y * TILE) + 16
            self.path.pop(0)
            self.timer = 0
        if self.last_room != self.current_room:
            self.last_room = self.current_room
            self.graph = astar.makeGraph(self.current_room)
            end = None
            doors = []
            for x in range (16):
                for y in range (11):
                    if self.graph[x,y] != None and self.graph[x,y].type == DOOR:
                        if self.sprite.bottom <= TILE and y != 0: #If at bottom of screen, add everything except bottom door
                            doors.append(self.graph[x,y])
                        elif self.sprite.top >= SCREEN_HEIGHT - TILE*5 and y != 10: #If at top of screen, add everything except top door
                            doors.append(self.graph[x,y])
                        elif self.sprite.left <= TILE and x != 0: #If at left of screen, add everything except left door
                            doors.append(self.graph[x,y])
                        elif (self.sprite.right >= (SCREEN_WIDTH - TILE*2)) and x != 15: #If at right of screen, add everything except right door
                            doors.append(self.graph[x,y])

                        
                        #end = self.graph[x,y]
            if len(doors) > 0:
                #end = doors.pop()
                door = random.randint(0, len(doors)-1)
                end = doors[door]

            
            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            if end == None:
                end = start
            self.path = astar.aStar(start, end)

        return