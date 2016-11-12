# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

""" Application Custom Exceptions """

class NoContentAvailableException(Exception):
    """This exception is thrown when the application is
    able to retrieve a page from EPTC web site but
    there is no content related to the bus line in it."""
    pass

class RemoteServerErrorException(Exception):
    """This exception is thrown when the application gets
    any error from the EPTC server"""
    pass
