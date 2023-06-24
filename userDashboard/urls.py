from django.urls import path, include
from . import views

app_name = "user"

urlpatterns = [
    path("", views.index, name="index"),
    path("stock/buy/", views.buy_stock, name="buy_stock"),
    path("stock/records/", views.retrieve_stock_update, name="retrieve_records"),
    path("register/", views.register, name="register"),
    path("overview/", views.overview, name="overview"),
    path("logout/", views.logout_view, name="logout"),
]