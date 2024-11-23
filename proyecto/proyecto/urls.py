
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('constancias.urls')),  # Incluye las URLs de la aplicación mi_app
    path('accounts/', include('django.contrib.auth.urls')),
]

