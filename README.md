Apache Password Changer
-----------------------

A web Interface for users change their own passwords on a htpasswd file.

Introduction
------------

Apache Password Changer is a simple Flask project that provides resources
to users change their own passwords in a secure way.(usually this operation
needs to be done by an administrator with direct access to the server).

Requirements
------------

* Apache and gunicorn installed or similar setup.
* The htpasswd file must be exist.
* The site must be served through SSL (Security Reasons).

For more information, take a look at:

http://flask.pocoo.org/docs/deploying/wsgi-standalone/

Other ways to deploy are available as well (uwsgi, passenger and others) at the
same page.

Installation
-----------

1. Install the project through PIP (a virtualenv is highly recommended):

```
pip install htpwd
```

Configuration - Apache + Gunicorn
---------------------------------

For quick purposes, the samples included in the deploy directory can help a fast
deploy in an Apache WebServer. If you choose to do so, the following guidelines
can be applied:

 * Create a specific user and group to run the project;
 * Copy the 'htpwd.sh', htpwd.ini and 'gunicorn.py' to the home directory of
 the user created and change the working directory of the virtualenv which will
 be used.

As default, the gunicorn uses the 8000 port to answer resquests. If you need a
different port for the gunicorn process, change it in gunicorn.py module.

Bellow a full example of the changes needed:

htpwd.sh
########
```
# Activate the virtualenv and then, start gunicorn
source /data/backstage3.3/bin/activate
gunicorn -D -c gunicorn.py htpwd.htmanager:APP
```

gunicorn.py
```
import multiprocessing

#The internal port, must be the same on the Apache Proxy configuration
bind = "127.0.0.1:8000"

# The best default configuration ever
workers = multiprocessing.cpu_count() * 2 + 1
```
htpwd_httpd.conf
################

```
#A virtualhost with SSL and mod_proxy activated.
<VirtualHost *:443>
    ServerName htpwd.mydomain.com,
    SSLEngine on
    SSLCertificateFile /data/your.cert
    SSLCertificateKeyFIle /data/your.key
    ErrorLog /var/log/httpd/htpwd_errors.log
    CustomLog /var/log/httpd/htpwd_custom.log common
    ProxyPreserveHost On

<Location "/">
    ProxyPass http://127.0.0.1:5558/
    ProxyPassReverse http://127.0.0.1:5558/
    RequestHeader set X-FORWARDED-PROTOCOL ssl
    RequestHeader set X-FORWARDED-SSL on
</Location>
</VirtualHost>
```

Now it's time to copy the files into the Htpwd User home and configure it:

```
cd /yourdirectory
wget https://raw.githubusercontent.com/gcavalcante8808/htpwd/master/htpwd/deploy/gunicorn.py
wget https://raw.github.com/gcavalcante8808/htpwd/blob/master/htpwd/deploy/htpwd.sh
wget https://raw.githubusercontent.com/gcavalcante8808/htpwd/master/htpwd/deploy/htpwd.sh
```

Create the htpasswd file (apache2-utils needs to be installed):

```
htpasswd -c /data/myfile.htpasswd my@test.com
```

And install (as root) and start the gunicorn server(as the user):

```
pip install gunicorn
su htpwd
cd /data
chmod +x htpwd.sh
./htpwd.sh
```

Now you should configure your webserver.

Development
-----------

To develop using the package, you can download it through git and create a 
development symlink using the following commands:

```
git clone https://github.com/gcavalcante8808/htpwd.git
cd htpwd
python setup.py develop
```

After this, all changes made into the htpwd will be mirrored to your virtual
environment (develop makes a symlink to the current dir into the site-packages
dir of your virtualenv).

Translations
------------

TO translate the pages included in the project, you must first add a new language
in the LANGUAGE DICT using the ISO language notation(info available at
http://www.loc.gov/standards/iso639-2/php/code_list.php), like the example bellow:

LANGUAGE = {
    'en': 'English',
    'pt_BR': 'Português do Brasil',
    'es': 'Espanish'
}

As noted, the espanish language was added into the current languages suuport.

By default, the project supports English (Native in the whole project) and
Brazilian Portuguese. After add a new language, you need to init the directory
with include the gettext .po file designed for the target language (at the top
of directory):

```
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l <ISO_LANGUAGE>
```

After that, a new directory will be created insided the translations directory,
within and LC_MESSAGES directory and a messages.po file; this last file, contains
all strings that will be translated.

For easy use, we recommend the translation using the poeditor or 'Loco' available
at https://localise.biz which allow users to translate and get .po and .mo files
directly from browser.