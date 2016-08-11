#!/usr/bin/env python3.5

# pylint: disable=superfluous-parens
# pylint: disable=missing-docstring
# pylint: disable=invalid-name

from collections import namedtuple
import os
import re
import sqlite3

Index = namedtuple("Index", "name path")

LINE_RE = re.compile("""
.*
name="(?P<anchor>.*)"
.*
</a>(?P<name>.*)<i>
""",
                     re.VERBOSE)
"""HTML index file line pattern."""

INDEX_FILE = "docSet.dsidx"
PROCEDURE_FILE = "r5rs-Z-H-9.html"
RESOURCES_DIR = "./Contents/Resources"


def _is_procedure_line(l):
    return "procedure:" in l


def _get_name(s):
    return s.partition("<i>")[0] \
            .replace("&lt;", "<") \
            .replace("&gt;", ">")


def _get_path(anchor):
    return "./%s#%s" % (PROCEDURE_FILE, anchor)


def _process_line(l):
    result = LINE_RE.match(l)
    if result:
        return Index(
            _get_name(result.group("name")),
            _get_path(result.group("anchor"))
        )


def _get_insert(index):
    return "INSERT OR IGNORE INTO searchIndex('name', 'type', 'path') VALUES ('%s', 'Procedure', '%s');" % \
        (index.name, index.path)


def _main():
    index_file_path = os.path.join(RESOURCES_DIR, INDEX_FILE)
    try:
        os.remove(index_file_path)
    except:  # pylint: disable=bare-except
        pass
    conn = sqlite3.connect(index_file_path)
    with conn, open(os.path.join(RESOURCES_DIR, "Documents", PROCEDURE_FILE)) as f:
        conn.execute("CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);")
        conn.execute("CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);")
        for l in f:
            if _is_procedure_line(l):
                index = _process_line(l)
                if index:
                    conn.execute(_get_insert(index))


if __name__ == "__main__":
    _main()
