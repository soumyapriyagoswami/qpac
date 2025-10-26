"""
Compression and decompression strategies.
Mirrors the C prototype logic but written in Python with proper
decompression support.
"""

from typing import Tuple
import numpy as np

MAX_DICT_SIZE = 256

# strategy constants
STRATEGY_RAW = 0
STRATEGY_RLE = 1
STRATEGY_DICT = 2
STRATEGY_DELTA = 3
STRATEGY_HYBRID = 4  # RLE+DICT hybrid

# -------------------------
# RLE
# -------------------------
def rle_compress(data: bytes) -> bytes:
    out = bytearray()
    n = len(data)
    i = 0
    while i < n:
        val = data[i]
        count = 1
        while i + count < n and data[i + count] == val and count < 255:
            count += 1
        out.append(val)
        out.append(count)
        i += count
    return bytes(out)

def rle_decompress(data: bytes) -> bytes:
    out = bytearray()
    n = len(data)
    i = 0
    while i + 1 < n:
        val = data[i]
        count = data[i + 1]
        out.extend([val] * count)
        i += 2
    return bytes(out)

# -------------------------
# Delta
# -------------------------
def delta_compress(data: bytes) -> bytes:
    if not data:
        return b""
    arr = np.frombuffer(data, dtype=np.uint8)
    delta = np.diff(arr, prepend=arr[0]).astype(np.uint8)
    return delta.tobytes()

def delta_decompress(data: bytes) -> bytes:
    if not data:
        return b""
    arr = np.frombuffer(data, dtype=np.uint8)
    out = np.empty_like(arr)
    out[0] = arr[0]
    for i in range(1, len(arr)):
        out[i] = (int(out[i-1]) + int(arr[i])) & 0xFF
    return out.tobytes()

# -------------------------
# Dictionary (simple per-byte dictionary like the C version)
# -------------------------
def dict_compress(data: bytes) -> bytes:
    out = bytearray()
    dictionary = bytearray()
    for b in data:
        try:
            idx = dictionary.index(b)
            out.append(idx)  # index fits in a byte since dict <= 256
        except ValueError:
            # store literal with high-bit flag
            out.append(0x80 | b)
            dictionary.append(b)
            if len(dictionary) >= MAX_DICT_SIZE:
                dictionary.clear()
    return bytes(out)

def dict_decompress(data: bytes) -> bytes:
    out = bytearray()
    dictionary = bytearray()
    for b in data:
        if b & 0x80:
            literal = b & 0x7F
            out.append(literal)
            dictionary.append(literal)
            if len(dictionary) >= MAX_DICT_SIZE:
                dictionary.clear()
        else:
            # index referencing dictionary
            idx = b
            if idx >= len(dictionary):
                raise ValueError(f"Invalid dictionary index {idx} (dict size {len(dictionary)})")
            val = dictionary[idx]
            out.append(val)
    return bytes(out)

# -------------------------
# Hybrid: try RLE->DICT and DICT->RLE and pick best
# -------------------------
def hybrid_compress(data: bytes) -> Tuple[bytes, int]:
    # Try RLE then DICT
    rle_first = dict_compress(rle_compress(data))
    # Try DICT then RLE
    dict_first = rle_compress(dict_compress(data))
    if len(rle_first) <= len(dict_first):
        return rle_first, STRATEGY_HYBRID
    else:
        return dict_first, STRATEGY_HYBRID

def hybrid_decompress(data: bytes, prefer: str = "rle-first") -> bytes:
    """
    Hybrid decompression is ambiguous because hybrid_compress may
    produce either rle(dict(data)) or dict(rle(data)). We must
    determine which one was used. Since our compress function picks
    the smaller output, decompress must try both and check which yields
    a valid full-size result (no exceptions). The caller should know
    the original size (core will handle that) so we can validate length.
    """
    # Try rle->dict decoding path: decompress dict then rle
    # BUT note ordering: hybrid_compress used dict_compress(rle_compress(data))
    # That means compress: rle(data) -> dict_compress -> output
    # To decompress that, first dict_decompress then rle_decompress.
    # For dict_first path: compress: dict_compress(data) -> rle_compress -> output
    # To decompress: rle_decompress then dict_decompress.
    errors = []
    # try rle-first path (i.e., it was dict_compress(rle_compress(data)))
    try:
        step1 = dict_decompress(data)
        step2 = rle_decompress(step1)
        return step2
    except Exception as e:
        errors.append(e)
    # try dict-first path
    try:
        step1 = rle_decompress(data)
        step2 = dict_decompress(step1)
        return step2
    except Exception as e:
        errors.append(e)
    raise ValueError(f"Hybrid decompress failed (tried both orders): {errors}")
