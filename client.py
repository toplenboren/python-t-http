"""
- Main guy, gets ARGUMENTS and returns RESULT
"""
import io


def process_output(param):
    pass


class http_client():

    def __init__(self, kwargs: dict):
        self.addr = kwargs['address']
        self.output = 'stdout'
        self.method = 'GET'
        self.timeout = 30
        self.body = {}
        self.header = {}
        self.process_options(kwargs)

    def fire(self):
        pass

    def process_options(self, kwargs: dict):
        if 'output' in kwargs:
            self.output = io.prepare_output_file(output)
