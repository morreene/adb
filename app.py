"""
This app creates a responsive sidebar layout with dash-bootstrap-components and
some custom css with media queries.

When the screen is small, the sidebar moved to the top of the page, and the
links get hidden in a collapse element. We use a callback to toggle the
collapse when on a small screen, and the custom CSS to hide the toggle, and
force the collapse to stay open when the screen is large.

dcc.Location is used to track the current location. There are two callbacks,
one uses the current location to render the appropriate page content, the other
uses the current location to toggle the "active" properties of the navigation
links.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
# import pandas as pd
# import sqlite3
import datetime
# import os
# import urllib.parse

# # Create connection with sqlite
# cnx = sqlite3.connect('tpr-data.db')
# matrix = pd.read_sql_query("SELECT * FROM tpr_matrix", cnx)

# member_list = pd.read_sql_query("SELECT * FROM all_mem", cnx)
# member_list = member_list['Member'].tolist()
# member_list = ['All Members'] + member_list

# cat_list = pd.read_sql_query("SELECT * FROM all_cat", cnx)
# cat_list = cat_list['Topic'].tolist()
# cat_list = ['All topics (slow loading)'] + cat_list

# # df = pd.read_sql_query("SELECT * FROM tpr_sec_data_20191112 where Topic='1. economic environment'", cnx)
# cnx.close()

member_list = ['1','2']

cat_list = ['1','2']


external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']
# with "__name__" local css under assets is also included
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

app.title = 'TPR Report Data'
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-62289743-10"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'UA-62289743-10');
        </script>

        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""


server = app.server
app.config.suppress_callback_exceptions = True
# we use the Row and Col components to construct the sidebar header
# it consists of a title, and a toggle, the latter is hidden on large screens
sidebar_header = dbc.Row([
    dbc.Col(html.H3("Analytical Database", className="display-logo")),
    dbc.Col(
        html.Button(
            # use the Bootstrap navbar-toggler classes to style the toggle
            html.Span(className="navbar-toggler-icon"),
            className="navbar-toggler",
            # the navbar-toggler classes don't set color, so we do it here
            style={
                "color": "rgba(0,0,0,.5)",
                "bordercolor": "rgba(0,0,0,.1)",
            },
            id="toggle",
        ),
        # the column containing the toggle will be only as wide as the
        # toggle, resulting in the toggle being right aligned
        width="auto",
        # vertically align the toggle in the center
        align="center",
    ),
])

sidebar = html.Div([
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "Download integrated tariff and trade data for research and analysis",
                    # className="lead",
                ),
                # html.Br(),
                # html.Hr(),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Download with API", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Download 2", href="/page-2", id="page-2-link"),
                    dbc.NavLink("Inventory", href="/page-3", id="page-3-link"),
                    dbc.NavLink("Help", href="/page-4", id="page-4-link"),
                ],
                vertical=True,
                pills=False,
            ),
            id="collapse",
            # id="sidebar",
        ),

        html.Div(
            [
                html.Hr(),
                html.P(
                    "Version 20230228 Plotly Dash",
                    # className="lead",
                ),
                # html.Br(),
                # html.Hr(),
            ],
            id="blurb-bottom",
        ),
    ],
    id="sidebar",
)

content = html.Div(id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False, False
    return [pathname == f"/page-{i}" for i in range(1, 5)]

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        [
                        html.P('Select member'),
                        dcc.Dropdown(
                            id='dropdown_sec_member',
                            options=[{'label': i, 'value': i} for i in member_list],
                            # options=[{'label': i[0], 'value': i[1]} for i in member_tuples], # See above
                            value='Albania',
                            clearable=False
                        ),
                        ], width=2
                    ),
                    dbc.Col([
                        html.P('Select topic'),
                        dcc.Dropdown(
                            id='dropdown_sec_topic',
                            # options=[{'label': i, 'value': i} for i in ['Select','China', 'Argentina', 'Belgium']],
                            options=[{'label': i, 'value': i} for i in cat_list],
                            # multi=True,
                            # value='0. summary',
                            value='1. economic environment',
                            clearable=False
                        ),
                        ], width=4, align="center"
                    ),
                    dbc.Col(
                        [
                        html.P('Search by keywords ...'),
                        dbc.Input(id="input-sec-search", placeholder="Type something...", type="text", value=''),
                        # html.Span('  ', id="example-output", style={"vertical-align": "middle"}),
                        dbc.Button('Search', id="button-sec-search", className="mr-2", color="info",),
                        # html.Br(),
                        # html.P(id="output"),

                        ], width=6
                    ),
                ],
            ),
            html.Br(),

            dbc.Row(
                [
                    dbc.Col(
                        [
                        html.P('Search by keywords ...'),
                        dbc.Input(id="search-input", placeholder="Type something...", type="text", value=''),
                        # html.Span('  ', id="example-output", style={"vertical-align": "middle"}),
                        dbc.Button('Search', id="button-sec-search", className="mr-2", color="info",),
                        # html.Br(),
                        # html.P(id="output"),
                    
                        ], width=6
                    ),
                    dbc.Col(
                        [
                        html.P('Export results to Excel ...'),
                        # dbc.Button("Download", id="download-link", className="mr-3"),
                        html.Span(id="example-output", style={"vertical-align": "middle"}),
                        html.A(
                            # 'Download Data',
                            id='download-link',
                            download="data-report-sec-"+ datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".csv",
                            href="",
                            target="_blank",
                            children = [dbc.Button("Download", id="download-link2", className="mr-4", color="info",)]
                        )
                        ], width=6
                    ),
                ],
            ),
            html.Br(),
            html.Div(id='table-container')
        ])
    elif pathname == "/page-2":
        # return html.H5("THIS APP IS FOR TESTING PURPOSES ONLYYYYY.")
        return html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.P('Select member'),
                            dcc.Dropdown(
                                id='dropdown_gov_member',
                                options=[{'label': i, 'value': i} for i in member_list],
                                # options=[{'label': i[0], 'value': i[1]} for i in member_tuples], # See above
                                value='Albania',
                                clearable=False
                            ),
                        ], width=6
                    ),
                    dbc.Col(
                        [
                            html.P('Search ...'),
                            dbc.Input(id="input-gov-search", placeholder="Type something...", type="text", value=''),
                            # html.Span('  ', id="example-output", style={"vertical-align": "middle"}),
                            dbc.Button('Search', id="button-gov-search", className="mr-2", color="info",),
                            # html.Br(),
                            # html.P(id="output"),
                        ], width=6
                    ),
                ],
            ),
            html.Br(),
            html.Div(id='table-container-gov')
        ])
    elif pathname == "/page-3":
        # return html.P("This is the content of page 2. Yay!")
        return html.Div([
                html.H4('List of members, years and reports: value = document symbol numbers'),
                dash_table.DataTable(
                    id='table',
                    columns=[
            # {"name": i, "id": i} for i in matrix.columns
            ],
                    # data=matrix.to_dict('records'),
                    style_cell_conditional=[
                        {'if': {'column_id': 'Member'},
                         'width': '100px'},
                    ]
                )
            ])

    elif pathname == "/page-4":
        # return html.H5("THIS APP IS FOR TESTING PURPOSES ONLY.")
        return html.Div([
                    # dbc.Container(
                        # [
                            html.H4("About WTO Analytical Database", className="display-about"),
                            html.P(
                                "Download integrated tariff and trade data for research and analysis...",
                                className="lead",
                            ),
                            html.Hr(className="my-2"),
                            # html.P(
                            #     "Jumbotrons use utility classes for typography and "
                            #     "spacing to suit the larger container."
                            # ),
                            dcc.Markdown('''
                                            This web app provides acces ... .
                                            ## Section 1
                                            
                                            ```
                                            {
                                            "firstName": "John",
                                            "lastName": "Smith",
                                            "age": 25
                                            }
                                            ```

                                            * Each record in the database represents a paragraph of TPR reports.
                                            * Report texts can be retrieved by report section and/or by member, or searched by keywords.
                                            * The app is for testing purposes only. Please download the official reports from [the WTO website](https://www.wto.org/english/tratop_e/tpr_e/tpr_e.htm).
                                        '''
                                        ),
                        # ]
                    # )
                ])

    # If the user tries to reach a different page, return a 404 message
    return dbc.Container(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

# Page 1 dropdown control
@app.callback(
        [dash.dependencies.Output('table-container', 'children'),
         dash.dependencies.Output('download-link', 'href')
         ],
        [dash.dependencies.Input('dropdown_sec_topic', 'value'),
         dash.dependencies.Input('dropdown_sec_member', 'value'),
         dash.dependencies.Input('button-sec-search', 'n_clicks')],
        [dash.dependencies.State('input-sec-search', 'value')]
    )
def display_table(dropdown_value_1, dropdown_value_2, n_clicks, search_str):
    # dff = df[(df['Cat'].str.contains(dropdown_value_1)) & (df['ConcernedCountriesCode'].str.contains(dropdown_value_2))]

    # cnx = sqlite3.connect('tpr-data.db')
    # if (dropdown_value_1 == 'All topics (slow loading)') & (dropdown_value_2 == 'All Members'):
    #     df = pd.read_sql_query("SELECT * FROM tpr_sec_data", cnx)
    # elif (dropdown_value_1 == 'All topics (slow loading)') & (dropdown_value_2 != 'All Members'):
    #     df = pd.read_sql_query("SELECT * FROM tpr_sec_data WHERE Member='" + dropdown_value_2 + "'", cnx)
    # elif (dropdown_value_1 != 'All topics (slow loading)') & (dropdown_value_2 == 'All Members'):
    #         df = pd.read_sql_query("SELECT * FROM tpr_sec_data WHERE Topic='" + dropdown_value_1 + "'", cnx)
    # else:
    #     df = pd.read_sql_query("SELECT * FROM tpr_sec_data WHERE Topic='" + dropdown_value_1 + "' AND Member='" + dropdown_value_2 + "'", cnx)
    # cnx.close()

    # if df.empty:
    #     dff = pd.DataFrame.from_dict({'Member': ['NA'],'Symbol': ['NA'],'ReportDate': ['NA'],'Topic': ['NA'],'ParaID': ['NA'], 'Text': ['NA'], 'ID': ['NA']})
    # else:
    #     dff = df[
    #             (df['Text'].str.contains(search_str, case=False))
    #             ].copy()
    #     # dff['Member'] = dff.apply(lambda x: member_dict[x['MemberCode']], axis=1)
    #     # dff = dff.drop(['MemberCode'], axis=1)
    #     dff = dff[['Member','Symbol','ReportDate','Topic','ParaID','Text','ID']].sort_values(['Member','ReportDate','Topic','ID'])
    #     # download links
    #     csv_string = dff.head(1500).to_csv(index=False, encoding='utf-8')
    #     csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    csv_string = "sdfdsfsd"


    return html.Div([
            # dbc.Alert('SELECTION: topic="'+ dropdown_value_1 + '", member="' + dropdown_value_2 + '", search="' + search_str + '"', color="info"),
            # dbc.Alert(str(len(dff)) + ' papragraphs found for selection criteria: topic = "'+ dropdown_value_1 + '", member = "' + member_dict[dropdown_value_2] + '", search = "' + search_str + '"', color="info"),
            # dbc.Alert(str(len(dff)) + ' papragraphs found for selection criteria: topic = "'+ dropdown_value_1 + '", member = "' + dropdown_value_2 + '", search = "' + search_str + '"', color="info"),
            # html.Blockquote(str(len(dff)) + ' papragraphs found for selection criteria: topic = "'+ dropdown_value_1 + '", member = "' + dropdown_value_2 + '", search = "' + search_str + '"'),
            # dash_table.DataTable(
            #         id='tab',
            #         columns=[
            #             {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns if i != 'ID'
            #         ],
            #         data = dff.to_dict('records'),
            #         editable=False,
            #         # filter_action="native",
            #         sort_action="native",
            #         sort_mode="multi",
            #         column_selectable=False,
            #         row_selectable=False,
            #         row_deletable=False,
            #         selected_columns=[],
            #         selected_rows=[],
            #         page_action="native",
            #         page_current= 0,
            #         page_size= 20,
            #         style_cell={
            #         'height': 'auto',
            #         'minWidth': '50px', 'maxWidth': '180px',
            #         'whiteSpace': 'normal',
            #         'textAlign': 'left',
            #         },
            #         style_cell_conditional=[
            #             {'if': {'column_id': 'Symbol'},
            #              'width': '100px'},
            #             {'if': {'column_id': 'Member'},
            #              'width': '70px'},
            #             {'if': {'column_id': 'ReportDate'},
            #              'width': '90px'},
            #             {'if': {'column_id': 'Topic'},
            #              'width': '200px'},
            #             {'if': {'column_id': 'ParaID'},
            #              'width': '40px'},
            #         ]
            #     )
            ]), csv_string
# End of Download button
# # Page 2 dropdown control
@app.callback(
        [dash.dependencies.Output('table-container-gov', 'children'),
         # dash.dependencies.Output('download-link-gov', 'href')
         ],
        [dash.dependencies.Input('dropdown_gov_member', 'value'),
         dash.dependencies.Input('button-gov-search', 'n_clicks')],
        [dash.dependencies.State('input-gov-search', 'value')]
    )
def display_table(dropdown_value_gov_1, n_clicks, search_str):
    # # dff = df[(df['Cat'].str.contains(dropdown_value_1)) & (df['ConcernedCountriesCode'].str.contains(dropdown_value_2))]

    # cnx = sqlite3.connect('tpr-data.db')
    # # df = pd.read_sql_query("SELECT * FROM tpr_gov_data", cnx)
    # if (dropdown_value_gov_1 == 'All Memebers'):
    #     df = pd.read_sql_query("SELECT * FROM tpr_gov_data", cnx)
    # else:
    #     df = pd.read_sql_query("SELECT * FROM tpr_gov_data WHERE Member='" + dropdown_value_gov_1 + "' ", cnx)
    # cnx.close()

    # if df.empty:
    #     dff = pd.DataFrame.from_dict({'Member':['NA'],'Symbol':['NA'],'ReportDate':['NA'],'Topic':['NA'],'ParaID':['NA'],'Text':['NA'],'ID':['NA']})
    # else:
    #     dff = df[(df['Text'].str.contains(search_str, case=False))].copy()
    #     # dff['Member'] = dff.apply(lambda x: member_dict[x['MemberCode']], axis=1)
    #     # dff = dff.drop(['Member'], axis=1)
    #     # dff = dff[['Member','Symbol','ReportDate','Topic','ParaID','Text']]
    #     dff = dff[['Member','Symbol','ReportDate','Topic','ParaID','Text','ID']].sort_values(['Member','ReportDate','Topic','ID'])
    #     # dff = dff[['MemberCode','Symbol','ReportDate','Topic','ParaID','Text']]
    #     # download links
    # # csv_string = dff.head(1500).to_csv(index=False, encoding='utf-8')
    # # csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)

    return html.Div([
            # dbc.Alert(str(len(dff)) + ' papragraphs found for selection criteria: member = "' + dropdown_value_gov_1 + '", search = "' + search_str + '"', color="info"),
            # html.Blockquote(str(len(dff)) + ' papragraphs found for selection criteria: member = "' + dropdown_value_gov_1 + '", search = "' + search_str + '"'),
            # dash_table.DataTable(
            #         id='tab',
            #         columns=[
            #                     {"name": i, "id": i, "deletable": False, "selectable": False} for i in dff.columns if i != 'ID'
            #                 ],
            #         data = dff.to_dict('records'),
            #         editable=False,
            #         # filter_action="native",
            #         sort_action="native",
            #         sort_mode="multi",
            #         column_selectable=False,
            #         row_selectable=False,
            #         row_deletable=False,
            #         selected_columns=[],
            #         selected_rows=[],
            #         page_action="native",
            #         page_current= 0,
            #         page_size= 20,
            #         style_cell={
            #                     'height': 'auto',
            #                     'minWidth': '50px', 'maxWidth': '180px',
            #                     'whiteSpace': 'normal',
            #                     'textAlign': 'left',
            #                     },
            #         style_cell_conditional=[
            #                     {'if': {'column_id': 'Symbol'},
            #                      'width': '100px'},
            #                     {'if': {'column_id': 'Member'},
            #                      'width': '70px'},
            #                     {'if': {'column_id': 'ReportDate'},
            #                      'width': '90px'},
            #                     {'if': {'column_id': 'Topic'},
            #                      'width': '200px'},
            #                     {'if': {'column_id': 'ParaID'},
            #                      'width': '40px'},
            #                      ]
            #     )
            ]), #csv_string

@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)