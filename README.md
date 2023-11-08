# MINIBLOG API

Bienvenido a la API Miniblog, una plataforma diseñada para permitir a los usuarios compartir sus pensamientos, ideas y experiencias a través de publicaciones y comentarios. Miniblog es una herramienta que facilita la creación, gestión y participación en una comunidad virtual.

## Esta aplicación te brinda la capacidad de:

- **Registrarte y Autenticarte:** Crea tu cuenta y accede de forma segura para comenzar a interactuar con la plataforma.

- **Publicar Contenido:** Comparte tus ideas y pensamientos mediante publicaciones que pueden ser vistas y comentadas por otros usuarios.

- **Interactuar con la Comunidad:** Comenta las publicaciones de otros usuarios, participa en discusiones y comparte tus opiniones.

- **Explorar Diversidad:** Descubre una amplia variedad de temas y puntos de vista de usuarios de todo el mundo.

- **Seguridad y Privacidad:** Mantenemos tus datos seguros y respetamos tu privacidad.

## Tutorial

1. Construir la aplicacion
```bash
sudo docker-compose build
```
2. Una vez que la aplicación esté construida, puedes ejecutarla con el siguiente comando:
```bash
sudo docker-compose up -d
```
3. Ejecutar la última migración (Primera vez)
Si estás ejecutando la aplicación por primera vez, debes realizar la última migración. Utiliza el siguiente comando:
```bash
sudo docker-compose run api flask db upgrade
```
## Uso de la API
Puedes acceder a la API a través de las rutas definidas en tu aplicación Flask. Asegúrate de revisar la documentación de la API para conocer las rutas disponibles y cómo interactuar con ellas.

## Requisitos
Asegúrate de tener instalados los siguientes componentes antes de ejecutar la aplicación:

[DOCKER](https://www.docker.com/)
  
## Contribuciones
Si deseas contribuir a este proyecto, puedes hacer un fork y enviar pull requests.

## Tecnologías Utilizadas
- Flask
- MySql
- Docker