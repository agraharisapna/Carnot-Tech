# api/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('device/<str:device_id>/', get_latest_device_info, name='get_latest_device_info'),
    path('device/<str:device_id>/locations/', get_start_end_locations, name='get_start_end_locations'),
    path('device/<str:device_id>/locations/<str:start_time>/<str:end_time>/', get_location_points, name='get_location_points'),
]
