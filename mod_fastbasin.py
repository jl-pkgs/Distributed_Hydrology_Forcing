# -*- coding: utf-8 -*-
import shutil
import arcpy
from arcpy import sa
import os
import sys
# Dongdong Kong, CUG-atmos, 2021-03-22

# from arcpy.sa import *
arcpy.CheckOutExtension("spatial")  # necessary!
arcpy.env.workspace = os.path.abspath("./Project_Hubei_500m")    # necessary!
arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "0%" # necessary! for demfill

# if workspace not exists, create it
if not os.path.exists(arcpy.env.workspace):
  os.makedirs(arcpy.env.workspace)
print(arcpy.env.workspace)


def cal_slope(dem, replacement=0, fout="dem_slope.tif"):
  # https://desktop.arcgis.com/zh-cn/arcmap/latest/tools/spatial-analyst-toolbox/applying-a-z-factor.htm
  # PERCENT_RISE, DEGREE
  slope = sa.Slope(dem, "PERCENT_RISE", 0.00001036) / 100 # 30°N, perc to ratio
  slope2 = sa.Con(arcpy.sa.IsNull(slope), replacement, slope)
  slope2.save(fout)


def filldem(dem, outfile="demfill.tif"):
  print("fill dem ...")
  outFill = arcpy.sa.Fill(dem)
  outFill.save(outfile)


def cal_flowdir(dem="demfill.tif", outfile="flowdir.tif"):
  print("running flowdir ...")
  print(dem)
  flowdir = arcpy.sa.FlowDirection(dem, "FORCE")
  flowdir.save(outfile)


def cal_flowaccu(flowdir="flowdir.tif", outfile="flowaccu.tif"):
  print("running flowaccu ...")
  outFlowAccumulation = arcpy.sa.FlowAccumulation(flowdir)
  outFlowAccumulation.save(outfile)


def cal_watershed(pour, flowdir="flowdir.tif", outfile="watershed.tif"):
  outWatershed = arcpy.sa.Watershed(flowdir, pour, "FID") + 1
  outWatershed.save(outfile)


def cal_stream(trs=100, accu="flowaccu.tif", flowdir="flowdir.tif"):
  stream = sa.Con(arcpy.Raster(accu) >= trs, 1, 0)
  stream_order = sa.StreamOrder(stream, flowdir, "STRAHLER")
  shp = "stream_%d.shp" % trs
  tif = "stream_%d.tif" % trs
  stream_order.save(tif)
  sa.StreamToFeature(stream_order, flowdir, shp,
                     "NO_SIMPLIFY")  # SIMPLIFY, NO_SIMPLIFY


def replace(ra, fout, replacement=0):
  fixed_raster = sa.Con(arcpy.sa.IsNull(ra), replacement, ra)
  fixed_raster.save(fout)


def flowdir_update_mask(ra="flowdir.tif", mask="watershed.tif", fout="flowdir2.tif"):
  flowdir = sa.ExtractByMask(ra, mask)
  flowdir.save(fout)


# dem = "./dem/GuanShan_dem500m.tif"
dem = "./Project_Hubei_500m/Hubei_dem_merit_500m.tif"
# pour = "./dem/shp/pour_GuShan.shp"

# filldem(dem)
# cal_flowdir()
# cal_flowaccu()
# cal_slope(dem)
cal_stream(trs=100)

# cal_watershed(pour)
# flowdir_update_mask() 

# shutil.copy(dem, "OUTPUT/elevtn.tif")
# shutil.copy("Project/flowaccu.tif", "OUTPUT/uparea.tif")
# shutil.copy("Project/flowdir2.tif", "OUTPUT/flwdir.tif")
# shutil.copy("Project/dem_slope.tif", "OUTPUT/lndslp.tif")
# shutil.copy("Project/watershed.tif", "OUTPUT/basins.tif")

# if __name__ == '__main__':
#     # dem = "N:/ChinaWater/project/dem_guanshan.tif"
#     nargs = len(sys.argv)
#     if nargs >= 2:
#         # print 'Number of arguments:', len(sys.argv), 'arguments.'
#         # print 'Argument List:', str(sys.argv)
#         # example:
#         #	fastbasin dem.tif
#         # 	fastbasin demfill.tif flowdir
#         # 	fastbasin flowdir.tif flowaccu
#         infile = sys.argv[1]
#         arcpy.env.workspace = os.path.dirname(os.path.abspath(infile))

#         if (nargs > 2):
#             begin = sys.argv[2] # fill, flowdir, flowaccu

#             options = {"fill": 1, "flowdir": 2, "flowaccu": 3}
#             Ibegin = options[begin]

#             if Ibegin <= 1:
#                 filldem(infile)
#                 cal_flowdir()
#                 cal_flowaccu()
#             if Ibegin <= 2:
#                 cal_flowdir(infile)
#                 cal_flowaccu()
#             if Ibegin <= 3:
#                 cal_flowaccu(infile)
#         else:
#             filldem(infile)
#             cal_flowdir()
#             cal_flowaccu()
