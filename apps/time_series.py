import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html


def generate_graph(df):
    traces = []
    for column in [column for column in df.columns if column not in ['date', 'period']]:
        traces.append(go.Scatter(
            x=df.index,
            y=df[column],
            mode='lines',
            name=column
        ))
    return {'data': traces}


data = pd.\
    read_csv('data/anotated.csv', encoding="ISO-8859-1").\
    add_date_columns()

data['period'] = data['date'].dt.to_period("M").map(str)

pivoted = data.\
    pivot_table(index='period', columns='label', values='amount', aggfunc=np.sum, fill_value=0)

layout = html.Div(id='time_series', children=[
    dcc.Graph(figure=generate_graph(pivoted))
])
