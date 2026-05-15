# -*- coding: utf-8 -*-

import afwf.api as afwf

from afwf_genpass.constants import (
    default_length,
    min_length,
    max_length,
    msg_enter_password,
    msg_invalid_length_value,
    n_password,
)
from afwf_genpass.genpass import (
    is_valid_password,
    random_password,
    main,
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
    assert len(random_password(min_length)) == min_length

    for _ in range(10):
        password = random_password(default_length)
        assert is_valid_password(password)


class TestMain:
    def test_generate_password(self):
        sf = main(query=str(default_length))
        assert len(sf.items) == n_password
        for item in sf.items:
            assert len(item.arg) == default_length
            assert item.title == item.arg
            assert item.valid is True

    def test_boundary_lengths(self):
        for length in (min_length, max_length):
            sf = main(query=str(length))
            assert len(sf.items) == n_password
            for item in sf.items:
                assert len(item.arg) == length

    def test_no_argument(self):
        sf = main(query="")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert item.title == msg_enter_password
        assert item.autocomplete == str(default_length)

    def test_whitespace_query_treated_as_empty(self):
        sf = main(query="   ")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert item.title == msg_enter_password

    def test_non_numeric_argument(self):
        sf = main(query="InValid")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert "InValid" in item.title
        assert "is NOT a valid length" in item.title
        assert item.icon is not None
        assert item.icon.path == str(afwf.IconFileEnum.error)

    def test_multi_token_argument(self):
        sf = main(query="Hello World")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert "Hello World" in item.title
        assert "is NOT a valid length" in item.title
        assert item.icon is not None

    def test_out_of_range_argument(self):
        for query in (str(min_length - 1), str(max_length + 1)):
            sf = main(query=query)
            assert len(sf.items) == 1
            item = sf.items[0]
            assert item.title == msg_invalid_length_value
            assert item.icon is not None


if __name__ == "__main__":
    from afwf_genpass.tests import run_cov_test

    run_cov_test(
        script=__file__,
        module="afwf_genpass.genpass",
        preview=False,
    )
