import unittest
from http_client.request import HttpRequest


class RequestTest(unittest.TestCase):
    def test_request_without_body_compilation(self):

        req_obj = HttpRequest("http://www.abc.com/zxc")
        req_obj.headers = {"Content-Type": "zxc", "Content-Length": "25"}

        req = "GET /zxc HTTP/1.1\r\nHost: www.abc.com\r\nContent-Type: zxc\r\nContent-Length: 25\r\n\r\n"

        self.assertEqual(req_obj.compile(), req)

    def test_request_with_body_compilation(self):
        req_obj2 = HttpRequest("http://www.abc.com/zxc")
        req_obj2.headers = {"Content-Type": "zxc", "Content-Length": "25"}
        req_obj2.method = "POST"
        req_obj2.body = {"Somebody": "Once", "Told": "Me"}

        req = (
            "POST /zxc HTTP/1.1\r\nHost: www.abc.com\r\nContent-Type: zxc\r\nContent-Length: 25\r\n\r\nSomebody: "
            "Once\r\nTold: Me\r\n"
        )

        self.assertEqual(req_obj2.compile(), req)


if __name__ == "__main__":
    unittest.main()
