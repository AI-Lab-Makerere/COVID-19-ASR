# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as da
# Multi-dropdown options
from controls import TIMESCALE,KEYWORDS

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server

# Create controls
keyword_options = [
    {"label": str(KEYWORDS[key_words]), "value": str(key_words)}
    for key_words in KEYWORDS
]

time_options = [
    {"label": str(TIMESCALE[time_scale]), "value": str(time_scale)}
    for time_scale in TIMESCALE
]


# Load data
df = pd.read_csv(DATA_PATH.joinpath("radio.csv"), low_memory=False)
df["date"] = pd.to_datetime(df["date"])






# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("moh.png"),
                            id="plotly-image",
                            style={
                                "height": "180px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "COVID-19 Analysis",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Overview of the Voices from the Public", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("View Details", id="learn-more-button"),
                            href="#",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Select by Date:",
                            className="control_label",
                        ),
                        dcc.DatePickerSingle(
                            id='stream-date',
                            min_date_allowed=da(2020, 6, 1),
                            max_date_allowed=da(2020, 6, 7),
                            initial_visible_month=da(2020, 6, 1),
                            date=str(da(2020, 6, 25, 23, 59, 59)),
                            className="dcc_control",
                            ),

                        html.P("Filter by Keywords:", className="control_label"),
                        dcc.RadioItems(
                            id="keywords_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="All",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="key_words",
                            options=keyword_options,
                            multi=True,
                            value=list(KEYWORDS.keys()),
                            className="dcc_control",
                        ),
                        html.P("Filter by Time Frame:", className="control_label"),
                        dcc.RadioItems(
                            id="timescale_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Customize ", "value": "custom"},
                            ],
                            value="All",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="time_scale",
                            options=time_options,
                            multi=True,
                            value=list(TIMESCALE.keys()),
                            className="dcc_control",
                        ),

                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="hits"), html.P("No. of hits")],
                                    id="hitsd",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="keywords"), html.P("Active keywords")],
                                    id="gas",
                                    className="mini_container",
                                ),

                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="count_graph",
                                    figure={
                                        'data': [
                                            {'x': df.keyword, 'y': df.start, 'type': 'bar'}
                                        ],
                                        'layout': {
                                            'title': 'Daily Hits',
                                            'xaxis':{'title': 'Keyword'},
                                            'yaxis': {'title': 'Time'}
                                        }
                                    }

                            )],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),

    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)








# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("count_graph", "figure")],
)




# Radio -> multi
@app.callback(
    Output("keywords", "value"), [Input("keywords_selector", "value")]
)
def display_status(selector):
    if selector == "all":
        return list(KEYWORDS.keys())
    elif selector == "custom":
        return ["CD", "CA", "LA", "SS", "AK"]
    return []


# Radio -> multi
@app.callback(Output("time_scale", "value"), [Input("timescale_selector", "value")])
def display_type(selector):
    if selector == "all":
        return list(TIMESCALE.keys())
    elif selector == "custom":
        return ["MO", "BK", "LM", "MD", "AN", "LN", "EV", "LE","MN"]
    return []





# # Selectors -> main graph
# @app.callback(
#     Output("count_graph", "figure"),
#     [
#         Input("key_words", "value"),
#         Input("time_scale", "value"),
#         Input("stream-date", "value"),
#     ],)
# def make_main_figure(key_words, time_scale, stream_date):
#
#     return 0
#
#
#
#
# # Selectors -> well text
@app.callback(
    [Output("hits", "children"),Output("keywords", "children")],
    [
        Input("key_words", "value"),
        Input("time_scale", "value"),
        Input("stream-date", "value"),
    ],
)
def update_summary(key_words, time_scale,stream):

    return [len(df),len(df.groupby(['keyword']))]






# Main
if __name__ == "__main__":
    app.run_server(debug=True)
