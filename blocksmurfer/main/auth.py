from config import Config
from flask import Blueprint, request, jsonify
from blocksmurfer.main.db import check_api_auth_key, update_auth_credits


auth = Blueprint('auth', __name__)


def authenticate_api_key(auth_key):
    return check_api_auth_key(auth_key)


@auth.before_app_request
def before_request():
    auth_key = request.headers.get('auth-key')
    if request.path.startswith('/api/'):
        auth_rec = authenticate_api_key(auth_key)
        if not auth_key or not auth_rec:
            return (jsonify(
                {'error': 'Unauthorized',
                 'message': 'You need an API authentication key to use the Blocksmurfer API. Please send an email to '
                            'explorer@blocksmurfer.io to apply for a key. Thanks!'}), 401)
        if Config.ENABLE_API_CREDITS_COUNTER:
            if auth_rec['credits'] < 0:
                return (jsonify(
                    {'error': 'Not Enough Credits',
                     'message': 'Not enough credits left for this account. Please send an email to '
                                'explorer@blocksmurfer.io to request more credits'}), 429)
            update_auth_credits(auth_key, auth_rec['credits'] - 1)
