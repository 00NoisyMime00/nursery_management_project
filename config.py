#only for local machine testing, to protect my passwords
from secret import name, password


# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  
BASE_IMG_DIR = os.path.join(BASE_DIR, 'app/static/images')
BASE_STATS_DIR = os.path.join(BASE_DIR, 'app/static/stats')

# Define the database
# CHANGE THISSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSsss
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{name}:{password}@localhost/nursery_management'.format(name = name, password = password)
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

SEND_FILE_MAX_AGE_DEFAULT = 0
