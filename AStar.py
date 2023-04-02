### IMPORTS ###
import math
import random
import arcade
import numpy as np

### CONSTANTS ###
FLOOR = 0
WALL = 1
DOOR = 2

### TILE OBJECT ###
class Node:
     def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.parent = None
        self.gcost = 0
        self.hcost = 0
        self.fcost = 0
        self.type = type
        self.neighbours = []

### ALGORITHM ###
def aStar(start, end):
    ### LISTS ###
    path = []
    openSet = []
    closedSet = []
    currentNode = start

    openSet.append(currentNode)

    ### MAIN LOOP ###
    while end not in closedSet and len(openSet) > 0:
        cheapest = 100000
        for node in openSet:
            if node.fcost < cheapest:
                currentNode = node
                cheapest = node.fcost
        openSet.remove(currentNode)
        closedSet.append(currentNode)
                
                
        for node in currentNode.neighbours:
            if node not in openSet and node not in closedSet:
                node.gcost = currentNode.gcost + 1
                node.hcost = abs(end.x - node.x) + abs(end.y - node.y)
                node.fcost = node.gcost + node.hcost
                node.parent = currentNode
                openSet.append(node)
            elif node not in closedSet:
                if currentNode.gcost + 1 < node.gcost:
                    node.gcost = currentNode.gcost + 1
                    node.fcost + node.gcost + node.hcost
                    node.parent = currentNode

    ## Backtrack from goal to find path ###
    nextNode = end
    while nextNode.parent != None:
        path.insert(0, nextNode)
        nextNode = nextNode.parent

    return path

### MAKE GRAPH ###
def makeGraph(room):
    graph = np.empty([16,11], Node)
    for x in range (16):
        for y in range(11):
            if room.map[10-y][x] != WALL:
                node = Node(x, y, room.map[10-y][x])
                graph[x,y] = node
                
    for x in range (16):
        for y in range(11):
            if graph[x,y] != None:
                addNeighbours(graph[x,y], graph)


    return graph

### CONNECT NODES ###
def addNeighbours(node, graph):
    if node.x + 1 < 16:
        if graph[node.x + 1, node.y] != None:
            newNode = graph[node.x + 1, node.y]
            node.neighbours.append(newNode)
            newNode.neighbours.append(node)
    
    if node.y + 1 < 11:
        if graph[node.x, node.y + 1] != None:
            newNode = graph[node.x, node.y + 1]
            node.neighbours.append(newNode)
            newNode.neighbours.append(node)