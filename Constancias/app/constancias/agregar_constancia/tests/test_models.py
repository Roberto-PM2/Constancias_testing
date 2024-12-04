from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Constancia, ClavesConstancia, ContratoConstancia, LicenciaConstancia


class TestConstancia(TestCase):

    def setUp(self):
        # Crear un usuario para asociar a las constancias
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_tabla_constancias_vacia(self):
        self.assertEqual(0, Constancia.objects.count())

    def test_agrega_constancia(self):
        constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_creacion_constancia='2024-11-09'
        )
        self.assertEqual(1, Constancia.objects.count())

    def test_nombre_completo_de_constancia_agregada(self):
        constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_creacion_constancia='2024-11-09'
        )
        self.assertEqual(constancia.nombre_completo, 'Wendy Lizeth')

    def test_fecha_expiracion_null(self):
        constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_creacion_constancia='2024-11-09'
        )
        self.assertIsNone(constancia.fecha_expiracion)

    def test_fecha_expiracion_no_null(self):
        constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_expiracion='2025-11-09',
            fecha_creacion_constancia='2024-11-09'
        )
        self.assertEqual(constancia.fecha_expiracion, '2025-11-09')

    def test_tipo_constancia_requerido(self):
        constancia = Constancia(
            usuario=self.usuario,
            tipo_constancia='NO_EXISTE',
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
            fecha_creacion_constancia='2024-11-09'
        )
        with self.assertRaises(ValidationError):
            constancia.full_clean()

    def test_tipo_nombramiento_requerido(self):
        constancia = Constancia(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='Wendy Lizeth',
            categoria_plaza='Estatal',
            tipo_nombramiento='00',  # Valor inválido
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
            fecha_creacion_constancia='2024-11-09'
        )
        with self.assertRaises(ValidationError):
            constancia.full_clean()

    def test_valor_por_defecto_Activa(self):
        constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_creacion_constancia='2024-11-09'
        )
        self.assertTrue(constancia.Activa)

    def test_longitud_maxima_nombre_completo(self):
        constancia = Constancia(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='A' * 256,  # Excede longitud máxima de 255
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
            fecha_creacion_constancia='2024-11-09'
        )
        with self.assertRaises(ValidationError):
            constancia.full_clean()

    def test_monto_sueldo_mensual_positivo(self):
        constancia = Constancia(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            sueldo_mensual=-1000,  # Sueldo negativo
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Motivo de la constancia',
            firma='Director General',
            incluir_logo=False,
            fecha_creacion_constancia='2024-11-09'
        )
        with self.assertRaises(ValidationError):
            constancia.full_clean()

    def test_longitud_maxima_clave_centro_trabajo(self):
        constancia = Constancia(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='Wendy Lizeth',
            categoria_plaza='Estatal',
            tipo_nombramiento='09',
            clave_centro_trabajo='C' * 51,  # Excede longitud máxima de 50
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
            fecha_creacion_constancia='2024-11-09'
        )
        with self.assertRaises(ValidationError):
            constancia.full_clean()

    def test_direccion_vacia(self):
        constancia = Constancia(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
            curp='RACW050729MMCSHNA2',
            filiacion='EXT990101NI1',
            nombre_completo='Wendy Lizeth',
            categoria_plaza='Estatal',
            tipo_nombramiento='09',
            clave_centro_trabajo='CCT12345',
            nombre_centro_trabajo='Escuela Primaria',
            direccion='',  # Dirección vacía
            municipio='Zacatecas',
            localidad='Zacatecas',
            sueldo_mensual=5000.50,
            partida='7-1103',
            fecha_input='2024-11-09',
            motivo_constancia='Motivo de la constancia',
            firma='Director General',
            incluir_logo=False,
            fecha_creacion_constancia='2024-11-09'
        )
        with self.assertRaises(ValidationError):
            constancia.full_clean()


