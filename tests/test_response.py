import socket
import unittest
from http_client.response import Response


class RequestTest(unittest.TestCase):
    def test_response_headers_parsing(self):
        s = socket.socket()
        resp = Response(s)
        resp.parse_headers(
            [b"Content-Length: 25\r\n", b"Content-Type: text/html; charset=UTF-16\r\n"]
        )

        headers = {"Content-Length": "25", "Content-Type": "text/html; charset=UTF-16"}
        self.assertEqual(resp.headers, headers)
        self.assertEqual(resp.body_length, 25)
        self.assertEqual(resp.encoding, "UTF-16")

    def test_response_status_parsing(self):
        s = socket.socket()
        resp = Response(s)
        resp.parse_status_code(b"HTTP 1/1 200 OK")

        self.assertEqual(resp.status, 200)


if __name__ == "__main__":
    unittest.main()
