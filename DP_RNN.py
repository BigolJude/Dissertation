import keras
import DP_GraphHelper

SAVE_FORMAT = 'keras'
MEAN_ABSOLUTE_ERROR = 'mae'
MEAN_SQUARED_ERROR = 'mse'

class DP_RNN():
    def __init__(self, *args):
        if len(args) == 2:
            initialLayerNeurons = args[0] 
            self.__epochs = args[1]
            self.__rnn = keras.models.Sequential([
                keras.layers.GRU(initialLayerNeurons, input_shape=(None, 1), return_sequences=True),
                keras.layers.GRU(int(round(initialLayerNeurons / 2, 0)), return_sequences=True),
                keras.layers.GRU(int(round(initialLayerNeurons / 4, 0))),
                keras.layers.Dense(5)])
            self.__learningRate_schedule = keras.optimizers.schedules.ExponentialDecay(
                initial_learning_rate=1e-3,
                decay_steps=10000,
                decay_rate=0.9)
            self.__optimizer = keras.optimizers.Adam(learning_rate=self.__learningRate_schedule)
            self.__rnn.compile(loss=MEAN_ABSOLUTE_ERROR, optimizer=self.__optimizer, metrics=[keras.metrics.MeanAbsolutePercentageError()])
        if len(args) == 1:
            modelLocation = args[0]
            self.__LoadModel(modelLocation)

    def train(self, xTrain, yTrain, xValid, yValid, showHistory):
        history = self.__rnn.fit(xTrain, yTrain, epochs=self.__epochs, validation_data=[xValid, yValid])
        if(showHistory):
            DP_GraphHelper.PlotTrainingHistory(history)

    def GetModel(self):
        return self.__rnn
    
    def SaveModel(self, fileLocation):
        return self.__rnn.save(fileLocation, overwrite=True, save_format=SAVE_FORMAT)
    
    def __LoadModel(self, fileLocation):
        self.__rnn = keras.models.load_model(fileLocation)