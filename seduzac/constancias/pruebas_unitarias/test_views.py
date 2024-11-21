from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from constancias.models import Configuracion, Constancia
from django.core.files.uploadedfile import SimpleUploadedFile

class ConstanciaTestCase(TestCase):
    def setUp(self):
        # Crear usuarios y grupos
        self.usuario_central = User.objects.create_user(username='central', password='1234')
        self.usuario_region = User.objects.create_user(username='region', password='1234')

        grupo_central = Group.objects.create(name="usuario_Central")
        grupo_region = Group.objects.create(name="usuario_Region")

        self.usuario_central.groups.add(grupo_central)
        self.usuario_region.groups.add(grupo_region)

        # Crear configuración inicial
        self.configuracion = Configuracion.objects.create(logo="default_logo.png")

        # Cliente para realizar solicitudes
        self.client = Client()

    def test_bienvenida_acceso(self):
        """La vista de bienvenida se carga correctamente."""
        response = self.client.get(reverse('bienvenida'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constancias/bienvenida.html')

    def test_iniciar_sesion(self):
        """Probar el inicio de sesión con credenciales válidas."""
        User.objects.create_user(username='fernando', password='asdf1234')
        response = self.client.post(reverse('login'), {'username': 'fernando', 'password': 'asdf1234'})
        self.assertEqual(response.status_code, 302)  # Redirección después del login

    def test_crear_constancia_usuario_region_incluye_logo(self):
        """El usuario del grupo `usuario_Region` debe incluir el logo por defecto sin opción de modificar."""
        self.client.login(username='region', password='1234')
        response = self.client.post(reverse('crear_constancia'), {'nombre': 'Constancia 1'})
        constancia = Constancia.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(constancia)
        self.assertTrue(constancia.incluir_logo)
        self.assertEqual(constancia.logo.name, self.configuracion.logo.name)

    def test_crear_constancia_usuario_central_incluye_logo(self):
        """El usuario del grupo `usuario_Central` puede elegir incluir el logo."""
        self.client.login(username='central', password='1234')
        response = self.client.post(reverse('crear_constancia'), {
            'nombre': 'Constancia 2',
            'incluir_logo': True,
        })
        constancia = Constancia.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(constancia)
        self.assertTrue(constancia.incluir_logo)

    def test_crear_constancia_usuario_central_excluye_logo(self):
        """El usuario del grupo `usuario_Central` puede elegir no incluir el logo."""
        self.client.login(username='central', password='1234')
        response = self.client.post(reverse('crear_constancia'), {
            'nombre': 'Constancia 3',
            'incluir_logo': False,
        })
        constancia = Constancia.objects.last()

        self.assertEqual(response.status_code, 302)
        self.assertIsNotNone(constancia)
        self.assertFalse(constancia.incluir_logo)

    def test_actualizar_logo_usuario_central(self):
        """El usuario del grupo `usuario_Central` puede actualizar el logo global."""
        self.client.login(username='central', password='1234')
        new_logo = SimpleUploadedFile("new_logo.png", b"logo_mock", content_type="image/png")
        response = self.client.post(reverse('configurar_logo'), {'logo': new_logo})

        self.configuracion.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.configuracion.logo.name, "logos/new_logo.png")

    def test_bienvenida_no_logueado(self):
        """Los usuarios no logueados deben ser redirigidos al inicio de sesión."""
        response = self.client.get(reverse('crear_constancia'))
        self.assertEqual(response.status_code, 302)  # Redirección al login