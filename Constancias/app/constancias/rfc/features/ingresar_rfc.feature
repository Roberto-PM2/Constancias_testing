Feature: Verificar y seleccionar constancias

  Scenario: Ingresar un RFC válido
    Given que ingreso mi RFC "ZABC123456XYZ" en el formulario
    When presiono el botón Verificar
    Then debo ser redirigido a la página de selección de constancias
    And debo ver el nombre del empleado "MARIA CARRILLO"

  Scenario: Ingresar un RFC inválido (longitud incorrecta)
    Given que ingreso mi RFC "ZABC123" en el formulario
    When presiono el botón Verificar
    Then debo ver el mensaje de error "El RFC debe tener exactamente 13 caracteres."

  Scenario: Ingresar un RFC inválido (caracteres no permitidos)
    Given que ingreso mi RFC "ZABC1234567@!" en el formulario
    When presiono el botón Verificar
    Then debo ver el mensaje de error "El RFC contiene caracteres no permitidos."

  Scenario: Ingresar un RFC que no existe
    Given que ingreso mi RFC "NONEXISTENT123" en el formulario
    When presiono el botón Verificar
    Then debo ver el mensaje de error "Empleado no encontrado."
