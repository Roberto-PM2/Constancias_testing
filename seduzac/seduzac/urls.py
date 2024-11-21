from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from constancias import views as constancias_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', constancias_views.inicio, name='inicio'),
    path('constancias/', include('constancias.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)