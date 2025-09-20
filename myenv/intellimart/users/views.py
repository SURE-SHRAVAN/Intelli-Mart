# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import Customer

# Registration View
def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation
        if not first_name or not email or not password or not confirm_password:
            messages.error(request, "Please fill all required fields.")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("register")

        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect("register")

        # Create user
        user = Customer.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )
        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "users/register.html")


# Login View
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome {user.first_name}!")
            return redirect("home")  # Redirect to your home page
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("login")

    return render(request, "users/login.html")


# Logout View
def logout(request):
    auth_logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("login")
