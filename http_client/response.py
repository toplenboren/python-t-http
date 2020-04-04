import re
from socket import socket
from typing import List

from http_client.socket_extensions import socket_read_section, socket_readline

DEFAULT_ENCODING = "utf-8"


class Response:
    """
    Has all the information about the single request in socket,
    Forges the response information and stores it into itself
    """

    def __init__(self, sock: socket):
        self.socket = sock
        self.headers = {}
        self.body = ""
        self.status = 0
        self.encoding = "utf-8"
        self.body_length = 0

    def receive_response(self):
        self.forge_status_code()
        self.forge_headers()
        self.forge_body()

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

    def forge_body(self):
        data = self.socket.recv(self.body_length)
        self.body = data.decode(self.encoding)
