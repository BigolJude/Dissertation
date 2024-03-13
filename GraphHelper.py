import numpy
import matplotlib
from matplotlib import pyplot

def PlotTrainingHistory(history):
    pyplot.plot(history.history['mean_absolute_percentage_error'])
    pyplot.plot(history.history['val_mean_absolute_percentage_error'])
    pyplot.plot(history.history['loss'])
    pyplot.xlabel('epochs')
    pyplot.ylabel('accuracy')
    pyplot.show()

def PlotTestData(data):
    f, axis = pyplot.subplots(4, 4, figsize=(15,8))
    for idx, ax in enumerate(axis.flatten()):
      ax.plot(data[idx], 'b.-')
      ax.grid(True)
    pyplot.show()

def PlotMultiPredictedData(current, expected, predicted):
    predictionRange = numpy.arange(len(current[0]),len(expected[0]))
    f,axes = pyplot.subplots(4, 3,figsize=(15,8))
    for idx, ax in enumerate(axes.flatten()):
       ax.plot(current[idx], 'b.-')
       ax.plot(predictionRange, predicted[idx], 'ro-')
       ax.plot(predictionRange, expected[idx], 'bo-')
       ax.grid(True)
    pyplot.show()

def PlotSinglePredictedData(current, expected, predicted):
    f,axes = pyplot.subplots(4, 3,figsize=(15,8))
    for idx, ax in enumerate(axes.flatten()):
        ax.plot(current[idx], 'b.-')
        ax.plot(53, predicted[idx], 'ro-')
        ax.plot(53, expected[idx], 'bo-')
        ax.grid(True)
    pyplot.show()