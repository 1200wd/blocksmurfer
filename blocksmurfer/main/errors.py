from flask import jsonify, request, render_template, Blueprint
from flask_babel import _
import logging


blueprint = Blueprint('error_handlers', __name__)
_logger = logging.getLogger(__name__)


@blueprint.app_errorhandler(Exception)
def handle_errors(e):
    if '/api/' in request.path:
        payload = {
            'error': "API request error: %s" % e.name,
            'description': e.description,
            'code': e.code,
        }
        _logger.warning("Error %d: %s (%s). Request URL: %s" % (e.code, e.name, e.description, request.path))
        return jsonify(payload)
    return render_template("error.html", title=_('Error: %s' % e.name), description=e.description, code=e.code)
