# -*- coding: utf-8 -*-

import os
import pytest
from afwf_genpass.handlers.genpass import (
    is_valid_password,
    random_password,
    default_length,
    msg_enter_password,
    msg_autocomplete,
    msg_invalid_length_value,
    n_password,
    handler,
)


def test_is_valid_password():
    assert is_valid_password("abcdef") is False
    assert is_valid_password("123456") is False

    assert is_valid_password("abc456XYZ!@#") is True
    assert is_valid_password("456XYZ!@#") is False
    assert is_valid_password("abcXYZ!@#") is False
    assert is_valid_password("abc456!@#") is False
    assert is_valid_password("abc456XYZ") is False


def test_random_password():
    assert len(random_password(8)) == 8

    for i in range(10):
        password = random_password(12)
        assert is_valid_password(password)


class TestHandler:
    def test_generate_password(self):
        sf = handler.handler("12")
        assert len(sf.items) == n_password
        for item in sf.items:
            assert len(item.arg) == default_length
            assert item.title == item.arg

    def test_no_argument(self):
        sf = handler.handler("")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert item.title == msg_enter_password
        assert item.autocomplete == str(default_length)

    def test_invalid_argument(self):
        sf = handler.handler("InValid")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert "InValid" in item.title
        assert "is NOT a valid length" in item.title

        sf = handler.handler("Hello World")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert "Hello World" in item.title
        assert "is NOT a valid length" in item.title

    def test_invalid_argument_value(self):
        cases = [
            "6",
            "100",
        ]
        for query in cases:
            sf = handler.handler(query)
            assert len(sf.items) == 1
            item = sf.items[0]
            assert item.title == msg_invalid_length_value


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
