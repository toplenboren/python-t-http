"""
- Compile REQUESTS from ARGUMENTS
- check if arguments are OK
"""

AVAILABLE_METHODS = ['GET', 'POST']
METHODS_WITH_BODY = ['POST']

AVAILABLE_PROTOCOLS = ['HTTP://', 'HTTPS://']


class Address:
    def __init__(self, addr: str):
        parsed_addr = Address.parse(addr)
        self.protocol = parsed_addr[0]
        self.host = parsed_addr[1]
        self.path = parsed_addr[2]

    # TODO rewrite
    @staticmethod
    def parse(addr: str) -> (str, str, str):
        if len(addr) < 8:
            raise ValueError("Bad address, please ensure it starts with http:// or https://")

        if addr[0:7].lower() == 'http://':
            protocol = addr[0:7]
            host = addr[7:].split('/')[0]
            path = '/'.join(addr[7:].split('/')[1:])
            return protocol, host, path

        elif addr[0:8].lower() == 'https://':
            protocol = addr[0:8]
            host = addr[8:].split('/')[0]
            path = '/'.join(addr[8:].split('/')[1:])
            return protocol, host, path

        else:
            raise ValueError("Bad address, please ensure it starts with http:// or https://")


class HttpRequest:
    def __init__(self, addr: str):
        self.addr = Address(addr)
        self.headers = {}
        self.body = {}
        self.method = "GET"

    @staticmethod
    def http_version_header() -> str:
        return 'HTTP/1.1'

    @staticmethod
    def method_is_ok(method: str):
        if method in AVAILABLE_METHODS:
            return True
        else:
            raise ValueError("Method not supported, supported are: " + AVAILABLE_METHODS.__str__())

    @staticmethod
    def compile_request_from_dict(request_props: dict) -> str:
        msg_array = []
        for key in request_props:
            msg_array.append(str(key) + ":" + str(request_props[key] + '\r\n'))
        return ''.join(msg_array)

    def compile(self) -> str:
        request_line = '{} {} {}'.format(self.method, '/' + self.addr.path, HttpRequest.http_version_header())
        arbitrary_headers = {'Host':self.addr.host}
        compiled_headers_dict = {**arbitrary_headers, **self.headers}
        headers = self.compile_request_from_dict(compiled_headers_dict)
        body = ''
        if self.method in METHODS_WITH_BODY:
            body = self.compile_request_from_dict(self.body)
        request = request_line + '\r\n' + headers + '\r\n' + body

        print(request)

        return request
