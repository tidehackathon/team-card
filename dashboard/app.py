import json
import re
from dash import Dash, html, dcc, Input, Output, State
import plotly.io as pio
import plotly.express as px
import numpy as np
import newspaper
from api_request import *
import pandas as pd
import plotly.graph_objects as go

pio.templates.default = "plotly_dark"  # set the default theme to dark

with open('results/confusion_matrix.npy', 'rb') as f:
    confusion_matrix = np.load(f)

with open('results/metrics.json', 'r') as f:
    metrics = json.load(f)


# Define the layout for the bar chart
heatmap_layout = {
    'title': 'Disinformation detection model confusion matrix',
    'paper_bgcolor': '#2B2E33',
    'plot_bgcolor': '#2B2E33',
    'font': {'color': 'white'},
}

bar_layout = {
    'title': 'Number of detected disinformation cases',
    'paper_bgcolor': '#2B2E33',
    'plot_bgcolor': '#2B2E33',
    'font': {'color': 'white'},
}
fig_heatmap = go.Figure(data=go.Heatmap(
                    z=confusion_matrix[[1,0]],
                    text=[[confusion_matrix[1][0], confusion_matrix[1][1]], 
                          [confusion_matrix[0][0], confusion_matrix[0][1]]],
                    texttemplate="%{text}",
                    textfont={"size":18},
                    colorscale='rdbu'),
                    layout=heatmap_layout)

fig_bar = go.Figure(go.Bar(
    x=['Fakenews', "Neutral"],
    y=np.sum(confusion_matrix, axis=1),
    name='Primary Product',
    marker_color='indianred'
), layout=bar_layout)

darkTheme = ['styles.css']

app = Dash(external_stylesheets=darkTheme, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
app.title = "This is title"


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
        html.Button("Analyse", id='url-submit-button', style={"margin-top": "15px"}, n_clicks=0),
    ], style={"text-align": "center"}
)

message_form = html.Div(
    [
        html.P("Message"),
        dcc.Input(id='message-input', type='text', placeholder='Message...'),
        html.Br(),
        html.Button("Match", id='message-submit-button', style={"margin-top": "15px", "margin-right": "10px"}, n_clicks=0),
    ], style={"text-align": "center", "margin-top": "20px"}
)

sidebar = html.Div([
    html.Div(children=[html.H2("Parameters")]),
    html.Hr(),
    article_link,
    message_form
], className="sidebar")

content = html.Div([
    html.H2("infoDesic dashboard"),
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
                dcc.Graph(id='heatmap_plot', figure=fig_heatmap, style={"margin-top": "20px", 'float': 'right'}),
                dcc.Graph(id='barchart', figure=fig_bar, style={"margin-top": "20px", 'width': '95%', 'float': 'right'})
        ], style={'display': 'flex', 'width': '100%', 'height': '100%', 'textAlign': 'center', 'justify-content': 'space-between'}),
         html.Div([
            html.Div([
                html.H2("Model Accuracy: " + str(round(metrics.get('Accuracy'), 2)), style={"margin-left": "20px"}),
                html.H2("Model Precision: " + str(round(metrics.get('Precision'), 2)), style={"margin-left": "20px"})
            ], style={'display': 'flex', 'justify-content': 'center'}),
            html.Div([
                html.H2("Model Recall: " + str(round(metrics.get('Recall'), 2)), style={"margin-left": "20px"}),
                html.H2("Model F1-Score: " + str(round(metrics.get('F1-score'), 2)), style={"margin-left": "20px"})
            ], style={'display': 'flex', 'justify-content': 'center'})
            ], style={'justify-content': 'center'})

    ], style={'height': '100%', 'width:': '100%'})
    elif tab == 'tab-4':
        return html.Div([
            html.H3('Tab content 4')
        ])


@app.callback(
    Output('bar-chart-container', 'children'),
    #Output('url-input', 'value'),
    Input('url-submit-button', 'n_clicks'),
    State('url-input', 'value'),
)
def bar_chart_tab(n_clicks, url):
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
                # print(dict_data['explanation'])
    image = px.bar(responses_df, x=0, y=1)
    # create a scatter plot using Plotly Express
    if n_clicks > 0:
        return dcc.Graph(id='bar-chart', figure=image)



@app.callback(
    Output('case-matching-container', 'children'),
    Input('message-submit-button', 'n_clicks'),
    State('message-input', 'value'),
)
def case_matching_tab(n_clicks, message):
    # Lower case message
    lower_case = message.lower()
    # Remove UTF symbols
    no_utf = re.sub(r'[^a-zA-Z0-9.,:/]', ' ', lower_case)
    # Case model matching request
    response = case_matching(no_utf)
    print(response.text)
    return html.Div(
        [
            html.H2("Title"),
            html.P("Paragraph")
        ]
    )


app.layout = html.Div([content])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True)
