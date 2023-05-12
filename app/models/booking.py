import datetime
from sqlalchemy import ForeignKey
from flask_wtf import FlaskForm
from wtforms import widgets, StringField, DateField, TimeField, SelectMultipleField, TextAreaField, \
    SubmitField, IntegerField, SelectField, EmailField
from wtforms.validators import DataRequired, Length, Optional
from wtforms_alchemy import QuerySelectMultipleField
from app.models.room import MultiCheckboxField, Room

from app.extensions import db
now = datetime.datetime.now()


class Booking(db.Model):
    __tablename__ = "bookings"

    #  Preliminary Events Form
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    creator_id = db.Column(db.Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    creator = db.relationship('User', foreign_keys=[creator_id])
    title = db.Column(db.String(150), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default='pending approval', nullable=False)
    event_start = db.Column(db.DateTime, nullable=False)

    time_start = db.Column(db.DateTime, nullable=False)
    time_end = db.Column(db.DateTime, nullable=False)
    created = db.Column(db.DateTime, default=now, nullable=False)

    attendees = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Booking "{self.title}">'


class CreateBookingForm(FlaskForm):
    title = StringField(u'Title', validators=[DataRequired('Please enter a Title.'), Length(max=40)])
    date = DateField(u'Date', validators=[DataRequired('Please enter a date.')], )
    time_start = TimeField(u'Start Time', validators=[DataRequired('Please enter a Start Time.')])
    time_end = TimeField(u'End Time', validators=[DataRequired('Please enter an End Time.')])
    summary = TextAreaField(u'Summary', validators=[DataRequired('Please provide a detailed event summary.')])
    attendees = IntegerField(u'Number of people attending', validators=[DataRequired('Please enter number of people.')])
    event_for = StringField(u'Who is the event for? (Students, Staff, External, Parents etc)',
                            validators=[DataRequired('Please enter who the event is for.')])
    submit = SubmitField('Submit')


