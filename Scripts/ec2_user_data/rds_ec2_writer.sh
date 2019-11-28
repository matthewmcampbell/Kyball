#!/bin/bash
yum update -y
yum install git -y
yum install python3 -y
git clone https://github.com/Kylexi/Kyball.git
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python3 get-pip.py
pip install pandas mysql-connector-python --user