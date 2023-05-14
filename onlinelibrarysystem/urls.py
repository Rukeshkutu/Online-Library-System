from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth
# from auth_users import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('auth_users.urls')),
    
    path('password-reset-done/', auth.PasswordResetDoneView.as_view(template_name='auth_users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth.PasswordResetConfirmView.as_view(template_name="auth_users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset-done/', auth.PasswordResetCompleteView.as_view(template_name='auth_users/password_reset_complete.html'), name='password_reset_complete'),     

]


    
    