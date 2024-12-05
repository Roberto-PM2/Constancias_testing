from behave import  given, when , then 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time

@given(u'que ingreso mi usuario "{username}" y contraseña "{password}"')
def step_impl(context, username, password):
    context.driver =  webdriver.Chrome()
    context.driver.get('http://localhost:8000/constancias/login')
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)


@when(u'presiono el botón  Iniciar sesión')
def step_impl(context):
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(3)


@then(u'puedo ver el mensaje de "{mensaje}"')
def step_impl(context,mensaje):
    try:
        mensaje_obtenido = context.driver.find_element(By.ID, "mensaje-principal").text
    except:
        mensaje_obtenido = context.driver.find_element(By.TAG_NAME, "p").text
    assert mensaje in mensaje_obtenido, f"El menasje esperado es {mensaje} y el obtenido es {mensaje_obtenido}"
    time.sleep(1)