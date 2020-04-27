from flask import Flask
from flask_babel import Babel
# from flask_pure import Pure
from blocksmurfer.main import bp
from config import Config
from flask_qrcode import QRcode

babel = Babel()
qrcode = QRcode()
# pure = Pure()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from blocksmurfer.main import bp as main_bp
    app.register_blueprint(main_bp)

    babel.init_app(app)
    qrcode.init_app(app)
    # pure.init_app(app)

    return app
