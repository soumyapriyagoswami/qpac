

# QPAC: Quantum-Inspired Pattern-Aware Compression

[![PyPI](https://img.shields.io/pypi/v/qpac)](https://pypi.org/project/qpac/)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)  

**QPAC** (Quantum-Inspired Pattern-Aware Compression) is a Python library for hybrid entropy-aware compression of data. Inspired by **LZ4**, it supports multiple compression strategies and can adaptively choose the best method for each block of data.  

---

## Features

- **Hybrid Compression**: Automatically selects between raw, RLE, dictionary, delta, and hybrid strategies.  
- **Entropy-Guided**: Compression decisions are guided by Shannon entropy to maximize efficiency.  
- **Fast and Lightweight**: Designed for small blocks (e.g., IoT or memory-constrained environments).  
- **Reversible**: Supports both compression and decompression for data integrity.  
- **Extensible**: Easily add custom compression strategies.

---

## Installation

### From PyPI (Test)
```bash
pip install -i https://test.pypi.org/simple qpac
```
### From PyPI (Production)
```bash
pip install qpac

```
### Usage
```bash
import qpac
from qpac import compress_block, decompress_block, CompressedBlock

# Sample data
data = bytearray([1,1,1,2,2,3,3,3,4,5,6,7,8])

# Compress
cb: CompressedBlock = compress_block(data)
print(f"Original size: {cb.original_size}")
print(f"Used strategy: {cb.strategy}, compressed size: {cb.compressed_size}")

# Decompress
decompressed = decompress_block(cb)
print(f"Roundtrip ok: {decompressed == data}")

```

## API Reference

### `compress_block(block: bytes) -> CompressedBlock`
Compresses a block of data using the most appropriate strategy based on entropy and patterns.

### `decompress_block(cb: CompressedBlock) -> bytes`
Reverses the compression and returns the original data.

### `CompressedBlock`
Represents a compressed block with the following attributes:

- `strategy`: Compression strategy used  
- `original_size`: Original block size  
- `compressed_size`: Compressed size  
- `data`: Compressed byte array  

### Entropy

#### `calculate_entropy(data: bytes) -> float`
Calculates the Shannon entropy of a data block.

---

## Compression Strategies

| Strategy        | Description                                          |
|-----------------|------------------------------------------------------|
| `STRATEGY_RAW`  | No compression; stores original data                |
| `STRATEGY_RLE`  | Run-length encoding for repeated patterns           |
| `STRATEGY_DICT` | Dictionary-based compression                        |
| `STRATEGY_DELTA`| Delta encoding for numerical sequences              |
| `STRATEGY_HYBRID` | Adaptive combination based on entropy             |
---

## License

This project is licensed under the **MIT License** © Soumyapriya Goswami.  
For full license details, see the [LICENSE](LICENSE) file.

---

## References

- **LZ4 Compression:** [https://lz4.github.io/lz4/](https://lz4.github.io/lz4/)  
- **Shannon Entropy:** C. E. Shannon, *A Mathematical Theory of Communication*, 1948

---

## Contact

**Soumyapriya Goswami**  
📧 Email: [email@Soumyapriya.com](mailto:soumyapriya.goswami.it2023@kgec.ac.in)  
💻 Project Repository: [GitHub](https://github.com/soumyapriyagoswami/qpac.git)


