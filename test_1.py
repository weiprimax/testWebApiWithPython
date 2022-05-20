import unittest
from testWebApi import cube


class Test_test_1(unittest.TestCase):
    def test_A(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_cube(self):
        self.assertEqual(cube(2), 8)


if __name__ == "__main__":
    unittest.main()
