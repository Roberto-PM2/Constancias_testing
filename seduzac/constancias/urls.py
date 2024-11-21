from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('bienvenida/', views.bienvenida, name='bienvenida'),
    path('login/', views.iniciar_sesion, name='login'),
    path('registro/', views.registrarse, name='registrarse'),
    path('logout/', views.cerrar_sesion, name='logout'),

    path('crear/', views.crear_constancia, name='crear_constancia'),
    path('generada/<int:constancia_id>/', views.constancia_generada, name='constancia_generada'),
]