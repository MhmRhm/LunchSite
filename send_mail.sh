#!/bin/bash
cd /path/to/LunchSite
source .venv/bin/activate
python manage.py send_daily_email
deactivate
