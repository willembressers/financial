import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app


def filter_df(df, year=None, month=None):
    if year is not None:
        df = df[df['year'] == year]
    if month is not None:
        df = df[df['month'] == month]
    return df


def generate_table(df, max_rows=100):
    columns = [column for column in df.columns if column not in ['year', 'month']]
    return html.Table(
        [html.Tr([html.Th(column) for column in columns])] +
        [html.Tr([
            html.Td(df.iloc[row][column]) for column in columns
        ]) for row in range(min(len(df), max_rows))]
    )


def generate_graph(df):
    columns = [column for column in df.columns if column not in ['date', 'year', 'month']]
    return {'data': [go.Bar(x=columns, y=df[columns].sum(axis=0))]}


data = pd.\
    read_csv('data/anotated.csv', encoding="ISO-8859-1").\
    add_date_columns()

pivoted = data.\
    pivot_table(index='date', columns='label', values='amount', aggfunc=np.sum, fill_value=0).\
    reset_index().\
    add_date_columns()

layout = html.Div(id='labels', children=[
    html.Div(children=[
        dcc.Dropdown(
            id="year",
            options=[{'label': year, 'value': year} for year in pivoted['year'].unique()],
            value=pivoted['year'].unique()[-1]
        ),
        dcc.Dropdown(id="month")
    ]),
    dcc.Graph(id='graph'),
    html.Div(id='table'),
])


@app.callback(Output("month", "options"), [Input('year', 'value')])
def month_options(year):
    return [{'label': month, 'value': month} for month in filter_df(pivoted, year)['month'].unique()]


@app.callback(Output('month', 'value'), [Input('month', 'options')])
def month_value(months):
    return months[-1]['value']


@app.callback(Output('table', 'children'), [Input('graph', 'hoverData'), Input('year', 'value'), Input('month', 'value')])
def display_table(hover_data, year, month):
    df = filter_df(data, year, month)
    if hover_data is not None:
        df = df[df['label'] == hover_data['points'][0]['x']]
    return generate_table(df)


@app.callback(Output('graph', 'figure'), [Input('year', 'value'), Input('month', 'value')])
def display_graph(year, month):
    df = filter_df(pivoted, year, month)
    return generate_graph(df)
