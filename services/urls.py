from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.create_request, name='create_request'),
    path('my-activities/', views.my_activities, name='my_activities'),
]