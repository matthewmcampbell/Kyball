#!/bin/bash
#Script to get requirements all setup, including Django-plotly-dash initial config

git clone https://github.com/GibbsConsulting/django-plotly-dash
cd django-plotly-dash
./make_env

pip3 install pandas django-plotly-dash
