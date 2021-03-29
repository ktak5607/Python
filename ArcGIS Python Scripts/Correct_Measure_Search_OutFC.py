"""
This program will search for roads with different M-values between the opposite routes.
First roads in the North and South and compared and then roads in the East and West are compared.
In the end a new field named MEAS_MATCH is added to the output table, with one of four values
for each route. The categories are YES, NO, INDET, and INCOMP ROADS. YES means that the M-values
matched, NO means they didn't match, INDET means that the M-value for one of the directions was NULL,
and INCOMP ROADS means that the roads didn't match correctly. A value of INDET is usually caused when
you have a one way street. INCOMP ROADS occurs when a false match occured. These usually occur in areas
where two roads overlap each other.

- Kevin Takala
"""
import arcpy
from arcpy import env
import os
import datetime


wrkspce = arcpy.GetParameter(0)
featureClass = arcpy.GetParameter(1)
finalNSTable = arcpy.GetParameterAsText(2)
finalEWTable = arcpy.GetParameterAsText(3)
arcpy.env.workspace = wrkspce
arcpy.env.overwriteOutput = True
fields = ['SHAPE@M', 'SHAPE@', 'RTE_NM','SHAPE@XY', 'EDGE_RTE_KEY', 'RTE_NBR']
###################################### Begin creating North Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "N_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("N_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("N_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("N_roads", "Key", "TEXT", 50)
arcpy.AddField_management("N_roads", "RTE_NBR", "LONG")
with arcpy.da.SearchCursor(featureClass, fields) as nSrchCrsr:
    with arcpy.da.InsertCursor('N_roads', fields) as nInsertCrsr:
        for row in nSrchCrsr:
            if ("NB" in str(row[2]) and "SC" in str(row[2])):
                nInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("N_roads", ["EDGE_RTE_KEY", "Key"]) as nUp:
    for row in nUp:
        row[1] = row[0].replace("NB", "_B")
        nUp.updateRow(row)


arcpy.FeatureVerticesToPoints_management("N_roads", "N_roads_points", "MID")


#search cursor for each point select each route from point name


rdsList = []
with arcpy.da.SearchCursor("N_roads_points", ["RTE_NBR"]) as search:
    i = 1
    for row in search:
        if row [0] in rdsList:
            continue
        elif row [0] not in rdsList:
            rdsList.append(row[0])
count = len(rdsList)
arcpy.AddMessage(count)

