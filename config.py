__author__ = 'Tauren'

import os

DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_URL = os.getenv('DB_URL')
DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URI = "postgresql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_URL, DB_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False