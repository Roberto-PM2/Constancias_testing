from django.db import models


class EmpleadoComp(models.Model):
    rfcemp = models.CharField(max_length=50)
    nom_emp = models.CharField(max_length=100)
    curp = models.CharField(max_length=18)
    catemp = models.CharField(max_length=50, default="Sin categoría")  # Agregamos el valor por defecto

    def __str__(self):
        return f'{self.nom_emp} ({self.rfcemp})'
