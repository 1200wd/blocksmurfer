from flask import Blueprint, request, jsonify
from blocksmurfer.main.db import check_api_auth_key


auth = Blueprint('auth', __name__)


def authenticate_api_key(auth_key):
    return check_api_auth_key(auth_key)


@auth.before_app_request
def before_request():
    auth_key = request.headers.get('auth-key')
    if request.path.startswith('/api/') and (not auth_key or not authenticate_api_key(auth_key)):
        return (jsonify(
            {'error': 'Unauthorized',
             'message': 'You need an API authentication key to use the Blocksmurfer API. Please send an email to '
                        'explorer@blocksmurfer.io to apply for a key. Thanks!'}), 401)
