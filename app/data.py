from app.models.user import User
from app.models.room import Room, RoomBooking
from app.models.resource import Resource, RoomResource
from werkzeug.security import generate_password_hash
from app.extensions import db


# dummy data for app
def import_dummy_data():
    # create users
    new_user = User(email="j.halpert@office.com", firstname="Jim", lastname="Halpert",
                    password=generate_password_hash("pam", method='sha256'))

    new_user1 = User(email="d.schrute@office.com", firstname="Dwight", lastname="Schrute",
                     password=generate_password_hash("beets", method='sha256'))

    new_user2 = User(email="m.scott@office.com", firstname="Michael", lastname="Scott", role="admin",
                     password=generate_password_hash("manager", method='sha256'))

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

    db.session.commit()

# create room booking

# new_room_booking = RoomBooking(creator_id="1", title="Jim's Booking", summary="Jim is booking this room",
#                                event_start=datetime.strptime(str(2023-05-30), '%Y-%m-%d'),
#                                time_start=time_start,
#                                time_end=time_end,
#                                room_id=1,
#                                attendees=2)
#
# new_room_booking1 = RoomBooking(creator_id="2", title=title, summary=summary, event_start=event_start,
#                                            time_start=time_start, time_end=time_end, room_id=room.id,
#                                            attendees=attendees)
#
# new_room_booking2 = RoomBooking(creator_id="3", title=title, summary=summary, event_start=event_start,
#                                            time_start=time_start, time_end=time_end, room_id=room.id,
#                                            attendees=attendees)
