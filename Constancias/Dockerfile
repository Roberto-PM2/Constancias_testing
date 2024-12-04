FROM debian:bookworm-slim

# Actualiza e instala dependencias necesarias
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    libmariadb-dev \
    libapache2-mod-wsgi-py3 \
    pkg-config \
    gcc && \
    apt-get clean

# Configura la zona horaria
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copia el archivo de requisitos
COPY ./requirements.txt /app/

# Establece el directorio de trabajo
WORKDIR /app

# Crea y activa el entorno virtual
RUN python3 -m venv /env
ENV PATH="/env/bin:$PATH"

# Instala las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copia el resto del código de la aplicación (opcional)
COPY . /app/

# Expone el puerto para Apache
EXPOSE 8000

# Comando por defecto para Apache
CMD ["apachectl", "-D", "FOREGROUND"]