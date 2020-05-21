# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import os
import base64

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import dash
import dash_table
from dash_table.Format import Format
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

###################################
# Private function and variable
###################################

def  get_data_num(case_type):    
    '''
    Generate case table, incremental number and percentage
    '''
    df_tmp = pd.read_csv('./lineplot_data/df_{}.csv'.format(case_type))
    df_tmp = df_tmp.astype({'Date': 'datetime64'})
    plusNum = df_tmp['plusNum'][0]
    plusPercent = df_tmp['plusPercentNum'][0]

    return df_tmp, plusNum, plusPercent

def make_country_table(countryName):
    '''This is the function for building df for Province/State of a given country'''
    countryTable = df_latest.loc[df_latest['Country/Region'] == countryName]

    if countryName == 'Australia':
        # Suppress SettingWithCopyWarning
        pd.options.mode.chained_assignment = None
        countryTable['Active'] = countryTable['Confirmed'] - countryTable['Recovered'] - countryTable['Deaths']
        countryTable['Death rate'] = countryTable['Deaths']/countryTable['Confirmed']
        countryTable['Confirmed/100k'] = ((countryTable['Confirmed']/countryTable['Population'])*100000).round()
        countryTable['Positive rate'] = countryTable['Confirmed']/countryTable['Tests']
        countryTable['Tests/100k'] = ((countryTable['Tests']/countryTable['Population'])*100000).round()

        countryTable = countryTable[['Province/State', 'Active', 'Confirmed', 'Recovered', 'Deaths', 'Death rate', 'Tests','Positive rate', 'Tests/100k', 'Confirmed/100k', 'lat', 'lon','Population']]
    else:
        # Suppress SettingWithCopyWarning
        pd.options.mode.chained_assignment = None
        countryTable['Active'] = countryTable['Confirmed'] - countryTable['Recovered'] - countryTable['Deaths']
        countryTable['Death rate'] = countryTable['Deaths']/countryTable['Confirmed']
        countryTable['Confirmed/100k'] = ((countryTable['Confirmed']/countryTable['Population'])*100000).round()

        countryTable = countryTable[['Province/State', 'Active', 'Confirmed', 'Recovered', 'Deaths', 'Death rate', 'Confirmed/100k', 'lat', 'lon']]
    countryTable = countryTable.sort_values(by=['Active', 'Confirmed'], ascending=False).reset_index(drop=True)
    # Set row ids pass to selected_row_ids
    countryTable['id'] = countryTable['Province/State']
    countryTable.set_index('id', inplace=True, drop=False)
    # Turn on SettingWithCopyWarning
    pd.options.mode.chained_assignment = 'warn'

    return countryTable

def make_Brazil_table(countrydata):

    # Suppress SettingWithCopyWarning
    pd.options.mode.chained_assignment = None
    countryTable = countrydata
    countryTable['Death rate'] = countryTable['Deaths']/countryTable['Confirmed']
    countryTable['Confirmed/100k'] = ((countryTable['Confirmed']/countryTable['Population'])*100000).round()

    countryTable = countryTable[['Province/State', 'Confirmed', 'Deaths', 'Death rate', 'Confirmed/100k', 'lat', 'lon','Population']]

    countryTable = countryTable.sort_values(by=['Confirmed'], ascending=False).reset_index(drop=True)
    # Set row ids pass to selected_row_ids
    countryTable['id'] = countryTable['Province/State']
    countryTable.set_index('id', inplace=True, drop=False)
    # Turn on SettingWithCopyWarning
    pd.options.mode.chained_assignment = 'warn'

    return countryTable

def make_continent_table(continent_list):
    '''This is the function for building df for Europe countries'''
    continent_table = WorldwildTable.loc[WorldwildTable['Country/Region'].isin(continent_list)]
    return continent_table

def make_dcc_Brazil_tab(countryName, dataframe):
    '''This is for generating tab component for country table'''
    return dcc.Tab(
        id='tab-datatable-interact-location-{}'.format(countryName),
        label=countryName,
        value=countryName,
        className='custom-tab',
        selected_className='custom-tab--selected',
        children=[
            dash_table.DataTable(
                id='datatable-interact-location-{}'.format(countryName),
                # Don't show coordinates
                columns=[{"name": 'Province/State', "id": 'Province/State'}
                            for i in dataframe.columns[0:1]] +
                        [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                            if i == 'Death rate' else {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                for i in dataframe.columns[1:5]],
                # But still store coordinates in the table for interactivity
                data=dataframe.to_dict("rows"),
                #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                row_selectable="single",
                sort_action="native",
                style_as_list_view=True,
                style_cell={'font_family': 'Roboto',
                            'backgroundColor': '#ffffff', 
                },
                fixed_rows={'headers': True, 'data': 0},
                style_table={'minHeight': '400px',
                             'height': '400px',
                             'maxHeight': '400px',
                             'overflowX': 'auto',
                },
                style_header={'backgroundColor': '#ffffff',
                              'fontWeight': 'bold'},
                style_cell_conditional=[{'if': {'column_id': 'Province/State'}, 'width': '20%'},
                                        {'if': {'column_id': 'Confirmed'}, 'width': '20%'},
                                        {'if': {'column_id': 'Deaths'}, 'width': '20%'},
                                        {'if': {'column_id': 'Death rate'}, 'width': '20%'},
                                        {'if': {'column_id': 'Confirmed/100k'}, 'width': '20%'},
                                        {'if': {'column_id': 'Confirmed'}, 'color': '#f03f42'},
                                        {'if': {'column_id': 'Deaths'}, 'color': '#7f7f7f'},
                                        {'textAlign': 'center'}
                ],
            ),
        ]
    )

def make_dcc_country_tab(countryName, dataframe):
    '''This is for generating tab component for country table'''
    if countryName == 'Australia':
        return dcc.Tab(
                id='tab-datatable-interact-location-{}'.format(countryName),
                label=countryName,
                value=countryName,
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dash_table.DataTable(
                        id='datatable-interact-location-{}'.format(countryName),
                        # Don't show coordinates
                        columns=[{"name": 'Province/State', "id": 'Province/State'}
                                    if i == 'Province/State' else {"name": 'Country/Region', "id": 'Country/Region'}
                                        for i in dataframe.columns[0:1]] +
                                [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                                    if i == 'Death rate' or i == 'Positive rate' else {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                        for i in dataframe.columns[1:10]],
                        # But still store coordinates in the table for interactivity
                        data=dataframe.to_dict("rows"),
                        #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                        row_selectable="single",
                        sort_action="native",
                        style_as_list_view=True,
                        style_cell={'font_family': 'Roboto',
                                    'backgroundColor': '#ffffff', 
                        },
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={'minHeight': '400px',
                                     'height': '400px',
                                     'maxHeight': '400px',
                                     'overflowX': 'auto',
                        },
                        style_header={'backgroundColor': '#ffffff',
                                      'fontWeight': 'bold'},
                        style_cell_conditional=[{'if': {'column_id': 'Province/State'}, 'width': '22%'},
                                                {'if': {'column_id': 'Country/Regions'}, 'width': '22%'},
                                                {'if': {'column_id': 'Active'}, 'width': '8%'},
                                                {'if': {'column_id': 'Confirmed'}, 'width': '8%'},
                                                {'if': {'column_id': 'Recovered'}, 'width': '8%'},
                                                {'if': {'column_id': 'Deaths'}, 'width': '8%'},
                                                {'if': {'column_id': 'Death rate'}, 'width': '8%'},
                                                {'if': {'column_id': 'Tests'}, 'width': '8%'},
                                                {'if': {'column_id': 'Positive rate'}, 'width': '10%'},
                                                {'if': {'column_id': 'Tests/100k'}, 'width': '10%'},    
                                                {'if': {'column_id': 'Confirmed/100k'}, 'width': '10%'},
                                                {'if': {'column_id': 'Active'}, 'color':'#f0953f'},
                                                {'if': {'column_id': 'Confirmed'}, 'color': '#f03f42'},
                                                {'if': {'column_id': 'Recovered'}, 'color': '#2ecc77'},
                                                {'if': {'column_id': 'Deaths'}, 'color': '#7f7f7f'},
                                                {'textAlign': 'center'}
                        ],
                    ),
                ]
            )
    elif countryName in ['Asia', 'Oceania', 'North America', 'Europe', 'South America', 'Africa']:
        return dcc.Tab(
                id='tab-datatable-interact-location-{}'.format(countryName),
                label=countryName,
                value=countryName,
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dash_table.DataTable(
                        id='datatable-interact-location-{}'.format(countryName),
                        # Don't show coordinates
                        columns=[{"name": 'Province/State', "id": 'Province/State'}
                                    if i == 'Province/State' else {"name": 'Country/Region', "id": 'Country/Region'}
                                        for i in dataframe.columns[0:1]] +
                                [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                                    if i == 'Death rate' or i == 'Positive rate' else {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                        for i in dataframe.columns[1:11]],
                        # But still store coordinates in the table for interactivity
                        data=dataframe.to_dict("rows"),
                        #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                        row_selectable="single",
                        sort_action="native",
                        style_as_list_view=True,
                        style_cell={'font_family': 'Roboto',
                                    'backgroundColor': '#ffffff', 
                        },
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={'minHeight': '400px',
                                     'height': '400px',
                                     'maxHeight': '400px',
                                     'overflowX': 'auto',
                        },
                        style_header={'backgroundColor': '#ffffff',
                                      'fontWeight': 'bold'},
                        style_cell_conditional=[{'if': {'column_id': 'Country/Regions'}, 'width': '17%'},
                                                {'if': {'column_id': 'Active'}, 'width': '8%'},
                                                {'if': {'column_id': 'Confirmed'}, 'width': '8%'},
                                                {'if': {'column_id': 'Recovered'}, 'width': '8%'},
                                                {'if': {'column_id': 'Deaths'}, 'width': '8%'},
                                                {'if': {'column_id': 'Critical'}, 'width': '8%'},
                                                {'if': {'column_id': 'Death rate'}, 'width': '8%'},
                                                {'if': {'column_id': 'Tests'}, 'width': '8%'},
                                                {'if': {'column_id': 'Positive rate'}, 'width': '9%'},
                                                {'if': {'column_id': 'Tests/100k'}, 'width': '9%'},    
                                                {'if': {'column_id': 'Confirmed/100k'}, 'width': '9%'},
                                                {'if': {'column_id': 'Active'}, 'color':'#f0953f'},
                                                {'if': {'column_id': 'Confirmed'}, 'color': '#f03f42'},
                                                {'if': {'column_id': 'Recovered'}, 'color': '#2ecc77'},
                                                {'if': {'column_id': 'Deaths'}, 'color': '#7f7f7f'},
                                                {'textAlign': 'center'}
                        ],
                    ),
                ]
            )
    else:
        return dcc.Tab(
                id='tab-datatable-interact-location-{}'.format(countryName) if countryName != 'United States' else 'tab-datatable-interact-location-US',
                label=countryName,
                value=countryName,
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    dash_table.DataTable(
                        id='datatable-interact-location-{}'.format(countryName),
                        # Don't show coordinates
                        columns=[{"name": 'Province/State', "id": 'Province/State'}
                                    if i == 'Province/State' else {"name": 'Country/Region', "id": 'Country/Region'}
                                        for i in dataframe.columns[0:1]] +
                                [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                                    if i == 'Death rate' else {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                        for i in dataframe.columns[1:7]],
                        # But still store coordinates in the table for interactivity
                        data=dataframe.to_dict("rows"),
                        #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                        row_selectable="single",
                        sort_action="native",
                        style_as_list_view=True,
                        style_cell={'font_family': 'Roboto',
                                    'backgroundColor': '#ffffff', 
                        },
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={'minHeight': '400px',
                                     'height': '400px',
                                     'maxHeight': '400px',
                                     'overflowX': 'auto',
                        },
                        style_header={'backgroundColor': '#ffffff',
                                      'fontWeight': 'bold'},
                        style_cell_conditional=[{'if': {'column_id': 'Province/State'}, 'width': '26%'},
                                                {'if': {'column_id': 'Country/Region'}, 'width': '26%'},
                                                {'if': {'column_id': 'Active'}, 'width': '10%'},
                                                {'if': {'column_id': 'Confirmed'}, 'width': '12.3%'},
                                                {'if': {'column_id': 'Recovered'}, 'width': '12.3%'},
                                                {'if': {'column_id': 'Deaths'}, 'width': '10%'},
                                                {'if': {'column_id': 'Death rate'}, 'width': '12.3%'},
                                                {'if': {'column_id': 'Confirmed/100k'}, 'width': '17%'},
                                                {'if': {'column_id': 'Active'}, 'color':'#f0953f'},
                                                {'if': {'column_id': 'Confirmed'}, 'color': '#f03f42'},
                                                {'if': {'column_id': 'Recovered'}, 'color': '#2ecc77'},
                                                {'if': {'column_id': 'Deaths'}, 'color': '#7f7f7f'},
                                                {'textAlign': 'center'}
                        ],
                    ),
                ]
            )

def render_region_map(countyrdata, dff, latitude, longitude, zoom):

    '''
    This is the function to render map for Brazil and Germany
    '''

    hovertext_value = ['Confirmed: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(h, i, j, k) 
                            for h, i, j, k in zip(
                                countyrdata['Confirmed'],
                                countyrdata['Deaths'], 
                                countyrdata['Deaths']/countyrdata['Confirmed'], 
                                countyrdata['Confirmed']*100000/countyrdata['Population']
                            )
    ]

    mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

    # Generate a list for hover text display
    textList = []
    for area, region in zip(countyrdata['Province/State'], countyrdata['Country/Region']):

        if type(area) is str:
            textList.append(area+', '+region)
        else:
            textList.append(region)

    fig2 = go.Figure(go.Scattermapbox(
        lat=countyrdata['lat'],
        lon=countyrdata['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color='#f03f42',
            size=[i**(1/3) for i in countyrdata['Confirmed']],
            sizemin=1,
            sizemode='area',
            sizeref=2.*max([math.sqrt(i)
                for i in countyrdata['Confirmed']])/(100.**2),
        ),
        text=textList,
        hovertext=hovertext_value,
        hovertemplate="<b>%{text}</b><br><br>" +
                      "%{hovertext}<br>" +
                      "<extra></extra>")
    )
    fig2.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        margin=go.layout.Margin(l=10, r=10, b=10, t=0, pad=40),
        hovermode='closest',
        transition={'duration': 500},
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            style="light",
            # The direction you're facing, measured clockwise as an angle from true north on a compass
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=latitude,
                lon=longitude
            ),
            pitch=0,
            zoom=zoom
        )
    )

    return fig2

