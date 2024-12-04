from django.test import TestCase
from .forms import (
    ConstanciaForm, ConstanciaOtroMotivoForm,
    ConstanciaPromocionVerticalForm, ConstanciaAdmisionForm,
    ConstanciaHorasAdicionalesForm, ConstanciaCambioCentroTrabajoForm,
    ConstanciaReconocimientoForm, ConstanciaPromocionHorizontalForm,
    ConstanciaBasificacionEstatalForm, ConstanciaCambioCentroTrabajoPreparatoriasForm
)


class ConstanciaFormTests(TestCase):
    def test_constancia_form_excludes_usuario_field(self):
        form = ConstanciaForm()
        self.assertNotIn('usuario', form.fields)


class ConstanciaOtroMotivoFormTests(TestCase):
    def test_otro_motivo_initial_and_disabled_fields(self):
        form = ConstanciaOtroMotivoForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'OTRO')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "fecha de ingreso")
        self.assertEqual(form.fields['nombre_completo'].label, "Hace constar que:")


class ConstanciaPromocionVerticalFormTests(TestCase):
    def test_promocion_vertical_initial_and_disabled_fields(self):
        form = ConstanciaPromocionVerticalForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'PROM_VERTICAL')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['categoria_plaza'].label, "Con categoria actual")
        self.assertEqual(form.fields['fecha_input'].label, "fecha de alta definitiva")


class ConstanciaAdmisionFormTests(TestCase):
    def test_admision_initial_and_disabled_fields(self):
        form = ConstanciaAdmisionForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'ADMISION')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "Fecha de contrato")
        self.assertEqual(form.fields['categoria_plaza'].label, "Con categoria actual")
        self.assertNotIn('10', [choice[0] for choice in form.fields['tipo_nombramiento'].choices])


class ConstanciaHorasAdicionalesFormTests(TestCase):
    def test_horas_adicionales_initial_and_disabled_fields(self):
        form = ConstanciaHorasAdicionalesForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'HORAS_ADIC')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "fecha de alta definitiva")
        self.assertEqual(form.fields['motivo_constancia'].initial, "Horas adicionales")
        self.assertTrue(form.fields['motivo_constancia'].disabled)


class ConstanciaCambioCentroTrabajoFormTests(TestCase):
    def test_cambio_centro_trabajo_initial_and_disabled_fields(self):
        form = ConstanciaCambioCentroTrabajoForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'CAMBIO_CENTRO')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "fecha de alta definitiva")


class ConstanciaReconocimientoFormTests(TestCase):
    def test_reconocimiento_initial_and_disabled_fields(self):
        form = ConstanciaReconocimientoForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'RECONOCIMIENTO')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "fecha de ingreso")


class ConstanciaPromocionHorizontalFormTests(TestCase):
    def test_promocion_horizontal_initial_and_disabled_fields(self):
        form = ConstanciaPromocionHorizontalForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'PROM_HORIZONTAL')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "fecha de alta definitiva")


class ConstanciaBasificacionEstatalFormTests(TestCase):
    def test_basificacion_estatal_initial_and_disabled_fields(self):
        form = ConstanciaBasificacionEstatalForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'BASE_ESTATAL')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "fecha de contrato")
        self.assertNotIn('10', [choice[0] for choice in form.fields['tipo_nombramiento'].choices])


class ConstanciaCambioCentroTrabajoPreparatoriasFormTests(TestCase):
    def test_cambio_centro_preparatorias_initial_and_disabled_fields(self):
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm()
        self.assertEqual(form.fields['tipo_constancia'].initial, 'CAMBIO_CENTRO_PREP')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['fecha_input'].label, "fecha de alta definitiva")


class FormInvalidoTests(TestCase):
    def test_constancia_form_invalid_data(self):
        form_data = {}  # Empty data
        form = ConstanciaForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre_completo', form.errors)  # Reemplaza por los campos obligatorios


    def test_constancia_otro_motivo_form_invalid_data(self):
        form_data = {
            'tipo_constancia': 'INVALID'  # Campo bloqueado
        }
        form = ConstanciaOtroMotivoForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_constancia_promocion_vertical_form_invalid_data(self):
        form_data = {
            'fecha_input': '10/11112/2020',
            'tipo_constancia': 'adsasdasd',
            'categoria_plaza': 'ads',
            'tipo_nombramiento': 'nombramiento1',
            'nombre_completo': '',
            'clave_centro_trabajo': 'asdasd' * 51
        }
        form = ConstanciaPromocionVerticalForm(data=form_data)
        self.assertFalse(form.is_valid())
        # fecha invalida
        self.assertIn('fecha_input', form.errors)
        # nombre vacio
        self.assertIn('nombre_completo', form.errors)
        # fuera de rango de caracteres
        self.assertIn('clave_centro_trabajo', form.errors)
        # tipo nombramiento inexistente
        # estos campos deben dar true al estar inicializados y desabilitados no pueden cambiarse de manera posterior
        self.assertEqual(form.fields['tipo_constancia'].initial, 'PROM_VERTICAL')
        self.assertTrue(form.fields['tipo_constancia'].disabled)
        self.assertEqual(form.fields['categoria_plaza'].label, "Con categoria actual")
        self.assertEqual(form.fields['tipo_nombramiento'].initial, '10')
        self.assertTrue(form.fields['tipo_nombramiento'].disabled)

    def test_constancia_admision_form_invalid_data(self):
        form_data = {
            'tipo_nombramiento': '10'  # Este valor debería ser filtrado por las opciones permitidas
        }
        form = ConstanciaAdmisionForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_nombramiento', form.errors)

    def test_constancia_horas_adicionales_form_invalid_data(self):
        form_data = {
            'motivo_constancia': 'Otro motivo'  # Valor bloqueado, solo puede ser 'Horas adicionales'
        }
        form = ConstanciaHorasAdicionalesForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.fields['motivo_constancia'].disabled)
        self.assertEqual(form.fields['motivo_constancia'].initial, 'Horas adicionales')

    def test_constancia_reconocimiento_form_invalid_data(self):
        form_data = {
            'motivo_constancia': 'Otro'  # Valor diferente al bloqueado
        }
        form = ConstanciaReconocimientoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.fields['motivo_constancia'].disabled)

    def test_constancia_cambio_centro_trabajo_form_invalid_data(self):
        form_data = {
            'fecha_input': ''  # Campo vacío, requiere valor
        }
        form = ConstanciaCambioCentroTrabajoForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_input', form.errors)

    def test_constancia_promocion_horizontal_form_invalid_data(self):
        form_data = {
            'categoria_plaza': ''  # Campo vacío, requiere valor
        }
        form = ConstanciaPromocionHorizontalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('categoria_plaza', form.errors)

    def test_constancia_basificacion_estatal_form_invalid_data(self):
        form_data = {
            'tipo_nombramiento': '10',  # Filtrado, debería excluir este valor
        }
        form = ConstanciaBasificacionEstatalForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('tipo_nombramiento', form.errors)

    def test_constancia_cambio_centro_trabajo_preparatorias_form_invalid_data(self):
        form_data = {
            'fecha_input': 'fecha_invalida'  # Formato de fecha inválido
        }
        form = ConstanciaCambioCentroTrabajoPreparatoriasForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fecha_input', form.errors)
