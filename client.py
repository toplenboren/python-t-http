"""
- Main guy, gets ARGUMENTS and returns RESULT
"""
from io_handler import prepare_output_file
from http_request import HttpRequest
from fetch import fetch


class HttpClient:

    def __init__(self, kwargs: dict):
        self.rq = HttpRequest(*kwargs['address'])
        self.output = 'stdout'
        self.timeout = 30
        self.process_options(kwargs)

    def process_options(self, kwargs: dict):

        def is_valid(arg: str) -> bool:
            return arg in kwargs and kwargs[arg] is not None

        if is_valid('output'):
            self.output = prepare_output_file(kwargs['output'])
        if is_valid('method') in kwargs and HttpRequest.method_is_ok(kwargs['method']):
            self.rq.method = kwargs['method']
        if is_valid('timeout'):
            self.timeout = kwargs['timeout']
        if is_valid('body'):
            self.rq.body = kwargs['body']
        if is_valid('headers'):
            self.rq.headers = kwargs['headers']

    def fire(self):
        compiled_request = self.rq.compile()
        outstream = fetch(self.rq.addr, compiled_request)
        print(outstream)
