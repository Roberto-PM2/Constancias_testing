# mi_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('constancias/', views.lista_constancias, name='lista_constancias'),
    path('constancias/<int:constanciaId>/cambiar_estado/', views.cambiar_estado, name='cambiar_estado'),
]
