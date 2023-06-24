from django.urls import path, include
from . import views

app_name = "adminUser"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("overview/", views.overview, name="overview"),
    path("user/all/", views.all_users, name="all_users"),
]