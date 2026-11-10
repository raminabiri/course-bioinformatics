#!/usr/bin/env python3
"""Pairwise SNP distance matrix from a FASTA alignment, like `snp-dists` (Windows route; stdlib only).

Counts, for every pair of sequences, the positions where both have A/C/G/T and they differ
(gaps '-' and N/ambiguous bases are ignored, as snp-dists does by default).
Usage:
    py snp_dists.py core.aln > distances.tsv
"""
import sys

if len(sys.argv) != 2:
    sys.exit(__doc__)

names, seqs = [], []
with open(sys.argv[1]) as fh:
    for line in fh:
        line = line.strip()
        if line.startswith(">"):
            names.append(line[1:].split()[0])
            seqs.append([])
        elif line:
            seqs[-1].append(line.upper())
seqs = ["".join(s) for s in seqs]
if len({len(s) for s in seqs}) > 1:
    sys.exit("sequences have different lengths: is this an alignment?")

ACGT = set("ACGT")
# keep only columns that vary, to make the pairwise loop fast on long alignments
cols = [i for i in range(len(seqs[0])) if len({s[i] for s in seqs} & ACGT) > 1]
short = ["".join(s[i] for i in cols) for s in seqs]

print("snp_dists.py\t" + "\t".join(names))
for a, sa in zip(names, short):
    row = []
    for sb in short:
        row.append(str(sum(1 for x, y in zip(sa, sb) if x != y and x in ACGT and y in ACGT)))
    print(a + "\t" + "\t".join(row))
