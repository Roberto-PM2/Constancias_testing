from django import forms
from .models import Configuracion, Constancia, Configuracion
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ConstanciaForm(forms.ModelForm):
    class Meta:
        model = Constancia
        fields = ['nombre', 'logo', 'incluir_logo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['logo'].required = False
    incluir_logo = forms.BooleanField(
        required=False, initial=False, label="Incluir logo")
    logo = forms.ImageField(required=False, label="Logo (opcional)")


class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['logo']


class RegistroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
