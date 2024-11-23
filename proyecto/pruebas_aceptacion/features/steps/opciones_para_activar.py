import time
from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Paso 1: Iniciar sesión como administrador
@given(u'que ingreso como administrador "{username}" y contraseña "{password}"')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/admin')  # Cambia a la URL correcta del login
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(3)  # Pausa para permitir la carga de la página

# Paso 2: Visitar la página de las constancias
@when(u'veo la página de las constancias')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias/')  # Cambia a la URL correcta de la lista de constancias
    time.sleep(3)  # Esperar para que la página cargue las constancias

# Paso 3: Ver las constancias inactivas
@when(u'veo las constancias inactivas')
def step_impl(context):
    # Buscar botones con la clase 'button-toggle inactiva' para identificar constancias inactivas
    constancias_inactivas = context.driver.find_elements(By.CSS_SELECTOR, '.button-toggle.inactiva')
    assert len(constancias_inactivas) > 0, "No se encontraron constancias inactivas o no cargaron a tiempo."

# Paso 4: Verificar la opción "Activar"
@then(u'el sistema debe mostrar la opción "Activar" junto a la constancia inactiva')
def step_impl(context):
    # Confirmar que el botón con la clase 'button-toggle inactiva' muestra el texto "Activar"
    boton_activar = context.driver.find_element(By.CSS_SELECTOR, '.button-toggle.inactiva')
    assert boton_activar.is_displayed(), "El botón 'Activar' no se muestra junto a la constancia inactiva."
    assert boton_activar.text == "Activar", "El botón junto a la constancia inactiva no muestra 'Activar'."
    context.driver.quit()
