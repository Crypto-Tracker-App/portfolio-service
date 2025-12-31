import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://dev_user:dev_password@localhost:5432/dev_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key')
    USER_SERVICE_URL = os.getenv('USER_SERVICE_URL', 'http://user-service:5000/current-user')
