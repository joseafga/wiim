from .models import db, ma
from .routes import api_bp


def init_app(app):
    """ Initialize module database and blueprint """

    # initilize database and marshmallow
    db.init_app(app)
    ma.init_app(app)
    # add blueprint to app
    app.register_blueprint(api_bp)
