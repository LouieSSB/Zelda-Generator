import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random
import Player
import Map
import Tilemap
from PIL import Image

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
        self.wallList = arcade.SpriteList()
        self.mapList = arcade.SpriteList()

        maze_width = 6
        maze_height = 6

        extraDoors = [2,2,2,2]
        rupeeDensity = [0.5, 0.0, 0.1, 0.1]
        enemyDensity = [0.0, 0.1, 0.1, 0.1]
        self.map = Map.Map(maze_width, maze_height, extraDoors, rupeeDensity, enemyDensity)

        self.current_room = self.map.rooms[0,0]
        
        self.last_room = self.current_room
        


        linkSprite = arcade.Sprite("link_01.png")
        self.miniSprite = arcade.Sprite("link_02.png")
        self.triforceSprite = arcade.Sprite("triforce_02.png")
        self.miniSprite.center_x = (TILE/2) + 91 
        self.miniSprite.center_y = SCREEN_HEIGHT -(2*TILE) - 5
        self.triforceSprite.center_x = (TILE/2) * (self.map.goal.location[0]) + 107
        self.triforceSprite.center_y = 408 + (TILE/4) * (self.map.goal.location[1]) + 3
       
        self.playerList.append(linkSprite)
        self.playerList.append(self.miniSprite)
        self.playerList.append(self.triforceSprite)

        ### LINK ###
        self.link = Player.Player(3, 3, linkSprite, self.current_room, self.map, 1.0)

        self.tilemap = Tilemap.SpriteSheetWriter((maze_width*TILE*16), (maze_height*TILE*11))
        #self.tilemap.addImage(Image.open("link_01.png"))
        Tilemap.generateMap(self.tilemap, self.map)
        self.tilemap.show()


        self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite, self.current_room.wallList)



### ON DRAW ###
    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        ### DRAW SPRITES ###
        self.map.tilelist.draw()
        self.link.current_room.floor.draw()
        self.link.current_room.doors.draw()
        self.playerList.draw()
        self.link.current_room.wallList.draw()
        self.link.current_room.rupees.draw()
        self.link.current_room.triforce.draw()
        self.link.current_room.enemySprites.draw()

        ### DRAW TEXT ###
        DEFAULT_FONT_SIZE = 10
        start_x = 420
        start_y = 450
        arcade.draw_text("Rupees: " + str(self.link.money),
                         start_x,
                         start_y,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )
        arcade.draw_text("Damage: " + str(self.link.damage),
                         start_x,
                         start_y - 20,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )
        arcade.draw_text("Kills: " + str(self.link.kills),
                         start_x,
                         start_y - 40,
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

        arcade.draw_text("Quadrant: " + str(self.link.current_room.quadrant),
                         start_x - 200,
                         start_y - 20,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )

### UPDATE ###
    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        rupeeHitList = arcade.check_for_collision_with_list(self.link.sprite, self.link.current_room.rupees)
        triforceHitList = arcade.check_for_collision_with_list(self.link.sprite, self.link.current_room.triforce)
        enemyHitList = arcade.check_for_collision_with_list(self.link.sprite, self.link.current_room.enemySprites)
        for rupee in rupeeHitList:
            rupee.kill()
            self.link.money += 1
        
        for enemy in enemyHitList:
            enemy.kill()
            self.link.kills += 1
            num = random.random()
            if self.link.combatAbility <= num:
                self.link.damage += 1

        
        for triforce in triforceHitList:
            triforce.kill()
            print("GAME DONE!")
            exit()
        
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
        
        if len(self.link.history) >= 2:
            if self.link.history[-2] == 0:
                self.link.history.pop()
                self.link.history.pop()


        self.physics_engine.update()
        
        if self.start:
            self.link.choose()
        for foe in self.link.current_room.enemies:
            foe.move()


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