# -*- coding: utf-8 -*-

import afwf.api as afwf

from afwf_genpass.cli import Command
from afwf_genpass.constants import (
    default_length,
    n_password,
    n_shortid,
    shortid_default_length,
)


class TestGenpass:
    def test_empty_query_uses_default_length(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().genpass(query="")

        assert len(captured) == 1
        assert len(captured[0].items) == n_password
        for item in captured[0].items:
            assert len(item.arg) == default_length

    def test_valid_length_returns_passwords(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().genpass(query=str(default_length))

        assert len(captured) == 1
        assert len(captured[0].items) == n_password
        for item in captured[0].items:
            assert len(item.arg) == default_length

    def test_invalid_argument_returns_error_item(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().genpass(query="not-a-number")

        assert len(captured) == 1
        assert len(captured[0].items) == 1
        assert captured[0].items[0].icon is not None


class TestShortid:
    def test_empty_query_uses_default_length(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().shortid(query="")

        assert len(captured) == 1
        assert len(captured[0].items) == n_shortid
        for item in captured[0].items:
            assert len(item.arg) == shortid_default_length

    def test_valid_length_returns_shortids(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().shortid(query=str(shortid_default_length))

        assert len(captured) == 1
        assert len(captured[0].items) == n_shortid
        for item in captured[0].items:
            assert len(item.arg) == shortid_default_length

    def test_invalid_argument_returns_error_item(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().shortid(query="not-a-number")

        assert len(captured) == 1
        assert len(captured[0].items) == 1
        assert captured[0].items[0].icon is not None


if __name__ == "__main__":
    from afwf_genpass.tests import run_cov_test

    run_cov_test(
        script=__file__,
        module="afwf_genpass.cli",
        preview=False,
    )
