# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from afwf_genpass.tests import run_cov_test

    run_cov_test(
        __file__,
        "afwf_genpass",
        is_folder=True,
        preview=False,
    )
