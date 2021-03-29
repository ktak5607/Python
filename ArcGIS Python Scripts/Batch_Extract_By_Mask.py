import arcpy
from arcpy import env
from arcpy.sa import *
import os


def ExtractByMask():
    photoSearch = arcpy.SearchCursor(featureClassName)
    #go through the workspace
    for file in os.listdir(inWs):
        arcpy.AddMessage("in for")
        imageBaseName = os.path.basename(file)
        imageName = os.path.splitext(imageBaseName)[0]
        if file.endswith(".tif"):
            for photo in photoSearch:
                arcpy.AddMessage(photo.Roll_Num)
                if (str(photo.Roll_Num) in imageName):
                    arcpy.AddMessage("it's in")
                    extractedPhoto = ExtractByMask(file, photo.SHAPE)
                    extractedPhoto.save ("shawblagoo.tif")
                        
                else:
                    arcpy.AddMessage("in else")
                    continue
        else:
           continue
    

     
#set the file override to true so that temp features can be deleted
arcpy.env.overwriteOutput = True

#make sure the spatial analyst extension is checked
arcpy.CheckOutExtension("Spatial")

#get user defined workspace
inWs = arcpy.GetParameterAsText(0)

#get the new featureclass to add data to
featureClassName = arcpy.GetParameter(1)

#set the active workspace
arcpy.env.workspace = inWs

ExtractByMask()
