from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from datetime import datetime

from constancias import settings
from .models import (
    Constancia,
    ClavesConstancia,
    LicenciaConstancia,
    ContratoConstancia,
    Configuracion,
    ConstanciaAccessControl
)
from .forms import (
    ConstanciaOtroMotivoForm,
    ConstanciaPromocionVerticalForm,
    ConstanciaAdmisionForm,
    ConstanciaHorasAdicionalesForm,
    ConstanciaCambioCentroTrabajoForm,
    ConstanciaReconocimientoForm,
    ConstanciaPromocionHorizontalForm,
    ConstanciaBasificacionEstatalForm,
    ConstanciaCambioCentroTrabajoPreparatoriasForm
)
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.http import HttpResponseForbidden


class TestViews(TestCase):
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
        self.constancia = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='OTRO',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='Wendy Lizeth',
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
            fecha_creacion_constancia='2024-11-09'
        )

        self.constanciaPV_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='PROM_VERTICAL',
            curp='CAAD191003HVZBRLA3',
            filiacion='RFC123456789',
            nombre_completo='Juan PV',
            categoria_plaza='Maestro',
            tipo_nombramiento='10',
            clave_centro_trabajo='PAM2311',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Proceso de promoción',
            firma='Capital Humano Edificio Central',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )

        self.constanciaAdmision_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='ADMISION',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='juan Admision',
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
            motivo_constancia='Proceso de admision',
            firma='Director General',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )

        self.constanciaHA_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='HORAS_ADIC',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='juan HA',
            categoria_plaza='Estatal',
            tipo_nombramiento='10',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Horas adicionales',
            firma='Director General',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )

        self.constanciaCambioCT_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='CAMBIO_CENTRO',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='juan CT',
            categoria_plaza='Estatal',
            tipo_nombramiento='10',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Proceso de cambios de centro de trabajo, permutas y re-adscripción.',
            firma='Director General',
            comentarios_observaciones='hola',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )

        self.ConstanciaReconocimiento_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='RECONOCIMIENTO',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='juan Reconocimiento',
            categoria_plaza='Estatal',
            tipo_nombramiento='10',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia=(
                "Se emite constancia laboral para participar en la convocatoria publicada por la DSICAMM, "
                "en el proceso de selección de personal docente y técnico docente que se desempeñará como tutor, "
                "personal directivo escolar que se desempeñará como asesor técnico y personal docente que se "
                "desempeñará como asesor técnico pedagógico, con el propósito de comprobar antigüedad en el servicio docente."
            ),
            firma='Director General',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )

        self.ConstanciaPH_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='PROM_HORIZONTAL',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='juan Promocion Horizontal',
            categoria_plaza='Estatal',
            tipo_nombramiento='10',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Proceso horizontal',
            firma='Director General',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )

        self.ConstanciaBE_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='BASE_ESTATAL',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='juan Basificacion Estatal',
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
            motivo_constancia='Proceso de basificación de Personal de Apoyo y Asistencia a la Educación.',
            firma='Director General',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )

        self.ConstanciaCambioCTP_test = Constancia.objects.create(
            usuario=self.user,
            tipo_constancia='CAMBIO_CENTRO_PREP',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='juan Promocion Horizontal',
            categoria_plaza='Estatal',
            tipo_nombramiento='10',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='Av. Principal 123',
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Proceso de cambios de centro de trabajo en Educación Media Nivel Preparatoria',
            firma='Director General',
            comentarios_observaciones='hola',
            incluir_logo=False,
            logo=logo_file,  
            fecha_creacion_constancia='2024-11-09'
        )


    def test_lista_constancias(self):
        # Verificar que la vista de la lista de constancias funciona correctamente
        response = self.client.get(reverse('lista_constancias'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Constancia')


    def test_eliminar_constancia(self):
        # Verificar que la eliminación de una constancia funciona correctamente
        response = self.client.get(reverse('eliminar_constancia', args=[self.constancia.id]))
        self.assertRedirects(response, reverse('lista_constancias'))
        self.assertFalse(Constancia.objects.filter(id=self.constancia.id).exists())

    def test_cambiar_estado_success(self):
        """Prueba la vista cambiar estado de la constancia"""
        response = self.client.post(reverse('cambiar_estado', args=[self.constancia.id]))
        self.constancia.refresh_from_db()
        self.assertRedirects(response, reverse('lista_constancias'))
        self.assertFalse(self.constancia.Activa)  # Verifica que la constancia fue desactivada

    def test_cambiar_estado_invalid_id(self):
        """Prueba el cambio de estado con una constancia no existente"""
        response = self.client.post(reverse('cambiar_estado', args=[99999]))  # ID inexistente
        self.assertEqual(response.status_code, 404)  # Debería devolver un error 404


    def test_nueva_constancia_om_post(self):
        # Crear un archivo ficticio para el logo
        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        
        data = {
            'curp': 'RACW050729MMCSHNA2',
            'filiacion': 'RFC123456',
            'nombre_completo': 'John Doe',
            'categoria_plaza': 'Profesor',
            'tipo_nombramiento': '09',
            'clave_centro_trabajo': 'CENTRO123',
            'nombre_centro_trabajo': 'Escuela Primaria',
            'direccion': '123 Calle Principal',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '7-1103',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'motivo_constancia': 'Por motivos personales',
            'firma': 'Capital Humano',
            'claves[]': ['CLAVE1', 'CLAVE2', 'CLAVE3'],
        }

        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar el POST con los datos y el archivo
        response = self.client.post(reverse('nuevoCOM'), data, files=files)

        # Verificar que la constancia se ha creado
        self.assertTrue(Constancia.objects.filter(tipo_constancia='OTRO').exists())

        # Verificar si la instancia de Constancia fue creada y obtenerla
        try:
            constancia = Constancia.objects.get(nombre_completo='John Doe')
        except Constancia.DoesNotExist:
            self.fail("No se ha creado la constancia para 'John Doe'. Formulario válido? Errores: %s" % form.errors)

        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'OTRO')
        self.assertEqual(constancia.motivo_constancia, 'Por motivos personales')

        # Verificar si las instancias de ClavesConstancia fueron creadas
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 3)
        self.assertTrue(claves.filter(clave='CLAVE1').exists())
        self.assertTrue(claves.filter(clave='CLAVE2').exists())
        self.assertTrue(claves.filter(clave='CLAVE3').exists())

    def test_editar_constanciaOM(self):
        # Ruta del archivo 'hola.jpg' en tu carpeta 'media'
        logo_path = os.path.join(settings.MEDIA_ROOT, 'hola.jpg')

        # Verifica que el archivo existe
        self.assertTrue(os.path.exists(logo_path), "El archivo 'hola.jpg' no existe en la carpeta media")

        # Agregar el archivo en el diccionario de archivos
        files = {'logo': open(logo_path, 'rb')}

        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaOtroMotivoForm(instance=self.constancia).initial
        data['nombre_completo'] = 'Jane Doe'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']

        # Realizar la solicitud POST, asegurándote de pasar el archivo como `files`
        response = self.client.post(
            reverse('editar_constancia', args=[self.constancia.id]),
            data
        )

        # Verifica si el formulario es válido
        form = ConstanciaOtroMotivoForm(data, instance=self.constancia)
        self.assertTrue(form.is_valid(), f"Form errors: {form.errors}")  # Verifica si el formulario es válido

        # Luego, realiza la comprobación del valor
        self.constancia.refresh_from_db()
        self.assertEqual(self.constancia.nombre_completo, 'Jane Doe')
        # Cierra el archivo después de usarlo
        files['logo'].close()

