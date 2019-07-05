# Attention: this script can not import code from other parts of bill-rec
import os
import logging
import logging.config

import yaml


def setup_logging(
        log_conf_path,
        default_level=logging.INFO,
        env_key='LOG_CFG'):
    path = log_conf_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):

        with open(path, 'rt') as f:
            string = f.read()
            config = yaml.load(string)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def digitalize_str(s):
    if type(s) is str and len(s) >= 2:
        if s[0] == "0" and s[1] != ".":
            return s
    try:
        return int(s)
    except (ValueError, TypeError):
        try:
            return float(s)
        except (ValueError, TypeError):
            return s
