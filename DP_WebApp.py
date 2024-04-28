import dash_bootstrap_components as DashBootstrap
import dash_leaflet as DashLeaflet
import plotly.graph_objects as GraphObjects
import plotly.express as PlotlyExpress
import dash_daq as daq
import pandas
import numpy
from dash import Dash, dcc, html, Input, Output, callback, dash_table
from dash_extensions.javascript import assign
from DP_CSV import *

ASSETS_LOCATION = 'assets/'
GEOJSON_LOCATION = '/assets/eer.json'
GRAPH_LOCATIONS = 'assets/generated_graphs/'
ASSETS_WAGE_LOCATION = 'UKWageResults_'
ASSETS_COL_LOCATION = 'UKCOLResults_'
ASSETS_WAGE_MODEL_HISTORY_LOCATION = ASSETS_LOCATION + 'CPI_Models_TrainingHistory.csv'
ASSETS_CPI_MODEL_HISTORY_LOCATION = ASSETS_LOCATION + 'Wage_Models_TrainingHistory.csv'
EXPECTED_FILE_TYPE = '.csv'
SIMPLE_TAG = 'Simple'
LSTM_TAG = 'LSTM'
GRU_TAG = 'GRU'

COLOUR_SCALE = ['#E51F1F','#F2A134','#F7E379','#BBDB44','#44CE1B']
CLASSES = [2000, 4000, 6000, 8000, 10000]
MODEL_OPTIONS = [SIMPLE_TAG, LSTM_TAG, GRU_TAG]
START_YEAR = 2003
STYLE = dict(weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)
STYLE_HANDLE = assign("""function(feature, context){
    const {classes, colorScale, expectedWages, style, year} = context.hideout;
    for (let countyIndex = 0; countyIndex < expectedWages.length; countyIndex++)
    {
        console.log(year);
        for (let i = 0; i < classes.length; i++)
        {
            if (expectedWages[countyIndex][0].includes(feature.properties.EER13NM))
            {
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

global expectedWages
global wageResults
global colResults
global year

def FormatResults(results):
    formattedResults = []

    buffer = 0
    if(results[0][0] == 'cpi'):
        buffer = 1
    for result in results:
        formattedResult = []
        formattedResult.append(result[buffer])
        formattedResult.append([int(x) for x in result[buffer + 1:]])
        formattedResults.append(formattedResult)
    return formattedResults

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

def SwitchDataset(dataset):
    results = ReadCSV(ASSETS_LOCATION + dataset + EXPECTED_FILE_TYPE)
    results = FormatResults(results)
    return results

def GetCountyInfoPanel(feature=None):
    values = []
    if feature:
        countyName = feature['properties']['EER13NM']
        if(countyName == 'Eastern'):
            countyName = 'East'
        values.append(html.H4(children=countyName))
        values.append(html.Br())
        yearIndex = GetYearIndex(year)
        for county in expectedWages:
            if county[0] == countyName:
                 values.append(html.B('Expected Savings: ' + str(county[1][yearIndex])))
                 values.append(html.Br())
        for county in colResults:
            if county[0] == countyName:
                values.append(html.B('Cost of living: ' + str(county[1][yearIndex])))
                values.append(html.Br())
        for county in wageResults:
            if county[0] == countyName:
                values.append(html.B('Wages:' + str(county[1][yearIndex])))
                values.append(html.Br())
    return values

def GenerateModelBarchart(data, name):
    labels, data = zip(*[(x[0], float(x[1])) for x in data])
    figure = GraphObjects.Figure()
    figure.add_trace(GraphObjects.Bar(x=labels, y=data, name=name))
    return figure

cpiModelData = ReadCSV(ASSETS_CPI_MODEL_HISTORY_LOCATION)
wageModelData = ReadCSV(ASSETS_WAGE_MODEL_HISTORY_LOCATION)

cpiBar = GenerateModelBarchart(cpiModelData, 'CPI Model Error Rates')
wageBar = GenerateModelBarchart(wageModelData, 'Wage Model Error Rates')

wageResults = SwitchDataset(ASSETS_WAGE_LOCATION + SIMPLE_TAG)
colResults = SwitchDataset(ASSETS_COL_LOCATION + SIMPLE_TAG)
expectedWages = CalculateExpectedWages(wageResults, colResults)
year = 2003

app = Dash(name=__name__, 
           external_stylesheets=[DashBootstrap.themes.JOURNAL],
           suppress_callback_exceptions=True)
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='Development Project'),
            html.H2(children='Mapped Financial Risk by Area (Expected Savings)'),
            html.Div(id='dash-leaflet-container'),
            dcc.Slider(2003, 2028, 1, 
                       included=False,
                       marks=None, 
                       value=year,
                       tooltip={"always_visible":True,
                                "placement": "bottom"},
                       id='date-slider'),
            html.Div(id="county-info"),
            html.Div([
                html.Div([
                    html.H3(children='Wages model.'),
                    dcc.RadioItems(MODEL_OPTIONS, 
                                   value='Simple', 
                                   inline=True,
                                   id='wages-model-radio',
                                   style={
                                       'display': 'flex',
                                       'alignContent': 'center',
                                       'justifyContent': 'space-evenly',
                                       'border': 'aquamarine',
                                       'borderStyle': 'inset',
                                       'borderRadius': '10px',
                                       'fontSize': '20px'
                                   })
                ], style={'padding':'1vh',
                          'width':'700px'}),
                html.Div([
                    html.H3(children='Cost of living model.'),
                    dcc.RadioItems(MODEL_OPTIONS, 
                                   value='Simple', 
                                   inline=True,
                                   id='col-model-radio',
                                   style={
                                       'display': 'flex',
                                       'alignContent': 'center',
                                       'justifyContent': 'space-evenly',
                                       'border': 'aquamarine',
                                       'borderStyle': 'inset',
                                       'borderRadius': '10px',
                                       'fontSize': '20px'})
                ], style={'padding':'1vh',
                          'width':'700px'}),
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'center'
            }),
            html.Div([
                dcc.Graph(id='col-line'),
                dcc.Graph(id='wages-line')
            ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'center'
            }),
            html.H2(children='Table of Calculated Savings by Area',
                    style={'padding':'1vh'}),
            
            html.Div(id='datatable'),
            daq.ToggleSwitch(
                label='Predictions only',
                labelPosition='bottom',
                id='predictions-toggle'
            ),
            html.H2(children='Background of the project.'),
            html.P(children='Over the period of the COVID pandemic there has seen a sharp rise in the cost of living for the average person within the UK. A large majority of people have found a decline in purchasing power and, due to this, many have fallen further into poverty. The project is designed to display to a governing body to assist in descision making. The graphs above display cost of living and wages predicted to 2028 and the map displays the savings calculated from both of these statistics.',
                   style={'width': '1400px',
                          'alignSelf': 'center'}),
            html.P(children='Disclaimer: Predictions are not 100% accurate and are only intended to aid and be combined with traditional forcasting methods',
                   style={'color': 'red'}),
            html.H2(children='Evaluation of the model.'),
            html.P(children='Using the World Banks dataset on Wages and Headline CPI Inflation, we can see that the CPI predictions are fairly accurate across the board however Wages struggles with its error rate and overfitting errors. The networks were individually trained for each recurrant layer type via Keras-Tuner using Hyperband.',
                   style={'width': '1400px',
                          'alignSelf': 'center'}),
            html.Div([
                html.Div([
                    html.H3(children='Error rate of the CPI Models.'),
                    dcc.Graph(figure=cpiBar),
                ], style={'width':'700px'}),
                html.Div([
                    html.H3(children='Error rate of the Wage Models.'),
                    dcc.Graph(figure=wageBar),
                ], style={'width':'700px'})
                ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'center'
            }),
            html.Div([
                html.H3(children='Training History'),
                html.Div([
                    html.Div([
                        html.H3(children='Simple RNN Layers'),
                        html.Img(src=GRAPH_LOCATIONS + 'TrainingHistory_Simple_cpi.jpg'),
                        html.H3(children='LSTM Layers'),
                        html.Img(src=GRAPH_LOCATIONS + 'TrainingHistory_LSTM_cpi.jpg'),
                        html.H3(children='GRU Layers'),
                        html.Img(src=GRAPH_LOCATIONS + 'TrainingHistory_GRU_cpi.jpg')
                    ]),
                    html.Div([
                        html.H3(children='Simple RNN Layers'),
                        html.Img(src=GRAPH_LOCATIONS + 'TrainingHistory_Simple_wage.jpg'),
                        html.H3(children='LSTM Layers'),
                        html.Img(src=GRAPH_LOCATIONS + 'TrainingHistory_LSTM_wage.jpg'),
                        html.H3(children='GRU Layers'),
                        html.Img(src=GRAPH_LOCATIONS + 'TrainingHistory_GRU_wage.jpg')
                    ])
                ], style={
                'display': 'flex',
                'flexDirection': 'row',
                'justifyContent': 'center'
            })
        ]),
        html.Div([
            html.H3(children='References'),
            html.Div([
                html.H4(children='The world Bank dataset on income per capita by country.'),
                html.A(href='https://data.worldbank.org/indicator/NY.ADJ.NNTY.PC.CD', 
                       children='https://data.worldbank.org/indicator/NY.ADJ.NNTY.PC.CD'),
                html.P(children='Used for training of the Wages Models.')
            ]),
            html.Div([
                html.H4(children='The world Bank dataset on Headline Consumer Prices Index.'),
                html.A(href='https://data.worldbank.org/indicator/NY.ADJ.NNTY.PC.CD',
                       children='https://data.worldbank.org/indicator/NY.ADJ.NNTY.PC.CD'),
                html.P(children='Ha, Jongrim, M. Ayhan Kose, and Franziska Ohnsorge (2023). "One-Stop Source: A Global Database of Inflation." Journal of International Money and Finance 137 (October): 102896.'),
                html.P(children='Used for training of the CPI Models.')
            ]),
            html.Div([
                html.H4(children='The UK governments dataset on average Wages by Area.'),
                html.A(href='https://commonslibrary.parliament.uk/research-briefings/cbp-8456/',
                       children='https://commonslibrary.parliament.uk/research-briefings/cbp-8456/'),
                html.P(children='Used for predicting UK average wages to 2028.')
            ]),
            html.Div([
                html.H4(children='GEOJSON of UK counties by Martin Chorley.'),
                html.A(href='https://github.com/martinjc/UK-GeoJSON',
                       children='https://github.com/martinjc/UK-GeoJSON'),
                html.P(children='Used for mapping predictions onto UK areas.')
            ]),
            html.Div([
                html.H4(children='Zoopla''s average rental cost by area'),
                html.A(href='https://www.zoopla.co.uk/discover/property-news/average-rent-uk/',
                       children='https://www.zoopla.co.uk/discover/property-news/average-rent-uk/'),
                html.P(children='Used for calculating cost of living.')
            ]),
            html.Div([
                html.H4(children='Homelets statistics on rental prices'),
                html.A(href='https://homelet.co.uk/homelet-rental-index',
                       children='https://homelet.co.uk/homelet-rental-index'),
                html.P(children='Used for corroborating data from zoopla.')
            ]),
            html.Div([
                html.H4(children='Homelets statistics on rental prices'),
                html.A(href='https://homelet.co.uk/homelet-rental-index',
                       children='https://homelet.co.uk/homelet-rental-index'),
                html.P(children='Used for corroborating data from zoopla.')
            ]),
            html.Div([
                html.H4(children='Numbeo''s statistics on cost of living by City'),
                html.A(href='https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+Kingdom',
                       children='https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+Kingdom'),
                html.P(children='Used for retrieving and averaging cost of living (without rent) by area.')
            ]),
            html.Div([
                html.H4(children='Money.co.uk''s statistics on cost of living by Area'),
                html.A(href='https://www.money.co.uk/cost-of-living/cost-of-living-statistics',
                       children='https://www.numbeo.com/cost-of-living/country_result.jsp?country=United+Kingdom'),
                html.P(children='Used for corroborating data from Numbeo.')
            ])
        ])
        ],style={
            'display': 'flex',
            'flexDirection': 'column',
            'textAlign': 'center'})
    ], style={
        'display': 'flex',
        'justifyContent':'center',
        'alignContent':'center'})
])

@callback(
    Output("county-info", "children"), 
    Input("geojson", "hoverData"))
def displayCountyData(geoJson=None):
    return GetCountyInfoPanel(geoJson)

@callback(
    Output('dash-leaflet-container', 'children'),
    Output('col-line', 'figure'),
    Output('wages-line', 'figure'),
    Output('datatable', 'children'),
    Input('date-slider', 'value'),
    Input('wages-model-radio', 'value'),
    Input('col-model-radio', 'value'),
    Input('predictions-toggle','value'))
def UpdateComponents(dateSlider, wagesRadio, colRadio, predictionsToggle):
    wageResults = SwitchDataset(ASSETS_WAGE_LOCATION + wagesRadio)
    colResults = SwitchDataset(ASSETS_COL_LOCATION + colRadio)
    expectedWages = CalculateExpectedWages(wageResults, colResults)
    global year
    year = dateSlider
    wagesLineGraph = GraphObjects.Figure()

    datatableStart = 0
    columns=['Area'] + [i for i in range(2003,2029,1)]
    if predictionsToggle:
        datatableStart = len(expectedWages[0][1][:-5])
        columns=['Area'] + [i for i in range(2024,2029,1)]
    
    print(datatableStart)
    data = []
    for i in expectedWages:
        dataRow = [i[0]]
        for j in i[1][datatableStart:]:
            dataRow.append(j)
        data.append(dataRow)

    dataFrame = pandas.DataFrame(data, columns=columns)

    tableFig = dash_table.DataTable(data=dataFrame.to_dict('records'), columns=[{"name": str(i), "id":str(i)} for i in dataFrame.columns])

    for wageResult in wageResults:
        wagesLineGraph.add_trace(
            GraphObjects.Scatter(
                x=numpy.array(range(2003,2028,1)),
                y=wageResult[1],
                name=wageResult[0],
                line_shape='spline'
            ))

    colLineGraph = GraphObjects.Figure()
    for wageResult in wageResults:
        for colResult in colResults:
            if(wageResult[0] == colResult[0]):
                colLineGraph.add_trace(
                    GraphObjects.Scatter(
                        x=numpy.array(range(2003,2028,1)),
                        y=colResult[1],
                        name=colResult[0],
                        line_shape='spline'
                    ))

    wagesLineGraph.update_traces(hoverinfo='text+name', mode='lines+markers')
    wagesLineGraph.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

    colLineGraph.update_traces(hoverinfo='text+name', mode='lines+markers')
    colLineGraph.update_layout(legend=dict(y=0.5, traceorder='reversed', font_size=16))

    profitMap = DashLeaflet.Map([
                    DashLeaflet.TileLayer(),
                    DashLeaflet.GeoJSON(url=GEOJSON_LOCATION, 
                                        zoomToBounds=True,
                                        id="geojson",
                                        hoverStyle=dict(weight=4, color='#666', dashArray=''),
                                        hideout=dict(classes=CLASSES, colorScale=COLOUR_SCALE, expectedWages=expectedWages, style=STYLE, year=GetYearIndex(dateSlider)), 
                                        style=STYLE_HANDLE)
                    ], style={'height': '50vh'}, center=[40, 10], zoom=6)

    return profitMap, wagesLineGraph, colLineGraph, tableFig

if __name__ == '__main__':
    app.run(debug=True)