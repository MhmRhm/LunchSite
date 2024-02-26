from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("order/<int:menu_id>/<int:meal_id>/", views.order_meal, name="order_meal"),
    path("vegi/<int:menu_id>/<int:meal_id>/", views.order_vegi, name="order_vegi"),
    path("cancel/<int:menu_id>/<int:meal_id>/", views.cancel_meal, name="cancel_meal"),
    path("report/<int:menu_id>/", views.report_menu, name="report_menu"),
]
