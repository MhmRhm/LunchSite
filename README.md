# LunchSite
A Food Ordering System for My Workplace

Get it running on your server:
```bash
tree -L 1
# .
# ├── LICENSE
# ├── LunchSite
# ├── manage.py
# ├── menus
# └── README.md
# 
# 2 directories, 3 files

#make sure python<VERSION>-venv is installed
python3 -m venv .venv

source .venv/bin/activate

python -m pip install Django
python -m pip install django-crispy-forms
python -m pip install crispy-bootstrap4

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8172
```
