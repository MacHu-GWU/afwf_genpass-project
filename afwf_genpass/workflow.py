# -*- coding: utf-8 -*-

import afwf

from .handlers import (
    genpass,
)

wf = afwf.Workflow()
wf.register(genpass.handler)
