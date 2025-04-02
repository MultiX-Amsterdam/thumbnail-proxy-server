"""Utility functions"""

from flask import jsonify
import traceback


class InvalidUsage(Exception):
    """Handle errors, such as a bad request."""
    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


def handle_invalid_usage(error):
    """
    Handle the error message of the InvalidUsage class.

    Parameters
    ----------
    error : InvalidUsage
        An InvalidUsage object.

    Returns
    -------
    dict
        A response that can be returned to the front-end client.
    """
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def try_wrap_response(func, status_code=400):
    """A decorator that wraps the try-except logic to handle errors."""
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            traceback.print_exc()
            if len(list(ex.args)) > 1:
                e = InvalidUsage(ex.args[0], status_code=status_code)
            else:
                e = InvalidUsage(traceback.format_exc(), status_code=status_code)
            return handle_invalid_usage(e)
    return inner_function
