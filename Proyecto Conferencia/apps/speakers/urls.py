from django.urls import path
from . import views

urlpatterns = [
    # Ponentes
    path('', views.speaker_list, name='speaker_list'),
    path('<int:pk>/', views.speaker_detail, name='speaker_detail'),
    path('perfil/crear/', views.speaker_profile_create, name='speaker_profile_create'),
    path('perfil/actualizar/', views.speaker_profile_update, name='speaker_profile_update'),
    
    # Presentaciones
    path('presentacion/agregar/', views.presentation_create, name='presentation_create'),
    path('presentacion/<int:pk>/actualizar/', views.presentation_update, name='presentation_update'),
    path('presentacion/<int:pk>/eliminar/', views.presentation_delete, name='presentation_delete'),
    
    # Especializaciones
    path('especializacion/<slug:slug>/', views.specialization_detail, name='specialization_detail'),
]