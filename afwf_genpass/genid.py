# -*- coding: utf-8 -*-

"""
YouTube-style random short-ID generator and its Alfred Script Filter entry point.

Charset design: 57 URL-safe characters — ``base62`` minus visually-confusing
``0`` / ``1`` / ``l`` / ``o`` / ``O`` (capital ``I`` is **kept**). Cryptographically
strong via :func:`secrets.choice`; suitable as opaque IDs in URLs, filenames,
slugs, etc. Survives being read aloud or hand-copied without ambiguity.
"""

import secrets

import afwf.api as afwf

from .constants import id_charset
from .constants import id_default_length
from .constants import id_max_length
from .constants import id_min_length
from .constants import msg_enter_id
from .constants import msg_id_autocomplete
from .constants import msg_id_invalid_length_value
from .constants import n_id


def gen_id(length: int) -> str:
    """Generate one random short ID of ``length`` chars from the module charset."""
    return "".join(secrets.choice(id_charset) for _ in range(length))


def gen_ids(length: int) -> afwf.ScriptFilter:
    """Return a ``ScriptFilter`` of ``n_id`` fresh short IDs of ``length``."""
    sf = afwf.ScriptFilter()
    for _ in range(n_id):
        sid = gen_id(length)
        item = afwf.Item(
            title=sid,
            subtitle="Hit 'Command + C' to copy",
            arg=sid,
            valid=True,
        )
        sf.items.append(item)
    return sf


def _invalid_length_sf(title: str) -> afwf.ScriptFilter:
    item = afwf.Item(
        title=title,
        subtitle=msg_id_autocomplete,
        autocomplete=str(id_default_length),
        valid=True,
    )
    item.icon = afwf.Icon.from_image_file(path=afwf.IconFileEnum.error)
    return afwf.ScriptFilter(items=[item])


def main(query: str) -> afwf.ScriptFilter:
    """Alfred entry point. ``query`` parses as int in ``[id_min_length, id_max_length]``,
    otherwise an error item is shown."""
    query = query.strip()

    if not query:
        item = afwf.Item(
            title=msg_enter_id,
            subtitle=msg_id_autocomplete,
            autocomplete=str(id_default_length),
            valid=True,
        )
        return afwf.ScriptFilter(items=[item])

    try:
        length = int(query)
    except ValueError:
        return _invalid_length_sf(f"`{query}` is NOT a valid length!")

    if id_min_length <= length <= id_max_length:
        return gen_ids(length)

    return _invalid_length_sf(msg_id_invalid_length_value)
