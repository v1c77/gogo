# -*- coding: utf-8 -*-

"""
gogo.vos.loader
~~~~~~~~~~~~~~~


load all the server env needed.
"""

import logging

from gogo.consts import APP_CONFIG_PATH
from gogo.vos.utils import parse_config_file

logger = logging.getLogger(__name__)


class ConfigLoader(object):

    def __init__(self, previous_loader=None):
        """

        :param previous_loader: the previous needed loader handler
        :type previous_loader: ConfigLoader
        """
        self.previous_loader = previous_loader
        if self.previous_loader:
            self.config = self.previous_loader.config
        else:
            self.config = {}

    def do_load(self):
        raise NotImplemented

    def load(self):
        if self.previous_loader:
            self.previous_loader.load()
        self.do_load()

    def _merge_config(self, config):
        for key, val in config.items():
            if isinstance(val, dict):
                self.config.setdefault(key, {}).update(val)
            else:
                self.config[key] = val


class AppEnvLoader(ConfigLoader):

    def do_load(self):
        config = parse_config_file(APP_CONFIG_PATH)
        if config is not None:
            self._merge_config(config)


class EnvConfigLoader(ConfigLoader):

    def do_load(self):
        if self.config is None:
            self.config = {}
        # env = os.getenv(CORE_CONFIG_ENV, None)
        # TODO(vici) add for docker support


def build_env_loader():
    # TODO(vici)
    return EnvConfigLoader(
        AppEnvLoader()
    )


