from django.db import models

from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User  # Importa el modelo de Usuario
from django.core.validators import MinValueValidator
from agregar_constancia.validadores import curp_validator


class Constancia(models.Model):
    # Usuario relacionado
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Campo de usuario logeado
    
    # Choices for 'tipoconstancia'
    TIPOS_CONSTANCIA = [
        ('OTRO', 'Otro Motivo'),
        ('PROM_VERTICAL', 'Promoción Vertical'),
        ('ADMISION', 'Admisión'),
        ('HORAS_ADIC', 'Horas Adicionales'),
        ('CAMBIO_CENTRO', 'Cambios de Centro de Trabajo'),
        ('RECONOCIMIENTO', 'Reconocimiento'),
        ('PROM_HORIZONTAL', 'Promoción Horizontal'),
        ('BASE_ESTATAL', 'Basificación estatal'),
        ('CAMBIO_CENTRO_PREP', 'Cambios de Centro de Trabajo nivel preparatoria'),
    ]
    tipo_constancia = models.CharField(max_length=20, choices=TIPOS_CONSTANCIA)
    Activa = models.BooleanField(default=True)

    # Datos básicos del docente se quita el validador de curp por el momento al estar obsuscados en la bd
    curp = models.CharField(max_length=18) #validators=[curp_validator]
    filiacion = models.CharField(max_length=13)  # RFC
    nombre_completo = models.CharField(max_length=255)
    categoria_plaza = models.CharField(max_length=100)

    # Tipo de nombramiento (campo de elección)
    TIPO_NOMBRAMIENTO = [
        ('09', 'Alta inicial'),
        ('10', 'Alta definitiva'),
        ('20', 'Alta interina limitada'),
        ('24', 'Alta en gravidez'),
        ('25', 'Alta en pensión'),
        ('95', 'Alta provisional'),
        ('96', 'Alta de confianza'),
        ('99', 'Alta provisional'),
    ]
    tipo_nombramiento = models.CharField(max_length=2, choices=TIPO_NOMBRAMIENTO)

    # Información del lugar de trabajo
    clave_centro_trabajo = models.CharField(max_length=50)
    nombre_centro_trabajo = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    municipio = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)

    # Otros datos del empleo
    sueldo_mensual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(Decimal('0.01'))])
    PARTIDA_CODES = [
        ('7-1103', 'Código 7-1103'),
        ('14-1204', 'Código 14-1204'),
        ('15-1205', 'Código 15-1205'),
    ]
    partida = models.CharField(max_length=10, choices=PARTIDA_CODES, blank=True, null=True)
    fecha_input = models.DateField()  # Fecha de ingreso, contrato o alta definitiva
    motivo_constancia = models.TextField()

    # Firma
    firma = models.CharField(max_length=255)  # Ejemplo: "Capital Humano Edificio Central"

    # Nueva funcionalidad para logos
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)  # Campo para subir el logo
    incluir_logo = models.BooleanField(default=False)  # Indica si el logo se debe incluir en la constancia

    # Campos adicionales para constancias específicas
    comentarios_observaciones = models.TextField(blank=True, null=True)
    fecha_expiracion = models.DateField(blank=True, null=True)
    fecha_creacion_constancia = models.DateField()

    # Métodos
    def __str__(self):
        return f"{self.nombre_completo} - {self.tipo_constancia}"

    
class Configuracion(models.Model):
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

    def __str__(self):
        return "Configuración General"
    
class ClavesConstancia(models.Model):
    constancia = models.ForeignKey(Constancia, related_name="claves", on_delete=models.CASCADE)
    clave = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.constancia} - {self.clave}"


class ContratoConstancia(models.Model):
    constancia = models.ForeignKey(Constancia, on_delete=models.CASCADE, related_name="contratos")
    adscripcion = models.CharField(max_length=20, verbose_name="Clave de Centro de Trabajo")
    clave_categoria = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_termino = models.DateField(verbose_name="Fecha de Término")

    class Meta:
        verbose_name_plural = "Contratos constancia"

    def __str__(self):
        return f"Contrato en {self.adscripcion} - {self.codigo}"


class LicenciaConstancia(models.Model):
    constancia = models.ForeignKey(Constancia, on_delete=models.CASCADE, related_name="licencias")
    adscripcion = models.CharField(max_length=20, verbose_name="Clave de Centro de Trabajo")
    clave_categoria = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)
    fecha_inicio = models.DateField(verbose_name="Fecha de Inicio")
    fecha_termino = models.DateField(verbose_name="Fecha de Término")

    class Meta:
        verbose_name_plural = "Licencias constancia"

    def __str__(self):
        return f"Licencia en {self.adscripcion} - {self.codigo}"