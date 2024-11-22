from django.urls import path
from . import views


# app/constancias/rfc/urls.py
from rfc import views

urlpatterns = [
    path('verificar_rfc/', views.verificar_rfc, name='verificar_rfc'),
    path('seleccionar_constancia/', views.seleccionar_constancia, name='seleccionar_constancia'),
]

