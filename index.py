import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import labels, time_series


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1(children='Financieel Overzichts Boekje'),
    dcc.Link('Home', href='/'),
    html.Br(),
    dcc.Link('Labels', href='/apps/labels'),
    html.Br(),
    dcc.Link('Time series', href='/apps/time_series'),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/labels':
        return labels.layout
    elif pathname == '/apps/time_series':
        return time_series.layout
    else:
        return None


if __name__ == '__main__':
    app.run_server(debug=True)
