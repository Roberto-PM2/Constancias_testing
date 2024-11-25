from django.shortcuts import render
from agregar_constancia.models import Constancia

def buscar_constancias(request):
    nombre = request.GET.get('nombre', '')
    fecha_emision = request.GET.get('fecha_emision', '')
    rfc = request.GET.get('rfc', '')
    tipo_constancia = request.GET.get('tipo_constancia', '')

    # Inicia con todas las constancias
    constancias = Constancia.objects.all()

    # Aplicar filtros según los parámetros
    if nombre:
        constancias = constancias.filter(nombre_completo__icontains=nombre)
    if fecha_emision:
        constancias = constancias.filter(fecha_creacion_constancia=fecha_emision)
    if rfc:
        constancias = constancias.filter(filiacion__icontains=rfc)
    if tipo_constancia:
        constancias = constancias.filter(tipo_constancia=tipo_constancia)

    # Contexto para la plantilla
    context = {
        'constancias': constancias,
        'filtros_aplicados': any([nombre, fecha_emision, rfc, tipo_constancia]),
        'nombre': nombre,
        'fecha_emision': fecha_emision,
        'rfc': rfc,
        'tipo_constancia': tipo_constancia,
        'tipos_constancia': Constancia.TIPOS_CONSTANCIA,  # Enviar los choices
    }
    return render(request, 'buscar_constancias.html', context)
