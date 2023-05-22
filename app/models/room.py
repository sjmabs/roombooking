from app.extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TimeField, TextAreaField, widgets, SelectMultipleField, SubmitField, \
    IntegerField, SelectField

from wtforms.widgets import CheckboxInput

from wtforms_alchemy import QuerySelectMultipleField

from wtforms.validators import DataRequired, Length
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref
from datetime import datetime
now = datetime.now()


class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String(150), unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)

    room_bookings = db.relationship('RoomBooking', back_populates="room", cascade='all, delete, delete-orphan')
    room_resources = db.relationship('RoomResource', back_populates="room", cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'<Room "{self.name}">'


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class RoomSelection(FlaskForm):
    choices = QuerySelectMultipleField('Rooms')


class ResourceSelection(FlaskForm):
    choices = QuerySelectMultipleField('Resources')


class CreateRoom(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    resources = MultiCheckboxField(u'Resources', validate_choice=False)


class RoomBooking(db.Model):
    __tablename__ = "roombookings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)

    creator_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default='pending approval', nullable=False)
    event_start = db.Column(db.DateTime, nullable=False)

    time_start = db.Column(db.DateTime, nullable=False)
    time_end = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, default=now, nullable=False)

    attendees = db.Column(db.Integer, nullable=False)

    booked_resources = db.relationship('BookedResource', back_populates="room_booking", cascade='all, delete, delete-orphan')

    creator = db.relationship('User', foreign_keys=[creator_id], backref=backref("user", cascade="all,delete"))
    room_id = db.Column(db.Integer, ForeignKey("rooms.id"), nullable=False)
    room = db.relationship('Room', foreign_keys=[room_id])

    def __repr__(self):
        return f'<Room Booking "{self.title}">'


class RoomBookingForm(FlaskForm):
    title = StringField(u'Title', validators=[DataRequired('Please enter a Title.'), Length(max=40)])

    event_start = DateField(u'Date', validators=[DataRequired('Please enter a date.')], )
    time_start = TimeField(u'Start Time', validators=[DataRequired('Please enter a Start Time.')])
    time_end = TimeField(u'End Time', validators=[DataRequired('Please enter an End Time.')])

    attendees = IntegerField(u'Number of people attending', validators=[DataRequired('Please enter number of people.')])
    summary = TextAreaField(u'Summary', validators=[DataRequired('Please provide a detailed event summary.')])
    resources = MultiCheckboxField(u'Resources')

    submit = SubmitField('Submit')


