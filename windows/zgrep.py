#!/usr/bin/env python3
"""Search text files, also gzip-compressed ones, like `zcat file.gz | grep -E PATTERN` (Windows route; stdlib only).

Usage:
    py zgrep.py PATTERN FILE [FILE ...] [-m N] [-c] [-v]
      PATTERN   a regular expression (Python re), e.g. "^ATOM" or "^ATOM|^HETATM"
      -m N      stop after N matching lines per file   (grep -m N)
      -c        print only the number of matching lines (grep -c)
      -v        lines that do NOT match               (grep -v)
Examples:
    py zgrep.py "^ATOM" 5UAC.cif.gz -m 2
    py zgrep.py "^ATOM|^HETATM" 5UAC.cif.gz -c
"""
import gzip
import re
import sys

args = sys.argv[1:]
max_n = None
count = invert = False
if "-m" in args:
    i = args.index("-m")
    max_n = int(args[i + 1])
    del args[i:i + 2]
if "-c" in args:
    count = True
    args.remove("-c")
if "-v" in args:
    invert = True
    args.remove("-v")
if len(args) < 2:
    sys.exit(__doc__)

pattern = re.compile(args[0])
for path in args[1:]:
    opener = gzip.open if path.endswith(".gz") else open
    n = 0
    with opener(path, "rt", errors="replace") as fh:
        for line in fh:
            if bool(pattern.search(line)) != invert:
                n += 1
                if not count:
                    prefix = f"{path}:" if len(args) > 2 else ""
                    print(prefix + line.rstrip("\r\n"))
                if max_n is not None and n >= max_n:
                    break
    if count:
        print(f"{path}:{n}" if len(args) > 2 else n)
