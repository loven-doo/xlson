# Attention: this script can not import code from other parts of bill-rec
import os
import logging
import logging.config
import configparser

import yaml


class ConfBase(object):

    def __init__(self, config_path):
        self.config_path = None
        self.config = None
        if config_path:
            self.update_by_config(config_path=config_path)

    def update_by_config(self, config_path):
        self.config_path = config_path
        self.config = _config_parser(config_path=config_path)
        config_sections = self.config.sections()
        for param in self.__dict__.keys():
            new_value = None
            for config_section in config_sections:
                if self._get_from_config(self.config, config_section, param, fallback=None):
                    new_value = self.config.get(config_section, param)
                    break
            if new_value:
                if type(self.__dict__[param]) is list:
                    self.__dict__[param] = [elm.strip() for elm in new_value.split(",")]
                elif type(self.__dict__[param]) is bool:
                    self.__dict__[param] = bool_from_str(new_value)
                elif new_value.lower() in ("0", "false", "f", "no", "n", "na", "none", "null"):
                    self.__dict__[param] = None
                else:
                    self.__dict__[param] = type(self.__dict__[param])(new_value)

    @staticmethod
    def _get_from_config(config_obj, section, option, fallback):
        try:
            return config_obj.get(section, option)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback


def _config_parser(config_path):
    """ Function parses config file and puts the result into an object of ConfigParser class
      :param config_path: path to config file
      :return: a ConfigParser object
      """
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def bool_from_str(string):
    if str(string).lower() in ("0", "false", "f", "no", "n", "na", "none", "null"):
        return False
    else:
        return True


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
