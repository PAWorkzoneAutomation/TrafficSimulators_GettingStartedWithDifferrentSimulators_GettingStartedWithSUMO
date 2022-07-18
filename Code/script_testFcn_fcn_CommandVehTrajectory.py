# This script is used to test the funciton fcn_CommandVehTrajectory.py
# For more information, please see fcn_CommandVehTrajectory.py
# Author: Wushuang Bai
# Revision history:
# 2022 06 29 - first write of the code
from fcn_CommandVehTrajectory import fcn_CommandVehTrajectory
# input file path
filePath = "commandTrajectoryInput.csv"
# time step used in seconds
timeStep = "1"
# output file path
outputFilePath = "commandTrajectoryOut1put.xml"
# call the function 
SimFlag = fcn_CommandVehTrajectory(filePath,timeStep,outputFilePath)
