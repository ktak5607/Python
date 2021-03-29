#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:      test if to and from measures match
#
# Author:      kevin.takala
#
# Created:     16/12/2014
# Copyright:   (c) kevin.takala 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import arcpy
from arcpy import env
import os
import arcpy.mapping as map
import datetime

#print "Program started at {0}".format(datetime.datetime.now())
arcpy.env.overwriteOutput = True
wrkspce = r"C:\Users\kevin.takala\Desktop\Arc_Proj\Maintenance_GIS\LRS.gdb"
featureClass = "testLRSdata2_1"
finalNSTable ="NSCOM3"
finalEWTable ="EWCOM3"
arcpy.env.workspace = wrkspce
fields = ['SHAPE@M', 'SHAPE@', 'RTE_NM', 'EDGE_RTE_KEY', 'TRANSPORT_EDGE_FROM_MSR', 'TRANSPORT_EDGE_TO_MSR']
###################################### Begin creating North Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "N_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("N_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("N_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("N_roads", "Key", "TEXT", 50)
arcpy.AddField_management("N_roads", 'TRANSPORT_EDGE_FROM_MSR', 'TEXT', 50)
arcpy.AddField_management("N_roads", 'TRANSPORT_EDGE_TO_MSR', 'TEXT', 50)
with arcpy.da.SearchCursor(featureClass, fields) as nSrchCrsr:
    with arcpy.da.InsertCursor('N_roads', fields) as nInsertCrsr:
        for row in nSrchCrsr:
            if ("NB" in str(row[2]) and "SC" in str(row[2])):
                nInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("N_roads", ["EDGE_RTE_KEY", "Key"]) as nUp:
    for row in nUp:
        row[1] = row[0].replace("NB", "_B")
        nUp.updateRow(row)
print "North Features Extracted"

