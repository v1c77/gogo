# -*- coding: utf-8 -*-

import click
import os
import sys
import importlib
import signal
import logging

logger = logging.getLogger(__name__)




@click.group()
@click.version_option(version=__VERSION__)
def vos():
    pass


@click.command(
    context_settings={
        "ignore_unknown_options": True,
        "allow_extra_args": True
    },
    add_help_option=True
)
def serve():
    """
    start server via grpcio
    :return:
    """
    from gogo.service import runner
    runner()


