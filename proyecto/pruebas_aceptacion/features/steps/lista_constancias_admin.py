from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

@given(u'que ingreso mi usuario administrador "{username}" y contraseña "{password}"')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/admin')  
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(5)  

@when(u'visito la página de las constancias')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias/')  
    time.sleep(5)  

@then(u'veo todas las constancias (activas e inactivas)')
def step_impl(context):
    filas = context.driver.find_elements(By.CSS_SELECTOR, 'tbody tr')
    assert len(filas) > 0, "No se encontraron constancias en la tabla"

    for fila in filas:
        estado_td = fila.find_element(By.CSS_SELECTOR, 'td[id^="estado-"]')
        estado_texto = estado_td.text.strip()
        assert estado_texto in ['Activa', 'Inactiva'], f"Estado inesperado: {estado_texto}"

    context.driver.quit()