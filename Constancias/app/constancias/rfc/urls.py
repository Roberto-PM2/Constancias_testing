from django.urls import path
from . import views

urlpatterns = [
    path('', views.ingresar_rfc, name='ingresar_rfc'),
    path('constancia/<str:tipo>/', views.ver_constancia, name='ver_constancia'),
]