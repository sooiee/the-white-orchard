from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    path('<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('list/', views.reservation_list, name='reservation_list'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('edit/<int:pk>/', views.edit_reservation, name='edit_reservation'),
    path(
        'cancel/<int:pk>/',
        views.cancel_reservation,
        name='cancel_reservation'
    ),
    path(
        'delete/<int:pk>/',
        views.delete_reservation,
        name='delete_reservation'
    ),
]
