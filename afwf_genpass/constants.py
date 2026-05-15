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
