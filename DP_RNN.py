import keras
import DP_GraphHelper
import keras_tuner

FIRST = 0
SAVE_FORMAT = 'keras'
MEAN_ABSOLUTE_ERROR = 'mae'
MEAN_SQUARED_ERROR = 'mse'
GRU_SETTING = 'GRU'
LSTM_SETTING = 'LSTM'
SIMPLE_RNN_SETTING = 'Simple'
DENSE_LAYER_ACTIVATION = 'relu'
MEAN_ABSOLUTE_ERROR_VAL = 'mean_absolute_percentage_error'


class DP_RNN():
    def __init__(self, *args):
        if len(args) == 3:
            self.__initialLayerNeurons = args[0] 
            self.__epochs = args[1]
            self.__type = args[2]
        elif len(args) == 1:
            modelLocation = args[0]
            self.__LoadModel(modelLocation)

    def train(self, xTrain, yTrain, xValid, yValid, showHistory, dataset):
        self.__BuildModel(keras_tuner.HyperParameters())
        tuner = keras_tuner.Hyperband(self.__BuildModel, project_name=self.GetModelDescription(), objective=MEAN_ABSOLUTE_ERROR_VAL, max_epochs=20)
        tuner.search(xTrain, yTrain, epochs=10 , validation_data=[xValid, yValid])
        self.__rnn = tuner.get_best_models()[FIRST]
        history = self.__rnn.fit(xTrain, yTrain, epochs=self.__epochs , validation_data=[xValid, yValid])
        if(showHistory):
            DP_GraphHelper.PlotTrainingHistory(history, dataset, self.GetModelDescription())
        return history

    def GetModel(self):
        return self.__rnn
    
    def SaveModel(self, fileLocation):
        return self.__rnn.save(fileLocation, overwrite=True, save_format=SAVE_FORMAT)
    
    def __LoadModel(self, fileLocation):
        self.__rnn = keras.models.load_model(fileLocation)

    def __BuildModel(self, hp):
        rnnLayers = 0
        firstLayer  = range(60, self.__initialLayerNeurons + 1, 20)
        secondLayer = range(20, int(round(self.__initialLayerNeurons / 2, 0)) + 1, 10)
        thirdLayer = range(10, int(round(self.__initialLayerNeurons / 4, 0)) + 1, 5)

        if(self.__type == GRU_SETTING):
            rnnLayers = [
                keras.layers.GRU(hp.Choice('units1', firstLayer),
                                 input_shape=(None, 1), 
                                 return_sequences=True),
                keras.layers.GRU(hp.Choice('units2', secondLayer), 
                                 return_sequences=True),
                keras.layers.GRU(hp.Choice('units3', thirdLayer))]
        if(self.__type == LSTM_SETTING):
            rnnLayers = [
                keras.layers.LSTM(hp.Choice('units1', firstLayer),
                                 input_shape=(None, 1), 
                                 return_sequences=True),
                keras.layers.LSTM(hp.Choice('units2', secondLayer), 
                                 return_sequences=True),
                keras.layers.LSTM(hp.Choice('units3', thirdLayer))]
        if(self.__type == SIMPLE_RNN_SETTING):
            rnnLayers = [
                keras.layers.SimpleRNN(hp.Choice('units1', firstLayer),
                                 input_shape=(None, 1), 
                                 return_sequences=True),
                keras.layers.SimpleRNN(hp.Choice('units2', secondLayer), 
                                 return_sequences=True),
                keras.layers.SimpleRNN(hp.Choice('units3', thirdLayer))]
        rnnLayers.append(keras.layers.Dense(5))
        rnn = keras.models.Sequential(rnnLayers)
        self.__learningRate_schedule = keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=1e-3,
            decay_steps=10000,
            decay_rate=0.9)
        self.__optimizer = keras.optimizers.Adam(learning_rate=self.__learningRate_schedule)
        rnn.compile(loss=MEAN_ABSOLUTE_ERROR, optimizer=self.__optimizer, metrics=[keras.metrics.MeanAbsolutePercentageError()])
        return rnn

    def GetModelDescription(self):
        return str(self.__type)+ '_' + str(self.__epochs) + '_' + str(self.__initialLayerNeurons)
    