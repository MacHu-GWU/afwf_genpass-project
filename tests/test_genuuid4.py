# -*- coding: utf-8 -*-

import re
import uuid

from afwf_genpass.constants import n_uuid4
from afwf_genpass.genuuid4 import (
    gen_uuid4,
    gen_uuid4s,
    main,
)

# 8-4-4-4-12 lowercase hex; version nibble == 4; variant nibble in [8,9,a,b]
_UUID4_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


def test_gen_uuid4_format():
    u = gen_uuid4()
    assert _UUID4_RE.match(u)
    # also round-trippable through stdlib
    parsed = uuid.UUID(u)
    assert parsed.version == 4


def test_gen_uuid4_is_random():
    samples = {gen_uuid4() for _ in range(50)}
    # With 122 bits of randomness, 50 samples should never collide.
    assert len(samples) == 50


def test_gen_uuid4s():
    sf = gen_uuid4s()
    assert len(sf.items) == n_uuid4
    for item in sf.items:
        assert _UUID4_RE.match(item.arg)
        assert item.title == item.arg
        assert item.valid is True
    titles = {item.title for item in sf.items}
    assert len(titles) == n_uuid4  # all distinct


class TestMain:
    def test_returns_n_uuid4_items(self):
        sf = main()
        assert len(sf.items) == n_uuid4
        for item in sf.items:
            assert _UUID4_RE.match(item.arg)
            assert item.title == item.arg
            assert item.valid is True

    def test_each_call_is_random(self):
        sf1 = main()
        sf2 = main()
        titles1 = {item.title for item in sf1.items}
        titles2 = {item.title for item in sf2.items}
        assert not (titles1 & titles2)


if __name__ == "__main__":
    from afwf_genpass.tests import run_cov_test

    run_cov_test(
        script=__file__,
        module="afwf_genpass.genuuid4",
        preview=False,
    )
