#!/usr/bin/python3
# This is a simple example to demonstrate how to talk with SUMO using python API through traci module, get the simulation data, and print out the data live. 
# Author: Wushuang
# Created on: 2022 06 20
# Revision history:
# 2022 07 18 added comments to example file
# For more information, please see https://sumo.dlr.de/docs/TraCI.html#examples

# SUMO example simulation file used in this script: I99.sumocfg 
# Please see https://github.com/ivsg-psu/TrafficSimulators_GettingStartedWithDifferrentSimulators_GettingStartedWithSUMO/tree/main/Data/I99


# These modules are needed to run this script
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from tracemalloc import start
#from turtle import position

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  
import traci  
import traci.constants as tc


#   __  __       _       
#  |  \/  |     (_)      
#  | \  / | __ _ _ _ __  
#  | |\/| |/ _` | | '_ \ 
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|   

# First you compose the command line to start either sumo or sumo-gui (leaving out the option which was needed before 0.28.0):
sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "./I99.sumocfg"]
# Then you start the simulation and connect to it with your script:
traci.start(sumoCmd)
# if there are any vehicles spawned
while traci.simulation.getMinExpectedNumber() > 0: 
    # Iterate the vehicle ID list
    for veh_id in traci.vehicle.getIDList():
        # Query vehicle position
        position = traci.vehicle.getPosition(veh_id)
        # print out vehicle position 
        print(traci.simulation.getTime(),veh_id,position)
    traci.simulationStep()
# close the connection
traci.close()