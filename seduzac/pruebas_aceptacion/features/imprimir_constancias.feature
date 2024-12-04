Característica: Impresion de constancia
Como usuario de la SEDUZAC
necesito imprimir las constancias
para garantizar los satisfaccion de los tramites.

        Escenario: Usuario Región genera una constancia con logo obligatorio y la imprime
            Dado que inicio sesión como usuario region "usuario_Region"
            Y completo el formulario de la constancia con "horizontal"
            Y presiono el botón Crear constancia y se crea la constancia
            Cuando presiono el botón Imprimir
            Entonces la constancia se manda a imprimir