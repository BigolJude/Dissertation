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

# Const strings
COMMA_SEPARATOR = ','
VERTICAL_ROTATION = 'vertical'
TIME_COLUMN = 'time'
CPI_COLUMN = 'CPI'
COUNTRY = 'United Kingdom'
WAGE_DATASET = 'wage'
CPI_DATASET = 'cpi'
SIMPLE_RNN = 'Simple'
LSTM_RNN = 'LSTM'
GRU_RNN = 'GRU'
APPEND = 'a'
MODEL_FILE_TYPE = '.keras'
MODEL_TYPES = [SIMPLE_RNN, LSTM_RNN, GRU_RNN]

# File Paths
MODEL_LOCATION = 'generated_models/'
DATASET_LOCATION = 'datasets/'
ASSETS_LOCATION = 'assets/'

CPI_DATASET_LOCATION = DATASET_LOCATION + 'Inflation-data - hcpi_m.csv'
WAGE_DATASET_LOCATION = DATASET_LOCATION + 'WagesPerCountry_WorldBank.csv'
WAGE_UK_DATASET_LOCATION = DATASET_LOCATION + 'CBP-8456.csv' 
OCOL_UK_DATASET_LOCATION = DATASET_LOCATION + 'UKCOLArea.csv'

def TrainModels(cpiInflationDataSplit, wageDataClean):
    xTrain_CPI, yTrain_CPI = cpiInflationDataSplit[:1900, :48], cpiInflationDataSplit[:1900, -5:]
    xValid_CPI, yValid_CPI = cpiInflationDataSplit[1900:2000, :48], cpiInflationDataSplit[1900:2000, -5:]

    xTrain_Wages, yTrain_Wages = wageDataClean[1:200,:59], wageDataClean[1:200, -5:]
    xValid_Wages, yValid_Wages = wageDataClean[200:220,:59], wageDataClean[200:220, -5:]

    cpiModels = GenerateModels(80, 50)
    cpiPercentageErrors = []

    for index, model in enumerate(cpiModels):
        history = model.train(xTrain_CPI, yTrain_CPI, xValid_CPI, yValid_CPI, True, CPI_DATASET)
        errorRate = history.history['mean_absolute_percentage_error']

        cpiPercentageErrors.append(errorRate)
        cpiTrainingHistoryFile = open("assets/CPI_Models_TrainingHistory.csv", APPEND)
        cpiTrainingHistoryFile.write(CPI_DATASET + '_' + model.GetModelType() + ', ' + str(errorRate[len(errorRate) - 1]) + '\n')
        cpiTrainingHistoryFile.close()
        model.SaveModel(MODEL_LOCATION + CPI_DATASET + '_' + model.GetModelType() + MODEL_FILE_TYPE)
        print(str(index + 1) +' out of' + str(len(cpiModels)) + 'trained')

    wageModels = GenerateModels(140, 150)
    wagePercentageErrors = []

    for index, model in enumerate(wageModels):
        history = model.train(xTrain_Wages, yTrain_Wages, xValid_Wages, yValid_Wages, True, WAGE_DATASET)

        errorRate = history.history['mean_absolute_percentage_error']
        wagePercentageErrors.append(errorRate)
        wageTrainingHistoryFile = open("assets/Wage_Models_TrainingHistory.csv", APPEND)
        wageTrainingHistoryFile.write(CPI_DATASET + '_' + model.GetModelType() + ', ' + str(errorRate[len(errorRate) - 1]) + '\n')
        wageTrainingHistoryFile.close()
        model.SaveModel(MODEL_LOCATION + WAGE_DATASET + '_' + model.GetModelType() + MODEL_FILE_TYPE)
        print(str(index + 1) +' out of' + str(len(wageModels)) + 'trained')

    return cpiModels, wageModels

def GenerateModels(maxNeurons, maxEpochs):
    models = []
    for model in MODEL_TYPES:
        models.append(DP_RNN(maxNeurons, maxEpochs, model))
    return models

def GetBestModel(percentageErrors, models):
    minError = 100
    minIndex = 0

    for index, cpiPercentageError in enumerate(percentageErrors):
        if minError > cpiPercentageError[len(cpiPercentageError) - 1]:
            minIndex = index
            minError = cpiPercentageError[len(cpiPercentageError) - 1]

    return models[minIndex]

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

cpiInflationDataset = ReadCSV(CPI_DATASET_LOCATION)
wagesDataset = ReadCSV(WAGE_DATASET_LOCATION)
ukWagesDataset = ReadCSV(WAGE_UK_DATASET_LOCATION)
ukCOLDataset = ReadCSV(OCOL_UK_DATASET_LOCATION)

