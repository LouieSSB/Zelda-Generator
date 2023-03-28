### IMPORTS ###
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
import sys
import csv

### CONSTANTS ###
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

### GAME WINDOW ###
class MyGame(arcade.Window):
    ### INIT ###
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
    
    ### SETUP GAME ###
    def setup(self, extraDoors, rupeeDensity, enemyDensity, seed, rupee_aff, combat_aff, combat_skill, heuristic, maze_width, maze_height, iteration):
        ### INITIALISE ###
        self.rooms = None       
        self.link = None
        self.playerList = None
        self.physics_engine = None 
        #self.start = False
        
        ### ATTRIBUTES ###
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.rupee_aff = rupee_aff
        self.combat_aff = combat_aff
        self.combat_skill = combat_skill
        self.heuristic = heuristic
        self.extraDoors = extraDoors
        self.rupeeDensity = rupeeDensity
        self.enemyDensity = enemyDensity
        self.iteration = iteration
        self.seed = seed
        random.seed(seed)

        ### SPRITE LISTS ###
        self.playerList = arcade.SpriteList()
        self.wallList = arcade.SpriteList()
        self.mapList = arcade.SpriteList()

        ### GENERATE MAZE ###
        self.map = Map.Map(maze_width, maze_height, extraDoors, rupeeDensity, enemyDensity)
        self.current_room = self.map.rooms[0,0]
        self.current_room.visited = True
        self.last_room = self.current_room
        
        ### SPRITES ###
        linkSprite = arcade.Sprite("graphics/link_01.png")
        self.miniSprite = arcade.Sprite("graphics/link_02.png")
        self.triforceSprite = arcade.Sprite("graphics/triforce_02.png")
        self.miniSprite.center_x = (TILE/2) + 91 
        self.miniSprite.center_y = SCREEN_HEIGHT -(2*TILE) - 5
        self.triforceSprite.center_x = (TILE/2) * (self.map.goal.location[0]) + 107
        self.triforceSprite.center_y = 408 + (TILE/4) * (self.map.goal.location[1]) + 3
       
        self.playerList.append(linkSprite)
        self.playerList.append(self.miniSprite)
        self.playerList.append(self.triforceSprite)

        ### LINK ###
        self.link = Player.Player(3, 3, linkSprite, self.current_room, self.map, rupee_aff, combat_aff, combat_skill, heuristic)
        self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite, self.current_room.wallList)

        ### MAKE TILEMAP ###
        if iteration == 4:
            self.tilemap = Tilemap.SpriteSheetWriter((maze_width*TILE*16), (maze_height*TILE*11))
            Tilemap.generateMap(self.tilemap, self.map, self.seed)
            #self.tilemap.show()





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
        arcade.draw_text("Visited: " + str(self.link.roomsVisited),
                         start_x - 200,
                         start_y - 40,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )
        arcade.draw_text("Frames: " + str(self.link.totaltime),
                         start_x - 200,
                         start_y - 60,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )
        arcade.draw_text("Iteration: " + str(self.iteration),
                         start_x - 200,
                         start_y - 80,
                         arcade.color.WHITE,
                         DEFAULT_FONT_SIZE,
                         width=150,
                         )

