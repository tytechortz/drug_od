from dash import dash, html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

df18 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths18.sas7bdat", encoding='iso-8859-1')
df18['year'] = 2018
df19 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths19.sas7bdat", encoding='iso-8859-1')
df19['year'] = 2019
df20 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths20.sas7bdat", encoding='iso-8859-1')
df20['year'] = 2020
df21 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths21.sas7bdat", encoding='iso-8859-1')
df21['year'] = 2021

df = pd.concat([df18,df19,df20,df21], axis=0)

conditions = [df['AgeId'] == 1, df['AgeId'] != 1]
choices = [df['age'], 0]
df['age_yr'] = np.select(conditions, choices)

county_conditions = [df['coor'] == 1, df['coor'] == 3, df['coor'] == 18]
county_choices = ['Adams', 'Arapahoe', 'Douglas']
df['county'] = np.select(county_conditions, county_choices)

age_groups = [-np.inf, 1,4,9,14,19,24,29,34,39,44,49,54,59,64,69,74,79,84,np.inf]
df['agegroup'] = pd.cut(df['age_yr'], bins=age_groups, labels=['0','1-4','5-9','10-14','15-19','20-24','25-29','30-34','35-39','40-44','45-49','50-54','55-59','60-64','65-69','70-74','75-79','80-84','85+'])
df['ucid'] = df['ucod'].str[:1]
df['u'] = df['ucod'].str[1:3].fillna(0).astype(int)
df.reset_index(inplace=True)


def get_layout():
    return html.Div(
        [
            html.Div([
                html.H4('Drug OD Data')
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.H6('Select Years')
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.RangeSlider(
                        2017,2021,1, value=[2017,2021],
                        id='years',
                        marks={2017:'2017',2018:'2018',2019:'2019',2020:'2020',2021:'2021'},
                    ),
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div(id='all-drug-stats'),
            ],
                className='row'
            ),
            html.Div([
                html.Div(id='opiod-stats'),
            ],
                className='row'
            ),
            dcc.Store(id='all-data', storage_type='memory'),
        ]
    
    )

app = dash.Dash(__name__)
app.layout = get_layout
# app.config.supress_callback_exceptions = True


if __name__ == "__main__":
    app.run_server(port=8080, debug=True)