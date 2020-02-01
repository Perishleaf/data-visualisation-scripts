# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import math 

import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash
import dash_core_components as dcc
import dash_html_components as html 
import dash_bootstrap_components as dbc

################################################################################
#### Data processing
################################################################################
# Import xlsx file and store each sheet in to a df list
xl_file = pd.ExcelFile('./data.xlsx',)

dfs = {sheet_name: xl_file.parse(sheet_name) 
          for sheet_name in xl_file.sheet_names}

# Data from each sheet can be accessed via key
keyList = list(dfs.keys())

# Data cleansing
for key, df in dfs.items():
    dfs[key].loc[:,'Confirmed'].fillna(value=0, inplace=True)
    dfs[key].loc[:,'Deaths'].fillna(value=0, inplace=True)
    dfs[key].loc[:,'Recovered'].fillna(value=0, inplace=True)
    dfs[key]=dfs[key].astype({'Confirmed':'int64', 'Deaths':'int64', 'Recovered':'int64'})
    # Change as China for coordinate search
    dfs[key]=dfs[key].replace({'Country/Region':'Mainland China'}, 'China')
    dfs[key]=dfs[key].replace({'Province/State':'Queensland'}, 'Brisbane')
    dfs[key]=dfs[key].replace({'Province/State':'New South Wales'}, 'Sydney')
    dfs[key]=dfs[key].replace({'Province/State':'Victoria'}, 'Melbourne')
    # Add a zero to the date so can be convert by datetime.strptime as 0-padded date
    dfs[key]['Last Update'] = '0' + dfs[key]['Last Update']
    dfs[key]['Date_last_updated'] = [datetime.strptime(d, '%m/%d/%Y %H:%M') for d in dfs[key]['Last Update']]

# Add coordinates for each area in the list for the latest table sheet
# To save time, coordinates calling was done seperately
# Import the data with coordinates
dfs[keyList[0]]=pd.read_csv('{}_data.csv'.format(keyList[0]))

# Save numbers into variables to use in the app
confirmedCases=dfs[keyList[0]]['Confirmed'].sum()
deathsCases=dfs[keyList[0]]['Deaths'].sum()
recoveredCases=dfs[keyList[0]]['Recovered'].sum()

# Construct confirmed cases dataframe for line plot
DateList = []
ChinaList =[]
OtherList = []

for key, df in dfs.items():
    dfTpm = df.groupby(['Country/Region'])['Confirmed'].agg(np.sum)
    dfTpm = pd.DataFrame({'Code':dfTpm.index, 'Confirmed':dfTpm.values})
    dfTpm = dfTpm.sort_values(by='Confirmed', ascending=False).reset_index(drop=True)
    DateList.append(df['Date_last_updated'][0])
    ChinaList.append(dfTpm['Confirmed'][0])
    OtherList.append(dfTpm['Confirmed'][1:].sum())
    
df_confirmed = pd.DataFrame({'Date':DateList,
                             'Mainland China':ChinaList,
                             'Other locations':OtherList})

# Construct recovered cases dataframe for line plot
DateList = []
ChinaList =[]
OtherList = []

for key, df in dfs.items():
    dfTpm = df.groupby(['Country/Region'])['Recovered'].agg(np.sum)
    dfTpm = pd.DataFrame({'Code':dfTpm.index, 'Recovered':dfTpm.values})
    dfTpm = dfTpm.sort_values(by='Recovered', ascending=False).reset_index(drop=True)
    DateList.append(df['Date_last_updated'][0])
    ChinaList.append(dfTpm['Recovered'][0])
    OtherList.append(dfTpm['Recovered'][1:].sum())
    
df_recovered = pd.DataFrame({'Date':DateList,
                             'Mainland China':ChinaList,
                             'Other locations':OtherList}) 

# Construct death case dataframe for line plot
DateList = []
ChinaList =[]
OtherList = []

for key, df in dfs.items():
    dfTpm = df.groupby(['Country/Region'])['Deaths'].agg(np.sum)
    dfTpm = pd.DataFrame({'Code':dfTpm.index, 'Deaths':dfTpm.values})
    dfTpm = dfTpm.sort_values(by='Deaths', ascending=False).reset_index(drop=True)
    DateList.append(df['Date_last_updated'][0])
    ChinaList.append(dfTpm['Deaths'][0])
    OtherList.append(dfTpm['Deaths'][1:].sum())
    
df_deaths = pd.DataFrame({'Date':DateList,
                          'Mainland China':ChinaList,
                          'Other locations':OtherList})

# Save numbers into variables to use in the app
# Change to Sydney time
latestDate=datetime.strftime(df_confirmed['Date'][0] + timedelta(hours=16), '%b %d %Y %H:%M AEDT')
daysOutbreak=(df_confirmed['Date'][0] + timedelta(hours=16) - datetime.strptime('12/31/2019', '%m/%d/%Y')).days