### UPDATE ###
    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        ### COLLISION ###
        rupeeHitList = arcade.check_for_collision_with_list(self.link.sprite, self.link.current_room.rupees)
        triforceHitList = arcade.check_for_collision_with_list(self.link.sprite, self.link.current_room.triforce)
        enemyHitList = arcade.check_for_collision_with_list(self.link.sprite, self.link.current_room.enemySprites)
        
        ### RUPEES ###
        for rupee in rupeeHitList:
            rupee.kill()
            self.link.money += 1
        
        ### ENEMIES ###
        for enemy in enemyHitList:
            enemy.kill()
            self.link.kills += 1
            num = random.random()
            if self.link.combatAbility <= num:
                self.link.damage += 1

        ### TRIFORCE ###
        for triforce in triforceHitList:
            triforce.kill()
            print("GAME DONE!")
            self.restart()
        
        ### EAST ###
        if self.link.sprite.center_x > (SCREEN_WIDTH - TILE):
            self.link.current_room.checkedDoors[2] = True

            self.link.current_room = self.link.current_room.east
            self.visitCheck(self.link.current_room)
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
            self.visitCheck(self.link.current_room)
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
            self.visitCheck(self.link.current_room)
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
            self.visitCheck(self.link.current_room)
            self.physics_engine = arcade.PhysicsEngineSimple(self.link.sprite,
                                                             self.link.current_room.wallList)
            self.link.sprite.center_y = SCREEN_HEIGHT - TILE*5.5
            self.miniSprite.center_y -= 8
            self.link.history.append(SOUTH)
            self.link.current_room.checkedDoors[0] = True
        
        ### BACKTRACKING ###
        if len(self.link.history) >= 2:
            if self.link.history[-2] == 0:
                # Pop twice to avoid getting in a loop of backtracking to where you just were
                self.link.history.pop()
                self.link.history.pop()


        self.physics_engine.update()
        
        ### AI ACTIONS ###
        if self.start:
            self.link.choose()
        for foe in self.link.current_room.enemies:
            foe.move()


        pass
    
    ### USER CONTROL ###
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

    ### VISITED CHECK ###
    def visitCheck(self, room):
        if room.visited:
            return
        else:
            room.visited = True
            self.link.roomsVisited += 1
            return

    ### CREATE CSV ###
    def createCSV(self):
        f = open('outputs/'+str(self.seed)+'.csv', 'w', newline='')
        header = ['rupee_0', 'rupee_1', 'enemy_0', 'enemy_1', 'doors_0', 'doors_1', 'fitness']
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()

    ### WRITE TO CSV ###
    def writeToCSV(self, rupeeDensity, enemyDensity, extraDoors, fitness):
        f = open('outputs/'+str(self.seed)+'.csv', 'a', newline='')
        num = random.randint(0,100)
        row = [rupeeDensity[0], rupeeDensity[1], enemyDensity[0],enemyDensity[1], extraDoors[0], extraDoors[1],fitness]
    
        writer = csv.writer(f)
        writer.writerow(row)
        f.close()

    ### RESET GAME ###
    def restart(self):
        fitness = self.link.money + 2*self.link.kills - 8*self.link.damage - 0.2*self.link.totaltime + 10*self.link.roomsVisited
        print(fitness)
        self.writeToCSV(self.rupeeDensity, self.enemyDensity, self.extraDoors, fitness)
        extraDoors = [2,2]
        rupeeDensity = [random.random(), random.random()]
        enemyDensity = [random.random(), random.random()]
        self.setup(extraDoors, rupeeDensity, enemyDensity, self.seed, self.rupee_aff, self.combat_aff, self.combat_skill, self.heuristic, self.maze_width, self.maze_height, self.iteration+1)

### MAIN ###
def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    ### Parameters are: enemy density, rupee density, extra doors, rng seed ###
    extraDoors = [2,2]
    rupeeDensity = [0.5, 0.0]
    enemyDensity = [0.0, 0.1]
    ### Player parameters ###
    rupee_aff = 0.4
    combat_aff = 0.6
    combat_skill = 0.7
    heuristic = 0.6

    ### Maze parameters ###
    maze_width = 2
    maze_height = 2

    ### Generate seed ###
    seed = random.randrange(sys.maxsize)
    #seed = 4453415329130735445
    print("seed: " , seed)

    
    
    ### Create game ###
    game.setup(extraDoors, rupeeDensity, enemyDensity, seed, rupee_aff, combat_aff, combat_skill, heuristic, maze_width, maze_height, 0)

    ### Initialise file ###
    game.createCSV()

    ### Run game ###
    arcade.run()


if __name__ == "__main__":
    main()