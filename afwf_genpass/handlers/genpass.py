# -*- coding: utf-8 -*-

import typing as T
import afwf
import attr

import random
import string

charset_upper: T.Set[str] = set(string.ascii_uppercase)
charset_lower: T.Set[str] = set(string.ascii_lowercase)
charset_alpha: T.Set[str] = set.union(charset_upper, charset_lower)
charset_digits: T.Set[str] = set(string.digits)
charset_symbols: T.Set[str] = set("!%@#&^*")  # allowed symbols in password
charset_banned: T.Set[str] = set(
    "1lIoO0"
)  # banned characters that is hard to distinguish

charset: T.Set[str] = set.union(
    charset_upper,
    charset_lower,
    charset_digits,
    charset_symbols,
).difference(charset_banned)
charset_list: T.List[str] = list(charset)

min_length = 8
default_length = 12
max_length = 32
msg_enter_password = f"Enter password length ({min_length} <= length <= {max_length}): "
msg_autocomplete = f"Hit 'Tab' to use {default_length} characters"
msg_invalid_length_value = (
    f"Password Length has to be between {min_length} and {max_length}!"
)
n_password = 8

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


@attr.define
class Handler(afwf.Handler):
    def main(self, length: int) -> afwf.ScriptFilter:
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

    def handler(self, query: str) -> afwf.ScriptFilter:  # pragma: no cover
        q = afwf.QueryParser().parse(query)
        n_parts = len(q.trimmed_parts)

        sf = afwf.ScriptFilter()  # script filter for edge case
        if n_parts == 0:
            item = afwf.Item(
                title=msg_enter_password,
                subtitle=msg_autocomplete,
                autocomplete=str(default_length),
                valid=True,
            )
            sf.items.append(item)
            return sf

        elif n_parts == 1:
            try:
                length = int(q.trimmed_parts[0])
            except:
                item = afwf.Item(
                    title=f"`{q.trimmed_parts[0]}` is NOT a valid length!",
                    subtitle=msg_autocomplete,
                    autocomplete=str(default_length),
                    valid=True,
                )
                sf.items.append(item)
                item.set_icon(afwf.IconFileEnum.error)
                return sf

            if 8 <= length <= 32:
                return self.main(length=length)
            else:
                item = afwf.Item(
                    title=msg_invalid_length_value,
                    subtitle=msg_autocomplete,
                    autocomplete=str(default_length),
                    valid=True,
                )
                item.set_icon(afwf.IconFileEnum.error)
                sf.items.append(item)
                return sf
        else:
            item = afwf.Item(
                title=f"`{query}` is NOT a valid length!",
                subtitle=msg_autocomplete,
                autocomplete=str(default_length),
                valid=True,
            )
            item.set_icon(afwf.IconFileEnum.error)
            sf.items.append(item)
            return sf


handler = Handler(id="genpass")
