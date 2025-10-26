import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from qpac.core import compress_block, decompress_block
from qpac import STRATEGY_HYBRID

def test_roundtrip_random():
    import os
    data = os.urandom(64)
    cb = compress_block(data)
    out = decompress_block(cb)
    assert out == data

def test_roundtrip_sample():
    sample = bytes([
        1,1,1,1,2,2,3,3,3,3,3,3,4,5,6,7,
        1,1,1,1,2,2,3,3,3,3,3,3,4,5,6,7,
        1,1,1,1,2,2,3,3,3,3,3,3,4,5,6,7,
        9,9,9,9,9,9,8,8,8,7,6,5,4,3,2,1
    ])
    cb = compress_block(sample, try_hybrid=True)
    out = decompress_block(cb)
    assert out == sample

def test_hybrid_roundtrip():
    # craft data where hybrid likely helps
    sample = bytes([1]*20 + [2]*20 + [3]*24)
    cb = compress_block(sample, try_hybrid=True)
    # ensure it sometimes picks hybrid or others, but always roundtrips
    out = decompress_block(cb)
    assert out == sample
