from flask import Blueprint

bp = Blueprint('main', __name__)

MAX_TRANSACTIONS_REQUESTS = 25

from blocksmurfer.main import routes, errors
