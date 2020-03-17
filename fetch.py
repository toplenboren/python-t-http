"""
- Send COMPILED_REQUESTS to the remote URL
- check remote URL to be correct
- determine http vs https
- hold connection logic
- process timeout argument and return exception if request is taking too long
"""
import ssl
import socket

from http_request import Address


DEFAULT_HTTP_PORT = 80
DEFAULT_HTTPS_PORT = 443


def resolve_port(https: bool) -> int:
    if https:
        return DEFAULT_HTTPS_PORT
    else:
        return DEFAULT_HTTP_PORT


def fetch(addr: Address, request: str) -> None:
    https = addr.protocol == 'https://'

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((addr.host, resolve_port(https)))
    if https:
        s = ssl.wrap_socket(s)
    s.sendall(bytes(request, encoding='utf-8'))

    while True:
        data = s.recv(64)
        if not data:
            s.close()
            break
        print(data)

    s.close()