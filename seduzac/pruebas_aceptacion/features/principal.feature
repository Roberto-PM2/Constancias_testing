Característica: Página principal
    Como usuario del sistema
    Deseo ver la página principal
    Para poder iniciar los procesos de constancias.

    Escenario: Pagina principal
        Dado que ingreso al sistema
        Cuando ingreso a la url "http://localhost:8000/constancias/bienvenida"
        Entonces puedo ver la página principal con el mensaje "Bienvenido"
