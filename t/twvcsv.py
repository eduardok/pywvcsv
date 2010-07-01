from wvtest import *
import wvcsv
from wvcsv import _wvcsv

import sys

@wvtest
def test_quote():
    WVPASSEQ(wvcsv.quote(None), "")
    WVPASSEQ(wvcsv.quote("test"), "test")
    WVPASSEQ(wvcsv.quote("t,est"), '"t,est"')
    WVPASSEQ(wvcsv.quote('t,e"st'), '"t,e""st"')

@wvtest
def test_dequote():
    WVPASSEQ(wvcsv.dequote(""), None)
    WVPASSEQ(wvcsv.dequote('test'), 'test')
    WVPASSEQ(wvcsv.dequote('"te,st"'), 'te,st')
    WVPASSEQ(wvcsv.dequote('"te,""st"'), 'te,"st')

    WVPASSEQ(wvcsv.dequote(wvcsv.quote('"foo,"bar,')), '"foo,"bar,')

@wvtest
def test_splitline():
    WVPASSEQ(_wvcsv.splitline(","), (None, None))
    WVPASSEQ(_wvcsv.splitline(",def"), (None, 'def'))
    WVPASSEQ(_wvcsv.splitline("abc,def"), ('abc', 'def'))
    WVPASSEQ(_wvcsv.splitline('"abc,",def'), ('abc,', 'def'))
    WVPASSEQ(_wvcsv.splitline('"a""bc,",def'), ('a"bc,', 'def'))
    WVPASSEQ(_wvcsv.splitline('"a""bc,",",def"'), ('a"bc,', ',def'))
    WVPASSEQ(_wvcsv.splitline('"a""bc,",",def"""'), ('a"bc,', ',def"'))
    WVPASSEQ(_wvcsv.splitline('"a""bc,",,",def"""'), ('a"bc,', None, ',def"'))

@wvtest
def test_getline_from_memory():
    r = wvcsv.Reader("ABCDEFG,efgh\n\"a\nbcd\",1234")
    i = iter(r)
    WVPASSEQ(i.next(), ('ABCDEFG','efgh'))
    WVPASSEQ(i.next(), ('a\nbcd','1234'))
    try:
        i.next()
        WVFAIL("i.next() should have thrown StopIteration")
    except StopIteration:
        WVPASS("wvcsv.Reader iterator throws StopIteration correctly")

@wvtest
def test_getline_from_file():
    r = wvcsv.Reader(open("data/test.csv"))
    i = iter(r)
    WVPASSEQ(i.next(), ('abc','def'))
    WVPASSEQ(i.next(), ('ghi', 'j\nkl'))
    WVPASSEQ(i.next(), ('1234', '5678'))
    WVPASSEQ(i.next(), (None,))
    WVPASSEQ(i.next(), ('9', '10'))
    try:
        i.next()
        WVFAIL("i.next() should have thrown StopIteration")
    except StopIteration:
        WVPASS("wvcsv.Reader iterator throws StopIteration correctly")
