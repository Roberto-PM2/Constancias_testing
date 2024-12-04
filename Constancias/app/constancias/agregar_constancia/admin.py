from django.contrib import admin
from .models import Constancia, ClavesConstancia, ContratoConstancia, LicenciaConstancia

# Register your models here.
admin.site.register(Constancia)
admin.site.register(ClavesConstancia)
admin.site.register(ContratoConstancia)
admin.site.register(LicenciaConstancia)

from .models import ConstanciaAccessControl

@admin.register(ConstanciaAccessControl)
class ConstanciaAccessControlAdmin(admin.ModelAdmin):
    list_display = ('tipo_constancia', 'habilitado')
    list_editable = ('habilitado',)