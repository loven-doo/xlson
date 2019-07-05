import os
import logging

from xlson._lib.general_utils import setup_logging


CONSTANTS_PATH = os.path.dirname(os.path.realpath(__file__))
TESTS_PATH = os.path.join(CONSTANTS_PATH, "tests")
CONF_DIR_PATH = os.path.join(CONSTANTS_PATH, "configs")

LOG_CONFIG = os.path.join(CONF_DIR_PATH, "log_conf.yaml")
LOGGER_NAME = "xlson_logger"

setup_logging(log_conf_path=LOG_CONFIG)
xlson_logger = logging.getLogger(LOGGER_NAME)
