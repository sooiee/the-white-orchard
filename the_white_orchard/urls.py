from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('reservations/', include('reservations.urls')),
]

handler404 = 'django.views.defaults.page_not_found'