###################################### Begin creating South Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "S_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("S_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("S_roads", "Key", "TEXT", 50)
arcpy.AddField_management("S_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("S_roads", 'TRANSPORT_EDGE_FROM_MSR', 'TEXT', 50)
arcpy.AddField_management("S_roads", 'TRANSPORT_EDGE_TO_MSR', 'TEXT', 50)
with arcpy.da.SearchCursor(featureClass, fields) as sSrchCrsr:
    with arcpy.da.InsertCursor('S_roads', fields) as sInsertCrsr:
        for row in sSrchCrsr:
            if ("SB" in str(row[2]) and "SC" in str(row[2])):
                sInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("S_roads", ["EDGE_RTE_KEY", "Key"]) as sUp:
    for row in sUp:
        row[1] = row[0].replace("SB", "_B")
        sUp.updateRow(row)

print "South Features Extracted"
################################## Begin join for North and South data
arcpy.MakeTableView_management ("N_Roads", "N_RoadsVw")
arcpy.MakeTableView_management ("S_Roads", "S_RoadsVw")
arcpy.AddJoin_management("N_RoadsVw", "Key", "S_RoadsVw", "Key")
arcpy.TableToTable_conversion("N_RoadsVw", wrkspce, finalNSTable)
arcpy.RemoveJoin_management("N_RoadsVw")

print "North and South Tables Joined"
arcpy.Delete_management("N_RoadsVw")
arcpy.Delete_management("S_RoadsVw")
arcpy.Delete_management("S_roads")
arcpy.Delete_management("N_roads")


################################# Begin calc to see if North and South measures match
arcpy.AddField_management(finalNSTable, 'TO_MEAS_MATCH', 'TEXT', '20')
arcpy.AddField_management(finalNSTable, 'FROM_MEAS_MATCH', 'TEXT', '20')

with arcpy.da.UpdateCursor(finalNSTable, ['TRANSPORT_EDGE_FROM_MSR', 'TRANSPORT_EDGE_TO_MSR', 'S_Roads_TRANSPORT_EDGE_FROM_MSR', 'S_Roads_TRANSPORT_EDGE_TO_MSR', 'FROM_MEAS_MATCH', 'TO_MEAS_MATCH']) as measCursor:
    for row in measCursor:
        if (str(row[2]) != "None"):

                if row[0] == row[2] :
                    row[4] = "YES"
                    measCursor.updateRow(row)
                elif row[0] != row[2]:
                    row[4] = "NO"
                    measCursor.updateRow(row)

        elif (str(row[2]) == "None"):
            row[4] = "INDET"
            measCursor.updateRow(row)


        if (str(row[3]) != "None"):

                if row[1] == row[3] :
                    row[5] = "YES"
                    measCursor.updateRow(row)
                elif row[1] != row[3]:
                    row[5] = "NO"
                    measCursor.updateRow(row)

        elif (str(row[3]) == "None"):
            row[5] = "INDET"
            measCursor.updateRow(row)
print "North and South Comparison Complete"
############################### End of calc to see if North and South measures match





################################## Begin creating East Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "E_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("E_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("E_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("E_roads", "Key", "TEXT", 50)
arcpy.AddField_management("E_roads", 'TRANSPORT_EDGE_FROM_MSR', 'TEXT', 50)
arcpy.AddField_management("E_roads", 'TRANSPORT_EDGE_TO_MSR', 'TEXT', 50)
with arcpy.da.SearchCursor(featureClass, fields) as eSrchCrsr:
    with arcpy.da.InsertCursor('E_roads', fields) as eInsertCrsr:
        for row in eSrchCrsr:
            if ("EB" in str(row[2]) and "SC" in str(row[2])):
                eInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("E_roads", ["EDGE_RTE_KEY", "Key"]) as eUp:
    for row in eUp:
        row[1] = row[0].replace("EB", "_B")
        eUp.updateRow(row)


print "East Features Extracted"

###################################### Begin creating West Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "W_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("W_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("W_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("W_roads", "Key", "TEXT", 50)
arcpy.AddField_management("W_roads", 'TRANSPORT_EDGE_FROM_MSR', 'TEXT', 50)
arcpy.AddField_management("W_roads", 'TRANSPORT_EDGE_TO_MSR', 'TEXT', 50)
with arcpy.da.SearchCursor(featureClass, fields) as wSrchCrsr:
    with arcpy.da.InsertCursor('W_roads', fields) as wInsertCrsr:
        for row in wSrchCrsr:
            if ("WB" in str(row[2]) and "SC" in str(row[2])):
                wInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("W_roads", ["EDGE_RTE_KEY", "Key"]) as wUp:
    for row in wUp:
        row[1] = row[0].replace("WB", "_B")
        wUp.updateRow(row)


print "West Features Extracted"

################################## Begin join for East and West data
arcpy.MakeTableView_management ("E_Roads", "E_RoadsVw")
arcpy.MakeTableView_management ("W_Roads", "W_RoadsVw")
arcpy.AddJoin_management("E_RoadsVw", "Key", "W_RoadsVw", "Key")
arcpy.TableToTable_conversion("E_RoadsVw", wrkspce, finalEWTable)
arcpy.RemoveJoin_management("E_RoadsVw")

print "East and West Tables Joined"

arcpy.Delete_management("E_RoadsVw")
arcpy.Delete_management("W_RoadsVw")
arcpy.Delete_management("W_roads")
arcpy.Delete_management("E_roads")




################################# Begin calc to see if East and West measures match
arcpy.AddField_management(finalEWTable, 'FROM_MEAS_MATCH', 'TEXT', '10')
arcpy.AddField_management(finalEWTable, 'TO_MEAS_MATCH', 'TEXT', '10')
with arcpy.da.UpdateCursor(finalEWTable, ['TRANSPORT_EDGE_FROM_MSR', 'TRANSPORT_EDGE_TO_MSR', 'W_Roads_TRANSPORT_EDGE_FROM_MSR', 'W_Roads_TRANSPORT_EDGE_TO_MSR', 'FROM_MEAS_MATCH', 'TO_MEAS_MATCH']) as measCursor:
    for row in measCursor:
        if (str(row[2]) != "None"):

                if row[0] == row[2] :
                    row[4] = "YES"
                    measCursor.updateRow(row)
                elif row[0] != row[2]:
                    row[4] = "NO"
                    measCursor.updateRow(row)

        elif (str(row[2]) == "None"):
            row[4] = "INDET"
            measCursor.updateRow(row)


        if (str(row[3]) != "None"):

                if row[1] == row[3] :
                    row[5] = "YES"
                    measCursor.updateRow(row)
                elif row[1] != row[3]:
                    row[5] = "NO"
                    measCursor.updateRow(row)

        elif (str(row[3]) == "None"):
            row[5] = "INDET"
            measCursor.updateRow(row)

print "East and West Comparison Complete"
#print "Program completed at {0}".format(datetime.datetime.now())

arcpy.AddMessage("VICTORY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

######################################################################################################################################################################











