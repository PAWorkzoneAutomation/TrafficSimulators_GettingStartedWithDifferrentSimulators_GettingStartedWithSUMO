#!/usr/bin/python3
# This is a simple example to demonstrate how to command an AV to be at an exact position using traci module which allows interfacing SUMO with python. 
# Author: Wushuang
# Created on: 2022 06 24
# For more information, please see https://sumo.dlr.de/docs/TraCI.html#examples

# These modules are needed to run this script
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from tracemalloc import start

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  
import traci  
import traci.constants as tc


def main():
    try:    
#   _____                   _       
#  |_   _|                 | |      
#    | |  _ __  _ __  _   _| |_ ___ 
#    | | | '_ \| '_ \| | | | __/ __|
#   _| |_| | | | |_) | |_| | |_\__ \
#  |_____|_| |_| .__/ \__,_|\__|___/
#              | |                  
#              |_|                  
        # user's input: what are the x and y position you want to command? 
        commandedX = 5.1
        commandedY = -1.6
        # user's input: how long do you want to simulate? 
        simulationLength = 100
#   __  __       _       
#  |  \/  |     (_)      
#  | \  / | __ _ _ _ __  
#  | |\/| |/ _` | | '_ \ 
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|                       
                               
        # First you compose the command line to start either sumo or sumo-gui (leaving out the option which was needed before 0.28.0):
        sumoBinary = "/usr/bin/sumo-gui"
        sumoCmd = [sumoBinary, "-c", "./hello.sumocfg","--start","--fcd-output","helloresults_CommandedPosition.xml"]
        # Then you start the simulation and connect to it with your script:
        traci.start(sumoCmd)
        veh_id = "veh0"
        while traci.simulation.getMinExpectedNumber() > 0:
            # get the position data
            position = traci.vehicle.getPosition(veh_id)
            # print out the data, including simulation time, vehicle id, position in X,Y. Please see more infomation at:https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-moveToXY 
            print(traci.simulation.getTime(),veh_id,position)
            # let the vehicle to move to this position. Edge ID is left as "" and lane is left as "-1" since they are optional. 
            traci.vehicle.moveToXY("veh0","","-1",commandedX,commandedY)
            traci.simulationStep()
            if traci.simulation.getTime()>=simulationLength:
                
                break
            
    finally:       
        print("Simulation is done!")
        # close the connection
        traci.close()


if __name__ == '__main__':
    main()


        