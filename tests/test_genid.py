# -*- coding: utf-8 -*-

import afwf.api as afwf

from afwf_genpass.constants import (
    id_charset,
    id_default_length,
    id_max_length,
    id_min_length,
    msg_enter_id,
    msg_id_invalid_length_value,
    n_id,
)
from afwf_genpass.genid import (
    gen_id,
    gen_ids,
    main,
)


def test_gen_id():
    _charset_set = set(id_charset)

    sid = gen_id(id_default_length)
    assert isinstance(sid, str)
    assert len(sid) == id_default_length
    assert all(ch in _charset_set for ch in sid)

    for length in (id_min_length, id_max_length):
        sid = gen_id(length)
        assert len(sid) == length
        assert all(ch in _charset_set for ch in sid)


def test_gen_id_excludes_confusing_chars():
    # Charset drops: 0 (looks like O/o), 1 (looks like l), l, O, o.
    # NOTE: capital `I` is kept in the charset.
    banned = set("01lOo")
    for _ in range(100):
        sid = gen_id(id_default_length)
        assert not (set(sid) & banned)


def test_gen_id_is_random():
    samples = {gen_id(id_default_length) for _ in range(20)}
    # With 57^16 ≈ 1e28 possibilities, 20 samples should never collide.
    assert len(samples) == 20


def test_gen_ids():
    sf = gen_ids(id_default_length)
    assert len(sf.items) == n_id
    for item in sf.items:
        assert len(item.arg) == id_default_length
        assert item.title == item.arg
        assert item.valid is True


class TestMain:
    def test_generate_id(self):
        sf = main(query=str(id_default_length))
        assert len(sf.items) == n_id
        for item in sf.items:
            assert len(item.arg) == id_default_length
            assert item.title == item.arg
            assert item.valid is True

    def test_boundary_lengths(self):
        for length in (id_min_length, id_max_length):
            sf = main(query=str(length))
            assert len(sf.items) == n_id
            for item in sf.items:
                assert len(item.arg) == length

    def test_no_argument(self):
        sf = main(query="")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert item.title == msg_enter_id
        assert item.autocomplete == str(id_default_length)

    def test_whitespace_query_treated_as_empty(self):
        sf = main(query="   ")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert item.title == msg_enter_id

    def test_non_numeric_argument(self):
        sf = main(query="InValid")
        assert len(sf.items) == 1
        item = sf.items[0]
        assert "InValid" in item.title
        assert "is NOT a valid length" in item.title
        assert item.icon is not None
        assert item.icon.path == str(afwf.IconFileEnum.error)

    def test_out_of_range_argument(self):
        for query in (str(id_min_length - 1), str(id_max_length + 1)):
            sf = main(query=query)
            assert len(sf.items) == 1
            item = sf.items[0]
            assert item.title == msg_id_invalid_length_value
            assert item.icon is not None


if __name__ == "__main__":
    from afwf_genpass.tests import run_cov_test

    run_cov_test(
        script=__file__,
        module="afwf_genpass.genid",
        preview=False,
    )
