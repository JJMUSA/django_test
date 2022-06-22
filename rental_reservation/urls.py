from django.urls import path
from .views import get_reservations

urlpatterns = [path('reservations', get_reservations)]