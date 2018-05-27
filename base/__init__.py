from common.logging import LoggerHandler
from common.utils import find_config_file, load_config_from_pyfile

__all__ = ['log', 'config']

config_file = find_config_file()
config = load_config_from_pyfile(config_file)
log = LoggerHandler(file_path=config['log_file'], log_level=config['log_level']).log_init()

log.info('use config file: "{}"'.format(config_file))
