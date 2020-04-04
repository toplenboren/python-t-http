import json
import os
import unittest

from http_client.client import HttpClient


class ProductionTest(unittest.TestCase):
    def test_http_get_request_to_httpbin(self):
        cl = HttpClient({"address": "http://httpbin.org/get?foo=bar"})
        cl.fire()

        correct_data = {"foo": "bar"}

        self.assertEqual(correct_data, json.loads(cl.last_response.body)["args"])

    def test_https_get_request_to_httpbin(self):
        cl = HttpClient({"address": "https://httpbin.org/get?foo=bar"})
        cl.fire()

        correct_data = {"foo": "bar"}

        self.assertEqual(correct_data, json.loads(cl.last_response.body)["args"])

    def test_http_post_request_to_httpbin(self):
        cl = HttpClient(
            {
                "address": "http://httpbin.org/post",
                "method": "POST",
                "body": {"foo": "bar"},
            }
        )
        cl.fire()

        correct_data = "foo: bar\r\n"

        self.assertEqual(correct_data, json.loads(cl.last_response.body)["data"])


if __name__ == "__main__":
    unittest.main()
