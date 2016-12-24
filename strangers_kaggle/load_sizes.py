import csv

def readFromFile(fileName):
    sizes = {}
    with open(fileName, 'rb') as csvfile:
        xyreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in xyreader:
            if len(row) == 3 and row[0]:
                sizes[row[0]] = {'xMax': float(row[1]), 'yMin': float(row[2])}
    return sizes
