# -*- coding: utf-8 -*-

import logging
import six
import yaml

logger = logging.getLogger(__name__)


def parse_config_file(file):
    try:
        if isinstance(file, six.string_types):
            with open(file) as f:
                return yaml.load(f)
        else:
            return yaml.load(f)

    except IOError:
        logger.warning('config file {!r} dose not exist.'.format(file))
    except yaml.error.YAMLError:
        logger.warning('cannot prase {!r} for config'.format(file))