class TestClavesConstancia(TestCase):

    def setUp(self):
        # Crear un usuario y una constancia para asociar con ClavesConstancia
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_creacion_constancia='2024-11-09'
        )

    def test_tabla_claves_constancia_vacia(self):
        self.assertEqual(0, ClavesConstancia.objects.count())

    def test_agregar_clave_constancia(self):
        clave_constancia = ClavesConstancia.objects.create(
            constancia=self.constancia,
            clave='ABC123'
        )
        self.assertEqual(ClavesConstancia.objects.count(), 1)
        self.assertEqual(clave_constancia.clave, 'ABC123')
        self.assertEqual(clave_constancia.constancia, self.constancia)

    def test_asociacion_multiple_claves_a_constancia(self):
        ClavesConstancia.objects.create(constancia=self.constancia, clave='ABC123')
        ClavesConstancia.objects.create(constancia=self.constancia, clave='DEF456')
        self.assertEqual(self.constancia.claves.count(), 2)

    def test_str_method(self):
        clave_constancia = ClavesConstancia.objects.create(
            constancia=self.constancia,
            clave='ABC123'
        )
        expected_str = f"{self.constancia} - ABC123"
        self.assertEqual(str(clave_constancia), expected_str)

    def test_longitud_maxima_clave(self):
        clave_larga = 'A' * 256
        clave_constancia = ClavesConstancia(constancia=self.constancia, clave=clave_larga)
        with self.assertRaises(ValidationError):
            clave_constancia.full_clean()


class TestContratoConstancia(TestCase):

    def setUp(self):
        # Crear un usuario y una constancia para asociar con ContratoConstancia
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_creacion_constancia='2024-11-09'
        )

    def test_crear_contrato_constancia(self):
        contrato = ContratoConstancia.objects.create(
            constancia=self.constancia,
            adscripcion='CCT12345',
            clave_categoria='Categoria1',
            codigo='COD123',
            fecha_inicio='2024-01-01',
            fecha_termino='2024-12-31'
        )
        self.assertEqual(ContratoConstancia.objects.count(), 1)
        self.assertEqual(contrato.constancia, self.constancia)
        self.assertEqual(contrato.adscripcion, 'CCT12345')
        self.assertEqual(contrato.clave_categoria, 'Categoria1')
        self.assertEqual(contrato.codigo, 'COD123')

    def test_str_method_contrato_constancia(self):
        contrato = ContratoConstancia.objects.create(
            constancia=self.constancia,
            adscripcion='CCT12345',
            clave_categoria='Categoria1',
            codigo='COD123',
            fecha_inicio='2024-01-01',
            fecha_termino='2024-12-31'
        )
        expected_str = "Contrato en CCT12345 - COD123"
        self.assertEqual(str(contrato), expected_str)

    def test_longitud_maxima_adscripcion_contrato(self):
        adscripcion_larga = 'A' * 21  # Excede la longitud máxima de 20 caracteres
        contrato = ContratoConstancia(
            constancia=self.constancia,
            adscripcion=adscripcion_larga,
            clave_categoria='Categoria1',
            codigo='COD123',
            fecha_inicio='2024-01-01',
            fecha_termino='2024-12-31'
        )
        with self.assertRaises(ValidationError):
            contrato.full_clean()


class TestLicenciaConstancia(TestCase):

    def setUp(self):
        # Crear un usuario y una constancia para asociar con LicenciaConstancia
        self.usuario = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.constancia = Constancia.objects.create(
            usuario=self.usuario,
            tipo_constancia='PROM_VERTICAL',
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
            fecha_creacion_constancia='2024-11-09'
        )

    def test_crear_licencia_constancia(self):
        licencia = LicenciaConstancia.objects.create(
            constancia=self.constancia,
            adscripcion='CCT12345',
            clave_categoria='Categoria1',
            codigo='COD123',
            fecha_inicio='2024-01-01',
            fecha_termino='2024-12-31'
        )
        self.assertEqual(LicenciaConstancia.objects.count(), 1)
        self.assertEqual(licencia.constancia, self.constancia)
        self.assertEqual(licencia.adscripcion, 'CCT12345')
        self.assertEqual(licencia.clave_categoria, 'Categoria1')
        self.assertEqual(licencia.codigo, 'COD123')

    def test_str_method_licencia_constancia(self):
        licencia = LicenciaConstancia.objects.create(
            constancia=self.constancia,
            adscripcion='CCT12345',
            clave_categoria='Categoria1',
            codigo='COD123',
            fecha_inicio='2024-01-01',
            fecha_termino='2024-12-31'
        )
        expected_str = "Licencia en CCT12345 - COD123"
        self.assertEqual(str(licencia), expected_str)

    def test_longitud_maxima_adscripcion_licencia(self):
        adscripcion_larga = 'A' * 21  # Excede la longitud máxima de 20 caracteres
        licencia = LicenciaConstancia(
            constancia=self.constancia,
            adscripcion=adscripcion_larga,
            clave_categoria='Categoria1',
            codigo='COD123',
            fecha_inicio='2024-01-01',
            fecha_termino='2024-12-31'
        )
        with self.assertRaises(ValidationError):
            licencia.full_clean()
