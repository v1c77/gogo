# -*- coding: utf-8 -*-

"""
gogo.vos.config
~~~~~~~~~~~~~~~

Used to load grpc server config.
"""
import logging
import sys

import yaml

from gogo.consts import REGISTRY_ENABLED, APP_CONFIG_PATH
from gogo.exc import AppConfigLoadFailException
from gogo.utils import EnvvarReader, cached_property
from gogo.vos.consts import ENV_DEV, SYSLOG_SOCKET, DEFAULT_APP_PORT
from gogo.vos.loader import build_env_loader

logger = logging.getLogger(__name__)


class CoreConfig(object):
    """
    Application independent configs, as a yaml file at
    `CORE_CONFIG_PATH`, example::

        env: 'dev'
        cluster: 'elf-master-1'
        zookeeper_config:
          hosts: localhost:2181
          username: root
          password:

    witch show clearly the app's dependence and identity.
    :type loader: ConfigLoader

    """

    def __init__(self, loader=None):
        self.config = None
        self.loader = loader if loader else build_env_loader()

    def load(self):
        self.config = self.loader.load()
        return self

    @property
    def env(self):
        return self.config.get('env', ENV_DEV)

    @property
    def registory_enabled(self):
        return self.config.get('registry_enabled', REGISTRY_ENABLED)

    @property
    def raw_cluster(self):
        # TODO(vici) topo in a server like elf
        raise NotImplementedError
        # return self.config.get('cluster', None)

    @property
    def cluster(self):
        raise NotImplemented

    @property
    def zookeeper_config(self):
        return self.config.get('zookeeper_configs', {
            'hosts': 'localhost:2181',
            'username': 'root',
            'password': '',
        })

    @property
    def etcd_config(self):
        # FIXME add default etcd config
        return self.config.get('etcd_configs', {})

    @property
    def statsd_uri(self):
        uri = self.config.get('statsd_url', None)
        if uri:
            return uri
        if self.env == ENV_DEV:
            return "statsd://127.0.0.1:8122"
        else:
            logger.error('no statsd host configured for env: %s cluster: %s',
                         self.env, self.cluster)

    @property
    def syslog_socket(self):
        return self.config.get('syslog_socket') or SYSLOG_SOCKET


# TODO(vici) a lot things to do. before load core_config
core_config = None


def load_core_config(raise_exc=False):
    raise NotImplementedError


app_config = None


class AppConfig(object):
    """Application related configs, as a yaml file at
    `APP_CONFIG_PATH`, e.g.:

        app_name: ves.note
        settings: note.settings
        services:
          app: note.service:service
          thrift_file: note/note.thrift
          requirements: thrift_requirements.txt
    """
    DEFAULT_APP_PORT = DEFAULT_APP_PORT

    def __init__(self):
        self.config = None
        self.etrace_enabled = False
        self.api_ops_metrics_enabled = False
        self.ves_stats_enabled = False

    def load(self, config_path=APP_CONFIG_PATH, raise_exc=False):
        try:
            self.config = yaml.load(open(config_path))
        except (IOError, yaml.error.YAMLError):
            if raise_exc is True:
                raise AppConfigLoadFailException
            logger.error('Connot load %s, exit.', config_path)
            sys.exit(1)
        return self

    def _get_conf(self, key, default=None):
        """Help to try config first on key 'services' and then root.
        """
        if 'services' in self.config:
            return self.config['services'].get(key, default)
        return self.config.get(key, default)

    @cached_property
    def app_uri(self):
        app = self._get_conf('app', None)
        if app is None:
            raise RuntimeError("Missing `app` in app.yaml. ")
        return app

    def get_grpc_module(self):
        pass


class GrpcAppConfig(AppConfig):
    TYPE_NAME = 'grpc'
    DEFAULT_APP_PORT = DEFAULT_APP_PORT


def load_app_config():
    """Load app config lazily
    AKA load_server_config.

    """
    global app_config
    if app_config is None:
        # from . import env
        # if env.is_grpc_app():
        app_config = GrpcAppConfig().load(raise_exc=raise_exc)
    return app_config


load_server_config = load_app_config

