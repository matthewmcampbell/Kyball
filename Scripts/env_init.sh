#!/bin/bash
#Script to get requirements all setup, including Django-plotly-dash initial config

apt-get install python3
apt-get install python3-pip

git clone https://github.com/GibbsConsulting/django-plotly-dash
cd django-plotly-dash
pip3 install -r requirements.txt
pip3 install -r dev_requirements.txt
#
python3 setup.py develop

pip3 install django-plotly-dash mysql-connector-python
