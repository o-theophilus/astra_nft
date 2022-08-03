from os import environ

SECRET_KEY = SECURITY_PASSWORD_SALT = environ.get("SECRET_KEY")

