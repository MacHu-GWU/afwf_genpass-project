# -*- coding: utf-8 -*-

import fire
import afwf.api as afwf

from .genpass import main as genpass_main
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


def run():
    fire.Fire(Command)
