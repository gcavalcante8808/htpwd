import six
from hashlib import md5
if six.PY2:
    import ConfigParser as configparser
elif six.PY3:
    import configparser


def create_secret_key(string):
    """
    :param string: A string that will be returned as a md5 hash/hexdigest.
    :return: the hexdigest (hash) of the string.
    """
    h = md5()
    h.update(string.encode('utf-8'))
    return h.hexdigest()


def create_config_file(htfile, key, target_page, regexp=r'[A-z0-9_.]+',
                       fname='htpwd.ini'):
    """
    :param htfile: the location of the htpasswd formated file.
    :param key: a secret_key(string, hex digest) that will be used in the page
     to give more security to the sessions.
    :param target_page: a string containing the http address that the user will
    be redirected to.
    :param regexp: a regexp that will be applied to the username parsing.
    :param fname: the filename of configfile, default as htpwd.ini.
    :return: a config file containing all the information passed.
    """
    config = configparser.ConfigParser()
    config['HTPWD'] = {'htpasswd_file': htfile,
                         'secret_key': key,
                         'target_page': target_page,
                         'regexp': regexp}
    with open(fname, 'w') as configfile:
        config.write(configfile)

    return config


def parse_config_file(file='htpwd.ini'):
    """
    :param file: the configfile that will be parsed. htpwd.ini will be used if
    no value is provided.
    :return: a ConfigParser object containing the information.
    """
    config = configparser.ConfigParser()
    config.read(file)

    if not config.has_section('HTPWD'):
        raise NotImplementedError('The file doesnt have a HTPWD Section')

    return config
