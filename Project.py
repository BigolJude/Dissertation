# Things to do:
# - xml comments on functions
# - add in some form of hill climbing
# - test the model with a full dataset.
# - code clean up.
# - do some arethmatic to caculate the indexes of countries within the split dataset.

import sys
import os
import math
import DP_RNN
import DP_GraphHelper

sys.path.append(os.path.relpath("/"))

from matplotlib import pyplot
from DP_RNN import DP_RNN
from DP_DataIngest import *
from DP_CSV import *

# Const ints
FIRST = 0
AVERAGE_COL = 805.24
AVERAGE_RENTAL = 542.61
AVERAGE_OCOL_COUNTRY = AVERAGE_RENTAL + AVERAGE_COL

# Const strings
COMMA_SEPARATOR = ','
VERTICAL_ROTATION = 'vertical'
TIME_COLUMN = 'time'
CPI_COLUMN = 'CPI'
COUNTRY = 'Cuba'
WAGE_DATASET = 'wage'
CPI_DATASET = 'cpi'
# File Paths
MODEL_LOCATION = 'generated_models/'
DATASET_LOCATION = 'datasets/'

CPI_DATASET_LOCATION = DATASET_LOCATION + 'Inflation-data - hcpi_m.csv'
CPI_MODEL_LOCATION = MODEL_LOCATION + 'cpi_model.keras'
WAGE_MODEL_LOCATION = MODEL_LOCATION + 'wage_model.keras'
WAGE_DATASET_LOCATION = DATASET_LOCATION + 'WagesPerCountry_WorldBank.csv' 

def TrainModels(cpiInflationDataSplit, wageDataClean):
    xTrain_CPI, yTrain_CPI = cpiInflationDataSplit[:1900, :48], cpiInflationDataSplit[:1900, -5:]
    xValid_CPI, yValid_CPI = cpiInflationDataSplit[1900:2000, :48], cpiInflationDataSplit[1900:2000, -5:]

    xTrain_Wages, yTrain_Wages = wageDataClean[1:200,:59], wageDataClean[1:200, -5:]
    xValid_Wages, yValid_Wages = wageDataClean[200:220,:59], wageDataClean[200:220, -5:]

    simpleCpiRnn = DP_RNN(150, 50, 'Simple')
    simpleWageRnn = DP_RNN(200, 100, 'Simple')

    lstmCpiRnn = DP_RNN(150, 50, 'LSTM')
    lstmWageRnn = DP_RNN(200, 100, 'LSTM')

    gruCpiRnn = DP_RNN(150, 50, 'GRU')
    gruWageRnn = DP_RNN(200, 100, 'GRU')

    simpleCPIHistory = simpleWageRnn.train(xTrain_Wages, yTrain_Wages, xValid_Wages, yValid_Wages, True, WAGE_DATASET)
    simpleWageHistory = simpleCpiRnn.train(xTrain_CPI, yTrain_CPI, xValid_CPI, yValid_CPI, True, CPI_DATASET)

    lstmCPIHistory = lstmWageRnn.train(xTrain_Wages, yTrain_Wages, xValid_Wages, yValid_Wages, True, WAGE_DATASET)
    lstmWageHistory = lstmCpiRnn.train(xTrain_CPI, yTrain_CPI, xValid_CPI, yValid_CPI, True, CPI_DATASET)

    gruCPIHistory = gruWageRnn.train(xTrain_Wages, yTrain_Wages, xValid_Wages, yValid_Wages, True, WAGE_DATASET)
    gruWageHistory = gruCpiRnn.train(xTrain_CPI, yTrain_CPI, xValid_CPI, yValid_CPI, True, CPI_DATASET)

    cpi_rnn.SaveModel(CPI_MODEL_LOCATION)
    wage_rnn.SaveModel(WAGE_MODEL_LOCATION)
    return cpi_rnn, wage_rnn

def RescaleDataRow(dataRow, maxValue):
    return [x * maxValue for x in dataRow]

