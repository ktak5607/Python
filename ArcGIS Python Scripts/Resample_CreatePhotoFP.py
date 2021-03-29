import arcpy
from arcpy import env
from arcpy.sa import *
import os
import sys
import datetime
import traceback

#set the file override to true so that temp features can be deleted
arcpy.env.overwriteOutput = True

#make sure the spatial analyst extension is checked
arcpy.CheckOutExtension("Spatial")
try:
    print str(datetime.datetime.now())
    #get user defined workspace
    inWs = r"C:\Users\kevin.takala\Desktop\Arc_Proj\test"#arcpy.GetParameterAsText(0)

    #get the new featureclass to add data to
    featureClassName = "test"#arcpy.GetParameter(1)
    featureClassFolder = inWs + "\\test.gdb"
    #get the values for the new fields
    rollNum = 142 #arcpy.GetParameter(2)
    startPhotoNum = 130 #arcpy.GetParameter(3)
    endPhotoNum = 131 #arcpy.GetParameter(4)
    date = "12/12/12" #arcpy.GetParameter(5)
    flownBy = "rice" #arcpy.GetParameter(6)
    scale = "2:50" #arcpy.GetParameter(7)

    #set the active workspace
    arcpy.env.workspace = inWs
    print arcpy.env.workspace
    os.chdir(inWs)
    #create a new folder for the new resampled images if it doesn't already exist
    outWs = os.path.join (inWs, "resampled_images")
    if not os.path.exists(outWs):
        os.makedirs(outWs)
    print outWs

    arcpy.CreateFeatureclass_management(featureClassFolder, featureClassName, "POLYGON", spatial_reference =  2283 )
    arcpy.env.workspace = featureClassFolder
    fields = ["Roll_Num", "Photo_Num", "Date", "Flown_By", "Scale"]

    #iterate through the fields
    for field in fields:

        #if it's the date field add it as a date feature
        if (field == "Date"):
            arcpy.AddField_management(featureClassName, field, "DATE")

        #if it's the flownby or scale fields add them as text
        elif (field == "Flown_By" or field == "Scale"):
            arcpy.AddField_management(featureClassName, field, "TEXT", "", "", "15")

        #the photo number and roll number are added as longs
        else:
            arcpy.AddField_management(featureClassName, field, "LONG", 10)

    arcpy.env.workspace = inWs
    #def ResampleImages():
    #go through the workspace and make sure there is no temp.tif or temp.shp files
    # already there, if there are it can cause errors
##    for file in os.listdir(inWs):
##        if(os.path.basename(file) == "temp.tif"):
##            arcpy.Delete_management("temp.tif")
##
##        if(os.path.basename(file) == "temp.shp"):
##            arcpy.Delete_management("temp.shp")
##    arcpy.env.workspace = inWs
    #go through the workspace
##    for root, dirs, files in os.walk('.'):
##        for name in files:
    for file in os.listdir(inWs):
        os.chdir(inWs)
        #make sure that the file is a tif image
        if file.endswith(".tif") and os.path.basename(file) != "temp.tif":
            #get the full name of the tif file including the extension
            basename = os.path.basename(file)
            print basename
            print os.path.abspath(file)
            #extract the file name with no extension
            nameNoExt = os.path.splitext(basename)[0]

            #extract the files extension
            nameExt = os.path.splitext(basename)[1]

            #create the new name for the resampled image
            newName = nameNoExt + "_resampled" + nameExt
            outFile = os.path.join(outWs, newName)
            #make the file a raster file
            InRaster = Raster(file)
            #get the mean x and y size of the cells
            CellsizeX = InRaster.meanCellWidth
            CellsizeY = InRaster.meanCellHeight
            #create the new cell sizes
            OutX = CellsizeX * 8
            OutY = CellsizeY * 8
            outCellSize = (OutX + OutY)/2

            try:
                print "creating resampled raster"
                #resample the raster with the new cell sizes
                tempResRaster = arcpy.Resample_management(InRaster, outFile, str(outCellSize), "CUBIC")
                print "resampled raster created"

                #arcpy.Delete_management(valtable)
                #print str(arcpy.GetRasterProperties_management (os.path.join(outWs, newName), "CELLSIZEX","Band_2"))
            except:
                print str(sys.exc_info()[1])
                msg = arcpy.GetMessages(2)
                print msg
            #create an empty raster
##            try:
##                print "creating temp raster at {0}".format(datetime.datetime.now())
##                OutRasPoly = arcpy.Resample_management(outFile, "temp.tif", "1000", "NEAREST")
##                #OutRasPoly = arcpy.CreateRasterDataset_management(inWs, "temp.tif", pixel_type="1_BIT", number_of_bands="1")
##                print "temp raster created at {0}".format(datetime.datetime.now())
##            except:
##                msg = arcpy.GetMessages(2)
##                print msg

            #computes a raster all with a cell value of 0 and puts it into the empty outRasPoly raster
            try:
                print "creating empty raster at {0}".format(datetime.datetime.now())
                OutRasPoly = InRaster * 0
                arcpy.AddMessage("empty raster created")
                print "empty raster created at {0}".format(datetime.datetime.now())
            except:
                msg = arcpy.GetMessages(2)
                arcpy.AddError(msg)
            arcpy.env.workspace = featureClassFolder
            print "converting raster to polygon at {0}".format(datetime.datetime.now())
            #convert raster to polygon and place in the temp feature class
            polygon = arcpy.RasterToPolygon_conversion (OutRasPoly, "temp", "SIMPLIFY")

            print "raster converted at {0}".format(datetime.datetime.now())
            #append the new polygon to the correct feature class
            print "appending polygon at {0}".format(datetime.datetime.now())
            arcpy.Append_management(polygon, featureClassName, "NO_TEST")
            print "polygon appended at {0}".format(datetime.datetime.now())
            #arcpy.env.workspace = inWs
            #remove the temporary raster and shape file for the next iteration
            #arcpy.Delete_management("temp.tif")
            #arcpy.Delete_management("temp.shp")
##total = endPhotoNum - startPhotoNum +1
##flownByQtd = "'" + flownBy + "'"
##scaleQtd = "'" + scale + "'"
##dateQtd = "'" + str(date) + "'"
##arcpy.CalculateField_management(featureClassName, fields[0], rollNum, "PYTHON")
##arcpy.CalculateField_management(featureClassName, fields[2], dateQtd, "PYTHON")
##arcpy.CalculateField_management(featureClassName, fields[3],flownByQtd, "PYTHON")
##arcpy.CalculateField_management(featureClassName, fields[4], scaleQtd, "PYTHON")

    i = 0
    print "updating fields at {0}".format(datetime.datetime.now())
    with arcpy.da.UpdateCursor(featureClassName, fields) as photoNumCursor:
        for row in photoNumCursor:
            print "in update"
            row[0] = rollNum
            print "rollnum"
            row[1] = startPhotoNum + i
            print "photonum"
            row[2] = date
            print "date"
            row[3] = flownBy
            print "flown by"
            row[4] = scale
            print "scale"
            photoNumCursor.updateRow(row)
            print str(row[0])
            i += 1
    print "process complete at {0}".format(datetime.datetime.now())
except Exception as e:
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    #
    pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
    msg = arcpy.GetMessages(2)
    if msg != "":
        print msg
    else:
        print e
        print pymsg




#ResampleImages()
#AddFields()
#PopFields()

