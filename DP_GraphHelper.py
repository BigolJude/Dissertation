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

def PlotTrainingHistory(history):
    pyplot.plot(history.history[MEAN_ABSOLUTE_ERROR])
    pyplot.plot(history.history[MEAN_ABSOLUTE_ERROR_VALUE])
    pyplot.plot(history.history[LOSS])
    pyplot.xlabel(EPOCHS)
    pyplot.ylabel(ACCURACY)
    pyplot.show()

def PlotData(*args):
        for arg in args:
            pyplot.plot(arg, LINED_DATA_POINTS_BLUE)
        pyplot.show()

def PlotTestData(*args):
    f, axis = pyplot.subplots(4, 4, figsize=(15,8))
    for idx, ax in enumerate(axis.flatten()):
      for arg in args:
        ax.plot(arg[idx], LINED_DATA_POINTS_BLUE)
      ax.grid(True)
    pyplot.show()

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
        pyplot.show()
    else:
        pyplot.plot(current[FIRST], LINED_DATA_POINTS_BLUE)
        pyplot.plot(predictionRange, predicted[FIRST], LINED_DATA_CROSSES_RED)
        if(len(expected) > 0):
            pyplot.plot(predictionRange, expected[FIRST], LINED_DATA_CROSSES_BLUE)
        pyplot.show()