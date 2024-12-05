from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from agregar_constancia.models import (
    Constancia,
    Configuracion,
)
from .forms import ConstanciaSearchForm
from constancias import settings
import os


class ConstanciaFormTests(TestCase):
    def test_form_campos_no_requeridos(self):
        # Verificar que los campos del formulario no sean requeridos
        form = ConstanciaSearchForm()
        self.assertFalse(form.fields['nombre'].required)
        self.assertFalse(form.fields['fecha_emision'].required)
        self.assertFalse(form.fields['rfc'].required)

    def test_form_datos_validos(self):
        # Prueba el formulario con datos validos
        form_data = {
            'nombre': 'Juan Pérez',
            'fecha_emision': '2024-01-01',
            'rfc': 'PECJ801201ABC'
        }
        form = ConstanciaSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_datos_vacios(self):
        # Prueba el formulario con datos vacios
        form_data = {}
        form = ConstanciaSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_nombre_longitud_minima(self):
        # Prueba longitud mínima del campo nombre en el formulario
        form_data = {'nombre': 'Jo'}
        form = ConstanciaSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_rfc_longitud_maxima(self):
        # Prueba longitud máxima del campo rfc en el formulario
        form_data = {'rfc': 'A' * 14}
        form = ConstanciaSearchForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rfc', form.errors)

# test de models de constancia estan en la carpeta agregar constancia


class BuscarConstanciasViewTests(TestCase):
    databases = {'default', 'personal'}  # Permite el acceso a 'personal'

    def setUp(self):
        # Crear un usuario de prueba
        # Crear usuario para autenticación
        self.user = User.objects.create_superuser(username='testsuperuser', password='12345')
        self.client = Client()
        self.client.login(username='testsuperuser', password='12345')  # Iniciar sesión como superusuario

        # Configurar datos de sesión
        session = self.client.session
        session['rfc'] = '000020860d47c'  # RFC de ejemplo
        session['claveCT'] = '32ABJ0001W'  # Clave de centro de trabajo de ejemplo
        session.save()  # Guarda los cambios en la sesión
        self.url = "http://localhost:8000/filtros/buscar_constancias/"

        # Crear configuración inicial
        self.configuracion = Configuracion.objects.create(logo='test_logo.png')

        # Crear o recuperar el grupo 'usuario_Region'
        group_usuario_region, created = Group.objects.get_or_create(name="usuario_Region")

        # Asignar el usuario al grupo
        self.user.groups.add(group_usuario_region)

        # Ruta del archivo 'hola.jpg' en tu carpeta 'media'
        logo_path = os.path.join(settings.MEDIA_ROOT, 'hola.jpg')

        # Verificar que el archivo existe
        self.assertTrue(os.path.exists(logo_path), "El archivo 'hola.jpg' no existe en la carpeta media")

        # Abrir el archivo 'hola.jpg' en modo binario y crear un SimpleUploadedFile
        with open(logo_path, 'rb') as f:
            logo_file = SimpleUploadedFile('hola.jpg', f.read(), content_type='image/jpeg')

        # Crear las constancias de prueba con el archivo 'hola.jpg'
        Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='OTRO',
            curp='RACW050729MMCSHNA2',
            filiacion='PECJ801201ABC',
            nombre_completo='Juan Pérez',
            categoria_plaza='Estatal',
            tipo_nombramiento='09',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Motivo de la constancia',
            firma='Director General',
            incluir_logo=False,
            logo=logo_file,  # Usar SimpleUploadedFile con el archivo 'hola.jpg'
            fecha_creacion_constancia='2024-01-01'
        )

        Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='OTRO',
            curp='RACW050729MMCSHNA2',
            filiacion='LOPA801202DEF',
            nombre_completo='Ana López',
            categoria_plaza='Estatal',
            tipo_nombramiento='09',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Motivo de la constancia',
            firma='Director General',
            incluir_logo=False,
            logo=logo_file,  # Usar SimpleUploadedFile con el archivo 'hola.jpg'
            fecha_creacion_constancia='2024-01-02'
        )

    def test_busqueda_sin_filtros(self):
        # Prueba la vista sin aplicar filtros
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 2)

    def test_busqueda_por_nombre(self):
        # Prueba la búsqueda por nombre
        response = self.client.get(self.url, {'nombre': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 1)
        self.assertEqual(
            response.context['constancias'][0].nombre_completo, 'Juan Pérez')

    def test_busqueda_por_fecha(self):
        # Prueba la búsqueda por fecha de emisión
        response = self.client.get(self.url, {'fecha_emision': '2024-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 1)
        self.assertEqual(
            response.context['constancias'][0].nombre_completo, 'Juan Pérez')

    def test_busqueda_por_rfc(self):
        # Prueba la búsqueda por RFC
        response = self.client.get(self.url, {'rfc': 'PECJ801201ABC'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 1)
        self.assertEqual(
            response.context['constancias'][0].filiacion, 'PECJ801201ABC')

    def test_busqueda_combinada(self):
        # Prueba la búsqueda combinando varios filtros
        response = self.client.get(self.url, {
            'nombre': 'Juan',
            'fecha_emision': '2024-01-01',
            'rfc': 'PECJ801201ABC',
            'tipo_constancia': 'OTRO',
            'activa': 'true',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 1)

    def test_busqueda_sin_resultados(self):
        # Prueba búsqueda que no tiene resultados
        response = self.client.get(self.url, {'nombre': 'Inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 0)
