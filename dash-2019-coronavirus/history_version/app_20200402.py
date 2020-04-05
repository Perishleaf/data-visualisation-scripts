# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math
import os
import base64

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

###################################
# Private function
###################################

def make_country_table(countryName):
    '''This is the function for building df for Province/State of a given country'''
    countryTable = df_latest.loc[df_latest['Country/Region'] == countryName]
    # Suppress SettingWithCopyWarning
    pd.options.mode.chained_assignment = None
    countryTable['Active'] = countryTable['Confirmed'] - countryTable['Recovered'] - countryTable['Deaths']
    countryTable['Death rate'] = countryTable['Deaths']/countryTable['Confirmed']
    countryTable['Confirmed/100k'] = ((countryTable['Confirmed']/countryTable['Population'])*100000).round()
    countryTable = countryTable[['Province/State', 'Active', 'Confirmed', 'Recovered', 'Deaths', 'Death rate', 'Confirmed/100k', 'lat', 'lon']]
    countryTable = countryTable.sort_values(
        by=['Active', 'Confirmed'], ascending=False).reset_index(drop=True)
    # Set row ids pass to selected_row_ids
    countryTable['id'] = countryTable['Province/State']
    countryTable.set_index('id', inplace=True, drop=False)
    # Turn on SettingWithCopyWarning
    pd.options.mode.chained_assignment = 'warn'
    return countryTable

def make_europe_table(europe_list):
  '''This is the function for building df for Europe countries'''
  europe_table = df_latest.loc[df_latest['Country/Region'].isin(europe_list)]
  # Suppress SettingWithCopyWarning
  pd.options.mode.chained_assignment = None
  europe_table['Active'] = europe_table['Confirmed'] - europe_table['Recovered'] - europe_table['Deaths']
  europe_table['Death rate'] = europe_table['Deaths']/europe_table['Confirmed']
  europe_table['Confirmed/100k'] = ((europe_table['Confirmed']/europe_table['Population'])*100000).round()
  europe_table = europe_table[['Country/Region', 'Active', 'Confirmed', 'Recovered', 'Deaths', 'Death rate', 'Confirmed/100k', 'lat', 'lon']]
  europe_table = europe_table.sort_values(
        by=['Active', 'Confirmed'], ascending=False).reset_index(drop=True)
  # Set row ids pass to selected_row_ids
  europe_table['id'] = europe_table['Country/Region']
  europe_table.set_index('id', inplace=True, drop=False)
  # Turn on SettingWithCopyWarning
  pd.options.mode.chained_assignment = 'warn'
  return europe_table

