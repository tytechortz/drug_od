from dash import dash, html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from flask import Flask
from flaskwebgui import FlaskUI

df17 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths17.sas7bdat", encoding='iso-8859-1')
df17['year'] = 2017
df18 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths18.sas7bdat", encoding='iso-8859-1')
df18['year'] = 2018
df19 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths19.sas7bdat", encoding='iso-8859-1')
df19['year'] = 2019
df20 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths20.sas7bdat", encoding='iso-8859-1')
df20['year'] = 2020
df21 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths21.sas7bdat", encoding='iso-8859-1')
df21['year'] = 2021

df_pop = pd.read_csv("/Users/jamesswank/Downloads/sya-county_2020.csv")
# print(df_pop)

df = pd.concat([df17,df18,df19,df20,df21], axis=0)

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
                html.H4('Drug OD Data', style={'text-align': 'center'})
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    html.H6('Select Drug', style={'text-align': 'center'})
                ],
                    className='four columns'
                ),
                html.Div([
                    html.H6('Select County', style={'text-align': 'center'})
                ],
                    className='four columns'
                ),
                html.Div([
                    html.H6('Select Years', style={'text-align': 'center'})
                ],
                    className='four columns'
                ),    
            ],
                className='row'
            ),
            html.Div([
            ],
                className='row'
            ),
            html.Div([
                html.Div([
                    dcc.RadioItems(
                        ['All Drugs','Opiod','Meth','Fentanyl','Heroin'],
                        id='drug',
                        value='All Drugs',
                        inline=True
                    ),
                ],
                    className='four columns'
                ),
                html.Div([
                    dcc.Dropdown(
                        ['Adams','Arapahoe','Douglas'],
                        id='counties',
                        value='Adams',
                        placeholder='Select County',
                        multi=False
                    ),
                ],
                    className='four columns'
                ),
                html.Div([
                    dcc.RangeSlider(
                        2017,2021,1, value=[2017,2021],
                        id='years',
                        marks={2017:'2017',2018:'2018',2019:'2019',2020:'2020',2021:'2021'},
                    ),
                ],
                    className='four columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                
                html.Div([
                    dcc.Graph(id='rate-histogram')
                ],
                    className='six columns'
                ),
                html.Div([
                    dcc.Graph(id='drug-histogram')
                ],
                    className='six columns'
                ),
            ],
                className='row'
            ),
            html.Div([
                    html.Div([
                        html.H5('County Data')
                    ],
                        className='row'
                    ),
                    html.Div(id='stats'),
                ],
                    className='six columns'
                ),
            # html.Div([
            #     html.Div(id='opiod-stats'),
            # ],
            #     className='row'
            # ),
            dcc.Store(id='all-data', storage_type='memory'),
            dcc.Store(id='pop-data', storage_type='memory'),
            dcc.Store(id='all-drug-data', storage_type='memory'),
            dcc.Store(id='opiod-data', storage_type='memory'),
            dcc.Store(id='meth-data', storage_type='memory'),
            dcc.Store(id='fent-data', storage_type='memory'),
            dcc.Store(id='heroin-data', storage_type='memory'),
            # dcc.Store(id='opiod-stats', storage_type='memory'),
        ]
    
    )



app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server
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
    # print(selected_df)
    
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
    Output('pop-data', 'data'),
    Input('years', 'value'))
def all_drugs(years):
    counties = ['Adams','Arapahoe','Douglas']
  
    df_pop1 = df_pop.loc[((df_pop['year'].between(2017,2021) & (df_pop['county'].isin(counties))))]
    # print(df_pop1)
    df_pop1.drop(['id','countyfips','age','malepopulation','femalepopulation','datatype'],axis=1,inplace=True)
    # print(df_pop1)
    pop_year_tot = df_pop1.groupby(['year','county']).sum()
    pop_year_tot.reset_index(inplace=True)

    # print(pop_year_tot)

    # df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    # adams_tot = len(df_adams_ad)
    # df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    # arapahoe_tot = len(df_arapahoe_ad)

    return pop_year_tot.to_json()

@app.callback(
    Output('opiod-data', 'data'),
    Input('all-drug-data', 'data'),
    Input('years', 'value'),
    Input('counties', 'value'))
def opiod_data(data, years, counties):
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
    Output('meth-data', 'data'),
    Input('all-drug-data', 'data'),
    Input('years', 'value'),
    Input('counties', 'value'))
def meth_data(data, years, counties):
    df_ad_meth = pd.read_json(data)

    meth_codes = ['T436']
    df_meth = df_ad_meth.loc[df_ad_meth.iloc[:, 1:13].isin(meth_codes).any(axis=1)]

    print(counties)

    # df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    # adams_tot = len(df_adams_ad)
    # df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    # arapahoe_tot = len(df_arapahoe_ad)

    return df_meth.to_json()

@app.callback(
    Output('fent-data', 'data'),
    Input('all-drug-data', 'data'),
    Input('years', 'value'),
    Input('counties', 'value'))
def meth_data(data, years, counties):
    df_ad_fent = pd.read_json(data)

    fent_codes = ['T404']
    df_fent = df_ad_fent.loc[df_ad_fent.iloc[:, 1:13].isin(fent_codes).any(axis=1)]

    print(years)

    # df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    # adams_tot = len(df_adams_ad)
    # df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    # arapahoe_tot = len(df_arapahoe_ad)

    return df_fent.to_json()

@app.callback(
    Output('heroin-data', 'data'),
    Input('all-drug-data', 'data'),
    Input('years', 'value'),
    Input('counties', 'value'))
