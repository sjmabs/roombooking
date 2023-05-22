from app.bookings import bp
from app.extensions import db
from app.main.routes import login_required
from flask import (flash, g, redirect, render_template, session, url_for)
from app.models.user import User
from app.models.resource import Resource, RoomResource, BookedResource
from app.models.room import Room, RoomBooking, RoomBookingForm
from werkzeug.exceptions import abort
from datetime import datetime


@bp.route('/', methods=["GET", "POST"])
@login_required
def index():

    # check if user is admin
    user_id = session.get('user_id')

    user = User.query.filter_by(
        id=user_id).first()

    # if admin return all bookings
    # change this to user.role = 'admin' once we have set up admin accounts
    if user.role == "admin":
        bookings = db.session.query(RoomBooking).order_by(
            RoomBooking.event_start
        ).order_by(
            RoomBooking.time_start
        ).all()

    # if normal user (return only their bookings)
    else:
        bookings = db.session.query(
            RoomBooking
        ).filter(
            RoomBooking.creator_id == user_id
        ).order_by(
            RoomBooking.event_start
        ).order_by(
            RoomBooking.time_start
        ).all()

    return render_template('bookings/index.html', bookings=bookings)


@bp.route('/create/<int:room_id>', methods=['GET', 'POST'])
@login_required
def create(room_id):

    form = RoomBookingForm()
    room = Room.query.filter_by(id=room_id).first()

    room_resources = [r for r in room.room_resources]
    room_resources = [resource.resource.name for resource in room_resources]
    form.resources.choices = room_resources

    if form.validate_on_submit():

        title = form.title.data
        summary = form.summary.data

        event_start = datetime.strptime(str(form.event_start.data), '%Y-%m-%d')

        time_start = datetime.strptime(str(form.time_start.data), '%H:%M:%S')
        time_end = datetime.strptime(str(form.time_end.data), '%H:%M:%S')
        attendees = form.attendees.data

        error = None

        if not title:
            error = 'Title is required.'
        if len(title) > 40:
            error = 'Title is too long.'
        if not event_start:
            error = 'Date is required.'
        if form.event_start.data < datetime.now().date():
            error = 'Date cannot be in past'
        if not summary:
            error = 'Summary is required.'
        if not time_start:
            error = 'Start Time is required.'
        if not time_end:
            error = 'End Time is required.'
        if not attendees:
            error = 'Please enter number of people expected to be attending.'

        if error is not None:
            flash(error)
            form = RoomBookingForm(date=event_start,
                                   attendees=attendees,
                                   time_start=time_start,
                                   time_end=time_end,
                                   )
            form.resources.choices = room_resources

            return render_template('bookings/create.html', form=form, room=room)

        # if no errors add the booking to the booking table
        else:
            new_room_booking = RoomBooking(creator_id=g.user.id, title=title, summary=summary, event_start=event_start,
                                           time_start=time_start, time_end=time_end, room_id=room.id,
                                           attendees=attendees)
            db.session.add(new_room_booking)

            booking = RoomBooking.query.filter_by(title=title, creator_id=g.user.id).first()

            if form.resources.data:
                # add new resources
                for r in form.resources.data:
                    # look for the resource
                    resource = Resource.query.filter_by(name=r).first()
                    # find the room_resource id
                    room_resource = RoomResource.query.filter_by(resource_id=resource.id).first()
                    new_booked_resource = BookedResource(room_resource_id=room_resource.id, room_booking_id=booking.id)
                    db.session.add(new_booked_resource)
            else:
                # clear if no data was given this time
                booking.booked_resources.clear()

            db.session.commit()

            flash('Booking Created Successfully!')
            return redirect(url_for('bookings.index'))

    return render_template('bookings/create.html', form=form, room=room)


def get_booking(id, check_author=True):
    user_id = session.get('user_id')
    booking = RoomBooking.query.filter_by(id=id).first()

    if booking is None:
        abort(404, f"Booking id {id} doesn't exist.")

    # check if admin
    admin = User.query.filter_by(
        id=user_id).first()

    # admin.role = "admin"
    # db.session.commit()

    if check_author and booking.creator_id != user_id and admin.role != "admin":
        abort(403)

    return booking


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    booking = get_booking(id)
    db.session.delete(booking)
    db.session.commit()
    return redirect(url_for('bookings.index'))


