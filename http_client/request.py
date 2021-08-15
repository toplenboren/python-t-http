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
        self.cookies = {}

    @staticmethod
    def method_is_ok(method: str):
        if method in AVAILABLE_METHODS:
            return True
        else:
            raise ValueError(
                "Method not supported, supported are: " + AVAILABLE_METHODS.__str__()
            )

    @staticmethod
    def compile_cookie_header_from_dict(cookies: dict) -> str:
        result = ''
        for k,v in cookies.items():
            cookie = k + '=' + v
            result += cookie + '; '
        return result

    @staticmethod
    def compile_request_from_dict(request_props: dict) -> str:
        msg_array = []
        for key in request_props:
            msg_array.append(str(key) + ": " + str(request_props[key] + "\r\n"))
        return "".join(msg_array)

    def compile(self) -> str:
        request_line = "{} {} {}".format(
            self.method, "/" + self.addr.path, HTTP_VERSION_HEADER
        )
        arbitrary_headers = {"Host": self.addr.host}
        body = ""
        if self.method in METHODS_WITH_BODY:
            body = self.compile_request_from_dict(self.body)
            arbitrary_headers["Content-Type"] = "application/json"
            arbitrary_headers["Content-Length"] = str(len(body))
        compiled_headers_dict = {**arbitrary_headers, **self.headers, **{"cookie": self.compile_cookie_header_from_dict(self.cookies)}}
        headers = self.compile_request_from_dict(compiled_headers_dict)

        request = request_line + "\r\n" + headers + "\r\n" + body

        print(request)
        return request
