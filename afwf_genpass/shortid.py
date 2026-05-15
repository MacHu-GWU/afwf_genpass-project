# -*- coding: utf-8 -*-

import secrets

import afwf.api as afwf

from .constants import (
    msg_enter_shortid,
    msg_shortid_autocomplete,
    msg_shortid_invalid_length_value,
    n_shortid,
    shortid_charset,
    shortid_default_length,
    shortid_max_length,
    shortid_min_length,
)


def gen_shortid(length: int) -> str:
    """
    Generate a single YouTube-style random short ID of ``length`` characters.

    Uses ``secrets.choice`` for cryptographic strength. The 57-char charset is
    base62 minus visually-confusing characters (``0/O/o`` and ``1/l/I``), so
    IDs survive being read aloud or hand-copied without ambiguity.
    """
    return "".join(secrets.choice(shortid_charset) for _ in range(length))


def gen_shortids(length: int) -> afwf.ScriptFilter:
    """
    Given an integer ``length`` in
    ``[shortid_min_length, shortid_max_length]``, return a ``ScriptFilter``
    containing ``n_shortid`` freshly generated short IDs.
    """
    sf = afwf.ScriptFilter()
    for _ in range(n_shortid):
        sid = gen_shortid(length)
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
        subtitle=msg_shortid_autocomplete,
        autocomplete=str(shortid_default_length),
        valid=True,
    )
    item.icon = afwf.Icon.from_image_file(path=afwf.IconFileEnum.error)
    return afwf.ScriptFilter(items=[item])


def main(query: str) -> afwf.ScriptFilter:
    """
    Alfred Script Filter entry point.

    ``query`` must be a string that parses as an integer in
    ``[shortid_min_length, shortid_max_length]``. Anything else returns an
    error item.
    """
    query = query.strip()

    if not query:
        item = afwf.Item(
            title=msg_enter_shortid,
            subtitle=msg_shortid_autocomplete,
            autocomplete=str(shortid_default_length),
            valid=True,
        )
        return afwf.ScriptFilter(items=[item])

    try:
        length = int(query)
    except ValueError:
        return _invalid_length_sf(f"`{query}` is NOT a valid length!")

    if shortid_min_length <= length <= shortid_max_length:
        return gen_shortids(length)

    return _invalid_length_sf(msg_shortid_invalid_length_value)
