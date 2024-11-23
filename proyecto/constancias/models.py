from django.db import models

class Constancia(models.Model):
    nombre = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)  # Indica si está activa o no

    @property
    def estado(self):
        return "Activa" if self.activo else "Inactiva"
 
    def __str__(self):
        return f"{self.nombre} ({'Activa' if self.activo else 'Inactiva'})"

        

