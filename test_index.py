#!/usr/bin/env python3.5

# pylint: disable=too-many-public-methods
# pylint: disable=missing-docstring
# pylint: disable=line-too-long
# pylint: disable=protected-access
# pylint: disable=superfluous-parens


import unittest

import index


class IndexTestCase(unittest.TestCase):

    def test_process_line(self):
        line = '<p><div align=left><u>optional procedure:</u>&nbsp;&nbsp;<tt>(<a name="%_idx_632"></a>transcript-on<i> filename</i>)</tt>&nbsp;</div>'
        expected = (
            "transcript-on",
            "./r5rs-Z-H-9.html#%_idx_632",
        )
        actual = index._process_line(line)
        self.assertEqual(expected, actual)

        line = '<p><div align=left><u>library procedure:</u>&nbsp;&nbsp;<tt>(<a name="%_idx_506"></a>string&lt;?<i> <i>string<sub>1</sub></i> <i>string<sub>2</sub></i></i>)</tt>&nbsp;</div>'
        expected = (
            "string<?",
            "./r5rs-Z-H-9.html#%_idx_506",
        )
        actual = index._process_line(line)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main(verbosity=2)
