"""Minimal NBT / region-file reader (no dependencies): rd(), chunk_nbt(), region_chunks(path) yields chunk compounds."""
import gzip, struct, zlib

# ---- minimal NBT reader (only what chunks need)
def rd(buf, pos, t):
    if t == 1: return struct.unpack_from(">b", buf, pos)[0], pos + 1
    if t == 2: return struct.unpack_from(">h", buf, pos)[0], pos + 2
    if t == 3: return struct.unpack_from(">i", buf, pos)[0], pos + 4
    if t == 4: return struct.unpack_from(">q", buf, pos)[0], pos + 8
    if t == 5: return struct.unpack_from(">f", buf, pos)[0], pos + 4
    if t == 6: return struct.unpack_from(">d", buf, pos)[0], pos + 8
    if t == 7:
        n = struct.unpack_from(">i", buf, pos)[0]; return None, pos + 4 + n
    if t == 8:
        n = struct.unpack_from(">H", buf, pos)[0]; return buf[pos + 2:pos + 2 + n].decode("utf-8", "replace"), pos + 2 + n
    if t == 9:
        it = buf[pos]; n = struct.unpack_from(">i", buf, pos + 1)[0]; pos += 5; out = []
        for _ in range(n):
            v, pos = rd(buf, pos, it); out.append(v)
        return out, pos
    if t == 10:
        d = {}
        while True:
            it = buf[pos]; pos += 1
            if it == 0: return d, pos
            n = struct.unpack_from(">H", buf, pos)[0]; k = buf[pos + 2:pos + 2 + n].decode("utf-8", "replace"); pos += 2 + n
            d[k], pos = rd(buf, pos, it)
    if t == 11:
        n = struct.unpack_from(">i", buf, pos)[0]; return None, pos + 4 + 4 * n
    if t == 12:
        n = struct.unpack_from(">i", buf, pos)[0]; return None, pos + 4 + 8 * n
    raise ValueError("bad tag %d" % t)


def chunk_nbt(raw, comp):
    data = zlib.decompress(raw) if comp == 2 else gzip.decompress(raw) if comp == 1 else raw
    if data[0] != 10: return None
    n = struct.unpack_from(">H", data, 1)[0]
    d, _ = rd(data, 3 + n, 10)
    return d


def region_chunks(path):
    with open(path, "rb") as f:
        head = f.read(4096)
        for i in range(1024):
            off = int.from_bytes(head[i * 4:i * 4 + 3], "big")
            if not off: continue
            f.seek(off * 4096)
            ln, comp = struct.unpack(">iB", f.read(5))
            try:
                nbt = chunk_nbt(f.read(ln - 1), comp)
            except Exception:
                continue
            if nbt: yield nbt


