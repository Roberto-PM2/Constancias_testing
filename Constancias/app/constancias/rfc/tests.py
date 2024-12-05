from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class ViewsTestCase(TestCase):
    databases = {'default', 'personal'}

    def setUp(self):
        """Configura los datos iniciales para las pruebas."""
        self.client = Client()
        self.valid_rfc = "000020860d47c"
        self.invalid_rfc = "INVALIDO1234!!"
        self.ingresar_rfc_url = reverse('ingresar_rfc')
        self.ver_constancia_url = reverse('ver_constancia', args=['tipo10'])
        # Configurar datos de sesión
        session = self.client.session
        session['rfc'] = '000020860d47c'  # RFC de ejemplo
        session['claveCT'] = '32ABJ0001W'  # Clave de centro de trabajo de ejemplo
        session.save()  # Guarda los cambios en la sesión

    def test_rfc_valido(self):
        """
        Prueba que una solicitud POST válida redirige 
        """
        response = self.client.post(reverse('ingresar_rfc'), {
            'rfc': '000020860d47c',
        })
        self.assertEqual(response.status_code, 200)

    def test_rfc_valido_get(self):
        """
        Prueba que una solicitud POST válida redirige 
        """
        response = self.client.get(reverse('ingresar_rfc'), {
            'rfc': '000020860d47c',
        })
        self.assertEqual(response.status_code, 200)

    def test_rfc_invalido(self):
        """
        Prueba que un RFC inválido no sea aceptado y se muestre un error en la misma página.
        """
        response = self.client.post(self.ingresar_rfc_url, {
            'rfc': '000020860dxxx',
        })
        self.assertEqual(response.status_code, 200)  # Verifica que no redirija, sino que cargue la misma página

    def test_rfc_invalido_limite_caracteres(self):
        """
        Prueba que un RFC con demasiados caracteres no sea aceptado.
        """
        response = self.client.post(self.ingresar_rfc_url, {
            'rfc': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El RFC debe tener 13 caracteres.")

    def test_rfc_invalido_caracter_especial(self):
        """
        Prueba que un RFC con caracteres especiales no sea aceptado.
        """
        response = self.client.post(self.ingresar_rfc_url, {
            'rfc': 'aaaa?+/(33|',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El RFC no debe contener caracteres especiales.")


class VerConstanciaTestCase(TestCase):
    databases = {'default', 'personal'}  # Usa la base de datos 'personal' en modo consulta

    def setUp(self):
        """Configura los datos iniciales para las pruebas."""
        self.client = Client()
        self.tipo_valido = "tipo10"
        self.ver_constancia_url = reverse('ver_constancia', args=[self.tipo_valido])

    def test_constancia_rfc_existente(self):
        """Prueba que se renderice la constancia cuando el RFC existe."""
        response = self.client.get(self.ver_constancia_url, {'rfc': '00004f491cad9'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constancia_tipo10.html')

    def test_constancia_rfc_inexistente(self):
        response = self.client.get(self.ver_constancia_url, {'rfc': '00004f4'})
        self.assertEqual(response.status_code, 200)
