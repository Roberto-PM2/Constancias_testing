from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

@given('que ingreso mi RFC "{rfc}" en el formulario')
def step_impl(context, rfc):
    context.driver = webdriver.Chrome()
    context.driver.get("http://127.0.0.1:8000/rfc")
    context.driver.find_element(By.NAME, "rfc").send_keys(rfc)
    time.sleep(2)

@when("presiono el botón Verificar")
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)  # Esperar la redirección


@then('debo ver el nombre del empleado "{nombre}"')
def step_impl(context, nombre):
    print(f"Nombre del empleado: {nombre}")
    empleado_element = context.driver.find_element(By.ID, "empleado")
    assert nombre in empleado_element.text

@then('debo ver el mensaje de error "{error_message}"')
def step_impl(context, error_message):
    error_element = context.driver.find_element(By.ID, "mensaje_error")
    assert error_element.text == error_message
    context.driver.quit()