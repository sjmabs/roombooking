from flask import Flask
from flask_admin import Admin
from app.models.user import User
from config import Config
from flask_admin.contrib.sqla import ModelView


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    from app.extensions import db
    db.init_app(app)

    # flask admin
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='roombooking', template_mode='bootstrap3')

    # add admin views here
    admin.add_view(ModelView(User, db.session))

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

