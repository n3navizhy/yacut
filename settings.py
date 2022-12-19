import re
import os
import string

LETTERS = string.ascii_lowercase + string.digits
SHORT_LINK_LENGTH = 6
LINK_SAMPLE = r'^[' + re.escape(LETTERS) + r']{1,' \
              + re.escape(str(SHORT_LINK_LENGTH)) + r'}$'
MAX_LENGTH_LINK = 2048
MAX_LENGTH_CUSTOM = 16


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',
                                        default='sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.getenv('SECRET_KEY')
