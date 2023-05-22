from wtforms import PasswordField
from werkzeug.security import generate_password_hash
from flask_admin.contrib import sqla


class UserView(sqla.ModelView):
    form_excluded_columns = 'password'
    #  Form will now use all the other fields in the model

    #  Add our own password form field - call it password2
    form_extra_fields = {
        'password2': PasswordField('Password')
    }

    # set the form fields to use
    form_columns = (
        'email',
        'firstname',
        'lastname',
        'password2',
        'created',
        'role',
    )

    def on_model_change(self, form, user, is_created):
        if form.password2.data != "":
            user.password = generate_password_hash(form.password2.data)
