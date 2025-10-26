
__version__ = "0.2.1"
from .core import compress_block, decompress_block, CompressedBlock
from .entropy import calculate_entropy
from .strategies import (
    STRATEGY_RAW, STRATEGY_RLE, STRATEGY_DICT, STRATEGY_DELTA, STRATEGY_HYBRID
)

__all__ = [
    "compress_block", "decompress_block", "CompressedBlock",
    "calculate_entropy",
    "STRATEGY_RAW", "STRATEGY_RLE", "STRATEGY_DICT", "STRATEGY_DELTA", "STRATEGY_HYBRID"
]