@bp.route('/<int:id>/details', methods=('GET',))
@login_required
def details(id):
    booking = get_booking(id)

    return render_template('bookings/details.html', booking=booking)


@bp.route('/<int:id>/accept', methods=('GET', 'POST',))
@login_required
def accept(id):
    booking = get_booking(id)
    admin = User.query.filter_by(
        id=session.get('user_id')).first()

    if admin.role != "admin":
        abort(403)

    return render_template('bookings/accept.html', booking=booking)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):

    booking = get_booking(id)
    # booking.booked_resources.clear()

    # set the current resources as ticked not working but will use some sort of logic here
    if booking.booked_resources:
        print(booking.booked_resources)
        current_booked_resources = booking.booked_resources
        print("booked_resources:", current_booked_resources[0].room_resource.resource.name)
        print("booked_resources:", [resource.room_resource for resource in current_booked_resources])
        current_booked_resources = [resource.room_resource.resource.name for resource in current_booked_resources]
    else:
        current_booked_resources = []
    form = RoomBookingForm(obj=booking,
                           date=booking.event_start,
                           attendees=booking.attendees,
                           time_start=booking.time_start,
                           time_end=booking.time_end,
                           data={"resources": current_booked_resources})

    # form.room.choices = ["", ] + [room.name for room in Room.query.all()]

    room_resources = [r for r in booking.room.room_resources]
    room_resources = [resource.resource.name for resource in room_resources]
    print(room_resources)
    form.resources.choices = room_resources

    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data
        event_start = datetime.strptime(str(form.event_start.data), '%Y-%m-%d')
        time_start = datetime.strptime(str(form.time_start.data), '%H:%M:%S')
        time_end = datetime.strptime(str(form.time_end.data), '%H:%M:%S')
        attendees = form.attendees.data

        error = None

        # backend validation for data entry
        if not title:
            error = 'Title is required.'
        if not event_start:
            error = 'Date is required.'
        if form.event_start.data < datetime.now().date():
            error = 'Date cannot be in past'
        if not summary:
            error = 'Summary is required.'
        if not time_start:
            error = 'Start Time is required.'
        if not time_end:
            error = 'End Time is required.'
        if not attendees:
            error = 'Please enter number of people expected to be attending.'

        if error is not None:
            flash(error)
            return render_template('bookings/update.html', form=form, booking=booking)
        else:
            booking.title = title
            booking.summary = summary
            booking.event_start = event_start
            booking.time_start = time_start
            booking.time_end = time_end
            booking.attendees = attendees
            booking.status = 'pending approval'

            # delete the BookedResources and add in the changes (if any)
            if form.resources.data:
                booking.booked_resources.clear()

                # add new resources
                for r in form.resources.data:
                    # look for the resource
                    resource = Resource.query.filter_by(name=r).first()
                    # find the room_resource id
                    room_resource = RoomResource.query.filter_by(resource_id=resource.id).first()
                    new_booked_resource = BookedResource(room_resource_id=room_resource.id, room_booking_id=booking.id)
                    db.session.add(new_booked_resource)
            else:
                # clear if no data was given this time
                booking.booked_resources.clear()

            db.session.commit()
            flash('Booking Updated Successfully!')
            return redirect(url_for('bookings.index'))
    return render_template('bookings/update.html', form=form, booking=booking)


@bp.route('/<int:id>/accepted', methods=('POST',))
@login_required
def accepted(id):

    booking = get_booking(id)
    booking.status = 'confirmed'
    db.session.commit()
    return redirect(url_for('bookings.index'))


@bp.route('/<int:id>/decline', methods=('POST',))
@login_required
def declined(id):
    booking = get_booking(id)
    booking.status = 'declined'
    db.session.commit()
    return redirect(url_for('bookings.index'))


@bp.route('/<int:id>/cancelled', methods=('POST',))
@login_required
def cancelled(id):
    booking = get_booking(id)
    booking.status = 'cancelled'
    db.session.commit()
    return redirect(url_for('bookings.index'))
