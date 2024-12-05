Feature: Verificar y seleccionar constancias

  Scenario: Ingresar un RFC válido
    Given que ingreso mi RFC "000020860d47c" en el formulario
    When presiono el botón Verificar
    Then debo ver el nombre del empleado "Nombres 000020860d47c APP1 APP2"

  Scenario: Ingresar un RFC inválido (longitud incorrecta)
    Given que ingreso mi RFC "ZABC123" en el formulario
    When presiono el botón Verificar
    Then debo ver el mensaje de error "El RFC debe tener 13 caracteres."

  Scenario: Ingresar un RFC inválido (caracteres no permitidos)
    Given que ingreso mi RFC "ZABC1234567@!" en el formulario
    When presiono el botón Verificar
    Then debo ver el mensaje de error "El RFC no debe contener caracteres especiales."

  Scenario: Ingresar un RFC que no existe
    Given que ingreso mi RFC "NONEXISTENT123" en el formulario
    When presiono el botón Verificar
    Then debo ver el mensaje de error "No se encontró un empleado con el RFC ingresado."