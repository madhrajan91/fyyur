import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://madhavrajan:@localhost:5432/fyyur'
SQLALCHEMY_TRACK_MODIFICATIONS ='FALSE'


WTF_CSRF_METHODS = []
WTF_CSRF_ENABLED = False