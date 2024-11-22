# app/constancias/rfc/views.py
from django.shortcuts import render, redirect
from django.db import connection

def validar_rfc(rfc):
    if len(rfc) != 13:  # Longitud estándar del RFC de persona moral o física
        return "El RFC debe tener 13 caracteres."
    if not rfc.isalnum():
        return "El RFC solo debe contener letras y números."
    return None

def verificar_rfc(request):
    if request.method == 'POST':
        rfc = request.POST.get('rfc', '').strip()
        
        # Validación de formato del RFC
        mensaje_error = validar_rfc(rfc)
        if mensaje_error:
            return render(request, 'validar_rfc.html', {'error': mensaje_error})

        # Verificar existencia en la base de datos
        with connection.cursor() as cursor:
            cursor.execute("SELECT rfc, nombre, curp FROM EMPLEADO_COMP WHERE rfc = %s", [rfc])
            row = cursor.fetchone()
        
        if row is None:
            return render(request, 'validar_rfc.html', {'error': "Empleado no encontrado."})

        # Guardar datos en sesión para que estén disponibles en la selección de constancia
        request.session['datos_empleado'] = {'RFC': row[0], 'nombre': row[1], 'CURP': row[2]}
        return redirect('seleccionar_constancia')
    
    return render(request, 'validar_rfc.html')

def seleccionar_constancia(request):
    datos_empleado = request.session.get('datos_empleado')
    if not datos_empleado:
        return redirect('verificar_rfc')
    
    constancia_tipo = request.POST.get('tipo_constancia', 'Constancia Vertical')
    datos_empleado['tipo_constancia'] = constancia_tipo  # Agregar el tipo de constancia seleccionado

    if request.method == 'POST':
        return render(request, 'mostrar_constancia.html', datos_empleado)
    
    return render(request, 'seleccionar_constancia.html', datos_empleado)