#############################################################################################
#### Start to make plots
#############################################################################################
# Line plot for confirmed cases
# Set up tick scale based on confirmed case number
tickList = list(np.arange(0, df_confirmed['Mainland China'].max()+1000, 1000))

# Create empty figure canvas
fig_confirmed = go.Figure()
# Add trace to the figure
fig_confirmed.add_trace(go.Scatter(x=df_confirmed['Date']+timedelta(hours=16), y=df_confirmed['Mainland China'],
                         mode='lines+markers',
                         name='Mainland China',
                         line=dict(color='#921113', width=2),
                         marker=dict(size=8),
                         text=[datetime.strftime(d+timedelta(hours=16), '%b %d %Y %H:%M AEDT') for d in df_confirmed['Date']],
                         hovertemplate='<b>%{text}</b><br></br>'+
                                       'Mainland China confirmed<br>'+
                                       '%{y} cases<br>'+
                                       '<extra></extra>'))
fig_confirmed.add_trace(go.Scatter(x=df_confirmed['Date']+timedelta(hours=16), y=df_confirmed['Other locations'],
                         mode='lines+markers',
                         name='Other Region',
                         line=dict(color='#eb5254', width=2),
                         marker=dict(size=8),
                         text=[datetime.strftime(d+timedelta(hours=16), '%b %d %Y %H:%M AEDT') for d in df_confirmed['Date']],
                         hovertemplate='<b>%{text}</b><br></br>'+
                                       'Other region confirmed<br>'+
                                       '%{y} cases<br>'+
                                       '<extra></extra>'))
