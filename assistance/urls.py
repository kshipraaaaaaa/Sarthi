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

    path('emergency-contacts/', views.emergency_contacts, name='emergency_contacts'),

    path('emergency-contacts/edit/<int:contact_id>/', views.edit_emergency_contact, name='edit_emergency_contact'),
    
    path('emergency-contacts/delete/<int:contact_id>/', views.delete_emergency_contact, name='delete_emergency_contact'),
    
]
