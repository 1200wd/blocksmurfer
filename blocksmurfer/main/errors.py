from flask import jsonify, request, render_template, Blueprint
from flask_babel import _
import logging


blueprint = Blueprint('error_handlers', __name__)
_logger = logging.getLogger(__name__)


@blueprint.app_errorhandler(Exception)
def handle_errors(e):
    try:
        _logger.error(str(e))
        name = e.get('name')
        description = e.get('description', str(e))
        code = e.get('code')
        if '/api/' in request.path:
            payload = {
                'error': "API request error: %s" % name,
                'description': description,
                'code': code,
            }
            _logger.warning("Error %d: %s (%s). Request URL: %s" % (e.code, e.name, e.description, request.path))
            resp = jsonify(payload)
            resp.status_code = code
            return resp, 500 if not code else code
    except:
        name = e
        description = ''
        code = 500
    return render_template("error.html", title=('Error: %s' % name), description=description, code=code), code
