import csv

COMMA_SEPARATOR = ','

def ReadCSV(filePath):
    csvData = []

    with open(filePath, newline='') as csvFile:
        file = csv.reader(csvFile, delimiter=' ', quotechar='|')
        for row in file:
            for column in row:
                csvData.append(column.split(COMMA_SEPARATOR))
                
    return csvData