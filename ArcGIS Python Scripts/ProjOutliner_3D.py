#-------------------------------------------------------------------------------
# Name:		module1
# Purpose:
#
# Author:	  kevin.takala
#
# Created:	 11/05/2016
# Copyright:   (c) kevin.takala 2016
# Licence:	 <your licence>

#Huge thanks to KEVIN DWYER from the HumanGeo Blog (MAXAR Technologies)
#for coming up with the concave hull portion of the code
#-------------------------------------------------------------------------------

from shapely.ops import cascaded_union, polygonize
from scipy.spatial import Delaunay
import numpy as np
import math
import fiona
from osgeo import ogr
from osgeo import osr
import shapely.geometry as geometry
import pylab as pl
import matplotlib.pyplot as mpl
import arcpy
from arcpy import env
import os

#use 107187.dgn for testing
def conv_coords (points, Dim):
	pntRP = []
	i = 0
	sf = 1.00006
	if(Dim == 3):
		for i in range (len(points)):
			points[i].coords[0][0] = pnt.coords[0][0]/sf + 8202083.33325
			points[i].coords[0][1] = pnt.coords[0][1]/sf + 6561666.6666
	return points


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
	coords = np.array([point.coords[0]
					   for point in points])
	coords2D = coords[:, 0:2]

	tri = Delaunay(coords2D)
	edges = set()
	edge_points = []
	# loop over triangles:
	# ia, ib, ic = indices of corner points of the
	# triangle
	i=0

	#3DFile
	if(tri.vertices.shape[1] == 4):
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
			# Semiperimeter of triangle
			s = (a + b + c)/2.0
			# Area of triangle by Heron's formula
			area = math.sqrt(s*(s-a)*(s-b)*(s-c))

			circum_r = a*b*c/(4.0*area)
			# Here's the radius filter.
			#print circum_r
			if circum_r < 250:

				add_edge(edges, edge_points, coords, ia, ib)
				add_edge(edges, edge_points, coords, ib, ic)
				add_edge(edges, edge_points, coords, ic, ia)


	#2DFile
	elif(tri.vertices.shape[1] == 3):
		for ia, ib, ic in tri.vertices:
			i += 1
			pa = coords[ia]
			pb = coords[ib]
			pc = coords[ic]
			# Lengths of sides of triangle
			a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
			b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
			c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)
			# Semiperimeter of triangle
			s = (a + b + c)/2.0
			# Area of triangle by Heron's formula
			area = math.sqrt(s*(s-a)*(s-b)*(s-c))

			circum_r = a*b*c/(4.0*area)
			# Here's the radius filter.
			#print circum_r
			if circum_r < 300:

				add_edge(edges, edge_points, coords, ia, ib)
				add_edge(edges, edge_points, coords, ib, ic)
				add_edge(edges, edge_points, coords, ic, ia)
	m = geometry.MultiLineString(edge_points)
	triangles = list(polygonize(m))
	return cascaded_union(triangles), edge_points



#################################
#BEGIN ARC PROCESSING
arcpy.env.overwriteOutput = True
inWs = r"C:\Users\kevin.takala\Desktop\Arc_Proj\test\107187"#arcpy.GetParameterAsText(0)
arcpy.env.workspace = inWs
gdb = inWs + "\CAD_Files.gdb"
CADFolder = inWs + r"\CADFiles"
dgnName = ""
lines = ""
##
'''
use when you get access to a database with dgn files in it
for file in CADFolder:
###sr = arcpy.SpatialReference(4501)


	if os.path.splitext(os.path.basename(file))[1] == "dgn":
		for UPC in jobs.xcl:  ###############################################################read excel file UPCs
			if UPC in os.path.basename(file):
				dgnName = "s" + str(UPC)
				arcpy.CADToGeodatabase_conversion(file, gdb, dgnName , "300")
				for FC in (gdb + "\\" + dgnName):
					if "Polyline" in FC:
						lines = os.path.abspath(FC)

'''

