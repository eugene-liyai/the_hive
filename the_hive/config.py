import os


class Config(object):
    """
    Common configurations
    """
    # email configuration
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('THE_HIVE_SQLALCHEMY')
    SECRET_KEY = os.getenv('SECRET_KEY')


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('THE_HIVE_SQLALCHEMY')
    SECRET_KEY = os.getenv('SECRET_KEY')


class TestingConfig(Config):
    """
    Testing configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('THE_HIVE_SQLALCHEMY')
    SECRET_KEY = os.getenv('SECRET_KEY')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}