# -*- coding: utf-8 -*-

import click
from . import __VERSION__


@click.group()
@click.version_option(version=__VERSION__)
def vos():
    pass


@click.command()
def serve():
    set_context_server()
    from gogo.service import run_server
    run_server()


