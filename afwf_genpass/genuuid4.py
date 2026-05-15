# -*- coding: utf-8 -*-

import uuid

import afwf.api as afwf

from .constants import n_uuid4


def gen_uuid4() -> str:
    """
    Generate a single random UUID4 in the canonical 8-4-4-4-12 lowercase hex
    form, e.g. ``550e8400-e29b-41d4-a716-446655440000``.
    """
    return str(uuid.uuid4())


def gen_uuid4s() -> afwf.ScriptFilter:
    """Return a ``ScriptFilter`` containing ``n_uuid4`` freshly generated UUID4s."""
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
    """
    Alfred Script Filter entry point.

    UUID4 has no parameters — each invocation simply returns ``n_uuid4``
    freshly generated UUID4s.
    """
    return gen_uuid4s()
