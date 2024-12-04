Característica: Generación de constancia
Como usuario de la SEDUZAC
necesito generar constancias
para garantizar los diferentes tramites.

        Escenario: Usuario Región genera una constancia con logo obligatorio
            Dado que inicio sesión como usuario del grupo region "usuario_Region"
            Y lleno el formulario de la constancia con "horizontal"
            Cuando presiono el botón Crear constancia
            Entonces la constancia incluye el logo institucional

            Escenario: Usuario Central genera una constancia sin logo obligatorio
            Dado que inicio sesión como usuario del grupo central "usuario_Central"
            Y lleno el formulario de la constancia con "horizontal" y sin logo
            Cuando presiono el botón Crear constancia
            Entonces la constancia no incluye el logo institucional

            Escenario: Usuario Central genera una constancia con logo
            Dado que inicio sesión como usuario del grupo central "usuario_Central"
            Y lleno el formulario de la constancia con "horizontal" y con logo
            Cuando presiono el botón Crear constancia
            Entonces la constancia incluye el logo institucional