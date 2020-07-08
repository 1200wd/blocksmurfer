from flask import jsonify, request, render_template, Blueprint
from flask_babel import _
import logging


blueprint = Blueprint('error_handlers', __name__)
_logger = logging.getLogger(__name__)


@blueprint.app_errorhandler(Exception)
def handle_errors(e):

    def getattr(object, attribute, default=''):
        try:
            return object.__getattribute__(attribute)
        except:
            try:
                return object.get(attribute, default)
            except:
                return default

    _logger.error(str(e))
    name = getattr(e, 'name')
    description = getattr(e, 'description', str(e))
    code = getattr(e, 'code', 500)

    if '/api/' in request.path:
        if code == 429:
            error_remark = "We are currently in a testing phase, so rate limits are set to low values. Please contact explorer@blocksmurfer.io if you would like to raise your limits"
        else:
            error_remark = "Please report errors and bugs to explorer@blocksmurfer.io. Thanks for your help!"
        payload = {
            'error': "API request error: %s. %s" % (name, error_remark),
            'description': description,
            'code': code,
        }
        _logger.warning("Error %d: %s (%s). Request URL: %s" % (e.code, e.name, e.description, request.path))
        resp = jsonify(payload)
        resp.status_code = code
        return resp, 500 if not code else code
    return render_template("error.html", title=('Error: %s' % name), description=description, code=code), code
