import os
from dotenv import load_dotenv
import binascii

key = binascii.hexlify(os.urandom(24)).decode()

load_dotenv('config.env')

DSN = os.getenv('DSN')

if DSN is None:
    print("Ошибка подключения к базе данных")
else:
    print("Токены успешно прочитаны")


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY',
                           'default_secret_key')
    SQLALCHEMY_DATABASE_URI = DSN
    SQLALCHEMY_TRACK_MODIFICATIONS = False
