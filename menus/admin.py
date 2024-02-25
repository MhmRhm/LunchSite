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
    list_display = ["employee", "menu", "selected_meal", "date"]
    list_filter = ["employee", "menu", "date"]
    search_fields = ["employee__get_full_name", "menu__name", "selected_meal__name"]
    date_hierarchy = "date"


@admin.register(DeliveryPayment)
class DeliveryPaymentAdmin(admin.ModelAdmin):
    list_display = ["menu", "date", "debt"]
    list_filter = ["menu", "date"]


@admin.register(ChefPayment)
class ChefPaymentAdmin(admin.ModelAdmin):
    list_display = ["menu", "date", "debt"]
    list_filter = ["menu", "date"]


admin.site.register(Menu, MenuAdmin)
admin.site.register(Meal, MealAdmin)
