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
TRAVERSING = 0
COLLECTING = 1
FIGHTING  = 2
FINISHING = 3
SPEED = 1

class Player():
    def __init__(self, x, y, sprite, starting_room, map):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.starting_room = starting_room
        self.current_room = starting_room
        self.last_room = None
        self.map = map
        self.path = []
        self.history = []
        self.rupeeTargets = arcade.SpriteList()
        self.enemyTargets = arcade.SpriteList()
        self.rupee = None
        self.foe = None

        self.damage = 0
        self.kills = 0
        self.lastKills = 0
        self.money = 0
        self.lastmoney = 0

        self.state = COLLECTING
        self.last_state = None
        
        
        self.graph = None
        self.timer = 0
        self.rupeeAffinity = 0.1
        self.combatAffinity = 1.0
        self.combatAbility = 0.9

        self.sprite.position = ((x+0.5)*TILE, (y+0.5)*TILE)
        
        
    def choose(self):

        self.finish()
        self.move()  
        self.gotoRupees()
        self.killEnemies()
        self.traverse()
        print(len(self.enemyTargets))

        return

    def move (self):
        self.timer += 1
        if len(self.path) > 0 and self.timer >= SPEED:
            self.sprite.center_x = (self.path[0].x * TILE) + 16
            self.sprite.center_y = (self.path[0].y * TILE) + 16
            self.path.pop(0)
            self.timer = 0

    def traverse(self):
        if self.state == TRAVERSING and self.last_state == FIGHTING:
            self.last_state = TRAVERSING
            self.graph = astar.makeGraph(self.current_room)
            end = None
            for i in range(4):
                if self.current_room.checkedDoors[i] == False:
                    point = self.doorLookup(self.convertDirection(i))
                    end = self.graph[point]

            ### BACKTRACKING ###
            if end == None: 
                if len(self.history) == 0:
                    print("ERROR: Triforce not found.")
                    exit()
                direction = self.history.pop()
                self.history.append(0) #Signifies that backtracking has happened
                point = self.doorLookup(-direction)
                end = self.graph[point]
        

            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            if end == None:
                end = start
            self.path = astar.aStar(start, end)
        

        return
    def findRupees(self):
        for rupee in self.current_room.rupees:
            num = random.random()
            if num <= self.rupeeAffinity:
                self.rupeeTargets.append(rupee)  
        return
    def gotoRupees(self):
        
        if self.last_room != self.current_room:
            self.last_room = self.current_room
            self.state = COLLECTING
            self.graph = astar.makeGraph(self.current_room)
            self.findRupees()
            self.rupee = self.selectRupee()
        if self.state != COLLECTING:
            return
        if len(self.rupeeTargets) > 0:
            if self.money != self.lastmoney:
                self.lastmoney = self.money
                self.rupee = self.selectRupee()

            self.graph = astar.makeGraph(self.current_room)
            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            endX = int((self.rupee.center_x - 16) / TILE)
            endY = int((self.rupee.center_y - 16) / TILE)
            end = self.graph[endX, endY]
            self.path = astar.aStar(start, end)

        else:
            self.state = FIGHTING
            self.last_state = COLLECTING

        return
    
    def selectRupee(self):
        lowest = 100000
        best = None
        for rupee in self.rupeeTargets:
            dist = self.manhattan(self.sprite.position, rupee.position) + (random.randint(0, 2))/2
            if dist <= lowest:
                lowest = dist
                best = rupee
        return best

    def finish(self):
        if len(self.current_room.triforce) > 0 and self.state != FINISHING:
            self.state = FINISHING
            self.graph = astar.makeGraph(self.current_room)
            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            endX = 7
            endY = 6
            end = self.graph[endX, endY]
            self.path = astar.aStar(start, end)

    def killEnemies(self):
        if self.state == FIGHTING and self.last_state == COLLECTING:
            self.last_state = FIGHTING
            self.graph = astar.makeGraph(self.current_room)
            self.findEnemies()
            self.foe = self.selectEnemy()
        if self.state != FIGHTING:
            return
        if len(self.enemyTargets) > 0:
            if self.kills != self.lastKills:
                self.lastKills = self.kills
                self.foe = self.selectEnemy()

            
            self.graph = astar.makeGraph(self.current_room)
            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            endX = int((self.foe.center_x - 14) / TILE)
            endY = int((self.foe.center_y - 16) / TILE)
            end = self.graph[endX, endY]
            if end == None:
                print("?")
                return
            self.path = astar.aStar(start, end)

        else:
            self.state = TRAVERSING
            self.last_state = FIGHTING

        return

    def findEnemies(self):
        for foe in self.current_room.enemySprites:
            num = random.random()
            if num <= self.combatAffinity:
                self.enemyTargets.append(foe)
                print("ADD")
        return
    
    def selectEnemy(self):
        lowest = 100000
        best = None
        for foe in self.enemyTargets:
            dist = self.manhattan(self.sprite.position, foe.position) + (random.randint(0, 2))/2
            if dist <= lowest:
                lowest = dist
                best = foe
        return best


    def manhattan(self, a, b):
        return sum(abs(val1-val2) for val1, val2 in zip(a,b))



    def doorLookup(self, i):
        ### NORTH ###
        if i == NORTH:
            return (7, 10)
        ### SOUTH ###
        elif i == SOUTH:
            return(7, 0)
        ### EAST ###
        elif i == EAST:
            return(15, 5)
        ### WEST ###
        elif i == WEST:
            return(0, 5)

    def convertDirection(self, i):
        if i == 0:
            return NORTH
        elif i == 1:
            return SOUTH
        elif i == 2:
            return EAST
        elif i == 3:
            return WEST