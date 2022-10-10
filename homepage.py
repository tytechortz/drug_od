import dash
# import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

body = html.Div([
    html.Div([
        html.H2('Drug Overdose Data by Drug Type'),
        dbc.Button('Open App', href="/drug-data"),
    ],
        className='row'
    ),
])

def Homepage():
    layout = html.Div([
    body
    ])
    return layout