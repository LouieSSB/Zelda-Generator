import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 480
SCREEN_TITLE = "Zelda Dungeon Generator"
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

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)
         # Sprite lists
        self.current_room = (0,0)

        # Set up the player
        self.rooms = None
        self.playerSprite = None
        self.playerList = None
        self.physics_engine = None
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        # Set up your game here
        
        self.playerList = arcade.SpriteList()
        self.rupeeList = arcade.SpriteList()
        self.wallList = arcade.SpriteList()
        self.mapList = arcade.SpriteList()
        self.money = 0
        self.path = None
        self.timer = 0

        self.rooms = np.empty([5,5], rooms.Room)

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

        for i in range (5):
            for (j) in range(5):
                if self.rooms[i,j] != None:
                    maptile = arcade.Sprite("room_01.png")
                    maptile.left = i*(TILE/2) + 100
                    maptile.bottom = 13*TILE + (8*j) - 8
                    self.mapList.append(maptile)

        self.current_room = self.rooms[0,0]
        self.last_room = self.current_room
        

        SPRITE_SCALING_RUPEE = 1.0
        SPRITE_SCALING_LINK = 1.0
        self.playerSprite = arcade.Sprite("link_01.png", SPRITE_SCALING_LINK)
        self.miniSprite = arcade.Sprite("link_02.png")
        self.triforceSprite = arcade.Sprite("triforce_02.png")
        self.miniSprite.center_x = (TILE/2) + 91 
        self.miniSprite.center_y = SCREEN_HEIGHT -(2*TILE) - 5
        self.triforceSprite.center_x = (TILE/2) + 123
        self.triforceSprite.center_y = SCREEN_HEIGHT -(1.5*TILE) - 5
        self.playerSprite.center_x = 112
        self.playerSprite.center_y = 112
        self.playerList.append(self.playerSprite)
        self.playerList.append(self.miniSprite)
        self.playerList.append(self.triforceSprite)

        self.barrierList = arcade.AStarBarrierList(self.playerSprite, self.wallList, TILE, 16, SCREEN_WIDTH-16, 16, SCREEN_HEIGHT - 4*TILE -16)

        self.physics_engine = arcade.PhysicsEngineSimple(self.playerSprite, self.current_room.wallList)

        #self.graph = makeGraph(room)
        self.graph = astar.makeGraph(room)

        doors = []
        end = None
        for x in range (15):
            for y in range (11):
                if self.graph[x,y] != None and self.graph[x,y].type == DOOR:
                    #doors.append[self.graph]
                    end = self.graph[x,y]
        
        playerX = int((self.playerSprite.center_x - 16)/TILE)
        playerY = int((self.playerSprite.center_y - 16)/TILE)
        start = self.graph[playerX, playerY]
        self.path = astar.aStar(start, end)
        


        for i in range(50):
            rupee = arcade.Sprite("rupee_01.png", SPRITE_SCALING_RUPEE)
            rupee.center_x = random.randrange(TILE*3, SCREEN_WIDTH-TILE*3)
            rupee.center_y = random.randrange(TILE*4, SCREEN_HEIGHT - TILE*6)
            self.rupeeList.append(rupee)
        
        pass

### ON DRAW ###
    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        self.mapList.draw()
        self.current_room.floor.draw()
        self.current_room.doors.draw()

        self.playerList.draw()
        self.rupeeList.draw()
        self.current_room.wallList.draw()
        
        DEFAULT_FONT_SIZE = 10
        start_x = 420
        start_y = 450
        arcade.draw_text("Rupees: " + str(self.money),
                         start_x,
                         start_y,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )
        arcade.draw_text("Room: " + str(self.current_room.location),
                         start_x - 200,
                         start_y,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )

### UPDATE ###
    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        rupeeHitList = arcade.check_for_collision_with_list(self.playerSprite, self.rupeeList)
        for rupee in rupeeHitList:
            rupee.kill()
            self.money += 1
        
        if self.playerSprite.center_x > (SCREEN_WIDTH - TILE):
            self.current_room = self.current_room.east
            self.physics_engine = arcade.PhysicsEngineSimple(self.playerSprite,
                                                             self.current_room.wallList)
            self.playerSprite.center_x = TILE*1.5
            self.miniSprite.center_x += 16

        elif self.playerSprite.center_x < TILE:
            self.current_room = self.current_room.west
            self.physics_engine = arcade.PhysicsEngineSimple(self.playerSprite,
                                                             self.current_room.wallList)
            self.playerSprite.center_x = SCREEN_WIDTH - TILE*1.5
            self.miniSprite.center_x -= 16

        elif self.playerSprite.center_y > SCREEN_HEIGHT - TILE*5:
            self.current_room = self.current_room.north
            self.physics_engine = arcade.PhysicsEngineSimple(self.playerSprite,
                                                             self.current_room.wallList)
            self.playerSprite.center_y = TILE*1.5
            self.miniSprite.center_y += 8

        elif self.playerSprite.center_y < TILE:
            self.current_room = self.current_room.south
            self.physics_engine = arcade.PhysicsEngineSimple(self.playerSprite,
                                                             self.current_room.wallList)
            self.playerSprite.center_y = SCREEN_HEIGHT - TILE*5.5
            self.miniSprite.center_y -= 8

        self.physics_engine.update()


        self.timer += 1;

        if len(self.path) > 0 and self.timer >= 20:
            self.playerSprite.center_x = (self.path[0].x * TILE) + 16
            self.playerSprite.center_y = (self.path[0].y * TILE) + 16
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
                        if self.playerSprite.bottom <= TILE and y != 0:
                            doors.append(self.graph[x,y])
                        elif self.playerSprite.top >= SCREEN_HEIGHT - TILE*5 and y != 10:
                            doors.append(self.graph[x,y])
                        elif self.playerSprite.left <= TILE and x != 0:
                            doors.append(self.graph[x,y])
                        elif (self.playerSprite.right >= (SCREEN_WIDTH - TILE*2)) and x != 15:
                            doors.append(self.graph[x,y])

                        
                        #end = self.graph[x,y]
            if len(doors) > 0:
                #end = doors.pop()
                door = random.randint(0, len(doors)-1)
                end = doors[door]

            
            playerX = int((self.playerSprite.center_x - 16)/TILE)
            playerY = int((self.playerSprite.center_y - 16)/TILE)
            start = self.graph[playerX, playerY]
            if end == None:
                end = start
            self.path = astar.aStar(start, end)

        pass
    

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        MOVEMENT_SPEED = 5
        if key == arcade.key.UP:
            self.playerSprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.playerSprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.playerSprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.playerSprite.change_x = MOVEMENT_SPEED
        if key == arcade.key.W:
            self.playerSprite.center_y += TILE
        if key == arcade.key.S:
            self.playerSprite.center_y -= TILE
        if key == arcade.key.D:
            self.playerSprite.center_x += TILE
        if key == arcade.key.A:
            self.playerSprite.center_x -= TILE

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.playerSprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.playerSprite.change_x = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()