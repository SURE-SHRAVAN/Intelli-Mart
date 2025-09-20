from django.shortcuts import render

# Create your views here.

def register(request):
    return render(request, 'users/register.html')   
def login(request):
    return render(request, 'users/login.html')  
def index(request):
    return render(request, 'users/index.html')  
 
def products(request):
    return render(request, 'users/products.html')