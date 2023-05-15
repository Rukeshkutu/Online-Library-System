from django.contrib import admin
from django.urls import path
from .import views

app_name = 'auth_users'
urlpatterns = [
    path('login/', views.signin_page, name = 'signin_page'),
    path('logout/', views.signout_page, name = 'signout_page'),
    path('register/', views.register_page, name = 'register'),
    
    path('password-reset/', views.password_reset_request, name ="password_reset"),
    
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name = 'admin_dashboard'),
    path('user-dashboard/', views.user_dashboard, name = 'user_dashboard'),
    
    path('profile/', views.profile, name= 'profile'),
    path('edit-profile-image', views.edit_profile_image, name = "edit_profile_image"),
    path('edit-profile-detail', views.edit_profile_detail, name = "edit_profile_detail"),
    
    path('view-users/', views.view_user, name = 'view_user'),
    path('delete-user/<str:id>', views.delete_User, name = 'delete_user'),
    
]

