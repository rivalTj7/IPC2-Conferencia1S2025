from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('acerca-de/', views.about, name='about'),
    path('contacto/', views.contact, name='contact'),
    path('preguntas-frecuentes/', views.faq, name='faq'),
    path('patrocinadores/', views.sponsors, name='sponsors'),
]