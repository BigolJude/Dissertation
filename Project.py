# Things to do:
# - xml comments on functions
# - add in some form of hill climbing
# - test the model with a full dataset.
# - code clean up.
# - do some arethmatic to caculate the indexes of countries within the split dataset.
# - data still needs to be destringerfied on Countries.

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
AVERAGE_COL_LITHUANIA = 846.9
AVERAGE_RENTAL_LITHUANIA = 1000
AVERAGE_OCOL_LITHUANIA = AVERAGE_RENTAL_LITHUANIA + AVERAGE_COL_LITHUANIA

# Const strings
COMMA_SEPARATOR = ','
VERTICAL_ROTATION = 'vertical'
TIME_COLUMN = 'time'
CPI_COLUMN = 'CPI'
COUNTRY_LITHUANIA = 'United Kingdom'

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

    cpi_rnn = DP_RNN(initialLayerNeurons=150, epochs=50)
    wage_rnn = DP_RNN(initialLayerNeurons=200, epochs=100)

    wage_rnn.train(xTrain_Wages, yTrain_Wages, xValid_Wages, yValid_Wages, True)
    cpi_rnn.train(xTrain_CPI, yTrain_CPI, xValid_CPI, yValid_CPI, True)

    cpi_rnn.SaveModel(CPI_MODEL_LOCATION)
    wage_rnn.SaveModel(WAGE_MODEL_LOCATION)
    return cpi_rnn, wage_rnn

def RescaleDataRow(dataRow, maxValue):
    scaledDataRow = []

    for dataPoint in dataRow:
        scaledDataRow.append(dataPoint * maxValue)
    return scaledDataRow

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

lithuanianWageData, lithuanianWageMetaData = GetCountryWageData(COUNTRY_LITHUANIA, wageMetaData, wageDataClean)
lithuanianCPIData, lithuanianCPIMetaData = GetCountryCPIData(COUNTRY_LITHUANIA, cpiInflationMetaData, cpiInflationDataSplit)

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

cpi_prediction = cpi_rnn.GetModel().predict(lithuanianCPIData)
wages_prediction = wage_rnn.GetModel().predict(lithuanianWageData)

lithaunianMaxWages = 0

for metaData in wageMetaData:
    country = metaData[FIRST].replace(QUOTE_MARKS, EMPTY_STRING)
    if country == COUNTRY_LITHUANIA:
        lithuanianMaxWages = metaData[1]


lithuanianCPIData = RescaleDataRow(lithuanianCPIData[FIRST], lithuanianCPIMetaData[FIRST][1])

val = lithuanianCPIData[FIRST][len(lithuanianCPIData[FIRST]) - 1]

lithuanianCPIData = [x / val for x in lithuanianCPIData]
lithuanianCPIData = RescaleDataRow(lithuanianCPIData, AVERAGE_OCOL_LITHUANIA * 12)
lithuanianWageData = RescaleDataRow(lithuanianWageData[FIRST], lithuanianMaxWages); 

DP_GraphHelper.PlotData(lithuanianWageData[FIRST][10:], lithuanianCPIData[FIRST])

print('done')