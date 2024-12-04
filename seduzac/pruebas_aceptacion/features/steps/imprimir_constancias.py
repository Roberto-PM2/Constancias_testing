from behave import  given, when , then 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time

@given(u'que inicio sesión como usuario region "{grupo}"')
def step_impl(context, grupo):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/constancias/login')
    context.driver.find_element(By.NAME, 'username').send_keys('usuario_region')
    context.driver.find_element(By.NAME, 'password').send_keys('region1234')
    context.driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(2)

@given(u'completo el formulario de la constancia con "{nombre}"')
def step_impl(context, nombre):
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)

@given(u'presiono el botón Crear constancia y se crea la constancia')
def step_impl(context):
    context.driver.find_element(By.ID, 'Crear Constancia').click()
    time.sleep(2)

@when(u'presiono el botón Imprimir')
def step_impl(context):
    context.driver.find_element(By.ID, 'boton-imprimir').click()
    time.sleep(2)

@then(u'la constancia se manda a imprimir')
def step_impl(context):
    alert = context.driver.switch_to.alert
    assert "Constancia enviada a imprimir" in alert.text, "La constancia no se mandó a imprimir"
    alert.accept()