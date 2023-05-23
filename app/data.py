from app.models.user import User
from app.models.room import Room, RoomBooking
from app.models.resource import Resource, RoomResource, BookedResource
from werkzeug.security import generate_password_hash
from app.extensions import db
from datetime import datetime


# dummy data for app
def import_dummy_data():
    # create users
    new_user = User(email="j.halpert@office.com", firstname="Jim", lastname="Halpert",
                    password=generate_password_hash("pam"))

    new_user1 = User(email="d.schrute@office.com", firstname="Dwight", lastname="Schrute",
                     password=generate_password_hash("beets"))

    new_user2 = User(email="m.scott@office.com", firstname="Michael", lastname="Scott", role="admin",
                     password=generate_password_hash("manager"))

    db.session.add(new_user)
    db.session.add(new_user1)
    db.session.add(new_user2)

    # create rooms
    new_room = Room(name="Room 1", description="A small meeting room")
    new_room1 = Room(name="Room 2", description="A medium-sized meeting room")
    new_room2 = Room(name="Room 3", description="A large meeting room")

    db.session.add(new_room)
    db.session.add(new_room1)
    db.session.add(new_room2)

    # create resources

    new_resource = Resource(name="TV", description="A 55 inch TV")
    new_resource1 = Resource(name="HDMI Cable", description="A HDMI cable for connecting laptop to the screen")
    new_resource2 = Resource(name="Laptop", description="A Lenovo L13 Yoga laptop")

    db.session.add(new_resource)
    db.session.add(new_resource1)
    db.session.add(new_resource2)

    # create room resources
    for x in range(3):
        for y in range(3):
            new_room_resource = RoomResource(room_id=x+1, resource_id=y+1)
            db.session.add(new_room_resource)

    # create room bookings
    #
    new_booking = RoomBooking(creator_id=1, title="Jim's Booking", summary="Jim is booking this room",
                              event_start=datetime.strptime(str("2023-05-27"), '%Y-%m-%d'),
                              time_start=datetime.strptime(str("09:00:00"), '%H:%M:%S'),
                              time_end=datetime.strptime(str("13:00:00"), '%H:%M:%S'), attendees=2, room_id=1)

    #
    new_booking1 = RoomBooking(creator_id=2, title="Dwight's Beet Conference", summary="Dwight is booking this room for"
                               " his annual beets conference.",
                               event_start=datetime.strptime(str("2023-05-30"), '%Y-%m-%d'),
                               time_start=datetime.strptime(str("09:00:00"), '%H:%M:%S'),
                               time_end=datetime.strptime(str("17:00:00"), '%H:%M:%S'), attendees=50, room_id=2,
                               status="declined")
    #
    new_booking2 = RoomBooking(creator_id=3, title="Michael's dundees award ceremony", summary="The annual awards show",
                               event_start=datetime.strptime(str("2023-06-01"), '%Y-%m-%d'),
                               time_start=datetime.strptime(str("19:00:00"), '%H:%M:%S'),
                               time_end=datetime.strptime(str("23:00:00"), '%H:%M:%S'), attendees=30, room_id=3,
                               status="confirmed")

    db.session.add(new_booking)
    db.session.add(new_booking1)
    db.session.add(new_booking2)

    # create booked resources
    booking_resources = BookedResource(room_booking_id=1, room_resource_id=3)
    booking_resources1 = BookedResource(room_booking_id=2, room_resource_id=4)
    booking_resources2 = BookedResource(room_booking_id=2, room_resource_id=5)
    booking_resources3 = BookedResource(room_booking_id=2, room_resource_id=6)

    booking_resources4 = BookedResource(room_booking_id=3, room_resource_id=7)

    db.session.add(booking_resources)
    db.session.add(booking_resources1)
    db.session.add(booking_resources2)
    db.session.add(booking_resources3)
    db.session.add(booking_resources4)

    db.session.commit()


