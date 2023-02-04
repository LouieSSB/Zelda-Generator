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
        self.tilelist = arcade.SpriteList()

        room = rooms.Room((0,0))
        room2 = rooms.Room((1,0))
        room3 = rooms.Room((2,0))
        room4 = rooms.Room((0,1))
        room5 = rooms.Room((1,1))
        room6 = rooms.Room((2,1))
        room7 = rooms.Room((1,2))
        room8 = rooms.Room((0,2))
        room9 = rooms.Room((2,2))
        #pairRooms(room, room2, EAST)
        rooms.pairRooms(room2, room3, EAST)
        rooms.pairRooms(room, room4, NORTH)
        rooms.pairRooms(room2, room5, NORTH)
        rooms.pairRooms(room4, room5, EAST)
        rooms.pairRooms(room3, room6, NORTH)
        rooms.pairRooms(room5, room7, NORTH)
        rooms.pairRooms(room7, room8, WEST)
        rooms.pairRooms(room6, room9, NORTH)


        room = rooms.makeRoom(room)
        room2 = rooms.makeRoom(room2)
        room3 = rooms.makeRoom(room3)
        room4 = rooms.makeRoom(room4)
        room5 = rooms.makeRoom(room5)
        room6 = rooms.makeRoom(room6)
        room7 = rooms.makeRoom(room7)
        room8 = rooms.makeRoom(room8)
        room9 = rooms.makeRoom(room9)

        self.rooms[room.location[0], room.location[1]] = room
        self.rooms[room2.location[0], room2.location[1]] = room2
        self.rooms[room3.location[0], room3.location[1]] = room3
        self.rooms[room4.location[0], room4.location[1]] = room4
        self.rooms[room5.location[0], room5.location[1]] = room5
        self.rooms[room6.location[0], room6.location[1]] = room6
        self.rooms[room7.location[0], room7.location[1]] = room7
        self.rooms[room8.location[0], room8.location[1]] = room8
        self.rooms[room9.location[0], room9.location[1]] = room9


        self.makeMinimap()

    def makeMinimap(self):
        for i in range (5):
            for (j) in range(5):
                if self.rooms[i,j] != None:
                    maptile = arcade.Sprite("room_01.png")
                    maptile.left = i*(TILE/2) + 100
                    maptile.bottom = 13*TILE + (8*j) - 8
                    self.tilelist.append(maptile)
