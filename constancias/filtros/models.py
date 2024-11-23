import re
from django.db import models
from django.core.exceptions import ValidationError


def validar_rfc(value):
    regex_rfc = r'^([A-ZÑ&]{3,4})\d{6}([A-Z\d]{3})$'
    if not re.match(regex_rfc, value):
        raise ValidationError("El RFC ingresado no es válido.")


def validar_longitud_minima(valor):
    if len(valor) < 3:
        raise ValidationError('El nombre debe tener al menos 3 caracteres')


class Constancia(models.Model):
    nombre = models.CharField(max_length=255, validators=[
                              validar_longitud_minima])
    fecha_emision = models.DateField()
    rfc = models.CharField(max_length=13, validators=[validar_rfc])

    def __str__(self):
        return f"{self.nombre} - {self.fecha_emision} - {self.rfc}"
