#!/bin/env python
# coding: utf-8
import uuid
from flask import Flask, render_template, redirect, url_for, request, flash
from flask.ext.login import LoginManager, UserMixin, login_user
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.babel import Babel, lazy_gettext as _
from flask.ext.admin import Admin, BaseView, expose
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Required, Regexp, EqualTo
from passlib.apache import HtpasswdFile
from htpwd.util.base import parse_config_file

# A simple App to change a htpasswd password.

# Some Usefull information come from the ini file. This is all we need.
config = parse_config_file('htpwd.ini')

SECRET_KEY = config['HTPWD']['secret_key']
REGEXP = config['HTPWD']['regexp']
HTPASSWD_FILE = config['HTPWD']['htpasswd_file']
TARGET_PAGE = config['HTPWD']['target_page']

APP = Flask(__name__)
APP.config['SECRET_KEY'] = SECRET_KEY
APP.debug = True
MANAGER = Manager(APP)

BOOTSTRAP = Bootstrap(APP)

BABEL = Babel(APP)

admin = Admin(APP, name='Apache Password Manager')
# admin.init_app(APP)

login_manager = LoginManager()
login_manager.init_app(APP)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    """
    :param userid: the user id.
    :return: the user id.
    """
    return User.get_id(userid)


LANGUAGE = {
    'en': 'English',
    'pt_BR': 'Brazilian Portuguese',
}


#Apache Password Manager - Administrative and login Interface.


class AdminView(BaseView):
    """
    Root View of Admin Interface.
    """
    @expose('/')
    def admin_index(self):
        return self.render('admin/index.html')


#
#     # def is_accessible(self):
#     #     return login.current_user.is_authenticated()
#User Interface - Apache Password Changer.
class HtForm(Form):
    """ Contains all form fields and validation needed """
    name = StringField(_('Username'),
                       validators=[Required(), Regexp(REGEXP)])
    passwd = PasswordField(_('Current Password'), validators=[Required()])
    newpwd = PasswordField(_('New Password'),
                           validators=[Required(), EqualTo('newpwd2')])
    newpwd2 = PasswordField(_('New Password(Confirm)'),
                            validators=[Required()])
    submit = SubmitField(_('Send'))

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """Validate the needed fields."""
        rv = Form.validate(self)

        if not rv:
            return False

        ht = HtpasswdFile(HTPASSWD_FILE)
        if self.name.data in ht.users():
            if ht.check_password(self.name.data, self.passwd.data):
                ht.set_password(self.name.data, self.newpwd.data)
                ht.save()
                return True
            else:
                self.passwd.errors.append('Senha Incorreta')
                return False
        else:
            self.name.errors.append('Usuário Desconhecido')
            return False


@APP.route('/', methods=['GET', 'POST'])
def root():
    """ Index Page, presents the user form."""
    form = HtForm()
    if form.validate_on_submit():
        return redirect(url_for('changed'))
    return render_template('index.html', form=form)


@APP.route('/changed')
def changed():
    """ Congratz page!"""
    destiny = TARGET_PAGE
    return render_template('changed.html', destiny=destiny)


class User(UserMixin):
    """
    Contains all neede information to validate and authenticate a user in the
    system using the htpasswd file.
    """
    def check_user(self, username, password):
        """
        Verify if the username and password are valid and the user can be
        authenticated against the htpasswd file properly.
        :param username: the username that matches the user in the htpasswd
        file.
        :param password: the password that will be hashed and verified against
         the htpasswd file.
        :return: The user itself.
        """
        ht = HtpasswdFile(HTPASSWD_FILE)
        if username in ht.users():
            if ht.check_password(username, password):
                return self

        return False

    def get_id(self):
        """
        As we dont have id's for users in the htpasswd file, we'll return a
         uuid4 string for the purpose of authentication.
        :return:
        """
        return uuid.uuid4()


class LoginForm(Form):
    """ Login Form """
    username = StringField(_('Username'), validators=[Required(),
                                                      Regexp(REGEXP)])
    password = PasswordField(_('Password'), validators=[Required()])
    submit = SubmitField(_('Submit'))

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)


@APP.route('/login/', methods=['GET', 'POST'])
def login():
    """
    The login page, with all elements, including the form and messages for the
    users.
    :return: the root page if form is valid or the page itself if not.
    """
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        registered_user = User().check_user(username, password)
        if registered_user is False:
            flash('Username or Password Invalid', 'error')
            return redirect(url_for('login'))

        login_user(registered_user)
        flash('Logged in Sucessfully')
        return redirect(request.args.get('next') or url_for(
            'root'))

    return render_template('login.html', form=form)

@BABEL.localeselector
def get_locale():
    """ The page will be display in the browser"""
    return request.accept_languages.best_match(LANGUAGE.keys())


if __name__ == '__main__':
    MANAGER.run()
