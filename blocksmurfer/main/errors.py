from flask import jsonify, request, render_template, Blueprint
from flask_babel import _
import logging


blueprint = Blueprint('error_handlers', __name__)
_logger = logging.getLogger(__name__)


@blueprint.app_errorhandler(Exception)
def handle_errors(e):
    try:
        if '/api/' in request.path:
            payload = {
                'error': "API request error: %s" % e.name,
                'description': e.description,
                'code': e.code,
            }
            _logger.warning("Error %d: %s (%s). Request URL: %s" % (e.code, e.name, e.description, request.path))
            resp = jsonify(payload)
            resp.status_code = e.code
            return resp
        name = e.name
        description = e.description
        code = e.code
    except:
        name = e
        description = ''
        code = ''
    return render_template("error.html", title=('Error: %s' % name), description=description, code=code), code
