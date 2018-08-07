# -*- coding: utf-8 -*-


class GoGoBaseException(Exception):
    """Base Exception for vespene"""


class AppConfigLoadFailException(GoGoBaseException):
    """Failed to load app.yaml, not found or yaml invalid"""


class AppImportError(GoGoBaseException):
    """ Exception raised when loading an application """


class AppUnknowError(GoGoBaseException):
    """ Exception raised when loading an application """
