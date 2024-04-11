import numpy
import matplotlib
from matplotlib import pyplot

FIRST = 0
LINED_DATA_POINTS_BLUE = 'b.-'
LINED_DATA_CROSSES_BLUE = 'bx-'
LINED_DATA_CROSSES_RED = 'rx-'
MEAN_ABSOLUTE_ERROR = 'mean_absolute_percentage_error'
MEAN_ABSOLUTE_ERROR_VALUE = 'val_' + MEAN_ABSOLUTE_ERROR
LOSS = 'loss'
EPOCHS = 'epochs'
ACCURACY = 'accuracy'
ERROR = 'error'
GRAPH_SAVE_LOCATION = 'generated_graphs/'


def PlotTrainingHistory(history, dataset, rnn_details):
    pyplot.plot(history.history[MEAN_ABSOLUTE_ERROR])
    pyplot.plot(history.history[MEAN_ABSOLUTE_ERROR_VALUE])
    pyplot.plot(history.history[LOSS])
    pyplot.xlabel(EPOCHS)
    pyplot.ylabel(ERROR)
    __SaveAndClearPlot(GRAPH_SAVE_LOCATION + 'TrainingHistory_' + rnn_details + '_' + dataset +'.jpg')

def PlotData(*args):
        for arg in args:
            pyplot.plot(arg, LINED_DATA_POINTS_BLUE)
        __SaveAndClearPlot(GRAPH_SAVE_LOCATION + 'SimpleGraph.jpg')        

def PlotTestData(*args):
    f, axis = pyplot.subplots(4, 4, figsize=(15,8))
    for idx, ax in enumerate(axis.flatten()):
      for arg in args:
        ax.plot(arg[idx], LINED_DATA_POINTS_BLUE)
      ax.grid(True)
    __SaveAndClearPlot(GRAPH_SAVE_LOCATION + 'PlottedTestData.jpg')

def PlotCountryPrediction(*args):
        predictionRange = 0

        for arg in args:
            dataSetLength = len(arg)
            dataSetRange = range(0, dataSetLength)
            if len(arg) > 5:
                pyplot.plot(dataSetRange, arg, LINED_DATA_POINTS_BLUE)
                predictionRange = range(dataSetLength, dataSetLength + 5)
            else:
                pyplot.plot(predictionRange, arg, LINED_DATA_CROSSES_RED)
        __SaveAndClearPlot(GRAPH_SAVE_LOCATION + 'CountryPrediction.jpg')



def PlotPredictedData(current, predicted, expected=[]):
    predictionRange = 0
    if (len(predicted[FIRST]) > 1):
        predictionRange = numpy.arange(len(current[FIRST]),
                                       len(current[FIRST]) + len(predicted[FIRST]))
    else:
        predictedIndex = len(current) + 1
    
    if(len(expected) == 0):
        return __PlotPredictedData(current, predicted, predictionRange)
    else:
        return __PlotPredictedData(current, predicted, predictionRange, expected)

def __PlotPredictedData(current, predicted, predictionRange, expected=[]):
    if(len(predicted) > 1):
        f,axes = pyplot.subplots(1, 2, figsize=(15,8))
        for idx, ax in enumerate(axes.flatten()):
            ax.plot(current[idx], LINED_DATA_POINTS_BLUE)
            ax.plot(predictionRange, predicted[idx], LINED_DATA_CROSSES_RED)
            if(len(expected) > 0):
                ax.plot(predictionRange, expected[idx], LINED_DATA_CROSSES_BLUE)
            ax.grid(True)
    else:
        pyplot.plot(current[FIRST], LINED_DATA_POINTS_BLUE)
        pyplot.plot(predictionRange, predicted[FIRST], LINED_DATA_CROSSES_RED)
        if(len(expected) > 0):
            pyplot.plot(predictionRange, expected[FIRST], LINED_DATA_CROSSES_BLUE)
    __SaveAndClearPlot(GRAPH_SAVE_LOCATION + 'PredictionSingular.jpg')

def __SaveAndClearPlot(plotName):
    pyplot.savefig(plotName)
    pyplot.clf()