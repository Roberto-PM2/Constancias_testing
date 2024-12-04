from django.shortcuts import render, get_object_or_404, redirect
from .forms import ConstanciaForm, ConfiguracionForm, RegistroForm
from .models import Constancia, Configuracion
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def inicio(request):
    return redirect('bienvenida')


@login_required
def crear_constancia(request):
    user = request.user
    configuracion = Configuracion.objects.first()
    is_usuario_region = user.groups.filter(name="usuario_Region").exists()

    if request.method == "POST":
        form = ConstanciaForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get(
                    'incluir_logo', False)

                if constancia.incluir_logo:
                    if form.cleaned_data.get('logo'):
                        constancia.logo = form.cleaned_data.get('logo')

                        if configuracion:
                            configuracion.logo = form.cleaned_data.get('logo')
                            configuracion.save()
                        else:
                            Configuracion.objects.create(
                                logo=form.cleaned_data.get('logo'))
                    else:
                        constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
                else:
                    constancia.logo = None

            constancia.save()
            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    return render(request, 'constancias/crear_constancia.html', {'form': form})


def constancia_generada(request, constancia_id):
    constancia = get_object_or_404(Constancia, id=constancia_id)
    configuracion = Configuracion.objects.first()

    logo_url = None
    if configuracion and constancia.incluir_logo:
        if configuracion.logo:
            logo_url = configuracion.logo.url
        else:
            from django.contrib import messages
            messages.warning(
                request, "El logo configurado no está disponible.")

    return render(request, 'constancias/constancia_generada.html', {
        'constancia': constancia,
        'logo_url': logo_url,
    })


def configurar_logo(request):
    configuracion = Configuracion.objects.first() or Configuracion()
    if request.method == "POST":
        form = ConfiguracionForm(
            request.POST, request.FILES, instance=configuracion)
        if form.is_valid():
            form.save()
            return redirect('crear_constancia')
    else:
        form = ConfiguracionForm(instance=configuracion)
    return render(request, 'constancias/configurar_logo.html', {'form': form})


def bienvenida(request):
    return render(request, 'constancias/bienvenida.html')


def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {'error': 'Usuario o contraseña incorrectos.'}
            return render(request, 'constancias/login.html', context)
        login(request, user)
        return redirect('crear_constancia')
    return render(request, 'constancias/login.html')


def registrarse(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('login')
        else:
            messages.error(
                request, 'Error en el registro. Verifica los datos ingresados.')
    else:
        form = RegistroForm()
    return render(request, 'constancias/registro.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect('bienvenida')
