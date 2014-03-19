from flask import Flask, render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Required, Regexp, EqualTo
from passlib.apache import HtpasswdFile
import os

#A simple App to change a htpasswd password.

# Some Usefull information come from environment. All are needed.
HTPASSWD_FILE = os.environ.get('HTPASSWD_FILE')
SECRET_KEY = os.environ.get('SECRET_KEY')
REGEXP = os.environ.get('USER_REGEXP')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
manager = Manager(app)
bootstrap = Bootstrap(app)


class HtForm(Form):
    """ Contains all form fields and validation needed """
    name = StringField('Nome de Usuário/CPF:',
                       validators=[Required(), Regexp(REGEXP)])
    passwd = PasswordField('Senha Atual:', validators=[Required()])
    newpwd = PasswordField('Nova Senha:',
                            validators=[Required(), EqualTo('newpwd2')])
    newpwd2 = PasswordField('Nova Senha(Confirmação):',
                                    validators=[Required()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
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


@app.route('/', methods=['GET', 'POST'])
def root():
    name = None
    form = HtForm()
    if form.validate_on_submit():
        name = form.name.data
        passwd = form.passwd.data
        form.name.data = ''
    return render_template('index.html', form=form, name=name)


if __name__ == '__main__':
    manager.run()