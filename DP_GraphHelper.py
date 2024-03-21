import numpy
import matplotlib
from matplotlib import pyplot

FIRST = 0
LINED_DATA_POINTS_BLUE = 'b.-'
LINED_DATA_CROSSES_BLUE = 'bx-'
LINED_DATA_CROSSES_RED = 'rx-'

def PlotTrainingHistory(history):
    pyplot.plot(history.history['mean_absolute_percentage_error'])
    pyplot.plot(history.history['val_mean_absolute_percentage_error'])
    pyplot.plot(history.history['loss'])
    pyplot.xlabel('epochs')
    pyplot.ylabel('accuracy')
    pyplot.show()

def PlotTestData(data):
    f, axis = pyplot.subplots(1, 2, figsize=(15,8))
    for idx, ax in enumerate(axis.flatten()):
      ax.plot(data[idx], LINED_DATA_POINTS_BLUE)
      ax.grid(True)
    pyplot.show()

def PlotPredictedData(current, predicted, expected=[]):
    if(len(expected) == 0):
        predictionRange = numpy.arange(len(current[FIRST]),
                                       len(current[FIRST]) + len(predicted[FIRST]))
        expected = None
        return __PlotPredictedData(current, expected, predicted, predictionRange)

    if (len(predicted[FIRST]) > 1):
        predictionRange = numpy.arange(len(current[FIRST]),
                                       len(current[FIRST]) + len(predicted[FIRST]))
        return __PlotPredictedData(current, expected, predicted, predictionRange)
    else:
        predictedIndex = len(current) + 1
        return __PlotPredictedData(current, expected, predicted, predictedIndex)

def __PlotPredictedData(current, expected, predicted, predictionRange):
    f,axes = pyplot.subplots(1, 2, figsize=(15,8))
    for idx, ax in enumerate(axes.flatten()):
        ax.plot(current[idx], LINED_DATA_POINTS_BLUE)
        ax.plot(predictionRange, predicted[idx], LINED_DATA_CROSSES_RED)
        if(len(expected)!=0):
            ax.plot(predictionRange, expected[idx], LINED_DATA_CROSSES_BLUE)
        ax.grid(True)
    pyplot.show()    