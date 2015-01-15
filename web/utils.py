import sys, os, decimal
from datetime import datetime
from flask import json, request, Response
from functools import wraps, update_wrapper, partial

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) is decimal.Decimal:
            return float(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, '__json__'):
            return obj.__json__()
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return json.JSONEncoder.default(self, obj)

class JsonResponse(Response):
    """ Response from a JSON API view """

    def __init__(self, response, status=None, headers=None, **kwargs):
        """ Init a JSON response
        :param response: Response data
        :type response: *
        :param status: Status code
        :type status: int|None
        :param headers: Additional headers
        :type headers: dict|None
        """
        # Store response
        self._response_data = response

        # Init super
        super(JsonResponse, self).__init__(
            json.dumps(self._response_data, cls=CustomJSONEncoder, indent=None),
            headers=headers, status=status, mimetype='application/json',
            direct_passthrough=True, **kwargs)

    def get_json(self):
        """ Get the response data object (preprocessed) """
        return self._response_data

    def __getitem__(self, item):
        """ Proxy method to get items from the underlying object """
        return self._response_data[item]


def normalize_response_value(rv):
    """ Normalize the response value into a 3-tuple (rv, status, headers)
        :type rv: tuple|*
        :returns: tuple(rv, status, headers)
        :rtype: tuple(Response|JsonResponse|*, int|None, dict|None)
    """
    status = headers = None
    if isinstance(rv, tuple):
        rv, status, headers = rv + (None,) * (3 - len(rv))
    return rv, status, headers


def make_json_response(rv):
    """ Make JsonResponse
    :param rv: Response: the object to encode, or tuple (response, status, headers)
    :type rv: tuple|*
    :rtype: JsonResponse
    """
    # Tuple of (response, status, headers)
    rv, status, headers = normalize_response_value(rv)

    # JsonResponse
    if isinstance(rv, JsonResponse):
        return rv

    # none check
    if rv == None:
        return JsonResponse({"error": "not found"} , 404)

    # Data
    return JsonResponse(rv, status, headers)

def json_response(f):
    """ Declare the view as a JSON API method
        This converts view return value into a :cls:JsonResponse.
        The following return types are supported:
            - tuple: a tuple of (response, status, headers)
            - any other object is converted to JSON
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        rv = f(*args, **kwargs)
        return make_json_response(rv)
    return wrapper