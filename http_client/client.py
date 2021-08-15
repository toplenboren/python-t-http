from http_client.io_handler import check_output_file, outprint
from http_client.request import HttpRequest
from http_client.fetch import fetch


class HttpClient:
    def __init__(self, arguments: dict, **kwargs):
        self.rq = HttpRequest(arguments["address"])
        self.progress_bar = kwargs.get('progress_bar')
        self.output = None
        self.timeout = 2
        self.process_options(arguments)

    def process_options(self, kwargs: dict):
        def is_valid(arg: str) -> bool:
            return arg in kwargs and kwargs[arg] is not None

        if is_valid("output") and check_output_file(kwargs["output"]):
            self.output = kwargs["output"]
        if is_valid("method") and HttpRequest.method_is_ok(kwargs["method"]):
            self.rq.method = kwargs["method"]
        if is_valid("timeout"):
            self.timeout = kwargs["timeout"]
        if is_valid("body"):
            self.rq.body = kwargs["body"]
        if is_valid("headers"):
            self.rq.headers = kwargs["headers"]

    def fire(self):
        """
        Gets the response and writes it to the output
        """
        self.progress_bar.start()
        response = fetch(self.rq.addr, self.rq.compile(), self.timeout, lambda x: self.progress_bar.set(x))
        self.progress_bar.finish()
        self.last_response = response
        outprint(self.output, response)
