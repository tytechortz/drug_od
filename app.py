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
                html.Div([
                    html.H6('Select Drug')
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
                    className='four columns'
                ),
                html.Div([
                    dcc.RadioItems(
                        ['All Drugs','Opiods','Meth'],
                        id='drugs',
                        inline=True
                    ),
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        ['Adams','Arapahoe','Douglas'],
                        id='counties',
                        placeholder='Select County',
                        multi=True
                    ),
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                html.Div(id='stats'),
            ],
                className='row'
            ),
            # html.Div([
            #     html.Div(id='opiod-stats'),
            # ],
            #     className='row'
            # ),
            dcc.Store(id='all-data', storage_type='memory'),
            dcc.Store(id='all-drug-data', storage_type='memory'),
            dcc.Store(id='opiod-data', storage_type='memory'),
            # dcc.Store(id='opiod-stats', storage_type='memory'),
        ]
    
    )

app = dash.Dash(__name__)
app.layout = get_layout
# app.config.supress_callback_exceptions = True

@app.callback(
    Output('all-data', 'data'),
    Input('years', 'value'))
def get_stats(years):
    print(years)
    # print(df)
    start_year = years[0]
    end_year = years[1]
    print(start_year)
    print(end_year)

    
    
    # selected_df = df[df['year']>=start_year & df['year']<=end_year]
    selected_df = df[df['year'].between(start_year, end_year)]
    print(selected_df)
    
    df1 = selected_df[[ 'age', 'ucod', 'acme1', 'acme2', 'acme3', 'acme4', 'acme5', 'acme6', 'acme7', 'acme8', 'acme9', 'acme10', 'acme11', 'year', 'coor', 'ucid', 'u','age_yr','AgeId','county']]
    # print(df1)
    return df1.to_json()

@app.callback(
    Output('all-drug-data', 'data'),
    Input('all-data', 'data'),
    Input('years', 'value'),
    Input('counties', 'value'))
def all_drugs(all_data, years, counties):
    df_ad = pd.read_json(all_data)
    df_ad = df_ad.loc[((df_ad['ucid']=='X') & ((df_ad['u'].between(40,44)) | (df_ad['u'].between(60,64)) | (df_ad['u']==85))) | ((df_ad['ucid']=='Y') & df_ad['u'].between(10,14))]

    # print(counties)

    # df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    # adams_tot = len(df_adams_ad)
    # df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    # arapahoe_tot = len(df_arapahoe_ad)

    return df_ad.to_json()

@app.callback(
    Output('opiod-data', 'data'),
    Input('all-drug-data', 'data'),
    Input('years', 'value'),
    Input('counties', 'value'))
def all_drugs(data, years, counties):
    df_ad_op = pd.read_json(data)

    opiod_codes = ['T402', 'T403', 'T404']
    df_opiods = df_ad_op.loc[df_ad_op.iloc[:, 1:13].isin(opiod_codes).any(axis=1)]

    print(counties)

    # df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    # adams_tot = len(df_adams_ad)
    # df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    # arapahoe_tot = len(df_arapahoe_ad)

    return df_opiods.to_json()


@app.callback(
    Output('stats', 'children'),
    Input('opiod-data', 'data'),
    Input('years', 'value'),
    Input('drugs', 'value'),
    Input('counties', 'value'))
def get_opiods(opiod_data,years,drug,counties):
    df_opiods = pd.read_json(opiod_data)
    print(drug)
    # print(df_opiods)
    df = df_opiods.loc[(df_opiods['county']==counties[0])]
    # print(df)
    opiod_od = len(df)


    if drug == 'Opiods':
        return html.Div([
            html.Div([
                html.H6('Data for {} County, {} to {}'.format(counties[0],years[0], years[1]))
            ],
                className='row'
            ),
            html.H6('Opiod OD Total = {}'.format(opiod_od))
        ])

    
    # return html.Div([
    #     html.Div([
    #         html.H4('All Drug OD Total For {}'.format(years))
    #     ],
    #         className='row'
    #     ),
    #     html.Div([
    #         html.H6('Adams = {}'.format(adams_tot))
    #     ],
    #         className='row'
    #     ),
    #     html.Div([
    #         html.H6('Arapahoe = {}'.format(arapahoe_tot))
    #     ],
    #         className='row'
    #     ),
    # ])
# @app.callback(
#     Output('stats', 'children'),
#     Input('drugs','value'),
#     Input('opiod-stats', 'children'))
# def get_stats(opiod_stats, drug):
#     print(drug)
#     if drug == 'Opiods':
#         return opiod_stats
    





if __name__ == "__main__":
    app.run_server(port=8080, debug=True)