from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('api/admin/v1/', include('accounts.api_admin_v1.urls')),
]