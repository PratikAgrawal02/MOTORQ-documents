# document_sharing_platform/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('documents.urls')),
    path('admin/', admin.site.urls),
    
]
