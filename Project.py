import numpy
import csv
import pandas
import matplotlib
import keras
from matplotlib import pyplot

COMMA_SEPARATOR = ','
FIRST = 0
VERTICAL_ROTATION = 'vertical'

time = []
value = []
xPlots = []
with open('CPI - Inflation.csv', newline='') as csvFile:
    cpiInflation = csv.reader(csvFile, delimiter=' ', quotechar='|')
    index = 0
    for row in cpiInflation:
        if index > 5:
            values = row[FIRST].split(COMMA_SEPARATOR)
            time.append(values[0])
            value.append(float(values[1]))
            xPlots.append(index)
        index += 1

data = {'time': time, 'CPI': value}
dataFrame = pandas.DataFrame(data)

pyplot.plot(dataFrame['time'], dataFrame['CPI'])
pyplot.xticks(rotation=VERTICAL_ROTATION)
pyplot.show()

CPI_RNN = keras.models.Sequential([
    keras.layers.SimpleRNN(1, input_shape=(None, 1), return_sequences=True),
    keras.layers.SimpleRNN(10, return_sequences=True),
    keras.layers.Dense(1)
])

print(len(value))

print(value[0:])
print(value[0:len(value)])


xTrain, yTrain = [value[0:80]], [value[0:80]]
print("-----")
print(xTrain)
print(yTrain)

CPI_RNN.compile(loss='mse', optimizer='adam')
CPI_RNN.fit(xTrain, yTrain, epochs=1000)

y_pred = CPI_RNN.predict([value[80:81]])

data2 = {'time': time[:81], 'CPI': xTrain[:80].append(y_pred)}
dataFrame2 = pandas.DataFrame(data)

pyplot.plot(dataFrame2['time'], dataFrame2['CPI'])
pyplot.xticks(rotation=VERTICAL_ROTATION)
pyplot.show()