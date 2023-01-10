import os
from .settings import *

DEBUG = False

# ALLOWED_HOSTS = ['*','https://admin-staging.lolab.id',
#                  'localhost', '10.101.213.97', "https://eirene.netlify.app",
#                     "https://form-perizinan.netlify.app",
#                     "https://hrds.netlify.app"]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv("DB_NAME"),
        'HOST': os.getenv("DB_HOST"),
        'USER': os.getenv("DB_USER"),
        'PASSWORD': os.getenv("DB_PASSWORD"),
        'PORT': os.getenv("DB_PORT"),
    }
}
