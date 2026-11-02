from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('assistance/', include('assistance.urls')),
    path('family/', include('familyconnect.urls')),
]
