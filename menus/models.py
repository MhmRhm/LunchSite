from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def get_full_name(self):
        return self.user.get_full_name()

    def __str__(self):
        return self.get_full_name()


class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    expire_at = models.DateTimeField()
    meals = models.ManyToManyField("Meal", related_name="menus")
    is_paid_for = models.BooleanField(default=False)
    employee_limit = models.IntegerField(default=10)

    def get_meals(self):
        names = [meal.name for meal in self.meals.all()]
        return ", ".join(names)

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_share = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def cost(self):
        return self.price + self.delivery_share

    def __str__(self):
        return self.name


class MenuSelection(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    selected_meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    is_paid_for = models.BooleanField(default=False)

    class Meta:
        unique_together = ("employee", "menu", "selected_meal")

    def __str__(self):
        return f"{self.employee.user.get_full_name()}'s Selection for {self.menu.name}"


class DeliveryPayment(models.Model):
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Delivery Payment for {self.menu.name}"


class ChefPayment(models.Model):
    menu = models.OneToOneField(Menu, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Chef Payment for {self.menu.name}"
