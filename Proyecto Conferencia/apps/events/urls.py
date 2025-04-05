from django.urls import path
from . import views

urlpatterns = [
    # Eventos
    path('', views.event_list, name='event_list'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('<slug:slug>/registrarse/', views.event_register, name='event_register'),
    
    # Registros
    path('registro/<int:registration_id>/cancelar/', views.registration_cancel, name='registration_cancel'),
    path('mis-registros/', views.user_registrations, name='user_registrations'),
    
    # Categorías
    path('categoria/<slug:slug>/', views.category_detail, name='category_detail'),
    
    # Sesiones
    path('sesion/<int:session_id>/', views.session_detail, name='session_detail'),
]