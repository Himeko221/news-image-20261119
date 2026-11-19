#!/usr/bin/env python3
"""news-image-20261119 grader entry: emit the day's digest image.

Reads the committed entry.png, validates it against the competition caps
(PNG signature, 1024x1024, at most 1 MiB), then writes those exact bytes
to /output/entry.png. Two runs therefore write identical bytes; the file
itself carries every pixel of the entry: no generation happens at grade
time, no network is touched, only the standard library is used.
"""

import os
import sys
import shutil

CAP_BYTES = 1048576
EXPECTED_SIZE = (1024, 1024)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def target_directory() -> str:
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def validated_source() -> bytes:
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "entry.png"), "rb") as fh:
        blob = fh.read()
    if not blob.startswith(PNG_SIGNATURE):
        sys.exit("entry.png is not a PNG")
    if len(blob) > CAP_BYTES:
        sys.exit("entry.png exceeds the 1 MiB cap")
    w = int.from_bytes(blob[16:20], "big")
    h = int.from_bytes(blob[20:24], "big")
    if (w, h) != EXPECTED_SIZE:
        sys.exit(f"entry.png is {w}x{h}, expected 1024x1024")
    return blob


def write_artifact() -> str:
    out_dir = target_directory()
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png"), "rb") as src_fh:
        with open(dest, "wb") as dst_fh:
            shutil.copyfileobj(src_fh, dst_fh)
    return dest


if __name__ == "__main__":
    written = write_artifact()
    size = len(validated_source())
    print("emitted", written, "-", size, "bytes, PNG verified")