# Customise layout
fig_confirmed.update_layout(
    title=dict(
        text="<b>Confirmed Cases Timeline<b>",
        y=0.96, x=0.5, xanchor='center', yanchor='top',
        font=dict(size=20, color="#7fafdf", family="Playfair Display")
    ),
    margin=go.layout.Margin(
        l=5,
        r=10,
        b=10,
        t=50,
        pad=0
    ),
    yaxis=dict(
        showline=True, linecolor='#272e3e',
        zeroline=False,
        gridcolor='#272e3e',
        gridwidth = .1,
        tickmode='array',
        # Set tick range based on the maximum number
        tickvals=tickList,
        # Set tick label accordingly
        ticktext=['{:.0f}k'.format(i/1000) for i in tickList]
    ),
    yaxis_title="Total Confirmed Case Number",
    xaxis=dict(
        showline=True, linecolor='#272e3e',
        gridcolor='#272e3e',
        gridwidth = .1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode = 'x',
    legend_orientation="h",
    plot_bgcolor='#151920',
    paper_bgcolor='#272e3e',
    font=dict(color='#7fafdf')
)

# Line plot for recovered cases
# Set up tick scale based on confirmed case number
tickList = list(np.arange(0, df_recovered['Mainland China'].max()+100, 20))

# Create empty figure canvas
fig_recovered = go.Figure()
# Add trace to the figure
fig_recovered.add_trace(go.Scatter(x=df_recovered['Date']+timedelta(hours=16), y=df_recovered['Mainland China'],
                         mode='lines+markers',
                         name='Mainland China',
                         line=dict(color='#168038', width=2),
                         marker=dict(size=8),
                         text=[datetime.strftime(d+timedelta(hours=16), '%b %d %Y %H:%M AEDT') for d in df_recovered['Date']],
                         hovertemplate='<b>%{text}</b><br></br>'+
                                       'Mainland China recovered<br>'+
                                       '%{y} cases<br>'+
                                       '<extra></extra>'))
fig_recovered.add_trace(go.Scatter(x=df_recovered['Date']+timedelta(hours=16), y=df_recovered['Other locations'],
                         mode='lines+markers',
                         name='Other Region',
                         line=dict(color='#25d75d', width=2),
                         marker=dict(size=8),
                         text=[datetime.strftime(d+timedelta(hours=16), '%b %d %Y %H:%M AEDT') for d in df_recovered['Date']],
                         hovertemplate='<b>%{text}</b><br></br>'+
                                       'Other region recovered<br>'+
                                       '%{y} cases<br>'+
                                       '<extra></extra>'))
# Customise layout
fig_recovered.update_layout(
    title=dict(
        text="<b>Recovered Cases Timeline<b>",
        y=0.96, x=0.5, xanchor='center', yanchor='top',
        font=dict(size=20, color="#7fafdf", family="Playfair Display")
    ),
    margin=go.layout.Margin(
        l=5,
        r=10,
        b=10,
        t=50,
        pad=0
    ),
    yaxis=dict(
        showline=True, linecolor='#272e3e',
        zeroline=False,
        gridcolor='#272e3e',
        gridwidth = .1,
        tickmode='array',
        # Set tick range based on the maximum number
        tickvals=tickList,
        # Set tick label accordingly
        ticktext=['{:.0f}'.format(i) for i in tickList]
    ),
    yaxis_title="Total Recovered Case Number",
    xaxis=dict(
        showline=True, linecolor='#272e3e',
        gridcolor='#272e3e',
        gridwidth = .1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode = 'x',
    legend_orientation="h",
    plot_bgcolor='#151920',
    paper_bgcolor='#272e3e',
    font=dict(color='#7fafdf')
)

# Line plot for deaths cases
# Set up tick scale based on confirmed case number
tickList = list(np.arange(0, df_deaths['Mainland China'].max()+100, 20))

# Create empty figure canvas
fig_deaths = go.Figure()
# Add trace to the figure
fig_deaths.add_trace(go.Scatter(x=df_deaths['Date']+timedelta(hours=16), y=df_deaths['Mainland China'],
                         mode='lines+markers',
                         name='Mainland China',
                         line=dict(color='#fc8715', width=2),
                         marker=dict(size=8),
                         text=[datetime.strftime(d+timedelta(hours=16), '%b %d %Y %H:%M AEDT') for d in df_deaths['Date']],
                         hovertemplate='<b>%{text}</b><br></br>'+
                                       'Mainland China death<br>'+
                                       '%{y} cases<br>'+
                                       '<extra></extra>'))
fig_deaths.add_trace(go.Scatter(x=df_deaths['Date']+timedelta(hours=16), y=df_deaths['Other locations'],
                         mode='lines+markers',
                         name='Other Region',
                         line=dict(color='#fed5ad', width=2),
                         marker=dict(size=8),
                         text=[datetime.strftime(d+timedelta(hours=16), '%b %d %Y %H:%M AEDT') for d in df_deaths['Date']],
                         hovertemplate='<b>%{text}</b><br></br>'+
                                       'Other region death<br>'+
                                       '%{y} cases<br>'+
                                       '<extra></extra>'))
# Customise layout
fig_deaths.update_layout(
    title=dict(
        text="<b>Death Cases Timeline<b>",
        y=0.96, x=0.5, xanchor='center', yanchor='top',
        font=dict(size=20, color="#7fafdf", family="Playfair Display")
    ),
    margin=go.layout.Margin(
        l=5,
        r=10,
        b=10,
        t=50,
        pad=0
    ),
    yaxis=dict(
        showline=True, linecolor='#272e3e',
        zeroline=False,
        gridcolor='#272e3e',
        gridwidth = .1,
        tickmode='array',
        # Set tick range based on the maximum number
        tickvals=tickList,
        # Set tick label accordingly
        ticktext=['{:.0f}'.format(i) for i in tickList]
    ),
    yaxis_title="Total Death Case Number",
    xaxis=dict(
        showline=True, linecolor='#272e3e',
        gridcolor='#272e3e',
        gridwidth = .1,
        zeroline=False
    ),
    xaxis_tickformat='%b %d',
    hovermode = 'x',
    legend_orientation="h",
    plot_bgcolor='#151920',
    paper_bgcolor='#272e3e',
    font=dict(color='#7fafdf')
)

#############################
#### Plot map
#############################
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

textList=[]
for area, region in zip(dfs[keyList[0]]['Province/State'], dfs[keyList[0]]['Country/Region']):
    
    if type(area) is str:
        if region == "Hong Kong" or region == "Macau" or region == "Taiwan":
            textList.append(area)
        else:
            textList.append(area+', '+region)
    else:
        textList.append(region)

fig2 = go.Figure(go.Scattermapbox(
        lat=dfs[keyList[0]]['lat'],
        lon=dfs[keyList[0]]['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            color='#ff1414',
            size=dfs[keyList[0]]['Confirmed'].tolist(), 
            sizemin=2,
            sizemode='area',
            sizeref=2.*max(dfs[keyList[0]]['Confirmed'].tolist())/(40.**2),
        ),
        text=textList,
        hovertext=['Comfirmed: {}<br>Recovered: {}<br>Death: {}'.format(i, j, k) for i, j, k in zip(dfs[keyList[0]]['Confirmed'],
                                                                                                    dfs[keyList[0]]['Recovered'],
                                                                                                    dfs[keyList[0]]['Deaths'])],
    
        hovertemplate = "<b>%{text}</b><br><br>" +
                        "%{hovertext}<br>" +
                        "<extra></extra>")
    
        )

fig2.update_layout(
    title=dict(
        text="<b>Latest Coronavirus Outbreak Map<b>",
        y=0.96, x=0.5, xanchor='center', yanchor='top',
        font=dict(size=20, color="#7fafdf", family="Playfair Display")
    ),
    plot_bgcolor='#151920',
    paper_bgcolor='#272e3e',
    margin=go.layout.Margin(
        l=10,
        r=10,
        b=10,
        t=50,
        pad=40
    ),
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        style="mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz",
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=29.538860, 
            lon=173.304781
        ),
        pitch=0,
        zoom=2
    )
)
##################################################################################################
#### Start dash app
##################################################################################################

