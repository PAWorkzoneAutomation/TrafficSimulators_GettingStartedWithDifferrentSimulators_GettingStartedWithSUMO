#!/usr/bin/python3
# This is a simple example to demonstrate how to command multiple AVs to drive based on input trajectories
# using traci module which allows interfacing SUMO with python. 
# Author: Wushuang
# Created on: 2022 07 20
# Revision history: 
# 2022 07 25- updated comments 
# 2022 07 26- added test script to exercise this function 
# For more information, please see https://sumo.dlr.de/docs/TraCI.html#examples

#   _____                   _       
#  |_   _|                 | |      
#    | |  _ __  _ __  _   _| |_ ___ 
#    | | | '_ \| '_ \| | | | __/ __|
#   _| |_| | | | |_) | |_| | |_\__ \
#  |_____|_| |_| .__/ \__,_|\__|___/
#              | |                  
#              |_|  
# inputFilePath: this is the csv file you want to use as commanded trajectories. This input should contain at least column vehicle_x and vehicle_y
#                format: csv
# timeStep: this is the time step you want to use in the simulation. If this input is not given, it uses the default value 1
#           format: string, such as "1"
# outputFilePath: this is the output file path of the simulation.
#           format: sumo outputs simulation as xml file. It can be then converted to csv file. 
# simConFigFilePath: this is the simulation configuration file that you want to run.  
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

def fcn_CommandVehTrajectory_MultiVeh(inputFilePath = './CommandSimInput.csv', timeStep="1",outputFilePath = "output.xml",simConFigFilePath = "./curvyRoad_irregularShape_multiVeh.sumocfg"):
    try:    
        Simulation_Flag = 0
        # user's input: what are the csv file you want to use as a command trajectory? The csv file should contain at least column vehicle_x and vehicle_y
        df = pd.read_csv(inputFilePath) 
        timestep_time = df["timestep_time"][df.index[df.vehicle_x.notnull()==True]]
        # get unique time stamps
        timestep_time_unique = timestep_time.unique()
        # get vehicle ID
        vehID_list =  df["vehicle_id"][df.index[df.vehicle_x.notnull()==True]]
        # what are the x and y position you want to command? 
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
        sumoCmd = [sumoBinary, "-c", simConFigFilePath,"--step-length",timeStep,"--start","--fcd-output",outputFilePath]
        # define beginning and end index of simulation 
        counter = np.array(df.index[df.vehicle_x.notnull()==True])[0]
        ind_end = np.array(df.index[df.vehicle_x.notnull()==True])[-1]
        # Then you start the simulation and connect to it with your script:
        traci.start(sumoCmd)
        
        while traci.simulation.getMinExpectedNumber() > 0:
            # get the position data
            # position = traci.vehicle.getPosition(veh_id)            
            
            # get current time stamp
            currentTimeStamp = timestep_time_unique[counter]   
            # get data element index that match this time stamp
            currentVehIDind = timestep_time[timestep_time == currentTimeStamp].index
            for veh_ind in currentVehIDind:
                # Iterate vehicle in the current time stamp. Let the vehicle to move to this position. 
                # Edge ID is left as "" and lane is left as "-1" since they are optional. 
                traci.vehicle.moveToXY(vehID_list[veh_ind],"","-1",commandedX[veh_ind],commandedY[veh_ind])
                # print out the data, including simulation time, vehicle id, position in X,Y. Please see more infomation at:https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-moveToXY 
                print(traci.simulation.getTime(),vehID_list[veh_ind],commandedX[veh_ind],commandedY[veh_ind])
            # run the simulation step
            traci.simulationStep()

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
    fcn_CommandVehTrajectory_MultiVeh(inputFilePath = './CommandSimInput.csv', timeStep="1",outputFilePath = "output.xml",simConFigFilePath = "./curvyRoad_irregularShape_multiVeh.sumocfg")


        