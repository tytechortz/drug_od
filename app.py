from dash import dash, html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

from homepage import Homepage
from drugs import drug_App
from county import county_App







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
# ad = df.loc[((df['ucid']=='X') & ((df['u'].between(40,44)) | (df['u'].between(60,64)) | (df['u']==85))) | ((df['ucid']=='Y') & df['u'].between(10,14))]



# print(df)


# def get_layout():
#     return html.Div(
#         [
#             html.Div([
#                 html.H4('Drug OD Data')
#             ],
#                 className='row'
#             ),
#             html.Div([
#                 html.Div([
#                     dcc.Dropdown(
#                         [2018,2019,2020,2021],
#                         id='years',
#                         multi=True
#                     ),
#                 ],
#                     className='four columns'
#                 ),
#             ],
#                 className='row'
#             ),
#             html.Div([
#                 html.Div(id='all-drug-stats'),
#             ],
#                 className='row'
#             ),
#             html.Div([
#                 html.Div(id='opiod-stats'),
#             ],
#                 className='row'
#             ),
#             dcc.Store(id='all-data', storage_type='memory'),
#         ]
    
#     )

app = dash.Dash(name=__name__, 
                title="Drug Overdose Data Dashboard",
                assets_folder="static",
                assets_url_path="static")

application = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh = False),
    html.Div(id = 'page-content'),
    dcc.Store(id='all-data', storage_type='memory'),
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/drugs':
        return drug_App()
    elif pathname == '/counties':
        return county_App()
    else:
        return Homepage()

# app = dash.Dash(__name__)
# app.layout = get_layout
# app.config.supress_callback_exceptions = True


@app.callback(
    Output('all-data', 'data'),
    Input('years', 'value'))
def get_stats(years):
    print(years)
    # print(df)
    

    selected_df = df[df['year'].isin(years)]
    # print(selected_df)
    
    df1 = selected_df[[ 'age', 'ucod', 'acme1', 'acme2', 'acme3', 'acme4', 'acme5', 'acme6', 'acme7', 'acme8', 'acme9', 'acme10', 'acme11', 'year', 'coor', 'ucid', 'u','age_yr','AgeId','county']]

    # print(df1)



    return df1.to_json()


@app.callback(
    Output('county-all-drug-stats', 'children'),
    Input('all-data', 'data'),
    Input('years', 'value'),
    Input('county', 'value'))
def all_drugs(all_drug_data, years, county):
    df_ad = pd.read_json(all_drug_data)
    df_ad = df_ad.loc[((df_ad['ucid']=='X') & ((df_ad['u'].between(40,44)) | (df_ad['u'].between(60,64)) | (df_ad['u']==85))) | ((df_ad['ucid']=='Y') & df_ad['u'].between(10,14))]


    df_ad = df_ad.loc[(df_ad['county'] == county)]

    total = len(df_ad)

    # df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    # adams_tot = len(df_adams_ad)
    # df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    # arapahoe_tot = len(df_arapahoe_ad)
    # df_douglas_ad = df_ad.loc[(df_ad['county'] == 'Douglas')]
    # douglas_tot = len(df_douglas_ad)
    # tc_tot = adams_tot + arapahoe_tot + douglas_tot
    # print(tc_tot)



    # print(df_ad)
    return html.Div([
        html.Div([
            html.H4('All Drug OD Total For {}'.format(years))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Adams = {}'.format(total))
        ],
            className='row'
        ),
        # html.Div([
        #     html.H6('Arapahoe = {}'.format(arapahoe_tot))
        # ],
        #     className='row'
        # ),
        # html.Div([
        #     html.H6('Douglas = {}'.format(douglas_tot))
        # ],
        #     className='row'
        # ),
        # html.Div([
        #     html.H6('Tri-County = {}'.format(tc_tot))
        # ],
        #     className='row'
        # ),
    ])

@app.callback(
    Output('all-drug-stats', 'children'),
    Input('all-data', 'data'),
    Input('years', 'value'))
def all_drugs(all_drug_data, years):
    df_ad = pd.read_json(all_drug_data)
    df_ad = df_ad.loc[((df_ad['ucid']=='X') & ((df_ad['u'].between(40,44)) | (df_ad['u'].between(60,64)) | (df_ad['u']==85))) | ((df_ad['ucid']=='Y') & df_ad['u'].between(10,14))]

    df_adams_ad = df_ad.loc[(df_ad['county'] == 'Adams')]
    adams_tot = len(df_adams_ad)
    df_arapahoe_ad = df_ad.loc[(df_ad['county'] == 'Arapahoe')]
    arapahoe_tot = len(df_arapahoe_ad)
    df_douglas_ad = df_ad.loc[(df_ad['county'] == 'Douglas')]
    douglas_tot = len(df_douglas_ad)
    tc_tot = adams_tot + arapahoe_tot + douglas_tot
    # print(tc_tot)



    # print(df_ad)
    return html.Div([
        html.Div([
            html.H4('All Drug OD Total For {}'.format(years))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Adams = {}'.format(adams_tot))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Arapahoe = {}'.format(arapahoe_tot))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Douglas = {}'.format(douglas_tot))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Tri-County = {}'.format(tc_tot))
        ],
            className='row'
        ),
    ])


@app.callback(
    Output('opiod-stats', 'children'),
    Input('all-data', 'data'),
    Input('years', 'value'))
def all_drugs(all_drug_data, years):
    df_ad_op = pd.read_json(all_drug_data)
    df_ad_op = df_ad_op.loc[((df_ad_op['ucid']=='X') & ((df_ad_op['u'].between(40,44)) | (df_ad_op['u'].between(60,64)) | (df_ad_op['u']==85))) | ((df_ad_op['ucid']=='Y') & df_ad_op['u'].between(10,14))]
    print(df_ad_op)

    opiod_codes = ['T402', 'T403', 'T404']
    df_opiod = df_ad_op.loc[df_ad_op.iloc[:, 1:13].isin(opiod_codes).any(axis=1)]
    print(df_opiod)
    df_adams_opiod = df_opiod.loc[(df_opiod['county'] == 'Adams')]
    adams_tot = len(df_adams_opiod)
    df_arapahoe_opiod = df_opiod.loc[(df_opiod['county'] == 'Arapahoe')]
    arapahoe_tot = len(df_arapahoe_opiod)
    df_douglas_opiod = df_opiod.loc[(df_opiod['county'] == 'Douglas')]
    douglas_tot = len(df_douglas_opiod)
    tc_opiod_tot = adams_tot + arapahoe_tot + douglas_tot
    # print(tc_tot)



    # print(df_ad)
    return html.Div([
        html.Div([
            html.H4('Opiod OD Total For {}'.format(years))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Adams = {}'.format(adams_tot))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Arapahoe = {}'.format(arapahoe_tot))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Douglas = {}'.format(douglas_tot))
        ],
            className='row'
        ),
        html.Div([
            html.H6('Tri-County = {}'.format(tc_opiod_tot))
        ],
            className='row'
        ),
    ])






if __name__ == "__main__":
    app.run_server(port=8080, debug=True)