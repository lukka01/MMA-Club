from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    UserListView,
    UserDetailView,
    CurrentUserView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordChangeView,
)

app_name = 'users'

urlpatterns = [
    #აუთენტიკაცია
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    #პაროლებისთვის
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),

    #მომხმარებლებისთვის
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/me/', CurrentUserView.as_view(), name='current-user'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),


]