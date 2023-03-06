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
RUPEE_DENSITY = 0.5
ENEMY_DENSITY = 0.1

class Map():
    def __init__(self, width, height, extraDoors, rupeeDensity, enemyDensity):
        self.height = height
        self.width = width
        self.rooms = np.empty([width, height], rooms.Room)
        
        self.quadrants = [[],[],[],[]]
        self.extraDoors = extraDoors #List that is 4 items long, one for each quadrant
        self.rupeeDensity = rupeeDensity
        self.enemyDensity = enemyDensity #Also list of numbers for each quadrant

        self.goal = None # Triforce room
        ### Create map array ###
        for x in range(width):
            for y in range(height):
                self.rooms[x,y] = rooms.Room((x,y))
                
        ### Map of which rooms have been visited for maze generation ###
        self.visited = np.full([width,height], False, dtype=bool)
        self.tilelist = arcade.SpriteList() # Sprite list for minimap

        ### Depth-first maze generation ###
        self.generateMaze()

        self.makeQuadrants()
        

        ### Locate room furthest from start ###
        highest = 0
        for i in range (width):
            for j in range(height):
                if self.rooms[i,j].distance >= highest:
                    self.goal = self.rooms[i,j]
                    highest = self.rooms[i,j].distance
        self.goal.final = True
        self.addDoors()
        
        ### Sets templates for each room, and builds their tiles ###
        for i in range (width):
            for j in range(height):
                if self.rooms[i,j] == self.goal: #Triforce room gets its own layout
                    self.goal.setTemplate(13)
                    rooms.makeRoom(self.rooms[i,j], 0, 0) #Room has no enemies or money
                else:
                    temp = random.randint(0, 12) #All other rooms are chosen randomly
                    self.rooms[i,j].setTemplate(temp)
                    rooms.makeRoom(self.rooms[i,j], self.rupeeDensity[self.rooms[i,j].quadrant], self.enemyDensity[self.rooms[i,j].quadrant])
                
        
        ### Make minimap based on map size ###   
        self.makeMinimap()

    

    ### MAZE GENERATOR ###
    def generateMaze(self):
        stack = [] #Stack for depth-first generation
        ### Starting co-ordinates ###
        x = 0
        y = 0

        ### Starting room, mark as visited ###
        room = self.rooms[x,y]
        room.distance = 0
        stack.append(room)
        self.visited[room.location] = True
        
        ### When stack is empty, every room has been visited ###
        while len(stack) > 0:
            neighbours = self.getAvNeighbours(room.location[0], room.location[1])
            ### Revisit each room in stack to look for unexplored neighbours ###
            while len(neighbours) == 0 and len(stack) > 0:
                room = stack.pop()
                neighbours = self.getAvNeighbours(room.location[0], room.location[1])
            if len(neighbours) == 0:
                break

            ### Choose a random neighbour to room to explore next ###
            if len(neighbours) > 0:
                stack.append(room)
                next = neighbours[random.randrange(0, len(neighbours))]
            
            ### Figures out the orientation of the 2 rooms from each other ###
            diff = tuple(map(lambda i, j: i - j, next.location, room.location))
            if diff == (0,1):
                rooms.pairRooms(room, next, NORTH)
            elif diff == (0,-1):
                rooms.pairRooms(room, next, SOUTH)
            elif diff == (1,0):
                rooms.pairRooms(room, next, EAST)
            elif diff == (-1,0):
                rooms.pairRooms(room, next, WEST)
                
            ### Each room is further from than the start than its parent ###
            next.distance = room.distance + 1
            room = next
            
            ### Room put on stack so that its neighbours can be checked again later ###
            stack.append(room)
            self.visited[room.location] = True
                
    ### MINIMAP GENERATION ###
    def makeMinimap(self):
        for i in range (self.width):
            for (j) in range(self.height):
                if self.rooms[i,j] != None:
                    maptile = arcade.Sprite("room_01.png") # Blue rectangle graphic
                    maptile.left = i*(TILE/2) + 100
                    maptile.bottom = 13*TILE + (8*j) - 8
                    self.tilelist.append(maptile)

    ### GET NEIGHBOURS FOR GENERATION ###
    def getNeighbours(self, x, y):
        neighbours = []
        ### Checks neighbours in each direction, add to list ###
        if (x - 1) >= 0:
            neighbours.append(self.rooms[x-1, y])
        if (x + 1) <= self.width - 1:
            neighbours.append(self.rooms[x+1, y])
        if (y - 1) >= 0:
            neighbours.append(self.rooms[x, y-1])
        if (y + 1) <= self.height - 1:
            neighbours.append(self.rooms[x, y+1])
        return neighbours
    
    ### GET UNVISITED NEIGHBOURS ###
    def getAvNeighbours(self,x,y):
        neighbours = self.getNeighbours(x,y)
        options = []
        ### Takes list of neighbours, checks if each has been visited ###
        for neighbour in neighbours:
            if self.visited[neighbour.location] == False:
                options.append(neighbour) 
        return options
    
    def addDoors(self):
        for i in range(4):
            for room in self.quadrants[i]:
                if room.x + 1 < self.width and self.extraDoors[i] > 0:
                    if room.east == None and not room.final and not self.rooms[room.x+1, room.y].final:
                        rooms.pairRooms(room, self.rooms[room.x+1, room.y], EAST)
                        self.extraDoors[i] -= 1

                if room.y + 1 < self.height and self.extraDoors[i] > 0:
                    if room.north == None and not room.final and not self.rooms[room.x, room.y+1].final:
                        rooms.pairRooms(room, self.rooms[room.x, room.y+1], NORTH)
                        self.extraDoors[i] -= 1




    def makeQuadrants(self):
        for x in range (self.width):
            for y in range (self.height):
                if (y+1) <= self.height/2:
                    if (x+1) <= self.width/2:
                        self.quadrants[0].append(self.rooms[x,y]) ### Bottom left
                        self.rooms[x,y].quadrant = 0
                    else:
                        self.quadrants[1].append(self.rooms[x,y]) ### Bottom right
                        self.rooms[x,y].quadrant = 1
                else:
                    if (x+1) <= self.width/2:
                        self.quadrants[2].append(self.rooms[x,y]) ### Top left
                        self.rooms[x,y].quadrant = 2
                    else:
                        self.quadrants[3].append(self.rooms[x,y]) ### Top right
                        self.rooms[x,y].quadrant = 3
        for i in range(4):
            random.shuffle(self.quadrants[i])


        



    
