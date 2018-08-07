# -*- coding: utf-8 -*-
from gogo.vos.config import load_core_config
from gogo.vos.consts import ENV_PROD, ENV_DEV, ENV_TEST, ENV_SHELL


def env():
    return load_core_config().env


def is_in_prod():
    return env() == ENV_PROD


def is_in_dev():
    return env() == ENV_DEV


def is_in_test():
    return env() == ENV_TEST


def is_in_shell():
    return env() == ENV_SHELL


def is_grpc_app():
    pass
