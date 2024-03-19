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
    cpiInflationDataRaw, cpiInflationData = __CleanData(cpiInflationData, CPI_ROW_LENGTH, CPI_COLUMN_START)
    cpiInflationData = __SplitDataByMonths(cpiInflationData)
    cpiInflationData = __FormatData(cpiInflationData)
    cpiInflationDataRaw = __FormatData(cpiInflationDataRaw)
    return cpiInflationDataRaw, cpiInflationData

def IngestWageData(wageData):
    wageDataRaw, wageData = __CleanData(wageData, WAGES_ROW_LENGTH, WAGES_COLUMN_START)
    wageData = __FormatData(wageData)
    wageDataRaw = __FormatData(wageDataRaw)
    return wageDataRaw, wageData    

def __CleanData(data, dataRowLength, dataColumnStart):
    data = data[1:]
    dataRaw = []
    dataNormalised = []

    for row in data:
        if len(row) > 10:
            dataRow = []
            lastValid = 0

            for index, value in enumerate(row[:640]):
                if index > dataColumnStart:
                    number, lastValid = __ConvertValueToFloat(value, lastValid)
                    dataRow.append(number)

            if len(dataRow) == dataRowLength:
                maxValue = max(dataRow) ## This value needs to be saved eventually.
                normalisedDataRow = __NormaliseDataRow(dataRow, maxValue)

                if(any(normalisedDataRow)):
                    dataRaw.append(dataRow)
                    dataNormalised.append(normalisedDataRow)

    return dataRaw, dataNormalised

def __SplitDataByMonths(cpiInflationDataNormalised):
    yearsInData = round(len(cpiInflationDataNormalised[FIRST]) / MONTHS, 0)
    yearsInData = int(yearsInData) - 1

    splitDataRows = []
    for dataRow in cpiInflationDataNormalised:
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