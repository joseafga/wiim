"""
wiim

Wiim Industrial Information Management

:copyright: © 2018 by José Almeida.
:license: CC BY-NC 4.0, see LICENSE for more details.
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
    # initialize modules
    with app.app_context():
        api.init_app(app)

        # set favicon icon
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, 'static/images'),
                'favicon.ico',
                mimetype='image/vnd.microsoft.icon'
            )

    # import modules blueprints
    # from wiim.api.controllers import mod_api
    # register blueprints
    # app.register_blueprint(mod_api)

    return app
