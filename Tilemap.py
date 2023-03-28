### IMPORTS ###
from PIL import Image
import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random
import Player
import Map

### CONSTANTS ###
TILE = 32

class SpriteSheetWriter:
	### INIT ###
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.spritesheet = Image.new("RGBA", (self.width, self.height), (0,0,0,255))
		self.tileX = 0
		self.tileY = 16
		self.margin = 1

	### INSERT TILE ###
	def addImage(self, image, x, y):
		self.posX = int(x)
		self.posY = int(y)
		destBox = (self.posX, self.posY, self.posX + image.size[0], self.posY + image.size[1])
		self.spritesheet.paste(image, destBox, image.convert("RGBA"))
		self.tileX = self.tileX + 1

	### DISPLAY ###	
	def show(self):
		self.spritesheet.show()

### CREATE ###
def generateMap(tilemap, map, seed):
	width = len(map.rooms)
	height = len(map.rooms[0])
	for x in range (width):
		for y in range (height):
			room = map.rooms[x,y]
			for floor in room.floor:
				tilemap.addImage(Image.open("graphics/floor_01.png"), floor.left + shiftX(x), shiftY(tilemap, y) - floor.bottom - 32)
			for wall in room.wallList:
				tilemap.addImage(Image.open("graphics/block_01.png"), wall.left + shiftX(x), shiftY(tilemap, y) - wall.bottom - 32)
			for door in room.doors:
				tilemap.addImage(Image.open("graphics/floor_02.png"), door.left + shiftX(x), shiftY(tilemap, y) - door.bottom - 32)
			for foe in room.enemies:
				tilemap.addImage(Image.open("graphics/stalfos_01.png"), foe.sprite.left + shiftX(x), shiftY(tilemap, y) - foe.sprite.bottom - 32)
			for rupee in room.rupees:
				tilemap.addImage(Image.open("graphics/rupee_01.png"), rupee.left + shiftX(x), shiftY(tilemap, y) - rupee.bottom - 32)
			for triforce in room.triforce:
				tilemap.addImage(Image.open("graphics/triforce_01.png"), triforce.left + shiftX(x), shiftY(tilemap, y) - triforce.bottom - 32)
	tilemap.spritesheet.save("maps/"+str(seed)+".png")
		
###	REALIGN ###
def shiftY(tilemap, y):
	return (tilemap.height - 352*y)
def shiftX(x):
	return (x*512)
