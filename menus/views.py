from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from .models import Menu, Employee, MenuSelection, Meal, DeliveryPayment, ChefPayment
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    processMenus(request)

    latest_menus = []

    user = request.user
    employee = Employee.objects.get(user=user)

    menus = Menu.objects.order_by("-expire_at")[:1].all()

    for menu in menus:
        meals = menu.meals.all()
        menu_items = []

        for meal in meals:
            orders = MenuSelection.objects.filter(
                employee=employee, menu=menu, selected_meal=meal
            )
            can_order = orders.count() == 0
            is_vegi = orders.count() != 0 and meal.has_vegi and orders.all()[0].is_vegi
            count = MenuSelection.objects.filter(menu=menu, selected_meal=meal).count()
            menu_items.append(
                {
                    "meal": meal,
                    "count": count,
                    "can_order": can_order,
                    "is_vegi": is_vegi,
                }
            )

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
        spendings += order.selected_meal.cost()
    if employee.balance < (spendings + meal.cost()):
        return index(request)

    if menu.expire_at > timezone.now():
        order = MenuSelection(employee=employee, menu=menu, selected_meal=meal)
        order.save()

    return index(request)


@login_required
def order_vegi(request, menu_id, meal_id):
    menu = Menu.objects.get(id=menu_id)
    meal = Meal.objects.get(id=meal_id)
    user = request.user
    employee = Employee.objects.get(user=user)

    if menu.expire_at > timezone.now():
        if meal.has_vegi:
            order = MenuSelection.objects.filter(
                employee=employee, menu=menu, selected_meal=meal
            ).last()
            if order:
                order.is_vegi = not order.is_vegi
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
    processMenus(request)
    meals = Meal.objects.all()
    menu = Menu.objects.get(id=menu_id)
    meals_report = []
    for meal in meals:
        employees = [
            (order.employee.user.get_full_name(), meal.has_vegi and order.is_vegi)
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


def processMenus(request):
    menus = Menu.objects.filter(is_paid_for=False)
    for menu in menus:
        if menu.expire_at < timezone.now():
            delivery_share = 0
            chef_share = 0

            orders = MenuSelection.objects.filter(menu=menu).all()

            for order in orders:
                if not order.is_paid_for and not order.is_canceled:
                    count = MenuSelection.objects.filter(
                        menu=menu, selected_meal=order.selected_meal
                    ).count()

                    employee = order.employee
                    if count >= menu.employee_limit:
                        employee.balance -= order.selected_meal.price
                        chef_share += order.selected_meal.price
                        employee.balance -= order.selected_meal.delivery_share
                        delivery_share += order.selected_meal.delivery_share

                        order.is_paid_for = True

                        employee.save()
                        order.save()
                    else:
                        order.is_canceled = True
                        order.save()

            menu.is_paid_for = True
            menu.save()

            if delivery_share:
                payment = DeliveryPayment(
                    menu=menu, date=menu.expire_at, debt=delivery_share
                )
                payment.save()
            if chef_share:
                payment = ChefPayment(menu=menu, date=menu.expire_at, debt=chef_share)
                payment.save()
