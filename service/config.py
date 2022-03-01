# -*- coding: utf-8 -*-


import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.urandom(32)
SQLALCHEMY_DATABASE_URI = 'sqlite:///phone_data.sqlite?charset=utf8'

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
PAGINATION_PAGE_SIZE = 100
PAGINATION_PAGE_ARGUMENT_NAME = 'page'
TESTING = True
#  Disable CSRF protection in the testing configuration
WTF_CSRF_ENABLED = False
JSON_AS_ASCII = False
