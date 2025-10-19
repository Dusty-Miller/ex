from django.urls import path
from . import views

urlpatterns = [
    path('sensor/', views.sensor_payload, name='sensor-payload'),
]
