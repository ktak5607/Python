"""
This script will search a feature layer for vertices with a null M-value.
In order to run this script in ArcGIS you need to add a script to a toolbox
and create two parameters in the properties box. The first should be workspace,
and the second should be a feature class. For more info on how to do this see
the ArcGIS online help.

- Kevin Takala
"""

import arcpy
from arcpy import env
import os
import numpy as np
arcpy.env.overwriteOutput = True
#Get the geodatabase to store the table in
env = arcpy.GetParameterAsText(0)
#Get the feature class to look through
featureClass = arcpy.GetParameter(1)
#Get the Spatial Reference for the output feature class
finalFCName = arcpy.GetParameterAsText(2)

#Set the workspace to the geodatabase
arcpy.env.workspace = env

#Create a numpy array from the points that make up the feature class, and store the OID, M value, and X,Y coordinates
array = arcpy.da.FeatureClassToNumPyArray(featureClass,["OID@", "SHAPE@XY", "SHAPE@M"], explode_to_points = True)

#Create an empty pyton list
outArray = []

#Iterate through the numpy array
for i in np.nditer(array):
        #Check the M Value of the point
        if(str(i["SHAPE@M"]) == "nan"):
                #If the M value is null add it to the python list
                outArray.append(i)

#check to see if there were any Null M values
if len(outArray) == 0:
        #None were found
        arcpy.AddMessage("No M values are Null.")

elif len(outArray) != 0:
        # There were Null M vaues

        #Create a new numpy array from the python list, create the column titles, and set the format for each column
        outNpArray = np.array(outArray, np.dtype([('Original_OID', np.int32), ('X_Coordinate', np.float64), ('Y_Coordinate', np.float64)]))

        finalFC = str(env) + "\\" + str(finalFCName)
        #Create the new table from the new numpy array
        arcpy.da.NumPyArrayToFeatureClass(outNpArray, finalFC, ['X_Coordinate', 'Y_Coordinate'], arcpy.Describe(featureClass).spatialReference)


