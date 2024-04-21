from dash import Dash, dcc, html
import dash_bootstrap_components as DashBootstrap
import dash_leaflet as DashLeaflet
from dash_extensions.javascript import assign
from DP_CSV import *


def FormatResults(results):
    formattedResults = []
    for result in results:
        formattedResult = []
        formattedResult.append(result[0])
        formattedResult.append([int(x) for x in result[1:]])
        formattedResults.append(formattedResult)
    return formattedResults

def CalculateExpectedWages(results):
    expectedWages = []
    for result in results:
        expectedWageRow = []
        expectedWageRow.append(result[0])
        wageDataPoints = []
        for index, value in enumerate(result[1]):
            wageDataPoints.append(value - results[len(results) - 1][1][index])
        expectedWageRow.append(wageDataPoints)
        expectedWages.append(expectedWageRow)
    return expectedWages

classes = [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000]
results = ReadCSV('assets/UKWageResults.csv')

results = FormatResults(results)
expectedWages = CalculateExpectedWages(results)

style_handle = assign("""function(feature, context){
    const {classes, numbers, results} = context.hideout;
    
    for (let i = 0; i < classes.length; i++)
      {
        if (value >)
        return {fillColor: 'grey', color: 'grey'}
      }
}""")

app = Dash(name=__name__, external_stylesheets=[DashBootstrap.themes.SLATE])
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='Development Project'),
            html.H2(children='Mapped Financial Risk by Area'),
            DashLeaflet.Map([
                DashLeaflet.TileLayer(),
                DashLeaflet.GeoJSON(url="/assets/eer.json", zoomToBounds=True, id="geojson",
                                   hideout=dict(selected=[]), style=style_handle)
                ], style={'height': '50vh'}, center=[40, 10], zoom=6)
        ],style={
            'display': 'flex',
            'flexDirection': 'column',
            'textAlign': 'center'})
    ], style={
        'display': 'flex',
        'justifyContent':'center',
        'alignContent':'centre'})
])

if __name__ == '__main__':
    app.run(debug=True)