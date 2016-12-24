import csv

def readFromFile(fileName):
    sizes = {}
    with open(fileName, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if len(row) == 3:
                sizes[row[0]] = {'xMax': row[1], 'yMin': row[2]}
    return sizes
