from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Reservation
from .forms import ReservationForm

def create_reservation(request):
    """Handle reservation creation"""
    
    if request.method == 'POST':
        # User submitted the form
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            # Save to database
            reservation = form.save()
            
            # Show success message
            messages.success(
                request,
                f'Reservation confirmed for {reservation.customer_name} on {reservation.date}!'
            )
            
            # Redirect to confirmation page
            return redirect('reservation_detail', pk=reservation.pk)
        else:
            # Form has errors
            messages.error(request, 'Please correct the errors below.')
    else:
        # GET request - show empty form
        form = ReservationForm()
    
    return render(request, 'reservations/create.html', {'form': form})


def reservation_detail(request, pk):
    """Show reservation confirmation"""
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(request, 'reservations/detail.html', {'reservation': reservation})


def reservation_list(request):
    """List all reservations (for admin)"""
    reservations = Reservation.objects.all().order_by('-date')
    return render(request, 'reservations/list.html', {'reservations': reservations})