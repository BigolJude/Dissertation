from dash import Dash, dcc, html
import dash_bootstrap_components as DashBootstrap
import dash_leaflet as DashLeaflet
from dash_extensions.javascript import assign

app = Dash(name=__name__, external_stylesheets=[DashBootstrap.themes.SLATE])


app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(children='Development Project'),
            html.H2(children='Mapped Financial Risk by Area'),
            DashLeaflet.Map([
    DashLeaflet.TileLayer(),
    DashLeaflet.GeoJSON(url="datasets/RegionsUK.geojson", zoomToBounds=True, id="geojson",
               hideout=dict(selected=[]), style=style_handle)
], style={'height': '50vh'}, center=[56, 10], zoom=6)
        ],style={
            'display': 'flex',
            'flex-direction': 'column',
            'text-align': 'center'})
    ], style={
        'display': 'flex',
        'justify-content':'center',
        'align-content':'centre'})
])

if __name__ == '__main__':
    app.run(debug=True)