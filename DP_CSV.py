import csv

COMMA_SEPARATOR = ','
NEW_LINE = '\n'
PIPEBAR = '|'

def ReadCSV(filePath):
    csvData = []

    with open(filePath, newline='') as csvFile:
        reader = csv.reader(csvFile, delimiter=NEW_LINE, quotechar=PIPEBAR)
        for row in reader:
            for column in row:
                csvData.append(column.split(COMMA_SEPARATOR))
                
    return csvData

def WriteCSV(filepath, data):
    with open(filepath, 'w', newline='') as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=NEW_LINE, quotechar=PIPEBAR, quoting=csv.QUOTE_MINIMAL)
        for row in data:
            csvWriter.writerow(row)