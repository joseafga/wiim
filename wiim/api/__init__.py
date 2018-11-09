from .models import db, ma
from .controllers import cache, api_bp


def init_app(app):
    """ Initialize module database and blueprint """

    # initilize database and marshmallow
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)

    # initilize routes
    # init_routes(app)

    # add blueprint to app
    app.register_blueprint(api_bp)

    return app
