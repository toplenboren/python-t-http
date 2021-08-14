"""
Prepare a socket and forge Response class
"""

import ssl
import socket
from typing import Callable

from http_client.request import Address
from http_client.response import Response

DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443


def resolve_port(https: bool) -> int:
    if https:
        return DEFAULT_HTTPS_PORT
    return DEFAULT_HTTP_PORT


def setup_socket(addr: Address, request: str, timeout: int):
    """
    Prepares a socket according to user settings
    """
    https = addr.protocol == "https://"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr.host, resolve_port(https)))
    if https:
        s = ssl.wrap_socket(s)
    s.sendall(bytes(request, encoding="utf-8"))
    s.settimeout(timeout)

    return s


def fetch(addr: Address, request: str, timeout: int, callback: Callable) -> Response:
    """
    Receives the response, progress callback should be lambda which accepts percentage (as float) and returns void
    """
    s = setup_socket(addr, request, timeout)
    response = Response(s)
    response.receive_response(callback)
    if 200 <= response.status < 400:
        return response
    else:
        raise Exception(
            "The response returned with an error-indicating status code:",
            response.status,
        )
