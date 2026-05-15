.. _maintainer-guide-genid:

genid — Short ID Generator
==============================================================================

Overview
------------------------------------------------------------------------------
The ``genid`` feature generates YouTube-style random short IDs suitable for
opaque identifiers in URLs, filenames, blog slugs, etc. Type ``genid <length>``
in Alfred and you get 8 candidate IDs of the requested length; hit ⌘C on any
item to copy.

Key properties:

- **Cryptographically strong**: backed by :func:`secrets.choice`, not
  :mod:`random`.
- **57-character URL-safe charset**: base62 minus the visually-confusing
  ``0``, ``1``, ``l``, ``o``, ``O``. Capital ``I`` is intentionally kept.
- Length between ``6`` and ``32`` (default ``16``).
- Safe to read aloud or hand-copy without ambiguity.


Files involved
------------------------------------------------------------------------------
- `afwf_genpass/genid.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/genid.py>`_

  The generator. Three public functions:

  - ``gen_id(length)`` — generate one random ID by sampling ``length``
    characters from ``id_charset`` via :func:`secrets.choice`.
  - ``gen_ids(length)`` — build an ``afwf.ScriptFilter`` containing
    ``n_id`` (8) freshly generated IDs.
  - ``main(query)`` — Alfred entry point. Parses ``query`` as an int in
    ``[id_min_length, id_max_length]``; otherwise shows an error item
    with an autocomplete hint.

- `afwf_genpass/constants.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/constants.py>`_

  Defines ``id_charset`` (the 57-char alphabet, declared inline so the
  exclusions are reviewable in diff), ``id_min_length=6``,
  ``id_default_length=16``, ``id_max_length=32``, ``n_id=8``, and the UI
  strings.

- `afwf_genpass/cli.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/afwf_genpass/cli.py>`_

  Two subcommands wrap ``genid``:

  - ``Command.genid(query)`` — Alfred Script Filter; empty ``query`` falls
    back to ``"16"``; exceptions are caught and rendered as an error item
    that opens the rotating log file on Enter.
  - ``Command.genid_one(length=id_default_length)`` — prints exactly one ID
    to stdout, no Alfred JSON. Suitable for shell pipelines (e.g.
    ``slug=$(afwf-genpass genid-one --length 10)``).

- `info.plist <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/info.plist>`_

  Alfred Script Filter node with ``keyword=genid``, ``argumenttype=1``
  (optional argument), calling::

      ~/.local/bin/uvx --from "afwf-genpass==X.Y.Z" afwf-genpass genid --query '{query}'


Tests
------------------------------------------------------------------------------
- `tests/test_genid.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_genid.py>`_

  Covers the generator, the ``ScriptFilter`` builder, and every branch of
  ``main()`` (valid length, boundary lengths, empty/whitespace query,
  non-numeric query, out-of-range length). Also asserts that the output
  charset never contains banned characters.

- `tests/test_cli.py <https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/tests/test_cli.py>`_

  The ``TestGenid`` and ``TestOneVariants`` classes exercise the CLI
  wrappers — including the ``genid_one`` stdout variant.
