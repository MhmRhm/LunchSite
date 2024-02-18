from django.db import models
from datetime import datetime

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    credit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Menu(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    expire_at = models.DateTimeField()
    meals = models.ManyToManyField('Meal', related_name='menus')

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class MenuSelection(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    selected_meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.employee.name}'s Selection for {self.menu.name}"
