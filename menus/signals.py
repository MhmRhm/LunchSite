from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Menu, DeliveryPayment


@receiver(post_save, sender=Menu)
def create_delivery_payment(sender, instance, created, **kwargs):
    if created:
        DeliveryPayment.objects.create(menu=instance, debt=0)