arcpy.CreateTable_management (wrkspce, "Npoints", "N_roads_points")
arcpy.AddField_management("Npoints", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("Npoints", "Key", "TEXT", 50)
arcpy.AddField_management("Npoints", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("Npoints", "RTE_NBR", "LONG")
arcpy.AddField_management("Npoints", "RID_N", "TEXT", 50)
arcpy.AddField_management("Npoints", "N_MEAS", "DOUBLE")

for rd in rdsList:
    arcpy.AddMessage(i)
    query = "RTE_NBR = {0}".format(rd)
    arcpy.MakeFeatureLayer_management("N_roads", "Nroadstemp", where_clause = query)
    arcpy.MakeFeatureLayer_management("N_roads_points", "Npointstemp", where_clause = query)
    arcpy.LocateFeaturesAlongRoutes_lr("Npointstemp", "Nroadstemp", "RTE_NM", "0 Feet", "locNRoads", "RID_N POINT N_MEAS", route_locations = "ALL",  distance_field = "NO_DISTANCE", in_fields = "FIELDS")
    arcpy.Append_management("locNRoads", "Npoints", "NO_TEST")
    i += 1
    arcpy.Delete_management("Nroadstemp")
    arcpy.Delete_management("Npointstemp")
time = str(datetime.datetime.now())
msg = "North features completed at {0}".format(time)
arcpy.AddMessage(msg)


######################################## Begin creating South Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "S_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("S_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("S_roads", "Key", "TEXT", 50)
arcpy.AddField_management("S_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("S_roads", "RTE_NBR", "LONG")
with arcpy.da.SearchCursor(featureClass, fields) as sSrchCrsr:
    with arcpy.da.InsertCursor('S_roads', fields) as sInsertCrsr:
        for row in sSrchCrsr:
            if ("SB" in str(row[2]) and "SC" in str(row[2])):
                sInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("S_roads", ["EDGE_RTE_KEY", "Key"]) as sUp:
    for row in sUp:
        row[1] = row[0].replace("SB", "_B")
        sUp.updateRow(row)


arcpy.FeatureVerticesToPoints_management("S_roads", "S_roads_points", "MID")


sRdsList = []
with arcpy.da.SearchCursor("S_roads_points", ["RTE_NBR"]) as search:
    i = 0
    for row in search:
        if row [0] in sRdsList:
            continue
        elif row [0] not in sRdsList:
            sRdsList.append(row[0])
count = len(sRdsList)
arcpy.AddMessage(count)


arcpy.CreateTable_management (wrkspce, "Spoints", "S_roads_points")
arcpy.AddField_management("Spoints", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("Spoints", "Key", "TEXT", 50)
arcpy.AddField_management("Spoints", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("Spoints", "RTE_NBR", "LONG")
arcpy.AddField_management("Spoints", "RID_S", "TEXT", 50)
arcpy.AddField_management("Spoints", "S_MEAS", "DOUBLE")

for rd in sRdsList:
    arcpy.AddMessage(i)
    query = "RTE_NBR = {0}".format(rd)
    arcpy.MakeFeatureLayer_management("S_roads", "Sroadstemp", where_clause = query)
    arcpy.MakeFeatureLayer_management("S_roads_points", "Spointstemp", where_clause = query)
    arcpy.LocateFeaturesAlongRoutes_lr("Spointstemp", "Sroadstemp", "RTE_NM", "0 Feet", "locSRoads", "RID_S POINT S_MEAS", route_locations = "ALL",  distance_field = "NO_DISTANCE", in_fields = "FIELDS")
    arcpy.Append_management("locSRoads", "Spoints", "NO_TEST")
    arcpy.Delete_management("Spointstemp")
    arcpy.Delete_management("Sroadstemp")
    i += 1

time = str(datetime.datetime.now())
msg = "South features completed at {0}".format(time)
arcpy.AddMessage(msg)


################################## Begin join for North and South data
arcpy.MakeTableView_management ("Npoints", "locNRdsVw")
arcpy.MakeTableView_management ("Spoints", "locSRdsVw")
arcpy.AddJoin_management("locNRdsVw", "Key", "locSRdsVw", "Key")
arcpy.TableToTable_conversion("locNRdsVw", wrkspce, finalNSTable)
arcpy.RemoveJoin_management("locNRdsVw")

arcpy.Delete_management("locNRdsVw")
arcpy.Delete_management("locSRdsVw")
#arcpy.Delete_management("S_roads")
#arcpy.Delete_management("N_roads")
#arcpy.Delete_management("N_roads_points")
#arcpy.Delete_management("S_roads_points")

fclist = arcpy.ListFields(finalNSTable)
for field in fclist:

    arcpy.AddMessage(field.name)
################################# Begin calc to see if North and South measures match
arcpy.AddField_management(finalNSTable, 'MEAS_MATCH', 'TEXT', '20')
with arcpy.da.UpdateCursor(finalNSTable, ['N_MEAS', 'Spoints_S_MEAS', 'MEAS_MATCH', "RID_N", "Spoints_RID_S"]) as measCursor:
    for row in measCursor:
            if (str(row[1]) != "None"):
                if row[3].replace("NB", "_B") == row[4].replace("SB", "_B"):

                    if row[0] == row[1] :
                        row[2] = "YES"
                        measCursor.updateRow(row)
                    elif row[0] != row[1]:
                        row[2] = "NO"
                        measCursor.updateRow(row)

                elif row[3].replace("NB", "_B") != row[4].replace("SB", "_B"):
                    row[2] = "INCOMP ROADS"
                    measCursor.updateRow(row)

            elif (str(row[1]) == "None"):
                row[2] = "INDET"
                measCursor.updateRow(row)

################################# End of calc to see if North and South measures match
##

##


################################## Begin creating East Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "E_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("E_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("E_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("E_roads", "Key", "TEXT", 50)
arcpy.AddField_management("E_roads", "RTE_NBR", "LONG")
with arcpy.da.SearchCursor(featureClass, fields) as eSrchCrsr:
    with arcpy.da.InsertCursor('E_roads', fields) as eInsertCrsr:
        for row in eSrchCrsr:
            if ("EB" in str(row[2]) and "SC" in str(row[2])):
                eInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("E_roads", ["EDGE_RTE_KEY", "Key"]) as eUp:
    for row in eUp:
        row[1] = row[0].replace("EB", "_B")
        eUp.updateRow(row)
arcpy.FeatureVerticesToPoints_management("E_roads", "E_roads_points", "MID")

eRdsList = []
with arcpy.da.SearchCursor("E_roads_points", ["RTE_NBR"]) as search:
    i = 1
    for row in search:
        if row [0] in eRdsList:
            continue
        elif row [0] not in eRdsList:
            eRdsList.append(row[0])
count = len(eRdsList)
arcpy.AddMessage(count)

arcpy.CreateTable_management (wrkspce, "Epoints", "E_roads_points")
arcpy.AddField_management("Epoints", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("Epoints", "Key", "TEXT", 50)
arcpy.AddField_management("Epoints", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("Epoints", "RTE_NBR", "LONG")
arcpy.AddField_management("Epoints", "RID_E", "TEXT", 50)
arcpy.AddField_management("Epoints", "E_MEAS", "DOUBLE")

for rd in eRdsList:
    arcpy.AddMessage(i)
    query = "RTE_NBR = {0}".format(rd)
    arcpy.MakeFeatureLayer_management("E_roads", "Eroadstemp", where_clause = query)
    arcpy.MakeFeatureLayer_management("E_roads_points", "Epointstemp", where_clause = query)
    arcpy.LocateFeaturesAlongRoutes_lr("Epointstemp", "Eroadstemp", "RTE_NM", "0 Feet", "locERoads", "RID_E POINT E_MEAS", route_locations = "ALL",  distance_field = "NO_DISTANCE", in_fields = "FIELDS")
    arcpy.Append_management("locERoads", "Epoints", "NO_TEST")
    i += 1
    arcpy.Delete_management("Eroadstemp")
    arcpy.Delete_management("Epointstemp")
time = str(datetime.datetime.now())
msg = "East features completed at {0}".format(time)
arcpy.AddMessage(msg)





###################################### Begin creating West Bound Roads data
arcpy.CreateFeatureclass_management(wrkspce, "W_roads", 'POLYLINE', has_m = 'ENABLED', spatial_reference = arcpy.Describe(featureClass).spatialReference)
arcpy.AddField_management("W_roads", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("W_roads", "Key", "TEXT", 50)
arcpy.AddField_management("W_roads", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("W_roads", 'RTE_NBR', 'LONG')
with arcpy.da.SearchCursor(featureClass, fields) as wSrchCrsr:
    with arcpy.da.InsertCursor('W_roads', fields) as wInsertCrsr:
        for row in wSrchCrsr:
            if ("WB" in str(row[2]) and "SC" in str(row[2])):
                wInsertCrsr.insertRow((row[0], row[1], row[2], row[3], row[4], row[5]))
with arcpy.da.UpdateCursor("W_roads", ["EDGE_RTE_KEY", "Key"]) as wUp:
    for row in wUp:
        row[1] = row[0].replace("WB", "_B")
        wUp.updateRow(row)
arcpy.FeatureVerticesToPoints_management("W_roads", "W_roads_points", "MID")

wRdsList = []
with arcpy.da.SearchCursor("W_roads_points", ["RTE_NBR"]) as search:
    i = 1
    for row in search:
        if row [0] in wRdsList:
            continue
        elif row [0] not in wRdsList:
            wRdsList.append(row[0])
count = len(wRdsList)
arcpy.AddMessage(count)

arcpy.CreateTable_management (wrkspce, "Wpoints", "W_roads_points")
arcpy.AddField_management("Wpoints", 'EDGE_RTE_KEY', 'TEXT', 50)
arcpy.AddField_management("Wpoints", "Key", "TEXT", 50)
arcpy.AddField_management("Wpoints", 'RTE_NM', 'TEXT', 50)
arcpy.AddField_management("Wpoints", "RTE_NBR", "LONG")
arcpy.AddField_management("Wpoints", "RID_W", "TEXT", 50)
arcpy.AddField_management("Wpoints", "W_MEAS", "DOUBLE")

for rd in wRdsList:
    arcpy.AddMessage(i)
    query = "RTE_NBR = {0}".format(rd)
    arcpy.MakeFeatureLayer_management("W_roads", "Wroadstemp", where_clause = query)
    arcpy.MakeFeatureLayer_management("W_roads_points", "Wpointstemp", where_clause = query)
    arcpy.LocateFeaturesAlongRoutes_lr("Wpointstemp", "Wroadstemp", "RTE_NM", "0 Feet", "locWRoads", "RID_W POINT W_MEAS", route_locations = "ALL",  distance_field = "NO_DISTANCE", in_fields = "FIELDS")
    arcpy.Append_management("locWRoads", "Wpoints", "NO_TEST")
    arcpy.Delete_management("Wroadstemp")
    arcpy.Delete_management("Wpointstemp")
    i += 1
time = str(datetime.datetime.now())
msg = "West features completed at {0}".format(time)
arcpy.AddMessage(msg)


################################## Begin join for East and West data
arcpy.MakeTableView_management ("Epoints", "locERdsVw")
arcpy.MakeTableView_management ("Wpoints", "locWRdsVw")
arcpy.AddJoin_management("locERdsVw", "Key", "locWRdsVw", "Key")
arcpy.TableToTable_conversion("locERdsVw", wrkspce, finalEWTable)
arcpy.RemoveJoin_management("locERdsVw")

arcpy.Delete_management("locERdsVw")
arcpy.Delete_management("locWRdsVw")
##arcpy.Delete_management("W_roads")
##arcpy.Delete_management("E_roads")
#arcpy.Delete_management("E_roads_points")
#arcpy.Delete_management("W_roads_points")




################################# Begin calc to see if East and West measures match
arcpy.AddField_management(finalEWTable, 'MEAS_MATCH', 'TEXT', '10')
with arcpy.da.UpdateCursor(finalEWTable, ['E_MEAS', 'Wpoints_W_MEAS', 'MEAS_MATCH', "RID_E", "Wpoints_RID_W"]) as measCursor:
    for row in measCursor:

            if (str(row[1]) != "None"):
                if row[3].replace("EB", "_B") == row[4].replace("WB", "_B"):

                    if row[0] == row[1]:
                        row[2] = "YES"
                        measCursor.updateRow(row)
                    elif row[0] != row[1]:
                        row[2] = "NO"
                        measCursor.updateRow(row)

                elif row[3].replace("EB", "_B") != row[4].replace("WB", "_B"):
                    row[2] = "INCOMP ROADS"
                    measCursor.updateRow(row)

            elif (str(row[1]) == "None"):
                row[2] = "INDET"
                measCursor.updateRow(row)


arcpy.AddMessage("VICTORY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
######################################################################################################################################################################











