from django.urls import path
from . import views

urlpatterns = [
    path('buscar_constancias/', views.buscar_constancias,
         name='buscar_constancias'),
]