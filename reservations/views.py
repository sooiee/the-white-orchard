from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Reservation
from .forms import ReservationForm


def create_reservation(request):
    """Handle reservation creation"""
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        
        if form.is_valid():
            reservation = form.save(commit=False)
            # Link to user account if authenticated
            if request.user.is_authenticated:
                reservation.user = request.user
            reservation.save()
            messages.success(
                request,
                f'Reservation confirmed for {reservation.customer_name} on '
                f'{reservation.date}!'
            )
            return redirect('reservation_detail', pk=reservation.pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReservationForm()
        # Pre-fill email for authenticated users
        if request.user.is_authenticated:
            form.initial['customer_email'] = request.user.email
    
    return render(request, 'reservations/create.html', {'form': form})


def reservation_detail(request, pk):
    """Show reservation confirmation"""
    reservation = get_object_or_404(Reservation, pk=pk)
    return render(
        request,
        'reservations/detail.html',
        {'reservation': reservation}
    )


def reservation_list(request):
    """List all reservations (for admin)"""
    reservations = Reservation.objects.all().order_by('-date')
    return render(
        request,
        'reservations/list.html',
        {'reservations': reservations}
    )


@login_required
def my_bookings(request):
    """Display user's bookings"""
    if request.user.is_authenticated:
        # Get bookings linked to user account OR email (backward compatibility)
        reservations = Reservation.objects.filter(
            Q(user=request.user) | Q(customer_email=request.user.email)
        ).select_related('time_slot').order_by('-date')
    else:
        reservations = []
    
    context = {
        'reservations': reservations,
    }
    return render(request, 'reservations/my_bookings.html', context)


@login_required
def edit_reservation(request, pk):
    """Edit a reservation"""
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Check if user owns this reservation (by user or email)
    owns_reservation = (
        reservation.user == request.user or
        reservation.customer_email == request.user.email or
        request.user.is_staff
    )
    
    if not owns_reservation:
        messages.error(
            request,
            'You do not have permission to edit this reservation.'
        )
        return redirect('my_bookings')
    
    # Check if reservation can be modified
    if not reservation.can_be_modified():
        messages.error(
            request,
            'This reservation cannot be modified '
            '(past date or cancelled).'
        )
        return redirect('my_bookings')
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your reservation has been updated successfully!'
            )
            return redirect('my_bookings')
    else:
        form = ReservationForm(instance=reservation)
    
    context = {
        'form': form,
        'reservation': reservation,
        'editing': True,
    }
    return render(request, 'reservations/edit.html', context)


@login_required
def cancel_reservation(request, pk):
    """Cancel a reservation"""
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Check if user owns this reservation (by user or email)
    owns_reservation = (
        reservation.user == request.user or
        reservation.customer_email == request.user.email or
        request.user.is_staff
    )
    
    if not owns_reservation:
        messages.error(
            request,
            'You do not have permission to cancel this reservation.'
        )
        return redirect('my_bookings')
    
    # Check if reservation can be cancelled
    if not reservation.can_be_cancelled():
        messages.error(
            request,
            'This reservation cannot be cancelled '
            '(past date or already cancelled).'
        )
        return redirect('my_bookings')
    
    if request.method == 'POST':
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Your reservation has been cancelled.')
        return redirect('my_bookings')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservations/cancel_confirm.html', context)


@login_required
def delete_reservation(request, pk):
    """Permanently delete a reservation from database"""
    reservation = get_object_or_404(Reservation, pk=pk)
    
    # Check if user owns this reservation (by user or email)
    owns_reservation = (
        reservation.user == request.user or
        reservation.customer_email == request.user.email or
        request.user.is_staff
    )
    
    if not owns_reservation:
        messages.error(
            request,
            'You do not have permission to delete this reservation.'
        )
        return redirect('my_bookings')
    
    # Allow deletion of any status (past, future, cancelled)
    if request.method == 'POST':
        reservation.delete()  # Hard delete from database
        messages.success(
            request,
            'Your reservation has been permanently deleted.'
        )
        return redirect('my_bookings')
    
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservations/delete_confirm.html', context)
