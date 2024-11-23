from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Constancia
import uuid


class ConstanicaViewTests(TestCase):
    def setUp(self):
        unique_id = uuid.uuid4().hex[:6]
        self.admin_user = User.objects.create_superuser(
            username=f'admin_{unique_id}',
            email='admin@example.com',
            password='admin123456'
        )
        self.normal_user = User.objects.create_user(
            username=f'anita_{unique_id}',
            email='anita@example.com',
            password='anita12345678'
        )
        self.constancia = Constancia.objects.create(
            nombre="Contancia Test", activo=True)
        Constancia.objects.create(nombre="Constancia Activa", activo=True)
        Constancia.objects.create(nombre="Constancia Inactiva", activo=False)
        self.client = Client()

    def tearDown(self):
        User.objects.all().delete()

    def test_acceso_para_administrador(self):
        login = self.client.login(
            username=self.admin_user.username, password='admin123456')
        self.assertTrue(login, "El usuario administrador no pudo autenticarse")
        response = self.client.get(reverse('lista_constancias'))
        self.assertContains(response, 'Acciones')

    def test_acceso_para_usuario_normal(self):
        login = self.client.login(
            username=self.normal_user.username, password='anita12345678')
        self.assertTrue(login, "El usuario no pudo autenticarse")
        response = self.client.get(reverse('lista_constancias'))
        self.assertNotContains(response, 'Acciones')

    def test_cambio_de_status_de_constancia_para_admin(self):
        login = self.client.login(
            username=self.admin_user.username, password='admin123456')
        self.assertTrue(login, "El usuario administrador no pudo autenticarse")
        self.assertTrue(self.constancia.activo)
        response = self.client.post(
            reverse('cambiar_estado', args=[self.constancia.id]), follow=True)
        self.assertEqual(response.status_code, 200,
                         f"Se esperaba 200 pero se obtuvo {response.status_code}")
        self.constancia.refresh_from_db()
        self.assertFalse(self.constancia.activo)

    def test_no_cambio_de_status_de_constancia_para_usuario_normal(self):
        unique_id = uuid.uuid4().hex[:6]
        self.client.login(
            username=f'admin_{unique_id}', password='anita12345678')
        response = self.client.post(
            reverse('cambiar_estado', args=[self.constancia.id]))
        # Verifica que no hubo cambios en el estado de la constancia
        self.constancia.refresh_from_db()
        self.assertEqual(self.constancia.activo, True)  
        self.assertNotEqual(response.status_code, 200)  

    def test_usuario_normal_no_ve_constancias_inactivas(self):
        self.client.login(username='usuario', password='testpassword')
        response = self.client.get(reverse('lista_constancias'))
        self.assertContains(response, "Constancia Activa")
        self.assertNotContains(response, "Constancia Inactiva")

    def test_usuario_super_ve_todas_las_constancias(self):
        login = self.client.login(
            username=self.admin_user.username, password='admin123456')
        self.assertTrue(login, "El usuario administrador no pudo autenticarse")
        response = self.client.get(reverse('lista_constancias'))
        self.assertContains(response, "Constancia Activa")
        self.assertContains(response, "Constancia Inactiva")

    
