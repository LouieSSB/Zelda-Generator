### IMPORTS ###
import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random
import copy

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
RUPEE_DENSITY = 0.5
ENEMY_DENSITY = 0.1

### MAZE CLASS ###
class Map():
    ### INIT ###
    def __init__(self, width, height, extraDoors, rupeeDensity, enemyDensity, difficulty):
        self.height = height
        self.width = width
        self.rooms = np.empty([width, height], rooms.Room)
        self.goal = None
        
        ### Lists that are 4 items long, one for each quadrant ###
        #self.quadrants = [[],[],[],[]]  
        self.quadrants = [[],[]]
        self.extraDoors = copy.deepcopy(extraDoors)
        self.rupeeDensity = rupeeDensity
        self.enemyDensity = enemyDensity
        self.difficulty = difficulty
        
        ### Create map array ###
        for x in range(width):
            for y in range(height):
                self.rooms[x,y] = rooms.Room((x,y))
                
        ### Map of which rooms have been visited for maze generation ###
        self.visited = np.full([width,height], False, dtype=bool)

        ### MINIMAP SPRITES ###
        self.tilelist = arcade.SpriteList() 

        ### Depth-first maze generation ###
        self.generateMaze()

        ### DIVIDE MAP ###
        self.makeQuadrants()
        

        ### Locate room furthest from start ###
        highest = 0
        for i in range (width):
            for j in range(height):
                if self.rooms[i,j].distance >= highest:
                    self.goal = self.rooms[i,j]
                    highest = self.rooms[i,j].distance
        self.goal.final = True
        
        ### ADD IN EXTRA DOORS ###
        self.addDoors()
        
        ### Sets templates for each room, and builds their tiles ###
        for i in range (width):
            for j in range(height):
                ### Triforce room gets its own layout ###
                if self.rooms[i,j] == self.goal: 
                    self.goal.setTemplate(13)
                    ### Room has no enemies or money ###
                    rooms.makeRoom(self.rooms[i,j], 0, 0) 
                else:
                    ### All other rooms are chosen randomly ###
                    #temp = random.randint(0, 12) 
                    temp = self.weightedTemplate(self.difficulty)
                    self.rooms[i,j].setTemplate(temp)
                    rooms.makeRoom(self.rooms[i,j], self.rupeeDensity[self.rooms[i,j].quadrant], self.enemyDensity[self.rooms[i,j].quadrant])
                
        
        ### Make minimap based on map size ###   
        self.makeMinimap()

    

    ### MAZE GENERATOR ###
    def generateMaze(self):
        ### Stack for depth-first generation ###
        stack = []
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
                    ### Blue rectangle graphic ###
                    maptile = arcade.Sprite("graphics/room_01.png") 
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
    
    ### ADD DOORS ###
    def addDoors(self):
        ### FOR EACH QUADRANT
        for i in range(2):
            for room in self.quadrants[i]:
                ### Don't add doors to last room ###
                if room.x + 1 < self.width and self.extraDoors[i] > 0:
                    if room.east == None and not room.final and not self.rooms[room.x+1, room.y].final:
                        rooms.pairRooms(room, self.rooms[room.x+1, room.y], EAST)
                        self.extraDoors[i] -= 1

                if room.y + 1 < self.height and self.extraDoors[i] > 0:
                    if room.north == None and not room.final and not self.rooms[room.x, room.y+1].final:
                        rooms.pairRooms(room, self.rooms[room.x, room.y+1], NORTH)
                        self.extraDoors[i] -= 1



    ### MAKE QUADRANTS ###
    def makeQuadrants(self):
        for x in range (self.width):
            for y in range (self.height):
                if (y+1) <= self.height/2:
                    ### BOTTOM LEFT ###
                    if (x+1) <= self.width/2:
                        self.quadrants[0].append(self.rooms[x,y]) 
                        self.rooms[x,y].quadrant = 0
                    ### BOTTOM RIGHT ###
                    else:
                        self.quadrants[1].append(self.rooms[x,y])
                        self.rooms[x,y].quadrant = 1
                else:
                    ### TOP LEFT ###
                    if (x+1) <= self.width/2:
                        #self.quadrants[2].append(self.rooms[x,y])
                        self.quadrants[0].append(self.rooms[x,y])
                        #self.rooms[x,y].quadrant = 2
                        self.rooms[x,y].quadrant = 0
                    ### TOP RIGHT ###
                    else:
                        #self.quadrants[3].append(self.rooms[x,y])
                        self.quadrants[1].append(self.rooms[x,y])
                        #self.rooms[x,y].quadrant = 3
                        self.rooms[x,y].quadrant = 1
        
        ### Shuffle rooms so extra doors are random ###
        #for i in range(4):
        #    random.shuffle(self.quadrants[i])
        for i in range(2):
            random.shuffle(self.quadrants[i])

    def weightedTemplate(self, difficulty):
        weights =      [1,1,1,1,1,1,1,1,1,1,1,1,1]
        weight = int(difficulty *13)
        weights[weight] = 2
        for n in range(weight - 1, weight - 4,-1):
            if n >= 0:
                weights[n] = 2
        for n in range(weight + 1, weight + 4, 1):
            if n < 13:
                weights[n] = 2

        population = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        temp = random.choices(population, weights=weights, k=1)
        return temp[0]

### parameter is between 0 and 1
### miltiply this by 13 and round to get middle index
### give the indexes 3 to the left and 3 to the right additional weight



        



    
