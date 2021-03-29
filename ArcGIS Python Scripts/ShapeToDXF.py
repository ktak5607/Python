# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 10:26:36 2019

@author: kevin.takala
"""

import arcpy
import os
import re


def Clip(folder):
    for file in os.listdir(folder):
        if (file.endswith(".shp")) and ("Clip" in os.path.basename(file) == False):
            arcpy.Clip_analysis(file, "Clip_Boundary.shp", folder + "\\" + os.path.basename(file) + "Clip.shp")
            
def Reproject(sr, folder):
    for file in os.listdir(folder):
        if file.endswith(".shp"):
            name = os.path.basename(file)
            desc = arcpy.Describe(file)
            if "Clip" in name and (desc.SpatialReference.name != "NAD 1983 2011 StatePlane Virginia North FIPS 4501 Ft US" or desc.SpatialReference.name != "NAD 1983 2011 StatePlane Virginia North FIPS 4501 Ft US"):
                outCoordSys = arcpy.SpatialReference(sr)
                arcpy.Project_management(file, name + "SP.shp", outCoordSys )

def Export(folder):
    for fc in arcpy.ListFeatureClasses(fc):
        name = os.path.basename(file)
        if "Clip" in name and "SP" in name:
            arcpy.ExportCAD_conversion(file, "DXF_R2010", os.path.basename(file))


            
print ("This tool is for converting GIS shapefile data to dxf files.\nIn order for it to run properly you will need to have a shape file named Clip_Boundary in the folder where your GIS data is.")
folder = raw_input("Enter the folder path where the files are stored. ")
coorSystem = raw_input("Enter the coorinate system(north or south). ")
arcpy.env.workspace = folder
Clip(folder)
if(coorSystem == "north"):
    reproject("NAD 1983 2011 StatePlane Virginia North FIPS 4501 Ft US", folder)
elif(coorSystem == "south"):
    Reproject("NAD 1983 2011 StatePlane Virginia North FIPS 4501 Ft US", folder)
Export(folder)

        
