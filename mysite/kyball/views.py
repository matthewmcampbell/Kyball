import dash
import dash_core_components as dcc
import dash_html_components as html
import mysql.connector
import os

from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
from .plotly.graph_update import update_graph_info, initial_query
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'kyball/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_data')[:5]


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'db_access_info.txt')

try:
    file   = list(open(filename, 'r').readlines())
    host   = file[0].strip()
    user   = file[1].strip()
    passwd = file[2].strip()
except:
    host = None
    user = None
    passwd = None

database = "Kyball_db"

max_connect_attempts = 1000
attempts = 0

while attempts < max_connect_attempts:
    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            passwd = passwd,
            database = database
        )
        mycursor = connection.cursor(buffered=True)
        dfs = initial_query(mycursor)
        break
    except:
        mycursor = None
        dfs = None
        attempts += 1  

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash("kyball_graph", external_stylesheets=external_stylesheets)

# app.layout = html.Div([
#     html.Div([
#         html.Div([
#             html.H3('Column 1'),
#             dcc.Graph(id='g1', figure={'data': [{'y': [1, 2, 3]}]})
#         ], className="six columns"),

#         html.Div([
#             html.H3('Column 2'),
#             dcc.Graph(id='g2', figure={'data': [{'y': [1, 2, 3]}]})
#         ], className="six columns"),
#     ], className="row"),
#     html.Div(
#     children=["Enter Name: ",dcc.Input(id='name', value='Babe Ruth', type='text', debounce=True)],  # fill out your Input however you need
#     style=dict(display='flex', justifyContent='center')
#     )
# ])

# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Br(),
    html.Div(
    children=["Enter Name: ",dcc.Input(id='name', value='Babe Ruth', type='text', debounce=True)],  # fill out your Input however you need
    style=dict(display='flex', justifyContent='center')
    )
])

@app.callback(
    Output('graph', 'figure'),
    [Input('name', 'value')])
def update_figure(name):
    return update_graph_info(name, dfs)