from django.shortcuts import render
from reservations.models import MenuItem

def home(request):
    """Home page"""
    return render(request, 'pages/home.html')

def menu(request):
    """Menu page - shows all available items"""
    items = MenuItem.objects.filter(is_available=True)
    return render(request, 'pages/menu.html', {'items': items})

def about(request):
    """About page"""
    return render(request, 'pages/about.html')