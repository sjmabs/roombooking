from app.main.routes import login_required
from app.rooms import bp
from app.extensions import db
from app.models.user import User
from app.models.room import Room, CreateRoom
from app.models.resource import Resource, RoomResource

from flask import (flash, g, redirect, render_template, request, session, url_for)
from werkzeug.exceptions import abort


@bp.route('/')
def index():
    rooms = Room.query.order_by(Room.name).all()
    return render_template('rooms/index.html', rooms=rooms)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    admin = User.query.filter_by(
        id=g.user.id).first()

    if admin.role != 'admin':
        abort(403)

    form = CreateRoom()
    form.resources.choices = [resource.name for resource in Resource.query.all()]

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        error = None

        if not name:
            error = 'Room name is required.'
        if not description:
            error = 'Room description is required.'

        if error is not None:
            flash(error)
            return render_template('rooms/create.html', form=form)

        else:
            new_room = Room(name=name, description=description)
            db.session.add(new_room)

            # add resources to RoomResources
            if form.resources.data:
                room = Room.query.filter_by(name=name, description=description).first()
                print(form.resources.data)
                for r in form.resources.data:
                    resource = Resource.query.filter_by(name=r).first()
                    new_room_resource = RoomResource(room_id=room.id, resource_id=resource.id)
                    db.session.add(new_room_resource)

            db.session.commit()
            flash('Room Created Successfully!')
            return redirect(url_for('rooms.index'))

    return render_template('rooms/create.html', form=form)


# need an update room route

# need a delete room route


@bp.route('/<int:id>/details', methods=('GET',))
@login_required
def details(id):
    room = Room.query.filter_by(id=id).first()
    room_resources = room.room_resources
    return render_template('rooms/details.html', room=room, room_resources=room_resources)


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    room = Room.query.filter_by(id=id).first()
    admin = User.query.filter_by(
        id=g.user.id).first()

    if admin.role != 'admin':
        abort(403)

    resources = Resource.query.all()

    # set the current resources as ticked not working but will use some sort of logic here
    current_resources = room.room_resources
    current_resources = [resource.resource.name for resource in current_resources]
    form = CreateRoom(obj=room, data={"resources": current_resources})

    form.resources.choices = resources

    # current_resources = room.room_resources
    # current_resources = [resource.resource.name for resource in current_resources]
    # form.resources.data = [r.name for r in resources if r.name in current_resources]

    if form.validate_on_submit():
        error = None

        if not form.name.data:
            error = 'Room name is required.'
        if not form.description.data:
            error = 'Room description is required.'

        if error is not None:
            flash(error)
            return render_template('rooms/update.html', form=form, room=room)

        else:
            # populate object
            room.name = form.name.data
            room.description = form.description.data

            print("new room resources: ", form.resources.data)

            # delete the RoomResources and add in the changes (if any)
            if form.resources.data:
                room.room_resources.clear()

                # add new resources
                for r in form.resources.data:
                    resource = Resource.query.filter_by(name=r).first()
                    new_room_resource = RoomResource(room_id=room.id, resource_id=resource.id)
                    db.session.add(new_room_resource)

            db.session.commit()
            print("room.resources: ", room.room_resources)

            flash('Room Updated Successfully!')
            return redirect(url_for('rooms.index'))

    return render_template('rooms/update.html', form=form, room=room)


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    room = Room.query.filter_by(id=id).first()
    admin = User.query.filter_by(
        id=g.user.id).first()

    if admin.role != 'admin':
        abort(403)

    db.session.delete(room)
    db.session.commit()
    return redirect(url_for('rooms.index'))

