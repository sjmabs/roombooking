from flask import Blueprint

bp = Blueprint('rooms', __name__)

from app.rooms import routes

