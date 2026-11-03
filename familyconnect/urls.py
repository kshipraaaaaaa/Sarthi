from django.urls import path
from django.http import HttpResponse
from . import views
urlpatterns = [
    path('', views.family_home, name='family_home'),
    path('connect/', views.connect_parent, name='connect_parent'),
    path('respond/<int:connection_id>/', views.respond_connection, name='respond_connection'),
    path('location-sharing/', views.location_sharing, name='location_sharing'),
    path('update-location/', views.update_location, name='update_location'),
    path('parent-location/', views.parent_location, name='parent_location'),
]
