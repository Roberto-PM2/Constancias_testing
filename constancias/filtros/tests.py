from datetime import date
from django.forms import ValidationError
from django.test import Client, TestCase
from .models import Constancia
from .forms import ConstanciaSearchForm


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


class ConstanciaModelTests(TestCase):
    def setUp(self):
        # Configuracion inicial
        self.constancia_data = {
            'nombre': 'Juan Pérez',
            'fecha_emision': date(2024, 1, 1),
            'rfc': 'PECJ801201ABC'
        }

    def test_crear_constancia_valida(self):
        # Prueba de crear una constancia con datos válidos
        constancia = Constancia.objects.create(**self.constancia_data)
        self.assertEqual(
            str(constancia), 'Juan Pérez - 2024-01-01 - PECJ801201ABC')

    def test_rfc_invalido(self):
        # Prueba el RFC invalido
        self.constancia_data['rfc'] = 'RFC_INVALIDO'
        with self.assertRaises(ValidationError):
            constancia = Constancia(**self.constancia_data)
            constancia.full_clean()

    def test_rfc_valido_persona_fisica(self):
        # Prueba RFC valido para una persona fisica
        self.constancia_data['rfc'] = 'PECJ801201ABC'
        constancia = Constancia(**self.constancia_data)
        constancia.full_clean()

    def test_rfc_valido_persona_moral(self):
        # Prueba RFC valido para persona moral
        self.constancia_data['rfc'] = 'AAA801201ABC'
        constancia = Constancia(**self.constancia_data)
        constancia.full_clean()

    def test_nombre_longitud_minima_model(self):
        # Prueba longitud min  del campo nombre en el modelo
        self.constancia_data['nombre'] = 'Jo'
        with self.assertRaises(ValidationError):
            constancia = Constancia(**self.constancia_data)
            constancia.full_clean()

    def test_rfc_longitud_maxima_model(self):
        # Prueba longitud max del campo rfc en el modelo
        self.constancia_data['rfc'] = 'A' * 14
        with self.assertRaises(ValidationError):
            constancia = Constancia(**self.constancia_data)
            constancia.full_clean()


class BuscarConstanciasViewTests(TestCase):
    def setUp(self):
        # Configuracion inicial
        self.client = Client()
        self.url = "http://localhost:8000/filtros/buscar_constancias/"

        Constancia.objects.create(
            nombre='Juan Pérez',
            fecha_emision=date(2024, 1, 1),
            rfc='PECJ801201ABC'
        )
        Constancia.objects.create(
            nombre='Ana López',
            fecha_emision=date(2024, 1, 2),
            rfc='LOPA801202DEF'
        )

    def test_busqueda_sin_filtros(self):
        # Prueba la vista sin aplicar filtros
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 0)

    def test_busqueda_por_nombre(self):
        # Prueba la búsqueda por nombre
        response = self.client.get(self.url, {'nombre': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 1)
        self.assertEqual(
            response.context['constancias'][0].nombre, 'Juan Pérez')

    def test_busqueda_por_fecha(self):
        # Prueba la búsqueda por fecha de emisión
        response = self.client.get(self.url, {'fecha_emision': '2024-01-01'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 1)
        self.assertEqual(
            response.context['constancias'][0].nombre, 'Juan Pérez')

    def test_busqueda_por_rfc(self):
        # Prueba la búsqueda por RFC
        response = self.client.get(self.url, {'rfc': 'PECJ801201ABC'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['filtros_aplicados'])
        self.assertEqual(len(response.context['constancias']), 1)
        self.assertEqual(
            response.context['constancias'][0].rfc, 'PECJ801201ABC')

    def test_busqueda_combinada(self):
        # Prueba la búsqueda combinando varios filtros
        response = self.client.get(self.url, {
            'nombre': 'Juan',
            'fecha_emision': '2024-01-01',
            'rfc': 'PECJ801201ABC'
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
