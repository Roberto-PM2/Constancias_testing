from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import (
    Constancia,
    Configuracion,
    ClavesConstancia,
    ContratoConstancia,
    LicenciaConstancia,
)
from .forms import (
    ConstanciaForm,
    ConfiguracionForm,
    RegistroForm,
    ConstanciaOtroMotivoForm,
    ConstanciaPromocionVerticalForm,
    ConstanciaAdmisionForm,
    ConstanciaHorasAdicionalesForm,
    ConstanciaCambioCentroTrabajoForm,
    ConstanciaReconocimientoForm,
    ConstanciaPromocionHorizontalForm,
    ConstanciaBasificacionEstatalForm,
    ConstanciaCambioCentroTrabajoPreparatoriasForm,
)


# Vista para calcular la duración entre fechas
def calcular_duracion(request):
    tipo = request.POST.get('tipo')
    fechas_inicio = request.POST.getlist('fechas_inicio[]')
    fechas_fin = request.POST.getlist('fechas_fin[]')

    total_dias = 0
    for inicio, fin in zip(fechas_inicio, fechas_fin):
        if inicio and fin:
            fecha_inicio = datetime.strptime(inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fin, '%Y-%m-%d')
            total_dias += (fecha_fin - fecha_inicio).days

    years = total_dias // 365
    months = (total_dias % 365) // 30
    days = total_dias % 30

    return JsonResponse({
        'tipo': tipo,
        'years': years,
        'months': months,
        'days': days
    })

def procesar_claves(constancia, claves):
    ClavesConstancia.objects.bulk_create([
        ClavesConstancia(constancia=constancia, clave=clave)
        for clave in claves if clave.strip()
    ])

def procesar_contratos(constancia, contratos_adscripcion, contratos_clave_categoria, contratos_codigo, contratos_fecha_inicio, contratos_fecha_termino):
    for i in range(len(contratos_adscripcion)):
        if contratos_adscripcion[i].strip():
            nuevo_contrato = ContratoConstancia(
                constancia=constancia,
                adscripcion=contratos_adscripcion[i],
                clave_categoria=contratos_clave_categoria[i],
                codigo=contratos_codigo[i],
                fecha_inicio=contratos_fecha_inicio[i],
                fecha_termino=contratos_fecha_termino[i]
            )
            nuevo_contrato.save()

def procesar_licencias(constancia, licencias_adscripcion, licencias_clave_categoria, licencias_codigo, licencias_fecha_inicio, licencias_fecha_termino):
    for i in range(len(licencias_adscripcion)):
        if licencias_adscripcion[i].strip():
            nueva_licencia = LicenciaConstancia(
                constancia=constancia,
                adscripcion=licencias_adscripcion[i],
                clave_categoria=licencias_clave_categoria[i],
                codigo=licencias_codigo[i],
                fecha_inicio=licencias_fecha_inicio[i],
                fecha_termino=licencias_fecha_termino[i]
            )
            nueva_licencia.save()


def editar_constancia(request, id_constancia):
    # Obtener la constancia existente
    constancia = Constancia.objects.get(id=id_constancia)
    tipo = constancia.tipo_constancia

    # Diccionario que mapea cada tipo de constancia a la vista correspondiente
    switch_vistas = {
        'OTRO': editar_constanciaOM,
        'PROM_VERTICAL': editar_constanciaPV,
        'ADMISION': editar_constanciaAdmision,
        'HORAS_ADIC': editar_constanciaHA,
        'CAMBIO_CENTRO': editar_constanciaCambioCT,
        'RECONOCIMIENTO': editar_constanciaReconocimiento,
        'PROM_HORIZONTAL': editar_constanciaPH,
        'BASE_ESTATAL': editar_constanciaBE,
        'CAMBIO_CENTRO_PREP': editar_constanciaCambioCTP,
    }

    # Llamar a la vista correspondiente
    vista = switch_vistas.get(tipo, None)
    if vista:
        return vista(request, id_constancia)

# Vista para listar constancias
def lista_constancias(request):
    constancias = Constancia.objects.all()
    return render(request, 'constancias/lista_constancias.html', {'constancias': constancias})

# Vista para eliminar constancias
def eliminar_constancia(request, id_constancia):
    Constancia.objects.filter(id=id_constancia).delete()
    return redirect('lista_constancias')

# Vista principal de inicio
def inicio(request):
    return redirect('bienvenida')

# Vista para mostrar la bienvenida
def bienvenida(request):
    return render(request, 'constancias/bienvenida.html')

