# Base de Python
# Selecciona una imagen base de Python 3.10 con la etiqueta "slim"
FROM python:3.10-slim

# Crear app directorio
# Establece el directorio de trabajo dentro del contenedor en "/app"
WORKDIR /app

# Instalar app dependencias
# Copia el archivo "requirements.txt" desde el directorio local al directorio de trabajo en el contenedor
# Luego, utiliza pip para instalar las dependencias especificadas en "requirements.txt"
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Mover el código base dentro del contenedor
# Copia todos los archivos y carpetas desde el directorio local al directorio de trabajo en el contenedor
COPY . .

# Exponer el puerto 5000
# Esto permite que cualquier servicio que se ejecute en el puerto 5000 dentro del contenedor sea accesible desde fuera del contenedor
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
# Inicia la aplicación Flask en el host "0.0.0.0" y el puerto "5000"
CMD [ "flask", "run","--host","0.0.0.0","--port","5000"]
