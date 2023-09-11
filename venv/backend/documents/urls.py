# documents/urls.py

from django.urls import path
from .views import UserSignupView, UserLoginView, UserListView , DocumentDetailView , DocumentListView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('document/', DocumentListView.as_view(), name='document-list'),
    path('document/<int:document_id>/', DocumentDetailView.as_view(), name='document-detail'),
]
