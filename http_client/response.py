import re
from socket import socket, timeout
from typing import List

from http_client.socket_extensions import socket_read_section, socket_readline

DEFAULT_ENCODING = "utf-8"
BUFFER = 128  # buffer in bytes


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
        self.body_length = None
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

    def parse_headers(self, header_data_lines: List[bytes]):
        for line in header_data_lines:
            decoded_line = line.decode(DEFAULT_ENCODING)
            header = decoded_line.split(": ")
            if len(header) < 2:
                continue
            else:
                self.headers[header[0]] = header[1].replace("\r\n", "")

        self.headers = dict((k.lower(), v) for k, v in self.headers.items())

        if "content-length" in self.headers.keys():
            self.body_length = int(self.headers["content-length"])
        # else:
        #     raise Exception("Content-Length header was not present!")

        if "content-type" in self.headers.keys():
            for prop in self.headers["content-type"].split("; ")[1:]:
                prop_name, value = prop.split("=")
                if prop_name == "charset":
                    self.response_encoding = value

    def forge_body(self, progress_callback):
        # get response
        if self.body_length is None:
            self.recv_all()
        else:
            self.recv_all_with_content_length(progress_callback)

        # try to decode if needed
        if self.response_encoding is not None:
            self.body = self.raw_body.decode(self.response_encoding)
        else:
            self.body = self.raw_body

    def recv_all_with_content_length(self, progress_callback):
        """
        Get response with present content length header. Supports progress bar
        """
        full_response_received = False
        while not full_response_received:
            to_receive = min(BUFFER, self.body_length - self.received)
            data = self.socket.recv(to_receive)
            self.raw_body += data
            self.received += to_receive
            progress_callback(self.received / self.body_length * 100)
            if self.received >= self.body_length:
                full_response_received = True

    def recv_all(self):
        """
        Get response without present content length header. Does not support progress bar
        """
        prev_timeout = self.socket.gettimeout()
        try:
            self.socket.settimeout(0.1)
            while True:
                try:
                    self.raw_body += (self.socket.recv(BUFFER))
                except timeout:
                    return
        finally:
            self.socket.settimeout(prev_timeout)
