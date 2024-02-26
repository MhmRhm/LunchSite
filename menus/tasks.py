import os
from datetime import time
from .models import Employee
from django.core.mail import send_mail
from dotenv import load_dotenv

def send_daily_email():
    load_dotenv()
    
    subject = "Daily Lunch Remainder"
    message = "Check the status at: 192.168.1.126:8172"
    employees = Employee.objects.all()
    recipient_list = [
        employee.user.email for employee in employees if len(employee.user.email) != 0
    ]
    
    print(os.getenv("EMAIL_HOST_USER"), recipient_list)
    send_mail(subject, message, os.getenv("EMAIL_HOST_USER"), recipient_list)
