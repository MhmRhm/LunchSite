from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Menu, Employee, MenuSelection, Meal
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def index(request):
    menu = Menu.objects.last()
    meals = menu.meals.all()
    user = request.user
    employee = Employee.objects.get(user=user)

    menu_items = []
    for meal in meals:
        previous_order = MenuSelection.objects.filter(
            employee=employee, menu=menu, selected_meal=meal
        )
        menu_items.append({"meal": meal, "can_order": previous_order.count() == 0})

    return render(
        request,
        "menus/index.html",
        {
            "menu_items": menu_items,
            "menu": menu,
            "credit": employee.credit,
            "is_expired": menu.expire_at < timezone.now(),
        },
    )


@login_required
def order_meal(request, menu_id, meal_id):
    menu = Menu.objects.get(id=menu_id)
    meal = Meal.objects.get(id=meal_id)
    user = request.user
    employee = Employee.objects.get(user=user)

    if menu.expire_at > timezone.now():
        order = MenuSelection(employee=employee, menu=menu, selected_meal=meal)
        order.save()

    return index(request)


@login_required
def cancel_meal(request, menu_id, meal_id):
    menu = Menu.objects.get(id=menu_id)
    meal = Meal.objects.get(id=meal_id)
    user = request.user
    employee = Employee.objects.get(user=user)

    if menu.expire_at > timezone.now():
        order = MenuSelection.objects.get(
            employee=employee, menu=menu, selected_meal=meal
        )
        order.delete()

    return index(request)


@staff_member_required
def report_menu(request, menu_id):
    meals = Meal.objects.all()

    menus = Menu.objects.filter(is_paid_for=False)
    for menu in menus:
        if menu.expire_at < timezone.now():
            orders = MenuSelection.objects.filter(menu=menu).all()
            for order in orders:
                if not order.is_paid_for:
                    employees = order.employee
                    employees.credit -= order.selected_meal.price
                    order.is_paid_for = True
                    employees.save()
                    order.save()
            menu.is_paid_for = True
            menu.save()

    menu = Menu.objects.get(id=menu_id)
    meals_report = []
    for meal in meals:
        employees = [
            order.employee.user.get_full_name()
            for order in MenuSelection.objects.filter(menu=menu, selected_meal=meal)
        ]
        meals_report.append(
            {
                "meal": meal,
                "count": len(employees),
                "employees": ", ".join(employees),
            }
        )
    return render(request, "menus/report.html", {"meals_report": meals_report})
