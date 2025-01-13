# -*- coding: utf-8 -*-
#
#    Blocksmurfer - Blockchain Explorer
#
#    © 2020-2021 March - 1200 Web Development
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#

import datetime
from flask import Flask, send_from_directory, request
from flask_babel import Babel
from blocksmurfer.main import errors, auth, db
from config import Config
from flask_qrcode import QRcode

babel = Babel()
qrcode = QRcode()


def current_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(errors.blueprint)

    @app.template_filter('ctime')
    def timectime(s):
        return datetime.datetime.fromtimestamp(s)

    @app.route('/robots.txt')
    @app.route('/sitemap.xml')
    def static_from_root():
        return send_from_directory(app.static_folder, request.path[1:])

    from blocksmurfer.main import bp as main_bp
    app.register_blueprint(main_bp)
    babel.init_app(app)
    qrcode.init_app(app)

    if Config.ENABLE_API and isinstance(Config.ENABLE_API, bool):
        from blocksmurfer.api import bp as api_bp
        app.register_blueprint(api_bp, url_prefix='/api/v1')
        if Config.ENABLE_API_KEY_AUTHENTICATION:
            db.init_db()
            app.register_blueprint(auth.auth)

    return app
