# small helpers (if you want to extend)
def hexdump(b: bytes, sep: str = " ") -> str:
    return sep.join(f"{x:02X}" for x in b)
