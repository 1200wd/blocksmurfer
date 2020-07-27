import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        from secrets import token_hex
        SECRET_KEY = token_hex(64)  # Don't use this in production environment
        # raise ValueError("No SECRET_KEY set for Flask application")
    BOOTSTRAP_SERVE_LOCAL = True
    FLASK_DEBUG = False
    DEBUG = False
    REQUEST_LIMIT_DEFAULT = 10
    REQUEST_LIMIT_MAX = 25
    NETWORKS_ENABLED = ['btc', 'ltc']   # Example: ['btc', 'ltc', 'tbtc', 'xlt'], see service.py
    NETWORK_DEFAULT = 'btc'  # Has no effect yet, only works for 'btc' at the moment
