#!/usr/bin/env python2.7

import functools
import hashlib
import itertools
import multiprocessing
import os
import string
import sys

# Constants

ALPHABET    = string.ascii_lowercase + string.digits
ARGUMENTS   = sys.argv[1:]
CORES       = 1
HASHES      = 'hashes.txt'
LENGTH      = 1
PREFIX      = ''

# Functions

def usage(exit_code=0):
    print '''Usage: {} [-a alphabet -c CORES -l LENGTH -p PATH -s HASHES]
    -a ALPHABET Alphabet to use in permutations
    -c CORES    CPU Cores to use
    -l LENGTH   Length of permutations
    -p PREFIX   Prefix for all permutations
    -s HASHES   Path of hashes file'''.format(os.path.basename(sys.argv[0]))
    sys.exit(exit_code)

def md5sum(s):
    ''' Generate MD5 digest for given string.

    >>> md5sum('abc')
    '900150983cd24fb0d6963f7d28e17f72'

    >>> md5sum('wake me up inside')
    '223a947ce000ce88e263a4357cca2b4b'
    '''
    # TODO: Implement

    h = hashlib.md5()
    h.update(s)
    return h.hexdigest()

def permutations(length, alphabet=ALPHABET):
    ''' Yield all permutations of alphabet up to provided length.

    >>> list(permutations(1, 'ab'))
    ['a', 'b']

    >>> list(permutations(2, 'ab'))
    ['aa', 'ab', 'ba', 'bb']

    >>> list(permutations(1))       # doctest: +ELLIPSIS
    ['a', 'b', ..., '9']

    >>> list(permutations(2))       # doctest: +ELLIPSIS
    ['aa', 'ab', ..., '99']
    '''
    # TODO: Implement as a generator
    
    if length == 1:
        for a in alphabet:
            yield a
    else:
        for a in alphabet:
            for p in permutations(length-1, alphabet):
                yield a + p

def smash(hashes, length, alphabet=ALPHABET, prefix=''):
    ''' Return all password permutations of specified length that are in hashes

    >>> smash([md5sum('ab')], 2)
    ['ab']

    >>> smash([md5sum('abc')], 2, prefix='a')
    ['abc']

    >>> smash(map(md5sum, 'abc'), 1, 'abc')
    ['a', 'b', 'c']
    '''
    # TODO: Implement

    #return [ prefix + p for h in hashes for p in permutations(length, alphabet) if h == md5sum(prefix+p) ]

    return [ prefix + p for p in permutations(length, alphabet) if md5sum(prefix+p) in hashes ]


# Main Execution

if __name__ == '__main__':
    # TODO: Parse command line arguments
    
    while len(ARGUMENTS) and ARGUMENTS[0].startswith('-') and len(ARGUMENTS[0]) > 1:
        ARG = ARGUMENTS.pop(0)
        if ARG == '-a':
            ALPHABET = ARGUMENTS.pop(0)
        elif ARG == '-c':
            CORES = int(ARGUMENTS.pop(0))
        elif ARG == '-l':
            LENGTH = int(ARGUMENTS.pop(0))
        elif ARG == '-p':
            PREFIX = ARGUMENTS.pop(0)
        elif ARG == '-s':
            HASHES = ARGUMENTS.pop(0)
        elif ARG == '-h':
            usage()
        else:
            usage(1)

    # TODO: Load hashes set
    hashes = set()
    for h in open(HASHES):
        hashes.add(h.strip()) 

    # TODO: Execute smash function to get passwords

    if  CORES > 1 and LENGTH > 1:
        pool = multiprocessing.Pool(CORES)
        subL = (LENGTH/4) + 1
        subsmash = functools.partial(smash, hashes, LENGTH - subL, ALPHABET) 
        passwords = itertools.chain.from_iterable(pool.imap(subsmash, [PREFIX + x for x in permutations(subL, ALPHABET)]))
            

    else:
        passwords = smash(hashes, LENGTH, ALPHABET, PREFIX)

    # TODO: Print passwords
    for password in passwords:
        print password

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
