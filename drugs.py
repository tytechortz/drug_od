import dash
from dash import html
from dash import dash, html, dcc


app = dash.Dash(__name__)
app.config['suppress_callback_exceptions']=True

def get_drug_header():

    header = html.Div([
        html.Div([
            html.H3('Drug Overdose Data By Drug Types', style={'text-align': 'center'})
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
                    html.H6(children='county'),
                    href='/counties'
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

def drug_App():
    return html.Div([
        get_drug_header(),
        get_nav_bar(),
        html.Div([
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

app.layout = drug_App