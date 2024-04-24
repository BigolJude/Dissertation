import numpy

FIRST = 0
MONTHS = 12
CPI_ROW_LENGTH = 635
CPI_COLUMN_START = 4
WAGES_ROW_LENGTH = 64
WAGES_COLUMN_START = 3

QUOTE_MARKS = "\""
EMPTY_STRING = ""

def IngestCPIData(cpiInflationData):
    cpiInflationMetaData, cpiInflationData = __CleanData(cpiInflationData, CPI_ROW_LENGTH, CPI_COLUMN_START, labelIndex=2)
    cpiInflationData = __SplitDataByMonths(cpiInflationData, cpiInflationMetaData)
    cpiInflationData = __FormatData(cpiInflationData)
    cpiInflationMetaData = __CleanDoubleStrings(cpiInflationMetaData)
    return cpiInflationMetaData, cpiInflationData

def IngestWageData(wageData):
    wageMetaData, wageData = __CleanData(wageData, WAGES_ROW_LENGTH, WAGES_COLUMN_START, labelIndex=FIRST)
    wageData = __FormatData(wageData)
    wageMetaData = __CleanDoubleStrings(wageMetaData)
    return wageMetaData, wageData

def IngestUKWageData(ukData):
    ukData = ukData[6:19]
    ukDataCleaned = []
    ukMetaData = []
    for row in ukData:
        max = 0
        place = ''
        dataRow = []
        metaDataRow = []
        for index, string in enumerate(row[1:26]):
            if index == 0:
                place = string
            else:
                if index != 3 and index != 5 and index != 11:
                    number = float(string)
                    if max < number:
                        max = number
                    dataRow.append(number)
        metaDataRow.append(place)
        metaDataRow.append(max)
        ukMetaData.append(metaDataRow)
        ukDataCleaned.append([x / max for x in dataRow])
    return ukMetaData, __FormatData(ukDataCleaned)

def IngestUKCOLData(ukData):
    return [[x[0],float(x[1]), float(x[2])] for x in ukData]

def __CleanData(data, dataRowLength, dataColumnStart, labelIndex):
    data = data[1:]
    metaData = []
    dataNormalised = []

    rowIndex = 0

    for row in data:
        if len(row) > 10:
            dataRow = []
            lastValid = 0

            zeroCount = 0

            for index, value in enumerate(row[:640]):
                if index > dataColumnStart:
                    lastLastValid = lastValid
                    number, lastValid = __ConvertValueToFloat(value, lastValid)

                    if number == 0:
                        zeroCount += 1
                    else:
                        if zeroCount > 0:
                            difference = (lastValid - lastLastValid) / zeroCount
                            for i in range(zeroCount):
                                dataIndexChange = index - (i + 2 + dataColumnStart)
                                dataRow[dataIndexChange] = lastValid - (difference * (1 + i))  
                            zeroCount = 0
                    dataRow.append(number)
                

            if len(dataRow) == dataRowLength:
                maxValue = max(dataRow) ## This value needs to be saved eventually.
                normalisedDataRow = __NormaliseDataRow(dataRow, maxValue)

                if(any(normalisedDataRow)):
                    metaDataRow = []
                    metaDataRow.append(row[labelIndex])
                    metaDataRow.append(maxValue)
                    metaDataRow.append(rowIndex)

                    metaData.append(metaDataRow)
                    dataNormalised.append(normalisedDataRow)

                    rowIndex = rowIndex + 1

    return metaData, dataNormalised

def __SplitDataByMonths(cpiInflationDataNormalised, cpiInflationMetaData):
    yearsInData = round(len(cpiInflationDataNormalised[FIRST]) / MONTHS, 0)
    yearsInData = int(yearsInData) - 1
    splitDataRows = []

    for index, dataRow in enumerate(cpiInflationDataNormalised):
        for month in range(MONTHS):
            splitDataRow = []

            for year in range(yearsInData):
                splitDataRow.append(dataRow[(year * MONTHS) + month])

            splitDataRows.append(splitDataRow)
    return splitDataRows

def __FormatData(dataRows):

    ## Converting data points [1,2,3] to [[1],[2],[3]]
    dataRows = [[[y] for y in x] for x in dataRows]
    dataRows = numpy.array(dataRows)
    return dataRows

def __ConvertValueToFloat(value, lastValid):
    try:
        value = value.replace(QUOTE_MARKS, EMPTY_STRING)
        number = float(value)
        lastValid = number
    except:
        number = lastValid
    return number, lastValid

def __NormaliseDataRow(dataRow, maxValue):
    normalisedDataRow = [] 
    for value in dataRow:
        if value > 0:
            value = (value / maxValue)
        normalisedDataRow.append(value)
    return normalisedDataRow

def __CleanDoubleStrings(dataSet):
    cleanedDataSet = []

    for dataRow in dataSet:
        cleanedDataRow = []
        for i in range(len(dataRow)):
            if(isinstance(dataRow[i], str)):
                cleanedDataRow.append(dataRow[i].replace(QUOTE_MARKS, EMPTY_STRING))
            else:
                cleanedDataRow.append(dataRow[i])
        cleanedDataSet.append(cleanedDataRow)
    return cleanedDataSet

