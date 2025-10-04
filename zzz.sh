#!/bin/bash

cd path/to/smart_study_planner

python3 -m venv venv
source venv/bin/activate

python3 --version

pip install -r requirements.txt

python app.py

