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
TRAVERSING = 0
COLLECTING = 1
FIGHTING  = 2
FINISHING = 3
SPEED = 1

### PLAYER ###
class Player():
    ### CONSTRUCTOR ###
    def __init__(self, x, y, sprite, starting_room, map, rupee_aff, combat_aff, combat_skill, heuristic):
        ### INIT ###
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
        self.graph = None

        ### STATISTICS ###
        self.damage = 0
        self.kills = 0
        self.lastKills = 0
        self.money = 0
        self.lastmoney = 0
        self.roomsVisited = 1

        ### STATES ###
        self.state = COLLECTING
        self.last_state = None
        
        ### PARAMETERS ###
        self.rupeeAffinity = rupee_aff
        self.combatAffinity = combat_aff
        self.combatAbility = combat_skill
        self.heuristic = heuristic

        ### FRAME COUNTER ###
        self.timer = 0
        self.totaltime = 0

        ### COORDINATES ###
        self.sprite.position = ((x+0.5)*TILE, (y+0.5)*TILE)
        
    ### DECISION MAKING ###    
    def choose(self):
        ### Check if in final room first ###
        self.finish()

        ### Move using current path ###
        self.move()

        ### Collect rupees first ###
        self.gotoRupees()

        ### Then kill enemies ###
        self.killEnemies()

        ### Leave room once done ###
        self.traverse()
        return

    ### MOVE ###
    def move (self):
        ### Increment frame timer ###
        self.timer += 1
        self.totaltime += 1

        ### Take next step in path, remove from list ###
        if len(self.path) > 0 and self.timer >= SPEED:
            self.sprite.center_x = (self.path[0].x * TILE) + 16
            self.sprite.center_y = (self.path[0].y * TILE) + 16
            self.path.pop(0)
            self.timer = 0

    ### TRAVERSE ###
    def traverse(self):
        ### Check to start traversing ###
        if self.state == TRAVERSING and self.last_state == FIGHTING:
            ### Set last state so this isn't repeated ###
            self.last_state = TRAVERSING
            self.graph = astar.makeGraph(self.current_room)
            end = None

            ### FIND BEST DOOR ###
            bestDoor = 10000000
            for i in range(4):
                ### Check for unexplored options ###
                if self.current_room.checkedDoors[i] == False:
                    ### Find location of door ###
                    point = self.doorLookup(self.convertDirection(i))

                    ### Randomly select best door based on heurisitc ###
                    num = random.random()
                    if num <= self.heuristic:
                        heuristic = self.findDoorHeuristic(self.convertDirection(i))
                    else:
                        heuristic = 10000
                    if heuristic < bestDoor:
                        end = self.graph[point]
                        bestDoor = heuristic

            ### BACKTRACKING ###           
            ### If there were no unexplored doors, we must backtrack ###
            if end == None: 
                ### If nowhere to backtrack to, game is unbeatable ###
                if len(self.history) == 0:
                    print("ERROR: Triforce not found.")
                    exit()
                
                ### Get last movement ###
                direction = self.history.pop()
                ### Signifies that backtracking has happened ###
                self.history.append(0) 
                ### Do reverse of previous movement ###
                point = self.doorLookup(-direction)
                end = self.graph[point]
        
            ### CALCULATE PATH ###
            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            if end == None:
                end = start
            self.path = astar.aStar(start, end)

        return
    
    ### CHOOSE RUPEES ###
    def findRupees(self):
        for rupee in self.current_room.rupees:
            num = random.random()
            ### Choose which rupees to collect based on parameter ###
            if num <= self.rupeeAffinity:
                self.rupeeTargets.append(rupee)  
        return
    
    ### COLLECT RUPEES ###
    def gotoRupees(self):
        ### INITIALISE ###
        if self.last_room != self.current_room:
            ### When entering room, set state to collecting ###
            self.last_room = self.current_room
            self.state = COLLECTING
            ### Make graph, find rupees, and choose which to collect ###
            self.graph = astar.makeGraph(self.current_room)
            self.findRupees()
            self.rupee = self.selectRupee()
        
        ### DONE COLLECTING ###
        if self.state != COLLECTING:
            return
        
        ### START COLLECTING ###
        if len(self.rupeeTargets) > 0:
            ### Check for collection by money count ###
            if self.money != self.lastmoney:
                self.lastmoney = self.money
                ### Select a new rupee ###
                self.rupee = self.selectRupee()

            ### Generate path to rupee ###
            self.graph = astar.makeGraph(self.current_room)
            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            endX = int((self.rupee.center_x - 16) / TILE)
            endY = int((self.rupee.center_y - 16) / TILE)
            end = self.graph[endX, endY]
            self.path = astar.aStar(start, end)

        else:
            ### If all are collected, move to next phase ###
            self.state = FIGHTING
            self.last_state = COLLECTING

        return
    
    ### TARGET RUPEE ###
    def selectRupee(self):
        lowest = 100000
        best = None
        ### Find rupee closest to Link ###
        for rupee in self.rupeeTargets:
            ### Add random modifier to avoid infinite loops ###
            dist = self.manhattan(self.sprite.position, rupee.position) + (random.randint(0, 2))/2
            if dist <= lowest:
                lowest = dist
                best = rupee
        return best

    ### FINISH CHECK ###
    def finish(self):
        ### Check if in triforce room ###
        if len(self.current_room.triforce) > 0 and self.state != FINISHING:
            ### Calculate path to triforce ###
            self.state = FINISHING
            self.graph = astar.makeGraph(self.current_room)
            self.x = int((self.sprite.center_x - 16)/TILE)
            self.y = int((self.sprite.center_y - 16)/TILE)
            start = self.graph[self.x, self.y]
            endX = 7
            endY = 6
            end = self.graph[endX, endY]
            self.path = astar.aStar(start, end)

    ### FIGHT ENEMIES ###
    def killEnemies(self):
        ### Set state, find enemies ###
        if self.state == FIGHTING and self.last_state == COLLECTING:
            self.last_state = FIGHTING
            self.graph = astar.makeGraph(self.current_room)
            self.findEnemies()
            self.foe = self.selectEnemy()
        ### Return when done ###
        if self.state != FIGHTING:
            return
        
        ### Start fighting enemies ###
        if len(self.enemyTargets) > 0:
            ### Find new enemy based on kill count ###
            if self.kills != self.lastKills:
                self.lastKills = self.kills
                self.foe = self.selectEnemy()

            ### FIND PATH ###
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
            ### Move to next phase ###
            self.state = TRAVERSING
            self.last_state = FIGHTING

        return

    ### FIND ENEMIES ###
    def findEnemies(self):
        ### Choose which enemies to fight based on parameters ###
        for foe in self.current_room.enemySprites:
            num = random.random()
            if num <= self.combatAffinity:
                self.enemyTargets.append(foe)
        return
    
    ### SELECT ENEMY
    def selectEnemy(self):
        lowest = 100000
        best = None
        ### Target enemy closest to Link ###
        for foe in self.enemyTargets:
            dist = self.manhattan(self.sprite.position, foe.position) + (random.randint(0, 2))/2
            if dist <= lowest:
                lowest = dist
                best = foe
        return best

    ### MANHATTAN DISTANCE ###
    def manhattan(self, a, b):
        return sum(abs(val1-val2) for val1, val2 in zip(a,b))


    ### DOOR LOCATIONS ###
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

    ### INDEX -> DIRECTION ###
    def convertDirection(self, i):
        if i == 0:
            return NORTH
        elif i == 1:
            return SOUTH
        elif i == 2:
            return EAST
        elif i == 3:
            return WEST
        
    ### FIND BEST DOOR ###
    def findDoorHeuristic(self, direction):
        room = None
        x = self.current_room.x
        y = self.current_room.y

        ### Find the room the door leads to ###
        if direction == NORTH:
            room = self.map.rooms[x, y+1]
        if direction == SOUTH:
            room = self.map.rooms[x, y-1]
        if direction == EAST:
            room = self.map.rooms[x+1, y]
        if direction == WEST:
            room = self.map.rooms[x-1, y]
        
        ### Calulate how close this room is to goal ###
        return sum(abs(val1-val2) for val1, val2 in zip(room.location, self.map.goal.location))
