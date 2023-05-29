from flask import Flask, redirect, Response
from flask_admin import Admin
from app.data import import_dummy_data
from app.models.admin import UserView
from app.models.user import User
from app.models.room import RoomBooking, Room
from app.models.resource import Resource, RoomResource
from werkzeug.exceptions import HTTPException
from sqlalchemy_utils import database_exists
from config import Config
from flask_admin.contrib import sqla
from flask_basicauth import BasicAuth


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    from app.extensions import db
    db.init_app(app)

    # flask basic-auth
    app.config['BASIC_AUTH_USERNAME'] = 'admin'
    app.config['BASIC_AUTH_PASSWORD'] = 'admin'

    basic_auth = BasicAuth(app)

    class ModelView(sqla.ModelView):
        def is_accessible(self):
            if not basic_auth.authenticate():
                raise AuthException('Not authenticated.')
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())

    class AuthException(HTTPException):
        def __init__(self, message):
            super().__init__(message, Response(
                "You could not be authenticated. Please refresh the page.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))

    class RoomResourceView(ModelView):
        column_hide_backrefs = False
        column_list = ('room', 'resource')

    # flask admin
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Room Booking Admin', template_mode='bootstrap3')

    # add admin views here
    admin.add_view(UserView(User, db.session))
    admin.add_view(ModelView(Room, db.session))
    admin.add_view(ModelView(Resource, db.session))
    admin.add_view(ModelView(RoomBooking, db.session))
    admin.add_view(RoomResourceView(RoomResource, db.session))
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.bookings import bp as bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/bookings')

    from app.rooms import bp as rooms_bp
    app.register_blueprint(rooms_bp, url_prefix='/rooms')

    from app.resources import bp as resources_bp
    app.register_blueprint(resources_bp, url_prefix='/resources')

    with app.app_context():
        if not database_exists(Config.SQLALCHEMY_DATABASE_URI):
            add_data = input("Would you like to input dummy data? (Y/N): ")
            db.create_all()

            if add_data.upper() == "Y":
                import_dummy_data()

    return app

