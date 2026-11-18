#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261117.

The entry image (entry.png beside this file) sums up the world news of
Tuesday 17 November 2026 in one frame. This program copies it to the
output directory: /output in the grader's container, or the directory
named by MAKEFUN_OUTPUT_DIR outside it. Standard library only, no
network, byte-for-byte the same output on every run.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # the gate's 1 MiB limit


def main() -> None:
    data = SOURCE.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise SystemExit("entry.png is not a PNG file")
    if len(data) > MAX_BYTES:
        raise SystemExit("entry.png exceeds the 1 MiB gate limit")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, out_dir / "entry.png")


if __name__ == "__main__":
    main()
