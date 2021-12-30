from os import environ 
from pathlib import Path

class Config(object):
    DEBUG = False

    SECRET_KEY = environ.get('SECRET_KEY')

    user = environ.get('DB_USER')
    password = environ.get('DB_PASS')
    host = environ.get('DB_HOST')
    database = environ.get('DB_DB')
    port = environ.get('DB_PORT')
    
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'

    UPLOAD_FOLDER =  (Path(__file__).parent / 'uploaded_files').resolve()
    ALLOWED_EXTENSIONS = {'pdf'}

    
