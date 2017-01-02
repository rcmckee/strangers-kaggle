from osgeo import gdal, gdalnumeric, ogr, osr
from PIL import Image, ImageDraw
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

def polySetToMask(ogr_geometry, pxWidth, pxHeight, geoTrans, xmax_ymin):
    points = []
    pixels = []
    xscale = 1
    yscale = 1
    # geom = poly.GetNextFeature().GetGeometryRef()
    # pts = geom.GetGeometryRef(0)
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
    if geometry_count < 100:
        for geo in xrange(geometry_count):
            geometry_instance = ogr_geometry.GetGeometryRef(geo)
            # print(geometry_instance.GetGeometryRef(0).GetPoints())
            ogr_poly = geometry_instance.GetGeometryRef(0)
            for p in xrange(ogr_poly.GetPointCount()):
                point_count += 1
                points.append((int(round(w_prime*(ogr_poly.GetX(p)/xmax_ymin['xMax']))), int(round(h_prime*(ogr_poly.GetY(p)/xmax_ymin['yMin'])))))
            for p in points:
                pixels.append(world2Pixel(geoTrans, p[0], p[1]))
        rasterPoly = Image.new("L", (pxWidth, pxHeight), 255)
        if point_count > 0:
            rasterize = ImageDraw.Draw(rasterPoly)
            rasterize.polygon(points, 0)
            return imageToArray(rasterPoly)
