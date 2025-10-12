from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TimeSlot(models.Model):
    """Available booking time slots"""
    SLOT_CHOICES = [
        ('11:00', '11:00 AM - Morning Tea'),
        ('13:00', '1:00 PM - Afternoon Tea'),
        ('15:00', '3:00 PM - Afternoon Tea'),
        ('17:00', '5:00 PM - Evening Tea'),
    ]
    
    time = models.CharField(max_length=5, choices=SLOT_CHOICES, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return dict(self.SLOT_CHOICES)[self.time]


class Reservation(models.Model):
    """Customer table reservations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Customer Information
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    
    # Booking Details
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    number_of_guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    special_requests = models.TextField(blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.customer_name} - {self.date}"


class MenuItem(models.Model):
    """Menu items for display"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name
    