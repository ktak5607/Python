#-------------------------------------------------------------------------------
# Name:     module1
# Purpose:
#
# Author:     kevin.takala
#
# Created:   6/6/2018
# Copyright:   (c) kevin.takala 2018
# Licence:   <your licence>

#Huge thanks to KEVIN DWYER from the HumanGeo Blog (MAXAR Technologies)
#for coming up with the concave hull portion of the code
#-------------------------------------------------------------------------------

from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import math
import fiona
import shapely.geometry as geometry
import arcpy
import os
import traceback

def add_edge(edges, edge_points, coords, i, j):

    """
    Add a line between the i-th and j-th points,
    if not in the list already
    """
    
    if (i, j) in edges or (j, i) in edges:
        # already added
        return
    edges.add( (i, j) )
    edge_points.append(coords[ [i, j] ])



def alpha_shape(points):
    """
    Compute the alpha shape (concave hull) of a set
    of points.
    @param points: Iterable container of points.
    @param alpha: alpha value to influence the
        gooeyness of the border. Smaller numbers
        don't fall inward as much as larger numbers.
        Too large, and you lose everything!
    """
    if len(points) < 4:
        # When you have a triangle, there is no sense
        # in computing an alpha shape.
        return geometry.MultiPoint(list(points)).convex_hull
            
    coords = np.array([point.coords[0] for point in points])
    coords2D = coords[:, 0:2]
    print("creating triangles")
    tri = Delaunay(coords2D)
    edges = set()
    edge_points = []
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the
    # triangle
    i=0

    #3DFile
    if(tri.vertices.shape[1] == 4):
            print("3D file detected")
            for ia, ib, ic in tri.vertices:
                i += 1
                #get vertices of triangle
                pa = coords[ia]
                pb = coords[ib]
                pc = coords[ic]
                # Lengths of sides of triangle
                #length of first side
                a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2 + (pa[2]-pb[2])**2)
                #length of second side
                b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2 + (pb[2]-pc[2])**2)
                #length of third side
                c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2 + (pc[2]-pa[2])**2)
                
                if a < 100 and b < 100 and c < 100:

                    add_edge(edges, edge_points, coords, ia, ib)
                    add_edge(edges, edge_points, coords, ib, ic)
                    add_edge(edges, edge_points, coords, ic, ia)


    #2DFile
    elif(tri.vertices.shape[1] == 3):
        print("2D file detected")
        for ia, ib, ic in tri.vertices:
            i += 1
            pa = coords[ia]
            pb = coords[ib]
            pc = coords[ic]
            # Lengths of sides of triangle
            a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
            b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
            c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
            
            if a < 100 and b < 100 and c < 100:

                add_edge(edges, edge_points, coords, ia, ib)
                add_edge(edges, edge_points, coords, ib, ic)
                add_edge(edges, edge_points, coords, ic, ia)
    m = geometry.MultiLineString(edge_points)
    triangles = list(polygonize(m))
    return cascaded_union(triangles), edge_points



