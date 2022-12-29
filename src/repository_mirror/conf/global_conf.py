import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.dirname(BASE_DIR)

HOME_DIR = str(Path.home())
CONFIG_DIR = os.path.join(HOME_DIR, '.repository-mirror')
ENVIRONMENT_CONF_PATH = os.path.join(CONFIG_DIR, 'environment.yml')
ENVIRONMENT_DIR = os.path.join(CONFIG_DIR, 'environments')

DEFAULT_ENVIRONMENT = 'default'