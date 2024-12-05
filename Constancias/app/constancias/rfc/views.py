from django.shortcuts import render
from django.db import connections
import re


def validar_rfc(rfc):
    """Valida que el RFC tenga 13 caracteres y no contenga caracteres especiales."""
    if not re.match(r"^[A-Za-z0-9]+$", rfc):
        return False, "El RFC no debe contener caracteres especiales."
    if len(rfc) != 13:
        return False, "El RFC debe tener 13 caracteres."
    return True, ""


def ingresar_rfc(request):
    if request.method == 'POST':
        rfc = request.POST.get('rfc', '').strip()

        es_valido, error = validar_rfc(rfc)
        if not es_valido:
            return render(request, 'ingresar_rfc.html', {'error': error})

        sql = """
           SELECT NOMBRE, CURP FROM EMPLEADO_COMP WHERE RFC = %s
        """
        with connections['personal'].cursor() as cursor:
            cursor.execute(sql, [rfc])
            result = cursor.fetchone()

        if result:
            empleado = {"nombre": result[0], "curp": result[1], "rfc": rfc}
            return render(request, 'seleccionar_constancia.html', {'empleado': empleado})
        else:
            return render(request, 'ingresar_rfc.html', {'error': "No se encontró un empleado con el RFC ingresado."})

    return render(request, 'ingresar_rfc.html')


def ver_constancia(request, tipo):
    rfc = request.GET.get('rfc')
    sql = """
        SELECT NOMBRE, CURP FROM EMPLEADO_COMP WHERE RFC = %s
    """
    with connections['personal'].cursor() as cursor:
        cursor.execute(sql, [rfc])
        result = cursor.fetchone()

    if not result:
        return render(request, 'error.html', {'mensaje': 'No se encontró el empleado.'})

    empleado = {"nombre": result[0], "curp": result[1], "rfc": rfc}
    return render(request, f'constancia_{tipo}.html', {'empleado': empleado})
