# -*- coding: utf-8 -*-

"""
Random UUID4 generator and its Alfred Script Filter entry point.

UUID4 has a fixed RFC 4122 format (``8-4-4-4-12`` lowercase hex, 36 chars
incl. hyphens) so this module takes no length / charset configuration —
it always produces 122 bits of randomness via :func:`uuid.uuid4`.
"""

import uuid

import afwf.api as afwf

from .constants import n_uuid4


def gen_uuid4() -> str:
    """Generate one random UUID4 string, e.g. ``550e8400-e29b-41d4-a716-446655440000``."""
    return str(uuid.uuid4())


def gen_uuid4s() -> afwf.ScriptFilter:
    """Return a ``ScriptFilter`` of ``n_uuid4`` fresh UUID4s."""
    sf = afwf.ScriptFilter()
    for _ in range(n_uuid4):
        u = gen_uuid4()
        item = afwf.Item(
            title=u,
            subtitle="Hit 'Command + C' to copy",
            arg=u,
            valid=True,
        )
        sf.items.append(item)
    return sf


def main() -> afwf.ScriptFilter:
    """Alfred entry point. No parameters — returns ``n_uuid4`` fresh UUID4s."""
    return gen_uuid4s()
