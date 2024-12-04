Característica: Buscar constancia
    Como usuario central o de región
    Quiero buscar constancias específicas mediante filtros
    Para agilizar la localización de documentos

    Escenario: Búsqueda de constancia por nombre
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso "Juan Luis" en el filtro de nombre
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra únicamente las constancias que coincidan con el nombre "Juan Luis"

    Escenario: Búsqueda de constancia por fecha de emisión
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso "04-12-2024" en el filtro de fecha de emisión
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra solo las constancias emitidas en la fecha "04-12-2024"

    Escenario: Búsqueda de constancia por RFC
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso "PALH800229XYZ" en el filtro de RFC
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra únicamente la constancia que coincide con el RFC "PALH800229XYZ"
    
    Escenario: Búsqueda por nombre "Sergio Pérez López" y fecha de emisión "04-12-2024"
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso "Sergio Pérez López" en el filtro de nombre
        Y ingreso "04-12-2024" en el filtro de fecha de emisión
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra únicamente las constancias que coincidan con el nombre "Sergio Pérez López" y fecha "04-12-2024"

    Escenario: Búsqueda por nombre "Pedro", fecha de emisión "08-01-2024" y RFC "PALH800229YYY"
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso "Pedro" en el filtro de nombre
        Y ingreso "04-12-2024" en el filtro de fecha de emisión
        Y ingreso "PALH800229YYY" en el filtro de RFC
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra únicamente la constancia que coincide con el nombre "Pedro", fecha "04-12-2024" y RFC "PALH800229YYY"

    Escenario: Búsqueda de constancia sin resultados
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso un nombre invalido "NombreInexistente" en el filtro de nombre
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra el mensaje "No se encontraron constancias que coincidan con los filtros aplicados."

    Escenario: Búsqueda con RFC inválido
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso un RFC inválido "RFC123" en el filtro de RFC
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra el mensaje de error "El RFC ingresado no es válido."

    Escenario: Limpiar formulario
        Dado que accedo a la sección de búsqueda de constancias
        Cuando ingreso "Juan Luis" en el filtro de nombre
        Y ingreso "04-12-2024" en el filtro de fecha de emisión
        Y ingreso "PALH800229XYZ" en el filtro de RFC
        Y presiono el botón de "Restablecer filtros"
        Entonces todos los campos del formulario están vacíos

    Escenario: Búsqueda por tipo de constancia
        Dado que accedo a la sección de búsqueda de constancias
        Cuando selecciono "Otro Motivo" en el filtro de tipo de constancia
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra únicamente las constancias de tipo "Otro Motivo"

    Escenario: Búsqueda por estado activo
        Dado que accedo a la sección de búsqueda de constancias
        Cuando selecciono "Activa" en el filtro de estado
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra únicamente las constancias "Activa"

    Escenario: Búsqueda por estado inactivo
        Dado que accedo a la sección de búsqueda de constancias
        Cuando selecciono "Inactiva" en el filtro de estado
        Y presiono el botón de "Buscar"
        Entonces el sistema muestra únicamente las constancias "Inactiva"

#----