for fl in os.listdir(CADFolder):
	print "searching cad folder"
	print fl
	print os.path.splitext(os.path.basename(fl))[1]
	if os.path.splitext(os.path.basename(fl))[1] == ".dgn":
		print "found a dgn file"
		dgnName = "s" + str(os.path.splitext(os.path.basename(fl))[0])
		print dgnName
		arcpy.CADToGeodatabase_conversion((CADFolder + "\\" + fl), gdb, dgnName , "300")
		arcpy.env.workspace = gdb
		for fds in arcpy.ListDatasets('', 'feature'):
			if fds == dgnName:
				for fc in arcpy.ListFeatureClasses('', '', fds):
					print "searching geodatabase for the new FC"
					if "Polyline" in fc:
						print "found a polyline file "
						#lines = fc
						endPoints = r"C:\Users\kevin.takala\Desktop\Arc_Proj\test\Endpoints.shp"
						arcpy.FeatureVerticesToPoints_management(fc, endPoints, "BOTH_ENDS")
						#shapefile = fiona.open(endPoints)
						with fiona.open(endPoints) as shapefile:
							 points = [geometry.shape(point['geometry']) for point in shapefile]
							 print str(len(points[0].coords[0]))
							 pntsSP = conv_coords(points, len(points[0].coords[0]))
							 concave_hull, edge_points = alpha_shape(pntsSP)
						arcpy.Delete_management (endPoints)

						myschema = {
							'geometry': 'Polygon',
							'properties': {'id': 'int'},
						}
						arcpy.env.workspace = inWs
						tempShp = inWs + "\\" + dgnName + "_temp.shp"

						with fiona.open(tempShp, 'w',driver='ESRI Shapefile', schema = myschema) as output:
							output.write({'geometry': geometry.mapping(concave_hull), 'properties': {'id': 107187}})
						output.close
						proj = arcpy.projection(3686)
						arcpy.Define_Projection_management(tempShp, proj)
						outShp = arcpy.CreateLayer(inWs + "\\" + dgnName + "Outline.shp")
						reProj = arcpy.projection(3857)
						arcpy.Project_management(tempShp, outShp, reProj)
						arcpy.Delete_management(tempShp)
					#get the input layer
##    					inShp = inWs + "\\" + dgnName + "Outline.shp"
##    					driver = ogr.GetDriverByName('ESRI Shapefile')
##
##    					polyShp = driver.Open(outShp)
##    					polyLyr = polyShp.GetLayer()
##
##    					#create the output layer
##    					outShp2 = inWs + "\\" + dgnName + "Outline2.shp"
##    					outDataSet = driver.CreateDataSource(outShp2)
##    					outLayer = outDataSet.CreateLayer("basemap_4326", geom_type=ogr.wkbMultiPolygon)
##    					outLayerDefn = outLayer.GetLayerDefn()
##
##    					inCS = osr.SpatialReference()
##    					inCS.ImportFromEPSG(3686)
##    					outCS = osr.SpatialReference()
##    					outCS.ImportFromEPSG(3857)
##    					transform = osr.CoordinateTransformation(inCS, outCS)
##
##    					polygon = polyLyr.GetNextFeature()
##    					while polygon:
##    						geom = polygon.GetGeometryRef()
##    						geom.Transform(transform)
##    						outPolygon = ogr.Feature(outLayerDefn)
##    						outPolygon.SetGeometry(geom)
##    						outLayer.CreateFeature(outPolygon)
##    						outPolygon = None
##    						polygon = polyLyr.GetNextFeature()
					#shpReproj = ogr.CreateGeometryFromJson(outShp)
					#fails here rem to delete geojson before run
##					for i in range(0, concave_hullReproj.GetGeometryCount()):
##						g = concave_hullReproj.GetGeometryRef(i)
##						g.Transform(transform)
##					outShpReproj = inWs + "\\" + dgnName + "Outline_Reproj.json"
##					with fiona.open(outShpReproj, 'w',driver='GeoJSON', schema = myschema) as output:
##						output.write({'geometry': geometry.mapping(concave_hullReproj), 'properties': {'id': 107187}})
##					output.close
					print "Success"

##input_DGN = r"C:\Users\kevin.takala\Documents\DGN\105584\105584_2D_Plan_Add_KT - Copy.dgn"
##DGN = fiona.open(input_DGN)
#input_shapefile = r'C:\Users\kevin.takala\Desktop\Arc_Proj\test\Endpoints.shp'
#shapefile = fiona.open(input_shapefile)






