#!/usr/bin/env python3
"""Count reads by their true origin, read from the read name (simulated course data only).

The course's simulated reads carry their source in the name: NC_006347.1_..., NC_000913.3_...,
HUMAN_chr21_..., HUMAN_chr1_... This script counts them, like
    zcat f.fastq.gz | awk 'NR%4==1' | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\\1/' | sort | uniq -c
Windows route of the course (stdlib only; works on any system).

Usage:
    py read_origins.py <reads.fastq.gz> [more files ...]
"""
import gzip
import re
import sys
from collections import Counter

if len(sys.argv) < 2:
    sys.exit(__doc__)
pattern = re.compile(r"^@?(HUMAN_chr[0-9]+|N[CZ]_[0-9A-Z.]+)")
for path in sys.argv[1:]:
    opener = gzip.open if path.endswith(".gz") else open
    counts = Counter()
    with opener(path, "rt") as fh:
        for i, line in enumerate(fh):
            if i % 4 == 0:
                m = pattern.match(line)
                counts[m.group(1) if m else "other"] += 1
    print("==", path)
    for origin, n in sorted(counts.items()):
        print(f"{n:>8} {origin}")
