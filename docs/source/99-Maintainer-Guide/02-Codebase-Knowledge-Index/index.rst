Codebase Knowledge Index
==============================================================================

Overview
------------------------------------------------------------------------------
``afwf_genpass`` is an Alfred workflow that ships three independent generators —
secure passwords, YouTube-style short IDs, and UUID4s — each wired to its own
Alfred keyword. Under the hood it is a thin layer on top of the
`afwf <https://github.com/MacHu-GWU/afwf-project>`_ SDK: every Alfred keyword
calls a Python function that returns an ``afwf.ScriptFilter`` object, which the
CLI serializes to JSON for Alfred to render.

This page is the **knowledge index** for the codebase — a one-stop list of the
files that define what the workflow does, what each file is responsible for,
and where to look when you need to change something. All paths are relative
to the project root.


Top-level configuration
------------------------------------------------------------------------------
- `pyproject.toml <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/pyproject.toml>`_

  Package metadata, dependencies (``afwf``, ``fire``, ``diskcache``), and the
  console-script entry point. The ``[project.scripts]`` block declares::

      afwf-genpass = "afwf_genpass.cli:run"

  This is the binary that Alfred invokes, and the same binary you reach from
  the shell via ``uvx --from afwf-genpass afwf-genpass ...``.

- `info.plist <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/info.plist>`_

  The Alfred workflow definition. Contains three Script Filter nodes —
  ``genpass``, ``genid``, ``genuuid4`` — each of which calls
  ``~/.local/bin/uvx --from "afwf-genpass==X.Y.Z" afwf-genpass <subcommand> ...``.
  Keep this file in the repo as the source of truth; the installed copy in
  Alfred is a snapshot taken at release time.

- `README.rst <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/README.rst>`_

  End-user documentation: what each keyword does, allowed length ranges,
  default values, banned visually-confusing characters, and install
  instructions.


Source package — ``afwf_genpass/``
------------------------------------------------------------------------------
- `afwf_genpass/cli.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/cli.py>`_

  The ``fire``-based command-line entry point exposed as the ``afwf-genpass``
  console script. Two flavours per generator:

  - ``gen*`` — Alfred Script Filter entry, emits JSON via ``afwf`` and routes
    uncaught errors to a rotating log file at
    ``~/.alfred-afwf/afwf_genpass/error.log``.
  - ``gen*-one`` — plain stdout, prints exactly one value. Independent of
    Alfred; handy in shell pipelines (e.g.
    ``export TOKEN=$(afwf-genpass genid-one)``).

- `afwf_genpass/constants.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/constants.py>`_

  Single source of truth for all configuration knobs: character sets, banned
  characters, length bounds, default lengths, item-count constants, and the
  human-readable UI messages shown in Alfred. Change a default length or a
  banned character here and the rest of the codebase picks it up.

- `afwf_genpass/genpass.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/genpass.py>`_

  Secure password generator. Detailed in :ref:`Section 03 <maintainer-guide-genpass>`.

- `afwf_genpass/genid.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/genid.py>`_

  YouTube-style short-ID generator. Detailed in :ref:`Section 04 <maintainer-guide-genid>`.

- `afwf_genpass/genuuid4.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/genuuid4.py>`_

  UUID4 generator. Detailed in :ref:`Section 05 <maintainer-guide-genuuid4>`.

- `afwf_genpass/paths.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/paths.py>`_

  Centralized ``PathEnum`` of all project paths (project home, cache directory,
  error log, docs, virtualenv, etc.). All file paths used elsewhere in the
  codebase should be resolved through ``path_enum`` rather than hard-coded.


Tests — ``tests/``
------------------------------------------------------------------------------
- `tests/test_genpass.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_genpass.py>`_
- `tests/test_genid.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_genid.py>`_
- `tests/test_genuuid4.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_genuuid4.py>`_
- `tests/test_cli.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_cli.py>`_

  Pytest-based unit tests covering both the pure ``main()`` functions and the
  ``Command`` class in ``cli.py`` (including the ``_one`` stdout variants).
  Each file can be run standalone — the ``if __name__ == "__main__":`` block
  invokes pytest with coverage for the matching module.


Reading order
------------------------------------------------------------------------------
If you are new to the codebase, read in this order:

1. ``README.rst`` — what the workflow does from a user's perspective
2. ``constants.py`` — every tunable parameter in the project
3. ``genpass.py`` / ``genid.py`` / ``genuuid4.py`` — the three generators
4. ``cli.py`` — how the generators are exposed to Alfred and the shell
5. ``info.plist`` — how Alfred binds keywords to CLI subcommands
