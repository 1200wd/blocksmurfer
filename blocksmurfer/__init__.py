from flask import Flask
from flask_babel import Babel
from blocksmurfer.main import errors
from config import Config
from flask_qrcode import QRcode
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

babel = Babel()
qrcode = QRcode()


def current_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(errors.blueprint)

    # Limit request, set to slow now because we're still in development phase
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

    from blocksmurfer.main import bp as main_bp
    app.register_blueprint(main_bp)
    babel.init_app(app)
    qrcode.init_app(app)

    from blocksmurfer.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    limiter.init_app(app)

    return app
