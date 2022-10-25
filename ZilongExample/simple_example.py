# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 16:47:59 2022

@author: zji
"""

import ratinabox #IMPORT 
from ratinabox.Environment import Environment
from ratinabox.Agent import Agent
from ratinabox.Neurons import *
#INITIALISE CLASSES
Env = Environment(params={
    "dimensionality": "2D",  # 1D or 2D environment
    "boundary_conditions": "solid",  # solid vs periodic
    "scale": 1,  # scale of environment (in metres)
    "aspect": 1,  # x/y aspect ratio for the (rectangular) 2D environment
    "dx": 0.01,  # discretises the environment (for plotting purposes only)
}) 
Ag = Agent(Env)
PCs = PlaceCells(Ag)
#EXPLORE
for i in range(int(2000/Ag.dt)): 
    Ag.update()
    PCs.update()
#ANALYSE/PLOT
print(Ag.history['pos'][:10]) 
print(PCs.history['firingrate'][:10])
fig, ax = Ag.plot_trajectory()
fig, ax = PCs.plot_rate_timeseries()

#%% import external trajectory data
DataMat = loadmat('HardcastleData.mat')