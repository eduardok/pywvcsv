from wvtest import *
from wvcsv import *

import sys

@wvtest
def test_quote():
    WVPASSEQ(csvquote(None), "")
    WVPASSEQ(csvquote("test"), "test")
    WVPASSEQ(csvquote("t,est"), '"t,est"')
    WVPASSEQ(csvquote('t,e"st'), '"t,e""st"')

@wvtest
def test_dequote():
    WVPASSEQ(csvdequote(""), None)
    WVPASSEQ(csvdequote('test'), 'test')
    WVPASSEQ(csvdequote('"te,st"'), 'te,st')
    WVPASSEQ(csvdequote('"te,""st"'), 'te,"st')

    WVPASSEQ(csvdequote(csvquote('"foo,"bar,')), '"foo,"bar,')

@wvtest
def test_splitline():
    WVPASSEQ(csvsplitline(","), (None, None))
    WVPASSEQ(csvsplitline(",def"), (None, 'def'))
    WVPASSEQ(csvsplitline("abc,def"), ('abc', 'def'))
    WVPASSEQ(csvsplitline('"abc,",def'), ('abc,', 'def'))
    WVPASSEQ(csvsplitline('"a""bc,",def'), ('a"bc,', 'def'))
    WVPASSEQ(csvsplitline('"a""bc,",",def"'), ('a"bc,', ',def'))
    WVPASSEQ(csvsplitline('"a""bc,",",def"""'), ('a"bc,', ',def"'))
    WVPASSEQ(csvsplitline('"a""bc,",,",def"""'), ('a"bc,', None, ',def"'))

@wvtest
def test_getline_from_memory():
    r = CsvReader("ABCDEFG,efgh\n\"a\nbcd\",1234")
    i = iter(r)
    WVPASSEQ(i.next(), "ABCDEFG,efgh")
    WVPASSEQ(i.next(), '"a\nbcd",1234')
    try:
        i.next()
        WVFAIL("i.next() should have thrown StopIteration")
    except StopIteration:
        WVPASS("CsvReader iterator throws StopIteration correctly")

@wvtest
def test_getline_from_file():
    r = CsvReader(open("t/data/test.csv"))
    i = iter(r)
    WVPASSEQ(i.next(), "abc,def")
    WVPASSEQ(i.next(), 'ghi,"j\nkl"')
    WVPASSEQ(i.next(), '1234,5678')
    WVPASSEQ(i.next(), '')
    WVPASSEQ(i.next(), "9,10")
    try:
        i.next()
        WVFAIL("i.next() should have thrown StopIteration")
    except StopIteration:
        WVPASS("CsvReader iterator throws StopIteration correctly")
