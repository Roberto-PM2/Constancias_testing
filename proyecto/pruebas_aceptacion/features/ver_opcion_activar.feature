Característica: Ver opción "Activar constancia" como administrador
    Como administrador del sistema
    quiero ver la opción de activar constancias
    para poder activar constancias inactivas cuando sea necesario

    Escenario: Ver la opción "Activar" junto a una constancia inactiva
        Dado que ingreso como administrador "admin" y contraseña "admin123456"
        Cuando veo la página de las constancias
        Y veo las constancias inactivas
        Entonces el sistema debe mostrar la opción "Activar" junto a la constancia inactiva
