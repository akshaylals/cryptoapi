import os

CERTIFICATE_DIR = 'certificates'

class Config(object):
    DEBUG = True

    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')

    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://DESKTOP-4GIE4U2\SQLEXPRESS01/crypto?driver=SQL+Server+Native+Client+11.0'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 