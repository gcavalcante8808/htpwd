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

* Apache with mod_wsgi installed or similar setup.
* The htpasswd must be exist.

For more information, take a look at:

http://flask.pocoo.org/docs/deploying/mod_wsgi/

Other ways to deploy are available as well (gunicorn, uwsgi and others) at the
same page.

Installation
-----------

1. Clone the project to your computer:

` git clone https://github.com/gcavalcante8808/htpwd `

2. Install the project's dependencies:

` cd htpwd`

`pip install -r requirements.txt `

Configuration
-------------

For quick purposes, the 'htpwd_httpd.conf' file can be used for a fast deploy in
an Apache WebServer. If you choose to do so, the following guidelines can be
applied:

 * Create a specific user and group to run the project;
 * Configure the final path of the project inside the file 'htpwd_wsgi.py';
 * Copy the 'htpwd_httpd.conf' inside the deploy directory to your sites-enabled
 or similar directory;
 * Change the needed configurations inside the file; pay some special attention
 for the path to your application and the user and group used to create the
 instances.

 If some of the information provided here is wrong, the apache server will
  refuse to start or restart(if started).

In any case, you need to define the following environment
variables as follows:

 * HTPASSWD_FILE: The location of htpasswd file (eg: /data/app.htpasswd)

 * SECRET_KEY: Secred key that will be used within session and csrf_token.
eg: echo "SOMESTRINGHERE" | md5sum

 * REGEXP: Some verification regexp, that will be used to verify the
 user name field. Must be provided. If unsure, define it as [A-z0-9_.]+ for
 all possible matches.

 eg: ^\d{11}@ENTERPRISE$ will match Brazilian CPF appended with the
 @ENTERPRISE suffix.

 * TARGET_PAGE: The link for a page which the user can access with the new
 password. eg: https://myzabbix.enterprise.com.

Bellow a full example of the changes needed:

Base dir: /var/www/html/htpwd

Base subdomain: htpwd.mydomain.com

User: htpwd

Group: htpwd

Secret Key: "MYKEYAAFADFADFAF"

Regexp: \d{11}@test.com

htpwd_wsgi.py
#############
```
import sys

sys.path.insert(0, '/var/www/html/htpwd')

from htpwd import app as application
```
htpwd_httpd.conf
################

```
<VirtualHost *>
    ServerName htpwd.domain.com
    SetEnv HTPASSWD_FILE /data/myfile.htpasswd
    SetEnv SECRET_KEY MYKEYAAFADFADFAF
    SetEnv REGEXP ^\d{11}@test.com
    SetEnv TARGET_PAGE www.google.com.br
    WSGIDaemonProcess htpwd user=htpwd group=htpwd threads=5
    WSGIScriptAlias / /var/www/html/htpwd/htpwd_wsgi.py

    <Directory /var/www/html/htpwd>
        WSGIProcessGroup htpwd
        WSGIApplicationGroup %{GLOBAL}
        Order deny,allow
        Allow from all
    </Directory>
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