#!/bin/bash
cd django
source env/bin/activate
cd invfabrica
cd app
python manage.py runserver 0:8000
