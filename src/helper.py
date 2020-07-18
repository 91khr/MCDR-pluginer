from ruamel.yaml import YAML
import collections
import os.path as path
import typing
from datetime import datetime



def load_conf(location, pattern: typing.Mapping[str, any]) -> dict:
    """ Load a config file according to the pattern """
    # Read the file
    try:
        with open(location, 'r') as f:
            rawconf = YAML(typ="safe").load(f)
    except FileNotFoundError:
        rawconf = {}
    # Load the items according to the pattern
    Conf_t = collections.namedtuple('Conf_t', pattern.keys())
    conf = {}
    for k in pattern.keys():
        conf[k] = (rawconf if k in rawconf else pattern)[k]
    return Conf_t(**conf)



def log(level : 'info' | 'warning' | 'fatal',
        source : str,
        msg : str):
    """ Log given msg """
    print("{} [{}] <{}>: {}".format(datetime.now(), source, level, msg))