input_list = [
    Input('tabs-table', 'value'),
    Input('datatable-interact-location', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location', 'selected_row_ids'),
    Input('datatable-interact-location-Asia', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Asia', 'selected_row_ids'),
    Input('datatable-interact-location-Oceania', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Oceania', 'selected_row_ids'),
    Input('datatable-interact-location-North America', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-North America', 'selected_row_ids'),
    Input('datatable-interact-location-South America', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-South America', 'selected_row_ids'),
    Input('datatable-interact-location-Africa', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Africa', 'selected_row_ids'),
    Input('datatable-interact-location-Europe', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Europe', 'selected_row_ids'),
    Input('datatable-interact-location-Australia', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Australia', 'selected_row_ids'),
    Input('datatable-interact-location-Brazil', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Brazil', 'selected_row_ids'),
    Input('datatable-interact-location-Canada', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Canada', 'selected_row_ids'),
    Input('datatable-interact-location-Germany', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Germany', 'selected_row_ids'),
    Input('datatable-interact-location-Mainland China', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-Mainland China', 'selected_row_ids'),
    Input('datatable-interact-location-United States', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location-United States', 'selected_row_ids'),
]

################################################################################
# Data processing
################################################################################
# Method #1
# Import csv file and store each csv in to a df list
# NOTE all following steps really rely on the correct order of these csv files in folder raw_data
filename = os.listdir('./raw_data/')
sheet_name = [i.replace('.csv', '')
                        for i in filename if 'data' not in i and i.endswith('.csv')]
sheet_name.sort(reverse=True)

brazil_file_name = [i for i in os.listdir('./') if i.endswith('Brazil_data.csv')]
germany_file_name = [i for i in os.listdir('./') if i.endswith('Germany_data.csv')]

# Add coordinates for each area in the list for the latest table sheet
# To save time, coordinates calling was done seperately
# Import the data with coordinates
df_latest = pd.read_csv('{}_data.csv'.format(sheet_name[0]))
df_latest = df_latest.astype({'Date_last_updated_AEDT': 'datetime64'})

# Import Brazil data
df_brazil = pd.read_csv('{}'.format(brazil_file_name[0]))
df_brazil = df_brazil.astype({'Date_last_updated_AEDT': 'datetime64'})

# Import Germany data
df_germany = pd.read_csv('{}'.format(germany_file_name[0]))
df_germany = df_germany.astype({'Date_last_updated_AEDT': 'datetime64'})

# Save numbers into variables to use in the app
confirmedCases = df_latest['Confirmed'].sum()
deathsCases = df_latest['Deaths'].sum()
recoveredCases = df_latest['Recovered'].sum()
remainCases = df_latest['Confirmed'].sum() - (df_latest['Deaths'].sum() + df_latest['Recovered'].sum())

# Construct confirmed cases dataframe for line plot and 24-hour window case difference
df_confirmed, plusConfirmedNum, plusPercentNum1 = get_data_num('confirmed')

# Construct recovered cases dataframe for line plot and 24-hour window case difference
df_recovered, plusRecoveredNum, plusPercentNum2 = get_data_num('recovered')

# Construct death case dataframe for line plot and 24-hour window case difference
df_deaths, plusDeathNum, plusPercentNum3 = get_data_num('deaths')

# Construct remaining case dataframe for line plot and 24-hour window case difference
df_remaining, plusRemainNum, plusRemainNum3 = get_data_num('remaining')

# Create data table to show in app
# Generate sum values for Country/Region level
dfCase = df_latest.groupby(by='Country/Region', sort=False).sum().reset_index()
dfCase = dfCase.sort_values(
    by=['Confirmed'], ascending=False).reset_index(drop=True)
# As lat and lon also underwent sum(), which is not desired, remove from this table.
dfCase = dfCase.drop(columns=['lat', 'lon'])

# Grep lat and lon by the first instance to represent its Country/Region
dfGPS = df_latest.groupby(
    by='Country/Region', sort=False).first().reset_index()
dfGPS = dfGPS[['Country/Region', 'lat', 'lon']]

# Merge two dataframes
WorldwildTable = pd.merge(dfCase, dfGPS, how='inner', on='Country/Region')
WorldwildTable = WorldwildTable.replace({'Country/Region': 'China'}, 'Mainland China')
WorldwildTable['Active'] = WorldwildTable['Confirmed'] - WorldwildTable['Recovered'] - WorldwildTable['Deaths']
WorldwildTable['Death rate'] = WorldwildTable['Deaths']/WorldwildTable['Confirmed']
WorldwildTable['Confirmed/100k'] = ((WorldwildTable['Confirmed']/WorldwildTable['Population'])*100000).round()
WorldwildTable['Positive rate'] = WorldwildTable['Confirmed']/WorldwildTable['Tests']
WorldwildTable['Tests/100k'] = ((WorldwildTable['Tests']/WorldwildTable['Population'])*100000).round()
# Rearrange columns to correspond to the number plate order
WorldwildTable = WorldwildTable[['Country/Region', 'Active',
    'Confirmed', 'Recovered', 'Deaths', 'Critical', 'Death rate', 'Tests', 'Positive rate', 'Tests/100k', 'Confirmed/100k', 'lat', 'lon','Population']]
# Sort value based on Active cases and then Confirmed cases
WorldwildTable = WorldwildTable.sort_values(
    by=['Confirmed'], ascending=False).reset_index(drop=True)
# Set row ids pass to selected_row_ids
WorldwildTable['id'] = WorldwildTable['Country/Region']
WorldwildTable.set_index('id', inplace=True, drop=False)

# Replace 0s in 'Tests' column as ''
WorldwildTable = WorldwildTable.replace({'Tests': 0, 'Positive rate':0, 'Tests/100k':0}, '')

# Create tables for tabs
MainlandChinaTable = make_country_table('China')
AustraliaTable = make_country_table('Australia')
UnitedStatesTable = make_country_table('US')
CanadaTable = make_country_table('Canada')
BrazilTable = make_Brazil_table(df_brazil)
GermanyTable = make_Brazil_table(df_germany)

# Remove dummy row of test/critical number in UnitedStatesTable
UnitedStatesTable = UnitedStatesTable.dropna(subset=['Province/State'])

# Remove dummy row of test/critical number in UnitedStatesTable
CanadaTable = CanadaTable.dropna(subset=['Province/State'])

# Remove dummy row of test/critical number in AustraliaTable
AustraliaTable = AustraliaTable.dropna(subset=['Province/State'])

# Remove dummy row of test/critical number in MainlandChinaTable
MainlandChinaTable = MainlandChinaTable.dropna(subset=['Province/State'])

# Generate country lists for different continents
list_dict = {}
table_dict = {}
for i in df_latest.Continent.unique():
  if i =='Asia':
    list_dict['{}'.format(i)] = list(df_latest[df_latest['Continent'] == i]['Country/Region'].unique())
    list_dict['{}'.format(i)] = ['Mainland China' if x == 'China' else x for x in list_dict['{}'.format(i)]]
  else:
    list_dict['{}'.format(i)] = list(df_latest[df_latest['Continent'] == i]['Country/Region'].unique())

  table_dict['{}Table'.format(i.replace(' ', ''))] = make_continent_table(list_dict[i])

# Use full country names
WorldwildTable = WorldwildTable.replace({'Country/Region': 'US'}, 'United States')
WorldwildTable = WorldwildTable.replace({'Country/Region': 'UK'}, 'United Kingdom')
WorldwildTable = WorldwildTable.replace({'Country/Region': 'DRC'}, 'Dem. Rep. Congo')
WorldwildTable = WorldwildTable.replace({'Country/Region': 'CAR'}, 'Central African Rep.')
table_dict['AfricaTable'] = table_dict['AfricaTable'].replace({'Country/Region': 'CAR'}, 'Central African Rep.')
table_dict['AfricaTable'] = table_dict['AfricaTable'].replace({'Country/Region': 'DRC'}, 'Dem. Rep. Congo')
table_dict['EuropeTable'] = table_dict['EuropeTable'].replace({'Country/Region': 'UK'}, 'United Kingdom')
table_dict['NorthAmericaTable'] = table_dict['NorthAmericaTable'].replace({'Country/Region': 'US'}, 'United States')

# Save numbers into variables to use in the app
latestDate = datetime.strftime(df_confirmed['Date'][0], '%b %d, %Y %H:%M GMT+10')
secondLastDate = datetime.strftime(df_confirmed['Date'][1], '%b %d')
daysOutbreak = (df_confirmed['Date'][0] - datetime.strptime('12/31/2019', '%m/%d/%Y')).days

# # Read confirmed growth data from ./lineplot_data folder
dfs_curve = pd.read_csv('./lineplot_data/dfs_curve.csv')
# Read death growth data from ./lineplot_data folder
dfs_curve_death = pd.read_csv('./lineplot_data/dfs_curve_death.csv')

# Pseduo data for logplot
pseduoDay = np.arange(1, daysOutbreak+1)
y1 = 100*(1.85)**(pseduoDay-1)  # 85% growth rate
y2 = 100*(1.35)**(pseduoDay-1)  # 35% growth rate
y3 = 100*(1.15)**(pseduoDay-1)  # 15% growth rate
y4 = 100*(1.05)**(pseduoDay-1)  # 5% growth rate
# Pseduo data for deathplot
z1 = 3*(1.85)**(pseduoDay-1)  # 85% growth rate
z2 = 3*(1.35)**(pseduoDay-1)  # 35% growth rate
z3 = 3*(1.15)**(pseduoDay-1)  # 15% growth rate
z4 = 3*(1.05)**(pseduoDay-1)  # 5% growth rate

# Remove tests/critical row for US and Canada and Australian and China
df_latest = df_latest.drop(df_latest[df_latest['Confirmed'] == 0].index, axis=0)

# Generate data for Sunburst plot
df_sunburst = df_latest

# Since child node cannot be mixture of None and string, so replace 'Yokohoma' as 'Diamond Princess' and 
# All as 'other'
df_sunburst.at[df_sunburst.loc[df_sunburst['Country/Region'] == 'Japan',].index[0], 'Province/State'] = 'Other'
# Require n/a as None type 
df_sunburst = df_sunburst.where(pd.notnull(df_sunburst), None)
df_sunburst['Province/State'].replace({'Yokohama':'Diamond Princess', 'Brussels':None}, inplace=True)

# Data for ternary chart
df_ternary = WorldwildTable.drop(WorldwildTable[WorldwildTable['Country/Region'] == 'Artania Cruise'].index, axis=0)

# generate option list for dropdown
optionList = []
for i in WorldwildTable['Country/Region']:
    optionList.append({'label':i, 'value':i})
optionList = sorted(optionList, key = lambda i: i['value'])
# Add 'All' at the beginning of the list
optionList = [{'label':'All', 'value':'All'}] + optionList


#############################################################################################
# Start to make plots
#############################################################################################

# Line plot for death rate cases
# Set up tick scale based on death case number of Mainland China
#tickList = np.arange(0, (df_recovered['Total']/df_confirmed['Total']*100).max()+0.5, 0.5)

# Create empty figure canvas
fig_rate = go.Figure()
# Add trace to the figure
fig_rate.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Total']/df_confirmed['Total']*100,
                                mode='lines+markers',
                                line_shape='spline',
                                name='Death Rate',
                                line=dict(color='#7f7f7f', width=2),
                                marker=dict(size=2, color='#7f7f7f',
                                            line=dict(width=.5, color='#7f7f7f')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_deaths['Date']],
                                hovertext=['Global death rate<br>{:.2f}%'.format(
                                    i) for i in df_deaths['Total']/df_confirmed['Total']*100],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
fig_rate.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Total']/df_confirmed['Total']*100,
                                mode='lines+markers',
                                line_shape='spline',
                                name='Recovery Rate',
                                line=dict(color='#2ecc77', width=2),
                                marker=dict(size=2, color='#2ecc77',
                                            line=dict(width=.5, color='#2ecc77')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_recovered['Date']],
                                hovertext=['Global recovery rate<br>{:.2f}%'.format(
                                    i) for i in df_recovered['Total']/df_confirmed['Total']*100],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
# Customise layout
fig_rate.update_layout(
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis=dict(
        showline=False, linecolor='#272e3e',
        zeroline=False,
        # showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        tickmode='array',
        # Set tick range based on the maximum number
        #tickvals=tickList,
        # Set tick label accordingly
        #ticktext=['{:.1f}'.format(i) for i in tickList]
    ),
#    yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x unified',
    showlegend=True,
    legend_orientation="h",
    legend=dict(x=.36, y=-0.1,),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)

# Default cumulative plot for tab
# Default plot is an empty canvas
#df_region_tab = pd.read_csv('./cumulative_data/{}.csv'.format('Worldwide'))
#df_region_tab = df_region_tab.astype({'Date_last_updated_AEDT': 'datetime64', 'date_day': 'datetime64'})

# Create empty figure canvas
fig_cumulative_tab = go.Figure()
# Customise layout
fig_cumulative_tab.update_layout(
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),
        yaxis_title="Cumulative cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
        ),
        xaxis_title="Select a location from the table (Toggle the legend to see specific curves)",
        xaxis=dict(
            showline=False, linecolor='#272e3e',
            showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            zeroline=False
        ),
        xaxis_tickformat='%b %d',
        # transition = {'duration':500},
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

# Create empty figure canvas
fig_daily_tab = go.Figure()
# Customise layout
fig_daily_tab.update_layout(
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),
        yaxis_title="Daily cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
        ),
        xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
        xaxis=dict(
            showline=False, linecolor='#272e3e',
            showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            zeroline=False
        ),
        xaxis_tickformat='%b %d',
        # transition = {'duration':500},
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )


# Default log curve plot for confirmed cases
# Create empty figure canvas
fig_curve_tab = go.Figure()

fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
)
for regionName in ['Worldwide', 'Japan', 'Italy', 'India', 'US']:

  dotgrayx_tab = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'DayElapsed'])[0]]
  dotgrayy_tab = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'Confirmed'])[0]]

  fig_curve_tab.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == regionName]['DayElapsed'],
                                     y=dfs_curve.loc[dfs_curve['Region'] == regionName]['Confirmed'],
                                     mode='lines',
                                     line_shape='spline',
                                     name=regionName,
                                     opacity=0.3,
                                     line=dict(color='#636363', width=1.5),
                                     text=[
                                            i for i in dfs_curve.loc[dfs_curve['Region'] == regionName]['Region']],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '<br>%{x} days after 100 cases<br>' +
                                                   'with %{y:,d} cases<br>'
                                                   '<extra></extra>'
                             )
  )

  fig_curve_tab.add_trace(go.Scatter(x=dotgrayx_tab,
                                     y=dotgrayy_tab,
                                     mode='markers',
                                     marker=dict(size=6, color='#636363',
                                     line=dict(width=1, color='#636363')),
                                     opacity=0.5,
                                     text=[regionName],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '<br>%{x} days after 100 cases<br>' +
                                                   'with %{y:,d} cases<br>'
                                                   '<extra></extra>'
                            )
  )

