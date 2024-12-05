import os
import django

def before_all(context):
    print("Configurando Django...")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'constancias.settings'
    django.setup()
    print("Django configurado correctamente.")
