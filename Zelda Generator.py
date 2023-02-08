import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random
import Player
import Map

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
        
        self.link = None
        self.playerList = None
        self.physics_engine = None
        self.start = False
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        # Set up your game here
        
        self.playerList = arcade.SpriteList()
        self.rupeeList = arcade.SpriteList()
        self.wallList = arcade.SpriteList()
        self.mapList = arcade.SpriteList()
        self.money = 0
        self.timer = 0

        
        self.map = Map.Map(4,4)

        self.current_room = self.map.rooms[0,0]
        
        self.last_room = self.current_room
        


        linkSprite = arcade.Sprite("link_01.png")
        self.miniSprite = arcade.Sprite("link_02.png")
        self.triforceSprite = arcade.Sprite("triforce_02.png")
        self.miniSprite.center_x = (TILE/2) + 91 
        self.miniSprite.center_y = SCREEN_HEIGHT -(2*TILE) - 5
        self.triforceSprite.center_x = (TILE/2) + 123
        self.triforceSprite.center_y = SCREEN_HEIGHT -(1.5*TILE) - 5
       
        self.playerList.append(linkSprite)
        self.playerList.append(self.miniSprite)
        self.playerList.append(self.triforceSprite)

        ### LINK ###
        self.link = Player.Player(3, 3, linkSprite, self.current_room, self.map)


        self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite, self.current_room.wallList)


        """
        for i in range(50):
            rupee = arcade.Sprite("rupee_01.png")
            rupee.center_x = random.randrange(TILE*3, SCREEN_WIDTH-TILE*3)
            rupee.center_y = random.randrange(TILE*4, SCREEN_HEIGHT - TILE*6)
            self.rupeeList.append(rupee)
        
        pass
        """

### ON DRAW ###
    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        self.map.tilelist.draw()
        self.link.current_room.floor.draw()
        self.link.current_room.doors.draw()
        self.playerList.draw()
        self.link.current_room.wallList.draw()
        self.link.current_room.rupees.draw()

        
        
        
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
        arcade.draw_text("Room: " + str(self.link.current_room.location),
                         start_x - 200,
                         start_y,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )

### UPDATE ###
    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        rupeeHitList = arcade.check_for_collision_with_list(self.link.sprite, self.link.current_room.rupees)
        for rupee in rupeeHitList:
            rupee.kill()
            self.money += 1
        
        ### EAST ###
        if self.link.sprite.center_x > (SCREEN_WIDTH - TILE):
            self.link.current_room.checkedDoors[2] = True

            self.link.current_room = self.link.current_room.east
            self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite,
                                                             self.link.current_room.wallList)
            self.link.sprite.center_x = TILE*1.5
            self.miniSprite.center_x += 16
            self.link.history.append(EAST)
            self.link.current_room.checkedDoors[3] = True
            

        ### WEST ###
        elif self.link.sprite.center_x < TILE:
            self.link.current_room.checkedDoors[3] = True

            self.link.current_room = self.link.current_room.west
            self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite,
                                                             self.link.current_room.wallList)
            self.link.sprite.center_x = SCREEN_WIDTH - TILE*1.5
            self.miniSprite.center_x -= 16
            self.link.history.append(WEST)
            self.link.current_room.checkedDoors[2] = True

        ### NORTH ###
        elif self.link.sprite.center_y > SCREEN_HEIGHT - TILE*5:
            self.link.current_room.checkedDoors[0] = True

            self.link.current_room = self.link.current_room.north
            self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite,
                                                             self.link.current_room.wallList)
            self.link.sprite.center_y = TILE*1.5
            self.miniSprite.center_y += 8
            self.link.history.append(NORTH)
            self.link.current_room.checkedDoors[1] = True

        ### SOUTH ###
        elif self.link.sprite.center_y < TILE:
            self.link.current_room.checkedDoors[1] = True

            self.link.current_room = self.link.current_room.south
            self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite,
                                                             self.link.current_room.wallList)
            self.link.sprite.center_y = SCREEN_HEIGHT - TILE*5.5
            self.miniSprite.center_y -= 8
            self.link.history.append(SOUTH)
            self.link.current_room.checkedDoors[0] = True

        self.physics_engine.update()
        
        if self.start:
            self.link.choose()

    

    


        pass
    

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        MOVEMENT_SPEED = 5
        if key == arcade.key.UP:
            self.link.sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.link.sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.link.sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.link.sprite.change_x = MOVEMENT_SPEED
        if key == arcade.key.W:
            self.link.sprite.center_y += TILE
        if key == arcade.key.S:
            self.link.sprite.center_y -= TILE
        if key == arcade.key.D:
            self.link.sprite.center_x += TILE
        if key == arcade.key.A:
            self.link.sprite.center_x -= TILE
        if key == arcade.key.RETURN:
            self.start = not self.start

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.link.sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.link.sprite.change_x = 0


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()