from datetime import timedelta
class Config(object):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://thia01:thiits@localhost:3306/thi_db_1398"
    SQLALCHEMY_ECHO = False
    SESSION_USE_SIGNER = True
    SECRET_KEY = 'bhuzEoloxh0PzzK8lEokw6B7WCw42qNjOcXYyaVwn0VnKDyWmDw9sB3Je'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_NAME = "session"
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
    MAIL_DEFAULT_SENDER = '<mail_sender>'
    MAIL_SERVER = '<mail_smtp_host>'
    MAIL_PORT = '<mail_port>'
    MAIL_USERNAME = '<mail_username>'
    MAIL_PASSWORD = '<mail_password>'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = '<upload_folder>'


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://thia01:thiits@localhost:3306/thi_db_1398"
    SQLALCHEMY_DATABASE_URI = "postgresql://root:thi168168@220.130.185.36:5432/postgres"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        'pool_timeout': 900,
        'pool_size': 10,
        'max_overflow': 5,
    }
    SESSION_USE_SIGNER = True
    SECRET_KEY = 'bhuzEoloxh0PzzK8lEokw6B7WCw42qNjOcXYyaVwn0VnKDyWmDw9sB3Je'
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SESSION_COOKIE_NAME = "session1417"
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
    MAIL_DEFAULT_SENDER = '<mail_sender>'
    MAIL_SERVER = '<mail_smtp_host>'
    MAIL_PORT = '<mail_port>'
    MAIL_USERNAME = '<mail_username>'
    MAIL_PASSWORD = '<mail_password>'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = '<upload_folder>'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mssql+pymssql://thi:thi@192.168.30.24:1433/thi_db?charset=utf8"
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECRET_KEY = 'SECRET-KEY'
    SECURITY_PASSWORD_SALT = 'SECRET-KEY-PASSWORD'
    MAIL_DEFAULT_SENDER = '<mail_sender>'
    MAIL_SERVER = '<mail_smtp_host>'
    MAIL_PORT = '<mail_port>'
    MAIL_USERNAME = '<mail_username>'
    MAIL_PASSWORD = '<mail_password>'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    UPLOAD_FOLDER = '<upload_folder>'
