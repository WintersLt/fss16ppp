#!/usr/bin/python

import sys
from utest import ok, oks
import utest
import who1
import who2
sys.dont_write_bytecode=True

def add(a, b):
	return (a + b)

@ok
def _test_add1():
	'''Add two numbers'''
	assert add(2, 3) == 5, "equality failure"

oks()