cpiInflationMetaData, cpiInflationDataSplit = IngestCPIData(cpiInflationDataset)
wageMetaData, wageDataClean = IngestWageData(wagesDataset)
ukMetaData, ukWagesByLocation = IngestUKWageData(ukWagesDataset)
ukCOLByLocation = IngestUKCOLData(ukCOLDataset)

print("datasets loaded.")

cpiModels = []
wageModels = []

while((len(cpiModels) == 0) | (len(wageModels) == 0)):
    try:
        for model in MODEL_TYPES:
            cpiModels.append(DP_RNN(MODEL_LOCATION + CPI_DATASET + '_' + model + MODEL_FILE_TYPE))
        for model in MODEL_TYPES:
            wageModels.append(DP_RNN(MODEL_LOCATION + WAGE_DATASET + '_' + model + MODEL_FILE_TYPE))
        break
    except:
        print('Some models not found continuing with training.')

    cpiModels, wageModels = TrainModels(cpiInflationDataSplit, wageDataClean)

xTest_CPI, yTest_CPI = cpiInflationDataSplit[2000:, :48], cpiInflationDataSplit[2000:, -5:]
for cpiModel in cpiModels:
    cpiPrediction = cpiModel.GetModel().predict(xTest_CPI)
    DP_GraphHelper.PlotPredictedData(xTest_CPI, cpiPrediction, yTest_CPI)

xTest_Wages, yTest_Wages = wageDataClean[210:, :59], wageDataClean[210:, -5:]
for wageModel in wageModels:
    wagesPrediction = wageModel.GetModel().predict(xTest_Wages)
    DP_GraphHelper.PlotPredictedData(xTest_Wages, wagesPrediction, yTest_Wages)

countryWageData, countryWageMetaData = GetCountryWageData(COUNTRY, wageMetaData, wageDataClean)
countryCPIData, countryCPIMetaData = GetCountryCPIData(COUNTRY, cpiInflationMetaData, cpiInflationDataSplit)

countryCPI = numpy.array(countryCPIData[FIRST])
countryWages = numpy.array(countryWageData[FIRST])

for modelIndex, wageModel in enumerate(wageModels):
    wageExportData = []
    wagesPrediction = wageModel.GetModel().predict(ukWagesByLocation)
    for index, wages in enumerate(ukWagesByLocation):
        ukWageValues = (RescaleDataRow(RescaleDataRow(wages, ukMetaData[index][1]), 52))
        ukWagePredictions = (RescaleDataRow(RescaleDataRow(wagesPrediction[FIRST], ukMetaData[index][1]), 52))
        wageExportData.append(
            COMMA_SEPARATOR.join([
                ukMetaData[index][FIRST], 
                COMMA_SEPARATOR.join([str(int(round(x[FIRST], 0))) for x in ukWageValues]), 
                COMMA_SEPARATOR.join([str(int(round(x, 0))) for x in ukWagePredictions])]))
    wageExportData = [[x] for x in wageExportData]
    WriteCSV(ASSETS_LOCATION + 'UKWageResults_' + MODEL_TYPES[modelIndex] + '.csv', wageExportData)

countryCPIData = RescaleDataRow(countryCPIData[FIRST], countryCPIMetaData[FIRST][1])
targetIndexVal = countryCPIData[FIRST][len(countryCPIData[FIRST]) - 1]

countryCPIData = [x / targetIndexVal for x in countryCPIData]
countryCPIData = [x[FIRST] for x in countryCPIData[FIRST]]

for index, cpiModel in enumerate(cpiModels):
    cpiPrediction = cpiModel.GetModel().predict(countryCPI)
    cpiPrediction = RescaleDataRow(cpiPrediction, countryCPIMetaData[FIRST][1])
    cpiPrediction = [x / targetIndexVal for x in cpiPrediction]
    colExportData = []
    for county in ukCOLByLocation:
        countyCOLData = RescaleDataRow(countryCPIData, (county[1] + county[2]) * 12)
        countyCOLPredictions = RescaleDataRow(cpiPrediction[FIRST], (county[1] + county[2]) * 12)
        colExportData.append(
            COMMA_SEPARATOR.join([
                CPI_DATASET,
                county[0],
                COMMA_SEPARATOR.join([str(int(round(x, 0))) for x in countyCOLData[(len(countyCOLData) - len(wages)):]]), 
                COMMA_SEPARATOR.join([str(int(round(x, 0))) for x in countyCOLPredictions])]))
    colExportData = [[x] for x in colExportData]
    WriteCSV(ASSETS_LOCATION + 'UKCOLResults_' + MODEL_TYPES[index] + '.csv', colExportData)

print('done')