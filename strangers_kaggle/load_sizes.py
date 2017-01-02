import csv
import sys
from osgeo import ogr

def readSizesFromFile(fileName):
    sizes = {}
    with open(fileName, 'rb') as csvfile:
        xyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        line_counter = 0
        for row in xyreader:
            if len(row) == 3 and line_counter > 0:
                sizes[row[0]] = {'xMax': float(row[1]), 'yMin': float(row[2])}
            line_counter += 1
    return sizes

def readTrainingDataFromFile(fileName):
    csv.field_size_limit(sys.maxsize)
    training = {}
    with open(fileName, 'rb') as csvfile:
        trainingreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        line_counter = 0
        for row in trainingreader:
            if row[0] not in training:
                training[row[0]] = {}
            if row[0] and row[1] and row[2] and line_counter > 0:
                training[row[0]][int(row[1])] = ogr.CreateGeometryFromWkt(row[2])
            line_counter += 1
    return training
