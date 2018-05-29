# coding:utf-8
import time
import os
import shutil
import uuid
import datetime


def find_config_file():
    config_file = '/etc/beyond/license/settings.py'
    if os.path.isfile(config_file):
        return config_file
    config_file = os.path.abspath('./settings.py')
    return config_file


def load_config_from_pyfile(config_file):
    d = {}
    try:
        with open(config_file, mode='rb') as f:
            exec(compile(f.read(), config_file, 'exec'), d)
        del d['__builtins__']
    except IOError as e:
        e.strerror = 'Unable to load configuration file (%s)' % e.strerror
        raise
    return d


def time_str_to_stamp(time_str):
    """
    :param time_str: eg. '1451663999' or '2016-01-01 23:59:59'
    :return: number timestamp: eg. 1451663999
    """
    try:
        time_stamp = int(float(time_str))
    except Exception:
        try:
            time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            time_stamp = time.mktime(time_array)
        except Exception:
            time_stamp = None
    return time_stamp


def get_metric_unit(metric):
    unit_dict = {'bytes': 'Bytes', 'hertz': 'HZ', 'mbs': 'MB', 'gbs': 'GB', 'ops': 'op/s', 'iops': 'op/s',
                 'ms': 'ms', 'util': '%', 'percent': '%', 'seconds': 'seconds', 'MBps': 'MB/s', 'KBps': 'KB/s',
                 'Bps': 'B/s', 'packets_rate': 'packets/s'}
    unit = unit_dict.get(metric.split('_')[-1], '')
    if unit:
        return unit
    for key in unit_dict:
        if metric.find('_' + key) > -1:
            return unit_dict[key]


def get_metric_args(args, index=0):
    if args and isinstance(args, (str,)):
        return args
    if isinstance(args, (list, tuple)) and len(args) > index:
        return args[index]


def append_or_replace_child(source_list, child, key, value):
    """
    the children of source_list must be dict,and 'key' must in the dict
    if target child in the source_list will replace the old child
    if target child not in the source_list will append to the source_list
    """
    exist = False
    for i, item in enumerate(source_list):
        if item[key] == value:
            source_list[i], exist = child, True
            break
    if not exist:
        source_list.append(child)


def delete_dict_from_list(source_list, match_key, match_value):
    """ the children of source_list must be dict,and 'key' must in the dict """
    for i, item in enumerate(source_list):
        if item[match_key] == match_value:
            del source_list[i]
            break


def backup_files(file_list):
    backup_file_list = []
    for filename in file_list:
        dst = u"{}.{}".format(filename, str(uuid.uuid1()))
        shutil.copyfile(src=filename, dst=dst)
        backup_file_list.append(dst)
    return backup_file_list


def recover_files(backup_file_list):
    for filename in backup_file_list:
        dst = os.path.splitext(filename)[0]
        shutil.move(filename, dst=dst)


def remove_backup_files(backup_file_list):
    for filename in backup_file_list:
        os.remove(filename)


def utc_time2local(utc_str):
    if isinstance(utc_str, (str,)) and len(utc_str) >= 19:
        now = time.time()
        utc_time = datetime.datetime.strptime(utc_str[0:19], '%Y-%m-%dT%H:%M:%S')
        offset = datetime.datetime.fromtimestamp(now) - datetime.datetime.utcfromtimestamp(now)
        local_str = (utc_time + offset).strftime("%Y-%m-%d %H:%M:%S")
        return local_str
    return utc_str


def local_time2utc(local_str):
    if isinstance(local_str, (str,)) and len(local_str) >= 19:
        local_time = time.strptime(local_str[0:19], "%Y-%m-%d %H:%M:%S")
        return datetime.datetime.utcfromtimestamp(time.mktime(local_time))
    return local_str
