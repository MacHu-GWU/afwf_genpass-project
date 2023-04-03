# -*- coding: utf-8 -*-

import os
import pytest
import afwf_genpass


def test_import():
    _ = afwf_genpass
    _ = afwf_genpass.wf


if __name__ == "__main__":
    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