def GetCountryWageData(country, wageMetaData, wageData):
    wageDataRow = []
    wageMetaDataRow = []

    for index, wageDataPoint in enumerate(wageData):
        countryName = wageMetaData[index][0].replace(QUOTE_MARKS, EMPTY_STRING)
        if countryName == country:
            wageDataRow.append([wageDataPoint])
            wageMetaDataRow = wageMetaData[index]
    return wageDataRow, wageMetaDataRow

def GetCountryCPIData(country, cpiMetaData, cpiData):
    cpiDataRow = []
    cpiMetaDataRow = []

    for index, cpiDataPoint in enumerate(cpiData):
        cpiMetaDataIndex = int(math.floor(index / 12))
        countryName = cpiMetaData[cpiMetaDataIndex][0] 
        if countryName == country:
            cpiDataRow.append([cpiDataPoint])
            cpiMetaDataRow.append(cpiMetaData[cpiMetaDataIndex])
            break
    return cpiDataRow, cpiMetaDataRow

cpiInflationData = ReadCSV(CPI_DATASET_LOCATION)
wagesPerCountry = ReadCSV(WAGE_DATASET_LOCATION)

cpiInflationMetaData, cpiInflationDataSplit = IngestCPIData(cpiInflationData)
wageMetaData, wageDataClean = IngestWageData(wagesPerCountry)

cpi_rnn = None
wage_rnn = None

print("datasets loaded.")

while((wage_rnn == None) | (cpi_rnn == None)):
    try:
        cpi_rnn = DP_RNN(CPI_MODEL_LOCATION)
        wage_rnn = DP_RNN(WAGE_MODEL_LOCATION)
    except:
        print('models not found continuing with training.')

    if(wage_rnn == None) | (cpi_rnn == None):
        cpi_rnn, wage_rnn = TrainModels(cpiInflationDataSplit, wageDataClean)

xTest_CPI, yTest_CPI = cpiInflationDataSplit[2000:, :48], cpiInflationDataSplit[2000:, -5:]
cpi_prediction = cpi_rnn.GetModel().predict(xTest_CPI)

xTest_Wages, yTest_Wages = wageDataClean[210:, :59], wageDataClean[210:, -5:]
wages_prediction = wage_rnn.GetModel().predict(xTest_Wages)

DP_GraphHelper.PlotPredictedData(xTest_CPI, cpi_prediction, yTest_CPI)
DP_GraphHelper.PlotPredictedData(xTest_Wages, cpi_prediction, yTest_Wages)

countryWageData, countryWageMetaData = GetCountryWageData(COUNTRY, wageMetaData, wageDataClean)
countryCPIData, countryCPIMetaData = GetCountryCPIData(COUNTRY, cpiInflationMetaData, cpiInflationDataSplit)

countryCPI = numpy.array(countryCPIData[FIRST])
countryWages = numpy.array(countryWageData[FIRST])

cpi_prediction = cpi_rnn.GetModel().predict(countryCPI)
wages_prediction = wage_rnn.GetModel().predict(countryWages)

lithaunianMaxWages = 0

countryCPIData = RescaleDataRow(countryCPIData[FIRST], countryCPIMetaData[FIRST][1])

val = countryCPIData[FIRST][len(countryCPIData[FIRST]) - 1]

countryCPIData = [x / val for x in countryCPIData]
countryCPIData = RescaleDataRow(countryCPIData, AVERAGE_OCOL_COUNTRY * 12)
countryWageData = RescaleDataRow(countryWageData[FIRST], countryWageMetaData[1])

cpi_prediction = RescaleDataRow(cpi_prediction, countryCPIMetaData[FIRST][1])
cpi_prediction = [x / val for x in cpi_prediction]
cpi_prediction = RescaleDataRow(cpi_prediction[FIRST], AVERAGE_OCOL_COUNTRY * 12)
wages_prediction = RescaleDataRow(wages_prediction[FIRST], countryWageMetaData[1])

DP_GraphHelper.PlotCountryPrediction(countryWageData[FIRST][10:], wages_prediction, countryCPIData[FIRST], cpi_prediction)

print('done')