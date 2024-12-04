Característica: Inicio de sesión
Como usuario del sistema
necesito iniciar sesiión
para realizar la generacion de constancias.


        Escenario: login correcto
            Dado que  ingreso mi usuario "fernando" y contraseña "asdf1234"
             Cuando presiono el botón  Iniciar sesión
             Entonces puedo ver el mensaje de "SEDUZAC 2024"

        Escenario: login incorrecto
            Dado que  ingreso mi usuario "fernandooo" y contraseña "asdf1234"
             Cuando presiono el botón  Iniciar sesión
             Entonces puedo ver el mensaje de "Usuario o contraseña incorrectos."