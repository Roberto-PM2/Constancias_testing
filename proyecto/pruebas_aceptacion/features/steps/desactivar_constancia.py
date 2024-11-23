from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Paso 1: Iniciar sesión como administrador
@given(u'que ingreso al sistema como administrador "{username}" y contraseña "{password}"')
def step_impl(context, username, password):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/admin')  # URL del login
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)
    context.driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(3)  # Espera breve para que cargue la página

# Paso 2: Entrar a la página de lista de constancias
@when(u'entro a la página de la lista de constancias')
def step_impl(context):
    context.driver.get('http://localhost:8000/constancias/')  # URL de constancias
    time.sleep(3)  # Espera breve para la carga de constancias

# Paso 3: Seleccionar una constancia marcada como "Activa"
@when(u'selecciono una constancia marcada como "Activa"')
def step_impl(context):
    constancias_activas = context.driver.find_elements(By.CSS_SELECTOR, 'td[id^="estado-"]')
    context.constancia_id = None
    for constancia in constancias_activas:
        if constancia.text.strip() == "Activa":
            # Guardar el ID de la constancia para desactivarla
            context.constancia_id = constancia.get_attribute("id").split("-")[1]
            break
    assert context.constancia_id is not None, "No se encontró ninguna constancia activa para desactivar"

# Paso 4: Elegir la opción de "Desactivar"
@when(u'elijo la opción de "Desactivar"')
def step_impl(context):
    # Encontrar el botón de desactivar usando el ID de la constancia obtenida en el paso anterior
    boton_desactivar = context.driver.find_element(By.ID, f"button-{context.constancia_id}")
    boton_desactivar.click()
    time.sleep(3)  # Espera para que el estado se actualice

# Paso 5: Verificar que el estado de la constancia cambie a "Inactiva"
@then(u'el sistema debe cambiar el estado de la constancia a "Inactiva"')
def step_impl(context):
    estado_actualizado = context.driver.find_element(By.ID, f"estado-{context.constancia_id}")
    assert estado_actualizado.text.strip() == "Inactiva", "La constancia no se desactivó correctamente"
    context.driver.quit()

