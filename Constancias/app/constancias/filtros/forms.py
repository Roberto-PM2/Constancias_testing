from django import forms
from django.core.exceptions import ValidationError


class ConstanciaSearchForm(forms.Form):
    def validar_longitud_minima(valor):
        if len(valor) < 3:
            raise ValidationError('El nombre debe tener al menos 3 caracteres')

    nombre = forms.CharField(required=False, max_length=255, validators=[
                             validar_longitud_minima])
    fecha_emision = forms.DateField(required=False)
    rfc = forms.CharField(required=False, max_length=13)