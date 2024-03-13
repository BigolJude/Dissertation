import numpy

FIRST = 0
MONTHS = 12
DATA_ROW_LENGTH = 639

def IngestData(cpiInflationData):
    cpiInflationData = __CleanData(cpiInflationData)
    cpiInflationData = __SplitDataByMonths(cpiInflationData)
    cpiInflationData = __FormatData(cpiInflationData)
    return cpiInflationData

def __CleanData(cpiInflationData):
    cpiInflationData = cpiInflationData[7:]
    cpiInflationDataRaw = []
    cpiInflationDataNormalised = []

    for rows in cpiInflationData:
        if len(rows) > 10:

            cpiDataRow = []
            lastValid = 0

            for string in rows[1:640]:
                try:
                    number = float(string)
                    lastValid = number
                except:
                    number = lastValid
                cpiDataRow.append(number)

            if len(cpiDataRow) == DATA_ROW_LENGTH:

                maxValue = max(cpiDataRow)
                normalisedDataRow = []

                for value in cpiDataRow:
                    if value > 0:
                        value = (value / maxValue)
                    normalisedDataRow.append(value)

                cpiInflationDataRaw.append(cpiDataRow)
                cpiInflationDataNormalised.append(normalisedDataRow)
    return cpiInflationDataNormalised

def __SplitDataByMonths(cpiInflationDataNormalised):
    yearsInData = round(len(cpiInflationDataNormalised[FIRST]) / MONTHS, 0)
    yearsInData = int(yearsInData)

    splitDataRows = []
    for dataRow in cpiInflationDataNormalised:
        for month in range(MONTHS):
            splitDataRow = []
            for year in range(yearsInData):
                splitDataRow.append(dataRow[(year * MONTHS) + month])
            splitDataRows.append(splitDataRow)
    return splitDataRows

def __FormatData(splitDataRows):
    cpiInflationDataSplit = [[[float(y)] for y in x] for x in splitDataRows]
    cpiInflationDataSplit = numpy.array(cpiInflationDataSplit)
    return cpiInflationDataSplit