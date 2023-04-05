import math
import random
import arcade
import numpy as np
import AStar as astar
import Rooms as rooms
import random
import Zelda_Generator as generator
from hpsklearn import HyperoptEstimator
import pandas as pd
from sklearn.model_selection import train_test_split
from scipy.stats.qmc import LatinHypercube
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import pickle
import time
import socket
import csv

trials = Trials()
engine = LatinHypercube(d=7)
sample = engine.random(n=10)
def learn():


    
    ### multiply last two by 20 and round down

    estim = HyperoptEstimator()
    space1 = hp.choice('b', [
        {
            'rupee_0': hp.uniform('r0', 0, 1),
            'rupee_1': hp.uniform('r1', 0, 1),
            'enemy_0': hp.uniform('e0', 0, 1),
            'enemy_1': hp.uniform('e1', 0, 1),
            'doors_0': hp.randint('d0', 5),
            'doors_1': hp.randint('d1', 5),
            'difficulty': hp.uniform('di0', 0,1)
        }
    ])
    ### Objective returns latest

    
    best = fmin(fn=objective,
        space=space1,
        algo=tpe.suggest,
        max_evals=2,
        trials=trials)
    
    print(best)
    sendBest(best)


### Send best params after trials ###
def sendBest(best):
    host = socket.gethostname()  
    port = 8080  
    s = socket.socket()
    s.connect((host, port))
    rupeeDensity = [best['r0'], best['r1']]
    enemyDensity = [best['e0'], best['e1']]
    extraDoors = [best['d0'], best['d1']]
    difficulty = best['di0']

    params = [rupeeDensity, enemyDensity, extraDoors, difficulty]
    message = str(params)
    s.send(message.encode('utf-8'))
    print("BEST SENT")

    s.close()

### Receive fitness after finishing ###
def receiveFitness():
    host = socket.gethostname()
    port = 8081 
  
    s = socket.socket()
    s.bind((host, port))
  
    s.listen(1)
    c, addr = s.accept()
    data = c.recv(1024).decode('utf-8')
    data = data.upper()
    c.send(data.encode('utf-8'))
    c.close()
    print("FITNESS RECEIVED")
    return data
    

### Send parameters before starting ###
def sendParams(rupeeDensity, enemyDensity, extraDoors, difficulty):
    host = socket.gethostname()  
    port = 8080  
    s = socket.socket()
    s.connect((host, port))
    params = [rupeeDensity, enemyDensity, extraDoors, difficulty]
    message = str(params)
    s.send(message.encode('utf-8'))
    print("PARAMS SENT")

    s.close()

### OBJECTIVE FUNCTION ###
def objective(space):
    trialNo = len(trials._dynamic_trials) - 1
    if trialNo < 10:
        rupeeDensity = [sample[trialNo][0], sample[trialNo][1]]
        enemyDensity = [sample[trialNo][2], sample[trialNo][3]]
        extraDoors = [int(sample[trialNo][4]*5), int(sample[trialNo][5]*5)]
        difficulty = sample[trialNo][6]
    else:
        rupeeDensity = [space['rupee_0'], space['rupee_1']]
        enemyDensity = [space['enemy_0'], space['enemy_1']]
        extraDoors = [space['doors_0'], space['doors_1']]
        difficulty = space['difficulty']
    sendParams(rupeeDensity, enemyDensity, extraDoors, difficulty)
    message = receiveFitness()
    return {'loss' : message, 'status' : STATUS_OK}

    

def main():
    learn()

if __name__ == "__main__":
    main()

