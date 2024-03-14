"""
tests of the Cython open file function

it is never called directly from Python, but the tests are here anyway
"""

from pathlib import Path
import pytest
import py_gd

OUTPUT_DIR = Path(__file__).parent / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


@pytest.mark.parametrize("filename", ["simple_ascii.txt",
                                      "file\u2014name_with_unicode.txt",  # u2014 is an EmDash])
                                      ])
def test_open_file(filename):
    """
    Can use full Unicode on all? filesystems
    """
    # write a test file

    contents = "Just a tiny bit of text\n"

    path = OUTPUT_DIR / filename
    with open(path, 'w', encoding="utf-8") as outfile:
        outfile.write(contents)

    # try to read it (which implies it could be opened)

    results = py_gd.py_gd._read_text_file(path, encoding="utf-8")

    assert results == contents

