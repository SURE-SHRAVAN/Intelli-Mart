from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def index(request):
    return render(request, "users/index.html")

# Register View
def register(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect("register")

        # Save user with hashed password
        user = User(fullname=fullname, email=email, password=make_password(password))
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return render(request, "users/login.html")

    return render(request, "users/register.html")


# Login View
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                # Store session
                request.session["user_id"] = user.id
                request.session["user_name"] = user.fullname
                return redirect("products")
            else:
                messages.error(request, "Invalid password!")
        except User.DoesNotExist:
            messages.error(request, "User not found!")

        return redirect("users/login.html")

    return render(request, "users/login.html")


# Products Page (after login)
def products(request):
    if "user_id" not in request.session:
        return redirect("user/login.html")  # force login if not logged in
    return render(request, "users/products.html", {"user_name": request.session["user_name"]})
