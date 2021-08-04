# -*- coding: utf-8 -*-

import unittest
from afwf_genpass.helpers import is_valid_password, random_password


class Test(unittest.TestCase):
    def test_is_valid_password(self):
        assert is_valid_password("abcdef") is False
        assert is_valid_password("123456") is False

        assert is_valid_password("abc456XYZ!@#") is True
        assert is_valid_password("456XYZ!@#") is False
        assert is_valid_password("abcXYZ!@#") is False
        assert is_valid_password("abc456!@#") is False
        assert is_valid_password("abc456XYZ") is False

    def test_random_password(self):
        assert len(random_password(8)) == 8

        for i in range(10):
            password = random_password(12)
            assert is_valid_password(password)


if __name__ == '__main__':
    unittest.main()
