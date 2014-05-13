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
 * Copy the 'htpwd.sh' and 'gunicorn.py' to the home directory of the user
 created and change the environment variables contained in 'htpwd.sh' as per
 following:

 * HTPASSWD_FILE: The location of htpasswd file (eg: /data/app.htpasswd)

 * SECRET_KEY: Secret key that will be used within session and csrf_token.
eg: echo "SOMESTRINGHERE" | md5sum

 * REGEXP: Some verification regexp, that will be used to verify the
 user name field. Must be provided. If False, it will be defined as [A-z0-9_.]+,
 all possible matches.

 eg: ^\d{11}@ENTERPRISE$ will match Brazilian CPF appended with the
 @ENTERPRISE suffix.

 * TARGET_PAGE: The link for a page which the user can access with the new
 password. eg: https://myzabbix.enterprise.com.

If you need a diferente port for the gunicorn process, change it in gunicorn.py
module.

Bellow a full example of the changes needed:

Base subdomain: htpwd.mydomain.com
User: htpwd
Group: htpwd
Secret Key: "MYKEYAAFADFADFAF"
Regexp: \d{11}@test.com

htpwd.sh
########
```
#Define all needed environment variables
HTPASSWD_FILE=/data/myfile.htpasswd
SECRET_KEY="MYKEYAAFADFADFAF"
REGEXP="\d{11}@test.com"
TARGET_PAGE=www.google.com

# And export then
export HTPASSWD_FILE SECRET_KEY REGEXP TARGET_PAGE

# Activate the virtualenv and then, start gunicorn
source /data/backstage3.3/bin/activate
gunicorn -D -c gunicorn.py htpwd.htpwd:app
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

Development
-----------

To develop using the package, you must install the requirements as noted, define
the environment variables and then, start the development server through the command:

```
runserver -d -r
```

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