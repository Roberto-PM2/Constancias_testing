from django.db import models


class Constancia(models.Model):
    nombre = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    incluir_logo = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class Configuracion(models.Model):
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return "Configuración General"
