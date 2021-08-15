import math
import re
from socket import socket
from typing import List

from http_client.socket_extensions import socket_read_section, socket_readline

DEFAULT_ENCODING = "utf-8"
BUFFER = 512 # buffer in bytes


class Response:
    """
    Has all the information about the single request in socket,
    Forges the response information and stores it into itself
    """

    def __init__(self, sock: socket):
        self.socket = sock
        self.headers = {}
        self.raw_body = b''
        self.body = ''
        self.status = 0
        self.encoding = DEFAULT_ENCODING
        self.response_encoding = None
        self.body_length = 0
        self.received = 0

    def receive_response(self, progress_callback):
        self.forge_status_code()
        self.forge_headers()
        self.forge_body(progress_callback)

    def forge_status_code(self):
        data = socket_readline(self.socket)
        self.parse_status_code(data)

    def parse_status_code(self, status_data_line: bytes):
        status_code_candidate = re.search(
            r"\d{3,}", status_data_line.decode(DEFAULT_ENCODING)
        )
        status_code_candidate = status_code_candidate.group()
        if status_code_candidate is None:
            raise Exception("Status code unknown, wrong server response")
        else:
            self.status = int(status_code_candidate)

    def forge_headers(self):
        section = socket_read_section(self.socket)
        self.parse_headers(section)
        content_type_header = self.headers.get('Content-Type', None),
        content_type_header = content_type_header[0]
        if content_type_header is not None:
            content_type_header = content_type_header.split('; ')
            for piece in content_type_header:
                if 'charset' in piece:
                    piece = piece.split('=')
                    if len(piece) == 2:
                        self.response_encoding = piece[-1]

    def parse_headers(self, header_data_lines: List[bytes]):
        for line in header_data_lines:
            decoded_line = line.decode(DEFAULT_ENCODING)
            header = decoded_line.split(": ")
            if len(header) < 2:
                continue
            else:
                self.headers[header[0]] = header[1].replace("\r\n", "")


        if "Content-Length" in self.headers.keys():
            self.body_length = int(self.headers["Content-Length"])
        else:
            raise Exception("Content-Length header was not present!")
        if "Content-Type" in self.headers.keys():
            for prop in self.headers["Content-Type"].split("; ")[1:]:
                prop_name, value = prop.split("=")
                if prop_name == "charset":
                    self.encoding = value
        else:
            self.encoding = DEFAULT_ENCODING

    def forge_body(self, progress_callback):
        full_response_received = False

        while not full_response_received:
            to_receive = min(BUFFER, self.body_length - self.received)
            data = self.socket.recv(to_receive)
            self.raw_body += data
            self.received += to_receive
            progress_callback(self.received / self.body_length * 100)
            if self.received >= self.body_length:
                full_response_received = True

        if self.response_encoding is not None:
            self.body = self.raw_body.decode(self.response_encoding)
        else:
            self.body = self.raw_body
