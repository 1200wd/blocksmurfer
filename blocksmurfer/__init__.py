from flask import Flask
from flask_babel import Babel
from blocksmurfer.main import bp
from config import Config
from flask_qrcode import QRcode

babel = Babel()
qrcode = QRcode()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from blocksmurfer.main import bp as main_bp
    app.register_blueprint(main_bp)
    babel.init_app(app)
    qrcode.init_app(app)

    from blocksmurfer.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
