import os
import logging

from xlson._lib.general_utils import ConfBase, setup_logging


CONSTANTS_PATH = os.path.dirname(os.path.realpath(__file__))
TESTS_PATH = os.path.join(CONSTANTS_PATH, "tests")
CONF_DIR_PATH = os.path.join(CONSTANTS_PATH, "configs")
DEFAULT_CONFIG = os.path.join(CONF_DIR_PATH, "default_config.ini")

LOG_CONFIG = os.path.join(CONF_DIR_PATH, "log_conf.yaml")
LOGGER_NAME = "xlson_logger"

class ConfConstants(ConfBase):

    def __init__(self, config_path=DEFAULT_CONFIG):
        # GENERAL

        super(ConfConstants, self).__init__(config_path=config_path)


conf_constants = ConfConstants()

setup_logging(log_conf_path=LOG_CONFIG)
xlson_logger = logging.getLogger(LOGGER_NAME)
