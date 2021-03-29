"""
This tool allows you to clip a feature class
into its individual county pieces by district.
If you need to clip multiple feature classes
with the temp keyword in them use the Batch
Clip With Temp tool.
"""
import arcpy
from arcpy import env
from arcpy.sa import *
import os

#The method that will preform the clip
def ClipFC():
    #a search cursor for the counties feature class
    countiesCursor = arcpy.SearchCursor(countiesFC, expression)
    arcpy.AddMessage("entering county search loop")
    countyNameNS = ""
    #Iterate through the counties feature class and clip
    #the desired featureclass to each county in the district
    for county in countiesCursor:
        #get the county name
        countyName = str(county.Name)
        #check to see if there is a space in the county name
        #if there is Arc will throw an error because it can't
        #handle spaces
        if " " in countyName:
            arcpy.AddMessage("space in name")
            #replace space with an underbar
            countyNameNS = countyName.replace(" ", "_")
            arcpy.AddMessage(countyNameNS)
            outFCName = countyNameNS + "_" + fcType
        else:
            outFCName = countyName + "_" + fcType
        arcpy.AddMessage(outFCName)
        #get the polygon to use to clip the feature class
        clipFeature = county.Shape
        #try to clip the feautre class
        try:
            arcpy.Clip_analysis(featureClassToClip, clipFeature, outFCName)
            arcpy.AddMessage("clip complete")
        except:
            arcpy.AddMessage("An error occured. Most likely the featureclass already exits.")
            continue
        
#end ClipFC method        

        
#set the file override to true so that temp features can be deleted
#arcpy.env.overwriteOutput = True

#make sure the spatial analyst extension is checked
arcpy.CheckOutExtension("Spatial")

#get the geodatabase to store the new feaures
geoDatabase = arcpy.GetParameter(0)
#get the feature class that will be clipped
featureClassToClip = arcpy.GetParameter(1)

#set the active workspace to the desired geodatabase
arcpy.env.workspace = geoDatabase

#get the counties featureclass
countiesFC = arcpy.GetParameter(2)
#get the feature class type i.e. roads, rivers/streams, or waterbodies
fcType = arcpy.GetParameterAsText(3)
#get the SQL expression that will define the district
expression = arcpy.GetParameter(4)
#call the ClipFC method
ClipFC()

