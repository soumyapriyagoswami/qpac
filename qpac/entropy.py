"""
Entropy helpers. Supports optional GPU calculation with CuPy if available.
"""

from typing import Optional
import numpy as np

def _entropy_from_probs(probs: np.ndarray) -> float:
    # Only positive probs
    p = probs[probs > 0]
    return -float((p * np.log2(p)).sum())

def calculate_entropy(data: bytes, use_gpu: Optional[bool] = False) -> float:
    """
    Calculate Shannon entropy of `data` (bytes).
    If use_gpu=True and CuPy is available, uses GPU; otherwise uses NumPy CPU.
    """
    if not data:
        return 0.0

    # Try GPU route
    if use_gpu:
        try:
            import cupy as cp
            arr = cp.frombuffer(data, dtype=cp.uint8)
            # bincount in cupy; ensure length 256
            freq = cp.bincount(arr, minlength=256).astype(cp.float64)
            probs = freq / arr.size
            # compute entropy on GPU then move to CPU
            p = probs[probs > 0]
            # cp.log2 -> sum -> item()
            ent = -float((p * cp.log2(p)).sum().item())
            return ent
        except Exception:
            # If anything goes wrong, fall back to CPU silently
            pass

    # CPU fallback
    arr = np.frombuffer(data, dtype=np.uint8)
    freq = np.bincount(arr, minlength=256).astype(np.float64)
    probs = freq / arr.size
    return _entropy_from_probs(probs)
