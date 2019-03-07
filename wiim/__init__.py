"""
wiim

Wiim Industrial Information Management

:copyright: © 2018 by José Almeida
:license: AGPLv3/Commercial, see LICENSE file for more details
"""

__version__ = '0.0.1'

import os
from flask import Flask, send_from_directory


def create_app(config_filename):
    """ Create application and initialize modules """

    # define the WSGI application object
    app = Flask(__name__)
    app.config.from_object(config_filename)  # set configurations

    # import modules
    from wiim import api

    # initialize modules and default routes
    with app.app_context():
        # set app folders routes
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, 'static'),
                'favicon.ico', mimetype='image/vnd.microsoft.icon')

        @app.route('/uploads/<path:filename>')
        def get_uploaded_file(filename):
            return send_from_directory(app.config['WIIM_UPLOAD_FOLDER'], filename)

        # initialize API module
        api.init_app(app)

    # import modules blueprints
    # from wiim.api.controllers import mod_api
    # register blueprints
    # app.register_blueprint(mod_api)

    return app
