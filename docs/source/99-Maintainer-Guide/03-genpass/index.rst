.. _maintainer-guide-genpass:

genpass — Secure Password Generator
==============================================================================

Overview
------------------------------------------------------------------------------
The ``genpass`` feature generates random passwords that are simultaneously
strong, hand-typeable, and unambiguous when read aloud. Type ``genpass <length>``
in Alfred and you get 8 candidate passwords of the requested length; hit ⌘C
on any item to copy.

Policy enforced for every accepted password:

- Length between ``8`` and ``32`` (default ``12``)
- Contains at least one lowercase letter, one uppercase letter, one digit,
  and one symbol (from ``!%@#&^*``)
- Starts with a letter
- Excludes the visually-confusing characters ``1``, ``l``, ``I``, ``O``, ``0``


Source modules
------------------------------------------------------------------------------
- :mod:`afwf_genpass.genpass` — the generator itself. Three public functions:

  - ``is_valid_password(password)`` — policy check (four-class +
    starts-with-letter).
  - ``random_password(length)`` — generate one password of ``length`` chars,
    rejection-sampling until ``is_valid_password`` returns ``True``.
  - ``gen_passwords(length)`` — build an ``afwf.ScriptFilter`` containing
    ``n_password`` (8) freshly generated passwords.
  - ``main(query)`` — Alfred entry point. Parses ``query`` as an int in
    ``[min_length, max_length]``; otherwise shows an error item with an
    autocomplete hint.

- :mod:`afwf_genpass.constants` — defines ``charset_lower``, ``charset_upper``,
  ``charset_digits``, ``charset_symbols``, ``charset_banned``, the combined
  ``charset_list``, ``min_length=8``, ``default_length=12``, ``max_length=32``,
  ``n_password=8``, and the UI strings shown in Alfred when the user enters
  nothing or an invalid value.

- :mod:`afwf_genpass.cli` — two subcommands wrap ``genpass``:

  - ``Command.genpass(query)`` — Alfred Script Filter; empty ``query`` falls
    back to ``"12"``; exceptions are caught and rendered as an error item
    that opens the rotating log file on Enter.
  - ``Command.genpass_one(length=default_length)`` — prints exactly one
    password to stdout, no Alfred JSON. Suitable for shell pipelines.


Alfred workflow definition
------------------------------------------------------------------------------
The Alfred Script Filter node for ``genpass`` lives in ``info.plist``, with
``keyword=genpass`` and ``argumenttype=1`` (optional argument). Its ``script``
field invokes::

    ~/.local/bin/uvx --from "afwf-genpass==X.Y.Z" afwf-genpass genpass --query '{query}'

.. dropdown:: info.plist

    .. literalinclude:: ../../../../info.plist
       :language: xml
       :linenos:


Tests
------------------------------------------------------------------------------
- :mod:`tests.test_genpass` — covers the policy check, the rejection-sampling
  generator, the ``ScriptFilter`` builder, and every branch of ``main()``
  (valid length, boundary lengths, empty/whitespace query, non-numeric query,
  out-of-range length).

- :mod:`tests.test_cli` — the ``TestGenpass`` and ``TestOneVariants`` classes
  exercise the CLI wrappers, including the ``genpass_one`` stdout variant.
