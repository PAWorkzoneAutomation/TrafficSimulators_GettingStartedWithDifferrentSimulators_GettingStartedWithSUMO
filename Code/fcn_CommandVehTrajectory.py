#!/usr/bin/python3
# This is a simple example to demonstrate how to command an AV to drive based on a trajectory using traci module which allows interfacing SUMO with python. 
# Author: Wushuang
# Created on: 2022 06 28
# Revision history: 
# 2022 06 29- rewrite into function, added comments
# For more information, please see https://sumo.dlr.de/docs/TraCI.html#examples

#   _____                   _       
#  |_   _|                 | |      
#    | |  _ __  _ __  _   _| |_ ___ 
#    | | | '_ \| '_ \| | | | __/ __|
#   _| |_| | | | |_) | |_| | |_\__ \
#  |_____|_| |_| .__/ \__,_|\__|___/
#              | |                  
#              |_|  
# inputFilePath: what are the csv file you want to use as a command trajectory? This input should  contain at least column vehicle_x and vehicle_y
#                format: csv
# timeStep: what is the time step you want to use in the simulation? If this input is not given, it uses the default value 1
#           format: string, such as "1"
# outputFilePath: this is the output file path of the simulation.
#           format: sumo outputs simulation as xml file. It can be then converted to csv file. 
#    ____        _               _       
#   / __ \      | |             | |      
#  | |  | |_   _| |_ _ __  _   _| |_ ___ 
#  | |  | | | | | __| '_ \| | | | __/ __|
#  | |__| | |_| | |_| |_) | |_| | |_\__ \
#   \____/ \__,_|\__| .__/ \__,_|\__|___/
#                   | |                  
#                   |_|                  
# Simulation_Flag: this flag confirms that the simulation runs succesfully. 
#                  format: int



# These modules are needed to run this script
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random
from tracemalloc import start
import pandas as pd
import numpy as np

# we need to import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  
import traci  
import traci.constants as tc

def fcn_CommandVehTrajectory(inputFilePath, timeStep="1",outputFilePath = "output.xml"):
    try:    
        Simulation_Flag = 0
        # user's input: what are the csv file you want to use as a command trajectory? The csv file should contain at least column vehicle_x and vehicle_y
        df = pd.read_csv(inputFilePath)       

        #what are the x and y position you want to command? 
        commandedX = df["vehicle_x"][df.index[df.vehicle_x.notnull()==True]]
        commandedY = df["vehicle_y"][df.index[df.vehicle_y.notnull()==True]]      
#   __  __       _       
#  |  \/  |     (_)      
#  | \  / | __ _ _ _ __  
#  | |\/| |/ _` | | '_ \ 
#  | |  | | (_| | | | | |
#  |_|  |_|\__,_|_|_| |_|                       
                               
        # First you compose the command line to start either sumo or sumo-gui (leaving out the option which was needed before 0.28.0):
        sumoBinary = "/usr/bin/sumo-gui"
        sumoCmd = [sumoBinary, "-c", "./hello.sumocfg","--step-length",timeStep,"--start","--fcd-output",outputFilePath]
        # define beginning and end of simulation 
        counter = np.array(df.index[df.vehicle_x.notnull()==True])[0]
        ind_end = np.array(df.index[df.vehicle_x.notnull()==True])[-1]
        # Then you start the simulation and connect to it with your script:
        traci.start(sumoCmd)
        veh_id = "veh0"
        while traci.simulation.getMinExpectedNumber() > 0:
             # get the position data
            position = traci.vehicle.getPosition(veh_id)            
            # let the vehicle to move to this position. Edge ID is left as "" and lane is left as "-1" since they are optional. 
            traci.vehicle.moveToXY("veh0","","-1",commandedX[counter],commandedY[counter])
            # run the simulation step
            traci.simulationStep()
            # print out the data, including simulation time, vehicle id, position in X,Y. Please see more infomation at:https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-moveToXY 
            print(traci.simulation.getTime(),veh_id,position)
            # go to next counter
            counter = counter + 1            
            if counter > ind_end:              
                break
            
    finally:       
        print("Simulation is done!")
        Simulation_Flag = 1
        # close the connection
        traci.close()
        return Simulation_Flag


if __name__ == '__main__':
    fcn_CommandVehTrajectory(filePath,timeStep=1,outputFilePath = "output.xml")


        