from django.contrib import admin
from .models import Constancia, ClavesConstancia, ContratoConstancia, LicenciaConstancia

# Register your models here.
admin.site.register(Constancia)
admin.site.register(ClavesConstancia)
admin.site.register(ContratoConstancia)
admin.site.register(LicenciaConstancia)
