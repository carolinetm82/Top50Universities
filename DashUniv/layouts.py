import dash_core_components as dcc
import dash_html_components as html
import dash_table
import urllib

from functions import *


# Create an index page for homepage
index_page = html.Div([
    dcc.Link('Go to Page 1', href='/apps/app1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/apps/app2'),
])

# Create page 1
layout1 = html.Div([
    html.H4(children='The 50 best ranked universities (2016)'),
    # Create the data table containing the universities dataset
    dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=10,
    style_table={'overflowX': 'auto'},
    id='table'
),
    # Create a button in order to download the data
    html.A(
        html.Button('Download Data'),
        id='download-link',
        download="rawdata.csv",
        href="",
        target="_blank"
    ),
    # Putting a Dropdown
    dcc.Dropdown(
        id='dropdown-univ',
        options=[{'label': i, 'value': i} for i in df2['country'].unique()],
        value='United States of America',
        placeholder="Select a country",
    ),

    # Display scatter plot research vs rank
    dcc.Graph(
        id='research-vs-world_rank'
    ),

    # Display bar plot
    dcc.Graph(
        id='top five',
        figure=fig2
    ),

    # Display bubble chart
        dcc.Graph(
        id='bubble-fig-3',
        figure=fig3
    ),



    # Display links to other pages
    html.Br(),
    dcc.Link('Go to Page 2', href='/apps/app2'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])


# Create page 2
layout2 = html.Div([
    html.H3('Principal Components Analysis'),

    # Display pca matrix
    dcc.Graph(
        id='pca-matrix',
        figure=fig4
    ),
    # Display explained variance graph
        dcc.Graph(
        id='pca-explained',
        figure=fig5
    ),
    # Display visualization
        dcc.Graph(
        id='pca-eigenvalues',
        figure=fig6
    ),
    # Display heatmap
        dcc.Graph(
        id='pca-heatmap',
        figure=fig7
    ),
    dcc.Link('Go to Page 1', href='/apps/app1'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
])