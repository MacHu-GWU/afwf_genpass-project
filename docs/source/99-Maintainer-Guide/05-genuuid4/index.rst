.. _maintainer-guide-genuuid4:

genuuid4 — UUID4 Generator
==============================================================================

Overview
------------------------------------------------------------------------------
The ``genuuid4`` feature generates standard RFC 4122 UUID4s, formatted as
``8-4-4-4-12`` lowercase hex (36 chars including hyphens), e.g.
``550e8400-e29b-41d4-a716-446655440000``. Type ``genuuid4`` in Alfred and you
get 8 freshly generated UUID4s; hit ⌘C on any item to copy.

UUID4 has a fixed format, so this generator takes **no parameters** — no
length, no charset, no configuration. Every call returns 122 bits of
randomness sourced from :func:`uuid.uuid4`.


Files involved
------------------------------------------------------------------------------
- `afwf_genpass/genuuid4.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/genuuid4.py>`_

  The generator. Three public functions:

  - ``gen_uuid4()`` — generate one UUID4 string.
  - ``gen_uuid4s()`` — build an ``afwf.ScriptFilter`` containing ``n_uuid4``
    (8) freshly generated UUID4s.
  - ``main()`` — Alfred entry point. No parameters; returns the ``ScriptFilter``
    directly.

- `afwf_genpass/constants.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/constants.py>`_

  Defines ``n_uuid4=8`` — the only knob this feature has. No charset or length
  bounds, since UUID4 is fully specified by RFC 4122.

- `afwf_genpass/cli.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/cli.py>`_

  Two subcommands wrap ``genuuid4``:

  - ``Command.genuuid4()`` — Alfred Script Filter; takes no arguments. The
    matching Alfred node uses ``argumenttype=2`` (no argument). Exceptions
    are caught and rendered as an error item that opens the rotating log
    file on Enter.
  - ``Command.genuuid4_one()`` — prints exactly one UUID4 to stdout, no
    Alfred JSON. Suitable for shell pipelines (e.g.
    ``id=$(afwf-genpass genuuid4-one)``).

- `info.plist <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/info.plist>`_

  Alfred Script Filter node with ``keyword=genuuid4``, ``argumenttype=2``
  (no argument — UUID4 has nothing to configure), calling::

      ~/.local/bin/uvx --from "afwf-genpass==X.Y.Z" afwf-genpass genuuid4


Tests
------------------------------------------------------------------------------
- `tests/test_genuuid4.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_genuuid4.py>`_

  Covers ``gen_uuid4``, ``gen_uuid4s``, and ``main()``. Each generated value
  is asserted to match the canonical UUID4 regex
  ``^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$``.

- `tests/test_cli.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_cli.py>`_

  The ``TestGenuuid4`` and ``TestOneVariants`` classes exercise the CLI
  wrappers — including the ``genuuid4_one`` stdout variant.
