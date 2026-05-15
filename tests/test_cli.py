# -*- coding: utf-8 -*-

import afwf.api as afwf

from afwf_genpass.cli import Command
from afwf_genpass.constants import (
    default_length,
    id_default_length,
    n_id,
    n_password,
    n_uuid4,
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


class TestGenid:
    def test_empty_query_uses_default_length(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().genid(query="")

        assert len(captured) == 1
        assert len(captured[0].items) == n_id
        for item in captured[0].items:
            assert len(item.arg) == id_default_length

    def test_valid_length_returns_ids(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().genid(query=str(id_default_length))

        assert len(captured) == 1
        assert len(captured[0].items) == n_id
        for item in captured[0].items:
            assert len(item.arg) == id_default_length

    def test_invalid_argument_returns_error_item(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().genid(query="not-a-number")

        assert len(captured) == 1
        assert len(captured[0].items) == 1
        assert captured[0].items[0].icon is not None


class TestGenuuid4:
    def test_returns_uuids(self, monkeypatch):
        captured = []
        monkeypatch.setattr(
            afwf.ScriptFilter,
            "send_feedback",
            lambda self: captured.append(self),
        )

        Command().genuuid4()

        assert len(captured) == 1
        assert len(captured[0].items) == n_uuid4


class TestOneVariants:
    """``_one`` variants print exactly one line to stdout, no Alfred JSON."""

    def test_genpass_one_default_length(self, capsys):
        Command().genpass_one()
        out = capsys.readouterr().out.strip()
        assert len(out) == default_length

    def test_genpass_one_custom_length(self, capsys):
        Command().genpass_one(length=20)
        out = capsys.readouterr().out.strip()
        assert len(out) == 20

    def test_genid_one_default_length(self, capsys):
        Command().genid_one()
        out = capsys.readouterr().out.strip()
        assert len(out) == id_default_length

    def test_genid_one_custom_length(self, capsys):
        Command().genid_one(length=10)
        out = capsys.readouterr().out.strip()
        assert len(out) == 10

    def test_genuuid4_one(self, capsys):
        import re

        Command().genuuid4_one()
        out = capsys.readouterr().out.strip()
        assert re.match(
            r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
            out,
        )


if __name__ == "__main__":
    from afwf_genpass.tests import run_cov_test

    run_cov_test(
        script=__file__,
        module="afwf_genpass.cli",
        preview=False,
    )
