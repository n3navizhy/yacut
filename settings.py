import os
import string

LETTERS = string.ascii_lowercase + string.digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv('SECRET_KEY')
