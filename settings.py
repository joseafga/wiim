# what environment the app is running in
ENV = 'development'

# statement for enabling the development environment
DEBUG = True

# SQLAlchemy options
SQLALCHEMY_ECHO = False
# SQLALCHEMY_TRACK_MODIFICATIONS = True
# define the database
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://wiim:wiimpass@localhost/wiim'

# JSON options
JSONIFY_PRETTYPRINT_REGULAR = False

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
