#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kevin.takala
#
# Created:     19/12/2014
# Copyright:   (c) kevin.takala 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
from arcpy import env
import os
import traceback


folder = arcpy.GetParameterAsText(0)
arcpy.env.workspace = folder
arcpy.env.outputMFlag = "Disabled"
arcpy.env.overwriteOutput = True
sr = arcpy.SpatialReference(3969)
for kmz in os.listdir(folder):
    if(kmz.endswith(".kmz") or kmz.endswith(".kml")):
        fileName = os.path.basename(kmz)
        fileNameOnly = os.path.splitext(fileName)[0]
        outWKT = folder + "\\" + fileNameOnly + ".wkt"
        try:
            
            outLyr = arcpy.KMLToLayer_conversion(folder + "\\" + kmz, folder)
            print("layer created")
            gdb = folder + "\\" +  fileNameOnly + ".gdb" 
            arcpy.env.workspace = gdb
            lccShp = arcpy.Project_management(r"\Placemarks\Polygons", "lccShp", sr)
            snglPrt = arcpy.MultipartToSinglepart_management(lccShp, "snglPrt")
            writeWKT = open(outWKT, 'w')
            for row in arcpy.da.SearchCursor(snglPrt, ["SHAPE@WKT"]):
                wktLine = row[0]
                wktPlyRep = wktLine.replace("MULTIPOLYGON Z", "$shape = 'polygon")
                wktParRep = wktPlyRep.replace(" (((", "((\n    ")
                wktParRep2 = wktParRep.replace(")))", "\n))'")
                writeWKT.write(wktParRep2)
            writeWKT.close()     
            arcpy.env.workspace = folder

        except:
            errorLog = folder + "\\errorlog.txt"
            errorWriter = open(errorLog, 'a')
            errorWriter.write(fileNameOnly + "\n")
            errorWriter.write(traceback.format_exc())
            errorWriter.close()


             

