from __future__ import division, print_function, absolute_import
import argparse
import sys
import os
import logging
import skimage
import gdal
import struct
from strangers_kaggle.load_sizes import *
from strangers_kaggle.geometry_utils import *
from strangers_kaggle.image_segmentation import *
from gdalconst import *
from strangers_kaggle import __version__
from skimage import data

__author__ = "eldavojohn"
__copyright__ = "eldavojohn"
__license__ = "none"

_logger = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Procssing through scikit-image for the tifs.")
    parser.add_argument(
        '--version',
        action='version',
        version='strangers-kaggle {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="d",
        help="The directory containing the tifs that should be preprocessed.")
    parser.add_argument(
        '-f',
        '--sizefile',
        dest="f",
        help="The CSV file containing the min and max scaling parameters.")
    parser.add_argument(
        '-t',
        '--trainFile',
        dest="t",
        help="The CSV file containing the WKT polygons for training on the given images.")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def processTifFile(file, subdir, xmax_ymin, train_wkt_polys):
    img_filename_16bandA = subdir + file
    dataset = gdal.Open(img_filename_16bandA, GA_ReadOnly)
    # segment(dataset, subdir, file)
    name = file[:-4]
    name = "_".join(name.split('_')[0:3])
    # print('Size is %d x %d x %d for file %s' % (dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount, file))
    band0 = dataset.GetRasterBand(1)
    band1 = dataset.GetRasterBand(2)
    band2 = dataset.GetRasterBand(3)
    # print(band0.ComputeRasterMinMax(0))
    # print(gdal.GetDataTypeName(band0.DataType))
    # print(band1.ComputeRasterMinMax(0))
    # print(gdal.GetDataTypeName(band1.DataType))
    # print(band2.ComputeRasterMinMax(0))
    # print(gdal.GetDataTypeName(band2.DataType))
    scanline = band2.ReadRaster( 0, 0, band2.XSize, 1, band1.XSize, 1, GDT_Float32 )
    tuple_of_floats = struct.unpack('f' * band2.XSize, scanline)
    # print(tuple_of_floats)
    if name in train_wkt_polys:
        # TODO image processing here where the scales are known
        # Load the source data as a gdalnumeric array
        srcArray = gdalnumeric.LoadFile(img_filename_16bandA)

        # Also load as a gdal image to get geotransform
        # (world file) info
        srcImage = gdal.Open(img_filename_16bandA)
        geoTrans = srcImage.GetGeoTransform()
        for geom_index in xrange(len(train_wkt_polys[name])):
            mask = polySetToMask(train_wkt_polys[name][geom_index + 1], dataset, geoTrans, xmax_ymin[name])
            if mask is not None and mask.any():
                # print('Starting processing!')
                gtiffDriver = gdal.GetDriverByName( 'GTiff' )
                if not os.path.exists(subdir + '../trainingMasks/'):
                    os.makedirs(subdir + '../trainingMasks/')
                if gtiffDriver is None:
                    raise ValueError("Can't find GeoTiff Driver")

                # TODO need to work in a way to see what it is overlapping maybe?
                # gdalnumeric.SaveArray(mask, subdir + "../trainingMasks/cl_" + str(geom_index + 1) + "_" + file, format="GTiff", prototype=srcImage)

                mask = mask.astype(gdalnumeric.uint8)
                gdalnumeric.SaveArray(mask, subdir + "../trainingMasks/" + file + "_cl" + str(geom_index + 1) + ".jpg", format="JPEG")
                # print('Completed processing!')
    # else:
        # print('Warning!  Couldn\'t find training data for this TIF named %s from the training csv!' % (name))

def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    print("The directory of TIF images for processing is {}".format(args.d))
    xmax_ymin = {}
    train_wkt_polys = {}
    if args.f:
        xmax_ymin = readSizesFromFile(args.f)
    if args.t:
        train_wkt_polys = readTrainingDataFromFile(args.t)
    for subdir, dirs, files in os.walk(args.d):
        for file in files:
            if file.endswith(".tif"):
                processTifFile(file, subdir, xmax_ymin, train_wkt_polys)
                _logger.debug("Processing image {}".format(file))
    _logger.info("Script ends here")

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
