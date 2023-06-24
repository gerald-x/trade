from django.shortcuts import render, redirect
from trade.decorators import admin_login_required
from django.contrib.auth import logout, login
from userDashboard.models import User, Records
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from trade.helpers import strip_space
from trade.tasks import generate_profit_loss


# Create your views here.
@admin_login_required
def all_users(request):
    if request.method == "POST":
        pass
    else:
        users = User.objects.all()
        users_data = []
        for user in users:
            first = Records.objects.filter(user=user).select_related("user").order_by("-time").first()
            if first:
                data = Records.objects.filter(pk=first.pk).values("initial_value", "profit_loss", "current_value", "time", "user__first_name", "user__last_name", "user__email", "user__initial_deposit", "user__time_created")
                users_data.append(list(data))
            else:
                user_object = User.objects.filter(id=user.id).values("first_name", "last_name", "email", "initial_deposit", "time_created",)
                users_data.append(list(user_object))
        return JsonResponse(users_data, safe=False)

@admin_login_required
def overview(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "admin/overview.html", {})

def login_view(request):
    if request.method == "POST":
        email = strip_space(request.POST.get("email"))
        password = request.POST.get("password")

        check_user=User.objects.filter(email=email).first()
        if not check_user:
            return render(request, "admin/login.html", {
                "message": "This user does not exist"
            })

        if not check_password(password, check_user.password):
            return render(request, "admin/login.html", {
                "message": "Incorrect Password"
            })
        
        if not check_user.is_admin:
            return render(request, "admin/login.html", {
                "message": "This user is not an admin."
            })

        if check_user:
            login(request, check_user)
            return redirect("adminUser:overview")
        else:
            return redirect("adminUser:login")
    else:
        return render(request, "admin/login.html", {
            "message": "user is not an admin" if request.GET.get("msg") else None
        })

