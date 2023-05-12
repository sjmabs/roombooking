import functools

from flask import (
    flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from app.main import bp
from app.extensions import db
from app.models.user import User


@bp.route('/', methods=['POST', 'GET'])
def index():
    # used for testing and adding accounts
    # print(generate_password_hash('shaun', method='sha256'))
    # print(datetime.date.today())
    # print(datetime.time())
    return render_template('index.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():

    # create a register form model
    if request.method == 'POST':
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']

        error = None

        if not firstname:
            error = "First Name is required."
        elif not lastname:
            error = "Surname is required."
        elif not email:
            error = "Email is required."
        elif not password:
            error = 'Password is required.'

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

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if session:
        return redirect('/')

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        error = None
        user = User.query.filter_by(
            email=email).first()

        if user is None or not check_password_hash(user.password, password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('bookings.index'))

        flash(error)

    return render_template('auth/login.html')


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

    if request.method == 'POST':
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

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

    return render_template('auth/account.html', user=user)
