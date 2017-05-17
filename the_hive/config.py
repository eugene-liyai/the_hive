import os


class Config(object):
    """
    Common configurations
    """


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.environ['THE_HIVE_SQLALCHEMY_DATABASE_URI']
    SECRET_KEY = os.environ['SECRET_KEY']


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['THE_HIVE_SQLALCHEMY_DATABASE_URI']
    SECRET_KEY = os.environ['SECRET_KEY']


class TestingConfig(Config):
    """
    Testing configurations
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['THE_HIVE_TEST_SQLALCHEMY_DATABASE_URI']
    SECRET_KEY = os.environ['SECRET_KEY']


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}