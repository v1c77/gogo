# -*- coding: utf-8 -*-
import time

from gogo.service import Service, dispatcher_with_meta
from example.hello_bro_pb2_grpc import BroServicer
from example.hello_bro_pb2 import HelloReply

service = Service(
    timeout=3 * 1000,
)


def func_cost():
    print('c is runing.!!!')
    start = time.time()
    end = start + 10
    i = 1

    while i > 0:
        i += 1
        if time.time() > end:
            break
    print('down')


def handler_hello():

    user = 'gogo_user'
    msg = 'Hello, {}'.format(user)
    by = 'gogo_server'
    return HelloReply(
        message=msg,
        by=by)


# TODO(vici)
# I need a meta with hello_bro_pb2_grpc

class Dispatcher(dispatcher_with_meta(BroServicer)):

    """the DispatcherMixin will handle error."""

    def SayHello(self, request, context):
        # a dispatcher method can only connect the handler to grpc service
        # method.
        return handler_hello()


service.register(Dispatcher)
