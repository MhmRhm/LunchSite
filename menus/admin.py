from django.contrib import admin
from .models import Menu, Meal, Employee, MenuSelection, DeliveryPayment, ChefPayment


class MealInline(admin.TabularInline):
    model = Menu.meals.through
    extra = 1


class MenuAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "get_meals"]
    fieldsets = [
        (None, {"fields": ["name", "description", "employee_limit"]}),
        ("Date information", {"fields": ["expire_at"]}),
    ]
    inlines = [MealInline]


class MealAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price"]
    search_fields = ["name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["get_full_name", "balance"]


@admin.register(MenuSelection)
class MenuSelectionAdmin(admin.ModelAdmin):
    list_display = ["employee", "menu", "selected_meal", "date", "is_paid_for"]
    list_filter = ["menu", "selected_meal", "date", "employee"]
    search_fields = ["employee__get_full_name", "menu__name", "selected_meal__name"]
    date_hierarchy = "date"


@admin.register(DeliveryPayment)
class DeliveryPaymentAdmin(admin.ModelAdmin):
    change_list_template = "admin/custom_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            response.context_data["debt"] = 0
            debt = 0
            for payment in DeliveryPayment.objects.all():
                debt += payment.debt
            response.context_data["debt"] = debt
        except:
            pass

        return response

    list_display = ["menu", "date", "debt"]
    list_filter = ["menu", "date"]


@admin.register(ChefPayment)
class ChefPaymentAdmin(admin.ModelAdmin):
    change_list_template = "admin/custom_change_list.html"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            response.context_data["debt"] = 0
            debt = 0
            for payment in ChefPayment.objects.all():
                debt += payment.debt
            response.context_data["debt"] = debt
        except:
            pass

        return response

    list_display = ["menu", "date", "debt"]
    list_filter = ["menu", "date"]


admin.site.register(Menu, MenuAdmin)
admin.site.register(Meal, MealAdmin)
