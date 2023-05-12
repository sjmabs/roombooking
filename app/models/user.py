from app.extensions import db
import datetime


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False)
    role = db.Column(db.String(150), default='user', nullable=False)

    bookings = db.relationship('Booking', back_populates="creator", cascade='all, delete, delete-orphan')

    def __repr__(self):
        return f'<User "{self.firstname} {self.lastname}">'