# Customise layout
fig_curve_tab.update_xaxes(range=[0, daysOutbreak-19])
fig_curve_tab.update_yaxes(range=[1.9, 7])
fig_curve_tab.update_layout(
        xaxis_title="Number of day since 3rd death case",
        yaxis_title="Confirmed cases (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        yaxis_type="log",
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

# Default curve plot for death toll curve
# Create empty figure canvas
fig_death_curve_tab = go.Figure()

fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
)
fig_death_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=z4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
)

for regionName in ['Worldwide', 'Japan', 'Italy', 'UK', 'US']:

  dotgrayx_tab_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'DayElapsed_death'])[0]]
  dotgrayy_tab_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'Deaths'])[0]]

  fig_death_curve_tab.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['DayElapsed_death'],
                                     y=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Deaths'],
                                     mode='lines',
                                     line_shape='spline',
                                     name=regionName,
                                     opacity=0.3,
                                     line=dict(color='#636363', width=1.5),
                                     text=[
                                            i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Region']],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '<br>%{x} days since 3rd death cases<br>' +
                                                   'with %{y:,d} death cases<br>'
                                                   '<extra></extra>'
                             )
  )

  fig_death_curve_tab.add_trace(go.Scatter(x=dotgrayx_tab_death,
                                     y=dotgrayy_tab_death,
                                     mode='markers',
                                     marker=dict(size=6, color='#636363',
                                     line=dict(width=1, color='#636363')),
                                     opacity=0.5,
                                     text=[regionName],
                                     hovertemplate='<b>%{text}</b><br>' +
                                                   '<br>%{x} days since 3rd death cases<br>' +
                                                   'with %{y:,d} death cases<br>'
                                                   '<extra></extra>'
                            )
  )

