from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_reservation, name='create_reservation'),
    path('<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('list/', views.reservation_list, name='reservation_list'),
]
