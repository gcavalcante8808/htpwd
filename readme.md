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

For more information, take a look at:

http://flask.pocoo.org/docs/deploying/mod_wsgi/

Other ways to deploy are available as well (gunicorn, uwsgi and others) at the
same page.

Installation
-----------

1. Clone the project to your computer:

` git clone https://github.com/gcavalcante8808/htpwd `

2. Install the project's dependencies:

` cd htpwd `
` pip install -r requirements.txt `

Configuration
-------------

For quick purposes, the deploy.wsgi file can be used for a fast deploy in an
Apache WebServer. In any case, you need to define the following environment
variables as follows:

 * HTPASSWD_FILE: The location of htpasswd file (eg: /data/app.htpasswd)

 * SECRET_KEY: Secred key that will be used within session and csrf_token.
eg: echo "SOMESTRINGHERE" | md5sum

 * USER_REGEXP: Some verification regexp, that will be used to verify the
 user name field. Must be provided. If unsure, define it as [A-z0-9_.]+ for
 all possible matches.

 eg: ^\d{11}@ENTERPRISE$ will match Brazilian CPF appended with the
 @ENTERPRISE suffix.

 * TARGET_PAGE: The link for a page which the user can access with the new
 password. eg: https://myzabbix.enterprise.com.