import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jfuUYH7472JUjlkjqmlluiNMh18n'
    BOOTSTRAP_SERVE_LOCAL = True
    FLASK_DEBUG = True
    DEBUG = True

