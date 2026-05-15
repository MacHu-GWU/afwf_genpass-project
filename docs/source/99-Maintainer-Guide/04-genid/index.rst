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


Source modules
------------------------------------------------------------------------------
- :mod:`afwf_genpass.genid` — the generator. Three public functions:

  - ``gen_id(length)`` — generate one random ID by sampling ``length``
    characters from ``id_charset`` via :func:`secrets.choice`.
  - ``gen_ids(length)`` — build an ``afwf.ScriptFilter`` containing
    ``n_id`` (8) freshly generated IDs.
  - ``main(query)`` — Alfred entry point. Parses ``query`` as an int in
    ``[id_min_length, id_max_length]``; otherwise shows an error item
    with an autocomplete hint.

- :mod:`afwf_genpass.constants` — defines ``id_charset`` (the 57-char
  alphabet, declared inline so the exclusions are reviewable in diff),
  ``id_min_length=6``, ``id_default_length=16``, ``id_max_length=32``,
  ``n_id=8``, and the UI strings.

- :mod:`afwf_genpass.cli` — two subcommands wrap ``genid``:

  - ``Command.genid(query)`` — Alfred Script Filter; empty ``query`` falls
    back to ``"16"``; exceptions are caught and rendered as an error item
    that opens the rotating log file on Enter.
  - ``Command.genid_one(length=id_default_length)`` — prints exactly one ID
    to stdout, no Alfred JSON. Suitable for shell pipelines (e.g.
    ``slug=$(afwf-genpass genid-one --length 10)``).


Alfred workflow definition
------------------------------------------------------------------------------
The Alfred Script Filter node for ``genid`` lives in ``info.plist``, with
``keyword=genid`` and ``argumenttype=1`` (optional argument). Its ``script``
field invokes::

    ~/.local/bin/uvx --from "afwf-genpass==X.Y.Z" afwf-genpass genid --query '{query}'

.. dropdown:: info.plist

    .. literalinclude:: ../../../../info.plist
       :language: xml
       :linenos:


Tests
------------------------------------------------------------------------------
- :mod:`tests.test_genid` — covers the generator, the ``ScriptFilter``
  builder, and every branch of ``main()`` (valid length, boundary lengths,
  empty/whitespace query, non-numeric query, out-of-range length). Also
  asserts that the output charset never contains banned characters.

- :mod:`tests.test_cli` — the ``TestGenid`` and ``TestOneVariants`` classes
  exercise the CLI wrappers, including the ``genid_one`` stdout variant.
