# -*- coding: utf-8 -*-

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
    """
    Generate a single YouTube-style random ID of ``length`` characters.

    Uses ``secrets.choice`` for cryptographic strength. The 57-char charset is
    base62 minus visually-confusing characters (``0/O/o`` and ``1/l``), so IDs
    survive being read aloud or hand-copied without ambiguity.
    """
    return "".join(secrets.choice(id_charset) for _ in range(length))


def gen_ids(length: int) -> afwf.ScriptFilter:
    """
    Given an integer ``length`` in ``[id_min_length, id_max_length]``, return a
    ``ScriptFilter`` containing ``n_id`` freshly generated short IDs.
    """
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
    """
    Alfred Script Filter entry point.

    ``query`` must be a string that parses as an integer in
    ``[id_min_length, id_max_length]``. Anything else returns an error item.
    """
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
