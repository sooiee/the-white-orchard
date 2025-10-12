from django.contrib import admin
from .models import TimeSlot, Reservation, MenuItem

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('time', 'is_active')
    list_filter = ('is_active',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'date', 'time_slot', 'number_of_guests', 'status', 'created_at')
    list_filter = ('status', 'date', 'time_slot')
    search_fields = ('customer_name', 'customer_email', 'customer_phone')
    ordering = ('-date',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
