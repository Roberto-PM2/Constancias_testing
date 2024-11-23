Característica: Desactivar una constancia
    Como administrador del sistema
    quiero desactivar una constancia que esta activa
    para que no esté disponible para los usuarios normales

    Escenario: Desactivar una constancia
        Dado que ingreso al sistema como administrador "admin" y contraseña "admin123456"
        Cuando entro a la página de la lista de constancias
        Y selecciono una constancia marcada como "Activa"
        Y elijo la opción de "Desactivar"
        Entonces el sistema debe cambiar el estado de la constancia a "Inactiva"
