# -*- coding: utf-8 -*-

import fire
import afwf.api as afwf

from .constants import (
    default_length as _genpass_default_length,
    id_default_length as _genid_default_length,
)
from .genpass import main as genpass_main, random_password
from .genid import main as genid_main, gen_id
from .genuuid4 import main as genuuid4_main, gen_uuid4
from .paths import path_enum

_log_error = afwf.log_error(
    log_file=path_enum.path_error_log,
    tb_limit=10,
)


def _error_sf(exc: Exception) -> afwf.ScriptFilter:
    item = afwf.Item(
        title=f"{type(exc).__name__}: {exc}",
        subtitle=f"Press Enter to open the error log: {path_enum.path_error_log}",
        icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.error),
        valid=True,
    )
    item.open_file(str(path_enum.path_error_log))
    return afwf.ScriptFilter(items=[item])


class Command:
    def genpass(self, query: str) -> None:
        """Script Filter: generate random passwords.

        Alfred Script field (dev):
            .venv/bin/afwf-genpass genpass --query '{query}'

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_genpass==<ver> afwf-genpass genpass --query '{query}'
        """
        if not query:
            query = "12"

        @_log_error
        def _run():
            genpass_main(query=str(query)).send_feedback()

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    def genid(self, query: str) -> None:
        """Script Filter: generate YouTube-style random short IDs.

        Alfred Script field (dev):
            .venv/bin/afwf-genpass genid --query '{query}'

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_genpass==<ver> afwf-genpass genid --query '{query}'
        """
        if not query:
            query = "16"

        @_log_error
        def _run():
            genid_main(query=str(query)).send_feedback()

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    def genuuid4(self) -> None:
        """Script Filter: generate random UUID4s.

        UUID4 has no parameters. Configure the Alfred Script Filter node with
        ``argumenttype=2`` (no argument).

        Alfred Script field (dev):
            .venv/bin/afwf-genpass genuuid4

        Alfred Script field (prod):
            ~/.local/bin/uvx --from afwf_genpass==<ver> afwf-genpass genuuid4
        """

        @_log_error
        def _run():
            genuuid4_main().send_feedback()

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    # --------------------------------------------------------------------------
    # "_one" variants — generate exactly one value and print it to stdout.
    # No Alfred ScriptFilter, no JSON; useful for shell pipelines / scripts.
    # --------------------------------------------------------------------------

    def genpass_one(self, length: int = _genpass_default_length) -> None:
        """Print one random password of the given ``length`` to stdout."""
        print(random_password(int(length)))

    def genid_one(self, length: int = _genid_default_length) -> None:
        """Print one YouTube-style random short ID of the given ``length`` to stdout."""
        print(gen_id(int(length)))

    def genuuid4_one(self) -> None:
        """Print one random UUID4 to stdout."""
        print(gen_uuid4())


def run():
    fire.Fire(Command)
