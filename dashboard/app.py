import json
from dash import Dash, html, dcc, Input, Output, State
import plotly.io as pio
import plotly.express as px
import numpy as np
import newspaper
from api_request import *
import pandas as pd
import plotly.graph_objects as go

from processing import preprocess_article, preprocess_message

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
app.title = "infoDesic"


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
                  style={"width": "35%", "padding": "15px", "font-size": "16px"}),
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
        html.H2("Found cases", style={"text-align": "left", "margin-left": "10%", "margin-top": "20px"}),
        html.Hr(style={"margin-right": "365px"}),
    ], style={"text-align": "center", "margin-top": "20px"}
)

content = html.Div([
    html.H2("infoDesic dashboard"),
    dcc.Tabs(id='tabs', value='tab-1', children=[
        html.Div(className="left-circle"),
        dcc.Tab(label='DISinformation Analyzer', value='tab-1', className="tab", selected_className="tab-selected"),
        dcc.Tab(label='Match DISinformation Cases', value='tab-2', className="tab", selected_className="tab-selected"),
        dcc.Tab(label='Model Accuracy Visualization', value='tab-3', className="tab", selected_className="tab-selected"),
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
                dcc.Graph(id='heatmap_plot', figure=fig_heatmap, style={"margin-top": "20px", 'float': 'right'}),
                dcc.Graph(id='barchart', figure=fig_bar, style={"margin-top": "20px", 'width': '95%', 'float': 'right'})
        ], style={'display': 'flex', 'width': '100%', 'height': '100%', 'textAlign': 'center', 'justify-content': 'space-between'}),
         html.Div([
            html.Div([
                html.H2("Model Accuracy: "),
                html.H2(str(round(metrics.get('Accuracy'), 2)), style={"color": "#ff5252", "margin-left": "10px"}),
                html.H2("Model Precision: ", style={"margin-left": "20px"}),
                html.H2(str(round(metrics.get('Precision'), 2)), style={"color": "#ff5252", "margin-left": "10px"}),
            ], style={'display': 'flex', 'justify-content': 'center'}),
            html.Div([
                html.H2("Model Recall: "),
                html.H2(str(round(metrics.get('Recall'), 2)), style={"color": "#ff5252", "margin-left": "10px"}),
                html.H2("Model F1-Score: ", style={"margin-left": "20px"}),
                html.H2(str(round(metrics.get('F1-score'), 2)), style={"color": "#ff5252", "margin-left": "10px"}),
            ], style={'display': 'flex', 'justify-content': 'center'})
            ], style={'justify-content': 'center'})

    ], style={'height': '100%', 'width:': '100%'})



@app.callback(
    Output('bar-chart-container', 'children'),
    # Output('url-input', 'value'),
    Input('url-submit-button', 'n_clicks'),
    State('url-input', 'value'),
)
def bar_chart_tab(n_clicks, url):
    # Get article
    article = url_to_article(url)

    # Preprocess article text
    processed_article = preprocess_article(article.text)

    response = model_request(processed_article[:500])

    # Response to dict
    dict_data = json.loads(response.text)

    # For testing
    #dict_data = json.loads("{\"result\": true, \"scoere\": 0.5, \"explanation\": [[\"war\",1], [\"warr\",0],[\"warrr\",0.5],[\"warrrrr\",-0.5], [\"desinformation\",-1]]}")

    chart_data = pd.DataFrame(dict_data['explanation'])

    # Make colors dependency on value
    colors = pd.DataFrame(['colors'])
    i = 0
    for elem in chart_data.iloc[:, 1]:
        if elem < 0:
            colors.loc[i] = 'Fake'
        else:
            colors.loc[i] = 'Neutral'
        i = i + 1
    chart_data.append(colors)
    concated_data = pd.concat([chart_data, colors], axis=1)

    concated_data.columns = ['x', 'y', 'colors']

    chart = px.bar(concated_data, x='x', y='y',
                   color='colors',
                   color_discrete_map={
                       'Fake': '#ff5252',
                       'Neutral': 'green'
                   })
    chart.update_layout(plot_bgcolor='#2B2E33')
    chart.update_layout(paper_bgcolor='#2B2E33')
    chart.update_xaxes(title='')
    chart.update_yaxes(title='Fake               -               Real')
    chart.update_layout(title="Words with most impact", title_x=0.5)
    chart.update_layout(
        legend=dict(
            yanchor="middle",
            y=0.5
        )
    )

    # Result convert to text
    res = "Fake" if dict_data['result'] else "Neutral"

    # create a scatter plot using Plotly Express
    return html.Div(
        [
            html.Div([
                html.H2("Result: "),
                html.H2(res, style={"color": "#ff5252", "margin-left": "10px"}),
                html.H2("Score: ", style={"margin-left": "100px"}),
                html.H2(dict_data['scoere'], style={"color": "#ff5252", "margin-left": "10px"}),
            ], style={'display': 'flex', 'justify-content': 'center', "margin-top": "20px"}),
            dcc.Graph(id='bar-chart', figure=chart, style={"margin-top": "20px"})
        ]
    )


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
    processed_message = preprocess_message(message)

    # Case model matching request
    response = case_matching(processed_message, slider)

    # test_response = "[{\"score\": 0.9,\"title\": \"The title of the disinformation case\",\"content\": \"The description of the disinformation case\"}," \
    #                "{\"score\": 0.5,\"title\": \"The title of test\",\"content\": \"The description of the test case\"}]"
    array = json.loads(response.text)  # should be response.text

    div_children = [html.Div(id=f"div-{obj['score']}",
                             children=visualise_match(obj['score'], obj['title'], obj['content'])) for obj in array]

    return div_children


app.layout = html.Div([content])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True)

