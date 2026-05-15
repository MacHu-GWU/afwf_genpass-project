
.. image:: https://readthedocs.org/projects/afwf-genpass/badge/?version=latest
    :target: https://afwf-genpass.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/afwf_genpass-project/actions/workflows/main.yml/badge.svg
    :target: https://github.com/MacHu-GWU/afwf_genpass-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/afwf_genpass-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/afwf_genpass-project

.. image:: https://img.shields.io/pypi/v/afwf-genpass.svg
    :target: https://pypi.python.org/pypi/afwf-genpass

.. image:: https://img.shields.io/pypi/l/afwf-genpass.svg
    :target: https://pypi.python.org/pypi/afwf-genpass

.. image:: https://img.shields.io/pypi/pyversions/afwf-genpass.svg
    :target: https://pypi.python.org/pypi/afwf-genpass

.. image:: https://img.shields.io/badge/✍️_Release_History!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/afwf_genpass-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/⭐_Star_me_on_GitHub!--None.svg?style=social&logo=github
    :target: https://github.com/MacHu-GWU/afwf_genpass-project

------

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://afwf-genpass.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_genpass-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_genpass-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/afwf_genpass-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/afwf-genpass#files


Welcome to ``afwf_genpass`` Documentation
==============================================================================
.. image:: https://afwf-genpass.readthedocs.io/en/latest/_static/afwf_genpass-logo.png
    :target: https://afwf-genpass.readthedocs.io/en/latest/

**Use Case**:

This Alfred workflow exposes two independent Script Filters, each bound to its own keyword:

- ``genpass`` — **Generate Secure Password**

  Type ``genpass <length>`` in Alfred to get 8 random passwords of the given
  ``<length>``. Each password is guaranteed to contain at least one lowercase
  letter, one uppercase letter, one digit and one symbol (from ``!%@#&^*``),
  and always starts with a letter.

  - Allowed length: ``8`` to ``32``; default is ``12`` (just hit Enter on ``genpass``)
  - Tab autocompletes to the default length
  - Hit ⌘C on any item to copy the password to your clipboard
  - Visually-confusing characters ``1``, ``l``, ``I``, ``O``, ``0`` are excluded for readability

- ``genid`` — **Generate Short ID**

  Type ``genid <length>`` in Alfred to get 8 random YouTube-style short IDs of
  the given ``<length>``. Backed by ``secrets.choice`` (cryptographically
  strong) over a 57-character URL-safe charset, suitable for use as opaque
  identifiers in URLs, filenames, blog slugs, etc.

  - Allowed length: ``6`` to ``32``; default is ``16`` (just hit Enter on ``genid``)
  - Tab autocompletes to the default length
  - Hit ⌘C on any item to copy the ID to your clipboard
  - Visually-confusing characters ``0``, ``1``, ``l``, ``O``, ``o`` are excluded for readability

For both keywords, if the value you type is not a valid integer in the
allowed range, the workflow shows an inline error item instead of producing
garbage results.

**Installation**:

Go to https://github.com/MacHu-GWU/afwf_genpass-project/releases, download the latest ``Generate Secure Password.alfredworkflow`` file, double click to install.
