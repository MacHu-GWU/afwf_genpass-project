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


Source modules
------------------------------------------------------------------------------
- :mod:`afwf_genpass.genuuid4` — the generator. Three public functions:

  - ``gen_uuid4()`` — generate one UUID4 string.
  - ``gen_uuid4s()`` — build an ``afwf.ScriptFilter`` containing ``n_uuid4``
    (8) freshly generated UUID4s.
  - ``main()`` — Alfred entry point. No parameters; returns the
    ``ScriptFilter`` directly.

- :mod:`afwf_genpass.constants` — defines ``n_uuid4=8``, the only knob this
  feature has. No charset or length bounds, since UUID4 is fully specified by
  RFC 4122.

- :mod:`afwf_genpass.cli` — two subcommands wrap ``genuuid4``:

  - ``Command.genuuid4()`` — Alfred Script Filter; takes no arguments. The
    matching Alfred node uses ``argumenttype=2`` (no argument). Exceptions
    are caught and rendered as an error item that opens the rotating log
    file on Enter.
  - ``Command.genuuid4_one()`` — prints exactly one UUID4 to stdout, no
    Alfred JSON. Suitable for shell pipelines (e.g.
    ``id=$(afwf-genpass genuuid4-one)``).


Alfred workflow definition
------------------------------------------------------------------------------
The Alfred Script Filter node for ``genuuid4`` lives in ``info.plist``, with
``keyword=genuuid4`` and ``argumenttype=2`` (no argument — UUID4 has nothing
to configure). Its ``script`` field invokes::

    ~/.local/bin/uvx --from "afwf-genpass==X.Y.Z" afwf-genpass genuuid4

.. dropdown:: info.plist

    .. literalinclude:: ../../../../info.plist
       :language: xml
       :linenos:


Tests
------------------------------------------------------------------------------
- :mod:`tests.test_genuuid4` — covers ``gen_uuid4``, ``gen_uuid4s``, and
  ``main()``. Each generated value is asserted to match the canonical UUID4
  regex ``^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$``.

- :mod:`tests.test_cli` — the ``TestGenuuid4`` and ``TestOneVariants`` classes
  exercise the CLI wrappers, including the ``genuuid4_one`` stdout variant.
