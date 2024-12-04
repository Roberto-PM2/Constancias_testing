from behave import  given, when , then 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By 
import time

@given(u'que inicio sesión como usuario del grupo region "{grupo}"')
def step_impl(context, grupo):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/constancias/login')
    context.driver.find_element(By.NAME, 'username').send_keys('usuario_region')
    context.driver.find_element(By.NAME, 'password').send_keys('region1234')
    context.driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(3)

@given(u'lleno el formulario de la constancia con "{nombre}"')
def step_impl(context, nombre):
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)

@when(u'presiono el botón Crear constancia')
def step_impl(context):
    context.driver.find_element(By.ID, 'Crear Constancia').click()
    time.sleep(2)

@then(u'la constancia incluye el logo institucional')
def step_impl(context):
    constancia_logo = context.driver.find_element(By.ID, 'logo-constancia').is_displayed()
    assert constancia_logo, "El logo institucional no se incluyó en la constancia"


@given(u'que inicio sesión como usuario del grupo central "{grupo}"')
def step_impl(context, grupo):
    context.driver = webdriver.Chrome()
    context.driver.get('http://localhost:8000/constancias/login')
    username = 'usuario_central'
    password = 'central1234'   
    context.driver.find_element(By.NAME, 'username').send_keys(username)
    context.driver.find_element(By.NAME, 'password').send_keys(password)
    context.driver.find_element(By.TAG_NAME, 'button').click()
    time.sleep(2)

@given(u'lleno el formulario de la constancia con "{nombre}" y sin logo')
def step_impl(context, nombre):
    context.driver.get('http://localhost:8000/constancias/crear')
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    logo_checkbox = context.driver.find_element(By.ID, 'id_incluir_logo')
    if logo_checkbox.is_selected():
        logo_checkbox.click()


@then(u'la constancia no incluye el logo institucional')
def step_impl(context):
    try:
        context.driver.find_element(By.ID, 'logo-constancia')
        logo_presente = True
    except Exception:
        logo_presente = False
    
    assert not logo_presente, "El logo institucional fue incluido en la constancia, pero no debería estarlo"

@given(u'lleno el formulario de la constancia con "{nombre}" y con logo')
def step_impl(context, nombre):
    context.driver.get('http://localhost:8000/constancias/crear')
    context.driver.find_element(By.NAME, 'nombre').send_keys(nombre)
    logo_checkbox = context.driver.find_element(By.ID, 'id_incluir_logo')
    if not logo_checkbox.is_selected():
        logo_checkbox.click()