from behave import  given, when , then 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time

@given(u'que he generado una constancia correctamente con "{nombre}')
def step_impl(context,nombre):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/constancias/login')
    context.driver.find_element(By.NAME, 'username').send_keys('usuario_region')
    context.driver.find_element(By.NAME, 'password').send_keys('region1234')
    context.driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(2)
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    context.driver.find_element(By.ID, 'Crear Constancia').click()
    time.sleep(2)

@given(u'estoy en la página de la constancia generada')
def step_impl(context):
    titulo = context.driver.find_element(By.TAG_NAME, "h1").text
    assert titulo == "Constancia", "No se encuentra en la página de la constancia generada"


@when(u'presiono el botón "Generar otra constancia"')
def step_impl(context):
    context.driver.find_element(By.ID, 'Generar_otra _constancia').click()
    time.sleep(2)

@then(u'soy redirigido a la página de creación de una nueva constancia')
def step_impl(context):
    current_url = context.driver.current_url
    assert "http://localhost:8000/constancias/crear" in current_url, f"No se redirigió correctamente. URL actual: {current_url}"

@then(u'puedo ver el título "Crear Constancia"')
def step_impl(context):
    titulo = context.driver.find_element(By.TAG_NAME, "h2").text
    assert titulo == "Crear Constancia", "No se encontró el título correcto en la página de creación"