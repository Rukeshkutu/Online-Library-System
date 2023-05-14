from django.contrib import admin
from django.urls import path
from .import views

app_name = 'auth_users'
urlpatterns = [
    path('login/', views.signin_page, name = 'signin_page'),
    path('logout/', views.signout_page, name = 'signout_page'),
    path('register/', views.register_page, name = 'register'),
    
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name = 'user_dashboard'),
]