def make_dcc_country_tab(countryName, dataframe):
    '''This is for generating tab component for country table'''

    if countryName == 'United States' or countryName == 'Canada':
      return dcc.Tab(
               id='tab-datatable-interact-location-{}'.format(countryName) if countryName == 'Canada' else 'tab-datatable-interact-location-US',
               label=countryName,
               value=countryName,
               className='custom-tab',
               selected_className='custom-tab--selected',
               children=[dash_table.DataTable(
                    id='datatable-interact-location-{}'.format(countryName),
                    # Don't show coordinates
                    columns=[{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                             if i == 'Death rate' else {"name": i, "id": i}
                             for i in dataframe.columns[0:7]],
                    # But still store coordinates in the table for interactivity
                    data=dataframe.to_dict("rows"),
                    row_selectable="single" if countryName != 'Schengen' else False,
                    sort_action="native",
                    style_as_list_view=True,
                    style_cell={'font_family': 'Arial',
                                'font_size': '1.1rem',
                                'padding': '.1rem',
                                'backgroundColor': '#ffffff', },
                    fixed_rows={'headers': True, 'data': 0},
                    style_table={'minHeight': '800px',
                                 'height': '800px',
                                 'maxHeight': '800px',
                                 #'overflowX': 'scroll',
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
                                            {'if': {'column_id': 'Active'}, 'color':'#e36209'},
                                            {'if': {'column_id': 'Confirmed'}, 'color': '#d7191c'},
                                            {'if': {'column_id': 'Recovered'}, 'color': '#1a9622'},
                                            {'if': {'column_id': 'Deaths'}, 'color': '#6c6c6c'},
                                            {'textAlign': 'center'}],
                        ),
            ]
          )
    else:
      return dcc.Tab(
               id='tab-datatable-interact-location-{}'.format(countryName),
               label=countryName,
               value=countryName,
               className='custom-tab',
               selected_className='custom-tab--selected',
               children=[dash_table.DataTable(
                    id='datatable-interact-location-{}'.format(countryName),
                    # Don't show coordinates
                    columns=[{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                             if i == 'Death rate' else {"name": i, "id": i}
                             for i in dataframe.columns[0:7]],
                    # But still store coordinates in the table for interactivity
                    data=dataframe.to_dict("rows"),
                    row_selectable="single" if countryName != 'Schengen' else False,
                    sort_action="native",
                    style_as_list_view=True,
                    style_cell={'font_family': 'Arial',
                                  'font_size': '1.1rem',
                                  'padding': '.1rem',
                                  'backgroundColor': '#ffffff', },
                    fixed_rows={'headers': True, 'data': 0},
                    style_table={'minHeight': '800px',
                                 'height': '800px',
                                 'maxHeight': '800px',
                                 #'overflowX': 'scroll',
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
                                            {'if': {'column_id': 'Active'}, 'color':'#e36209'},
                                            {'if': {'column_id': 'Confirmed'}, 'color': '#d7191c'},
                                            {'if': {'column_id': 'Recovered'}, 'color': '#1a9622'},
                                            {'if': {'column_id': 'Deaths'}, 'color': '#6c6c6c'},
                                            {'textAlign': 'center'}],
                        ),
            ]
          )



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

# dfs = {sheet_name: pd.read_csv('./raw_data/{}.csv'.format(sheet_name))
#          for sheet_name in sheet_name}

# Method #2
# Import xls file and store each sheet in to a df list
# xl_file = pd.ExcelFile('./data.xls')

# dfs = {sheet_name: xl_file.parse(sheet_name)
#          for sheet_name in xl_file.sheet_names}

# Data from each sheet can be accessed via key
# keyList = list(dfs.keys())

# Data cleansing
# for key, df in dfs.items():
#    dfs[key].loc[:,'Confirmed'].fillna(value=0, inplace=True)
#    dfs[key].loc[:,'Deaths'].fillna(value=0, inplace=True)
#    dfs[key].loc[:,'Recovered'].fillna(value=0, inplace=True)
#    dfs[key]=dfs[key].astype({'Confirmed':'int64', 'Deaths':'int64', 'Recovered':'int64'})
#    # Change as China for coordinate search
#    dfs[key]=dfs[key].replace({'Country/Region':'Mainland China'}, 'China')
#    # Add a zero to the date so can be convert by datetime.strptime as 0-padded date
#    dfs[key]['Last Update'] = '0' + dfs[key]['Last Update']
#    # Convert time as Australian eastern daylight time
#    dfs[key]['Date_last_updated_AEDT'] = [datetime.strptime(d, '%m/%d/%Y %H:%M') for d in dfs[key]['Last Update']]
#    dfs[key]['Date_last_updated_AEDT'] = dfs[key]['Date_last_updated_AEDT'] + timedelta(hours=16)
#   #dfs[key]['Active'] = dfs[key]['Confirmed'] - dfs[key]['Recovered'] - dfs[key]['Deaths']

# Add coordinates for each area in the list for the latest table sheet
# To save time, coordinates calling was done seperately
# Import the data with coordinates
df_latest = pd.read_csv('{}_data.csv'.format(sheet_name[0]))
df_latest = df_latest.astype({'Date_last_updated_AEDT': 'datetime64'})

# Save numbers into variables to use in the app
confirmedCases = df_latest['Confirmed'].sum()
deathsCases = df_latest['Deaths'].sum()
recoveredCases = df_latest['Recovered'].sum()

# Construct confirmed cases dataframe for line plot and 24-hour window case difference
df_confirmed = pd.read_csv('./lineplot_data/df_confirmed.csv')
df_confirmed = df_confirmed.astype({'Date': 'datetime64'})
plusConfirmedNum = df_confirmed['plusNum'][0]
plusPercentNum1 = df_confirmed['plusPercentNum'][0]

# Construct recovered cases dataframe for line plot and 24-hour window case difference
df_recovered = pd.read_csv('./lineplot_data/df_recovered.csv')
df_recovered = df_recovered.astype({'Date': 'datetime64'})
plusRecoveredNum = df_recovered['plusNum'][0]
plusPercentNum2 = df_recovered['plusPercentNum'][0]

# Construct death case dataframe for line plot and 24-hour window case difference
df_deaths = pd.read_csv('./lineplot_data/df_deaths.csv')
df_deaths = df_deaths.astype({'Date': 'datetime64'})
plusDeathNum = df_deaths['plusNum'][0]
plusPercentNum3 = df_deaths['plusPercentNum'][0]

# Construct remaining case dataframe for line plot and 24-hour window case difference
df_remaining = pd.read_csv('./lineplot_data/df_remaining.csv')
df_remaining = df_remaining.astype({'Date': 'datetime64'})
plusRemainNum = df_remaining['plusNum'][0]
plusRemainNum3 = df_remaining['plusPercentNum'][0]

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
dfSum = pd.merge(dfCase, dfGPS, how='inner', on='Country/Region')
dfSum = dfSum.replace({'Country/Region': 'China'}, 'Mainland China')
dfSum['Active'] = dfSum['Confirmed'] - dfSum['Recovered'] - dfSum['Deaths']
dfSum['Death rate'] = dfSum['Deaths']/dfSum['Confirmed']
dfSum['Confirmed/100k'] = ((dfSum['Confirmed']/dfSum['Population'])*100000).round()
# Rearrange columns to correspond to the number plate order
dfSum = dfSum[['Country/Region', 'Active',
    'Confirmed', 'Recovered', 'Deaths', 'Death rate', 'Confirmed/100k', 'lat', 'lon']]
# Sort value based on Active cases and then Confirmed cases
dfSum = dfSum.sort_values(
    by=['Active', 'Confirmed'], ascending=False).reset_index(drop=True)
# Set row ids pass to selected_row_ids
dfSum['id'] = dfSum['Country/Region']
dfSum.set_index('id', inplace=True, drop=False)

# Create tables for tabs
CNTable = make_country_table('China')
AUSTable = make_country_table('Australia')
USTable = make_country_table('US')
CANTable = make_country_table('Canada')

europe_list = ['Austria', 'Belgium', 'Czechia', 'Denmark', 'Estonia',
                  'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
                  'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
                  'Malta', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Slovakia',
                  'Slovenia', 'Spain', 'Sweden', 'Switzerland']
EuroTable = make_europe_table(europe_list)

# Remove dummy row of recovered case number in USTable
#USTable = USTable.dropna(subset=['Province/State'])

# Remove dummy row of recovered case number in USTable
#CANTable = CANTable.dropna(subset=['Province/State'])

# Save numbers into variables to use in the app
latestDate = datetime.strftime(df_confirmed['Date'][0], '%b %d, %Y %H:%M GMT+11')
secondLastDate = datetime.strftime(df_confirmed['Date'][1], '%b %d')
daysOutbreak = (df_confirmed['Date'][0] - datetime.strptime('12/31/2019', '%m/%d/%Y')).days

# Read cumulative data of a given region from ./cumulative_data folder
dfs_curve = pd.read_csv('./lineplot_data/dfs_curve.csv')

# Pseduo data for logplot
pseduoDay = np.arange(1, daysOutbreak+1)
y1 = 100*(1.85)**(pseduoDay-1)  # 85% growth rate
y2 = 100*(1.35)**(pseduoDay-1)  # 35% growth rate
y3 = 100*(1.15)**(pseduoDay-1)  # 15% growth rate
y4 = 100*(1.05)**(pseduoDay-1)  # 5% growth rate

#############################################################################################
# Start to make plots
#############################################################################################
# Line plot for confirmed cases
# Set up tick scale based on confirmed case number
#tickList = np.arange(0, df_confirmed['Other locations'].max()+5000, 30000)

# Create empty figure canvas
fig_confirmed = go.Figure()
# Add trace to the figure
fig_confirmed.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Mainland China'],
                                   mode='lines+markers',
                                   line_shape='spline',
                                   name='Mainland China',
                                   line=dict(color='#921113', width=4),
                                   marker=dict(size=4, color='#f4f4f2',
                                               line=dict(width=1, color='#921113')),
                                   text=[datetime.strftime(
                                       d, '%b %d %Y AEDT') for d in df_confirmed['Date']],
                                   hovertext=['Mainland China confirmed<br>{:,d} cases<br>'.format(
                                       i) for i in df_confirmed['Mainland China']],
                                   hovertemplate='<b>%{text}</b><br></br>' +
                                                 '%{hovertext}' +
                                                 '<extra></extra>'))
fig_confirmed.add_trace(go.Scatter(x=df_confirmed['Date'], y=df_confirmed['Other locations'],
                                   mode='lines+markers',
                                   line_shape='spline',
                                   name='Other Region',
                                   line=dict(color='#eb5254', width=4),
                                   marker=dict(size=4, color='#f4f4f2',
                                               line=dict(width=1, color='#eb5254')),
                                   text=[datetime.strftime(
                                       d, '%b %d %Y AEDT') for d in df_confirmed['Date']],
                                   hovertext=['Other region confirmed<br>{:,d} cases<br>'.format(
                                       i) for i in df_confirmed['Other locations']],
                                   hovertemplate='<b>%{text}</b><br></br>' +
                                                 '%{hovertext}' +
                                                 '<extra></extra>'))
# Customise layout
fig_confirmed.update_layout(
#    title=dict(
#    text="<b>Confirmed Cases Timeline<b>",
#    y=0.96, x=0.5, xanchor='center', yanchor='top',
#    font=dict(size=20, color="#292929", family="Playfair Display")
#   ),
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
        #tickmode='array',
        # Set tick range based on the maximum number
        #tickvals=tickList,
        # Set tick label accordingly
        #ticktext=["{:.0f}k".format(i/1000) for i in tickList]
    ),
#   yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=False, linecolor='#272e3e',
        showgrid=False,
        gridcolor='rgba(203, 210, 211,.3)',
        gridwidth=.1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode='x',
    legend_orientation="h",
#   legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)

# Line plot for combine recovered cases
# Set up tick scale based on total recovered case number
#tickList = np.arange(0, df_remaining['Total'].max()+10000, 30000)

