from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

@given(u'que ingreso a la pagina como administrador "{username}" y contraseña "{password}"')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()  # Cambia a tu driver configurado
    context.driver.get("http://localhost:8000/admin")  # URL de tu login
    
    # Esperar 2 segundos para que cargue la página de login
    time.sleep(2)
    
    # Realiza el login
    context.driver.find_element(By.NAME, "username").send_keys(username)
    context.driver.find_element(By.NAME, "password").send_keys(password)
    context.driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

@when(u'visito la página de la lista de constancias')
def step_impl(context):
    context.driver.get("http://localhost:8000/constancias/")  # Ajusta la URL según tu proyecto
    
    # Esperar 5 segundos para que la página de constancias cargue
    time.sleep(5)

@when(u'selecciono una constancia marcada como "Inactiva"')
def step_impl(context):
    # Esperar 2 segundos para que los botones de estado estén disponibles
    time.sleep(2)
    
    # Busca una constancia inactiva
    context.inactive_constancia = context.driver.find_element(By.CSS_SELECTOR, "button.button-toggle.inactiva")
    assert context.inactive_constancia, "No se encontró una constancia inactiva"

@when(u'elijo la opción de "Activar"')
def step_impl(context):
    # Haz clic en el botón "Activar"
    context.inactive_constancia.click()
    
    # Espera 2 segundos para que el cambio de estado se procese
    time.sleep(2)

@then(u'el sistema debe cambiar el estado de la constancia a "Activa"')
def step_impl(context):
    # Extraer el ID de la constancia seleccionada
    constancia_id = context.inactive_constancia.get_attribute("id").split("-")[1]
    
    # Esperar 3 segundos para verificar el cambio de estado
    time.sleep(3)
    
    # Verificar que el estado de la constancia cambió a "Activa"
    estado_actual = context.driver.find_element(By.ID, f"estado-{constancia_id}").text
    assert estado_actual == "Activa", "El estado de la constancia no cambió a 'Activa'"
    
    # Cerrar el navegador
    context.driver.quit()
