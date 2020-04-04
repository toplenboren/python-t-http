"""
Compiles Requests from user's settings
"""
from http_client.address import Address

AVAILABLE_METHODS = ["GET", "POST"]
METHODS_WITH_BODY = ["POST"]

AVAILABLE_PROTOCOLS = ["HTTP://", "HTTPS://"]

HTTP_VERSION_HEADER = "HTTP/1.1"


class HttpRequest:
    def __init__(self, addr: str):
        self.addr = Address(addr)
        self.headers = {}
        self.body = {}
        self.method = "GET"

    @staticmethod
    def method_is_ok(method: str):
        if method in AVAILABLE_METHODS:
            return True
        else:
            raise ValueError(
                "Method not supported, supported are: " + AVAILABLE_METHODS.__str__()
            )

    @staticmethod
    def compile_request_from_dict(request_props: dict) -> str:
        msg_array = []
        for key in request_props:
            msg_array.append(str(key) + ":" + str(request_props[key] + "\r\n"))
        return "".join(msg_array)

    def compile(self) -> str:
        request_line = "{} {} {}".format(
            self.method, "/" + self.addr.path, HTTP_VERSION_HEADER
        )
        arbitrary_headers = {"Host": self.addr.host}
        compiled_headers_dict = {**arbitrary_headers, **self.headers}
        headers = self.compile_request_from_dict(compiled_headers_dict)
        body = ""
        if self.method in METHODS_WITH_BODY:
            body = self.compile_request_from_dict(self.body)
        request = request_line + "\r\n" + headers + "\r\n" + body

        return request
