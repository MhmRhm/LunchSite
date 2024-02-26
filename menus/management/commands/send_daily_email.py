from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time
from menus.tasks import send_daily_email


class Command(BaseCommand):
    help = "Sends daily email"

    def handle(self, *args, **options):
        send_daily_email()
        self.stdout.write(
            self.style.SUCCESS("Daily emails sent successfully at 8:00 AM.")
        )
