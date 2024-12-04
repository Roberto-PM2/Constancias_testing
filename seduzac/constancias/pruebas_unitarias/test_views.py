from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from constancias.models import Configuracion, Constancia
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class ConstanciaTestCase(TestCase):
    def setUp(self):
        self.usuario_central = User.objects.create_user(
            username='central', password='1234')
        self.usuario_region = User.objects.create_user(
            username='region', password='1234')

        grupo_central = Group.objects.create(name="usuario_Central")
        grupo_region = Group.objects.create(name="usuario_Region")

        self.usuario_central.groups.add(grupo_central)
        self.usuario_region.groups.add(grupo_region)
        self.configuracion = Configuracion.objects.create(
            logo="default_logo.png")
        self.client = Client()

    def test_bienvenida_acceso(self):
        response = self.client.get(reverse('bienvenida'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constancias/bienvenida.html')

    def test_registro_usuario_nuevo(self):
        response = self.client.post(reverse('registrarse'), {
            'username': 'nuevo_usuario',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        nuevo_usuario = User.objects.filter(username='nuevo_usuario').exists()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(nuevo_usuario)

    def test_redireccion_despues_del_login(self):
        self.client.login(username='central', password='1234')
        response = self.client.post(
            reverse('login'), {'username': 'central', 'password': '1234'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/constancias/crear/', response.url)

    def test_bienvenida_no_logueado(self):
        response = self.client.get(reverse('crear_constancia'))
        self.assertEqual(response.status_code, 302)

    def test_iniciar_sesion(self):
        User.objects.create_user(username='fernando', password='asdf1234')
        response = self.client.post(
            reverse('login'), {'username': 'fernando', 'password': 'asdf1234'})
        self.assertEqual(response.status_code, 302)

    def test_crear_constancia_usuario_region_incluye_logo(self):
        self.client.login(username='region', password='1234')
        response = self.client.post(reverse('crear_constancia'), {
                                    'nombre': 'Constancia 1'})
        constancia = Constancia.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(constancia)
        self.assertTrue(constancia.incluir_logo)
        self.assertEqual(constancia.logo.name, self.configuracion.logo.name)

    def test_crear_constancia_usuario_central_incluye_logo(self):
        self.client.login(username='central', password='1234')
        response = self.client.post(reverse('crear_constancia'), {
                                    'nombre': 'Constancia 2', 'incluir_logo': True, })
        constancia = Constancia.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(constancia)
        self.assertTrue(constancia.incluir_logo)

    def test_usuario_central_crea_constancia_sin_logo(self):
        self.client.login(username='central', password='1234')
        response = self.client.post(reverse('crear_constancia'), {
                                    'nombre': 'Constancia Sin Logo', 'incluir_logo': False, })
        constancia = Constancia.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(constancia)
        self.assertEqual(constancia.nombre, 'Constancia Sin Logo')
        self.assertFalse(constancia.incluir_logo)
