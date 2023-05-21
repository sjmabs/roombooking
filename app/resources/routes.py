from app.main.routes import login_required
from app.resources import bp
from app.extensions import db
from app.models.user import User
from app.models.room import Room
from app.models.resource import Resource, RoomResource, CreateResource
from flask import (flash, g, redirect, render_template, request, session, url_for)
from werkzeug.exceptions import abort


@bp.route('/')
@login_required
def index():
    resources = Resource.query.all()
    return render_template('resources/index.html', resources=resources)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    admin = User.query.filter_by(
        id=g.user.id).first()

    if admin.role != 'admin':
        abort(403)

    form = CreateResource()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        error = None

        if not name:
            error = 'Resource name is required.'
        if not description:
            error = 'Resource description is required.'

        if error is not None:
            flash(error)

        else:
            new_resource = Resource(name=name, description=description)
            db.session.add(new_resource)
            db.session.commit()
            flash('Resource Created Successfully!')
            return redirect(url_for('resources.index'))

    return render_template('resources/create.html', form=form)


# need an update resource route
@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    resource = Resource.query.filter_by(id=id).first()

    admin = User.query.filter_by(
        id=g.user.id).first()

    if admin.role != 'admin':
        abort(403)

    form = CreateResource(obj=resource)

    if form.validate_on_submit():
        error = None

        if not form.name.data:
            error = 'Resource name is required.'
        if not form.description.data:
            error = 'Resource description is required.'

        if error is not None:
            flash(error)
            return render_template('resources/update.html', form=form, resource=resource)

        else:
            # populate object
            resource.name = form.name.data
            resource.description = form.description.data
            db.session.commit()

            flash('Resource Updated Successfully!')
            return redirect(url_for('resources.index'))

    return render_template('resources/update.html', form=form, resource=resource)

# need a delete resource route


@bp.route('/<int:id>/details', methods=('GET',))
@login_required
def details(id):
    resource = Resource.query.filter_by(id=id).first()
    return render_template('resources/details.html', resource=resource)


@bp.route('/<int:id>/delete', methods=('POST', 'GET'))
@login_required
def delete(id):
    resource = Resource.query.filter_by(id=id).first()
    admin = User.query.filter_by(
        id=g.user.id).first()

    if admin.role != 'admin':
        abort(403)

    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for('resources.index'))

