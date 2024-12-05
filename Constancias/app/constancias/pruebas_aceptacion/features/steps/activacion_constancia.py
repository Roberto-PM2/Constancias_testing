from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from selenium.common.exceptions import NoSuchElementException


@given(u'que ingreso mi usuario "{username}" y contraseña "{password}" admin')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/admin')
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)


@given(u'presiono el botón Identificarse como admin')
def step_impl(context):
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(1)  # Espera para permitir la carga de la página


@given(u'cambio el estado de constancia otro motivo a desactivada')
def step_impl(context):
    # Paso 1: Ir a la lista de constancias desde el panel de administración
    context.driver.get('http://localhost:8000/admin/agregar_constancia/constanciaaccesscontrol/')

    # Paso 2: Seleccionar la casilla de verificación de la constancia "OTRO"
    checkbox_otro = context.driver.find_element(By.CSS_SELECTOR, 'input[type="checkbox"][aria-label*="OTRO"]')
    checkbox_otro.click()  # Marca la casilla de selección para la acción

    # Paso 3: Desmarcar el checkbox "habilitado" correspondiente
    checkbox_habilitado = context.driver.find_element(By.ID, 'id_form-8-habilitado')
    if checkbox_habilitado.is_selected():  # Asegurarse de desmarcarlo
        checkbox_habilitado.click()

    # Paso 4: Guardar cambios
    save_button = context.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Save"]')
    save_button.click()
    time.sleep(5)


@when(u'viajo al formulario de creacion de constancias a verificar')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias/crear/')
    time.sleep(5)


@then(u'ya no aparece otro motivo')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias/crear/')
    data = {
        'rfc': '000020860d47c',
        'claveCT': '32ABJ0001W',
        'tipo_constancia': 'OTRO'
    }
    # Llenar los campos requeridos
    context.driver.find_element(By.NAME, 'rfc').send_keys(data['rfc'])
    context.driver.find_element(By.NAME, 'claveCT').send_keys(data['claveCT'])

    # Verificar que "OTRO" no esté en el select de tipo_constancia
    select_tipo = Select(context.driver.find_element(By.NAME, 'tipo_constancia'))
    try:
        select_tipo.select_by_value(data['tipo_constancia'])
        # Si no se lanza excepción, el valor está disponible (falla la prueba)
        raise AssertionError(f'El tipo de constancia "{data["tipo_constancia"]}" todavía está disponible en el select.')
    except NoSuchElementException:
        # Si se lanza la excepción, significa que no está disponible (éxito esperado)
        pass

# activar----------------------


@given(u'cambio el estado de constancia otro motivo a activada')
def step_impl(context):
    # Paso 1: Ir a la lista de constancias desde el panel de administración
    context.driver.get('http://localhost:8000/admin/agregar_constancia/constanciaaccesscontrol/')

    # Paso 2: Localizar el checkbox de habilitación para "OTRO"
    checkbox_habilitado_otro = context.driver.find_element(By.ID, 'id_form-8-habilitado')

    # Verificar si está desmarcado y marcarlo si es necesario
    if not checkbox_habilitado_otro.is_selected():
        checkbox_habilitado_otro.click()

    # Paso 3: Guardar cambios
    save_button = context.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"][value="Save"]')
    save_button.click()

    # Esperar para confirmar que los cambios se han guardado
    time.sleep(5)


@then(u'si me aparece otro motivo')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias/crear/')
    data = {
        'rfc': '000020860d47c',
        'claveCT': '32ABJ0001W',
        'tipo_constancia': 'OTRO'
    }
    # Llenar los campos requeridos
    context.driver.find_element(By.NAME, 'rfc').send_keys(data['rfc'])
    context.driver.find_element(By.NAME, 'claveCT').send_keys(data['claveCT'])

    # Verificar que "OTRO" sí esté en el select de tipo_constancia
    select_tipo = Select(context.driver.find_element(By.NAME, 'tipo_constancia'))
    try:
        select_tipo.select_by_value(data['tipo_constancia'])
        # Si se selecciona sin problemas, la prueba pasa
        print(f'El tipo de constancia "{data["tipo_constancia"]}" está disponible en el select.')
    except NoSuchElementException:
        # Si se lanza la excepción, la prueba falla
        raise AssertionError(f'El tipo de constancia "{data["tipo_constancia"]}" no está disponible en el select.')
    time.sleep(5)
