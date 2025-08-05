# config.py

class Config:
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/login'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskdb.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'  # Cambia por tu servidor SMTP
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'cajlpj@gmail.com'  # Cambia por tu correo
    MAIL_PASSWORD = 'hkqfaeomtsoamvfd'        # Cambia por tu contraseña o app password
    MAIL_DEFAULT_SENDER = 'cajlpj@gmail.com'  # Cambia por tu correo