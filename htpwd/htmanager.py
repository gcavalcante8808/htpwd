#!/bin/env python
# coding: utf-8
from flask import Flask, render_template, redirect, url_for, request
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.babel import Babel, lazy_gettext as _
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Required, Regexp, EqualTo
from passlib.apache import HtpasswdFile
from htpwd.util.base import parse_config_file

#A simple App to change a htpasswd password.

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

LANGUAGE = {
    'en': 'English',
    'pt_BR': 'Brazilian Portuguese',
}


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
    """ Index Page, presents the form."""
    form = HtForm()
    if form.validate_on_submit():
        return redirect(url_for('changed'))
    return render_template('index.html', form=form)


@APP.route('/changed')
def changed():
    """ Congratz page!"""
    destiny = TARGET_PAGE
    return render_template('changed.html', destiny=destiny)


@BABEL.localeselector
def get_locale():
    """ The page will be display in the browser"""
    return request.accept_languages.best_match(LANGUAGE.keys())


if __name__ == '__main__':
    MANAGER.run()
