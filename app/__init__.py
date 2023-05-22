from flask import Flask, redirect, render_template, Response
from flask_admin import Admin
from wtforms.validators import InputRequired

from app.models.user import User
from app.models.room import RoomBooking
from app.models.resource import Resource
from wtforms import PasswordField
from werkzeug.security import check_password_hash, generate_password_hash


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

    from werkzeug.exceptions import HTTPException

    class AuthException(HTTPException):
        def __init__(self, message):
            super().__init__(message, Response(
                "You could not be authenticated. Please refresh the page.", 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))

    class UserView(ModelView):
        form_excluded_columns = 'password'
        #  Form will now use all the other fields in the model

        #  Add our own password form field - call it password2
        form_extra_fields = {
            'password2': PasswordField('Password')
        }

        # set the form fields to use
        form_columns = (
            'email',
            'firstname',
            'lastname',
            'password2',
            'created',
            'role',
        )

        def on_model_change(self, form, User, is_created):
            if form.password2.data is not "":
                User.password = generate_password_hash(form.password2.data)

    # flask admin
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Room Booking Admin', template_mode='bootstrap3')

    # add admin views here
    admin.add_view(UserView(User, db.session))
    admin.add_view(ModelView(RoomBooking, db.session))

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.bookings import bp as bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/bookings')

    from app.rooms import bp as rooms_bp
    app.register_blueprint(rooms_bp, url_prefix='/rooms')

    from app.resources import bp as resources_bp
    app.register_blueprint(resources_bp, url_prefix='/resources')

    return app

