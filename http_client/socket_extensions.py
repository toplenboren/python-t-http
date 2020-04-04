"""
This file contains additional logic to the socket method — Readline and ReadSection
"""

import socket
from typing import List

CONTINUATION = b'\r\n'
BREAK = b'\r\n\r\n'


def socket_readline(self: socket) -> bytes:
    """
    Gets all data before \r\n
    """
    data = [b'']

    while True:
        chunk = self.recv(1)
        if data[-1] + chunk == CONTINUATION:
            data.append(chunk)
            break
        data.append(chunk)

    return b''.join(data)


def socket_read_section(self: socket) -> List[bytes]:
    """
    Gets all data before \r\n\r\n
    """
    data = [b'', b'', b'', b'']

    while True:
        chunk = socket_readline(self)
        data.append(chunk)
        if b''.join(data[-2:])[-4:] == BREAK:
            break

    return data