app = dash.Dash(__name__, assets_folder='./assets/',
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, height=device-height, initial-scale=1.0"}
    ])

server = app.server

app.layout = html.Div(style={'backgroundColor':'#151920'},
    children=[
        html.Div(
            id="header",
            children=[                          
                html.H4(children="Wuhan Coronavirus (2019-nCoV) Outbreak Monitor"),
                html.P(
                    id="description",
                    children="On Dec 31, 2019, the World Health Organization (WHO) was informed of \
                    an outbreak of “pneumonia of unknown cause” detected in Wuhan City, Hubei Province, China – the \
                    seventh-largest city in China with 11 million residents. As of {}, there are over {} cases \
                    of 2019-nCoV confirmed globally.\
                    This dash board is developed to visualise and track the recent reported \
                    cases on a daily timescale.".format(latestDate, confirmedCases),
                ),
                html.P(style={'fontWeight':'bold'},
                    children="Last updated on {}.".format(latestDate))
            ]        
        ),
        html.Div(
            id="number-plate",
            style={'marginLeft':'1.5%','marginRight':'1.5%','marginBottom':'.5%'},
                 children=[
                     html.Div(
                         style={'width':'24.4%','backgroundColor':'#272e3e','display':'inline-block','marginRight':'.8%'},
                              children=[html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#ffffbf','padding':'1rem'},
                                               children="Days Since Outbreak"),
                                        html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#ffffbf'},
                                               children='{}'.format(daysOutbreak))]),
                     html.Div(style={'width':'24.4%','backgroundColor':'#272e3e','display':'inline-block','marginRight':'.8%'},
                              children=[html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#d7191c','padding':'1rem'},
                                               children="Confirmed Cases"),
                                        html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#d7191c'},
                                                children='{}'.format(confirmedCases))]),
                     html.Div(style={'width':'24.4%','backgroundColor':'#272e3e','display':'inline-block','marginRight':'.8%'},
                              children=[html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#1a9641','padding':'1rem'},
                                               children="Recovered Cases"),
                                        html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#1a9641'},
                                               children='{}'.format(recoveredCases))]),
                     html.Div(style={'width':'24.4%','backgroundColor':'#272e3e','display':'inline-block','marginTop':'.5%'},
                              children=[html.P(style={'textAlign':'center',
                                                      'fontWeight':'bold','color':'#fdae61','padding':'1rem'},
                                               children="Death Cases"),
                                        html.H3(style={'textAlign':'center',
                                                       'fontWeight':'bold','color':'#fdae61'},
                                                children='{}'.format(deathsCases))])]),
        html.Div(style={'marginLeft':'1.5%','marginRight':'1.5%','marginBottom':'.35%','marginTop':'.5%'},
                 children=[
                     html.Div(style={'width':'32.79%','display':'inline-block','marginRight':'.8%'},
                              children=[dcc.Graph(figure=fig_confirmed)]),
                     html.Div(style={'width':'32.79%','display':'inline-block','marginRight':'.8%'},
                              children=[dcc.Graph(figure=fig_recovered)]),
                     html.Div(style={'width':'32.79%','display':'inline-block'},
                              children=[dcc.Graph(figure=fig_deaths)])]),
        html.Div(style={'marginLeft':'1.5%','marginRight':'1.5%','marginBottom':'.5%'},
                 children=[
                     html.Div(style={'width':'100%','display':'inline-block'},
                              children=[dcc.Graph(figure=fig2)]),]),
        html.Div(style={'marginLeft':'1.5%','marginRight':'1.5%'},
                 children=[
                     html.P(style={'textAlign':'center','margin':'auto'},
                            children=["Data source from ", 
                                      html.A('JHU CSSE,', href='https://docs.google.com/spreadsheets/d/1yZv9w9z\
                                      RKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/htmlview?usp=sharing&sle=true#'),
                                      html.A(' Dingxiangyuan', href='https://ncov.dxy.cn/ncovh5/view/pneumonia?sce\
                                      ne=2&clicktime=1579582238&enterid=1579582238&from=singlemessage&isappinstalled=0'),
                                      " | 🙏 Pray for China, Pray for the World 🙏 |",
                                      " Developed by ",html.A('Jun', href='https://junye0798.com/')," with ❤️"])])

])


if __name__ == "__main__":
    app.run_server(debug=True)

