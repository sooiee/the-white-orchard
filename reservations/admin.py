from django.contrib import admin
from .models import TimeSlot, Reservation, MenuItem, Enquiry


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
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Booking Details', {
            'fields': ('date', 'time_slot', 'number_of_guests', 'special_requests')
        }),
        ('Status', {
            'fields': ('status',)
        }),
    )


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_responded')
    list_filter = ('is_responded', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Enquiry Details', {
            'fields': ('subject', 'message')
        }),
        ('Admin', {
            'fields': ('is_responded', 'admin_notes')
        }),
    )