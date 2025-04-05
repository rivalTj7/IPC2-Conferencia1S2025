from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Registro y perfil
    path('registro/', views.register, name='register'),
    path('perfil/', views.profile, name='profile'),
    path('perfil/editar/', views.profile_update, name='profile_update'),
    
    # Cambio de contraseña
    path('cambiar-password/', 
         auth_views.PasswordChangeView.as_view(template_name='users/password_change_form.html'), 
         name='password_change'),
    path('cambiar-password/hecho/', 
         auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),
    
    # Recuperación de contraseña
    path('restablecer-password/',
         auth_views.PasswordResetView.as_view(template_name='users/password_reset_form.html'),
         name='password_reset'),
    path('restablecer-password/enviado/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('restablecer-password/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('restablecer-password/completado/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]