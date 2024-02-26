# LunchSite
A Food Ordering System for My Workplace

Get it running on your server:
```bash
tree -L 1
# .
# ├── db.sqlite3
# ├── LICENSE
# ├── LunchSite
# ├── manage.py
# ├── menus
# ├── README.md
# └── send_mail.sh
# 
# 2 directories, 3 files

# find current time
date
# adjust the addresses in send_mail.sh
chmod +x send_mail.sh
# add the crontab schedule for remainder email at noon
# 0 12 * * * /bin/bash /home/mohammad/repos/LunchSite/send_mail.sh
crontab -e

#make sure python<VERSION>-venv is installed
python3 -m venv .venv

source .venv/bin/activate

python -m pip install Django
python -m pip install django-crispy-forms
python -m pip install crispy-bootstrap4
python -m pip install python-dotenv

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8172
```
You also need to put your `SECRET_KEY`, `EMAIL_HOST`, `EMAIL_HOST_USER`,
`EMAIL_HOST_PASSWORD` from _settings.py_ in the _.env_ file.
