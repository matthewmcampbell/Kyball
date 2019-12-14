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


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import mysql.connector
from .plotly.graph_update import update_graph_info

host = "kyball-mysql.cjgpo2iwqpsx.us-east-1.rds.amazonaws.com"
user = "kylexi"
passwd = "Nine9clock!"
database = "Kyball_db"

connection = mysql.connector.connect(
    host = host,
    user = user,
    passwd = passwd,
    database = database
)
mycursor = connection.cursor(buffered=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = DjangoDash("kyball_graph", external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Graph(id='graph'),
    html.Div(
    children=["Enter Name: ",dcc.Input(id='name', value='Babe Ruth', type='text', debounce=True)],  # fill out your Input however you need
    style=dict(display='flex', justifyContent='center')
    )
])

@app.callback(
    Output('graph', 'figure'),
    [Input('name', 'value')])
def update_figure(name):
    return update_graph_info(name, mycursor)