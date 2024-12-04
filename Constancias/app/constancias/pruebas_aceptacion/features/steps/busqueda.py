from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time


@given(u'que accedo a la sección de búsqueda de constancias')
def acceder_seccion_busqueda(context):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/filtros/buscar_constancias/')


@when(u'ingreso "{nombre}" en el filtro de nombre')
def ingresar_nombre(context, nombre):
    time.sleep(3)
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    time.sleep(3)


@when(u'presiono el botón de "Buscar"')
def presionar_boton_buscar(context):
    time.sleep(3)
    context.driver.find_element(By.ID, 'btnBuscar').click()
    time.sleep(3)


@then(u'el sistema muestra únicamente las constancias que coincidan con el nombre "{nombre}"')
def verificar_resultados_nombre(context, nombre):
    resultados = context.driver.find_elements(
        By.CLASS_NAME, 'resultado_constancia')
    assert all(nombre.lower() in resultado.text.lower() for resultado in resultados), \
        f"No se encontraron resultados coincidentes con el nombre '{nombre}'"
    context.driver.quit()


@when(u'ingreso "{fecha}" en el filtro de fecha de emisión')
def ingresar_fecha(context, fecha):
    fecha_input = context.driver.find_element(By.NAME, 'fecha_emision')
    fecha_input.clear()
    fecha_input.send_keys(fecha)
    time.sleep(1)


@then(u'el sistema muestra solo las constancias emitidas en la fecha "{fecha}"')
def verificar_resultados_fecha(context, fecha):
    resultados = context.driver.find_elements(
        By.CLASS_NAME, 'resultado_constancia')
    assert all(fecha in resultado.text for resultado in resultados), \
        f"No se encontraron constancias con la fecha de emisión '{fecha}'"
    context.driver.quit()


@when(u'ingreso "{rfc}" en el filtro de RFC')
def ingresar_rfc(context, rfc):
    rfc_input = context.driver.find_element(By.NAME, 'rfc')
    rfc_input.clear()
    rfc_input.send_keys(rfc)
    time.sleep(1)


@when(u'ingreso un RFC inválido "{rfc}" en el filtro de RFC')
def ingresar_rfc_invalido(context, rfc):
    rfc_input = context.driver.find_element(By.NAME, 'rfc')
    rfc_input.clear()
    rfc_input.send_keys(rfc)
    time.sleep(10)


@then(u'el sistema muestra el mensaje de error "{msj_rfc_error}"')
def verificar_mensaje_error_rfc(context, msj_rfc_error):
    mensaje_error = context.driver.find_element(By.ID, 'rfc-error')
    time.sleep(10)
    assert mensaje_error.is_displayed(
    ), "El mensaje de error para RFC no válido no se mostró"
    assert mensaje_error.text == msj_rfc_error, \
        f"El mensaje de error para RFC no coincide con el esperado. \
        Se encontró: {mensaje_error.text} y no {msj_rfc_error}"
    context.driver.quit()


@then(u'el sistema muestra únicamente la constancia que coincide con el RFC {rfc}')
def verificar_resultados_rfc(context, rfc):
    resultados = context.driver.find_elements(
        By.CLASS_NAME, 'resultado_constancia')
    assert all(rfc in resultado.text for resultado in resultados), \
        f"No se encontraron constancias con el RFC '{rfc}'"
    context.driver.quit()


@when(u'ingreso un nombre invalido "{nombre_invalido}" en el filtro de nombre')
def ingresar_nombre_invalido(context, nombre_invalido):
    nombre_input = context.driver.find_element(By.NAME, 'nombre')
    nombre_input.clear()
    nombre_input.send_keys(nombre_invalido)
    time.sleep(1)


@then(u'el sistema muestra el mensaje "{mensaje}"')
def verificar_mensaje_error(context, mensaje):
    mensaje_error = context.driver.find_element(By.ID, 'mensaje_error')
    assert mensaje_error.text == mensaje, \
        "El mensaje de error no se mostró o no coincide con el esperado"
    context.driver.quit()


@when(u'presiono el botón de "Restablecer filtros"')
def presionar_boton_restablecer(context):
    time.sleep(2)
    context.driver.find_element(By.ID, 'btnRestablecer').click()
    time.sleep(1)


@then(u'todos los campos del formulario están vacíos')
def verificar_campos_vacios(context):
    nombre_input = context.driver.find_element(By.NAME, 'nombre')
    fecha_input = context.driver.find_element(By.NAME, 'fecha_emision')
    rfc_input = context.driver.find_element(By.NAME, 'rfc')

    assert nombre_input.get_attribute(
        'value') == '', "El campo de nombre no está vacío"
    assert fecha_input.get_attribute(
        'value') == '', "El campo de fecha de emisión no está vacío"
    assert rfc_input.get_attribute(
        'value') == '', "El campo de RFC no está vacío"

    context.driver.quit()


@then(u'el sistema muestra únicamente la constancia que coincide con el nombre "{nombre}", fecha "{fecha}" y RFC "{rfc}"')
def verifica_resultados_varios_filtros(context, nombre, fecha, rfc):
    resultados = context.driver.find_elements(
        By.CLASS_NAME, 'resultado_constancia')
    # Verificar que cada resultado contiene el nombre, la fecha y el RFC
    assert all(
        nombre.lower() in resultado.text.lower() and
        fecha in resultado.text and
        rfc in resultado.text
        for resultado in resultados
    ), f"No se encontraron constancias que coincidan con nombre '{nombre}', fecha '{fecha}', y RFC '{rfc}'"
    context.driver.quit()

@when(u'selecciono "{tipo_constancia}" en el filtro de tipo de constancia')
def seleccionar_tipo_constancia(context, tipo_constancia):
    select = Select(context.driver.find_element(By.NAME, 'tipo_constancia'))
    select.select_by_visible_text(tipo_constancia)
    context.driver.find_element(By.ID, 'btnBuscar').click()
    time.sleep(2)


@then(u'el sistema muestra únicamente las constancias de tipo "{tipo_constancia}"')
def verificar_resultados_tipo_constancia(context, tipo_constancia):
    resultados = context.driver.find_elements(By.CLASS_NAME, 'result-item')
    assert all(tipo_constancia in resultado.text for resultado in resultados), \
        f"No se encontraron constancias de tipo '{tipo_constancia}'"

@when(u'selecciono "{estado}" en el filtro de estado')
def seleccionar_estado(context, estado):
    select = Select(context.driver.find_element(By.NAME, 'activa'))
    select.select_by_visible_text(estado)
    context.driver.find_element(By.ID, 'btnBuscar').click()
    time.sleep(2)

@then(u'el sistema muestra únicamente las constancias "{estado}"')
def verificar_resultados_estado(context, estado):
    resultados = context.driver.find_elements(By.CLASS_NAME, 'result-item')
    assert all(estado.lower() in resultado.text.lower() for resultado in resultados), \
        f"No se encontraron constancias con estado '{estado}'"