# Customise layout
fig_death_curve_tab.update_xaxes(range=[0, daysOutbreak-19])
fig_death_curve_tab.update_yaxes(range=[0.477, 5.5])
fig_death_curve_tab.update_layout(
        xaxis_title="Number of days since 3 deaths recorded",
        yaxis_title="Death cases (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        yaxis_type="log",
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

##################################################################################################
# Start dash app
##################################################################################################
BS = "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"

app = dash.Dash(__name__,
                assets_folder='./assets/',
                external_stylesheets=[BS],
                meta_tags=[
                    {"name": "author", "content": "Jun Ye"},
                    {"name": "keywords", "content": "coronavirus dashboard, COVID-19, dashborad, global cases, coronavirus, monitor, real time, 世界，疫情, 冠状病毒, 肺炎, 新型肺炎, 最新疫情, 实时疫情, 疫情地图, 疫情"},
                    {"name": "description", "content": "The coronavirus COVID-19 dashboard/monitor provides up-to-date data, map, cumulative curve, growth trajectory for the global spread of coronavirus.\
                      As of {}, there are {:,d} confirmed cases globally.\
                     In the meanwhile, please keep calm, stay home and wash your hand!".format(latestDate, confirmedCases)},
                    {"property": "og:title",
                        "content": "Coronavirus COVID-19 Outbreak Global Cases Monitor Dashboard"},
                    {"property": "og:type", "content": "website"},
                    {"property": "og:image", "content": "https://junye0798.com/post/build-a-dashboard-to-track-the-spread-of-coronavirus-using-dash/featured_hu9ce2660d9033d1f04035dc6d42b64a44_967087_1200x0_resize_lanczos_2.png"},
                    {"property": "og:url",
                        "content": "https://dash-coronavirus-2020.herokuapp.com/"},
                    {"property": "og:description",
                        "content": "The coronavirus COVID-19 dashboard/monitor provides up-to-date data and map for the global spread of coronavirus.\
                      As of {}, there are {:,d} confirmed cases globally.\
                     In the meanwhile, please keep calm, stay home and wash your hand!".format(latestDate, confirmedCases)},
                    {"name": "twitter:card", "content": "summary_large_image"},
                    {"name": "twitter:site", "content": "@perishleaf"},
                    {"name": "twitter:title",
                        "content": "Coronavirus COVID-19 Outbreak Global Cases Monitor Dashboard"},
                    {"name": "twitter:description",
                        "content": "The coronavirus COVID-19 dashboard/monitor provides up-to-date data and map for the global spread of coronavirus.\
                      As of {}, there are {:,d} confirmed cases globally.\
                     In the meanwhile, please keep calm, stay home and wash your hand!".format(latestDate, confirmedCases)},
                    {"name": "twitter:image", "content": "https://junye0798.com/post/build-a-dashboard-to-track-the-spread-of-coronavirus-using-dash/featured_hu9ce2660d9033d1f04035dc6d42b64a44_967087_1200x0_resize_lanczos_2.png"},
                    {"name": "viewport",
                        "content": "width=device-width, height=device-height, initial-scale=1.0"}
                ]
      )

app.title = 'Coronavirus COVID-19 Global Monitor'

# Section for Google annlytic and donation #
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <script data-name="BMC-Widget" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="qPsBJAV" data-description="Support the app server for running!" data-message="Please support the app server for running!" data-color="#FF813F" data-position="right" data-x_margin="18" data-y_margin="25"></script>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-154901818-2"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'UA-154901818-2');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <script type='text/javascript' src='https://platform-api.sharethis.com/js/sharethis.js#property=5e5e32508d3a3d0019ee3ecb&product=sticky-share-buttons&cms=website' async='async'></script>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""

server = app.server

app.config['suppress_callback_exceptions'] = True # This is to prevent app crash when loading since we have plot that only render when user clicks.

app.layout = html.Div(
    id='app-body',
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(
                    id='herder-title',
                    children="Coronavirus (COVID-19) Outbreak Global Cases Monitor"),
                html.P(
                    id="description",
                    children=dcc.Markdown(
                        children=(
                            '''
                            On Dec 31, 2019, the World Health Organization (WHO) was informed 
                            an outbreak of “pneumonia of unknown cause” detected in Wuhan, Hubei Province, China. 
                            The virus that caused the outbreak of COVID-19 was lately known as _severe acute respiratory syndrome coronavirus 2_ (SARS-CoV-2). 
                            The WHO declared the outbreak to be a Public Health Emergency of International Concern on 
                            Jan 30, 2020 and recognized it as a pandemic on Mar 11, 2020. As of {}, there are {:,d} confirmed cases globally.
                        
                            This dashboard is developed to visualise and track the recent reported 
                            cases on a hourly timescale.'''.format(latestDate, confirmedCases),
                        )
                    )
                ),
                html.P(
                    className='time-stamp',
                    children="Last update: {}. (Hover over items for additional information)".format(latestDate)
                ),
                html.Hr(
                ),
            ]
        ),
        html.Div(
            className="number-plate",
            children=[
                html.Div(
                    className='number-plate-single',
                    style={'border-top': '#292929 solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#292929',},
                            children="Days since outbreak"
                        ),
                        html.H3(
                            style={'color': '#292929'},
                            children=[
                                '{}'.format(daysOutbreak),
                                html.P(
                                    style={'color': '#ffffff',},
                                    children='xxxx xx xxx xxxx xxx xxxxx'
                                ), 
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-active',
                    style={'border-top': '#f0953f solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#f0953f'},
                            children="Active cases"
                        ),
                        html.H3(
                        	style={'color': '#f0953f'},
                            children=[
                                '{:,d}'.format(remainCases),
                                html.P(
                                    children='+ {:,d} in the past 24h ({:.1%})'.format(plusRemainNum, plusRemainNum3)
                                ),      
                            ]
                        ),
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-confirm',
                    style={'border-top': '#f03f42 solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#f03f42'},
                            children="Confirmed cases"
                        ),
                        html.H3(
                            style={'color': '#f03f42'},
                            children=[
                                '{:,d}'.format(confirmedCases),
                                html.P(
                                    children='+ {:,d} in the past 24h ({:.1%})'.format(plusConfirmedNum, plusPercentNum1)
                                ),
                                
                            ]
                        ),
                        
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-recover',
                    style={'border-top': '#2ecc77 solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#2ecc77'},
                            children="Recovered cases"
                        ),
                        html.H3(
                            style={'color': '#2ecc77'},
                            children=[
                                '{:,d}'.format(recoveredCases),
                                html.P(
                                    children='+ {:,d} in the past 24h ({:.1%})'.format(plusRecoveredNum, plusPercentNum2)
                                ),
                                
                            ]
                        ),
                        
                    ]
                ),
                html.Div(
                    className='number-plate-single',
                    id='number-plate-death',
                    style={'border-top': '#7f7f7f solid .2rem',},
                    children=[
                        html.H5(
                            style={'color': '#7f7f7f'},
                            children="Death cases"
                        ),
                        html.H3(
                        	style={'color': '#7f7f7f'},
                            children=[
                                '{:,d}'.format(deathsCases),
                                html.P(
                                    children='+ {:,d} in the past 24h ({:.1%})'.format(plusDeathNum, plusPercentNum3)
                                ),
                                
                            ]
                        ),
                        
                    ]
                ),
                dbc.Tooltip(
                    target='number-plate-active',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            1 day ago: **{:,d}**

                            2 days ago: **{:,d}** 

                            '''.format(df_confirmed['Total'][1] - df_deaths['Total'][1] - df_recovered['Total'][1], df_confirmed['Total'][2]- df_deaths['Total'][2] - df_recovered['Total'][2]),
                        ) 
                ),
                dbc.Tooltip(
                    target='number-plate-confirm',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            1 day ago: **{:,d}**

                            2 days ago: **{:,d}** 

                            '''.format(df_confirmed['Total'][1], df_confirmed['Total'][2]),
                        ) 
                ),
                dbc.Tooltip(
                    target='number-plate-recover',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            1 day ago: **{:,d}**

                            2 days ago: **{:,d}** 

                            '''.format(df_recovered['Total'][1], df_recovered['Total'][2]),
                        ) 
                ),
                dbc.Tooltip(
                    target='number-plate-death',
                    style={"fontSize":"1.8em", 'textAlign':'right', 'padding':'10px',},
                    children=
                        dcc.Markdown(
                            '''
                            1 day ago: **{:,d}**

                            2 days ago: **{:,d}** 

                            '''.format(df_deaths['Total'][1], df_deaths['Total'][2]),
                        ) 
                ),
            ]
        ),
        html.Div(
            className='section-line',
            children=[
                html.Hr(
                ),
            ]
        ),
        html.Div(
            className='row dcc-plot',
            children=[
                html.Div(
                	className='dcc-sub-plot',
                    children=[
                        html.Div(
                            id='case-timeline-log-button',
                            children=[
                                html.H5(
                                    children='Case Timeline | Worldwide'
                                ),
                                daq.PowerButton(
                                    id='log-button',
                                    size=22,
                                    color="#2674f6",
                                    on=False,
                                ),
                                dbc.Tooltip(
                                	"Switch between linear and logarithmic y-axis",
                                    target='log-button',
                                    style={"fontSize":"1.8em"},
                                ),
                            ],
                        ),
                        dcc.Graph(
                            id='combined-line-plot',
                            config={"displayModeBar": False, "scrollZoom": False}, 
                        ),
                    ]
                ),
                html.Div(
                	className='dcc-sub-plot',
                    children=[                                  
                        html.H5(
                            id='dcc-death-graph-head',
                            children='Recovery/Death Rate (%) Timeline | Worldwide'
                        ),
                        dcc.Graph(
                            style={'height': '301px'}, 
                            figure=fig_rate,
                            config={"displayModeBar": False, "scrollZoom": False},
                        ),
                        dbc.Tooltip(
                            target='dcc-death-graph-head',
                            style={"fontSize":"1.8em", 'textAlign':'left', 'padding':'10px','width':'auto', 'maxWidth':'450px'},
                            children=[
                                dcc.Markdown(
                                    '''
                                    Death rate is calculated using the formula: 

                                    **Death rate = (Deaths/Confirmed cases) x 100%**
                                    
                                    Note that this is only a conservative estimation. The real death rate can only be 
                                    revealed as all cases are resolved. 
                                    ''',
                                )
                            ] 
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className='row dcc-plot',
            children=[
                html.Div(
                	className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Latest Coronavirus Outbreak Map'
                        ),
                        dcc.Graph(
                            id='datatable-interact-map',
                            style={'height': '400px'},
                            config={"displayModeBar": False, "scrollZoom": True},
                        ),
                    ]
                ),
                html.Div(
                	className='dcc-sub-plot',
                    children=[
                        html.H5(
                            children='Summary Graph'
                        ),
                        dcc.Dropdown(
                            id="dcc-dropdown",
                            placeholder="Select a graph type",
                            value='Daily Cases',
                            options=[
                                {'label':'Cumulative Cases', 'value':'Cumulative Cases'},
                                {'label':'Daily Cases', 'value':'Daily Cases'},
                                {'label':'Confirmed Case Trajectories', 'value':'Confirmed Case Trajectories'},
                                {'label':'Death Toll Trajectories', 'value':'Death Toll Trajectories'},
                            ]
                        ),                                  
                        html.Div(
                        	id='tabs-content-plots',
                        ),
                    ]
                ),
            ]
        ),
        html.Div(
            className='dcc-table',
            children=[
                html.H5(
                    id='dcc-table-header',
                    children='Cases Summary by Location'
                ),
                dcc.Tabs(
                    id="tabs-table",
                    value='Worldwide',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                    children=[
                        dcc.Tab(
                        	label='Worldwide',
                            value='Worldwide',
                            className='custom-tab',
                            selected_className='custom-tab--selected',
                            children=[
                                dash_table.DataTable(
                                    id='datatable-interact-location',
                                    # Don't show coordinates
                                    columns=[{"name": 'Country/Region', "id": 'Country/Region'}] +
                                            [{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                                                if i == 'Death rate' or i == 'Positive rate' else {"name": i, "id": i, 'type': 'numeric', 'format': Format(group=',')}
                                                    for i in WorldwildTable.columns[1:11]],
                                    # But still store coordinates in the table for interactivity
                                    data=WorldwildTable.to_dict("rows"),
                                    #css= [{'selector': 'tr:hover', 'rule': 'background-color: #2674f6;'}],
                                    row_selectable="single",
                                    sort_action="native",
                                    style_as_list_view=True,
                                    style_cell={
                                        'fontFamily': 'Roboto',
                                        'backgroundColor': '#ffffff', 
                                    },
                                    fixed_rows={
                                        'headers': True, 'data': 0},
                                    style_table={
                                        'minHeight': '400px',
                                        'height': '400px',
                                        'maxHeight': '400px',
                                        'overflowX': 'auto',
                                    },
                                    style_header={
                                        'backgroundColor': '#ffffff',
                                        'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                        {'if': {'column_id': 'Country/Regions'}, 'width': '17%'},
                                        {'if': {'column_id': 'Active'}, 'width': '8%'},
                                        {'if': {'column_id': 'Confirmed'}, 'width': '8%'},
                                        {'if': {'column_id': 'Recovered'}, 'width': '8%'},
                                        {'if': {'column_id': 'Critical'}, 'width': '8%'},
                                        {'if': {'column_id': 'Deaths'}, 'width': '8%'},
                                        {'if': {'column_id': 'Death rate'}, 'width': '8%'},
                                        {'if': {'column_id': 'Tests'}, 'width': '8%'},
                                        {'if': {'column_id': 'Positive rate'}, 'width': '9%'},
                                        {'if': {'column_id': 'Tests/100k'}, 'width': '9%'},    
                                        {'if': {'column_id': 'Confirmed/100k'}, 'width': '9%'},
                                        {'if': {'column_id': 'Active'}, 'color':'#f0953f'},
                                        {'if': {'column_id': 'Confirmed'}, 'color': '#f03f42'},
                                        {'if': {'column_id': 'Recovered'}, 'color': '#2ecc77'},
                                        {'if': {'column_id': 'Deaths'}, 'color': '#7f7f7f'},
                                        {'textAlign': 'center'}
                                    ],
                                )
                            ]
                        ),
                        make_dcc_country_tab(
                            'Africa', table_dict['AfricaTable']),
                        make_dcc_country_tab(
                            'Asia', table_dict['AsiaTable']),                              
                        make_dcc_country_tab(
                            'Europe', table_dict['EuropeTable']),
                        make_dcc_country_tab(
                            'North America', table_dict['NorthAmericaTable']),
                        make_dcc_country_tab(
                            'Oceania', table_dict['OceaniaTable']),
                        make_dcc_country_tab(
                            'South America', table_dict['SouthAmericaTable']),
                        make_dcc_country_tab(
                            'Australia', AustraliaTable),
                        make_dcc_Brazil_tab(
                            'Brazil', BrazilTable),
                        make_dcc_country_tab(
                            'Canada', CanadaTable),
                        make_dcc_Brazil_tab(
                            'Germany', GermanyTable),
                        make_dcc_country_tab(
                            'Mainland China', MainlandChinaTable),
                        make_dcc_country_tab(
                            'United States', UnitedStatesTable),

                    ]
                ),
                dbc.Tooltip(
                    target='tab-datatable-interact-location-Australia',
                    style={"fontSize":"1.8em", 'textAlign':'left', 'padding':'10px','width':'auto', 'maxWidth':'450px'},
                    children=
                        dcc.Markdown(
                            children=(
                                '''
                                Note that under _National Notifiable Diseases Surveillance
                                System_ reporting requirements, cases are reported based on their Australian
                                jurisdiction of residence rather than where they were detected.

                                '''
                            )
                        )                                              
                ),
                dbc.Tooltip(
                    target='tab-datatable-interact-location-US',
                    style={"fontSize":"1.8em", 'textAlign':'left', 'padding':'10px','width':'auto', 'maxWidth':'250px'},
                    children=
                        dcc.Markdown(
                            children=(
                                '''
                                Add case data for US Military, Veteran Affair and Federal Bureau of Prisons on April 24 2020. 
                                '''
                            )
                        )                                              
                ),
                dbc.Tooltip(
                    target='dcc-table-header',
                    style={"fontSize":"1.8em", 'textAlign':'left', 'padding':'10px', 'width':'auto', 'maxWidth':'450px'},
                    children=
                        dcc.Markdown(
                            children=(
                                '''
                                Data is collected from multiple sources.

                                * [Worldometers](https://www.worldometers.info/coronavirus/)
                                * [Johns Hopkins Dashboard](https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/htmlview?usp=sharing&sle=true#)
                                * [Australia Government Department of Health](https://www.health.gov.au/news/coronavirus-update-at-a-glance)
                                * [2020 coronavirus pandemic in Australia](https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Australia)
                                * [National Health Commission of the People's Republic of China](http://www.nhc.gov.cn/)
                                * [DX Doctor](https://ncov.dxy.cn/ncovh5/view/en_pneumonia?from=dxy&source=&link=&share=)
                                * [Tencent News](https://news.qq.com//zt2020/page/feiyan.htm#charts)
                                * [COVID-19 in US and Canada by 1Point3Acres](https://coronavirus.1point3acres.com/en)
                                * [Robert Koch Institute](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html)

                                '''
                            )
                        )
                ),
            ]
        ),
        html.Div(
            className='dcc-plot',
            id='sunburst-chart',
            children=[
                html.Div(
                    className='dcc-sub-plot sunburst-ternary-plot',
                    children=[
                        html.Div(
                            className='header-container',                            
                            children=[
                                html.H5(
                                    children='Sunburst Chart | Worldwide'
                                ),
                            ]
                        ),
                        dcc.Dropdown(
                        	id="sunburst-dropdown",
                            placeholder="Select a metric",
                            value='Confirmed',
                            searchable=False,
                            clearable=False,
                            options=[{'label':'Active cases', 'value':'Remaining'},
                                     {'label':'Confirmed cases', 'value':'Confirmed'},
                                     {'label':'Recovered cases', 'value':'Recovered'},
                                     {'label':'Deaths', 'value':'Deaths'},
                            ]
                        ),                                  
                        dcc.Graph(
                        	id='dropdown-sunburst-plots',
                            style={'height': '500px'},
                            config={"displayModeBar": False, "scrollZoom": False},
                        ),
                    ]
                ),
                html.Div(
                    className='dcc-sub-plot sunburst-ternary-plot',
                    children=[
                        html.Div(
                            className='header-container',
                            id='ternary-plot',
                            children=[
                                html.H5(
                                    children='Ternary Chart | Worldwide'
                                ),
                            ]
                        ),
                        dcc.Dropdown(
                        	id="ternary-dropdown",
                            placeholder="Select or search a location name",
                            value='All',
                            options=optionList,
                        ),                 
                        dcc.Graph(
                            id='ternary-dropdown-chart',
                            style={'height': '500px'},
                            config={"displayModeBar": False, "scrollZoom": False}, 
                        ),
                    ]
                ),
                dbc.Tooltip(
                    target='ternary-plot',
                    style={"fontSize":"1.8em", 'textAlign':'left', 'padding':'10px'},
                    children=
                        dcc.Markdown(
                            children=(
                                '''
                                The ternary diagram displays the proportion of **active**, **recovered** and **deaths** cases in confirmed cases.

                                Point size represents population. 

                                '''
                            )
                        )
                ),
            ]
        ),
        html.Div(
            className='footer-container',
            id='my-footer',
            children=[
                html.P(
                    'Keep calm and stay home',
                ),
                html.P(
                    ' | ',
                ),
                html.P(
                    children=[
                        html.A(
                            'Developed by Jun with ❤️ in Sydney', 
                            href='https://junye0798.com/', 
                            target='_blank'
                        ),
                    ],
                ),
                html.P(
                    ' | ',
                ),
                html.Div(
                    id='contributor-button',
                    children=[
                        dbc.Button(
                            "Contributor", 
                            id="open-contributor", 
                            className="button", 
                        ),
                        dbc.Modal(
                            id='modal-contributor',
                            children=[
                                dbc.ModalHeader("Contributor"),
                                dbc.ModalBody(
                                    html.Div(
                                        html.P(
                                            children=[
                                                html.A(
                                                    'Johannes Pistorius', 
                                                    href='https://www.johannespistorius.de/', 
                                                    target='_blank'
                                                ),
                                                ': CSS Design, ',
                                                html.A(
                                                    'Nick Byrne',
                                                    href='https://www.linkedin.com/in/nbyrne/?originalSubdomain=au',
                                                    target='_blank'
                                                ),
                                                ': Strategic Support',
                                            ],
                                        ),
                                    ),  
                                ),
                                dbc.ModalFooter(
                                    children=[
                                        dbc.Button(
                                            "Close", 
                                            id="close-contributor", 
                                            className="ml-auto",
                                            style={'background-color':'#20b6e6', 'font-weight':'bold'}
                                        )
                                    ],            
                                ),
                            ],
                        ),
                    ]
                ),
                html.P(
                    ' | ',
                ),
                html.P(
                    children=[
                        html.A(
                            'About this dashboard', 
                            href='https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus',
                            target='_blank'
                        ),
                    ],
                ),
                html.P(
                    ' | ',
                ),           
                html.P(
                    children=[
                        html.A(
                            'Report a bug', 
                            href='https://twitter.com/perishleaf', 
                            target='_blank'
                        ),
                    ],
                ),                
                html.P(
                    ' | ',
                ),
                html.P(
                    children=[
                        html.A(
                            'COVID-19 infographic in Australia', 
                            href='https://www.health.gov.au/sites/default/files/documents/2020/05/coronavirus-covid-19-at-a-glance-coronavirus-covid-19-at-a-glance-infographic_19.pdf', 
                            target='_blank'
                                ),
                    ],
                ),
                html.P(
                    ' | ',
                ), 
                html.Div(
                    id='disclaimer-button',
                    children=[
                        dbc.Button(
                        	"Disclaimer", 
                        	id="open", 
                        	#color="info", 
                        	className="button", 
                        ),
                        dbc.Modal(
                        	id='modal',
                            children=[
                                dbc.ModalHeader("Disclaimer"),
                                dbc.ModalBody(
                                    '''
                                    This website and its contents herein, including all data, 
                                    mapping, and analysis, is provided to the public strictly 
                                    for general information purposes only. All the information was 
                                    collected from multiple publicly available data sources that do 
                                    not always agree. While I will try my best to keep the information up 
                                    to date and correct, I make no representations or warranties of any kind, 
                                    express or implied, about the completeness, accuracy, reliability, with 
                                    respect to the website or the information. I do not bear any legal responsibility 
                                    for any consequence caused by the use of the information provided. Reliance on 
                                    the website for medical guidance or use of the website in commerce is strongly 
                                    not recommended. Any action you take upon the information on this website is 
                                    strictly at your own risk. and I will not be liable for any losses and damages 
                                    in connection with the use of this website. Screenshots of the website are 
                                    permissible so long as you provide appropriate credit.
                                    '''
                                ),
                                dbc.ModalFooter(
                                	children=[
                                	    dbc.Button(
                                		    "Close", 
                                		    id="close", 
                                		    className="ml-auto",
                                            style={'background-color':'#20b6e6', 'font-weight':'bold'}
                                        )
                                    ],            
                                ),
                            ],
                        ),
                    ]
                ),
            ]
        ),
    ]
)

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(
    Output("modal-contributor", "is_open"),
    [Input("open-contributor", "n_clicks"), Input("close-contributor", "n_clicks")],
    [State("modal-contributor", "is_open")],
)
def toggle_modal_contributor(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

@app.callback(Output('tabs-content-plots', 'children'),
              [Input('dcc-dropdown', 'value')]
)
def render_content(tab):
    if tab == 'Cumulative Cases':
        return dcc.Graph(id='datatable-interact-lineplot',
                         style={'height': '364px'},
                         figure=fig_cumulative_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )
    elif tab == 'Daily Cases':
        return dcc.Graph(id='datatable-interact-dailyplot',
                         style={'height': '364px'},
                         figure=fig_daily_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )
    elif tab == 'Confirmed Case Trajectories':
        return dcc.Graph(id='datatable-interact-logplot',
                         style={'height': '364px'},
                         figure=fig_curve_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )
    elif tab == 'Death Toll Trajectories':
        return dcc.Graph(id='datatable-interact-deathplot',
                         style={'height': '364px'},
                         figure=fig_death_curve_tab,
                         config={"displayModeBar": False, "scrollZoom": False},
                )

@app.callback(Output('combined-line-plot', 'figure'),
              [Input('log-button', 'on')])

def render_combined_line_plot(log):
  if log is True:
    axis_type = 'log'
  else:
    axis_type = 'linear'

  # Line plot for combine recovered cases
  # Set up tick scale based on total recovered case number
  #tickList = np.arange(0, df_remaining['Total'].max()+10000, 30000)

  # Create empty figure canvas
  fig_combine = go.Figure()
  # Add trace to the figure
  
  fig_combine.add_trace(go.Scatter(x=df_remaining['Date'], y=df_remaining['Total'],
                                mode='lines+markers',
                                line_shape='spline',
                                name='Active',
                                line=dict(color='#f0953f', width=2),
                                marker=dict(size=2, color='#f0953f',
                                            line=dict(width=.5, color='#f0953f')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_deaths['Date']],
                                hovertext=['Total active<br>{:,d} cases<br>'.format(
                                    i) for i in df_remaining['Total']],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
  fig_combine.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Total'],
                                   mode='lines+markers',
                                   line_shape='spline',
                                   name='Confirmed',
                                   line=dict(color='#f03f42', width=2),
                                   marker=dict(size=2, color='#f03f42',
                                               line=dict(width=.5, color='#f03f42')),
                                   text=[datetime.strftime(
                                       d, '%b %d %Y GMT+10') for d in df_confirmed['Date']],
                                   hovertext=['Total confirmed<br>{:,d} cases<br>'.format(
                                       i) for i in df_confirmed['Total']],
                                   hovertemplate='%{hovertext}' +
                                                 '<extra></extra>'))
  fig_combine.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Total'],
                                   mode='lines+markers',
                                   line_shape='spline',
                                   name='Recovered',
                                   line=dict(color='#2ecc77', width=2),
                                   marker=dict(size=2, color='#2ecc77',
                                               line=dict(width=.5, color='#2ecc77')),
                                   text=[datetime.strftime(
                                       d, '%b %d %Y GMT+10') for d in df_recovered['Date']],
                                   hovertext=['Total recovered<br>{:,d} cases<br>'.format(
                                       i) for i in df_recovered['Total']],
                                   hovertemplate='%{hovertext}' +
                                                 '<extra></extra>'))
  fig_combine.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Total'],
                                mode='lines+markers',
                                line_shape='spline',
                                name='Death',
                                line=dict(color='#7f7f7f', width=2),
                                marker=dict(size=2, color='#7f7f7f',
                                            line=dict(width=.5, color='#7f7f7f')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y GMT+10') for d in df_deaths['Date']],
                                hovertext=['Total death<br>{:,d} cases<br>'.format(
                                    i) for i in df_deaths['Total']],
                                hovertemplate='%{hovertext}' +
                                              '<extra></extra>'))
  # Customise layout
  fig_combine.update_layout(
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=5,
        pad=0
    ),
    yaxis_type=axis_type,
    yaxis=dict(
        showline=False, linecolor='#272e3e',
        zeroline=False,
        # showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        #tickmode='array',
        # Set tick range based on the maximum number
        #tickvals=tickList,
        # Set tick label accordingly
        #ticktext=["{:.0f}k".format(i/1000) for i in tickList]
    ),
#    yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x unified',
    legend_orientation="h",
    legend=dict(x=.26, y=-.1,),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
  )
  
  return fig_combine

@app.callback(Output('dropdown-sunburst-plots', 'figure'),
              [Input('sunburst-dropdown', 'value')])

def render_sunburst_plot(metric):
    colorTheme=px.colors.qualitative.Safe

    if metric == 'Confirmed':
        hovertemplate = '<b>%{label} </b> <br><br>Confirmed: %{value} cases'
    elif metric == 'Recovered':
        hovertemplate = '<b>%{label} </b> <br>Recovered: %{value} cases'
    elif metric == 'Deaths':
        hovertemplate = '<b>%{label} </b> <br>Deaths: %{value} cases'
    elif metric == 'Remaining':
        hovertemplate = '<b>%{label} </b> <br>Active: %{value} cases'


    fig_sunburst = px.sunburst(
        df_sunburst, 
        path=['Continent','Country/Region', 'Province/State'], 
        values=metric,
        hover_data=[metric],
        color_discrete_sequence=colorTheme,           
    )

    fig_sunburst.update_traces(
        textinfo='label+percent root',
  	    hovertemplate=hovertemplate
    )
    fig_sunburst.update_layout(
        annotations=[
            dict(
                x=0.5,
                y=-0.2,
                xref='paper',
                yref='paper',
                text='Click to unfold segment',
                showarrow=False,
                font=dict(
                    family='Roboto, sans-serif',
                    size=16,
                    color="#292929"
                ),
            )
        ]
    )

    return fig_sunburst

@app.callback(Output('ternary-dropdown-chart', 'figure'),
              [Input('ternary-dropdown', 'value')]
        )

def render_ternary_plot(value):
    # make ternary chart
    if value == 'All':
        fig_ternary = px.scatter_ternary(df_ternary, a="Recovered", b="Active", c="Deaths", template='plotly_white', 
            size=[i**(1/3) for i in df_ternary['Population']],
            color='Confirmed/100k',
            color_continuous_scale=px.colors.sequential.Aggrnyl,
        )
        fig_ternary.update_traces(
            text=df_ternary['Country/Region'],
            hovertemplate="<b>%{text}</b><br><br>" +
                          "Recovery rate: %{a:.2f}<br>" +
                          "Active rate: %{b: .2f}<br>" +
                          "Death rate: %{c: .2f}<br>" +
                          "Confirmed/100k: %{marker.color: .0f}",
            marker=dict(line=dict(width=1, color='White')),               
        )
        fig_ternary.update_layout(
            annotations=[
                dict(
                    x=0.5,
                    y=-0.2,
                    xref='paper',
                    yref='paper',
                    text='Double click the chart to reset view after zoom in',
                    showarrow=False,
                    font=dict(
                        family='Roboto, sans-serif',
                        size=16,
                        color="#292929"
                    ),
                )
            ]
        )
        return fig_ternary 
    else:
        fig_ternary = px.scatter_ternary(df_ternary, a="Recovered", b="Active", c="Deaths", template='plotly_white', 
            size=[i**(1/3) for i in df_ternary['Population']],
            opacity=[1 if i == value else 0.1 for i in WorldwildTable['Country/Region']],
            color='Confirmed/100k',
            color_continuous_scale=px.colors.sequential.Aggrnyl,
        )
        fig_ternary.update_traces(
            text=df_ternary['Country/Region'],
            hovertemplate="<b>%{text}</b><br><br>" +
                          "Recovery rate: %{a:.2f}<br>" +
                          "Active rate: %{b: .2f}<br>" +
                          "Death rate: %{c: .2f}<br>" +
                          "Confirmed/100k: %{marker.color: .0f}",
            marker=dict(line=dict(width=1, color='White')),               
        )
        fig_ternary.update_layout(
            annotations=[
                dict(
                    x=0.5,
                    y=-0.2,
                    xref='paper',
                    yref='paper',
                    text='Double click the chart to reset view after zoom in',
                    showarrow=False,
                    font=dict(
                        family='Roboto, sans-serif',
                        size=16,
                        color="#292929"
                    ),
                )
            ]
        )

        return fig_ternary 

@app.callback(
    Output('datatable-interact-map', 'figure'),
    input_list
)
def update_figures(
    value, 
    Worldwide_derived_virtual_selected_rows, Worldwide_selected_row_ids,
    Asia_derived_virtual_selected_rows, Asia_selected_row_ids,
    Oceania_derived_virtual_selected_rows, Oceania_selected_row_ids,
    NorthAmerica_derived_virtual_selected_rows, NorthAmerica_selected_row_ids,
    SouthAmerica_derived_virtual_selected_rows, SouthAmerica_selected_row_ids,
    Africa_derived_virtual_selected_rows, Africa_selected_row_ids,
    Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
    Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
    Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
    Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
    Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
    MainlandChina_derived_virtual_selected_rows, MainlandChina_selected_row_ids,
    UnitedStates_derived_virtual_selected_rows, UnitedStates_selected_row_ids,
):

    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncracy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.

    if value not in ['Brazil', 'Germany']:

        if value == 'Worldwide':
            if Worldwide_derived_virtual_selected_rows is None:
                Worldwide_derived_virtual_selected_rows = []
            dff = WorldwildTable
            latitude = 14.056159 if len(Worldwide_derived_virtual_selected_rows) == 0 else dff.loc[Worldwide_selected_row_ids[0]].lat
            longitude = 6.395626 if len(Worldwide_derived_virtual_selected_rows) == 0 else dff.loc[Worldwide_selected_row_ids[0]].lon
            zoom = 1.02 if len(Worldwide_derived_virtual_selected_rows) == 0 else 4
      
        elif value == 'Australia':
            if Australia_derived_virtual_selected_rows is None:
                Australia_derived_virtual_selected_rows = []

            dff = AustraliaTable
            latitude = -25.931850 if len(Australia_derived_virtual_selected_rows) == 0 else dff.loc[Australia_selected_row_ids[0]].lat
            longitude = 134.024931 if len(Australia_derived_virtual_selected_rows) == 0 else dff.loc[Australia_selected_row_ids[0]].lon
            zoom = 3 if len(Australia_derived_virtual_selected_rows) == 0 else 5
      
        elif value == 'Canada':
            if Canada_derived_virtual_selected_rows is None:
                Canada_derived_virtual_selected_rows = []

            dff = CanadaTable
            latitude = 55.474012 if len(Canada_derived_virtual_selected_rows) == 0 else dff.loc[Canada_selected_row_ids[0]].lat
            longitude = -97.344913 if len(Canada_derived_virtual_selected_rows) == 0 else dff.loc[Canada_selected_row_ids[0]].lon
            zoom = 3 if len(Canada_derived_virtual_selected_rows) == 0 else 5
      
        elif value == 'Mainland China':
            if MainlandChina_derived_virtual_selected_rows is None:
                MainlandChina_derived_virtual_selected_rows = []

            dff = MainlandChinaTable
            latitude = 33.471197 if len(MainlandChina_derived_virtual_selected_rows) == 0 else dff.loc[MainlandChina_selected_row_ids[0]].lat
            longitude = 106.206780 if len(MainlandChina_derived_virtual_selected_rows) == 0 else dff.loc[MainlandChina_selected_row_ids[0]].lon
            zoom = 2.5 if len(MainlandChina_derived_virtual_selected_rows) == 0 else 5
      
        elif value == 'United States':
            if UnitedStates_derived_virtual_selected_rows is None:
                UnitedStates_derived_virtual_selected_rows = []

            dff = UnitedStatesTable
            latitude = 40.022092 if len(UnitedStates_derived_virtual_selected_rows) == 0 else dff.loc[UnitedStates_selected_row_ids[0]].lat
            longitude = -98.828101 if len(UnitedStates_derived_virtual_selected_rows) == 0 else dff.loc[UnitedStates_selected_row_ids[0]].lon
            zoom = 3 if len(UnitedStates_derived_virtual_selected_rows) == 0 else 5
      
        elif value == 'Europe':
            if Europe_derived_virtual_selected_rows is None:
                Europe_derived_virtual_selected_rows = []

            dff = table_dict['EuropeTable']
            latitude = 52.405175 if len(Europe_derived_virtual_selected_rows) == 0 else dff.loc[Europe_selected_row_ids[0]].lat
            longitude = 11.403996 if len(Europe_derived_virtual_selected_rows) == 0 else dff.loc[Europe_selected_row_ids[0]].lon
            zoom = 1.5 if len(Europe_derived_virtual_selected_rows) == 0 else 5

        elif value == 'Asia':
            if Asia_derived_virtual_selected_rows is None:
                Asia_derived_virtual_selected_rows = []

            dff = table_dict['AsiaTable']
            latitude = 23.066523 if len(Asia_derived_virtual_selected_rows) == 0 else dff.loc[Asia_selected_row_ids[0]].lat
            longitude = 104.937341 if len(Asia_derived_virtual_selected_rows) == 0 else dff.loc[Asia_selected_row_ids[0]].lon
            zoom = 1 if len(Asia_derived_virtual_selected_rows) == 0 else 5

        elif value == 'North America':
            if NorthAmerica_derived_virtual_selected_rows is None:
                NorthAmerica_derived_virtual_selected_rows = []

            dff = table_dict['NorthAmericaTable']
            latitude = 40.022092 if len(NorthAmerica_derived_virtual_selected_rows) == 0 else dff.loc[NorthAmerica_selected_row_ids[0]].lat
            longitude = -98.828101 if len(NorthAmerica_derived_virtual_selected_rows) == 0 else dff.loc[NorthAmerica_selected_row_ids[0]].lon
            zoom = 1 if len(NorthAmerica_derived_virtual_selected_rows) == 0 else 5

        elif value == 'South America':
            if SouthAmerica_derived_virtual_selected_rows is None:
                SouthAmerica_derived_virtual_selected_rows = []

            dff = table_dict['SouthAmericaTable']
            latitude = -6.171080 if len(SouthAmerica_derived_virtual_selected_rows) == 0 else dff.loc[SouthAmerica_selected_row_ids[0]].lat
            longitude = -62.361203 if len(SouthAmerica_derived_virtual_selected_rows) == 0 else dff.loc[SouthAmerica_selected_row_ids[0]].lon
            zoom = 1 if len(SouthAmerica_derived_virtual_selected_rows) == 0 else 5

        elif value == 'Oceania':
            if Oceania_derived_virtual_selected_rows is None:
                Oceania_derived_virtual_selected_rows = []

            dff = table_dict['OceaniaTable']
            latitude = -25.931850 if len(Oceania_derived_virtual_selected_rows) == 0 else dff.loc[Oceania_selected_row_ids[0]].lat
            longitude = 134.024931 if len(Oceania_derived_virtual_selected_rows) == 0 else dff.loc[Oceania_selected_row_ids[0]].lon
            zoom = 2 if len(Oceania_derived_virtual_selected_rows) == 0 else 5

        elif value == 'Africa':
            if Africa_derived_virtual_selected_rows is None:
                Africa_derived_virtual_selected_rows = []

            dff = table_dict['AfricaTable']
            latitude = 5.986935 if len(Africa_derived_virtual_selected_rows) == 0 else dff.loc[Africa_selected_row_ids[0]].lat
            longitude = 22.252163 if len(Africa_derived_virtual_selected_rows) == 0 else dff.loc[Africa_selected_row_ids[0]].lon
            zoom = 1 if len(Africa_derived_virtual_selected_rows) == 0 else 5
      
        hovertext_value = ['Active: {:,d}<br>Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(h, i, j, k, t, q) 
                            for h, i, j, k, t, q in zip(
                                df_latest['Confirmed']-df_latest['Recovered']-df_latest['Deaths'],
                                df_latest['Confirmed'],  df_latest['Recovered'],
                                df_latest['Deaths'], df_latest['Deaths']/df_latest['Confirmed'], 
                                df_latest['Confirmed']*100000/df_latest['Population']
                            )
        ]

        mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

        # Generate a list for hover text display
        textList = []
        for area, region in zip(df_latest['Province/State'], df_latest['Country/Region']):

            if type(area) is str:
                if region == "Hong Kong" or region == "Macau" or region == "Taiwan":
                    textList.append(area)
                else:
                    textList.append(area+', '+region)
            else:
                textList.append(region)

        # Generate a list for color gradient display
        colorList = []
        for comfirmed, recovered, deaths in zip(df_latest['Confirmed'], df_latest['Recovered'], df_latest['Deaths']):
            remaining = comfirmed - deaths - recovered
            colorList.append(remaining)

        fig2 = go.Figure(go.Scattermapbox(
            lat=df_latest['lat'],
            lon=df_latest['lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                color=['#f03f42' if i > 0 else '#2ecc77' for i in colorList],
                size=[i**(1/3) for i in df_latest['Confirmed']],
                sizemin=1,
                sizemode='area',
                sizeref=2.*max([math.sqrt(i)
                    for i in df_latest['Confirmed']])/(100.**2),
            ),
            text=textList,
            hovertext=hovertext_value,
            hovertemplate="<b>%{text}</b><br><br>" +
                          "%{hovertext}<br>" +
                          "<extra></extra>")
        )
        fig2.update_layout(
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            margin=go.layout.Margin(l=10, r=10, b=10, t=0, pad=40),
            hovermode='closest',
            transition={'duration': 500},
            annotations=[
                dict(x=.5,
                    y=-.0,
                    align='center',
                    showarrow=False,
                    text="Points are placed based on data geolocation levels.<br>Province/State level - Australia, China, Canada, and United States; Country level- other countries.",
                    xref="paper",
                    yref="paper",
                    font=dict(size=10, color='#292929'),
                )
            ],
            mapbox=go.layout.Mapbox(
                accesstoken=mapbox_access_token,
                style="light",
                # The direction you're facing, measured clockwise as an angle from true north on a compass
                bearing=0,
                center=go.layout.mapbox.Center(
                    lat=latitude,
                    lon=longitude
                ),
                pitch=0,
                zoom=zoom
            )
        )

        return fig2
    else:
        if value == 'Brazil':
            if Brazil_derived_virtual_selected_rows is None:
                Brazil_derived_virtual_selected_rows = []

            dff = BrazilTable
            latitude = -12.423067 if len(Brazil_derived_virtual_selected_rows) == 0 else dff.loc[Brazil_selected_row_ids[0]].lat
            longitude = -58.627803 if len(Brazil_derived_virtual_selected_rows) == 0 else dff.loc[Brazil_selected_row_ids[0]].lon
            zoom = 3 if len(Brazil_derived_virtual_selected_rows) == 0 else 5

            fig2 = render_region_map(df_brazil, dff, latitude, longitude, zoom)
        
        elif value == 'Germany':
            if Germany_derived_virtual_selected_rows is None:
                Germany_derived_virtual_selected_rows = []

            dff = GermanyTable
            latitude = 50.849548 if len(Germany_derived_virtual_selected_rows) == 0 else dff.loc[Germany_selected_row_ids[0]].lat
            longitude = 10.231292 if len(Germany_derived_virtual_selected_rows) == 0 else dff.loc[Germany_selected_row_ids[0]].lon
            zoom = 5 if len(Germany_derived_virtual_selected_rows) == 0 else 5

            fig2 = render_region_map(df_germany, dff, latitude, longitude, zoom)
           
        return fig2

@app.callback(
    Output('datatable-interact-lineplot', 'figure'),
    input_list
)
def update_lineplot(value, derived_virtual_selected_rows, selected_row_ids,
  Asia_derived_virtual_selected_rows,Asia_selected_row_ids,
  Oceania_derived_virtual_selected_rows,Oceania_selected_row_ids,
  NorthAmerica_derived_virtual_selected_rows,NorthAmerica_selected_row_ids,
  SouthAmerica_derived_virtual_selected_rows,SouthAmerica_selected_row_ids,
  Africa_derived_virtual_selected_rows,Africa_selected_row_ids,
  Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
  Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  CHN_derived_virtual_selected_rows, CHN_selected_row_ids,
  US_derived_virtual_selected_rows, US_selected_row_ids,  
  ):

    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      dff = WorldwildTable

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide' # Display the global total case number 

    elif value == 'Australia':
      if Australia_derived_virtual_selected_rows is None:
        Australia_derived_virtual_selected_rows = []

      dff = AustraliaTable
      if Australia_selected_row_ids:
        Region = Australia_selected_row_ids[0]
      else:
        Region = 'Australia'

    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      dff = BrazilTable
      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'

    elif value == 'Canada':
      if Canada_derived_virtual_selected_rows is None:
        Canada_derived_virtual_selected_rows = []

      dff = CanadaTable
      if Canada_selected_row_ids:
        Region = Canada_selected_row_ids[0]
      else:
        Region = 'Canada'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      dff = GermanyTable
      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Mainland China':
      if CHN_derived_virtual_selected_rows is None:
        CHN_derived_virtual_selected_rows = []

      dff = MainlandChinaTable
      if CHN_selected_row_ids:
        Region = CHN_selected_row_ids[0]
      else:
        Region = 'China'

    elif value == 'United States':
      if US_derived_virtual_selected_rows is None:
        US_derived_virtual_selected_rows = []

      dff = UnitedStatesTable
      if US_selected_row_ids:
        Region = US_selected_row_ids[0]
      else:
        Region = 'US'

    elif value == 'Europe':
      if Europe_derived_virtual_selected_rows is None:
        Europe_derived_virtual_selected_rows = []

      dff = table_dict['EuropeTable']
      if Europe_selected_row_ids:
        Region = Europe_selected_row_ids[0]
      else:
        Region = 'Europe' # Display the Europe total case number 

    elif value == 'Asia':
      if Asia_derived_virtual_selected_rows is None:
        Asia_derived_virtual_selected_rows = []

      dff = table_dict['AsiaTable']

      if Asia_selected_row_ids:
        if Asia_selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = Asia_selected_row_ids[0]
      else:
        Region = 'Asia'

    elif value == 'North America':
      if NorthAmerica_derived_virtual_selected_rows is None:
        NorthAmerica_derived_virtual_selected_rows = []

      dff = table_dict['NorthAmericaTable']
      if NorthAmerica_selected_row_ids:
        Region = NorthAmerica_selected_row_ids[0]
      else:
        Region = 'North America'

    elif value == 'South America':
      if SouthAmerica_derived_virtual_selected_rows is None:
        SouthAmerica_derived_virtual_selected_rows = []

      dff = table_dict['SouthAmericaTable']
      if SouthAmerica_selected_row_ids:
        Region = SouthAmerica_selected_row_ids[0]
      else:
        Region = 'South America'

    elif value == 'Oceania':
      if Oceania_derived_virtual_selected_rows is None:
        Oceania_derived_virtual_selected_rows = []

      dff = table_dict['OceaniaTable']
      if Oceania_selected_row_ids:
        Region = Oceania_selected_row_ids[0]
      else:
        Region = 'Oceania'

    elif value == 'Africa':
      if Africa_derived_virtual_selected_rows is None:
        Africa_derived_virtual_selected_rows = []

      dff = table_dict['AfricaTable']
      if Africa_selected_row_ids:
        Region = Africa_selected_row_ids[0]
      else:
        Region = 'Africa'  

    # Read cumulative data of a given region from ./cumulative_data folder
    df_region = pd.read_csv('./cumulative_data/{}.csv'.format(Region))
    df_region = df_region.astype(
      {'date_day': 'datetime64'})

    if dff is UnitedStatesTable or dff is CanadaTable:
      # Create empty figure canvas
      fig3 = go.Figure()
      # Add trace to the figure
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Confirmed'],
                             mode='lines+markers',
                             name='Confirmed case',
                             line=dict(color='#f03f42', width=2),
                             text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Confirmed<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Confirmed']],
                             hovertemplate=
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Recovered'],
                             mode='lines+markers',
                             name='Recovered case',
                             line=dict(color='#2ecc77', width=2),
                             text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Recovered<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Recovered']],
                             hovertemplate=
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Deaths'],
                             mode='lines+markers',
                             name='Death case',
                             line=dict(color='#7f7f7f', width=2),
                             text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Deaths<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Deaths']],
                             hovertemplate=
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      # Customise layout
      fig3.update_layout(
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),
        annotations=[
            dict(
                x=.5,
                y=.4,
                xref="paper",
                yref="paper",
                text=Region,
                opacity=0.5,
                font=dict(family='Roboto, sans-serif',
                          size=40,
                          color="grey"),
            )
        ],
        yaxis_title="Cumulative cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
        ),
        xaxis_title="Select a location from the table (Toggle the legend to see specific curves)",
        xaxis=dict(
            showline=False, linecolor='#272e3e',
            showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            zeroline=False
        ),
        xaxis_tickformat='%b %d',
        #transition = {'duration':500},
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=.02, y=1.15, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
      )

      return fig3
    else:
      # Create empty figure canvas
      fig3 = go.Figure()
      # Add trace to the figure
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Confirmed'],
                             mode='lines+markers',
                             name='Confirmed case',
                             line=dict(color='#f03f42', width=2),
                             text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Confirmed<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Confirmed']],
                             hovertemplate=
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Recovered'],
                             mode='lines+markers',
                             name='Recovered case',
                             line=dict(color='#2ecc77', width=2),
                             text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Recovered<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Recovered']],
                             hovertemplate=
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Deaths'],
                             mode='lines+markers',
                             name='Death case',
                             line=dict(color='#7f7f7f', width=2),
                             text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Deaths<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Deaths']],
                             hovertemplate=
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      # Customise layout
      fig3.update_layout(
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),
        annotations=[
            dict(
                x=.5,
                y=.4,
                xref="paper",
                yref="paper",
                text=Region,
                opacity=0.5,
                font=dict(family='Roboto, sans-serif',
                          size=40,
                          color="grey"),
            )
        ],
        yaxis_title="Cumulative case numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
        ),
        xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
        xaxis=dict(
            showline=False, linecolor='#272e3e',
            showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            zeroline=False
        ),
        xaxis_tickformat='%b %d',
        #transition = {'duration':500},
        hovermode='x unified',
        legend_orientation="h",
        legend=dict(x=.02, y=1.15, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
      )

      return fig3

@app.callback(
    Output('datatable-interact-dailyplot', 'figure'),
    input_list
)

def update_dailyplot(value, derived_virtual_selected_rows, selected_row_ids,
  Asia_derived_virtual_selected_rows,Asia_selected_row_ids,
  Oceania_derived_virtual_selected_rows,Oceania_selected_row_ids,
  NorthAmerica_derived_virtual_selected_rows,NorthAmerica_selected_row_ids,
  SouthAmerica_derived_virtual_selected_rows,SouthAmerica_selected_row_ids,
  Africa_derived_virtual_selected_rows,Africa_selected_row_ids,
  Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
  Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  CHN_derived_virtual_selected_rows, CHN_selected_row_ids,
  US_derived_virtual_selected_rows, US_selected_row_ids,  
  ):

    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      dff = WorldwildTable

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide' # Display the global total case number 

    elif value == 'Australia':
      if Australia_derived_virtual_selected_rows is None:
        Australia_derived_virtual_selected_rows = []

      dff = AustraliaTable
      if Australia_selected_row_ids:
        Region = Australia_selected_row_ids[0]
      else:
        Region = 'Australia'

    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      dff = BrazilTable
      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'

    elif value == 'Canada':
      if Canada_derived_virtual_selected_rows is None:
        Canada_derived_virtual_selected_rows = []

      dff = CanadaTable
      if Canada_selected_row_ids:
        Region = Canada_selected_row_ids[0]
      else:
        Region = 'Canada'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      dff = GermanyTable
      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Mainland China':
      if CHN_derived_virtual_selected_rows is None:
        CHN_derived_virtual_selected_rows = []

      dff = MainlandChinaTable
      if CHN_selected_row_ids:
        Region = CHN_selected_row_ids[0]
      else:
        Region = 'China'

    elif value == 'United States':
      if US_derived_virtual_selected_rows is None:
        US_derived_virtual_selected_rows = []

      dff = UnitedStatesTable
      if US_selected_row_ids:
        Region = US_selected_row_ids[0]
      else:
        Region = 'US'

    elif value == 'Europe':
      if Europe_derived_virtual_selected_rows is None:
        Europe_derived_virtual_selected_rows = []

      dff = table_dict['EuropeTable']
      if Europe_selected_row_ids:
        Region = Europe_selected_row_ids[0]
      else:
        Region = 'Europe' # Display the Europe total case number

    elif value == 'Asia':
      if Asia_derived_virtual_selected_rows is None:
        Asia_derived_virtual_selected_rows = []

      dff = table_dict['AsiaTable']
      if Asia_selected_row_ids:
        if Asia_selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = Asia_selected_row_ids[0]
      else:
        Region = 'Asia'

    elif value == 'North America':
      if NorthAmerica_derived_virtual_selected_rows is None:
        NorthAmerica_derived_virtual_selected_rows = []

      dff = table_dict['NorthAmericaTable']
      if NorthAmerica_selected_row_ids:
        Region = NorthAmerica_selected_row_ids[0]
      else:
        Region = 'North America'

    elif value == 'South America':
      if SouthAmerica_derived_virtual_selected_rows is None:
        SouthAmerica_derived_virtual_selected_rows = []

      dff = table_dict['SouthAmericaTable']
      if SouthAmerica_selected_row_ids:
        Region = SouthAmerica_selected_row_ids[0]
      else:
        Region = 'South America'

    elif value == 'Oceania':
      if Oceania_derived_virtual_selected_rows is None:
        Oceania_derived_virtual_selected_rows = []

      dff = table_dict['OceaniaTable']
      if Oceania_selected_row_ids:
        Region = Oceania_selected_row_ids[0]
      else:
        Region = 'Oceania'

    elif value == 'Africa':
      if Africa_derived_virtual_selected_rows is None:
        Africa_derived_virtual_selected_rows = []

      dff = table_dict['AfricaTable']
      if Africa_selected_row_ids:
        Region = Africa_selected_row_ids[0]
      else:
        Region = 'Africa' 

    # Read cumulative data of a given region from ./cumulative_data folder
    df_region = pd.read_csv('./cumulative_data/{}.csv'.format(Region))
    df_region = df_region.astype(
        {'date_day': 'datetime64'}
    )
    df_region = df_region.sort_values(by='date_day')
    df_region['rolling_mean'] = df_region['New'].rolling(7).mean()
    #df_region['rolling_mean'] = df_region['rolling_mean'].fillna(value=0)

    if dff is UnitedStatesTable or dff is CanadaTable:
        # Create empty figure canvas
        fig_daily = go.Figure()
        # Add trace to the figure
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily confirmed case',
                                line=dict(color='#f03f42', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily confirmed cases {:,d} <br>'.format(
                                  i) for i in df_region['New']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['rolling_mean'],
                                mode='lines',
                                line_shape='spline',
                                name='7-day rolling mean',
                                line=dict(color='#f03f42', width=2),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['7-day average confirmed cases {:.0f} <br>'.format(
                                  i) for i in df_region['rolling_mean']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New_recover'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily recovered case',
                                line=dict(color='#2ecc77', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily recovered cases {:,d} <br>'.format(
                                  i) for i in df_region['New_recover']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New_death'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily death case',
                                line=dict(color='#7f7f7f', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily death cases {:,d} <br>'.format(
                                  i) for i in df_region['New_death']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
      
        # Customise layout
        fig_daily.update_layout(
            margin=go.layout.Margin(
                l=10,
                r=10,
                b=10,
                t=5,
                pad=0
            ),
            annotations=[
                dict(
                    x=.5,
                    y=.4,
                    xref="paper",
                    yref="paper",
                    text=Region,
                    opacity=0.5,
                    font=dict(family='Roboto, sans-serif',
                        size=40,
                        color="grey"
                    ),
                )
            ],
            yaxis_title="Daily cases numbers",
            yaxis=dict(
                showline=False, linecolor='#272e3e',
                zeroline=False,
                gridcolor='rgba(203, 210, 211,.3)',
                gridwidth=.1,
                tickmode='array',
            ),
            xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
            xaxis=dict(
                showline=False, linecolor='#272e3e',
                showgrid=False,
                gridcolor='rgba(203, 210, 211,.3)',
                gridwidth=.1,
                zeroline=False
            ),
            xaxis_tickformat='%b %d',
            #transition = {'duration':500},
            hovermode='x unified',
            legend_orientation="h",
            legend=dict(x=.02, y=1.15, bgcolor="rgba(0,0,0,0)",),
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(color='#292929', size=10)
        )

        return fig_daily
    else:
        # Create empty figure canvas
        fig_daily = go.Figure()
        # Add trace to the figure
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily confirmed case',
                                line=dict(color='#f03f42', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily confirmed cases {:,d} <br>'.format(
                                  i) for i in df_region['New']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['rolling_mean'],
                                mode='lines',
                                line_shape='spline',
                                name='7-day rolling mean',
                                line=dict(color='#f03f42', width=2),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['7-day average confirmed cases {:.0f} <br>'.format(
                                  i) for i in df_region['rolling_mean']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New_recover'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily recovered case',
                                line=dict(color='#2ecc77', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily recovered cases {:,d} <br>'.format(
                                  i) for i in df_region['New_recover']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
        fig_daily.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New_death'],
                                fill='tozeroy',
                                mode='lines',
                                name='Daily death case',
                                line=dict(color='#7f7f7f', width=0),
                                text=[datetime.strftime(d, '%b %d %Y GMT+10')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily death cases {:,d} <br>'.format(
                                  i) for i in df_region['New_death']],
                                hovertemplate=
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
      
        # Customise layout
        fig_daily.update_layout(
            margin=go.layout.Margin(
                l=10,
                r=10,
                b=10,
                t=5,
                pad=0
            ),
            annotations=[
                dict(
                    x=.5,
                    y=.4,
                    xref="paper",
                    yref="paper",
                    text=Region,
                    opacity=0.5,
                    font=dict(family='Roboto, sans-serif',
                        size=40,
                        color="grey"
                    ),
                )
            ],
            yaxis_title="Daily case numbers",
            yaxis=dict(
                showline=False, linecolor='#272e3e',
                zeroline=False,
                gridcolor='rgba(203, 210, 211,.3)',
                gridwidth=.1,
                tickmode='array',
            ),
            xaxis_title="Select a location from the table (Toggle the legend to see specific curve)",
            xaxis=dict(
                showline=False, linecolor='#272e3e',
                showgrid=False,
                gridcolor='rgba(203, 210, 211,.3)',
                gridwidth=.1,
                zeroline=False
            ),
            xaxis_tickformat='%b %d',
            #transition = {'duration':500},
            hovermode='x unified',
            legend_orientation="h",
            legend=dict(x=.02, y=1.15, bgcolor="rgba(0,0,0,0)",),
            plot_bgcolor='#ffffff',
            paper_bgcolor='#ffffff',
            font=dict(color='#292929', size=10)
            )

        return fig_daily

@app.callback(
    Output('datatable-interact-logplot', 'figure'),
    input_list
)
def update_logplot(value, derived_virtual_selected_rows, selected_row_ids,
  Asia_derived_virtual_selected_rows,Asia_selected_row_ids,
  Oceania_derived_virtual_selected_rows,Oceania_selected_row_ids,
  NorthAmerica_derived_virtual_selected_rows,NorthAmerica_selected_row_ids,
  SouthAmerica_derived_virtual_selected_rows,SouthAmerica_selected_row_ids,
  Africa_derived_virtual_selected_rows,Africa_selected_row_ids,
  Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
  Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  CHN_derived_virtual_selected_rows, CHN_selected_row_ids,
  US_derived_virtual_selected_rows, US_selected_row_ids,  
  ):
   
    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide'
    
    elif value == 'Australia':
      if Australia_derived_virtual_selected_rows is None:
        Australia_derived_virtual_selected_rows = []

      if Australia_selected_row_ids:
        Region = Australia_selected_row_ids[0]
      else:
        Region = 'Australia'

    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'

    elif value == 'Canada':
      if Canada_derived_virtual_selected_rows is None:
        Canada_derived_virtual_selected_rows = []

      if Canada_selected_row_ids:
        Region = Canada_selected_row_ids[0]
      else:
        Region = 'Canada'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Mainland China':
      if CHN_derived_virtual_selected_rows is None:
        CHN_derived_virtual_selected_rows = []

      if CHN_selected_row_ids:
        Region = CHN_selected_row_ids[0]
      else:
        Region = 'China'

    elif value == 'United States':
      if US_derived_virtual_selected_rows is None:
        US_derived_virtual_selected_rows = []

      if US_selected_row_ids:
        Region = US_selected_row_ids[0]
      else:
        Region = 'US'

    elif value == 'Europe':
      if Europe_derived_virtual_selected_rows is None:
        Europe_derived_virtual_selected_rows = []

      if Europe_selected_row_ids:
        Region = Europe_selected_row_ids[0]
      else:
        Region = 'Europe'

    elif value == 'Asia':
      if Asia_derived_virtual_selected_rows is None:
        Asia_derived_virtual_selected_rows = []

      if Asia_selected_row_ids:
        if Asia_selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = Asia_selected_row_ids[0]
      else:
        Region = 'Asia'

    elif value == 'North America':
      if NorthAmerica_derived_virtual_selected_rows is None:
        NorthAmerica_derived_virtual_selected_rows = []

      if NorthAmerica_selected_row_ids:
        Region = NorthAmerica_selected_row_ids[0]
      else:
        Region = 'North America'

    elif value == 'South America':
      if SouthAmerica_derived_virtual_selected_rows is None:
        SouthAmerica_derived_virtual_selected_rows = []

      if SouthAmerica_selected_row_ids:
        Region = SouthAmerica_selected_row_ids[0]
      else:
        Region = 'South America'

    elif value == 'Oceania':
      if Oceania_derived_virtual_selected_rows is None:
        Oceania_derived_virtual_selected_rows = []

      if Oceania_selected_row_ids:
        Region = Oceania_selected_row_ids[0]
      else:
        Region = 'Oceania'

    elif value == 'Africa':
      if Africa_derived_virtual_selected_rows is None:
        Africa_derived_virtual_selected_rows = []

      if Africa_selected_row_ids:
        Region = Africa_selected_row_ids[0]
      else:
        Region = 'Africa'

    elapseDay = daysOutbreak
    # Create empty figure canvas
    fig_curve = go.Figure()

    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                       '85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
    )

    # Add trace to the figure
    if Region in set(dfs_curve['Region']):

        dotx = [np.array(dfs_curve.loc[dfs_curve['Region'] == Region,'DayElapsed'])[0]]
        doty = [np.array(dfs_curve.loc[dfs_curve['Region'] == Region,'Confirmed'])[0]]

        for regionName in ['Worldwide', 'Japan', 'Italy', 'India', 'US']:

          dotgrayx = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'DayElapsed'])[0]]
          dotgrayy = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'Confirmed'])[0]]


          fig_curve.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == regionName]['DayElapsed'],
                                         y=dfs_curve.loc[dfs_curve['Region'] == regionName]['Confirmed'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve.loc[dfs_curve['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days after 100 cases<br>' +
                                                       'with %{y:,d} cases in total<br>'
                                                       '<extra></extra>'
                             )
          )
          fig_curve.add_trace(go.Scatter(x=dotgrayx,
                                         y=dotgrayy,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days after 100 cases<br>' +
                                                       'with %{y:,d} cases in total<br>'
                                                       '<extra></extra>'
                            )
          )
          
        fig_curve.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == Region]['DayElapsed'],
                                       y=dfs_curve.loc[dfs_curve['Region'] == Region]['Confirmed'],
                                       mode='lines',
                                       line_shape='spline',
                                       name=Region,
                                       line=dict(color='#f03f42', width=3),
                                       text=[
                                           i for i in dfs_curve.loc[dfs_curve['Region'] == Region]['Region']],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '<br>%{x} days after 100 cases<br>' +
                                                     'with %{y:,d} cases in total<br>'
                                                     '<extra></extra>'
                            )
          )
        fig_curve.add_trace(go.Scatter(x=dotx,
                                       y=doty,
                                       mode='markers',
                                       marker=dict(size=7, color='#f03f42',
                                       line=dict(width=1, color='#f03f42')),
                                       text=[Region],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '<br>%{x} days after 100 cases<br>' +
                                                     'with %{y:,d} cases in total<br>'
                                                     '<extra></extra>'
                            )
        )

    else:
        for regionName in ['Worldwide', 'Japan', 'Italy', 'India', 'US']:

          dotgrayx = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'DayElapsed'])[0]]
          dotgrayy = [np.array(dfs_curve.loc[dfs_curve['Region'] == regionName, 'Confirmed'])[0]]

          fig_curve.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == regionName]['DayElapsed'],
                                         y=dfs_curve.loc[dfs_curve['Region'] == regionName]['Confirmed'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve.loc[dfs_curve['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days after 100 cases<br>' +
                                                       'with %{y:,d} cases in total<br>'
                                                       '<extra></extra>'
                             )
          )

          fig_curve.add_trace(go.Scatter(x=dotgrayx,
                                         y=dotgrayy,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days after 100 cases<br>' +
                                                       'with %{y:,d} cases in total<br>'
                                                       '<extra></extra>'
                            )
          )

    # Customise layout
    fig_curve.update_xaxes(range=[0, elapseDay-19])
    fig_curve.update_yaxes(range=[1.9, 7])
    fig_curve.update_layout(
        xaxis_title="Number of day since 100th confirmed cases",
        yaxis_title="Confirmed cases (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        annotations=[
            dict(
                x=.5,
                y=.4,
                xref="paper",
                yref="paper",
                text=Region if Region in set(dfs_curve['Region']) else "Not over 100 cases",
                opacity=0.5,
                font=dict(family='Roboto, sans-serif',
                          size=40,
                          color="grey"),
            )
        ],
        yaxis_type="log",
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        transition = {'duration':500},
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

    return fig_curve

@app.callback(
    Output('datatable-interact-deathplot', 'figure'),
    input_list
)
def update_deathplot(value, derived_virtual_selected_rows, selected_row_ids,
  Asia_derived_virtual_selected_rows,Asia_selected_row_ids,
  Oceania_derived_virtual_selected_rows,Oceania_selected_row_ids,
  NorthAmerica_derived_virtual_selected_rows,NorthAmerica_selected_row_ids,
  SouthAmerica_derived_virtual_selected_rows,SouthAmerica_selected_row_ids,
  Africa_derived_virtual_selected_rows,Africa_selected_row_ids,
  Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
  Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
  Brazil_derived_virtual_selected_rows, Brazil_selected_row_ids,
  Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
  Germany_derived_virtual_selected_rows, Germany_selected_row_ids,
  CHN_derived_virtual_selected_rows, CHN_selected_row_ids,
  US_derived_virtual_selected_rows, US_selected_row_ids,  
  ):
   
    if value == 'Worldwide':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      if selected_row_ids:
        if selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = selected_row_ids[0]
      else:
        Region = 'Worldwide'
    
    elif value == 'Australia':
      if Australia_derived_virtual_selected_rows is None:
        Australia_derived_virtual_selected_rows = []

      if Australia_selected_row_ids:
        Region = Australia_selected_row_ids[0]
      else:
        Region = 'Australia'

    elif value == 'Brazil':
      if Brazil_derived_virtual_selected_rows is None:
        Brazil_derived_virtual_selected_rows = []

      if Brazil_selected_row_ids:
        Region = Brazil_selected_row_ids[0]
      else:
        Region = 'Brazil'

    elif value == 'Canada':
      if Canada_derived_virtual_selected_rows is None:
        Canada_derived_virtual_selected_rows = []

      if Canada_selected_row_ids:
        Region = Canada_selected_row_ids[0]
      else:
        Region = 'Canada'

    elif value == 'Germany':
      if Germany_derived_virtual_selected_rows is None:
        Germany_derived_virtual_selected_rows = []

      if Germany_selected_row_ids:
        Region = Germany_selected_row_ids[0]
      else:
        Region = 'Germany'

    elif value == 'Mainland China':
      if CHN_derived_virtual_selected_rows is None:
        CHN_derived_virtual_selected_rows = []

      if CHN_selected_row_ids:
        Region = CHN_selected_row_ids[0]
      else:
        Region = 'China'

    elif value == 'United States':
      if US_derived_virtual_selected_rows is None:
        US_derived_virtual_selected_rows = []

      if US_selected_row_ids:
        Region = US_selected_row_ids[0]
      else:
        Region = 'US'

    elif value == 'Europe':
      if Europe_derived_virtual_selected_rows is None:
        Europe_derived_virtual_selected_rows = []

      if Europe_selected_row_ids:
        Region = Europe_selected_row_ids[0]
      else:
        Region = 'Europe'

    elif value == 'Asia':
      if Asia_derived_virtual_selected_rows is None:
        Asia_derived_virtual_selected_rows = []

      if Asia_selected_row_ids:
        if Asia_selected_row_ids[0] == 'Mainland China':
          Region = 'China'
        else:
          Region = Asia_selected_row_ids[0]
      else:
        Region = 'Asia'

    elif value == 'North America':
      if NorthAmerica_derived_virtual_selected_rows is None:
        NorthAmerica_derived_virtual_selected_rows = []

      if NorthAmerica_selected_row_ids:
        Region = NorthAmerica_selected_row_ids[0]
      else:
        Region = 'North America'

    elif value == 'South America':
      if SouthAmerica_derived_virtual_selected_rows is None:
        SouthAmerica_derived_virtual_selected_rows = []

      if SouthAmerica_selected_row_ids:
        Region = SouthAmerica_selected_row_ids[0]
      else:
        Region = 'South America'

    elif value == 'Oceania':
      if Oceania_derived_virtual_selected_rows is None:
        Oceania_derived_virtual_selected_rows = []

      if Oceania_selected_row_ids:
        Region = Oceania_selected_row_ids[0]
      else:
        Region = 'Oceania'

    elif value == 'Africa':
      if Africa_derived_virtual_selected_rows is None:
        Africa_derived_virtual_selected_rows = []

      if Africa_selected_row_ids:
        Region = Africa_selected_row_ids[0]
      else:
        Region = 'Africa'

    elapseDay = daysOutbreak
    # Create empty figure canvas
    fig_curve_death = go.Figure()

    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                       '85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 1.1 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 2.3 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 5 days<br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve_death.add_trace(go.Scatter(x=pseduoDay,
                                   y=z4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 'Doubles every 14.2 days<br>' +
                                                 '<extra></extra>'
                            )
    )

    # Add trace to the figure
    if Region in set(dfs_curve_death['Region']):

        dotx_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == Region,'DayElapsed_death'])[0]]
        doty_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == Region,'Deaths'])[0]]

        for regionName in ['Worldwide', 'Japan', 'Italy', 'India', 'US']:

          dotgrayx_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'DayElapsed_death'])[0]]
          dotgrayy_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'Deaths'])[0]]


          fig_curve_death.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['DayElapsed_death'],
                                         y=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Deaths'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days since 3rd death cases<br>' +
                                                       'with %{y:,d} death cases in total<br>'
                                                       '<extra></extra>'
                             )
          )
          fig_curve_death.add_trace(go.Scatter(x=dotgrayx_death,
                                         y=dotgrayy_death,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days since 3rd death cases<br>' +
                                                       'with %{y:,d} death cases in total<br>'
                                                       '<extra></extra>'
                            )
          )
          
        fig_curve_death.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == Region]['DayElapsed_death'],
                                       y=dfs_curve_death.loc[dfs_curve_death['Region'] == Region]['Deaths'],
                                       mode='lines',
                                       line_shape='spline',
                                       name=Region,
                                       line=dict(color='#7f7f7f', width=3),
                                       text=[
                                           i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == Region]['Region']],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '<br>%{x} days since 3rd death cases<br>' +
                                                     'with %{y:,d} death cases in total<br>'
                                                     '<extra></extra>'
                            )
          )
        fig_curve_death.add_trace(go.Scatter(x=dotx_death,
                                       y=doty_death,
                                       mode='markers',
                                       marker=dict(size=7, color='#7f7f7f',
                                       line=dict(width=1, color='#7f7f7f')),
                                       text=[Region],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '<br>%{x} days since 3rd death cases<br>' +
                                                     'with %{y:,d} death cases in total<br>'
                                                     '<extra></extra>'
                            )
        )

    else:
        for regionName in ['Worldwide', 'Japan', 'Italy', 'India', 'US']:

          dotgrayx_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'DayElapsed_death'])[0]]
          dotgrayy_death = [np.array(dfs_curve_death.loc[dfs_curve_death['Region'] == regionName, 'Deaths'])[0]]

          fig_curve_death.add_trace(go.Scatter(x=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['DayElapsed_death'],
                                         y=dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Deaths'],
                                         mode='lines',
                                         line_shape='spline',
                                         name=regionName,
                                         opacity=0.3,
                                         line=dict(color='#636363', width=1.5),
                                         text=[
                                            i for i in dfs_curve_death.loc[dfs_curve_death['Region'] == regionName]['Region']],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days since 3rd death cases<br>' +
                                                       'with %{y:,d} death cases in total<br>'
                                                       '<extra></extra>'
                             )
          )

          fig_curve_death.add_trace(go.Scatter(x=dotgrayx_death,
                                         y=dotgrayy_death,
                                         mode='markers',
                                         marker=dict(size=6, color='#636363',
                                         line=dict(width=1, color='#636363')),
                                         opacity=0.5,
                                         text=[regionName],
                                         hovertemplate='<b>%{text}</b><br>' +
                                                       '<br>%{x} days since 3rd death cases<br>' +
                                                       'with %{y:,d} death cases in total<br>'
                                                       '<extra></extra>'
                            )
          )

    # Customise layout
    fig_curve_death.update_xaxes(range=[0, elapseDay-19])
    fig_curve_death.update_yaxes(range=[0.477, 5.5])
    fig_curve_death.update_layout(
        xaxis_title="Number of days since 3 deaths recorded",
        yaxis_title="Death cases (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        annotations=[dict(
            x=.5,
            y=.4,
            xref="paper",
            yref="paper",
            text=Region if Region in set(dfs_curve['Region']) else "Not over 3 death cases",
            opacity=0.5,
            font=dict(family='Roboto, sans-serif',
                          size=40,
                          color="grey"),
                    )
        ],
        yaxis_type="log",
        yaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            zeroline=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
        ),
        xaxis=dict(
            showline=False, 
            linecolor='#272e3e',
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth = .1,
            zeroline=False
        ),
        showlegend=False,
        # hovermode = 'x unified',
        transition = {'duration':500},
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

    return fig_curve_death



if __name__ == "__main__":
    app.run_server(debug=True)

