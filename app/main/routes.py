import functools

from flask import (
    flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from app.main import bp
from app.extensions import db
from app.models.user import User
from app.models.auth import RegisterForm, LoginForm, AccountForm


@bp.route('/', methods=['POST', 'GET'])
def index():
    return redirect(url_for('bookings.index'))


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    # create a register form model
    if form.validate_on_submit():
        password = form.password.data
        confirm = form.confirm.data
        firstname = form.first_name.data
        lastname = form.surname.data
        email = form.email.data
        error = None

        if not firstname:
            error = "First Name is required."
        elif not lastname:
            error = "Surname is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = 'Password is required.'
        elif password != confirm:
            error = 'Passwords do not match.'

        if error is None:
            user = User.query.filter_by(
                email=email).first()  # if this returns a user, then the email already exists in database
            if user:
                error = f"Email is already in use."
                return redirect(url_for('main.register'))
            else:
                new_user = User(email=email, firstname=firstname, lastname=lastname, password=generate_password_hash(password, method='sha256'))

                # add the new user to the database
                db.session.add(new_user)
                db.session.commit()

                error = "Successfully registered"
                user = User.query.filter_by(
                    email=email).first()

                session['user_id'] = user.id
                return redirect(url_for('main.login'))

        flash(error)
        return render_template('auth/register.html', form=form)

    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    # if session:
    #     return redirect(url_for('bookings.index'))

    form = LoginForm()

    if form.validate_on_submit():
        password = form.password.data
        email = form.email.data

        error = None

        if not email:
            error = "Email is required."
        elif not password:
            error = 'Password is required.'

        user = User.query.filter_by(
            email=email).first()

        if user is None or not check_password_hash(user.password, password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            load_logged_in_user()
            return redirect(url_for('bookings.index'))

        flash(error)

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(
                id=user_id).first()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('main.login'))

        return view(**kwargs)

    return wrapped_view


@bp.route('/account', methods=('GET', 'POST'))
@login_required
def account():
    user = User.query.filter_by(
                id=g.user.id).first()

    form = AccountForm(obj=user, first_name=user.firstname, surname=user.lastname)

    if form.validate_on_submit():
        password = form.old_password.data
        firstname = form.first_name.data
        lastname = form.surname.data
        email = form.email.data
        password1 = form.password.data
        password2 = form.confirm.data

        error = None

        if not firstname:
            error = "First Name is required."
        elif not lastname:
            error = "Surname is required."
        elif not email:
            error = "Email is required."
        elif password1 and not password2 or password2 and not password1:
            error = 'New password must be entered twice.'
        elif password1 != password2:
            error = 'Passwords do not match.'

        # if this returns a user, then the email already exists in database
        if error is None:
            new_email = User.query.filter_by(
                email=email).first()

            if new_email.id != user.id:
                error = "Email is already in use."
                flash(error)
                return redirect(url_for('main.account'))

            if not check_password_hash(user.password, password):
                error = "Old password is incorrect."
                flash(error)
                return redirect(url_for('main.account'))

            else:
                user.password = generate_password_hash(password1)
                user.firstname = firstname
                user.lastname = lastname
                user.email = email

                # update the user in the database
                db.session.commit()

                error = "Successfully updated user"

            flash(error)

            return redirect(url_for('main.account'))

        flash(error)

    return render_template('auth/account.html', form=form)
