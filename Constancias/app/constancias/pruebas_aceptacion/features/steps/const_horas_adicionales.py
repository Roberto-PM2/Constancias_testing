from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import time


@given(u'que ingreso mi usuario "{username}" y contraseña "{password}" horas adicionales')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/admin')
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)


@given(u'presiono el botón Identificarse horas adicionales')
def step_impl(context):
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(1)  # Espera para permitir la carga de la página


@given(u'entro a la página de registro horas adicionales')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias/crear/')
    data = {
        'rfc': '000020860d47c',
        'claveCT': '32ABJ0001W',
        'tipo_constancia': 'HORAS_ADIC'
    }
    context.driver.find_element(By.NAME, 'rfc').send_keys(data['rfc'])
    context.driver.find_element(By.NAME, 'claveCT').send_keys(data['claveCT'])
    # Seleccionar el tipo de constancia
    select_nombramiento = Select(context.driver.find_element(By.NAME, 'tipo_constancia'))
    select_nombramiento.select_by_value(data['tipo_constancia'])
    context.driver.find_element(By.ID, 'btnCrear').click()
    time.sleep(1)  # Espera para procesar la solicitud


@when(u'completo el formulario de constancia horas adicionales')
def step_impl(context):
    data = {
        'curp': 'CHAW050729MMCSHNA2',
        'filiacion': 'RFC123456',
        'nombre_completo': 'John Doe',
        'categoria_plaza': 'Profesor',
        'tipo_nombramiento': '09',
        'clave_centro_trabajo': 'CENTRO123',
        'nombre_centro_trabajo': 'Escuela Primaria',
        'direccion': '123 Calle Principal',
        'municipio': 'Ciudad',
        'localidad': 'Localidad',
        'sueldo_mensual': '12345.67',
        'partida': '7-1103',
        'fecha_input': datetime.today().strftime('%Y-%m-%d'),
        'firma': 'Capital Humano',
        'clave': 'Clave1'
    }

    # Rellenar cada campo del formulario
    context.driver.find_element(By.NAME, 'curp').clear()
    context.driver.find_element(By.NAME, 'curp').send_keys(data['curp'])
    context.driver.find_element(By.NAME, 'filiacion').send_keys(data['filiacion'])
    context.driver.find_element(By.NAME, 'nombre_completo').send_keys(data['nombre_completo'])
    context.driver.find_element(By.NAME, 'categoria_plaza').send_keys(data['categoria_plaza'])

    context.driver.find_element(By.NAME, 'clave_centro_trabajo').send_keys(data['clave_centro_trabajo'])
    context.driver.find_element(By.NAME, 'nombre_centro_trabajo').send_keys(data['nombre_centro_trabajo'])
    context.driver.find_element(By.NAME, 'direccion').send_keys(data['direccion'])
    context.driver.find_element(By.NAME, 'municipio').send_keys(data['municipio'])
    context.driver.find_element(By.NAME, 'localidad').send_keys(data['localidad'])
    # context.driver.find_element(By.NAME, 'sueldo_mensual').send_keys(data['sueldo_mensual'])
    # Seleccionar el tipo de partida desde un dropdown
    select_nombramiento = Select(context.driver.find_element(By.NAME, 'partida'))
    select_nombramiento.select_by_value(data['partida'])
    context.driver.find_element(By.NAME, 'fecha_input').send_keys(data['fecha_input'])
    context.driver.find_element(By.NAME, 'firma').send_keys(data['firma'])

    time.sleep(2)

    # Rellenar campos de "claves[]"
    context.driver.find_element(By.ID, 'clave-nueva').send_keys(data['clave'])
    # for i, clave in enumerate(data['claves[]']):
    #     clave_field = context.driver.find_element(By.ID, f'clave-{i+1}')  # Asegúrate de usar el ID correcto
    #     clave_field.send_keys(clave)


@when(u'presiono el botón de guardar constancia horas adicionales')
def step_impl(context):
    context.driver.find_element(By.ID, 'btnAgregar').click()
    time.sleep(1)  # Espera para procesar la solicitud
    context.driver.get('http://localhost:8000/constancias/lista/')
    time.sleep(2)


@then(u'puedo ver mi constancia de horas adicionales')
def step_impl(context):
    tb_resultados = context.driver.find_element(By.ID, 'tbResultados')
    trs = tb_resultados.find_elements(By.TAG_NAME, 'tr')
    constancias = []
    constancia = "CHAW050729MMCSHNA2"

    for tr in trs:
        tds = tr.find_elements(By.TAG_NAME, 'td')
        constancias.append(tds[0].text)

    assert constancia in constancias, \
        f"La constancia no se encuentra en la lista"

    time.sleep(5)