# Create empty figure canvas
fig_combine = go.Figure()
# Add trace to the figure
fig_combine.add_trace(go.Scatter(x=df_recovered['Date'], y=df_recovered['Total'],
                                   mode='lines+markers',
                                   line_shape='spline',
                                   name='Total Recovered Cases',
                                   line=dict(color='#168038', width=4),
                                   marker=dict(size=4, color='#f4f4f2',
                                               line=dict(width=1, color='#168038')),
                                   text=[datetime.strftime(
                                       d, '%b %d %Y AEDT') for d in df_recovered['Date']],
                                   hovertext=['Total recovered<br>{:,d} cases<br>'.format(
                                       i) for i in df_recovered['Total']],
                                   hovertemplate='<b>%{text}</b><br></br>' +
                                                 '%{hovertext}' +
                                                 '<extra></extra>'))
fig_combine.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Total'],
                                mode='lines+markers',
                                line_shape='spline',
                                name='Total Death Cases',
                                line=dict(color='#626262', width=4),
                                marker=dict(size=4, color='#f4f4f2',
                                            line=dict(width=1, color='#626262')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y AEDT') for d in df_deaths['Date']],
                                hovertext=['Total death<br>{:,d} cases<br>'.format(
                                    i) for i in df_deaths['Total']],
                                hovertemplate='<b>%{text}</b><br></br>' +
                                              '%{hovertext}' +
                                              '<extra></extra>'))