#promocion vertical-----------------------------------------------------

    def test_crear_nueva_constancia_PV(self):
        # Datos de prueba para la solicitud POST
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '7-1103',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
            'licencias_adscripcion[]': ['licencia1', 'licencia2'],
            'licencias_clave_categoria[]': ['lic_cat1', 'lic_cat2'],
            'licencias_codigo[]': ['1', '2'],
            'licencias_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'licencias_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }

        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCPV'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'PROM_VERTICAL')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '10')  # Verificar valor predeterminado
        self.assertEqual(constancia.motivo_constancia, 'Proceso de promoción')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

        # Verificar licencias relacionadas con la constancia
        licencias = LicenciaConstancia.objects.filter(constancia=constancia)
        self.assertEqual(licencias.count(), 2)
        self.assertEqual(licencias[0].adscripcion, 'licencia1')
        self.assertEqual(licencias[1].adscripcion, 'licencia2')

    def test_editar_constanciaPV(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaPromocionVerticalForm(instance=self.constanciaPV_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']
        data['licencias_adscripcion[]'] = ['licencia1', 'licencia2']
        data['licencias_clave_categoria[]'] = ['lic_cat1', 'lic_cat2']
        data['licencias_codigo[]'] = ['1', '2']
        data['licencias_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['licencias_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.constanciaPV_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.constanciaPV_test.refresh_from_db()
        self.assertEqual(self.constanciaPV_test.nombre_completo, 'Jane Doe')

#admision-----------------------------------------------------

    def test_crear_nueva_constancia_Admision(self):
        # Datos de prueba para la solicitud POST
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'tipo_nombramiento': '09',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '7-1103',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }

        # Realizar una solicitud POST a la vista
        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCAdmision'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'ADMISION')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '09')  # Verificar valor predeterminado
        self.assertEqual(constancia.motivo_constancia, 'Proceso de admision')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

    def test_editar_constanciaAdmision(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaAdmisionForm(instance=self.constanciaAdmision_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']
        data['licencias_adscripcion[]'] = ['licencia1', 'licencia2']
        data['licencias_clave_categoria[]'] = ['lic_cat1', 'lic_cat2']
        data['licencias_codigo[]'] = ['1', '2']
        data['licencias_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['licencias_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.constanciaAdmision_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.constanciaAdmision_test.refresh_from_db()
        self.assertEqual(self.constanciaAdmision_test.nombre_completo, 'Jane Doe')

#horas adicionales------------------------------------
    def test_crear_nueva_Horas_Adicionales(self):
        # Datos de prueba para la solicitud POST
        self.client.login(username='testuser', password='password')
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '7-1103',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
            'licencias_adscripcion[]': ['licencia1', 'licencia2'],
            'licencias_clave_categoria[]': ['lic_cat1', 'lic_cat2'],
            'licencias_codigo[]': ['1', '2'],
            'licencias_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'licencias_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }

        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCHA'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'HORAS_ADIC')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '10')  # Verificar valor predeterminado
        self.assertEqual(constancia.motivo_constancia, 'Horas adicionales')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

        # Verificar licencias relacionadas con la constancia
        licencias = LicenciaConstancia.objects.filter(constancia=constancia)
        self.assertEqual(licencias.count(), 2)
        self.assertEqual(licencias[0].adscripcion, 'licencia1')
        self.assertEqual(licencias[1].adscripcion, 'licencia2')

    def test_editar_constanciaHA(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaHorasAdicionalesForm(instance=self.constanciaHA_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']
        data['licencias_adscripcion[]'] = ['licencia1', 'licencia2']
        data['licencias_clave_categoria[]'] = ['lic_cat1', 'lic_cat2']
        data['licencias_codigo[]'] = ['1', '2']
        data['licencias_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['licencias_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.constanciaHA_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.constanciaHA_test.refresh_from_db()
        self.assertEqual(self.constanciaHA_test.nombre_completo, 'Jane Doe')

#cambio centro-----------------------------------------------

    def test_crear_nueva_Cambio_Centro(self):
        # Datos de prueba para la solicitud POST
        self.client.login(username='testuser', password='password')
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '14-1204',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
            'licencias_adscripcion[]': ['licencia1', 'licencia2'],
            'licencias_clave_categoria[]': ['lic_cat1', 'lic_cat2'],
            'licencias_codigo[]': ['1', '2'],
            'licencias_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'licencias_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }

        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCCambioCT'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'CAMBIO_CENTRO')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '10')  # Verificar valor predeterminado
        self.assertEqual(constancia.motivo_constancia, 'Proceso de cambios de centro de trabajo, permutas y re-adscripción.')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

        # Verificar licencias relacionadas con la constancia
        licencias = LicenciaConstancia.objects.filter(constancia=constancia)
        self.assertEqual(licencias.count(), 2)
        self.assertEqual(licencias[0].adscripcion, 'licencia1')
        self.assertEqual(licencias[1].adscripcion, 'licencia2')

    def test_editar_constanciaCambioCT(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaCambioCentroTrabajoForm(instance=self.constanciaCambioCT_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['comentarios_observaciones'] = 'un comentario'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']
        data['licencias_adscripcion[]'] = ['licencia1', 'licencia2']
        data['licencias_clave_categoria[]'] = ['lic_cat1', 'lic_cat2']
        data['licencias_codigo[]'] = ['1', '2']
        data['licencias_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['licencias_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.constanciaCambioCT_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.constanciaCambioCT_test.refresh_from_db()
        self.assertEqual(self.constanciaCambioCT_test.nombre_completo, 'Jane Doe')
        self.assertEqual(self.constanciaCambioCT_test.comentarios_observaciones, 'un comentario')

#reconocimiento--------------------------------------------

    def test_crear_nueva_Reconocimiento(self):
        # Datos de prueba para la solicitud POST
        self.client.login(username='testuser', password='password')
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '14-1204',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
            'licencias_adscripcion[]': ['licencia1', 'licencia2'],
            'licencias_clave_categoria[]': ['lic_cat1', 'lic_cat2'],
            'licencias_codigo[]': ['1', '2'],
            'licencias_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'licencias_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }

        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCReconocimiento'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'RECONOCIMIENTO')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '10')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

        # Verificar licencias relacionadas con la constancia
        licencias = LicenciaConstancia.objects.filter(constancia=constancia)
        self.assertEqual(licencias.count(), 2)
        self.assertEqual(licencias[0].adscripcion, 'licencia1')
        self.assertEqual(licencias[1].adscripcion, 'licencia2')

    def test_editar_constanciaReconocimiento(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaReconocimientoForm(instance=self.ConstanciaReconocimiento_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']
        data['licencias_adscripcion[]'] = ['licencia1', 'licencia2']
        data['licencias_clave_categoria[]'] = ['lic_cat1', 'lic_cat2']
        data['licencias_codigo[]'] = ['1', '2']
        data['licencias_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['licencias_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.ConstanciaReconocimiento_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.ConstanciaReconocimiento_test.refresh_from_db()
        self.assertEqual(self.ConstanciaReconocimiento_test.nombre_completo, 'Jane Doe')

#promocion horizontal------------------------------

    def test_crear_nueva_Promoción_Horizontal(self):
        # Datos de prueba para la solicitud POST
        self.client.login(username='testuser', password='password')
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '14-1204',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
            'licencias_adscripcion[]': ['licencia1', 'licencia2'],
            'licencias_clave_categoria[]': ['lic_cat1', 'lic_cat2'],
            'licencias_codigo[]': ['1', '2'],
            'licencias_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'licencias_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }
        
        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCPH'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'PROM_HORIZONTAL')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '10')  # Verificar valor predeterminado
        self.assertEqual(constancia.motivo_constancia, 'Proceso horizontal')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

        # Verificar licencias relacionadas con la constancia
        licencias = LicenciaConstancia.objects.filter(constancia=constancia)
        self.assertEqual(licencias.count(), 2)
        self.assertEqual(licencias[0].adscripcion, 'licencia1')
        self.assertEqual(licencias[1].adscripcion, 'licencia2')

    def test_editar_constanciaPH(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaPromocionHorizontalForm(instance=self.ConstanciaPH_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']
        data['licencias_adscripcion[]'] = ['licencia1', 'licencia2']
        data['licencias_clave_categoria[]'] = ['lic_cat1', 'lic_cat2']
        data['licencias_codigo[]'] = ['1', '2']
        data['licencias_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['licencias_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.ConstanciaPH_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.ConstanciaPH_test.refresh_from_db()
        self.assertEqual(self.ConstanciaPH_test.nombre_completo, 'Jane Doe')

#basificacion estatal---------------------------

    def test_crear_nueva_Basificación_estatal(self):
        # Datos de prueba para la solicitud POST
        self.client.login(username='testuser', password='password')
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'tipo_nombramiento': '20',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '14-1204',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }

        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCBE'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'BASE_ESTATAL')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '20')  # Verificar valor predeterminado
        self.assertEqual(constancia.motivo_constancia, 'Proceso de basificación de Personal de Apoyo y Asistencia a la Educación.')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

    def test_editar_constanciaBE(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaBasificacionEstatalForm(instance=self.ConstanciaBE_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.ConstanciaBE_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.ConstanciaBE_test.refresh_from_db()
        self.assertEqual(self.ConstanciaBE_test.nombre_completo, 'Jane Doe')

#cambio centro preparatoria-------------------

    def test_crear_nueva_Cambio_Centro_preparatoria(self):
        # Datos de prueba para la solicitud POST
        self.client.login(username='testuser', password='password')
        data = {
            'curp': 'CAAD191003HVZBRLA3',
            'filiacion': 'RFC123456789',
            'nombre_completo': 'Dilan Cabrera',
            'categoria_plaza': 'Maestro',
            'clave_centro_trabajo': 'PAM2311',
            'nombre_centro_trabajo': 'Centro Escolar',
            'direccion': 'Calle Falsa 123',
            'municipio': 'Ciudad',
            'localidad': 'Localidad',
            'sueldo_mensual': '12345.67',
            'partida': '14-1204',
            'fecha_input': datetime.today().strftime('%Y-%m-%d'),
            'firma': 'Capital Humano Edificio Central',
            'claves[]': ['clave1', 'clave2'],
            'contratos_adscripcion[]': ['adscripcion1', 'adscripcion2'],
            'contratos_clave_categoria[]': ['cat1', 'cat2'],
            'contratos_codigo[]': ['1', '2'],
            'contratos_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'contratos_fecha_termino[]': ['2024-03-01', '2024-04-01'],
            'licencias_adscripcion[]': ['licencia1', 'licencia2'],
            'licencias_clave_categoria[]': ['lic_cat1', 'lic_cat2'],
            'licencias_codigo[]': ['1', '2'],
            'licencias_fecha_inicio[]': ['2024-01-01', '2024-02-01'],
            'licencias_fecha_termino[]': ['2024-03-01', '2024-04-01'],
        }

        logo_file = SimpleUploadedFile("logo.jpg", b"file_content", content_type="image/jpeg")
        files = {
            'logo': logo_file  # Nombre del campo que espera el formulario
        }

        # Realizar una solicitud POST a la vista
        response = self.client.post(reverse('nuevoCCambioCTP'), data, files=files)

        # Verificar redirección después de crear la constancia
        self.assertEqual(response.status_code, 302)

        # Verificar que la constancia fue creada y se asignaron datos correctamente
        constancia = Constancia.objects.get(nombre_completo='Dilan Cabrera')
        self.assertEqual(constancia.usuario, self.user)
        self.assertEqual(constancia.tipo_constancia, 'CAMBIO_CENTRO_PREP')
        self.assertEqual(constancia.curp, 'CAAD191003HVZBRLA3')
        self.assertEqual(constancia.tipo_nombramiento, '10')  # Verificar valor predeterminado
        self.assertEqual(constancia.motivo_constancia, 'Proceso de cambios de centro de trabajo en Educación Media Nivel Preparatoria')  # Verificar valor predeterminado

        # Verificar claves relacionadas con la constancia
        claves = ClavesConstancia.objects.filter(constancia=constancia)
        self.assertEqual(claves.count(), 2)
        self.assertEqual(claves[0].clave, 'clave1')
        self.assertEqual(claves[1].clave, 'clave2')

        # Verificar contratos relacionados con la constancia
        contratos = ContratoConstancia.objects.filter(constancia=constancia)
        self.assertEqual(contratos.count(), 2)
        self.assertEqual(contratos[0].adscripcion, 'adscripcion1')
        self.assertEqual(contratos[1].adscripcion, 'adscripcion2')

        # Verificar licencias relacionadas con la constancia
        licencias = LicenciaConstancia.objects.filter(constancia=constancia)
        self.assertEqual(licencias.count(), 2)
        self.assertEqual(licencias[0].adscripcion, 'licencia1')
        self.assertEqual(licencias[1].adscripcion, 'licencia2')

    def test_editar_constanciaCambioCTP(self):
        # Verificar que la vista de edición de constancia funciona correctamente
        data = ConstanciaCambioCentroTrabajoPreparatoriasForm(instance=self.ConstanciaCambioCTP_test).initial
        data['nombre_completo'] = 'Jane Doe'
        data['comentarios_observaciones'] = 'un comentario'
        data['claves[]'] = ['CLAVE1', 'CLAVE2', 'CLAVE3']
        data['contratos_adscripcion[]'] = ['adscripcion1', 'adscripcion2']
        data['contratos_clave_categoria[]'] = ['cat1', 'cat2']
        data['contratos_codigo[]'] = ['1', '2']
        data['contratos_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['contratos_fecha_termino[]'] = ['2024-03-01', '2024-04-01']
        data['licencias_adscripcion[]'] = ['licencia1', 'licencia2']
        data['licencias_clave_categoria[]'] = ['lic_cat1', 'lic_cat2']
        data['licencias_codigo[]'] = ['1', '2']
        data['licencias_fecha_inicio[]'] = ['2024-01-01', '2024-02-01']
        data['licencias_fecha_termino[]'] = ['2024-03-01', '2024-04-01']

        response = self.client.post(reverse('editar_constancia', args=[self.ConstanciaCambioCTP_test.id]), data)
        self.assertEqual(response.status_code, 302)
        self.ConstanciaCambioCTP_test.refresh_from_db()
        self.assertEqual(self.ConstanciaCambioCTP_test.nombre_completo, 'Jane Doe')
        self.assertEqual(self.ConstanciaCambioCTP_test.comentarios_observaciones, 'un comentario')

#otras vistas------------------------------

class CalcularDuracionTest(TestCase):
    def test_calcular_duracion_contratos(self):
        # Datos de prueba
        data = {
            'tipo': 'contratos',
            'fechas_inicio[]': ['2024-01-01', '2024-02-01'],
            'fechas_fin[]': ['2024-03-01', '2024-04-01']
        }

        # Realizar solicitud POST a la URL de cálculo de duración
        response = self.client.post(reverse('calcular_duracion'), data)

        # Verificar que la respuesta es exitosa y en formato JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Convertir respuesta JSON a un diccionario para verificación
        response_data = response.json()

        # Verificar que el tipo sea correcto
        self.assertEqual(response_data['tipo'], 'contratos')

        # Verificar los cálculos de duración
        # La primera duración es 59 días y la segunda es 59 días, total 118 días
        # 118 días = 0 años, 3 meses y 28 días

        self.assertEqual(response_data['months'], 4)

    def test_calcular_duracion_licencias(self):
        # Datos de prueba para licencias
        data = {
            'tipo': 'licencias',
            'fechas_inicio[]': ['2023-06-01', '2023-07-01'],
            'fechas_fin[]': ['2024-06-01', '2024-07-01']
        }

        # Realizar solicitud POST a la URL de cálculo de duración
        response = self.client.post(reverse('calcular_duracion'), data)

        # Verificar que la respuesta es exitosa y en formato JSON
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        # Convertir respuesta JSON a un diccionario para verificación
        response_data = response.json()

        # Verificar que el tipo sea correcto
        self.assertEqual(response_data['tipo'], 'licencias')

        # Verificar los cálculos de duración
        # La primera duración es 365 días y la segunda es 365 días, total 730 días
        # 730 días = 2 años, 0 meses y 0 días
        self.assertEqual(response_data['years'], 2)

class LogosViews(TestCase):
    def setUp(self):
        # Abrir el archivo 'hola.jpg' en modo binario y crear un SimpleUploadedFile
        logo_path = os.path.join(settings.MEDIA_ROOT, 'hola.jpg')
        with open(logo_path, 'rb') as f:
            logo_file = SimpleUploadedFile('hola.jpg', f.read(), content_type='image/jpeg')
        # Crear usuarios y grupos
        self.usuario_central = User.objects.create_user(username='central', password='1234')
        self.usuario_region = User.objects.create_user(username='region', password='1234')

        grupo_central = Group.objects.create(name="usuario_Central")
        grupo_region = Group.objects.create(name="usuario_Region")

        self.usuario_central.groups.add(grupo_central)
        self.usuario_region.groups.add(grupo_region)

        # Crear configuración inicial
        self.configuracion = Configuracion.objects.create(logo=logo_file)

        # Cliente para realizar solicitudes
        self.client = Client()

    def test_bienvenida_acceso(self):
        logo_path = os.path.join(settings.MEDIA_ROOT, 'hola.jpg')
        """La vista de bienvenida se carga correctamente."""
        response = self.client.get(reverse('bienvenida'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constancias/bienvenida.html')

    def test_iniciar_sesion(self):
        logo_path = os.path.join(settings.MEDIA_ROOT, 'hola.jpg')
        """Probar el inicio de sesión con credenciales válidas."""
        User.objects.create_user(username='fernando', password='asdf1234')
        response = self.client.post(reverse('login'), {'username': 'fernando', 'password': 'asdf1234'})
        self.assertEqual(response.status_code, 302)  # Redirección después del login

    def test_actualizar_logo_usuario_central(self):
        """El usuario del grupo `usuario_Central` puede actualizar el logo global."""
        logo_path2 = os.path.join(settings.MEDIA_ROOT, 'adios.jpg')
        with open(logo_path2, 'rb') as f:
            logo_file2 = SimpleUploadedFile('adios.jpg', f.read(), content_type='image/jpeg')
        self.client.login(username='central', password='1234')
        new_logo = SimpleUploadedFile("new_logo.png", b"logo_mock", content_type="image/png")
        response = self.client.post(reverse('configurar_logo'), {'logo': logo_file2})

        #prueba solo pasa si la carpeta de medios esta vacia de primeras
        #nconfigurar una carpeta de medios prueba que se borre automaticamente
        self.configuracion.refresh_from_db()
        self.assertEqual(self.configuracion.logo.name, "logos/adios.jpg")


    def test_bienvenida_no_logueado(self):
        logo_path = os.path.join(settings.MEDIA_ROOT, 'hola.jpg')
        """Los usuarios no logueados deben ser redirigidos al inicio de sesión."""
        response = self.client.get(reverse('crear_constancia'))
        self.assertEqual(response.status_code, 302)  # Redirección al login


class CrearConstanciaViewTests(TestCase):
    databases = {'default', 'personal'}  # Permite el acceso a 'personal'

    def setUp(self):
        # Crear datos de prueba para ConstanciaAccessControl
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = Client()
        self.client.login(username='testuser', password='12345')  # Iniciar sesión como superusuario
        ConstanciaAccessControl.objects.create(tipo_constancia='PROM_VERTICAL', habilitado=True)
        ConstanciaAccessControl.objects.create(tipo_constancia='ADMISION', habilitado=False)

    def test_crear_constancia_get(self):
        """
        Prueba que el formulario se renderiza correctamente en una solicitud GET.
        """
        response = self.client.get(reverse('crear_constancia'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'constancias/crear_constancia.html')
        self.assertIn('constancias_habilitadas', response.context)
        self.assertIn('tipos_constancia', response.context)

    def test_crear_constancia_post_valid(self):
        """
        Prueba que una solicitud POST válida redirige a la URL correcta según el tipo de constancia.
        """
        response = self.client.post(reverse('crear_constancia'), {
            'rfc': '000020860d47c',
            'claveCT': '32ABJ0001W',
            'tipo_constancia': 'PROM_VERTICAL'
        })
        self.assertRedirects(response, reverse('nuevoCPV'))

    def test_crear_constancia_post_desactivada_tipo(self):
        """
        Prueba que una solicitud POST con un tipo de constancia no habilitado no redirige.
        """
        response = self.client.post(reverse('crear_constancia'), {
            'rfc': 'XAXX010101000',
            'claveCT': 'ABC123',
            'tipo_constancia': 'ADMISION'
        })
        self.assertEqual(response.status_code, 302)

    def test_crear_constancia_post_invalid_tipo(self):
        """
        Prueba que una solicitud POST con un tipo de constancia no habilitado no redirige.
        """
        response = self.client.post(reverse('crear_constancia'), {
            'rfc': 'XAXX010101000',
            'claveCT': 'ABC123',
            'tipo_constancia': 'DESCONOCIDO'
        })
        self.assertEqual(response.status_code, 200)

    def test_crear_constancia_sesion(self):
        """
        Prueba que los datos se almacenan correctamente en la sesión.
        """
        session = self.client.session
        session['rfc'] = 'XAXX010101000'
        session['claveCT'] = 'ABC123'
        session.save()

        response = self.client.post(reverse('crear_constancia'), {
            'rfc': 'XAXX010101000',
            'claveCT': 'ABC123',
            'tipo_constancia': 'PROM_VERTICAL'
        })

        self.assertEqual(self.client.session['rfc'], 'XAXX010101000')
        self.assertEqual(self.client.session['claveCT'], 'ABC123')


class TestViewsLogin(TestCase):

    def setUp(self):
        # Crear un usuario de prueba para las vistas de inicio de sesión
        self.user = User.objects.create_user(username='testuser', password='1234')
        self.client.login(username='testuser', password='1234')
        

    def test_logout(self):
        """Prueba el inicio de sesión con credenciales válidas"""
        response = self.client.post(reverse('logout'), {'username': 'testuser', 'password': '1234'})
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_iniciar_sesion_success(self):
        """Prueba el inicio de sesión con credenciales válidas"""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': '1234'})
        self.assertRedirects(response, reverse('crear_constancia'))  # Debe redirigir a 'crear_constancia'
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_iniciar_sesion_failure(self):
        self.client.logout()
        """Prueba el inicio de sesión con credenciales incorrectas"""
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertTemplateUsed(response, 'constancias/login.html')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_registrarse_success(self):
        """Prueba el registro exitoso de un nuevo usuario"""
        response = self.client.post(reverse('registrarse'), {
            'username': 'newuser', 
            'password1': 'contraseña_kj148ds', 
            'password2': 'contraseña_kj148ds'
        })
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Verifica que el usuario fue creado
        

    def test_registrarse_failure(self):
        """Prueba el registro con datos inválidos"""
        response = self.client.post(reverse('registrarse'), {
            'username': 'newuser2', 
            'password1': 'contraseña_kj148ds', 
            'password2': 'otro'
        })
        self.assertFalse(User.objects.filter(username='newuser2').exists())  # Verifica que el usuario no fue creado
        self.assertTemplateUsed(response, 'constancias/registro.html')

