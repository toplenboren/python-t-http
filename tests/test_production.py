import unittest

from http_client.client import HttpClient


class ProductionTest(unittest.TestCase):
    def test_get_request_to_example_com(self):
        cl = HttpClient({'address': 'http://example.com', 'output': 'save'})
        cl.fire()

        with open('production/example.txt', 'r') as f:
            example = f.read()

        self.assertEqual(cl.last_response.body.replace(' ', ''), example.replace(' ', ''))


if __name__ == '__main__':
    unittest.main()
