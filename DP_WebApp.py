import dash
from dash import Dash, html
 
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div(children='Piss off')
])

if __name__ == '__main__':
    app.run(debug=True)