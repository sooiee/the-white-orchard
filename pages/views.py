from django.shortcuts import render, redirect
from django.contrib import messages
from reservations.models import MenuItem
from reservations.forms import EnquiryForm


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


def contact(request):
    """Contact page with enquiry form"""
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Thank you for your enquiry! We will respond within 24 hours.'
            )
            return redirect('contact')
    else:
        form = EnquiryForm()
    
    return render(request, 'pages/contact.html', {'form': form})