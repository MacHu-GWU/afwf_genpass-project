# -*- coding: utf-8 -*-

import string

charset_upper: set[str] = set(string.ascii_uppercase)
charset_lower: set[str] = set(string.ascii_lowercase)
charset_alpha: set[str] = set.union(charset_upper, charset_lower)
charset_digits: set[str] = set(string.digits)
# allowed symbols in password
charset_symbols: set[str] = set("!%@#&^*")
# banned characters that are hard to visually distinguish
charset_banned: set[str] = set("1lIoO0")

charset: set[str] = set.union(
    charset_upper,
    charset_lower,
    charset_digits,
    charset_symbols,
).difference(charset_banned)
charset_list: list[str] = list(charset)

min_length = 8
default_length = 12
max_length = 32
n_password = 8

msg_enter_password = f"Enter password length ({min_length} <= length <= {max_length}): "
msg_autocomplete = f"Hit 'Tab' to use {default_length} characters"
msg_invalid_length_value = (
    f"Password Length has to be between {min_length} and {max_length}!"
)

# ------------------------------------------------------------------------------
# Short ID (YouTube-style) — 57-char URL-safe charset:
#   base62 minus visually confusing characters
#     digits: drop 0 (like O/o), drop 1 (like l)            → 2-9        (8)
#     lowercase: drop l (like 1), drop o (like 0)           → 24 chars
#     uppercase: drop O (like 0)                            → 25 chars
# ------------------------------------------------------------------------------
id_charset: str = (
    "23456789"
    "abcdefghijkmnpqrstuvwxyz"
    "ABCDEFGHIJKLMNPQRSTUVWXYZ"
)

id_min_length = 6
id_default_length = 16
id_max_length = 32
n_id = 8

msg_enter_id = (
    f"Enter ID length "
    f"({id_min_length} <= length <= {id_max_length}): "
)
msg_id_autocomplete = (
    f"Hit 'Tab' to use {id_default_length} characters"
)
msg_id_invalid_length_value = (
    f"ID Length has to be between {id_min_length} and {id_max_length}!"
)
