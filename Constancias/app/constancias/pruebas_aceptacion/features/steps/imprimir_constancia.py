from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from datetime import datetime
import time


@given(u'que inicio sesión como usuario region "{username}" y contraseña "{password}"')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/constancias/login')
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(1)


@given(u'ingreso en el menu de creacion mi rfc "{rfc}" y clave "{clave}"')
def step_impl(context, rfc, clave):
    time.sleep(1)
    context.driver.get('http://localhost:8000/constancias/crear/')
    data = {
        'tipo_constancia': 'OTRO'
    }
    context.driver.find_element(By.NAME, 'rfc').send_keys(rfc)
    context.driver.find_element(By.NAME, 'claveCT').send_keys(clave)
    # Seleccionar el tipo de constancia
    select_constancia = Select(context.driver.find_element(By.NAME, 'tipo_constancia'))
    select_constancia.select_by_value(data['tipo_constancia'])
    context.driver.find_element(By.ID, 'btnCrear').click()
    time.sleep(1)  # Espera para procesar la solicitud


@given(u'completo el formulario de la constancia para imprimir')
def step_impl(context):
    data = {
        'categoria_plaza': 'Profesor',
        'tipo_nombramiento': '09',
        'sueldo_mensual': '12345.67',
        'partida': '7-1103',
        'fecha_input': datetime.today().strftime('%Y-%m-%d'),
        'motivo_constancia': 'Por motivos personales',
        'firma': 'Capital Humano',
        'clave': 'Clave1'
    }

    context.driver.find_element(By.NAME, 'categoria_plaza').send_keys(data['categoria_plaza'])

    # Seleccionar el tipo de nombramiento desde un dropdown
    select_nombramiento = Select(context.driver.find_element(By.NAME, 'tipo_nombramiento'))
    select_nombramiento.select_by_value(data['tipo_nombramiento'])

    context.driver.find_element(By.NAME, 'sueldo_mensual').send_keys(data['sueldo_mensual'])
    # Seleccionar el tipo de partida desde un dropdown
    select_nombramiento = Select(context.driver.find_element(By.NAME, 'partida'))
    select_nombramiento.select_by_value(data['partida'])
    context.driver.find_element(By.NAME, 'fecha_input').send_keys(data['fecha_input'])
    context.driver.find_element(By.NAME, 'motivo_constancia').send_keys(data['motivo_constancia'])
    context.driver.find_element(By.NAME, 'firma').send_keys(data['firma'])

    time.sleep(1)

    context.driver.find_element(By.ID, 'clave-nueva').send_keys(data['clave'])


@given(u'presiono el botón guardar constancia y se crea la constancia')
def step_impl(context):
    context.driver.find_element(By.ID, 'btnAgregar').click()
    time.sleep(2)


@when(u'presiono el botón Imprimir')
def step_impl(context):
    context.driver.find_element(By.ID, 'boton-imprimir').click()
    time.sleep(2)


@then(u'la constancia se manda a imprimir')
def step_impl(context):
    alert = context.driver.switch_to.alert
    assert "Constancia enviada a imprimir, haz clic en aceptar para continuar" in alert.text, "La constancia no se mandó a imprimir"
    alert.accept()
