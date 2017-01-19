from osgeo import gdal, gdalnumeric, ogr, osr
from PIL import Image, ImageDraw, ImageChops, ImageOps
import numpy as np
import os, sys
gdal.UseExceptions()

def imageToArray(i):
    """
    Converts a Python Imaging Library array to a
    gdalnumeric image.
    """
    a=gdalnumeric.fromstring(i.tobytes(),'b')
    a.shape=i.im.size[1], i.im.size[0]
    return a

def OpenArray( array, prototype_ds = None, xoff=0, yoff=0 ):
    ds = gdalnumeric.OpenArray(array)

    if ds is not None and prototype_ds is not None:
        if type(prototype_ds).__name__ == 'str':
            prototype_ds = gdal.Open( prototype_ds )
        if prototype_ds is not None:
            gdalnumeric.CopyDatasetInfo( prototype_ds, ds, xoff=xoff, yoff=yoff )
    return ds

def world2Pixel(geoMatrix, x, y):
  """
  Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
  the pixel location of a geospatial coordinate
  """
  ulX = geoMatrix[0]
  ulY = geoMatrix[3]
  xDist = geoMatrix[1]
  yDist = geoMatrix[5]
  rtnX = geoMatrix[2]
  rtnY = geoMatrix[4]
  pixel = int((x - ulX) / xDist)
  line = int((ulY - y) / xDist)
  return (pixel, line)

def stretch(a):
  """
  Performs a histogram stretch on a gdalnumeric array image.
  """
  hist = histogram(a)
  im = arrayToImage(a)
  lut = []
  for b in range(0, len(hist), 256):
    # step size
    step = reduce(operator.add, hist[b:b+256]) / 255
    # create equalization lookup table
    n = 0
    for i in range(256):
      lut.append(n / step)
      n = n + hist[i+b]
  im = im.point(lut)
  return imageToArray(im)

def polySetToMask(ogr_geometry, dataset, geoTrans, xmax_ymin):
    pxWidth = dataset.RasterXSize
    pxHeight = dataset.RasterYSize
    points = []
    pixels = []
    xscale = 1
    yscale = 1
    geometry_count = ogr_geometry.GetGeometryCount()
    point_count = 0
    if xmax_ymin:
        floatWidth = float(pxWidth)
        floatHeight = float(pxHeight)
        w_prime = (floatWidth*(floatWidth/(floatWidth + 1)))
        xscale = w_prime/xmax_ymin['xMax']
        h_prime = (floatHeight*(floatHeight/(floatHeight + 1)))
        yscale = h_prime/xmax_ymin['yMin']
    else:
        print("Warning!  Couldn't find transform data for this TIF from the sizes csv!")
    if geometry_count < 500 and geometry_count > 0:
        rasterPoly = Image.new("L", (pxWidth, pxHeight), 256)
        for geo in xrange(geometry_count):
            rasterPolySingle = Image.new("L", (pxWidth, pxHeight), 256)
            points = []
            geometry_instance = ogr_geometry.GetGeometryRef(geo)
            ogr_poly = geometry_instance.GetGeometryRef(0)
            for p in xrange(ogr_poly.GetPointCount()):
                point_count += 1
                points.append((int(round(w_prime*(ogr_poly.GetX(p)/xmax_ymin['xMax']))), int(round(h_prime*(ogr_poly.GetY(p)/xmax_ymin['yMin'])))))
            for p in points:
                pixels.append(world2Pixel(geoTrans, p[0], p[1]))
            if point_count > 0:
                rasterize = ImageDraw.Draw(rasterPolySingle)
                rasterize.polygon(points, 0)
                rasterPoly = ImageChops.multiply(rasterPoly, rasterPolySingle)
        # multiply the sum of masks against the original dataset
        datasetToPilImage = Image.fromarray(np.uint8(dataset.GetRasterBand(3).ReadAsArray()))
        rasterPoly = ImageChops.multiply(ImageOps.invert(rasterPoly), datasetToPilImage)
        # TODO the value of rasterpoly that aren't black represent a human viewable view of
        # that class's values harvested from the image.  These are the values that we need to
        # train on for each class.
        if point_count > 0:
            rasterize = ImageDraw.Draw(rasterPoly)
            rasterize.polygon(points, 0)
            # print(imageToArray(rasterPoly))
            return imageToArray(rasterPoly)
    elif geometry_count > 0:
        print "Too many geometries! Encountered multipolygon with %d geometries." % geometry_count
