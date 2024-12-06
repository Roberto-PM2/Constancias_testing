Característica: Inicio de sesión
Como usuario del sistema
necesito iniciar sesión
para realizar la generacion de constancias.


        Escenario: login correcto
            Dado que ingreso mi usuario "fernando" y contraseña "dEK8kTHetu42cFh"
             Cuando presiono el botón  Iniciar sesión
             Entonces puedo ver el mensaje de "© SEDUZAC"

        Escenario: login incorrecto
            Dado que ingreso mi usuario "fernandooo" y contraseña "asdf123ss4"
             Cuando presiono el botón  Iniciar sesión
             Entonces puedo ver el mensaje de "Usuario o contraseña incorrectos."