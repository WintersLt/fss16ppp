#!/usr/bin/python

from utest import ok

def count_words(s):
    '''Count number of words in a sentence'''    
    return len(s.split(" "));

@ok
def _who2_test1(): 
    s = '''This is a fine sentence.'''
    assert count_words(s) == 5, "Count should be 5"

@ok
def _who2_test2(): 
    s = '''All vowels from the uppercase string should be removed'''
    assert count_words(s) == 8, "Count should be 9"
