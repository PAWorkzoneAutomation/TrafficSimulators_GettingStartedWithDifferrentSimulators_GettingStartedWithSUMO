# This script is used to test the funciton fcn_CommandVehTrajectory_MultiVeh.py
# For more information, please see fcn_CommandVehTrajectory_MultiVeh.py
# Author: Wushuang Bai
# Revision history:
# 2022 07 26 - first write of the code
from fcn_CommandVehTrajectory_MultiVeh import fcn_CommandVehTrajectory_MultiVeh
# input file path
inputFilePath = "/media/wushuang/SeagateMac/SUMOWork/curvyRoad_irregularShape_multiVeh/curvyRoad_irregularShape_multiVeh_InputTrajectory.csv"
# time step used 
timeStep = "1"
# output file path
outputFilePath = "/media/wushuang/SeagateMac/SUMOWork/curvyRoad_irregularShape_multiVeh/curvyRoad_irregularShape_multiVeh_OutputTrajectory.xml"
# simulation configuration file path
simConfigFilePath = "/media/wushuang/SeagateMac/SUMOWork/curvyRoad_irregularShape_multiVeh/curvyRoad_irregularShape_multiVeh.sumocfg"
# call the function 
SimFlag = fcn_CommandVehTrajectory_MultiVeh(inputFilePath,timeStep,outputFilePath,simConfigFilePath)

