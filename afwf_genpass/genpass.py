# -*- coding: utf-8 -*-

"""
Random password generator and its Alfred Script Filter entry point.

Charset design:

- ``lowercase + uppercase + digits + symbols`` (``!%@#&^*``)
- minus visually-confusing characters: ``0``, ``1``, ``l``, ``I``, ``o``, ``O``

Policy: every accepted password must contain at least one character from each
of the four classes (lower, upper, digit, symbol) and must start with a letter
— hand-typeable, mixed-class, and unambiguous when read aloud.
"""

import random

import afwf.api as afwf

from .constants import charset_alpha
from .constants import charset_digits
from .constants import charset_lower
from .constants import charset_list
from .constants import charset_symbols
from .constants import charset_upper
from .constants import default_length
from .constants import max_length
from .constants import min_length
from .constants import msg_autocomplete
from .constants import msg_enter_password
from .constants import msg_invalid_length_value
from .constants import n_password


def is_valid_password(password: str) -> bool:
    """Check that ``password`` satisfies the four-class + starts-with-letter policy."""
    has_lower = len(set(password).intersection(charset_lower)) > 0
    has_upper = len(set(password).intersection(charset_upper)) > 0
    has_digits = len(set(password).intersection(charset_digits)) > 0
    has_symbol = len(set(password).intersection(charset_symbols)) > 0
    startswith_alpha = password[0] in charset_alpha
    return has_lower and has_upper and has_digits and has_symbol and startswith_alpha


def random_password(length: int) -> str:
    """Generate one random password of ``length`` chars; retries until valid."""
    password = "".join([random.choice(charset_list) for _ in range(length)])
    if not is_valid_password(password):
        return random_password(length)
    return password


def gen_passwords(length: int) -> afwf.ScriptFilter:
    """Return a ``ScriptFilter`` of ``n_password`` fresh passwords of ``length``."""
    sf = afwf.ScriptFilter()
    for _ in range(n_password):
        password = random_password(length)
        item = afwf.Item(
            title=password,
            subtitle="Hit 'Command + C' to copy",
            arg=password,
            valid=True,
        )
        sf.items.append(item)
    return sf


def _invalid_length_sf(title: str) -> afwf.ScriptFilter:
    item = afwf.Item(
        title=title,
        subtitle=msg_autocomplete,
        autocomplete=str(default_length),
        valid=True,
    )
    item.icon = afwf.Icon.from_image_file(path=afwf.IconFileEnum.error)
    return afwf.ScriptFilter(items=[item])


def main(query: str) -> afwf.ScriptFilter:
    """Alfred entry point. ``query`` parses as int in ``[min_length, max_length]``,
    otherwise an error item is shown."""
    query = query.strip()

    if not query:
        item = afwf.Item(
            title=msg_enter_password,
            subtitle=msg_autocomplete,
            autocomplete=str(default_length),
            valid=True,
        )
        return afwf.ScriptFilter(items=[item])

    try:
        length = int(query)
    except ValueError:
        return _invalid_length_sf(f"`{query}` is NOT a valid length!")

    if min_length <= length <= max_length:
        return gen_passwords(length)

    return _invalid_length_sf(msg_invalid_length_value)
