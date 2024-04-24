from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as DashBootstrap
import dash_leaflet as DashLeaflet
from dash_extensions.javascript import assign
from DP_CSV import *

def FormatResults(results):
    formattedResults = []
    formattedCOLResults = []
    for result in results:
        if(result[0] == 'cpi'):
            formattedCOLResult = []
            formattedCOLResult.append(result[1])
            formattedCOLResult.append([int(x) for x in result[2:]])
            formattedCOLResults.append(formattedCOLResult)
        else:
            formattedResult = []
            formattedResult.append(result[0])
            formattedResult.append([int(x) for x in result[1:]])
            formattedResults.append(formattedResult)
    return formattedResults, formattedCOLResults

def CalculateExpectedWages(results, colResults):
    expectedWages = []
    for result in results:
        expectedWageRow = []
        expectedWageRow.append(result[0])
        wageDataPoints = []
        for colResult in colResults:
            if colResult[0] == result[0]:
                for index, value in enumerate(result[1]):
                    wageDataPoints.append(value - colResult[1][index])
                break
        expectedWageRow.append(wageDataPoints)
        expectedWages.append(expectedWageRow)
    return expectedWages

def GetYearIndex(year):
    return year - 2003

colorScale = ['#E51F1F','#F2A134','#F7E379','#BBDB44','#44CE1B']
classes = [2000, 4000, 6000, 8000, 10000]
style = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)

results = ReadCSV('assets/UKWageResults.csv')
results, colResults = FormatResults(results)
expectedWages = CalculateExpectedWages(results, colResults)

styleHandle = assign("""function(feature, context){
    const {classes, colorScale, expectedWages, style, year} = context.hideout;
    for (let countyIndex = 0; countyIndex < expectedWages.length; countyIndex++)
    {
        console.log(year);
        for (let i = 0; i < classes.length; i++)
        {
            if (expectedWages[countyIndex][0].includes(feature.properties.EER13NM))
            {
                console.log("value: " + expectedWages[countyIndex][1][year])
                console.log("threshold: " + classes[i])
                if (expectedWages[countyIndex][1][year] < classes[i])
                {
                    style.fillColor = colorScale[i];
                    break;
                }
            }
        } 
    }
    return style;
}""")

app = Dash(name=__name__, external_stylesheets=[DashBootstrap.themes.FLATLY])
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='Development Project'),
            html.H2(children='Mapped Financial Risk by Area'),
            html.Div(id='dash-leaflet-container'),
            dcc.Slider(2003, 2028, 1, 
                       included=False,
                       marks=None, 
                       tooltip={"always_visible":True,
                                "placement": "bottom"},
                       id='date-slider')
        ],style={
            'display': 'flex',
            'flexDirection': 'column',
            'textAlign': 'center'})
    ], style={
        'display': 'flex',
        'justifyContent':'center',
        'alignContent':'centre'})
])

@callback(
    Output('dash-leaflet-container', 'children'),
    Input('date-slider', 'value'))
def updateOutput(value):
    return DashLeaflet.Map([
                DashLeaflet.TileLayer(),
                DashLeaflet.GeoJSON(url="/assets/eer.json", 
                                    zoomToBounds=True, 
                                    id="geojson",
                                    hideout=dict(classes=classes, colorScale=colorScale, expectedWages=expectedWages, style=style, year=GetYearIndex(value)), 
                                    style=styleHandle)
                ], style={'height': '50vh'}, center=[40, 10], zoom=6)

if __name__ == '__main__':
    app.run(debug=True)