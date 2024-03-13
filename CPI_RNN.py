import keras
import GraphHelper


class CPI_RNN():
    def __init__(self):
        self.__cpi_rnn = keras.models.Sequential([
            keras.layers.GRU(30, input_shape=(None, 1), return_sequences=True),
            keras.layers.GRU(25, return_sequences=True),
            keras.layers.GRU(25),
            keras.layers.Dense(1)])
        self.__learningRate_schedule = keras.optimizers.schedules.ExponentialDecay(
            initial_learning_rate=1e-3,
            decay_steps=10000,
            decay_rate=0.9)
        self.__optimizer = keras.optimizers.Adam(learning_rate=self.__learningRate_schedule)
        self.__cpi_rnn.compile(loss='mse', optimizer=self.__optimizer, metrics=[keras.metrics.MeanAbsolutePercentageError()])

    def train(self, xTrain, yTrain, xValid, yValid, showHistory):
        history = self.__cpi_rnn.fit(xTrain, yTrain, epochs=5, batch_size=30, validation_data=[xValid, yValid])
        if(showHistory):
            GraphHelper.PlotTrainingHistory(history)

    def GetModel(self):
        return self.__cpi_rnn