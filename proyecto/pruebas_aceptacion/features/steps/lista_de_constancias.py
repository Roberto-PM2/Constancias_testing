from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

@given(u'que ingreso mi usuario "{username}" y contraseña "{password}"')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/accounts/login')  
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)

@when(u'presiono el boton iniciar sesion')
def step_impl(context):
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(1)

@when(u'visito la pagina de las constancias')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias')  
    time.sleep(1)

@then(u'veo solo las constancias activas')
def step_impl(context):
    constancias = context.driver.find_elements(By.CLASS_NAME, 'constancia-activa')  
    for constancia in constancias:
        estado = constancia.get_attribute('data-activo')
        assert estado == 'True', f"Se encontró una constancia inactiva con estado {estado}"
    time.sleep(1)
    context.driver.quit()