def heroin_data(data, years, counties):
    df_ad_he = pd.read_json(data)

    heroin_codes = ['T401']
    df_heroin = df_ad_he.loc[df_ad_he.iloc[:, 1:13].isin(heroin_codes).any(axis=1)]

    print(counties)

    # df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    # adams_tot = len(df_adams_ad)
    # df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    # arapahoe_tot = len(df_arapahoe_ad)

    return df_heroin.to_json()


@app.callback(
    Output('stats', 'children'),
    Input('all-drug-data', 'data'),
    Input('opiod-data', 'data'),
    Input('meth-data', 'data'),
    Input('fent-data', 'data'),
    Input('heroin-data', 'data'),
    Input('years', 'value'),
    Input('drug', 'value'),
    Input('counties', 'value'))
def get_opiods(all_drugs_data,opiod_data,meth_data,fent_data,heroin_data,years,drug,counties):

    if drug == 'Opiod':
        df = pd.read_json(opiod_data)
    elif drug == 'Meth':
        df = pd.read_json(meth_data)
    elif drug == 'Fentanyl':
        df = pd.read_json(fent_data)
    elif drug == 'Heroin':
        df = pd.read_json(heroin_data)
    else:
        df = pd.read_json(all_drugs_data)

    df = df.loc[(df['county']==counties)]
    od_total = len(df)



    return html.Div([
            html.Div([
                html.H5('{} County, {} to {}'.format(counties,years[0], years[1]))
            ],
                className='row'
            ),
            html.H6('{} OD Total = {}'.format(drug,od_total))
        ])



@app.callback(
    Output('drug-histogram', 'figure'),
    Input('all-drug-data', 'data'),
    Input('opiod-data', 'data'),
    Input('meth-data', 'data'),
    Input('fent-data', 'data'),
    Input('heroin-data', 'data'),
    Input('counties', 'value'),
    Input('drug', 'value'),
    Input('years', 'value'))
def drug_graph(ad_data,opiod_data,meth_data,fent_data,heroin_data,county,drug,years):
    opg = pd.read_json(opiod_data)

    if drug == 'All Drugs':
        df = pd.read_json(ad_data)
        # print(df)
        df = df.loc[df['county']==county]
    elif drug == 'Opiod':
        df = pd.read_json(opiod_data)
        df = df.loc[df['county']==county]
    elif drug == 'Meth':
        df = pd.read_json(meth_data)
        df = df.loc[df['county']==county] 
    elif drug == 'Fentanyl':
        df = pd.read_json(fent_data)
        df = df.loc[df['county']==county]
    elif drug == 'Heroin':
        df = pd.read_json(heroin_data)
        df = df.loc[df['county']==county]


    deaths = df.groupby(['year']).size()
    # print(deaths.index)
    deaths = deaths.to_frame()
    deaths['text_year'] = deaths.index.map(str)
 
    year_list = list(range(years[0],(years[-1]+1)))
    print(year_list)
    
    drug_traces = []

    drug_traces.append(go.Bar(
        y = deaths[0],
        x = deaths['text_year'],
        text=deaths[0],
        name='Water Level',
    )),

    xaxis_values = year_list

    drug_layout = go.Layout(
        height =500,
        title = '{} County Annual OD Totals for {}'.format(county, drug),
        yaxis = {'title':'OD Total'},
        xaxis = {'title':'Year','tickmode':'array', 'tickvals':xaxis_values},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': drug_traces, 'layout': drug_layout}

@app.callback(
    Output('rate-histogram', 'figure'),
    Input('all-drug-data', 'data'),
    Input('pop-data', 'data'),
    Input('opiod-data', 'data'),
    Input('meth-data', 'data'),
    Input('fent-data', 'data'),
    Input('heroin-data', 'data'),
    Input('counties', 'value'),
    Input('drug', 'value'),
    Input('years', 'value'))
def rate_graph(ad_data,pop_data,opiod_data,meth_data,fent_data,heroin_data,county,drug,years):
    pop = pd.read_json(pop_data)
    # pop = pop.unstack()
    print(pop)

    if drug == 'All Drugs':
        df = pd.read_json(ad_data)
        # print(df)
        df = df.loc[df['county']==county]
        df_pop = pop.loc[pop['county']==county]
        

    elif drug == 'Opiod':
        df = pd.read_json(opiod_data)
        df = df.loc[df['county']==county]
    elif drug == 'Meth':
        df = pd.read_json(meth_data)
        df = df.loc[df['county']==county] 
    elif drug == 'Fentanyl':
        df = pd.read_json(fent_data)
        df = df.loc[df['county']==county]
    elif drug == 'Heroin':
        df = pd.read_json(heroin_data)
        df = df.loc[df['county']==county]


    deaths = df.groupby(['year']).size()
    # print(deaths.index)
    deaths = deaths.to_frame()
    deaths['text_year'] = deaths.index.map(str)

    
 
    year_list = list(range(years[0],(years[-1]+1)))
    print(year_list)
    
    drug_traces = []

    drug_traces.append(go.Bar(
        y = deaths[0],
        x = deaths['text_year'],
        text=deaths[0],
        name='Water Level',
    )),

    xaxis_values = year_list

    drug_layout = go.Layout(
        height =500,
        title = '{} County Annual OD Totals for {}'.format(county, drug),
        yaxis = {'title':'OD Total'},
        xaxis = {'title':'Year','tickmode':'array', 'tickvals':xaxis_values},
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )

    return {'data': drug_traces, 'layout': drug_layout}
    
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
    app.run_server(port=8000, debug=True)
# if __name__ == "__main__":
#     FlaskUI(server, close_server_on_exit=False).run()