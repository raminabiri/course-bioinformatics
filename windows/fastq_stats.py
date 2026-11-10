#!/usr/bin/env python3
"""Simple statistics of FASTQ files (.fastq or .fastq.gz), like `seqkit stats -a -T` (a subset).

Windows route of the course (stdlib only; works on any system).
Usage:
    py fastq_stats.py raw\\minigut_R1.fastq.gz raw\\minigut_R2.fastq.gz ...
Prints a tab-separated table: file, reads, bases, min_len, avg_len, max_len, Q20(%), Q30(%), GC(%).
Q20/Q30 = percent of bases with Phred quality >= 20 / 30 (Sanger offset 33), as seqkit computes them.
"""
import gzip
import os
import sys

if len(sys.argv) < 2:
    sys.exit(__doc__)

print("file\treads\tbases\tmin_len\tavg_len\tmax_len\tQ20(%)\tQ30(%)\tGC(%)")
for path in sys.argv[1:]:
    opener = gzip.open if path.endswith(".gz") else open
    reads = bases = q20 = q30 = gc = 0
    min_len, max_len = None, 0
    with opener(path, "rt") as fh:
        for i, line in enumerate(fh):
            line = line.rstrip("\r\n")
            if i % 4 == 1:                       # sequence line
                n = len(line)
                reads += 1
                bases += n
                gc += line.count("G") + line.count("C") + line.count("g") + line.count("c")
                min_len = n if min_len is None else min(min_len, n)
                max_len = max(max_len, n)
            elif i % 4 == 3:                     # quality line
                for ch in line:
                    q = ord(ch) - 33
                    if q >= 20:
                        q20 += 1
                        if q >= 30:
                            q30 += 1
    if reads == 0:
        print(f"{os.path.basename(path)}\t0\t0\t0\t0\t0\t0\t0\t0")
        continue
    print(f"{os.path.basename(path)}\t{reads}\t{bases}\t{min_len}\t{bases / reads:.1f}\t{max_len}\t"
          f"{q20 / bases * 100:.2f}\t{q30 / bases * 100:.2f}\t{gc / bases * 100:.2f}")
