# document_sharing_platform/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic.base import RedirectView


schema_view = get_schema_view(
    openapi.Info(
        title='MotorQ SDE Document',
        default_version='v1',
        description='ass. for SDE track',
        contact=openapi.Contact(email='pratik.a21@iiits.in'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', RedirectView.as_view(url='/docs/')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('api/', include('documents.urls')),
    path('admin/', admin.site.urls),
    
]
