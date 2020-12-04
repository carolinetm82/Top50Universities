from dash.dependencies import Input, Output
from layouts import df,urllib
from app import app

@app.callback(
    Output('download-link', 'href'),
    Input('table', 'value'))
def update_download_link(filter_value):
    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

'''
@app.callback(
    Output('app-2-display-value', 'children'),
    Input('app-2-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)
'''