#################################
#BEGIN ARC PROCESSING
arcpy.env.overwriteOutput = True
folder = r"C:\Users\kevin.takala\Documents\kmztest\Example"#arcpy.GetParameterAsText(0)
arcpy.env.workspace = folder
linePoints = folder + "\\LinePoints.shp"
polygonPoints = folder + "\\PolygonPoints.shp"
linePntsLst = []
polygonPntsLst = []
pointsLst = []
wgsSR = arcpy.SpatialReference(4326)
vaLLCSR = arcpy.SpatialReference(3969)
lastGdb = ""
for fl in os.listdir(folder):
    if (fl.endswith(".kmz") or fl.endswith(".kml")):
        
        kmzName = os.path.splitext(os.path.basename(fl))[0]
        print (kmzName)
        try:
            arcpy.KMLToLayer_conversion(folder + "\\" + fl, folder)
            print("KML converted")
        except:
            errorWriter = open(folder + "\\errorlog.txt", 'a')
            errorWriter.write("Error converting " + kmzName + "\n")
            errorWriter.write(traceback.format_exc() + "\n")
            errorWriter.close()
            break
        gdb = folder + "\\" + kmzName + ".gdb" + "\\Placemarks"
        arcpy.env.workspace = gdb
        try:
            if(arcpy.env.workspace == lastGdb):
                raise Exception
        except:
            errorWriter = open(folder + "\\errorlog.txt", 'a')
            errorWriter.write("Error changing gdb for " + kmzName + "\n")
            errorWriter.close()
            break
        lastGdb = arcpy.env.workspace
        
        try:
            for fc in arcpy.ListFeatureClasses():
                
                if "Polyline" in fc:
                    print("found polylines")
                    arcpy.FeatureVerticesToPoints_management(fc, linePoints, "ALL")
                    lineReproj = folder + "\\" + kmzName + "Polyline_reproj.shp"
                    arcpy.Project_management(linePoints, lineReproj, vaLLCSR)
                    with fiona.open(lineReproj) as shapefile:
                        linePntsLst = [geometry.shape(point['geometry']) for point in shapefile]
                        

                elif "Polygon" in fc: 
                    print("found polygons")
                    arcpy.FeatureVerticesToPoints_management(fc, polygonPoints, "ALL")
                    polygonReproj = folder + "\\" + kmzName + "Polygon_reproj.shp"
                    arcpy.Project_management(polygonPoints, polygonReproj, vaLLCSR)
                    with fiona.open(polygonReproj) as shapefile:
                        polygonPntsLst = [geometry.shape(point['geometry']) for point in shapefile]
                        
                elif "Point" in fc:
                    print("found points")
                    pointsFc = arcpy.FeatureClassToFeatureClass_conversion (fc, folder, "Points.shp")
                    pntsReproj = pointsFc, folder + "\\" + kmzName + "Points_reproj.shp"
                    pntsReproj = arcpy.Project_management(pntsReproj, vaLLCSR)
                    with fiona.open(pntsReproj) as shapefile:
                        pointsLst = [geometry.shape(point['geometry']) for point in shapefile]
        except:
            
            errorWriter = open(folder + "\\errorlog.txt", 'a')
            errorWriter.write("Error creating points for " + kmzName + "\n")
            errorWriter.write(traceback.format_exc() + "\n")
            errorWriter.close()
            break
                    
        
        points = pointsLst + linePntsLst + polygonPntsLst
        
        try:
            
            concave_hull, edge_points = alpha_shape(points)
        except:
            errorWriter = open(folder + "\\errorlog.txt", 'a')
            errorWriter.write("Error triangulating points for " + kmzName + "\n")
            errorWriter.write(traceback.format_exc() + "\n")
            errorWriter.close()
            break

        myschema = {
                'geometry': 'Polygon',
                'properties': {'id': 'int'},
        }
        arcpy.env.workspace = folder
        tempShp = folder + "\\" + kmzName + "_temp.shp"

        with fiona.open(tempShp, 'w',driver='ESRI Shapefile', schema = myschema) as output:
                output.write({'geometry': geometry.mapping(concave_hull), 'properties': {'id': kmzName}})
        output.close()
                
        arcpy.DefineProjection_management(tempShp, vaLLCSR)
        wktName = folder + "\\" + kmzName + ".wkt"
        wktWriter = open(wktName, 'w')
        scur = arcpy.da.SearchCursor(tempShp, ['SHAPE@WKT'])
        for poly in scur:
            try:
                wkt = poly[0]
                wktPlyRep = wkt.replace("MULTIPOLYGON", "$shape = 'polygon")
                wktParRep = wktPlyRep.replace(" (((", "((\n    ")
                wktParRep2 = wktParRep.replace(")))", "\n))'")
                wktWriter.write(wktParRep2)
                wktWriter.close()
            except:
                    
                errorWriter = open(folder + "\\errorlog.txt", 'a')
                errorWriter.write("Error creating wkt for " + kmzName + "\n")
                errorWriter.write(traceback.format_exc() + "\n")
                errorWriter.close()
                break

        
        #arcpy.Delete_management(tempShp)
        arcpy.Delete_management (linePoints)
        arcpy.Delete_management(polygonPoints)
        arcpy.Delete_management(folder + "\\" + kmzName + "Polyline_reproj.shp")
        arcpy.Delete_management(folder + "\\" + kmzName + "Polygon_reproj.shp")
        arcpy.Delete_management(folder + "\\" + kmzName + "Points_reproj.shp")
        arcpy.Delete_management (folder + "\\Points.shp")
        del linePntsLst[:]
        del polygonPntsLst[:]
        del pointsLst[:]
        









