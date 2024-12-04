from behave import given, when, then 
from selenium import webdriver 
from selenium.webdriver.common.by import By 
import time

@given(u'que ingreso al sistema')
def step_impl(context):
    context.driver = webdriver.Chrome()


@when(u'ingreso a la url "{url}"')
def step_impl(context,url):
    context.driver.get(url)

@then(u'puedo ver la página principal con el mensaje "{mensaje}"')
def step_impl(context,mensaje):
    time.sleep(4)
    mensaje_obtenido = context.driver.find_element(By.ID, 'mensaje-bienvenida').text
    assert mensaje == mensaje_obtenido, \
        f"El mensaje obtenido es {mensaje_obtenido} y el mensaje esperado es {mensaje}"
