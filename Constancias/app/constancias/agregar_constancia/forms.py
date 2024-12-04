from django import forms
from .models import Configuracion,Constancia,Configuracion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ConstanciaForm(forms.ModelForm):
    class Meta:
        model = Constancia
        fields = ['nombre_completo', 'logo', 'incluir_logo']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo'].required = False
    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['logo']

class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ConstanciaOtroMotivoForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'comentarios_observaciones', 'fecha_creacion_constancia', 'fecha_expiracion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bloquea el campo de tipo_constancia y asigna "OTRO" como valor predeterminado
        self.fields['tipo_constancia'].initial = 'OTRO'
        self.fields['tipo_constancia'].disabled = True
        self.fields['fecha_input'].label = "fecha de ingreso"

        # Cambia la etiqueta de nombre_completo
        self.fields['nombre_completo'].label = "Hace constar que:"

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaPromocionVerticalForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'comentarios_observaciones', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'PROM_VERTICAL'
        self.fields['tipo_constancia'].disabled = True
        self.fields['tipo_nombramiento'].initial = '10'
        self.fields['tipo_nombramiento'].disabled = True

        # Etiqueta personalizada
        self.fields['categoria_plaza'].label = "Con categoria actual"
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "fecha de alta definitiva"
        self.fields['motivo_constancia'].initial = "Proceso de promoción"
        self.fields['motivo_constancia'].disabled = True

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaAdmisionForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'comentarios_observaciones', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'ADMISION'
        self.fields['tipo_constancia'].disabled = True

        # Etiqueta personalizada
        self.fields['categoria_plaza'].label = "Con categoria actual"
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "Fecha de contrato"
        self.fields['motivo_constancia'].initial = "Proceso de admision"
        self.fields['motivo_constancia'].disabled = True

        # Filtrar las opciones de 'tipo_nombramiento' para excluir '10' (Alta definitiva)
        self.fields['tipo_nombramiento'].choices = [
            choice for choice in self.fields['tipo_nombramiento'].choices if choice[0] != '10'
        ]

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaHorasAdicionalesForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'comentarios_observaciones', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'HORAS_ADIC'
        self.fields['tipo_constancia'].disabled = True
        self.fields['tipo_nombramiento'].initial = '10'
        self.fields['tipo_nombramiento'].disabled = True

        # Etiqueta personalizada
        self.fields['categoria_plaza'].label = "Con categoria actual"
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "fecha de alta definitiva"
        self.fields['motivo_constancia'].initial = "Horas adicionales"
        self.fields['motivo_constancia'].disabled = True

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaCambioCentroTrabajoForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual', 'partida']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'CAMBIO_CENTRO'
        self.fields['tipo_constancia'].disabled = True
        self.fields['tipo_nombramiento'].initial = '10'
        self.fields['tipo_nombramiento'].disabled = True

        # Etiqueta personalizada
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "fecha de alta definitiva"
        self.fields['motivo_constancia'].initial = "Proceso de cambios de centro de trabajo, permutas y re-adscripción."
        self.fields['motivo_constancia'].disabled = True

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaReconocimientoForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'comentarios_observaciones', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'RECONOCIMIENTO'
        self.fields['tipo_constancia'].disabled = True
        self.fields['tipo_nombramiento'].initial = '10'
        self.fields['tipo_nombramiento'].disabled = True

        # Etiqueta personalizada
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "fecha de ingreso"
        self.fields['motivo_constancia'].initial = (
            "Se emite constancia laboral para participar en la convocatoria publicada por la DSICAMM, "
            "en el proceso de selección de personal docente y técnico docente que se desempeñará como tutor, "
            "personal directivo escolar que se desempeñará como asesor técnico y personal docente que se "
            "desempeñará como asesor técnico pedagógico, con el propósito de comprobar antigüedad en el servicio docente."
        )
        self.fields['motivo_constancia'].disabled = True

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaPromocionHorizontalForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'comentarios_observaciones', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'PROM_HORIZONTAL'
        self.fields['tipo_constancia'].disabled = True
        self.fields['tipo_nombramiento'].initial = '10'
        self.fields['tipo_nombramiento'].disabled = True

        # Etiqueta personalizada
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "fecha de alta definitiva"
        self.fields['motivo_constancia'].initial = "Proceso horizontal"

        self.fields['motivo_constancia'].disabled = True

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaBasificacionEstatalForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'comentarios_observaciones', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual', 'partida']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'BASE_ESTATAL'
        self.fields['tipo_constancia'].disabled = True

        # Etiqueta personalizada
        self.fields['categoria_plaza'].label = "Con categoria actual"
        # self.fields['clave_centro_trabajo'].label = "lugar donde presta sus servicios"
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "fecha de contrato"
        self.fields['motivo_constancia'].initial = "Proceso de basificación de Personal de Apoyo y Asistencia a la Educación."
        self.fields['motivo_constancia'].disabled = True

        self.fields['tipo_nombramiento'].choices = [
            choice for choice in self.fields['tipo_nombramiento'].choices if choice[0] != '10'
        ]

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConstanciaCambioCentroTrabajoPreparatoriasForm(forms.ModelForm):
    class Meta:
        model = Constancia
        exclude = ['Activa', 'usuario', 'fecha_creacion_constancia', 'fecha_expiracion', 'sueldo_mensual', 'partida']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Campos informativos
        self.fields['tipo_constancia'].initial = 'CAMBIO_CENTRO_PREP'
        self.fields['tipo_constancia'].disabled = True
        self.fields['tipo_nombramiento'].initial = '10'
        self.fields['tipo_nombramiento'].disabled = True

        # Etiqueta personalizada
        self.fields['nombre_completo'].label = "Hace constar que:"
        self.fields['fecha_input'].label = "fecha de alta definitiva"
        self.fields['motivo_constancia'].initial = "Proceso de cambios de centro de trabajo en Educación Media Nivel Preparatoria"
        self.fields['motivo_constancia'].disabled = True

    incluir_logo = forms.BooleanField(required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")
