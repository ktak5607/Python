import arcpy
from arcpy import env
import os
import re
arcpy.env.overwriteOutput = True

featureClass = arcpy.GetParameter(0)
filePath = arcpy.GetParameterAsText(1)
saveFilePath = filePath + "\\test.txt"
saveFile = open (saveFilePath, 'a')
with arcpy.da.SearchCursor(featureClass, ['RTE_NM']) as mCursor:
    for row in mCursor:
        #if(row[0] == "NULL"):
            try:
                arcpy.AddMessage("writing to file")
                saveFile.write("works")
            except:
                msg = arcpy.GetMessages(2)
                arcpy.AddError(msg)
saveFile.close()
#arcpy.Delete_management("temp")
######look at select analysis tool!!!!!!!!!!!


