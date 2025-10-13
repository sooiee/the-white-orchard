from django import forms
from .models import Reservation, Enquiry
from datetime import date


class ReservationForm(forms.ModelForm):
    """Form for creating and editing reservations"""
    
    class Meta:
        model = Reservation
        fields = [
            'customer_name',
            'customer_email', 
            'customer_phone',
            'date',
            'time_slot',
            'number_of_guests',
            'special_requests'
        ]
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'time_slot': forms.Select(attrs={'class': 'form-select'}),
            'number_of_guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 8
            }),
            'special_requests': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
        }
    
    def clean_date(self):
        """Validate date is not in the past"""
        booking_date = self.cleaned_data['date']
        
        if booking_date < date.today():
            raise forms.ValidationError("Cannot book a date in the past.")
        
        return booking_date


class EnquiryForm(forms.ModelForm):
    """Contact enquiry form"""
    class Meta:
        model = Enquiry
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }