import dash
from dash import html
from dash import dash, html, dcc
from drugs import get_emptyrow


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

def get_county_header():

    header = html.Div([
        html.Div([
            html.H3('Drug Overdose Data By County', style={'text-align': 'center'})
        ],
            className='row'
        ),
    ])

    return header

def get_nav_bar():
    navbar = html.Div([
        html.Div([
            html.Div([], className = 'two columns'),
            html.Div([
                dcc.Link(
                    html.H6(children='drug'),
                    href='/drugs'
                )
            ],
                className='two columns'
            ),
        ],
            className='row',
                style={'background-color' : 'dark-green',
                        'box-shadow': '2px 5px 5px 1px rgba(0, 100, 0, .5)'}
        ),
    ])

    return navbar


def county_App():
    return html.Div([
        get_county_header(),
        get_nav_bar(),
        get_emptyrow(),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    ['Adams', 'Arapahoe', 'Douglas'],
                    id='county',
                    multi=True
                ),
            ],
                className='four columns'
            ),
            html.Div([
                dcc.Dropdown(
                    [2018,2019,2020,2021],
                    id='years',
                    multi=True
                ),
            ],
                className='four columns'
            ),
        ],
            className='row'
        ),
        html.Div(id='all-drug-stats'),
        # dcc.Store(id='all-data', storage_type='memory'),
    ])

app.layout = county_App