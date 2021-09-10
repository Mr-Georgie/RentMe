"""
Production settings for heroku
"""
import environ

from config.settings.base import *

env = environ.Env()

DEBUG = env('DEBUG')

SECRET_KEY = env('SECRET_KEY') 

ALLOWED_HOSTS = []

DATABASES = {
    'default': env.db()
}

EMAIL_BACKEND ='django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True    # use port 465
EMAIL_USE_TLS = False    # use port 587
EMAIL_PORT = 465 # OR 587

# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
