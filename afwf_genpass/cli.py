# -*- coding: utf-8 -*-

"""
Fire-based command-line entry point exposed as the ``afwf-genpass`` script.

Two flavours per generator:

- ``gen*`` — Alfred Script Filter entry, emits JSON via afwf and routes errors
  to a rotating log file at :attr:`paths.path_enum.path_error_log`.
- ``gen*-one`` — plain stdout, prints exactly one value. Independent of Alfred;
  handy in shell pipelines (e.g. ``export TOKEN=$(afwf-genpass genid-one)``).
"""

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
    """Build an error ScriptFilter; pressing Enter opens the log file."""
    item = afwf.Item(
        title=f"{type(exc).__name__}: {exc}",
        subtitle=f"Press Enter to open the error log: {path_enum.path_error_log}",
        icon=afwf.Icon.from_image_file(path=afwf.IconFileEnum.error),
        valid=True,
    )
    item.open_file(str(path_enum.path_error_log))
    return afwf.ScriptFilter(items=[item])


class Command:
    """Fire subcommand container. ``gen*`` → Alfred JSON; ``gen*-one`` → stdout."""

    def genpass(self, query: str) -> None:
        """Script Filter: random passwords. Empty ``query`` falls back to length 12."""
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
        """Script Filter: random short IDs. Empty ``query`` falls back to length 16."""
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
        """Script Filter: random UUID4s. Configure Alfred with ``argumenttype=2``."""

        @_log_error
        def _run():
            genuuid4_main().send_feedback()

        try:
            _run()
        except Exception as e:
            _error_sf(e).send_feedback()

    # --------------------------------------------------------------------------
    # "_one" variants — print exactly one value to stdout. Plain text, no afwf.
    # --------------------------------------------------------------------------

    def genpass_one(self, length: int = _genpass_default_length) -> None:
        """Print one random password of ``length`` chars."""
        print(random_password(int(length)))

    def genid_one(self, length: int = _genid_default_length) -> None:
        """Print one random short ID of ``length`` chars."""
        print(gen_id(int(length)))

    def genuuid4_one(self) -> None:
        """Print one random UUID4."""
        print(gen_uuid4())


def run():
    """Console-script entry point declared in ``pyproject.toml``."""
    fire.Fire(Command)
