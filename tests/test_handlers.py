# -*- coding: utf-8 -*-

import unittest
from workflow import Workflow3
from afwf_genpass.handlers import handler, MSG_ENTER_DATETIME, DEFAULT_LENGTH, MSG_INVALID_LENGTH


class Test(unittest.TestCase):
    def test_generate_password(self):
        wf = Workflow3()
        handler(wf, args=["12", ])
        for item in wf._items:
            assert len(item.arg) == 12
            assert item.title == item.arg

    def test_no_argument(self):
        wf = Workflow3()
        handler(wf, args=[])
        assert len(wf._items) == 1
        item = wf._items[0]
        assert item.title == MSG_ENTER_DATETIME
        assert item.autocomplete == DEFAULT_LENGTH

    def test_invalid_argument(self):
        wf = Workflow3()
        handler(wf, args=["InValid", ])
        assert len(wf._items) == 1
        item = wf._items[0]
        assert "is NOT a valid length" in item.title

        wf = Workflow3()
        handler(wf, args=["Hello", "World"])
        assert len(wf._items) == 1
        item = wf._items[0]
        assert item.title == "`Hello World` is NOT a valid length!"

    def test_invalid_argument_value(self):
        cases = [
            ["6", ],
            ["100", ],
        ]
        for args in cases:
            wf = Workflow3()
            handler(wf, args=args)
            assert len(wf._items) == 1
            item = wf._items[0]
            assert item.title == MSG_INVALID_LENGTH


if __name__ == '__main__':
    unittest.main()
