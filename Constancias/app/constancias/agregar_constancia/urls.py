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
    #urls constancias tipos
    path('nuevoCOM/', views.nueva_constanciaOM, name='nuevoCOM'),
    path('nuevoCPV/', views.nueva_constanciaPV, name='nuevoCPV'),
    path('nuevoCAdmision/', views.nueva_constanciaAdmision, name='nuevoCAdmision'),
    path('nuevoCHA/', views.nueva_constanciaHA, name='nuevoCHA'),
    path('nuevoCCambioCT/', views.nueva_constanciaCambioCT, name='nuevoCCambioCT'),
    path('nuevoCReconocimiento/', views.nueva_constanciaReconocimiento, name='nuevoCReconocimiento'),
    path('nuevoCPH/', views.nueva_constanciaPH, name='nuevoCPH'),
    path('nuevoCBE/', views.nueva_constanciaBE, name='nuevoCBE'),
    path('nuevoCCambioCTP/', views.nueva_constanciaCambioCTP, name='nuevoCCambioCTP'),

    path('lista/', views.lista_constancias, name='lista_constancias'),
    path('estado-constancia/<int:id_constancia>', views.cambiar_estado, name='cambiar_estado'),
    path('eliminar-constancia/<int:id_constancia>', views.eliminar_constancia, name='eliminar_constancia'),
    path('editar-constancia/<int:id_constancia>', views.editar_constancia, name='editar_constancia'),
    path('calcular_duracion/', views.calcular_duracion, name='calcular_duracion'),
]