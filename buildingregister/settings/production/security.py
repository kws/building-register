import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_AGE = 86400 * 365  # 365 days in seconds

ALLOWED_HOSTS = []