fig_combine.add_trace(go.Scatter(x=df_remaining['Date'], y=df_remaining['Total'],
                                mode='lines+markers',
                                line_shape='spline',
                                name='Total Active Cases',
                                line=dict(color='#e36209', width=4),
                                marker=dict(size=4, color='#f4f4f2',
                                            line=dict(width=1, color='#e36209')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y AEDT') for d in df_deaths['Date']],
                                hovertext=['Total active<br>{:,d} cases<br>'.format(
                                    i) for i in df_remaining['Total']],
                                hovertemplate='<b>%{text}</b><br></br>' +
                                              '%{hovertext}' +
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
    hovermode='x',
    legend_orientation="h",
    # legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)

# Line plot for death rate cases
# Set up tick scale based on death case number of Mainland China
tickList = np.arange(0, (df_deaths['Other locations']/df_confirmed['Other locations']*100).max()+0.5, 0.5)

# Create empty figure canvas
fig_rate = go.Figure()
# Add trace to the figure
fig_rate.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Mainland China']/df_confirmed['Mainland China']*100,
                                mode='lines+markers',
                                line_shape='spline',
                                name='Mainland China',
                                line=dict(color='#626262', width=4),
                                marker=dict(size=4, color='#f4f4f2',
                                            line=dict(width=1, color='#626262')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y AEDT') for d in df_deaths['Date']],
                                hovertext=['Mainland China death rate<br>{:.2f}%'.format(
                                    i) for i in df_deaths['Mainland China']/df_confirmed['Mainland China']*100],
                                hovertemplate='<b>%{text}</b><br></br>' +
                                              '%{hovertext}' +
                                              '<extra></extra>'))
fig_rate.add_trace(go.Scatter(x=df_deaths['Date'], y=df_deaths['Other locations']/df_confirmed['Other locations']*100,
                                mode='lines+markers',
                                line_shape='spline',
                                name='Other Region',
                                line=dict(color='#a7a7a7', width=4),
                                marker=dict(size=4, color='#f4f4f2',
                                            line=dict(width=1, color='#a7a7a7')),
                                text=[datetime.strftime(
                                    d, '%b %d %Y AEDT') for d in df_deaths['Date']],
                                hovertext=['Other region death rate<br>{:.2f}%'.format(
                                    i) for i in df_deaths['Other locations']/df_confirmed['Other locations']*100],
                                hovertemplate='<b>%{text}</b><br></br>' +
                                              '%{hovertext}' +
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
        tickvals=tickList,
        # Set tick label accordingly
        ticktext=['{:.1f}'.format(i) for i in tickList]
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
    hovermode='x',
    legend_orientation="h",
    # legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
    plot_bgcolor='#ffffff',
    paper_bgcolor='#ffffff',
    font=dict(color='#292929', size=10)
)

# Default cumulative plot for tab
# Default plot is an empty canvas
#df_region_tab = pd.read_csv('./cumulative_data/{}.csv'.format('The World'))
#df_region_tab = df_region_tab.astype({'Date_last_updated_AEDT': 'datetime64', 'date_day': 'datetime64'})

# Create empty figure canvas
fig_cumulative_tab = go.Figure()
# Add trace to the figure
#fig_cumulative_tab.add_trace(go.Scatter(x=df_region_tab['date_day'],
#                                        y=df_region_tab['Confirmed'],
#                                        mode='lines+markers',
#                                        # line_shape='spline',
#                                        name='Confirmed case',
#                                        line=dict(color='#d7191c', width=2),
#                                        # marker=dict(size=4, color='#f4f4f2',
#                                        #            line=dict(width=1,color='#921113')),
#                                        text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_region_tab['date_day']],
#                                        hovertext=['{} Confirmed<br>{:,d} cases<br>'.format('The World', i) for i in df_region_tab['Confirmed']],
#                                        hovertemplate='<b>%{text}</b><br></br>' +
#                                                      '%{hovertext}' +
#                                                      '<extra></extra>'))
#fig_cumulative_tab.add_trace(go.Scatter(x=df_region_tab['date_day'],
#                                        y=df_region_tab['Recovered'],
#                                        mode='lines+markers',
#                                        # line_shape='spline',
#                                        name='Recovered case',
#                                        line=dict(color='#1a9622', width=2),
#                                        # marker=dict(size=4, color='#f4f4f2',
#                                        #            line=dict(width=1,color='#168038')),
#                                        text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_region_tab['date_day']],
#                                        hovertext=['{} Recovered<br>{:,d} cases<br>'.format('The World', i) for i in df_region_tab['Recovered']],
#                                        hovertemplate='<b>%{text}</b><br></br>' +
#                                                      '%{hovertext}' +
#                                                      '<extra></extra>'))
#fig_cumulative_tab.add_trace(go.Scatter(x=df_region_tab['date_day'],
#                                        y=df_region_tab['Deaths'],
#                                        mode='lines+markers',
#                                        # line_shape='spline',
#                                        name='Death case',
#                                        line=dict(color='#626262', width=2),
#                                        # marker=dict(size=4, color='#f4f4f2',
#                                        #            line=dict(width=1,color='#626262')),
#                                        text=[datetime.strftime(d, '%b %d %Y AEDT') for d in df_region_tab['date_day']],
#                                        hovertext=['{} Deaths<br>{:,d} cases<br>'.format('The World', i) for i in df_region_tab['Deaths']],
#                                        hovertemplate='<b>%{text}</b><br></br>' +
#                                                      '%{hovertext}' +
#                                                      '<extra></extra>'))
# Customise layout
fig_cumulative_tab.update_layout(
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
        ),
#        annotations=[
#            dict(
#                x=.5,
#                y=.4,
#                xref="paper",
#                yref="paper",
#                text='The World',
#                opacity=0.5,
#                font=dict(family='Arial, sans-serif',
#                          size=60,
#                          color="grey"),
#            )
#        ],
        yaxis_title="Cumulative cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
            # Set tick range based on the maximum number
            # tickvals=tickList,
            # Set tick label accordingly
            # ticktext=["{:.0f}k".format(i/1000) for i in tickList]
        ),
        xaxis_title="Select A Location From Table",
        xaxis=dict(
            showline=False, linecolor='#272e3e',
            showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            zeroline=False
        ),
        xaxis_tickformat='%b %d',
        # transition = {'duration':500},
        hovermode='x',
        legend_orientation="h",
        legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

# Default curve plot for tab
# Create empty figure canvas
fig_curve_tab = go.Figure()

fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
)
fig_curve_tab.add_trace(go.Scatter(x=pseduoDay,
                                   y=y4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=['5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
)
for regionName in ['The World', 'Japan', 'Italy', 'Turkey', 'US']:

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
        xaxis_title="Number of day since 100th confirmed cases",
        yaxis_title="Confirmed cases (Logarithmic)",
        margin=go.layout.Margin(
            l=10,
            r=10,
            b=10,
            t=5,
            pad=0
            ),
        #annotations=[dict(
        #    x=.5,
        #    y=.4,
        #    xref="paper",
        #    yref="paper",
        #    text=dfSum['Country/Region'][0] if dfSum['Country/Region'][0] in set(dfs_curve['Region']) else "Not over 100 cases",
        #    opacity=0.5,
        #    font=dict(family='Arial, sans-serif',
        #              size=60,
        #              color="grey"),
        #            )
        #],
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
        # hovermode = 'x',
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
                      As of {}, there are {:,d} cases of COVID-19 confirmed globally.\
                     In the meanwhile, please keep calm, stay home and wash your hand!".format(latestDate, confirmedCases)},
                    {"property": "og:title",
                        "content": "Coronavirus COVID-19 Outbreak Global Cases Monitor Dashboard"},
                    {"property": "og:type", "content": "website"},
                    {"property": "og:image", "content": "https://junye0798.com/post/build-a-dashboard-to-track-the-spread-of-coronavirus-using-dash/featured_hu031431b9019186307c923e911320563b_1304417_1200x0_resize_lanczos_2.png"},
                    {"property": "og:url",
                        "content": "https://dash-coronavirus-2020.herokuapp.com/"},
                    {"property": "og:description",
                        "content": "The coronavirus COVID-19 dashboard/monitor provides up-to-date data and map for the global spread of coronavirus.\
                      As of {}, there are {:,d} cases of COVID-19 confirmed globally.\
                     In the meanwhile, please keep calm, stay home and wash your hand!".format(latestDate, confirmedCases)},
                    {"name": "twitter:card", "content": "summary_large_image"},
                    {"name": "twitter:site", "content": "@perishleaf"},
                    {"name": "twitter:title",
                        "content": "Coronavirus COVID-19 Outbreak Global Cases Monitor Dashboard"},
                    {"name": "twitter:description",
                        "content": "The coronavirus COVID-19 dashboard/monitor provides up-to-date data and map for the global spread of coronavirus.\
                      As of {}, there are {:,d} cases of COVID-19 confirmed globally.\
                     In the meanwhile, please keep calm, stay home and wash your hand!".format(latestDate, confirmedCases)},
                    {"name": "twitter:image", "content": "https://junye0798.com/post/build-a-dashboard-to-track-the-spread-of-coronavirus-using-dash/featured_hu031431b9019186307c923e911320563b_1304417_1200x0_resize_lanczos_2.png"},
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

app.layout = html.Div(style={'backgroundColor': '#fafbfd'},
    children=[
        html.Div(style={'marginRight': '1.5%',},
            id="header",
            children=[
                html.H4(
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
                        Jan 30, 2020 and recognized it as a pandemic on Mar 11, 2020. As of {}, there are {:,d} cases of COVID-19 confirmed globally.
                        
                        This dash board is developed to visualise and track the recent reported 
                        cases on a hourly timescale.'''.format(latestDate, confirmedCases),
                      )
                    )
                ),
                html.Div(
                  id="header-button",
                  children=[
                      html.P(
                        id='time-stamp',
                        # style={'fontWeight':'bold'},
                        children="Last update: {}. (👷Safari user may experience issue in displaying tables, I am working on it.🔧)".format(latestDate)
                      ),
                      html.Div(
                        [dbc.Button("Disclaimer", id="open", color="link"),
                         dbc.Modal(
                          id="modal",
                          children=[dbc.ModalHeader("Disclaimer"),
                           dbc.ModalBody("This is the content of the modal"),
                           dbc.ModalFooter(
                            dbc.Button("Close", id="close", className="ml-auto")
                            ),
                          ],
                          
                         ),
                        ]
                       )
                  ],),                 

                html.Hr(style={'marginTop': '.5%'},),
                    ]
                ),
        html.Div(
            id="number-plate",
            style={'marginLeft': '1.5%',
                'marginRight': '1.5%', 'marginBottom': '.8%'},
                 children=[
                     #html.Hr(),
                     html.Div(
                         style={'width': '24.4%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                              children=[
                                  html.H3(style={'textAlign': 'center',
                                                 'fontWeight': 'bold', 'color': '#2674f6'},
                                               children=[
                                                   html.P(style={'color': '#ffffff', 'padding': '.5rem'},
                                                              children='xxxx xx xxx xxxx xxx xxxxx'),
                                                   '{}'.format(daysOutbreak),
                                               ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#2674f6', 'padding': '.1rem'},
                                               children="days since outbreak")
                                       ]),
                     html.Div(
                         style={'width': '24.4%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                              children=[
                                  html.H3(style={'textAlign': 'center',
                                                 'fontWeight': 'bold', 'color': '#d7191c'},
                                                children=[
                                                    html.P(style={'padding': '.5rem'},
                                                              children='+ {:,d} in the past 24h ({:.1%})'.format(plusConfirmedNum, plusPercentNum1)),
                                                    '{:,d}'.format(
                                                        confirmedCases)
                                                         ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#d7191c', 'padding': '.1rem'},
                                               children="confirmed cases")
                                       ]),
                     html.Div(
                         style={'width': '24.4%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                              children=[
                                  html.H3(style={'textAlign': 'center',
                                                       'fontWeight': 'bold', 'color': '#1a9622'},
                                               children=[
                                                   html.P(style={'padding': '.5rem'},
                                                              children='+ {:,d} in the past 24h ({:.1%})'.format(plusRecoveredNum, plusPercentNum2)),
                                                   '{:,d}'.format(
                                                       recoveredCases),
                                               ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#1a9622', 'padding': '.1rem'},
                                               children="recovered cases")
                                       ]),
                     html.Div(
                         style={'width': '24.4%', 'backgroundColor': '#ffffff', 'display': 'inline-block',
                                'verticalAlign': 'top', 
                                'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                              children=[
                                  html.H3(style={'textAlign': 'center',
                                                       'fontWeight': 'bold', 'color': '#6c6c6c'},
                                                children=[
                                                    html.P(style={'padding': '.5rem'},
                                                              children='+ {:,d} in the past 24h ({:.1%})'.format(plusDeathNum, plusPercentNum3)),
                                                    '{:,d}'.format(deathsCases)
                                                ]),
                                  html.H5(style={'textAlign': 'center', 'color': '#6c6c6c', 'padding': '.1rem'},
                                               children="death cases")
                                       ])
                          ]),
        html.Div(
            id='dcc-plot',
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'backgroundColor': '#ffffff',
                   'marginBottom': '.8%', 'marginTop': '.5%',
                   'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                },
                 children=[
                     html.Div(
                         style={'width': '32.79%', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top',
                                #'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                                },
                         children=[
                                  html.H5(
                                    style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                           'color': '#292929', 'padding': '1rem', 'marginBottom': '0','marginTop': '0'},
                                    children='Confirmed Case Timeline'),
                                  dcc.Graph(
                                    style={'height': '300px'}, 
                                    figure=fig_confirmed),
                                  ]),
                     html.Div(
                         style={'width': '32.79%', 'display': 'inline-block',
                                'marginRight': '.8%', 'verticalAlign': 'top',
                                #'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                                },
                         children=[
                                  html.H5(
                                    style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                           'color': '#292929', 'padding': '1rem', 'marginBottom': '0','marginTop': '0'},
                                    children='Active/Recovered/Death Case Timeline'),
                                  dcc.Graph(
                                    style={'height': '300px'}, 
                                    figure=fig_combine),
                                  ]),
                     html.Div(
                         style={'width': '32.79%', 'display': 'inline-block',
                                'verticalAlign': 'top',
                                #'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'
                                },
                         children=[
                                  html.H5(
                                    style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                           'color': '#292929', 'padding': '1rem', 'marginBottom': '0','marginTop': '0'},
                                    children='Death Rate (%) Timeline'),
                                  dcc.Graph(
                                    style={'height': '300px'}, 
                                    figure=fig_rate),
                                  ]),
                     ]),
        html.Div(
            id='dcc-map',
            style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '.5%'},
                 children=[
                     html.Div(style={'width': '61.31%', 'marginRight': '.8%', 'display': 'inline-block', 'verticalAlign': 'top',
                                     'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee',
                                     },
                              children=[
                                  html.H5(style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                                 'color': '#292929', 'padding': '1rem', 'marginBottom': '0', 'marginTop': '0'},
                                               children='Latest Coronavirus Outbreak Map'),
                                  dcc.Graph(
                                      id='datatable-interact-map',
                                      style={'height': '500px'},),
                                  dcc.Tabs(
                                      id="tabs-plots", 
                                      value='Cumulative Cases',
                                      parent_className='custom-tabs',
                                      className='custom-tabs-container', 
                                      children=[dcc.Tab(className='custom-tab',
                                                        selected_className='custom-tab--selected',
                                                        label='Cumulative Cases', 
                                                        value='Cumulative Cases'),
                                                dcc.Tab(className='custom-tab',
                                                        selected_className='custom-tab--selected',
                                                        label='Confirmed Case Trajectories', 
                                                        value='Confirmed Case Trajectories'),
                                      ]
                                  ),
                                  html.Div(id='tabs-content-plots'),
                              ]),
                     html.Div(style={'width': '37.89%', 'display': 'inline-block', 'verticalAlign': 'top',
                                     'box-shadow':'0px 0px 10px #ededee', 'border': '1px solid #ededee'},
                              children=[
                                  html.H5(style={'textAlign': 'center', 'backgroundColor': '#ffffff',
                                                 'color': '#292929', 'padding': '1rem', 'marginBottom': '0', 'marginTop': '0'},
                                               children='Cases Summary by Location'),
                                  dcc.Tabs(
                                      id="tabs-table",
                                      value='The World',
                                      parent_className='custom-tabs',
                                      className='custom-tabs-container',
                                      children=[
                                          dcc.Tab(label='The World',
                                              value='The World',
                                              className='custom-tab',
                                              selected_className='custom-tab--selected',
                                              children=[
                                                  dash_table.DataTable(
                                                      id='datatable-interact-location',
                                                      # Don't show coordinates
                                                      columns=[{"name": i, "id": i, "type": "numeric","format": FormatTemplate.percentage(2)}
                                                               if i == 'Death rate' else {"name": i, "id": i}
                                                               for i in dfSum.columns[0:7]],
                                                      # But still store coordinates in the table for interactivity
                                                      data=dfSum.to_dict(
                                                          "rows"),
                                                      row_selectable="single",
                                                      sort_action="native",
                                                      style_as_list_view=True,
                                                      style_cell={'font_family': 'Arial',
                                                                  'font_size': '1.1rem',
                                                                  'padding': '.1rem',
                                                                  'backgroundColor': '#ffffff', },
                                                      fixed_rows={
                                                          'headers': True, 'data': 0},
                                                      style_table={'minHeight': '800px',
                                                                   'height': '800px',
                                                                   'maxHeight': '800px',
                                                                   #'overflowX': 'scroll',
                                                                   },
                                                      style_header={'backgroundColor': '#ffffff',
                                                                    'fontWeight': 'bold'},
                                                      style_cell_conditional=[{'if': {
                                                                                  'column_id': 'Country/Regions'}, 'width': '20%'},
                                                                              {'if': {
                                                                                  'column_id': 'Active'}, 'width': '11%'},
                                                                              {'if': {
                                                                                  'column_id': 'Confirmed'}, 'width': '13.3%'},
                                                                              {'if': {
                                                                                  'column_id': 'Recovered'}, 'width': '13.3%'},
                                                                              {'if': {
                                                                                  'column_id': 'Deaths'}, 'width': '11%'},
                                                                              {'if': {
                                                                                  'column_id': 'Death rate'}, 'width': '13.3%'},
                                                                              {'if': {
                                                                                  'column_id': 'Confirmed/100k'}, 'width': '17.9%'},
                                                                              {'if': {
                                                                                  'column_id': 'Active'}, 'color':'#e36209'},
                                                                              {'if': {
                                                                                  'column_id': 'Confirmed'}, 'color': '#d7191c'},
                                                                              {'if': {
                                                                                  'column_id': 'Recovered'}, 'color': '#1a9622'},
                                                                              {'if': {
                                                                                  'column_id': 'Deaths'}, 'color': '#6c6c6c'},
                                                                              {'textAlign': 'center'}],
                                                  )
                                            ]),
                                          make_dcc_country_tab(
                                              'Australia', AUSTable),
                                          make_dcc_country_tab(
                                              'Canada', CANTable),
                                          make_dcc_country_tab(
                                               'Europe', EuroTable),
                                          make_dcc_country_tab(
                                              'Mainland China', CNTable),
                                          make_dcc_country_tab(
                                              'United States', USTable),
                                          ]
                                       )
                                    ]),
                                  dbc.Tooltip(
                                    target='tab-datatable-interact-location-Australia',
                                    style={"font-size":"1.5em"},
                                    children=dcc.Markdown(
                                      children=(
                                        '''
                                        Note that under _National Notifiable Diseases Surveillance
                                        System_ reporting requirements, cases are reported based on their Australian
                                        jurisdiction of residence rather than where they were detected.

                                        Additionally, the recovered cases in NSW, QLD, SA, TAS, NT are not actively reported.
                                        '''
                                        )
                                      )                                              
                                    ),
                                  dbc.Tooltip("Case data of Canada and the United States now provided by https://coronavirus.1point3acres.com/en",
                                              target='tab-datatable-interact-location-Canada',
                                              style={"font-size":"1.5em"},
                                             ),
                                  dbc.Tooltip("Case data of Canada and the United States now provided by https://coronavirus.1point3acres.com/en",
                                              target='tab-datatable-interact-location-US',
                                              style={"font-size":"1.5em"},
                                             ),
                                  dbc.Tooltip("This list comprises 26 European countries within Schengen Area.",
                                              target='tab-datatable-interact-location-Europe',
                                              style={"font-size":"1.5em"},
                                             ),
                              ]),
        html.Div(
          id='my-footer',
          style={'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginBottom': '1%', 'marginTop': '.5%'},
                 children=[
                     html.Hr(style={'marginBottom': '.5%'},),
                     html.P(style={'textAlign': 'center', 'margin': 'auto'},
                            children=['Keep calm and stay home | ',
                                      html.A('Developed by Jun with ❤️ in Sydney', href='https://junye0798.com/', target='_blank'), ' | ',
                                      html.A('About this dashboard', href='https://github.com/Perishleaf/data-visualisation-scripts/tree/master/dash-2019-coronavirus',target='_blank'), " | ",
                                      html.A('Report a bug', href='https://twitter.com/perishleaf', target='_blank'),
                                     ],
                            ),            
                     html.P(style={'textAlign': 'center', 'margin': 'auto', 'marginTop': '.5%'},
                            children=['Proudly supported by']
                      ),
                     html.P(style={'textAlign': 'center', 'margin': 'auto', 'marginTop': '.5%'},
                            children=[html.A(html.Img(style={'height' : '10%', 'width' : '10%',}, src=app.get_asset_url('TypeHuman.png')),
                            href='https://www.typehuman.com/', target='_blank')]
                      )
                  ]
              ),
        ])

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
    Output('datatable-interact-map', 'figure'),
    [Input('tabs-table', 'value'),
     Input('datatable-interact-location', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location', 'selected_row_ids'),
     Input('datatable-interact-location-Australia', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Australia', 'selected_row_ids'),
     Input('datatable-interact-location-Canada', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Canada', 'selected_row_ids'),
     Input('datatable-interact-location-Europe', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Europe', 'selected_row_ids'),
     Input('datatable-interact-location-Mainland China', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Mainland China', 'selected_row_ids'),
     Input('datatable-interact-location-United States', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-United States', 'selected_row_ids'),
     ]
)
def update_figures(value, derived_virtual_selected_rows, selected_row_ids, 
  Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
  Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
  Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
  CHN_derived_virtual_selected_rows, CHN_selected_row_ids,
  US_derived_virtual_selected_rows, US_selected_row_ids
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

    if value == 'The World':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      dff = dfSum
      latitude = 14.056159 if len(derived_virtual_selected_rows) == 0 else dff.loc[selected_row_ids[0]].lat
      longitude = 6.395626 if len(derived_virtual_selected_rows) == 0 else dff.loc[selected_row_ids[0]].lon
      zoom = 1.02 if len(derived_virtual_selected_rows) == 0 else 4
      hovertext_value = ['Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(i, j, k, t, q) 
                          for i, j, k, t, q in zip( df_latest['Confirmed'],  df_latest['Recovered'],  df_latest['Deaths'], df_latest['Deaths']/df_latest['Confirmed'], df_latest['Confirmed']*100000/df_latest['Population'])]

    elif value == 'Australia':
      if Australia_derived_virtual_selected_rows is None:
        Australia_derived_virtual_selected_rows = []

      dff = AUSTable
      latitude = -25.931850 if len(Australia_derived_virtual_selected_rows) == 0 else dff.loc[Australia_selected_row_ids[0]].lat
      longitude = 134.024931 if len(Australia_derived_virtual_selected_rows) == 0 else dff.loc[Australia_selected_row_ids[0]].lon
      zoom = 3 if len(Australia_derived_virtual_selected_rows) == 0 else 5
      hovertext_value = ['Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(i, j, k, t, q) 
                          for i, j, k, t, q in zip( df_latest['Confirmed'],  df_latest['Recovered'],  df_latest['Deaths'], df_latest['Deaths']/df_latest['Confirmed'], df_latest['Confirmed']*100000/df_latest['Population'])]

    elif value == 'Canada':
      if Canada_derived_virtual_selected_rows is None:
        Canada_derived_virtual_selected_rows = []

      dff = CANTable
      latitude = 55.474012 if len(Canada_derived_virtual_selected_rows) == 0 else dff.loc[Canada_selected_row_ids[0]].lat
      longitude = -97.344913 if len(Canada_derived_virtual_selected_rows) == 0 else dff.loc[Canada_selected_row_ids[0]].lon
      zoom = 3 if len(Canada_derived_virtual_selected_rows) == 0 else 5
      hovertext_value = ['Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(i, j, k, t, q) 
                          for i, j, k, t, q in zip( df_latest['Confirmed'],  df_latest['Recovered'],  df_latest['Deaths'], df_latest['Deaths']/df_latest['Confirmed'], df_latest['Confirmed']*100000/df_latest['Population'])]

    elif value == 'Mainland China':
      if CHN_derived_virtual_selected_rows is None:
        CHN_derived_virtual_selected_rows = []

      dff = CNTable
      latitude = 33.471197 if len(CHN_derived_virtual_selected_rows) == 0 else dff.loc[CHN_selected_row_ids[0]].lat
      longitude = 106.206780 if len(CHN_derived_virtual_selected_rows) == 0 else dff.loc[CHN_selected_row_ids[0]].lon
      zoom = 2.5 if len(CHN_derived_virtual_selected_rows) == 0 else 5
      hovertext_value = ['Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(i, j, k, t, q) 
                          for i, j, k, t, q in zip( df_latest['Confirmed'],  df_latest['Recovered'],  df_latest['Deaths'], df_latest['Deaths']/df_latest['Confirmed'], df_latest['Confirmed']*100000/df_latest['Population'])]

    elif value == 'United States':
      if US_derived_virtual_selected_rows is None:
        US_derived_virtual_selected_rows = []

      dff = USTable
      latitude = 40.022092 if len(US_derived_virtual_selected_rows) == 0 else dff.loc[US_selected_row_ids[0]].lat
      longitude = -98.828101 if len(US_derived_virtual_selected_rows) == 0 else dff.loc[US_selected_row_ids[0]].lon
      zoom = 3 if len(US_derived_virtual_selected_rows) == 0 else 5
      hovertext_value = ['Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(i, j, k, t, q) 
                          for i, j, k, t, q in zip( df_latest['Confirmed'],  df_latest['Recovered'],  df_latest['Deaths'], df_latest['Deaths']/df_latest['Confirmed'], df_latest['Confirmed']*100000/df_latest['Population'])]

    elif value == 'Europe':
      if Europe_derived_virtual_selected_rows is None:
        Europe_derived_virtual_selected_rows = []

      dff = EuroTable
      latitude = 52.405175 if len(Europe_derived_virtual_selected_rows) == 0 else dff.loc[Europe_selected_row_ids[0]].lat
      longitude = 11.403996 if len(Europe_derived_virtual_selected_rows) == 0 else dff.loc[Europe_selected_row_ids[0]].lon
      zoom = 2.5 if len(Europe_derived_virtual_selected_rows) == 0 else 5
      hovertext_value = ['Confirmed: {:,d}<br>Recovered: {:,d}<br>Death: {:,d}<br>Death rate: {:.2%}<br>Confirmed cases/100k population: {:.0f}'.format(i, j, k, t, q) 
                          for i, j, k, t, q in zip( df_latest['Confirmed'],  df_latest['Recovered'],  df_latest['Deaths'], df_latest['Deaths']/df_latest['Confirmed'], df_latest['Confirmed']*100000/df_latest['Population'])]

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
            color=['#d7191c' if i > 0 else '#1a9622' for i in colorList],
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
        transition={'duration': 50},
        annotations=[
        dict(
            x=.5,
            y=-.0,
            align='center',
            showarrow=False,
            text="Points are placed based on data geolocation levels.<br>Province/State level - Australia, China, Canada, and United States; Country level- other countries.",
            xref="paper",
            yref="paper",
            font=dict(size=10, color='#292929'),
        )],
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

@app.callback(Output('tabs-content-plots', 'children'),
              [Input('tabs-plots', 'value')])
def render_content(tab):
    if tab == 'Cumulative Cases':
        return dcc.Graph(id='datatable-interact-lineplot',
                         style={'height': '300px'},
                         figure=fig_cumulative_tab,)
    elif tab == 'Confirmed Case Trajectories':
        return dcc.Graph(id='datatable-interact-logplot',
                         style={'height': '300px'},
                         figure=fig_curve_tab,)

@app.callback(
    Output('datatable-interact-lineplot', 'figure'),
    [Input('tabs-table', 'value'),
     Input('datatable-interact-location', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location', 'selected_row_ids'),
     Input('datatable-interact-location-Australia', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Australia', 'selected_row_ids'),
     Input('datatable-interact-location-Canada', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Canada', 'selected_row_ids'),
     Input('datatable-interact-location-Europe', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Europe', 'selected_row_ids'),
     Input('datatable-interact-location-Mainland China', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Mainland China', 'selected_row_ids'),
     Input('datatable-interact-location-United States', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-United States', 'selected_row_ids'),
     ]
)
def update_lineplot(value, derived_virtual_selected_rows, selected_row_ids, 
  Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
  Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
  Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
  CHN_derived_virtual_selected_rows, CHN_selected_row_ids,
  US_derived_virtual_selected_rows, US_selected_row_ids
  ):

    if value == 'The World':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      dff = dfSum

      if selected_row_ids:
        if dff.loc[selected_row_ids[0]]['Country/Region'] == 'Mainland China':
          Region = 'China'
        else:
          Region = dff.loc[selected_row_ids[0]]['Country/Region']
      else:
        Region = 'The World' # Display the global total case number 

    elif value == 'Australia':
      if Australia_derived_virtual_selected_rows is None:
        Australia_derived_virtual_selected_rows = []

      dff = AUSTable
      if Australia_selected_row_ids:
        Region = dff.loc[Australia_selected_row_ids[0]]['Province/State']
      else:
        Region = 'Australia'

    elif value == 'Canada':
      if Canada_derived_virtual_selected_rows is None:
        Canada_derived_virtual_selected_rows = []

      dff = CANTable
      if Canada_selected_row_ids:
        Region = dff.loc[Canada_selected_row_ids[0]]['Province/State']
      else:
        Region = 'Canada'

    elif value == 'Mainland China':
      if CHN_derived_virtual_selected_rows is None:
        CHN_derived_virtual_selected_rows = []

      dff = CNTable
      if CHN_selected_row_ids:
        Region = dff.loc[CHN_selected_row_ids[0]]['Province/State']
      else:
        Region = 'China'

    elif value == 'United States':
      if US_derived_virtual_selected_rows is None:
        US_derived_virtual_selected_rows = []

      dff = USTable
      if US_selected_row_ids:
        Region = dff.loc[US_selected_row_ids[0]]['Province/State']
      else:
        Region = 'US'

    elif value == 'Europe':
      if Europe_derived_virtual_selected_rows is None:
        Europe_derived_virtual_selected_rows = []

      dff = EuroTable
      if Europe_selected_row_ids:
        Region = dff.loc[Europe_selected_row_ids[0]]['Country/Region']
      else:
        Region = 'Europe' # Display the Europe total case number 

    # Read cumulative data of a given region from ./cumulative_data folder
    df_region = pd.read_csv('./cumulative_data/{}.csv'.format(Region))
    df_region = df_region.astype(
      {'Date_last_updated_AEDT': 'datetime64', 'date_day': 'datetime64'})

    if dff is USTable or dff is CANTable:
      # Create empty figure canvas
      fig3 = go.Figure()
      # Add trace to the figure
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                                y=df_region['New'],
                                fill='tozeroy',
                                mode='lines',
                                line_shape='spline',
                                name='Daily confirmed case',
                                line=dict(color='rgba(215, 25, 28, .2)', width=2),
                                # marker=dict(size=4, color='#f4f4f2',
                                #            line=dict(width=1,color='#626262')),
                                text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily confirmed cases {:,d} <br>'.format(
                                  i) for i in df_region['New']],
                                hovertemplate='<b>%{text}</b><br></br>' +
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Confirmed'],
                             mode='lines+markers',
                             # line_shape='spline',
                             name='Confirmed case',
                             line=dict(color='#d7191c', width=2),
                             # marker=dict(size=4, color='#f4f4f2',
                             #            line=dict(width=1,color='#921113')),
                             text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Confirmed<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Confirmed']],
                             hovertemplate='<b>%{text}</b><br></br>' +
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Recovered'],
                             mode='lines+markers',
                             # line_shape='spline',
                             name='Recovered case',
                             line=dict(color='#1a9622', width=2),
                             # marker=dict(size=4, color='#f4f4f2',
                             #            line=dict(width=1,color='#168038')),
                             text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Recovered<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Recovered']],
                             hovertemplate='<b>%{text}</b><br></br>' +
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Deaths'],
                             mode='lines+markers',
                             # line_shape='spline',
                             name='Death case',
                             line=dict(color='#626262', width=2),
                             # marker=dict(size=4, color='#f4f4f2',
                             #            line=dict(width=1,color='#626262')),
                             text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Deaths<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Deaths']],
                             hovertemplate='<b>%{text}</b><br></br>' +
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
                font=dict(family='Arial, sans-serif',
                          size=60,
                          color="grey"),
            )
        ],
        yaxis_title="Cumulative cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
            # Set tick range based on the maximum number
            # tickvals=tickList,
            # Set tick label accordingly
            # ticktext=["{:.0f}k".format(i/1000) for i in tickList]
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
        hovermode='x',
        legend_orientation="h",
        legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
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
                                y=df_region['New'],
                                fill='tozeroy',
                                mode='lines',
                                line_shape='spline',
                                name='Daily confirmed case',
                                line=dict(color='rgba(215, 25, 28, .2)', width=2),
                                # marker=dict(size=4, color='#f4f4f2',
                                #            line=dict(width=1,color='#626262')),
                                text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                                hovertext=['Daily confirmed cases {:,d} <br>'.format(
                                  i) for i in df_region['New']],
                                hovertemplate='<b>%{text}</b><br></br>' +
                                                      '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Confirmed'],
                             mode='lines+markers',
                             # line_shape='spline',
                             name='Confirmed case',
                             line=dict(color='#d7191c', width=2),
                             # marker=dict(size=4, color='#f4f4f2',
                             #            line=dict(width=1,color='#921113')),
                             text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Confirmed<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Confirmed']],
                             hovertemplate='<b>%{text}</b><br></br>' +
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Recovered'],
                             mode='lines+markers',
                             # line_shape='spline',
                             name='Recovered case',
                             line=dict(color='#1a9622', width=2),
                             # marker=dict(size=4, color='#f4f4f2',
                             #            line=dict(width=1,color='#168038')),
                             text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Recovered<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Recovered']],
                             hovertemplate='<b>%{text}</b><br></br>' +
                                                     '%{hovertext}' +
                                                     '<extra></extra>'))
      fig3.add_trace(go.Scatter(x=df_region['date_day'],
                             y=df_region['Deaths'],
                             mode='lines+markers',
                             # line_shape='spline',
                             name='Death case',
                             line=dict(color='#626262', width=2),
                             # marker=dict(size=4, color='#f4f4f2',
                             #            line=dict(width=1,color='#626262')),
                             text=[datetime.strftime(d, '%b %d %Y AEDT')
                                                     for d in df_region['date_day']],
                             hovertext=['{} Deaths<br>{:,d} cases<br>'.format(
                                 Region, i) for i in df_region['Deaths']],
                             hovertemplate='<b>%{text}</b><br></br>' +
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
                font=dict(family='Arial, sans-serif',
                          size=60,
                          color="grey"),
            )
        ],
        yaxis_title="Cumulative cases numbers",
        yaxis=dict(
            showline=False, linecolor='#272e3e',
            zeroline=False,
            # showgrid=False,
            gridcolor='rgba(203, 210, 211,.3)',
            gridwidth=.1,
            tickmode='array',
            # Set tick range based on the maximum number
            # tickvals=tickList,
            # Set tick label accordingly
            # ticktext=["{:.0f}k".format(i/1000) for i in tickList]
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
        hovermode='x',
        legend_orientation="h",
        legend=dict(x=.02, y=.95, bgcolor="rgba(0,0,0,0)",),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
      )

      return fig3

@app.callback(
    Output('datatable-interact-logplot', 'figure'),
    [Input('tabs-table', 'value'),
     Input('datatable-interact-location', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location', 'selected_row_ids'),
     Input('datatable-interact-location-Australia', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Australia', 'selected_row_ids'),
     Input('datatable-interact-location-Canada', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Canada', 'selected_row_ids'),
     Input('datatable-interact-location-Europe', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Europe', 'selected_row_ids'),
     Input('datatable-interact-location-Mainland China', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-Mainland China', 'selected_row_ids'),
     Input('datatable-interact-location-United States', 'derived_virtual_selected_rows'),
     Input('datatable-interact-location-United States', 'selected_row_ids'),
     ]
)
def update_logplot(value, derived_virtual_selected_rows, selected_row_ids,
  Australia_derived_virtual_selected_rows, Australia_selected_row_ids,
  Canada_derived_virtual_selected_rows, Canada_selected_row_ids,
  Europe_derived_virtual_selected_rows, Europe_selected_row_ids,
  CHN_derived_virtual_selected_rows, CHN_selected_row_ids,
  US_derived_virtual_selected_rows, US_selected_row_ids
  ):
   
    if value == 'The World':
      if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

      dff = dfSum
      elapseDay = daysOutbreak

      if selected_row_ids:
        if dff.loc[selected_row_ids[0]]['Country/Region'] == 'Mainland China':
          Region = 'China'
        else:
          Region = dff.loc[selected_row_ids[0]]['Country/Region']
      else:
        Region = 'The World'
    
    elif value == 'Australia':
      if Australia_derived_virtual_selected_rows is None:
        Australia_derived_virtual_selected_rows = []

      dff = AUSTable
      elapseDay = daysOutbreak

      if Australia_selected_row_ids:
        Region = dff.loc[Australia_selected_row_ids[0]]['Province/State']
      else:
        Region = 'Australia'

    elif value == 'Canada':
      if Canada_derived_virtual_selected_rows is None:
        Canada_derived_virtual_selected_rows = []

      dff = CANTable
      elapseDay = daysOutbreak

      if Canada_selected_row_ids:
        Region = dff.loc[Canada_selected_row_ids[0]]['Province/State']
      else:
        Region = 'Canada'

    elif value == 'Mainland China':
      if CHN_derived_virtual_selected_rows is None:
        CHN_derived_virtual_selected_rows = []

      dff = CNTable
      elapseDay = daysOutbreak

      if CHN_selected_row_ids:
        Region = dff.loc[CHN_selected_row_ids[0]]['Province/State']
      else:
        Region = 'China'

    elif value == 'United States':
      if US_derived_virtual_selected_rows is None:
        US_derived_virtual_selected_rows = []

      dff = USTable
      elapseDay = daysOutbreak

      if US_selected_row_ids:
        Region = dff.loc[US_selected_row_ids[0]]['Province/State']
      else:
        Region = 'US'

    elif value == 'Europe':
      if Europe_derived_virtual_selected_rows is None:
        Europe_derived_virtual_selected_rows = []

      dff = EuroTable
      elapseDay = daysOutbreak

      if Europe_selected_row_ids:
        Region = dff.loc[Europe_selected_row_ids[0]]['Country/Region']
      else:
        Region = 'Europe'

    # Create empty figure canvas
    fig_curve = go.Figure()

    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y1,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                       '85% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y2,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '35% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y3,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '15% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
    )
    fig_curve.add_trace(go.Scatter(x=pseduoDay,
                                   y=y4,
                                   line=dict(color='rgba(0, 0, 0, .3)', width=1, dash='dot'),
                                   text=[
                                        '5% growth rate' for i in pseduoDay],
                                   hovertemplate='<b>%{text}</b><br>' +
                                                 '<extra></extra>'
                            )
    )

    # Add trace to the figure
    if Region in set(dfs_curve['Region']):

        dotx = [np.array(dfs_curve.loc[dfs_curve['Region'] == Region,'DayElapsed'])[0]]
        doty = [np.array(dfs_curve.loc[dfs_curve['Region'] == Region,'Confirmed'])[0]]

        for regionName in ['The World', 'Japan', 'Italy', 'Turkey', 'US']:

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
                                                       'with %{y:,d} cases<br>'
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
                                                       'with %{y:,d} cases<br>'
                                                       '<extra></extra>'
                            )
          )
          
        fig_curve.add_trace(go.Scatter(x=dfs_curve.loc[dfs_curve['Region'] == Region]['DayElapsed'],
                                       y=dfs_curve.loc[dfs_curve['Region'] == Region]['Confirmed'],
                                       mode='lines',
                                       line_shape='spline',
                                       name=Region,
                                       line=dict(color='#d7191c', width=3),
                                       text=[
                                           i for i in dfs_curve.loc[dfs_curve['Region'] == Region]['Region']],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '<br>%{x} days after 100 cases<br>' +
                                                     'with %{y:,d} cases<br>'
                                                     '<extra></extra>'
                            )
          )
        fig_curve.add_trace(go.Scatter(x=dotx,
                                       y=doty,
                                       mode='markers',
                                       marker=dict(size=7, color='#d7191c',
                                       line=dict(width=1, color='#d7191c')),
                                       text=[Region],
                                       hovertemplate='<b>%{text}</b><br>' +
                                                     '<br>%{x} days after 100 cases<br>' +
                                                     'with %{y:,d} cases<br>'
                                                     '<extra></extra>'
                            )
        )

    else:
        for regionName in ['The World', 'Japan', 'Italy', 'Turkey', 'US']:

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
                                                       'with %{y:,d} cases<br>'
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
                                                       'with %{y:,d} cases<br>'
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
        annotations=[dict(
            x=.5,
            y=.4,
            xref="paper",
            yref="paper",
            text=Region if Region in set(dfs_curve['Region']) else "Not over 100 cases",
            opacity=0.5,
            font=dict(family='Arial, sans-serif',
                      size=60,
                      color="grey"),
                    )
        ],
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
        # hovermode = 'x',
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(color='#292929', size=10)
    )

    return fig_curve



if __name__ == "__main__":
    app.run_server(debug=True)

