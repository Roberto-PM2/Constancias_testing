Característica: Activar una constancia
    Como administrador del sistema
    quiero activar una constancia previamente desactivada
    para que esté disponible para los usuarios normales

    Escenario: Activar una constancia
        Dado que ingreso a la pagina como administrador "admin" y contraseña "admin123456"
        Cuando visito la página de la lista de constancias
        Y selecciono una constancia marcada como "Inactiva"
        Y elijo la opción de "Activar"
        Entonces el sistema debe cambiar el estado de la constancia a "Activa"
