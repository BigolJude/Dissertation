
import numpy
import csv
import pandas
import matplotlib
import sys
import os
import keras
import sklearn
import CPI_RNN
import CPI_DataIngest
import GraphHelper
import CSV

sys.path.append(os.path.relpath("/"))

from sklearn.preprocessing import MinMaxScaler
from matplotlib import pyplot
from CPI_RNN import CPI_RNN
from CPI_DataIngest import *
from CSV import *

FIRST = 0

COMMA_SEPARATOR = ','
VERTICAL_ROTATION = 'vertical'
TIME_COLUMN = 'time'
CPI_COLUMN = 'CPI'

cpiInflationData = ReadCSV('Inflation-data - hcpi_m.csv')
cpiInflationDataSplit = IngestData(cpiInflationData)

xTrain, yTrain = cpiInflationDataSplit[:1800,:52], cpiInflationDataSplit[:1800, -1]
xValid, yValid = cpiInflationDataSplit[1800:2000, :52], cpiInflationDataSplit[1800:2000, -1]
xTest, yTest = cpiInflationDataSplit[2000:, :52], cpiInflationDataSplit[2000:, -1]

GraphHelper.PlotTestData(xTrain)

cpi_rnn = CPI_RNN()
cpi_rnn.train(xTrain, yTrain, xValid, yValid, True)

prediction = cpi_rnn.GetModel().predict(xTest)

GraphHelper.PlotSinglePredictedData(xTest, yTest, prediction)
print('done')