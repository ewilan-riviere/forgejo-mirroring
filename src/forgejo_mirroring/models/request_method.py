"""Request method for HTTP"""

from enum import Enum


class RequestMethod(Enum):
    """Request method for HTTP"""

    GET = "get"
    POST = "post"
    PATCH = "patch"
    PUT = "PUT"
    DELETE = "DELETE"
