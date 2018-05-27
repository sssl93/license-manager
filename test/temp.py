import types


def load_config_from_pyfile(config_file):
    d = types.ModuleType('config')
    d.__file__ = config_file
    try:
        with open(config_file, mode='rb') as f:
            exec(compile(f.read(), config_file, 'exec'), d.__dict__)
    except IOError as e:
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
    return d


print(load_config_from_pyfile('/opt/develop/license-manager/test/c.py'))
