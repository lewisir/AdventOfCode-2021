# A pytest file to test functions in aoc08.py

import pytest
import aoc08

def test_stringSubtract():
    assert aoc08.stringSubtract("abc","ab") == "c"
    assert aoc08.stringSubtract("abc","c") == "ab"
    assert aoc08.stringSubtract("cdef","ab") == "cdef"
    assert aoc08.stringSubtract("cdef","abc") == "def"

def test_compareString():
    assert aoc08.compareStrings("abc","cdef") == "c"
    assert aoc08.compareStrings("ab","abc") == "ab"
    assert aoc08.compareStrings("cdef","ab") == ""

def test_extractDisplays():
    assert aoc08.extractDisplays(["acedgfb","cdfbe","gcdfa","fbcad","dab","cefabd","cdfgeb","eafb","cagedb","ab"],2) == ["ab"]
    assert aoc08.extractDisplays(["acedgfb","cdfbe","gcdfa","fbcad","dab","cefabd","cdfgeb","eafb","cagedb","ab"],3) == ["dab"]
    assert aoc08.extractDisplays(["acedgfb","cdfbe","gcdfa","fbcad","dab","cefabd","cdfgeb","eafb","cagedb","ab"],4) == ["eafb"]
    assert aoc08.extractDisplays(["acedgfb","cdfbe","gcdfa","fbcad","dab","cefabd","cdfgeb","eafb","cagedb","ab"],5) == ["cdfbe","gcdfa","fbcad"]
    assert aoc08.extractDisplays(["acedgfb","cdfbe","gcdfa","fbcad","dab","cefabd","cdfgeb","eafb","cagedb","ab"],6) == ["cefabd","cdfgeb","cagedb"]
    assert aoc08.extractDisplays(["acedgfb","cdfbe","gcdfa","fbcad","dab","cefabd","cdfgeb","eafb","cagedb","ab"],7) == ["acedgfb"]

