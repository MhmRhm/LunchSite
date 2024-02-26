#!/bin/bash
cd /home/mohammad/repos/lunch_site
source .venv/bin/activate
python manage.py send_daily_email
deactivate
