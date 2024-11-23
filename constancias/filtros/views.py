from django.shortcuts import render
from .models import Constancia


def buscar_constancias(request):
    nombre = request.GET.get('nombre', '')
    fecha_emision = request.GET.get('fecha_emision', '')
    rfc = request.GET.get('rfc', '')

    filtros_aplicados = nombre or fecha_emision or rfc
    constancias = []

    if filtros_aplicados:
        constancias = Constancia.objects.all()
        if nombre and len(nombre) > 2:
            constancias = constancias.filter(nombre__icontains=nombre)
        if fecha_emision:
            constancias = constancias.filter(fecha_emision=fecha_emision)
        if rfc:
            constancias = constancias.filter(rfc__iexact=rfc)

    context = {
        'constancias': constancias,
        'filtros_aplicados': filtros_aplicados,
        'nombre': nombre,
        'fecha_emision': fecha_emision,
        'rfc': rfc,
    }
    return render(request, 'buscar_constancias.html', context)
