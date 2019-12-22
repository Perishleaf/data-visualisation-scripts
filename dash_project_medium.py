# -*- coding: utf-8 -*-

import json

import pandas as pd

import plotly
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html

# Import data 
median_price_new = pd.read_csv('median_price_new_for_dash.csv')

with open('Sydney_suburb.geojson') as json_data:
    Sydney_data = json.load(json_data)

# mapbox token
mapbox_accesstoken = 'YOUR TOKEN GOES HERE'

# This is the part to create plotly fig
########################################################
suburbs=median_price_new['Suburb'].str.title().tolist()

pl_deep=[[0.0, 'rgb(253, 253, 204)'],
         [0.1, 'rgb(201, 235, 177)'],
         [0.2, 'rgb(145, 216, 163)'],
         [0.3, 'rgb(102, 194, 163)'],
         [0.4, 'rgb(81, 168, 162)'],
         [0.5, 'rgb(72, 141, 157)'],
         [0.6, 'rgb(64, 117, 152)'],
         [0.7, 'rgb(61, 90, 146)'],
         [0.8, 'rgb(65, 64, 123)'],
         [0.9, 'rgb(55, 44, 80)'],
         [1.0, 'rgb(39, 26, 44)']]

Types = ['Unit_buy/M','Unit_rent','House_rent','House_buy/M']    

trace1 = []    
    
# Suburbs order should be the same as "id" passed to location
for q in Types:
    trace1.append(go.Choroplethmapbox(
        geojson = Sydney_data,
        locations = median_price_new['id'].tolist(),
        z = median_price_new[q].tolist(), 
        colorscale = pl_deep,
        text = suburbs, 
        colorbar = dict(thickness=20, ticklen=3),
        marker_line_width=0, marker_opacity=0.7,
        visible=False,
        subplot='mapbox1',
        hovertemplate = "<b>%{text}</b><br><br>" +
                        "Price: %{z}<br>" +
                        "<extra></extra>")) # "<extra></extra>" means we don't display the info in the secondary box, such as trace id.
    
trace1[0]['visible'] = True

trace2 = []    
    
# Suburbs order should be the same as "id" passed to location
for q in Types:
    trace2.append(go.Bar(
        x=median_price_new.sort_values([q], ascending=False).head(10)[q],
        y=median_price_new.sort_values([q], ascending=False).head(10)['Suburb_name_geojson'].str.title().tolist(),
        xaxis='x2',
        yaxis='y2',
        marker=dict(
            color='rgba(91, 207, 135, 0.3)',
            line=dict(
                color='rgba(91, 207, 135, 2.0)',
                width=0.5),
        ),
        visible=False,
        name='Top 10 suburbs with the highest {} median price'.format(q),
        orientation='h',
    ))
    
trace2[0]['visible'] = True


# Sydney latitude and longitude values
latitude = -33.892319
longitude = 151.146167

layout = go.Layout(
    title = {'text': 'Sydney property buy/rent median price 2019',
    		 'font': {'size':28, 
    		 		  'family':'Arial'}},
    autosize = True,
    
    mapbox1 = dict(
        domain = {'x': [0.3, 1],'y': [0, 1]},
        center = dict(lat=latitude, lon=longitude),
        accesstoken = mapbox_accesstoken, 
        zoom = 12),

    xaxis2={
        'zeroline': False,
        "showline": False,
        "showticklabels":True,
        'showgrid':True,
        'domain': [0, 0.25],
        'side': 'left',
        'anchor': 'x2',
    },
    yaxis2={
        'domain': [0.4, 0.9],
        'anchor': 'y2',
        'autorange': 'reversed',
    },
    margin=dict(l=100, r=20, t=70, b=70),
    paper_bgcolor='rgb(204, 204, 204)',
    plot_bgcolor='rgb(204, 204, 204)',
)
layout.update(updatemenus=list([
    dict(x=0,
         y=1,
         xanchor='left',
         yanchor='middle',
         buttons=list([
             dict(
                 args=['visible', [True, False, False, False]],
                 label='Property type: Unit buy/M',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, True, False, False]],
                 label='Property type: Unit rent',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, False, True, False]],
                 label='Property type: House rent',
                 method='restyle'
                 ),
             dict(
                 args=['visible', [False, False, False, True]],
                 label='Property type: House buy/M',
                 method='restyle'
                )
            ]),
        )]))

fig=go.Figure(data=trace2 + trace1, layout=layout)
#####################################################################
# This is the part to initiate Dash app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children=''),

    dcc.Graph(
        id='example-graph-1',
        figure=fig
    ),

    html.Div(children='''
        Data source from https://www.realestate.com.au/neighbourhoods @Dec 2019
    ''')
])

if __name__ == '__main__':
    app.run_server(debug=True)
