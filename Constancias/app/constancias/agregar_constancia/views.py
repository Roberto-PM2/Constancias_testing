from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import (
    Constancia,
    Configuracion,
    ClavesConstancia,
    ContratoConstancia,
    LicenciaConstancia,
    ConstanciaAccessControl
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
from django.db import connections

from .decorators import verificar_acceso_constancia

#funcion para buscar datos del maestro a partir del rfc
def getInfo_Empleado_RFC(rfc):
    """
    Consulta en la base de datos los datos del empleado a partir del RFC.
    Retorna un diccionario con los datos del empleado o None si no se encuentra.
    """
    sql = """
        SELECT NOMBRE, CURP FROM EMPLEADO_COMP WHERE RFC = %s
    """
    with connections['personal'].cursor() as cursor:
        cursor.execute(sql, [rfc])
        result = cursor.fetchone()

    if result:
        return {"nombre": result[0], "curp": result[1], "rfc": rfc}
    return None


#funcion para obtener datos a partir de la clave del centro de trabajo
def getInfo_Clave_Centro_Trabajo(claveCT):
    """
    Consulta en la base de datos los datos del centro a partir de la clave.
    Retorna un diccionario con los datos del centro o None si no se encuentra.
    """
    sql = """
        SELECT NOMBRECT, DOMICILIO, MUNICIPIO, LOCALIDAD FROM A_CTBA WHERE CLAVECCT = %s
    """
    with connections['personal'].cursor() as cursor:
        cursor.execute(sql, [claveCT])
        result = cursor.fetchone()

    if result:
        return {"nombre": result[0], 
                "domicilio": result[1], 
                "municipio": result[2], 
                "localidad": result[3], 
                "claveCT": claveCT}
    return None


# Vista para calcular la duración entre fechas para contratos y licencias
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

#funciones que procesan las claves contratos y licencias dentro del template y las almacenan en
#tablas asociadas a la constancia
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

#funcion que a partir del id de constancia redirige al tipo de constancia apropiada
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
    
#lista tipos constancia
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
    
# Vista para crear una constancia
@login_required
def crear_constancia(request):
    if request.method == 'POST':
        rfc = request.POST.get('rfc', '').strip()
        claveCT = request.POST.get('claveCT', '').strip()
        tipo_constancia = request.POST.get('tipo_constancia')

        # Consultar la información del empleado
        #comentar para hacer verificaciones
        # empleado = getInfoEmpleadoRFC(rfc)
        # if not empleado:
        #     return render(request, 'constancias/crear_constancia.html', {'error': "No se encontró un empleado con el RFC ingresado."})

        # Almacenar los parámetros en la sesión
        request.session['rfc'] = rfc
        request.session['claveCT'] = claveCT
        request.session.save()

        # Redirigir a la vista correspondiente según el tipo de constancia
        switch_urls = {
            'OTRO': 'nuevoCOM',
            'PROM_VERTICAL': 'nuevoCPV',
            'ADMISION': 'nuevoCAdmision',
            'HORAS_ADIC': 'nuevoCHA',
            'CAMBIO_CENTRO': 'nuevoCCambioCT',
            'RECONOCIMIENTO': 'nuevoCReconocimiento',
            'PROM_HORIZONTAL': 'nuevoCPH',
            'BASE_ESTATAL': 'nuevoCBE',
            'CAMBIO_CENTRO_PREP': 'nuevoCCambioCTP',
        }

        url_name = switch_urls.get(tipo_constancia)
        if url_name:
            return redirect(reverse(url_name))

     # Obtener los tipos de constancia habilitados
    constancias_habilitadas = ConstanciaAccessControl.objects.filter(habilitado=True).values_list('tipo_constancia', flat=True)

    return render(request, 'constancias/crear_constancia.html', {
        'constancias_habilitadas': constancias_habilitadas,
        'tipos_constancia': TIPOS_CONSTANCIA,
    })
    

# Vista para listar constancias
def lista_constancias(request):
    constancias = Constancia.objects.all()
    return render(request, 'constancias/lista_constancias.html', {'constancias': constancias})

# vista para activar/desactivar constancias
def cambiar_estado(request, id_constancia):
    #constancia = Constancia.objects.filter(id=id_constancia)
    constancia = get_object_or_404(Constancia, id=id_constancia)
    constancia.Activa = not constancia.Activa
    constancia.save()
    return redirect('lista_constancias')

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

#funcion que crea un array de datos de acuerdo a las consultas para pasarlos al formulario
def inicializar_Datos_Form_Constancias(rfc,claveCT):
    empleado = getInfo_Empleado_RFC(rfc)
    centroT = getInfo_Clave_Centro_Trabajo(claveCT)
    if not empleado:
        return render(request, 'constancias/crear_constancia.html', {'error': "No se encontró un empleado con el RFC ingresado."})
    if not centroT:
        return render(request, 'constancias/crear_constancia.html', {'error': "No se encontró un Centro de trabajo"})
    initial_data = {
        'nombre_completo':empleado.get('nombre'),
        'curp':empleado.get('curp'),
        'filiacion':empleado.get('rfc'),
        'clave_centro_trabajo':centroT.get('claveCT'),
        'nombre_centro_trabajo':centroT.get('nombre'),
        'direccion':centroT.get('domicilio'),
        'municipio':centroT.get('municipio'),
        'localidad':centroT.get('localidad'),
    }
    return initial_data

#Otro Motivo-----------------------------------------

# Vista para crear constancias de "Otro Motivo"
#cada tipo de constancia tiene su respectivo decorador para verificar permisos de acceso
@login_required
@verificar_acceso_constancia('OTRO')
def nueva_constanciaOM(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()

    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaOtroMotivoForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            constancia = form.save(commit=False)
            constancia.usuario = request.user
            constancia.fecha_creacion_constancia = datetime.now()

            constancia.incluir_logo = is_usuario_region or form.cleaned_data.get('incluir_logo', False)
            constancia.logo = configuracion.logo if is_usuario_region else form.cleaned_data.get('logo')

            constancia.save()

            procesar_claves(constancia, request.POST.getlist('claves[]'))

            if is_usuario_region:
                constancia.incluir_logo = True
                constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
            else:
                constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
                constancia.logo = configuracion.logo if configuracion else None

            return redirect('constancia_generada', constancia_id=constancia.id)
    else:
        form = ConstanciaOtroMotivoForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaOM.html', context)

# Vista para editar constancias de "Otro Motivo"
@login_required
@verificar_acceso_constancia('OTRO')
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

            procesar_claves(constancia, request.POST.getlist('claves[]'))

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
@verificar_acceso_constancia('PROM_VERTICAL')
def nueva_constanciaPV(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()

    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaPromocionVerticalForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaPromocionVerticalForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaPV.html', context)

@login_required
@verificar_acceso_constancia('PROM_VERTICAL')
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
@verificar_acceso_constancia('ADMISION')
def nueva_constanciaAdmision(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()

    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaAdmisionForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaAdmisionForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaAdmision.html', context)

@login_required
@verificar_acceso_constancia('ADMISION')
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
@verificar_acceso_constancia('HORAS_ADIC')
def nueva_constanciaHA(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaHorasAdicionalesForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaHorasAdicionalesForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaHA.html', context)


@login_required
@verificar_acceso_constancia('HORAS_ADIC')
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
@verificar_acceso_constancia('CAMBIO_CENTRO')
def nueva_constanciaCambioCT(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()
    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaCambioCentroTrabajoForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaCambioCentroTrabajoForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaCambioCT.html', context)


@login_required
@verificar_acceso_constancia('CAMBIO_CENTRO')
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
@verificar_acceso_constancia('RECONOCIMIENTO')
def nueva_constanciaReconocimiento(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()

    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaReconocimientoForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaReconocimientoForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaReconocimiento.html', context)


@login_required
@verificar_acceso_constancia('RECONOCIMIENTO')
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
@verificar_acceso_constancia('PROM_HORIZONTAL')
def nueva_constanciaPH(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()

    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaPromocionHorizontalForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaPromocionHorizontalForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaPH.html', context)

@login_required
@verificar_acceso_constancia('PROM_HORIZONTAL')
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
@verificar_acceso_constancia('BASE_ESTATAL')
def nueva_constanciaBE(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()

    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaBasificacionEstatalForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaBasificacionEstatalForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaBE.html', context)


@login_required
@verificar_acceso_constancia('BASE_ESTATAL')
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
@verificar_acceso_constancia('CAMBIO_CENTRO_PREP')
def nueva_constanciaCambioCTP(request):
    configuracion = Configuracion.objects.first()
    is_usuario_region = request.user.groups.filter(name="usuario_Region").exists()

    # Obtener los valores de la sesión
    rfc = request.session.get('rfc')
    claveCT = request.session.get('claveCT')
    initial_data=inicializar_Datos_Form_Constancias(rfc, claveCT)

    if request.method == 'POST':
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm(request.POST, request.FILES, initial=initial_data)
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
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm(initial=initial_data)
        if is_usuario_region:
            form.fields['incluir_logo'].disabled = True
            form.fields['logo'].disabled = True

    context = {
        'form': form,
        'editar': False
    }
    return render(request, 'constancias/nueva_constanciaCambioCTP.html', context)


@login_required
@verificar_acceso_constancia('CAMBIO_CENTRO_PREP')
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


#crear constancia viejo

# @login_required
# def crear_constancia(request):
#     user = request.user
#     configuracion = Configuracion.objects.first()
#     is_usuario_region = user.groups.filter(name="usuario_Region").exists()

#     if request.method == "POST":
#         form = ConstanciaForm(request.POST, request.FILES)
#         if form.is_valid():
#             constancia = form.save(commit=False)

#             if is_usuario_region:
#                 constancia.incluir_logo = True
#                 constancia.logo = configuracion.logo if configuracion and configuracion.logo else None
#             else:
#                 constancia.incluir_logo = form.cleaned_data.get('incluir_logo', False)
#                 constancia.logo = configuracion.logo if configuracion else None

#             constancia.save()
#             return redirect('constancia_generada', constancia_id=constancia.id)
#     else:
#         form = ConstanciaForm()
#         if is_usuario_region:
#             form.fields['incluir_logo'].disabled = True
#             form.fields['logo'].disabled = True

#     return render(request, 'constancias/crear_constancia.html', {'form': form})