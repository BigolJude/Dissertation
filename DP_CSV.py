import csv

COMMA_SEPARATOR = ','
NEW_LINE = '\n'
PIPEBAR = '|'

def ReadCSV(filePath):
    csvData = []

    with open(filePath, newline='') as csvFile:
        file = csv.reader(csvFile, delimiter=NEW_LINE, quotechar=PIPEBAR)
        for row in file:
            for column in row:
                csvData.append(column.split(COMMA_SEPARATOR))
                
    return csvData