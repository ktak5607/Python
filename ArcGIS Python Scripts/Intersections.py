#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      kevin.takala
#
# Created:     17/12/2014
# Copyright:   (c) kevin.takala 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
import os
import sys
import traceback
wrkspc = r"C:\Users\kevin.takala\Desktop\Arc_Proj\Maintenance_GIS\LRS_INTR.gdb" #arcpy.GetParameter(0)
lrs = r"C:\Users\kevin.takala\Desktop\Arc_Proj\Maintenance_GIS\LRS_INTR.gdb\testLRSdataSmall" #arcpy.GetParameter(1)
interFC = r"C:\Users\kevin.takala\Desktop\Arc_Proj\Maintenance_GIS\LRS_INTR.gdb\SDE_VDOT_INTERSECTION_W_XY" #arcpy.GetParameter(2)
outFC = "test"
arcpy.env.workspace = wrkspc
arcpy.env.overwriteOutput = True
try:
    rteQuery = "RTE_NM = MASTER_RTE_NM"
    fromQuery = "FROM_INTERSECTION_ID IS NOT NULL"
    toQuery = "TO_INTERSECTION_ID IS NOT NULL"
    arcpy.FeatureClassToFeatureClass_conversion(lrs, wrkspc, "mstrRTE", where_clause = rteQuery)
    arcpy.FeatureClassToFeatureClass_conversion("mstrRTE",  wrkspc, "fromInter", where_clause = fromQuery)
    arcpy.FeatureClassToFeatureClass_conversion("mstrRTE", wrkspc, "toInter", where_clause = toQuery)
    ##outFrom = wrkspc + "\\" + "fromLRS"
    ##arcpy.CopyFeatures_management("fromInter", outFrom)
    arcpy.Delete_management("mstrRTE")

    fromFields = arcpy.ListFields("fromInter")
    fromFromFields = []
    fromToFields = []
    for field in fromFields:
        if "FROM" in field.name:
            fromFromFields.append(field)

        elif "TO" in field.name:

            fromToFields.append(field)
        else:
           continue

    for toField in fromToFields:
        arcpy.DeleteField_management("fromInter", toField.name)

    for fromField in fromFromFields:
        newName = fromField.name.replace("FROM_", "")
        arcpy.AlterField_management("fromInter", fromField.name, newName, newName)


    toFields = arcpy.ListFields("toInter")
    toToFields = []
    toFromFields = []
    for field in toFields:
        if "TO" in field.name:
            toToFields.append(field)

        elif "FROM" in field.name:
            toFromFields.append(field)

        else:
            continue
    print "fields categorized"
    for fromField in toFromFields:

        arcpy.DeleteField_management("toInter", fromField.name)
    print "fields deleted"
    for toField in toToFields:
        newName = toField.name.replace("TO_", "")
        arcpy.AlterField_management("toInter", toField.name, newName, newName)
    print "fields renamed"

    arcpy.Merge_management (["fromInter", "toInter"], "mergedRtes")
    print "Merged"
##    fields = arcpy.ListFields("mergedRtes", "INTERSECTION_ID")
##    for field in fields:
##        field.type = "Integer"
    arcpy.DeleteIdentical_management ("mergedRtes", ["RTE_NM", "Intersection_ID"])
    print "Identical features deleted"

    arcpy.CreateRelationshipClass_management(interFC, "mergedRtes", outFC, "SIMPLE", "Attributes from mergedRtes", "Atts and Features from intersectionsFC", "NONE", "ONE_TO_MANY",  origin_primary_key="INTERSECTION_ID", origin_foreign_key="INTERSECTION_ID")
    print "Complete"



except Exception as e:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]


    # Concatenate information together concerning the error into a message string
    #
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"

    # Return python error messages for use in script tool or Python Window
    #
    #print(pymsg)
    #print(msgs)

    # Print Python error messages for use in Python / Python Window
    #
    print pymsg + "\n"
    print msgs
    del e
    del tb
    del tbinfo
    del pymsg
    del msgs
