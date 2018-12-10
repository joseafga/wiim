class Config(object):
    DEBUG = False
    TESTING = False
    # SQLAlchemy options
    SQLALCHEMY_ECHO = False
    # define the database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wiim:wiimpass@localhost/wiim'
    # Caching type
    CACHE_TYPE = 'simple'
    # Maximum items to fetch in paginate
    WIIM_COUNT_LIMIT = 100
    # Path of icons and upload folders
    WIIM_ICONS_FOLDER = 'static/icons'
    WIIM_UPLOAD_FOLDER = 'static/upload'
    # SQLAlchemy options
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # application processor threads
    THREADS_PER_PAGE = 2
    # enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED = True
    # secret key for signing the data
    CSRF_SESSION_KEY = 'wiim_secret'
    # secret key for signing cookies
    SECRET_KEY = 'wiim_secret'

    # image configuration TODO
    # IMAGE_STORE_TYPE = 'fs'
    # IMAGE_STORE_PATH = 'app/static/images/'
    # IMAGE_STORE_BASE_URL = 'http://localhost/images/'


class ProductionConfig(Config):
    ENV = 'production'
    # Caching times in seconds
    CACHE_DEFAULT_TIMEOUT = 1


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    # SQLAlchemy options
    SQLALCHEMY_ECHO = False
    # define the database
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wiim:wiimpass@localhost/wiim_dev'
    # Caching times in seconds
    CACHE_DEFAULT_TIMEOUT = 5


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