# Vista para iniciar sesión
def iniciar_sesion(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return render(request, 'constancias/login.html')

        login(request, user)
        return redirect('crear_constancia')

    return render(request, 'constancias/login.html')

# Vista para registrarse
def registrarse(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada correctamente.')
            return redirect('login')
        else:
            messages.error(request, 'Error en el registro. Verifica los datos ingresados.')
    else:
        form = RegistroForm()
    return render(request, 'constancias/registro.html', {'form': form})

# Vista para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('bienvenida')

# Vista para crear una constancia
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
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            constancia.save()
            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    return render(request, 'constancias/crear_constancia.html', {'form': form})

# Vista para generar constancias
def constancia_generada(request, constancia_id):
    constancia = get_object_or_404(Constancia, id=constancia_id)
    configuracion = Configuracion.objects.first()

    logo_url = configuracion.logo.url if configuracion and constancia.incluir_logo and configuracion.logo else None

    return render(request, 'constancias/constancia_generada.html', {
        'constancia': constancia,
        'logo_url': logo_url,
    })

# Vista para configurar el logo
def configurar_logo(request):
    configuracion = Configuracion.objects.first() or Configuracion()
    if request.method == "POST":
        form = ConfiguracionForm(request.POST, request.FILES, instance=configuracion)
        if form.is_valid():
            form.save()
            return redirect('crear_constancia')
    else:
        form = ConfiguracionForm(instance=configuracion)
    return render(request, 'constancias/configurar_logo.html', {'form': form})

# Vista para crear constancias de "Otro Motivo"
@login_required
def nueva_constanciaOM(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaOtroMotivoForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()

            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')

            constancia.save()

            claves = request.POST.getlist('claves[]')
            ClavesConstancia.objects.bulk_create([
                ClavesConstancia(constancia=constancia, clave=clave)
                for clave in claves if clave.strip()
            ])

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaOtroMotivoForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaOM.html', context)

# Vista para editar constancias de "Otro Motivo"
def editar_constanciaOM(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaOtroMotivoForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()

            claves = request.POST.getlist('claves[]')
            ClavesConstancia.objects.bulk_create([
                ClavesConstancia(constancia=constancia, clave=clave)
                for clave in claves if clave.strip()
            ])

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            
            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaOtroMotivoForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaOM.html', context)

#promocion vertical-------------------------------

@login_required
def nueva_constanciaPV(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaPromocionVerticalForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaPromocionVerticalForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaPV.html', context)

def editar_constanciaPV(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)
    licencias_existentes = LicenciaConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaPromocionVerticalForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()
            licencias_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaPromocionVerticalForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'licencias_existentes': licencias_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaPV.html', context)

#Admision-------------------------------

@login_required
def nueva_constanciaAdmision(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaAdmisionForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaAdmisionForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaAdmision.html', context)

def editar_constanciaAdmision(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaAdmisionForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaAdmisionForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaAdmision.html', context)

#Horas Adicionales-------------------------------

@login_required
def nueva_constanciaHA(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaHorasAdicionalesForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaHorasAdicionalesForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaHA.html', context)

def editar_constanciaHA(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)
    licencias_existentes = LicenciaConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaHorasAdicionalesForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()
            licencias_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaHorasAdicionalesForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'licencias_existentes': licencias_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaHA.html', context)

#Cambio Centro Trabajo-------------------------------

@login_required
def nueva_constanciaCambioCT(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaCambioCentroTrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaCambioCentroTrabajoForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaCambioCT.html', context)

def editar_constanciaCambioCT(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)
    licencias_existentes = LicenciaConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaCambioCentroTrabajoForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()
            licencias_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaCambioCentroTrabajoForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'licencias_existentes': licencias_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaCambioCT.html', context)

#Reconocimiento-------------------------------

@login_required
def nueva_constanciaReconocimiento(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaReconocimientoForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaReconocimientoForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaReconocimiento.html', context)

def editar_constanciaReconocimiento(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)
    licencias_existentes = LicenciaConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaReconocimientoForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()
            licencias_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaReconocimientoForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'licencias_existentes': licencias_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaReconocimiento.html', context)

#Promocion Horizontal-------------------------------

@login_required
def nueva_constanciaPH(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaPromocionHorizontalForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaPromocionHorizontalForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaPH.html', context)

def editar_constanciaPH(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)
    licencias_existentes = LicenciaConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaPromocionHorizontalForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()
            licencias_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaPromocionHorizontalForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'licencias_existentes': licencias_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaPH.html', context)

#Basificacion Estatal-------------------------------

@login_required
def nueva_constanciaBE(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaBasificacionEstatalForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaBasificacionEstatalForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaBE.html', context)

def editar_constanciaBE(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaBasificacionEstatalForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaBasificacionEstatalForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaBE.html', context)

#Cambio Centro Trabajo Preparatorias-------------------------------

@login_required
def nueva_constanciaCambioCTP(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    if request.method == 'POST':
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm(request.POST, request.FILES)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()
            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')
            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm()
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaCambioCTP.html', context)

def editar_constanciaCambioCTP(request, id_constancia):
    configuracion = Configuracion.objects.first()
    constancia = get_object_or_404(Constancia, id=id_constancia)
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    claves_existentes = ClavesConstancia.objects.filter(constancia=constancia)
    contratos_existentes = ContratoConstancia.objects.filter(constancia=constancia)
    licencias_existentes = LicenciaConstancia.objects.filter(constancia=constancia)

    if request.method == 'POST':
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm(request.POST, request.FILES, instance=constancia)
        if form.is_valid():
            constancia = form.save()
            claves_existentes.delete()
            contratos_existentes.delete()
            licencias_existentes.delete()

            procesar_claves(constancia, request.POST.getlist('claves[]'))
            procesar_contratos(
                constancia,
                request.POST.getlist('contratos_adscripcion[]'),
                request.POST.getlist('contratos_clave_categoria[]'),
                request.POST.getlist('contratos_codigo[]'),
                request.POST.getlist('contratos_fecha_inicio[]'),
                request.POST.getlist('contratos_fecha_termino[]')
            )
            procesar_licencias(
                constancia,
                request.POST.getlist('licencias_adscripcion[]'),
                request.POST.getlist('licencias_clave_categoria[]'),
                request.POST.getlist('licencias_codigo[]'),
                request.POST.getlist('licencias_fecha_inicio[]'),
                request.POST.getlist('licencias_fecha_termino[]')
            )

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm(instance=constancia)

    context = {
        'form': form,
        'claves_existentes': claves_existentes,
        'contratos_existentes': contratos_existentes,
        'licencias_existentes': licencias_existentes,
        'editar': True
    }

    return render(request, 'constancias/nueva_constanciaCambioCTP.html', context)