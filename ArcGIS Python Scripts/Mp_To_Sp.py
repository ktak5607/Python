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
gdb = r"C:\Users\kevin.takala\Desktop\Arc_Proj\Maintenance_GIS\test.gdb"#arcpy.GetParameter(0)
arcpy.env.workspace = gdb
try:
    listfc = arcpy.ListFeatureClasses()
    print listfc
    for fc in listfc:
        if arcpy.Describe(fc).shapeType == "MultiPoint":
            name = fc + "_SP"
            arcpy.MultipartToSinglepart_management(fc, name)
        else:
            continue
except Exception as e:
    print e