# -*- coding: utf-8 -*-
import logging
import time
import functools

import grpc
import six
from concurrent import futures

from example.server import Bro
from gogo.exc import AppUnknowError
from .utils import load_obj

from types import FunctionType


from gogo.ctx import g
# TODO(vici) db session manager for mongo
# TODO(vici) config module
from gogo.vos.config import load_app_config
# TODO(vici) request data meta
# TODO(vici) env module
from gogo.consts import PlACE_HODER
from gogo.log import make_meta_dict
from utils import random_string


# TODO(vici) hook event import for diff handlers of gunicorn


def _save_mate_data(func):
    """the id and other info for each request"""
    @functools.wraps(func)
    def wrapper(*args):
        # default values
        seq = PlACE_HODER
        rid = g.get_call_meta('tracker_request_id')
        seq = g.get_call_meta('tracker_seq')
        meta = g.get_call_meta('meta', {})
        if rid == PlACE_HODER:
            rid = 'fake_' + random_string(8)

        g.clear_api_ctx()  # clean exist local info

        g.set_call_meta('call_time', time.time())
        g.set_call_meta('method', func.func_name)
        g.set_call_meta('args', args)
        g.set_call_meta('request_id', rid)
        g.set_call_meta('seq', seq)
        g.set_call_meta('meta', meta)
        make_meta_dict("meta", meta)

        return func(*args)
    return wrapper

# TODO(vici) add profile handler
# TODO(vici) with db session tracker


class Service(dict):
    PROHIBITED_ATTRS = {}  # attrs can not visit
    REQUESTED_PROCESSORS = {}  # processors for gogo server

    __getattr__ = dict.__getitem__

    def __setattr__(self, name, value):
        return super(Service, self).__setattr__(name, value)

    def __init__(self, *args, **kwargs):
        super(Service, self).__init__(*args, **kwargs)
        self['__apis_to_shield'] = {}  # ???
        self.logger = logging.getLogger(__name__)

        # TODO(vici) grpc dispatcher cls
        self.grpc_service_dispatcher_cls = None
        self.grpc_module = self.get('grpc', None) or \
            load_app_config().get_grpc_module()

        # TODO(vici) workders rely on
        self.threading_pool = futures.ThreadPoolExecutor(max_workers=20)

        # TODO(vici) reopen after add exception module.
        # for exc_name in ('user_exc', 'system_exc', 'unknown_exc'):
        #     if exc_name not in self:
        #         raise RuntimeError(
        #             "Service should contain following exception definitions: "
        #             "'user_exc', 'system_exc', 'unknown_exc'"
        #         )

        # if 'error' not in self:
        #     self.error = self.user_exc, self.system_exc, self.unknown_exc

        # if service not has `name` attr, load from app.yaml
        if 'name' not in self:
            self.name = load_app_config().app_name

        # else:
        #     if self.name != load_app_config().app_name:
        #         msg = ("`app name` in `app.yaml` is different from that in "
        #                "`service.py`, and we take `app name` in `app.yaml` "
        #                "as standard.")
        #         self.logger.error(msg)
        #         raise RuntimeError(msg)
        #
        # self.timeout = self.get("timeout", DEFAULT_SOFT_TIMEOUT)
        # self.api_hard_timeout = self.get("api_hard_timeout",
        #                                  DEFAULT_HARD_TIMEOUT)
        # self.__processors = []
        # for proc_cls in self.REQUESTED_PROCESSORS:
        #     self.__processors.append(proc_cls(self))

    def register(self, dispatcher):
        self.grpc_service_dispatcher_cls = dispatcher

    def serve(self):
        # TODO(vici) split every line to their own file_path
        pool = self.threading_pool
        _server = grpc.server(thread_pool=pool)
        self.grpc_module.add_BroServicer_to_server(Bro(), _server)
        _server.add_insecure_port('[::]:1994')
        _server.start()
        try:
            while True:
                time.sleep(1 << 50)
        except KeyboardInterrupt:
            _server.stop(0)


def wrapper_grpc_method(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        # TODO(vici)  add handler for server
        raise NotImplementedError
    return wrapper


class DispatcherMata(type):
    # TODO(vici) add error handler, event, log, ctx handler.

    def __new__(mcs, cls_name, bases, cls_dict):
        new_cls_dict = {}
        for attr_name, attr in cls_dict:
            if isinstance(attr, FunctionType):
                new_cls_dict[attr_name] = wrapper_grpc_method(attr)
            else:
                new_cls_dict[attr_name] = attr
        return type.__new__(mcs, cls_name, bases, new_cls_dict)


def dispatcher_with_meta(grpc_base):
    return six.with_metaclass(DispatcherMata, grpc_base)


class GrpcApplication(object):
    """gogo grpc application"""

    def __init__(self):
        self.app_config = load_app_config()
        self.app_uri = self.app_config.app_uri

    def run(self):
        app = self.load_grpc_app()
        app.serve()

    def load_grpc_app(self):
        app = load_obj(self.app_uri)
        if isinstance(app, Service):
            return app

        raise AppUnknowError("Application object in unknow type: %r" % app)


def runner():
    GrpcApplication().run()
