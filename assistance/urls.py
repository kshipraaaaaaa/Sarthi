from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.create_request, name='create_request'),
    path('my-activities/', views.my_activities, name='my_activities'),
    
    path('request/', views.create_request, name='create_request'),
    path('my-activities/', views.my_activities, name='my_activities'),

    path('available/', views.available_requests, name='available_requests'),
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('volunteer-activities/', views.volunteer_activities, name='volunteer_activities'),


]