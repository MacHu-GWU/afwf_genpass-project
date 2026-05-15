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
files that define what the workflow does and where to look when you need to
change something.


Top-level configuration files
------------------------------------------------------------------------------

The package metadata, dependencies (``afwf``, ``fire``, ``diskcache``), and the
console-script entry point ``afwf-genpass = "afwf_genpass.cli:run"`` are
declared in ``pyproject.toml``. This is the binary that Alfred invokes — and
the same binary you can reach from the shell via ``uvx --from afwf-genpass``.

.. dropdown:: pyproject.toml

    .. literalinclude:: ../../../../pyproject.toml
       :language: toml
       :linenos:

The Alfred workflow definition lives in ``info.plist``. It contains three
Script Filter nodes — ``genpass``, ``genid``, ``genuuid4`` — each of which
calls ``~/.local/bin/uvx --from "afwf-genpass==X.Y.Z" afwf-genpass <subcommand>``.
Keep this file in the repo as the source of truth; the installed copy in
Alfred is a snapshot taken at release time.

.. dropdown:: info.plist

    .. literalinclude:: ../../../../info.plist
       :language: xml
       :linenos:

End-user documentation — what each keyword does, allowed length ranges,
default values, banned visually-confusing characters, and install instructions
— lives in ``README.rst``.

.. dropdown:: README.rst

    .. literalinclude:: ../../../../README.rst
       :language: rst
       :linenos:


Source package — ``afwf_genpass/``
------------------------------------------------------------------------------
- :mod:`afwf_genpass.cli` — the ``fire``-based command-line entry point
  exposed as the ``afwf-genpass`` console script. Two flavours per generator:

  - ``gen*`` — Alfred Script Filter entry, emits JSON via ``afwf`` and routes
    uncaught errors to a rotating log file at
    ``~/.alfred-afwf/afwf_genpass/error.log``.
  - ``gen*-one`` — plain stdout, prints exactly one value. Independent of
    Alfred; handy in shell pipelines (e.g.
    ``export TOKEN=$(afwf-genpass genid-one)``).

- :mod:`afwf_genpass.constants` — single source of truth for all configuration
  knobs: character sets, banned characters, length bounds, default lengths,
  item-count constants, and the human-readable UI messages shown in Alfred.
  Change a default length or a banned character here and the rest of the
  codebase picks it up.

- :mod:`afwf_genpass.genpass` — secure password generator. Detailed in
  :ref:`Section 03 <maintainer-guide-genpass>`.

- :mod:`afwf_genpass.genid` — YouTube-style short-ID generator. Detailed in
  :ref:`Section 04 <maintainer-guide-genid>`.

- :mod:`afwf_genpass.genuuid4` — UUID4 generator. Detailed in
  :ref:`Section 05 <maintainer-guide-genuuid4>`.

- :mod:`afwf_genpass.paths` — centralized ``PathEnum`` of all project paths
  (project home, cache directory, error log, docs, virtualenv, etc.). All file
  paths used elsewhere in the codebase should be resolved through
  ``path_enum`` rather than hard-coded.


Tests — ``tests/``
------------------------------------------------------------------------------
- :mod:`tests.test_genpass`
- :mod:`tests.test_genid`
- :mod:`tests.test_genuuid4`
- :mod:`tests.test_cli`

Pytest-based unit tests covering both the pure ``main()`` functions and the
``Command`` class in :mod:`afwf_genpass.cli` (including the ``_one`` stdout
variants). Each file can be run standalone — the ``if __name__ == "__main__":``
block invokes pytest with coverage for the matching module.


Reading order
------------------------------------------------------------------------------
If you are new to the codebase, read in this order:

1. ``README.rst`` — what the workflow does from a user's perspective
2. :mod:`afwf_genpass.constants` — every tunable parameter in the project
3. :mod:`afwf_genpass.genpass` / :mod:`afwf_genpass.genid` /
   :mod:`afwf_genpass.genuuid4` — the three generators
4. :mod:`afwf_genpass.cli` — how the generators are exposed to Alfred and the
   shell
5. ``info.plist`` — how Alfred binds keywords to CLI subcommands
