import json
import re
from dash import Dash, html, dcc, Input, Output, State
import plotly.io as pio
import plotly.express as px
import newspaper
from api_request import *
import pandas as pd
import plotly.graph_objects as go

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
        dcc.Input(id='url-input', type='text', placeholder='Article URL link...',
                  style={"width": "35%", "padding": "15px", "font-size": "16px"}),
        html.Br(),
        html.Button("Analyse", id='url-submit-button',
                    style={"margin-top": "20px", "font-size": "14px", "padding-left": "10%", "padding-right": "10%",},
                    n_clicks=0),
    ], style={"text-align": "center", "margin-top": "20px"}
)

message_form = html.Div(
    [
        dcc.Input(id='message-input', type='text', placeholder='Message...',
                  style={"width": "35%", "font-size": "16px", "padding": "15px"}),
        html.Div(
            [
                dcc.Slider(
                id='slider',
                min=0.75,
                max=0.98,
                step=0.05,
                value=0.75,
        ),
            ], style={"margin-left": "30%", "margin-right": "30%", "margin-top": "10px"}
        ),
        html.Button("Match", id='message-submit-button',
                    style={"margin-top": "10px", "font-size": "14px", "padding-left": "10%", "padding-right": "10%"},
                    n_clicks=0),
        html.H2("Found cases", style={"text-align": "left", "margin-left": "18%", "margin-top": "20px"}),
        html.Hr(style={"margin-right": "50%"}),
    ], style={"text-align": "center", "margin-top": "20px"}
)

sidebar = html.Div([
    html.Div(children=[html.H2("Parameters")]),
    html.Hr(),
    article_link,
    message_form
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
              Input('tabs', 'value'), )
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            article_link,
            html.Div(id='bar-chart-container')
        ])
    elif tab == 'tab-2':
        return html.Div([
            message_form,
            html.Div(id='case-matching-container')
        ])
    elif tab == 'tab-3':
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

        ], style={'height': '100%', 'width:': '100%'})
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


@app.callback(
    Output('bar-chart-container', 'children'),
    # Output('url-input', 'value'),
    Input('url-submit-button', 'n_clicks'),
    State('url-input', 'value'),
)
def bar_chart_tab(n_clicks, url):
    article = url_to_article(url)

    # Lower case article text
    lower_case = article.text.lower()
    # Remove UTF characters
    no_utf = re.sub(r'[^a-zA-Z0-9.,:/]', ' ', lower_case)
    response = model_request(no_utf[:2000])
    # Response to dict
    dict_data = json.loads(response.text)

    chart_data = pd.DataFrame(dict_data['explanation'])
    chart = px.bar(chart_data, x=0, y=1)
    # create a scatter plot using Plotly Express
    if n_clicks > 0:
        return dcc.Graph(id='bar-chart', figure=chart)


def visualise_match(case_score, case_title, case_content):
    return html.Div([
        html.Div(
            [
                html.H2(case_title + "."),
                html.Div([
                    html.H2("Score: ", style={"margin-left": "50px"}),
                    html.H2(case_score, style={"color": "#ff5252", "margin-left": "10px"})
                ], style={'display': 'flex', 'justify-content': 'space-around', "margin": "0"}),

            ], style={'display': 'flex', 'justify-content': 'left'}
        ),
        html.P(case_content),
    ], style={"margin-bottom": "50px"})


@app.callback(
    Output('case-matching-container', 'children'),
    Input('message-submit-button', 'n_clicks'),
    Input('slider', 'value'),
    State('message-input', 'value'),
)
def case_matching_tab(n_clicks, slider, message):
    # Lower case message
    lower_case = message.lower()
    # # Remove UTF symbols
    no_utf = re.sub(r'[^a-zA-Z0-9.,:/]', ' ', lower_case)

    # # Case model matching request
    response = case_matching(no_utf)

    test_response = "[{\"score\": 0.9,\"title\": \"The title of the disinformation case\",\"content\": \"The description of the disinformation case\"}," \
                    "{\"score\": 0.5,\"title\": \"The title of test\",\"content\": \"The description of the test case\"}]"
    array = json.loads(response.text)  # response.text

    div_children = [html.Div(id=f"div-{obj['score']}",
                             children=visualise_match(obj['score'], obj['title'], obj['content'])) for obj in array]

    return div_children


app.layout = html.Div([content])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True)

