import os  # Importa el módulo "os" para trabajar con variables de entorno

class Settings:
    # Configuración general
    DEBUG = True  # Activa el modo de depuración, útil para el desarrollo
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')  # Obtiene la clave secreta JWT desde una variable de entorno

    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # Obtiene la URL de la base de datos desde una variable de entorno
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactiva el seguimiento de modificaciones en SQLAlchemy
