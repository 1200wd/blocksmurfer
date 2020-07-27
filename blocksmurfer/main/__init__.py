from flask import Blueprint

bp = Blueprint('main', __name__)


from blocksmurfer.main import routes, errors
