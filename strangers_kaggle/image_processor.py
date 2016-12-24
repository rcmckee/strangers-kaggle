from __future__ import division, print_function, absolute_import
import argparse
import sys
import os
import logging
import skimage
import gdal
from strangers_kaggle.load_sizes import *
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
        help="The directory containing the tifs that should be preprocessed.")
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

def processTifFile(file, subdir, xmax_ymin):
    img_filename_16bandA = subdir + file
    datasetA = gdal.Open(img_filename_16bandA, GA_ReadOnly)
    name = "_".join(file.split('_')[0:3])
    print('Size is %d x %d x %d for file %s' % (datasetA.RasterXSize, datasetA.RasterYSize, datasetA.RasterCount, file))
    if name in xmax_ymin:
        w_prime = datasetA.RasterXSize*(datasetA.RasterXSize/(datasetA.RasterXSize + 1))
        xscale = w_prime/xmax_ymin[name]['xMax']
        h_prime = datasetA.RasterYSize*(datasetA.RasterYSize/(datasetA.RasterYSize + 1))
        yscale = w_prime/xmax_ymin[name]['yMin']
        # TODO image processing here where the scales are known
        # segment(datasetA, file)
    else:
        print("Warning!  Couldn't find transform data for this TIF from the csv!")

def main(args):
    args = parse_args(args)
    setup_logging(args.loglevel)
    print("The directory of TIF images for processing is {}".format(args.d))
    xmax_ymin = {}
    if args.f:
        xmax_ymin = readFromFile(args.f)
    for subdir, dirs, files in os.walk(args.d):
        for file in files:
            if file.endswith(".tif"):
                processTifFile(file, subdir, xmax_ymin)
                _logger.debug("Processing image {}".format(file))
    _logger.info("Script ends here")

def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])

if __name__ == "__main__":
    run()
