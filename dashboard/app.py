import json
import re

from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objs as go
import plotly.io as pio
import plotly.express as px
import pandas as pd
import newspaper

from api_request import *

import pandas as pd
import plotly.graph_objects as go
import numpy as np

pio.templates.default = "plotly_dark"  # set the default theme to dark
# sample data
x = ['A', 'B', 'C', 'D', 'E']
y = [10, 20, 30, 25, 15]

fig = go.Figure(data=[go.Bar(x=x, y=y)])
fig.update_layout(
    title="Sample Pie Chart",
    font=dict(
        family="Arial",
        size=12,
        color="white"
    ),
    plot_bgcolor="#1f2630",
    paper_bgcolor="#1f2630"
)

data = {
    'x': ['Apples', 'Oranges', 'Bananas'],
    'y': [3, 2, 4]
}

# Define the layout for the bar chart
layout = {
    'title': 'Fruit Sales',
    'paper_bgcolor': '#2B2E33',
    'plot_bgcolor': '#2B2E33',
    'font': {'color': 'white'},
    'xaxis': {'title': 'Fruit'},
    'yaxis': {'title': 'Number of Sales'}
}

# Define the figure for the bar chart
figure = {
    'data': [{'type': 'bar', 'marker': {'color': 'Orange'}, 'x': data['x'], 'y': data['y']}],
    'layout': layout
}

darkTheme = ['styles.css']

app = Dash(external_stylesheets=darkTheme, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.title = "This is title"

parameters = html.Div([
    html.P("Dropdown"),
    dcc.Dropdown(options=[
        {'label': 'Vilnius', 'value': 'VLN'},
        {'label': 'Kaunas', 'value': 'KAU'},
        {'label': 'Klaipeda', 'value': 'KLP'},
    ], placeholder="select city", id='demo-dropdown', className="dropdown"),
    html.P("Range Slider"),
    dcc.RangeSlider(
        id='range_slider',
        min=0,
        max=20,
        step=5,
        value=[5, 15]
    ),
    html.P("Check Box"),
    dcc.Checklist(
        id='check_list',
        options=[{
            'label': 'Value One',
            'value': 'value1'
        },
            {
                'label': 'Value Two',
                'value': 'value2'
            },
            {
                'label': 'Value Three',
                'value': 'value3'
            }
        ],
        value=['value1', 'value2'],
        inline=False,
        style={"display": "flex", "flex-direction": "column"},
    ),
    html.Button("Apply", style={"margin-top": "30px"}),
], style={"text-align": "center"})


def url_to_article(url):
    # create a newspaper Article object
    article = newspaper.Article(url)
    # download the article content
    article.download()
    # parse the article content
    article.parse()
    return article


article_link = html.Div(
    [
        html.P("Article URL link"),
        dcc.Input(id='url-input', type='text', placeholder='Article URL...'),
        html.Br(),
        html.Button("Apply", id='submit-button', style={"margin-top": "15px"}, n_clicks=0),
    ], style={"text-align": "center"}
)

sidebar = html.Div([
    html.Div(children=[html.H2("Parameters")]),
    html.Hr(),
    article_link
], className="sidebar")

content = html.Div([
    html.H2("DISinformation Analyser Dashboard"),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        html.Div(className="left-circle"),
        dcc.Tab(label='Tab 1', value='tab-1', className="tab", selected_className="tab-selected"),
        dcc.Tab(label='Tab 2', value='tab-2', className="tab", selected_className="tab-selected"),
        dcc.Tab(label='Tab 3', value='tab-3', className="tab", selected_className="tab-selected"),
        dcc.Tab(label='Tab 4', value='tab-4', className="tab", selected_className="tab-selected"),
        html.Div(className="right-circle"),
    ]),
    html.Div(id='tabs-content')
], className="content")


@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'),)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.P("This is container with elements"),
                    ], className='container card-style', ),
                    html.Div([
                        html.P("This is container with elements"),
                    ], className='container card-style', ),
                    html.Div([
                        html.P("This is container with elements"),
                    ], className='container card-style', ),
                ], className="card-container"),
                dcc.Graph(
                    id='bar-chart',
                    figure=figure,
                    style={"margin-top": "20px"}
                ),

            ], style={'display': 'inline-block', 'width': '100%', 'height': '100%', 'textAlign': 'center'}),

        ], style={'height': '100%', 'width:': '100%'});
    elif tab == 'tab-2':
        return html.Div(id='output-container')
    elif tab == 'tab-3':
        return html.Div([
            html.H3('Tab content 3')
        ])
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


@app.callback(
    Output('output-container', 'children'),
    #Output('url-input', 'value'),
    Input('submit-button', 'n_clicks'),
    State('url-input', 'value'),
)
def display_output(n_clicks, url):
    article = url_to_article(url)
    # print(article.text)
    # Lower case article text
    lower_case = article.text.lower()

    # Request to models
    responses_df = pd.DataFrame()
    # Split the paragraphs
    for paragraph in lower_case.split("\n"):
        # Remove non text-digit characters
        no_utf = re.sub(r'[^a-zA-Z0-9.,:/]', ' ', paragraph)
        if len(no_utf) > 5:
            response = model_request(no_utf)
            # Response to dict
            dict_data = json.loads(response.text)
            # Check if it's disinformation
            if dict_data['result']:
                responses_df = responses_df.append(dict_data['explanation'])
                #print(dict_data['explanation'])

    image = px.bar(responses_df, x=0, y=1)
    # create a scatter plot using Plotly Express
    if n_clicks > 0:
        return dcc.Graph(id='bar-chart', figure=image)


app.layout = html.Div([sidebar, content])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True)
