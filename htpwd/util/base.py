import six
from hashlib import md5
if six.PY2:
    import ConfigParser as configparser
elif six.PY3:
    import configparser


def create_secret_key(string):
    h = md5()
    h.update(string.encode('utf-8'))
    return h.hexdigest()


def create_config_file(htfile, key, target_page, regexp=r'[A-z0-9_.]+',
                       fname='htpwd.ini'):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'htpasswd_file': htfile,
                         'secret_key': key,
                         'target_page': target_page,
                         'regexp': regexp}
    with open(fname, 'w') as configfile:
        config.write(configfile)

    return config


def parse_config_file(file):
    config = configparser.ConfigParser()
    config.read(file)
    return config


