from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Menu, Employee, MenuSelection, Meal
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def index(request):
    latest_menus = []
    user = request.user
    employee = Employee.objects.get(user=user)
    menus = Menu.objects.order_by("-expire_at")[:2].all()
    for menu in menus:
        meals = menu.meals.all()
        menu_items = []
        for meal in meals:
            can_order = (
                MenuSelection.objects.filter(
                    employee=employee, menu=menu, selected_meal=meal
                ).count()
                == 0
            )
            count = MenuSelection.objects.filter(menu=menu, selected_meal=meal).count()
            menu_items.append({"meal": meal, "count": count, "can_order": can_order})

        latest_menus.append(
            {
                "menu_items": menu_items,
                "menu": menu,
                "is_expired": menu.expire_at < timezone.now(),
            }
        )

    return render(
        request,
        "menus/index.html",
        {
            "recents": latest_menus,
            "balance": employee.balance,
        },
    )


@login_required
def order_meal(request, menu_id, meal_id):
    menu = Menu.objects.get(id=menu_id)
    meal = Meal.objects.get(id=meal_id)
    user = request.user
    employee = Employee.objects.get(user=user)

    spendings = 0
    orders = MenuSelection.objects.filter(employee=employee, menu=menu).all()
    for order in orders:
        spendings += order.selected_meal.price
    if employee.balance < (spendings + meal.price):
        return index(request)

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


@login_required
def report_menu(request, menu_id):
    meals = Meal.objects.all()

    menus = Menu.objects.filter(is_paid_for=False)
    for menu in menus:
        if menu.expire_at < timezone.now():
            orders = MenuSelection.objects.filter(menu=menu).all()
            for order in orders:
                if not order.is_paid_for:
                    count = MenuSelection.objects.filter(
                        menu_id=menu_id, selected_meal=order.selected_meal
                    ).count()
                    employee = order.employee
                    if count >= menu.employee_limit:
                        employee.balance -= order.selected_meal.price
                        order.is_paid_for = True
                        employee.save()
                        order.save()
                    else:
                        order.delete()
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
                "employees": employees,
            }
        )
    return render(request, "menus/report.html", {"meals_report": meals_report})
