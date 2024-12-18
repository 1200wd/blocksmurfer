import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 'de4055e624fe25f7e195f627a839c2a48f6d1ce698e5fce1c0ba97c5e4a80413-replace-with-your-key'
    if not SECRET_KEY:
        from secrets import token_hex
        SECRET_KEY = token_hex(64)  # Don't use this in production environment
        # raise ValueError("No SECRET_KEY set for Flask application")
    BOOTSTRAP_SERVE_LOCAL = True
    FLASK_DEBUG = False
    DEBUG = False
    REQUEST_LIMIT_DEFAULT = 10
    REQUEST_LIMIT_MAX = 25
    NETWORKS_ENABLED = {
        'btc': 'bitcoin',
        'ltc': 'litecoin',
        # 'doge': 'dogecoin',
        'tbtc': 'testnet',
        'tbtc4': 'testnet4',
        # 'xlt': 'litecoin_testnet',
        # 'tdoge': 'doge_testnet',
        # 'reg': 'regtest',
    }
    NETWORK_DEFAULT = 'btc'  # Has no effect yet, only works for 'btc' at the moment
    ENABLE_API = True
    API_BASE_URL = ''  # Enter full url to redirect API to another server
    ENABLE_WEBSITE = True
