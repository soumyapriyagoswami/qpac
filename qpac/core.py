"""
Main wrapper: compress_block and decompress_block
Stores a small header (strategy, original_size, compressed_size) in a simple container class.
"""

from dataclasses import dataclass
from typing import Tuple
from .strategies import (
    STRATEGY_RAW, STRATEGY_RLE, STRATEGY_DICT, STRATEGY_DELTA, STRATEGY_HYBRID,
    rle_compress, rle_decompress,
    delta_compress, delta_decompress,
    dict_compress, dict_decompress,
    hybrid_compress, hybrid_decompress
)
from .entropy import calculate_entropy

@dataclass
class CompressedBlock:
    strategy: int
    original_size: int
    compressed_size: int
    data: bytes

def compress_block(block: bytes, try_hybrid: bool = True, entropy_gpu: bool = False) -> CompressedBlock:
    """
    Compress a single block (bytes). Returns CompressedBlock with chosen strategy.
    - try_hybrid: If True, also tries hybrid RLE+DICT.
    - entropy_gpu: If True, attempt to compute entropy on GPU (CuPy) with fallback.
    """
    if not isinstance(block, (bytes, bytearray)):
        raise TypeError("block must be bytes-like")

    orig_size = len(block)
    # default best = raw
    best_data = bytes(block)
    best_strategy = STRATEGY_RAW

    # entropy
    entropy = calculate_entropy(block, use_gpu=entropy_gpu)

    # RLE
    rle_out = rle_compress(block)
    if len(rle_out) < len(best_data):
        best_data = rle_out
        best_strategy = STRATEGY_RLE

    # Delta: only for low entropy numeric-like sequences
    if entropy < 4.0:
        delta_out = delta_compress(block)
        if len(delta_out) < len(best_data):
            best_data = delta_out
            best_strategy = STRATEGY_DELTA

    # Dict
    dict_out = dict_compress(block)
    if len(dict_out) < len(best_data):
        best_data = dict_out
        best_strategy = STRATEGY_DICT

    # Hybrid
    if try_hybrid:
        hybrid_out, _ = hybrid_compress(block)
        if len(hybrid_out) < len(best_data):
            best_data = hybrid_out
            best_strategy = STRATEGY_HYBRID

    return CompressedBlock(
        strategy=best_strategy,
        original_size=orig_size,
        compressed_size=len(best_data),
        data=best_data
    )

def decompress_block(cb: CompressedBlock) -> bytes:
    """
    Reverse compress_block. For hybrid, attempts both decoding orders (as compress
    picks the smaller between rle(dict(...)) and dict(rle(...))).
    """
    s = cb.strategy
    data = cb.data
    if s == STRATEGY_RAW:
        return data
    elif s == STRATEGY_RLE:
        return rle_decompress(data)
    elif s == STRATEGY_DELTA:
        return delta_decompress(data)
    elif s == STRATEGY_DICT:
        return dict_decompress(data)
    elif s == STRATEGY_HYBRID:
        return hybrid_decompress(data)
    else:
        raise ValueError(f"Unknown strategy {s}")

# Demo CLI when run as module
if __name__ == "__main__":
    sample = bytes([
        1,1,1,1,2,2,3,3,3,3,3,3,4,5,6,7,
        1,1,1,1,2,2,3,3,3,3,3,3,4,5,6,7,
        1,1,1,1,2,2,3,3,3,3,3,3,4,5,6,7,
        9,9,9,9,9,9,8,8,8,7,6,5,4,3,2,1
    ])

    print("Original size:", len(sample))
    cb = compress_block(sample, try_hybrid=True)
    print(f"Used strategy: {cb.strategy}, compressed size: {cb.compressed_size}")
    decompressed = decompress_block(cb)
    print("Roundtrip ok:", decompressed == sample)
    # hex dump
    print("Data hex:", " ".join(f"{b:02X}" for b in cb.data))
