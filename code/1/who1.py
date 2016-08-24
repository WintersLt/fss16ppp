#!/usr/bin/python

from utest import ok

def remove_vowels(s):
    ''' Remove all vowels from a string'''
    vowels = ['a', 'e', 'i', 'o', 'u']
    return ''.join([l for l in s if l not in vowels]);

@ok
def _who1_test1(): 
    '''All vowels from lowercase string should be removed'''
    assert remove_vowels("vowels") == "vwls", "equality failure"

@ok
def _who1_test2(): 
    '''All vowels from the uppercase string should be removed'''
    assert remove_vowels("VOWELS") == "vwls", "equality failure"
