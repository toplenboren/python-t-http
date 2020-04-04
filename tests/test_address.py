import unittest
from http_client.address import Address


class AddressTest(unittest.TestCase):
    def test_correct_address_parsing(self):
        addr_with_long_path = "http://host.com/a/b/c/d/e/f/g/h"
        addr_without_path = "http://host.com"
        short_address = "http://a.b"
        self.assertEqual(
            Address.parse(addr_with_long_path),
            ("http://", "host.com", "a/b/c/d/e/f/g/h"),
        )
        self.assertEqual(Address.parse(addr_without_path), ("http://", "host.com", ""))
        self.assertEqual(Address.parse(short_address), ("http://", "a.b", ""))

    def test_incorrect_address_parsing(self):
        bad_short_address = "http:/a.b"
        with self.assertRaises(Exception):
            Address.parse(bad_short_address)

    def test_address_init(self):
        addr_example = "https://github.com/user/toplenboren"
        addr_obj = Address(addr_example)
        self.assertEqual("github.com", addr_obj.host)
        self.assertEqual("https://", addr_obj.protocol)
        self.assertEqual("user/toplenboren", addr_obj.path)


if __name__ == "__main__":
    unittest.main()
