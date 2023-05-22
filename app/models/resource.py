from app.extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from sqlalchemy import ForeignKey


class Resource(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    room_resources = db.relationship('RoomResource', back_populates="resource", cascade='all, delete, delete-orphan')

    def __str__(self):
        return self.name


class RoomResource(db.Model):
    __tablename__ = "roomresources"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    room_id = db.Column(db.Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False)
    room = db.relationship('Room', foreign_keys=[room_id])

    resource_id = db.Column(db.Integer, ForeignKey("resources.id", ondelete="CASCADE"), nullable=False)
    resource = db.relationship('Resource', foreign_keys=[resource_id])
    quantity = db.Column(db.Integer)

    booked_resources = db.relationship('BookedResource', back_populates="room_resource",
                                       cascade='all, delete, delete-orphan')


class BookedResource(db.Model):
    __tablename__ = "bookedresources"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    booked_quantity = db.Column(db.Integer)

    room_resource_id = db.Column(db.Integer, ForeignKey("roomresources.id", ondelete="CASCADE"), nullable=False)
    room_resource = db.relationship('RoomResource', foreign_keys=[room_resource_id])

    room_booking_id = db.Column(db.Integer, ForeignKey("roombookings.id", ondelete="CASCADE"), nullable=False)
    room_booking = db.relationship('RoomBooking', foreign_keys=[room_booking_id])


class CreateResource(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
