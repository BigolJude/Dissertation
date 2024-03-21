# Things to do:
# - xml comments on functions
# - save and load the models0
# - add in some form of hill climbing
# - test the model with a full dataset.
# - code clean up.


import sys
import os
import DP_RNN
import DP_DataIngest
import DP_GraphHelper
import DP_CSV

sys.path.append(os.path.relpath("/"))

from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot
from DP_RNN import DP_RNN
from DP_DataIngest import *
from DP_CSV import *

FIRST = 0

COMMA_SEPARATOR = ','
VERTICAL_ROTATION = 'vertical'
TIME_COLUMN = 'time'
CPI_COLUMN = 'CPI'
COUNTRY_LITHUANIA = 'Lithuania'

cpiInflationData = ReadCSV('Inflation-data - hcpi_m.csv')
wagesPerCountry = ReadCSV('WagesPerCountry_WorldBank.csv')

cpiInflationMetaData, cpiInflationDataSplit = IngestCPIData(cpiInflationData)
wageMetaData, wageDataClean = IngestWageData(wagesPerCountry)

lithuanianWageData = []
lithuanianMetaData = []

for country in wageMetaData:
    countryName = country[FIRST].replace("\"","")
    if(countryName == COUNTRY_LITHUANIA):
        lithuanianWageData = wageDataClean[country[2]]
        lithuanianMetaData = country

lithuanianWageData = numpy.array([lithuanianWageData])

xTrain_CPI, yTrain_CPI = cpiInflationDataSplit[:1900, :48], cpiInflationDataSplit[:1900, -5:]
xValid_CPI, yValid_CPI = cpiInflationDataSplit[1900:2000, :48], cpiInflationDataSplit[1900:2000, -5:]
xTest_CPI, yTest_CPI = cpiInflationDataSplit[2000:, :48], cpiInflationDataSplit[2000:, -5:]

xTrain_Wages, yTrain_Wages = wageDataClean[1:200,:59], wageDataClean[1:200, -5:]
xValid_Wages, yValid_Wages = wageDataClean[200:220,:59], wageDataClean[200:220, -5:]
xTest_Wages, yTest_Wages = wageDataClean[210:, :59], wageDataClean[210:, -5:]

DP_GraphHelper.PlotTestData(xTrain_CPI)
DP_GraphHelper.PlotTestData(xTrain_Wages)

cpi_rnn = DP_RNN(initialLayerNeurons=80, epochs=5)
wage_rnn = DP_RNN(initialLayerNeurons=80, epochs=5)

wage_rnn.train(xTrain_Wages, yTrain_Wages, xValid_Wages, yValid_Wages, True)
cpi_rnn.train(xTrain_CPI, yTrain_CPI, xValid_CPI, yValid_CPI, True)

cpi_prediction = cpi_rnn.GetModel().predict(xTest_CPI)
wages_prediction = wage_rnn.GetModel().predict(xTest_Wages)

DP_GraphHelper.PlotPredictedData(xTest_CPI, yTest_CPI, cpi_prediction)
DP_GraphHelper.PlotPredictedData(xTest_Wages, yTest_Wages, wages_prediction)

lithuanian_prediction = wage_rnn.GetModel().predict([lithuanianWageData])

DP_GraphHelper.PlotPredictedData(lithuanianWageData, lithuanian_prediction)
print('done')