from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from trade.decorators import user_login_required
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import User
from django.shortcuts import redirect
from django.core import serializers
from .models import Records, User
from django.http import JsonResponse
from trade.helpers import strip_space
from trade.tasks import generate_profit_loss

generate_profit_loss()


@user_login_required
def retrieve_stock_update(request):
    generate_profit_loss()
    if request.method == "GET":
        records = Records.objects.filter(user=request.user).order_by('time').values()
        #serialized_records = serializers.serialize("json", records)
        if not records:
            built_record = [{
                "initial_value": request.user.initial_deposit,
                "profit_loss": 0.00,
                "current_value": request.user.initial_deposit,
                "time": request.user.date_joined,
                "user": request.user.id
            }]
            return JsonResponse(built_record, safe=False, content_type="application/json")
        return JsonResponse(list(records), safe=False)

@user_login_required
def buy_stock(request):
    generate_profit_loss()
    if request.method == "POST":
        pass
    else:
        return render(request, "user/buy-stock.html", {})


@user_login_required
def overview(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "user/overview.html", {})
        

def register(request):
    if request.method == "POST":
        first_name = strip_space(request.POST.get("first_name"))
        last_name = strip_space(request.POST.get("last_name"))
        email = strip_space(request.POST.get("email"))
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        admin_status = request.POST.get("admin_status")


        if not first_name or not last_name or not email or not password or not confirm_password:
            return render(request, "user/register.html", {
                "message": "All fields must be validated to continue",
            })
        
        
        check_email = User.objects.filter(email=email).first()
    
        if check_email:
            return render(request, "user/register.html", {
                "message": "Email already registered",
            }) 
        
        if password != confirm_password:
            return render(request, "user/register.html", {
                "message": "Passwords do not match"
            })
        
        try:
            user = User(
                first_name = first_name.capitalize(),
                last_name=last_name.capitalize(),
                email=email,
                is_admin=True if admin_status else False
            )
            user.set_password(password)
            user.full_clean()
        except ValidationError:
            return render(request, "user/register.html", {
                "message": "Ensure the email is correct"
            })
        
        user.save()
        login(request, user)
        return redirect("user:overview")
    else:
        return render(request, "user/register.html", {})

def index(request):
    if request.method == "POST":
        email = strip_space(request.POST.get("email"))
        password = strip_space(request.POST.get("password"))

        check_user=User.objects.filter(email=email).first()
        if not check_user:
            return render(request, "user/login.html", {
                "message": "This user does not exist"
            })

        if not check_password(password, check_user.password):
            return render(request, "user/login.html", {
                "message": "Incorrect Password"
            })

        if check_user:
            login(request, check_user)
            return redirect("user:overview")
        else:
            return redirect("user:index")
    else:
        if request.user.is_authenticated:
            return redirect("user:overview")
        return render(request, "user/login.html", {})

def logout_view(request):
    logout(request)
    return redirect("user:index")