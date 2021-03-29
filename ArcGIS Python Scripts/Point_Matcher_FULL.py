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
import arcpy.mapping as map
import math

gDB = arcpy.GetParameterAsText(0)
oldFC = arcpy.GetParameter(1)
newFC = arcpy.GetParameter(2)
dist = arcpy.GetParameter(3)
outFC = arcpy.GetParameter(4)

arcpy.env.workspace = gDB
arcpy.env.overwriteOutput = True

try:
    arcpy.CopyFeatures_management(newFC, outFC)
    arcpy.AddField_management(outFC, "CORRECTED", "TEXT", 10)

    fields = arcpy.ListFields(outFC, field_type = "STRING")
    newFields = ["FKEY", "SHAPE@XY", "SHAPE@", "CORRECTED"]
    oldFields = ["FKEY", "SHAPE@XY", "SHAPE@"]
    i = 0
    for field in fields:
        print field.name
        if field.name == "CRS_LOC":

            newFields.insert(2, "CRS_LOC")
            oldFields.insert(2, "CRS_LOC")
            i = 1
            break
        elif field.name == "CRSLOC":
            newFields.insert(2, "CRSLOC")
            oldFields.insert(2, "CRSLOC")
            i = 1
            break
        elif field.name == "CSG_RS_LOC":
            newFields.insert(2, "CSG_RS_LOC")
            oldFields.insert(2, "CSG_RS_LOC")
            i = 1
            break
        elif field.name == "Curb_Ends_CRS_LOC":
            print "in curb ends crs loc"
            newFields.insert(2, "CURB_ENDS_CRS_LOC")
            oldFields.insert(2, "CURB_ENDS_CRS_LOC")
            i = 1
            break
        elif field.name == "Curb_Starts_CRS_LOC":
            newFields.insert(2, "CURB_STARTS_CRS_LOC")
            oldFields.insert(2, "CURB_STARTS_CRS_LOC")
            i = 1
            break
        elif field.name == "Guardrail_Ends_CRS_LOC":
            newFields.insert(2, "Gaurdrail_Ends_CRS_LOC")
            oldFields.insert(2, "Gaurdrail_Ends_CRS_LOC")
            i = 1
            break
    arcpy.MakeFeatureLayer_management(outFC, "temp")
    arcpy.MakeFeatureLayer_management(oldFC, "oldtemp")
    k = 0
    unit = "degree"
    if arcpy.Describe(newFC).spatialReference.type == "Geographic":
        unit = "degree"
    elif arcpy.Describe(newFC).spatialReference.type == "Projected":
        if arcpy.Describe(newFC).spatialReference.linearUnitName == "Meter":
            unit = "meter"
        elif arcpy.Describe(newFC).spatialReference.linearUnitName == "Feet":
            unit = "feet"
        elif arcpy.Describe(newFC).spatialReference.linearUnitName == "Kilometer":
            unit = "kilometer"

    if i == 0:
        arcpy.AddMessage("WARNING: No Direction Field Found.\n Matching will be done only on FKEY values.")
        with arcpy.da.SearchCursor("oldtemp", oldFields) as oldCursor:
            with arcpy.da.UpdateCursor("temp", newFields) as newCursor:
                for newRow in newCursor:
                    for oldRow in oldCursor :
                        if newRow[0] == oldRow[0]:
                            if unit == "degree":
                                oldX = (oldRow[1][0] * (10000/90)) * 3280.4
                                oldY = (oldRow[1][1] * (10000/90)) * 3280.4
                                newX = (newRow[1][0] * (10000/90)) * 3280.4
                                newY = (newRow[1][1] * (10000/90)) * 3280.4
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[2] = oldRow[2]
                                    newRow[3] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1

                            elif unit == "feet":
                                oldX = oldRow[1][0]
                                oldY = oldRow[1][1]
                                newX = newRow[1][0]
                                newY = newRow[1][1]
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[2] = oldRow[2]
                                    newRow[3] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1

                            elif unit == "meter":
                                oldX = oldRow[1][0] * 0.3048
                                oldY = oldRow[1][1] * 0.3048
                                newX = newRow[1][0] * 0.3048
                                newY = newRow[1][1] * 0.3048
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[2] = oldRow[2]
                                    newRow[3] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1

                            elif unit == "kilometer":
                                oldX = oldRow[1][0] * 0.0003048
                                oldY = oldRow[1][1] * 0.0003048
                                newX = newRow[1][0] * 0.0003048
                                newY = newRow[1][1] * 0.0003048
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[2] = oldRow[2]
                                    newRow[3] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1
                    else:
                        oldCursor.reset()
                        continue
                    oldCursor.reset()

    elif i == 1:
        msg = "{0} is the direction field being used.\n".format(newFields[2])
        arcpy.AddMessage(msg)
        with arcpy.da.SearchCursor("oldtemp", oldFields) as oldCursor:
            with arcpy.da.UpdateCursor("temp", newFields) as newCursor:
                for newRow in newCursor:
                    for oldRow in oldCursor :
                        if(newRow[0] == oldRow[0]) and (newRow[2] == oldRow[2]):
                            if unit == "degree":
                                oldX = (oldRow[1][0] * (10000/90)) * 3280.4
                                oldY = (oldRow[1][1] * (10000/90)) * 3280.4
                                newX = (newRow[1][0] * (10000/90)) * 3280.4
                                newY = (newRow[1][1] * (10000/90)) * 3280.4
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[3] = oldRow[3]
                                    newRow[4] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1

                            elif unit == "feet":
                                oldX = oldRow[1][0]
                                oldY = oldRow[1][1]
                                newX = newRow[1][0]
                                newY = newRow[1][1]
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[3] = oldRow[3]
                                    newRow[4] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1

                            elif unit == "meter":
                                oldX = oldRow[1][0] * 0.3048
                                oldY = oldRow[1][1] * 0.3048
                                newX = newRow[1][0] * 0.3048
                                newY = newRow[1][1] * 0.3048
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[3] = oldRow[3]
                                    newRow[4] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1

                            elif unit == "kilometer":
                                oldX = oldRow[1][0] * 0.0003048
                                oldY = oldRow[1][1] * 0.0003048
                                newX = newRow[1][0] * 0.0003048
                                newY = newRow[1][1] * 0.0003048
                                distance = math.sqrt(math.pow((newX-oldX), 2) + math.pow((newY - oldY), 2))
                                if distance > dist:
                                    newRow[1] = oldRow[1]
                                    newRow[3] = oldRow[3]
                                    newRow[4] = "YES"
                                    newCursor.updateRow(newRow)
                                    k += 1
                    else:
                        oldCursor.reset()
                        continue
                    oldCursor.reset()

    with arcpy.da.UpdateCursor (outFC, ["CORRECTED"]) as finalUp:
        for row in finalUp:
            if str(row[0]) == "None":
                row[0]= "NO"
                finalUp.updateRow(row)

    msg = "The number of features moved was: {0}".format(str(k))
    arcpy.AddMessage(msg)
    arcpy.Delete_management("temp")
    arcpy.Delete_management("oldtemp")
    arcpy.AddMessage("VICTORY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

except Exception as e:
    #tb = sys.exc_info()[2]
    #tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    #
    #pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    #msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    # Return python error messages for use in script tool or Python Window
    #
    #arcpy.AddError(pymsg)
    #arcpy.AddError(msgs)
    arcpy.AddMessage("Error: \n")
    arcpy.AddMessage(e)
