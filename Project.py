import numpy
import csv
import pandas
import matplotlib
import keras
from matplotlib import pyplot

COMMA_SEPARATOR = ','
FIRST = 0
VERTICAL_ROTATION = 'vertical'
TIME_COLUMN = 'time'
CPI_COLUMN = 'CPI'

# Function
def DisplayGraph(dataFrame):
    pyplot.plot(dataFrame[TIME_COLUMN], dataFrame[CPI_COLUMN])
    pyplot.xticks(rotation=VERTICAL_ROTATION)


# End Functions

data = pandas.DataFrame({})

columns = []

#Main
with open('Inflation-data - hcpi_m.csv', newline='') as csvFile:
    cpiInflation = csv.reader(csvFile, delimiter=' ', quotechar='|')
    for row in cpiInflation:
        x = 0
        if x == 1:
            y = 0
            for column in row:
                if y == 5: 
                    columns.append(column.split(COMMA_SEPARATOR))
                y += 1
        else:
            for column in row:
                columns.append(column.split(COMMA_SEPARATOR))
        x += 1

columnsNames = columns[5:6]
columnsData = columns[7:]
columnsData2 = []


for rows in columnsData:
    if len(rows) > 10:
        values = []
        for string in rows[1:640]:
            try:
                string = float(string)
            except:
                string = 0
            values.append(string)
        columnsData2.append(values)

f,axes = pyplot.subplots(10, 10, figsize=(15, 8))
for idx, ax in enumerate(axes.flatten()):
    maxNum = float(max(columnsData2[idx])) + 100
    y_plots = []
    for i in range(0, round(maxNum + 1), 10):
        y_plots.append(i)
    ax.set_yticks(y_plots, y_plots)
    ax.set_ylim(0, maxNum)
    ax.set_xticks(columnsNames[1:])
    ax.plot(columnsData2[idx], 'b.-')
    ax.grid(True)

pyplot.show()

columnsNames = columnsNames[:640]

print(columnsNames)
print("------")
print(columnsData2)



data = {
    TIME_COLUMN: columnsNames,
    CPI_COLUMN: columnsData2
}

before = pandas.DataFrame(data)

DisplayGraph(before)
pyplot.show()

CPI_RNN = keras.models.Sequential([
    keras.layers.SimpleRNN(1, input_shape=(None, 1), return_sequences=True),
    keras.layers.SimpleRNN(10, return_sequences=True),
    keras.layers.Dense(1)
])

xTrain, yTrain = [value[0:80]], [value[0:80]]

CPI_RNN.compile(loss='mse', optimizer='adam')
CPI_RNN.fit(xTrain, yTrain, epochs=1000)

y_pred = CPI_RNN.predict([value[80:81]])

data2 = {
        TIME_COLUMN: time[:81], 
        CPI_COLUMN: xTrain[:80].append(y_pred)
}
results = pandas.DataFrame(data)

DisplayGraph(results)
# End Main