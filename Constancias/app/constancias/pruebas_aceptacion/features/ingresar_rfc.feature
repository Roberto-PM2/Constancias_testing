Característica: Verificar y seleccionar constancias

  Escenario: Ingresar un RFC válido
    Dado que ingreso mi RFC "000020860d47c" en el formulario
    Cuando presiono el botón Verificar
    Entonces debo ver el nombre del empleado "Nombres 000020860d47c APP1 APP2"

  Escenario: Ingresar un RFC inválido (longitud incorrecta)
    Dado que ingreso mi RFC "ZABC123" en el formulario
    Cuando presiono el botón Verificar
    Entonces debo ver el mensaje de error "El RFC debe tener 13 caracteres."

  Escenario: Ingresar un RFC inválido (caracteres no permitidos)
    Dado que ingreso mi RFC "ZABC1234567@!" en el formulario
    Cuando presiono el botón Verificar
    Entonces debo ver el mensaje de error "El RFC no debe contener caracteres especiales."

  Escenario: Ingresar un RFC que no existe
    Dado que ingreso mi RFC "NONEXISTENT123" en el formulario
    Cuando presiono el botón Verificar
    Entonces debo ver el mensaje de error "No se encontró un empleado con el RFC ingresado."
