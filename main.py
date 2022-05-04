"""Main Python Module

Description
===============================

Create a interactive dashboard to display trends in Twitch Viewership
during the pandemic, and the covid cases, on graphs

Copyright and Usage Information
===============================

All forms of distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2021 Winston Chieng, Justin Li, Derrick Cho
"""

import covid_data
import twitch_data
import plotly.graph_objs as go
import plotly.express as px

from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Twitch and Covid Graphs for 2020/2021",
            style={'text-align': 'center', 'font-family': 'Helvetica',
                   'backgroundColor': '#9146FB', 'color': '#ffffff'}),
    dcc.Dropdown(id='select_year',
                 options=[
                     {'label': '2020', 'value': 2020},
                     {'label': '2019', 'value': 2019},
                     {'label': '2018', 'value': 2018},
                     {'label': '2017', 'value': 2017},
                     {'label': '2016', 'value': 2016}],
                 value=2020,
                 style={'width': '30%'}
                 ),

    dcc.Graph(id='twitch_graph', figure={}),

    html.Br(),

    dcc.Graph(id='twitch_graph1', figure={}),

    html.Br(),

    dcc.Dropdown(id='select_year2',
                 options=[
                     {'label': '2020', 'value': 2020},
                     {'label': '2019', 'value': 2019},
                     {'label': '2018', 'value': 2018},
                     {'label': '2017', 'value': 2017},
                     {'label': '2016', 'value': 2016}],
                 value=2020,
                 style={'width': '30%'}
                 ),

    dcc.Dropdown(id='select_game',
                 options=[
                     {'label': 'League of Legends', 'value': 'League of Legends'},
                     {'label': 'VALORANT', 'value': 'VALORANT'},
                     {'label': 'Counter-Strike: Global Offensive', 'value':
                         'Counter-Strike: Global Offensive'},
                     {'label': 'Call of Duty: Black Ops III',
                      'value': 'Call of Duty: Black Ops III'},
                     {'label': 'Super Smash Bros. Melee', 'value': 'Super Smash Bros. Melee'},
                     {'label': 'Rocket League', 'value': 'Rocket League'}
                 ],
                 value='League of Legends',
                 style={'width': '30%'}
                 ),

    dcc.Graph(id='twitch_graph2', figure={}),

    html.Br(),

    dcc.Dropdown(id='select_country',
                 options=[
                     {'label': 'Canada', 'value': 'Canada'},
                     {'label': 'Mexico', 'value': 'Mexico'},
                     {'label': 'USA', 'value': 'USA'},
                     {'label': 'Australia', 'value': 'Australia'},
                     {'label': 'Germany', 'value': 'Germany'},
                     {'label': 'South Korea', 'value': 'South Korea'}
                 ],
                 value='Canada',
                 style={'width': '30%'}
                 ),

    dcc.Dropdown(id='select_year3',
                 options=[
                     {'label': '2021', 'value': 2021},
                     {'label': '2020', 'value': 2020}],
                 value=2020,
                 style={'width': '30%'}
                 ),

    dcc.Graph(id='covid_graph', figure={})
])


@app.callback(
    [Output(component_id='twitch_graph', component_property='figure'),
     Output(component_id='twitch_graph1', component_property='figure'),
     Output(component_id='twitch_graph2', component_property='figure'),
     Output(component_id='covid_graph', component_property='figure')],
    [Input(component_id='select_year', component_property='value'),
     Input(component_id='select_year2', component_property='value'),
     Input(component_id='select_game', component_property='value'),
     Input(component_id='select_country', component_property='value'),
     Input(component_id='select_year3', component_property='value')]
)
def update_graph(selected_year: int, selected_year2: int, selected_game: str, selected_country: str,
                 selected_year3: int):
    """populate the graphs with data"""
    twitch_data_global = twitch_data.load_data_global('twitch_global.csv', [selected_year])
    twitch_game_data = twitch_data.load_data_game('twitch_game_data.csv',
                                                  selected_game, [selected_year2])
    tdm_global = [twitch.month for twitch in twitch_data_global]
    tdm_game = [twitch.month for twitch in twitch_game_data]

    # Twitch Graph #1 (Average Viewership)
    td_avg = [twitch_data.average_viewership_v2(twitch_data_global, a)[1] for a in tdm_global]
    # Twitch Graph #2 (Streams)
    td_stream = [twitch.streams for twitch in twitch_data_global]
    # Twitch Graph #3 (Games)
    td_game = [twitch_data.average_viewership_v2(twitch_game_data, a)[1] for a in tdm_game]

    # Covid Graph Data
    cd = covid_data.load_data_country('covid_by_year.csv', selected_country, [selected_year3])
    cdy = [covid_data.total_cases(cd, selected_year3, a) for a in range(1, 13)]

    dfv = {'Month': tdm_global, 'Viewership': td_avg}
    df = {'Month': tdm_global, 'Streams': td_stream}
    dff = {'Month': [i for i in range(1, 13)], 'Cases': cdy}
    dfx = {'Month': tdm_game, 'Viewership': td_game}

    fig = px.line(dfv, x="Month", y="Viewership", title="Viewers per month (global)",
                  template="plotly_dark")
    fig_two = px.line(df, x="Month", y="Streams",
                      title="Streams per month (global)", template="plotly_dark")
    fig_three = px.line(dfx, x="Month", y="Viewership",
                        title="Viewers per month ({})".format(selected_game),
                        template="plotly_dark")
    fig_four = px.line(dff, x='Month', y='Cases',
                       title='Cases per month ({})'.format(selected_country),
                       template="plotly_dark")

    return [go.Figure(fig), go.Figure(fig_two), go.Figure(fig_three), go.Figure(fig_four)]


if __name__ == '__main__':
    app.run_server(debug=True)
