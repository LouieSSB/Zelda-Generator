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
from hyperopt import fmin, tpe, hp, STATUS_OK
import pickle
import time
import socket

def learn():

    
    #dataset = pd.read_csv("outputs/"+fileName+".csv")
    #x = dataset[['rupee_0','rupee_1','enemy_0','enemy_1','doors_0','doors_1']]
    #y = dataset[['fitness']]
    #x_train, x_test, y_train, y_test = train_test_split(x, y, shuffle = True, test_size = 0.3, random_state = 40)

    engine = LatinHypercube(d=6)
    sample = engine.random(n=10)
    ### multiply last two by 20 and round down

    estim = HyperoptEstimator()
    space1 = hp.choice('b', [
        {
            'rupee_0': hp.uniform('r0', 0, 1),
            'rupee_1': hp.uniform('r1', 0, 1),
            'enemy_0': hp.uniform('e0', 0, 1),
            'enemy_1': hp.uniform('e1', 0, 1),
            'doors_0': hp.randint('d0', 0, 5),
            'doors_1': hp.randint('d1', 0, 5)
        }
    ])
    ### Objective returns latest

    best = fmin(fn=objective,
        space=space1,
        algo=tpe.suggest,
        max_evals=20)
    
    print(best)
    

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
def sendParams(rupeeDensity, enemyDensity, extraDoors):
    host = socket.gethostname()  # get local machine name
    port = 8080  # Make sure it's within the > 1024 $$ <65535 range
  
    s = socket.socket()
    s.connect((host, port))
    params = [rupeeDensity, enemyDensity, extraDoors]
    message = str(params)
    s.send(message.encode('utf-8'))
    print("PARAMS SENT")

    s.close()

def objective(space):
    rupeeDensity = [space['rupee_0'], space['rupee_1']]
    enemyDensity = [space['enemy_0'], space['enemy_1']]
    extraDoors = [space['doors_0'], space['doors_1']]
    sendParams(rupeeDensity, enemyDensity, extraDoors)
    message = receiveFitness()
    return {'loss' : message, 'status' : STATUS_OK}

    

def main():
    learn()

    #while True:
    #    extraDoors = [2,2]
    #    rupeeDensity = [random.random(), random.random()]
    #    enemyDensity = [random.random(), random.random()]
    #    message = objective(rupeeDensity, enemyDensity, extraDoors)
    #    print("PRINTING: " + message)
    

if __name__ == "__main__":
    main()

