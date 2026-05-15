# -*- coding: utf-8 -*-

import random

import afwf.api as afwf

from .constants import (
    charset_alpha,
    charset_digits,
    charset_lower,
    charset_list,
    charset_symbols,
    charset_upper,
    default_length,
    max_length,
    min_length,
    msg_autocomplete,
    msg_enter_password,
    msg_invalid_length_value,
    n_password,
)


def is_valid_password(password: str) -> bool:
    has_lower = len(set(password).intersection(charset_lower)) > 0
    has_upper = len(set(password).intersection(charset_upper)) > 0
    has_digits = len(set(password).intersection(charset_digits)) > 0
    has_symbol = len(set(password).intersection(charset_symbols)) > 0
    startswith_alpha = password[0] in charset_alpha
    return has_lower and has_upper and has_digits and has_symbol and startswith_alpha


def random_password(length: int) -> str:
    password = "".join([random.choice(charset_list) for _ in range(length)])
    if not is_valid_password(password):
        return random_password(length)
    return password


def gen_passwords(length: int) -> afwf.ScriptFilter:
    """
    Given an integer ``length`` in ``[min_length, max_length]``, return a
    ``ScriptFilter`` containing ``n_password`` freshly generated passwords.
    """
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
    """
    Alfred Script Filter entry point.

    ``query`` must be a string that parses as an integer in
    ``[min_length, max_length]``. Anything else returns an error item.
    """
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
