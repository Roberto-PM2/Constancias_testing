Característica: Agregar constancia admisión
  Como administrador del sistema
  quiero desactivar una constancia de admision
  para inhabilitarlos temporalmente

  Escenario: desactivar constancia
    Dado que ingreso mi usuario "robert" y contraseña "soyunico13" admin
    Y presiono el botón Identificarse como admin
    Y cambio el estado de constancia otro motivo a desactivada
    Cuando viajo al formulario de creacion de constancias a verificar
    Entonces ya no aparece otro motivo

  Escenario: activar constancia
    Dado que ingreso mi usuario "robert" y contraseña "soyunico13" admin
    Y presiono el botón Identificarse como admin
    Y cambio el estado de constancia otro motivo a activada
    Cuando viajo al formulario de creacion de constancias a verificar
    Entonces si me aparece otro motivo