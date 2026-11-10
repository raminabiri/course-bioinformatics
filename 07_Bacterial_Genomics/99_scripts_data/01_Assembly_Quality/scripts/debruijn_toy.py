#!/usr/bin/env python3
"""A tiny de Bruijn graph, by hand: why a repeat breaks an assembly (part 07, module 01).

Each k-mer is an arrow from its first (k-1) bases to its last (k-1) bases. A node with more than one
different outgoing arrow is a fork: the assembler cannot know which way to go and stops the contig there.

Usage: python3 debruijn_toy.py [SEQUENCE] [--k 4 6 8 9]
Default sequence: ATGCGTACGTTAGCGTACGA (the 7-base repeat GCGTACG appears twice).
Standard library only (runs the same on Windows: py debruijn_toy.py).
"""
import argparse
from collections import defaultdict

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("seq", nargs="?", default="ATGCGTACGTTAGCGTACGA")
ap.add_argument("--k", type=int, nargs="+", default=[4, 6, 8, 9])
args = ap.parse_args()
seq = args.seq.upper()

print(f"sequence: {seq}  ({len(seq)} bases)")
print("k\tkmers\tdistinct\tforks (node -> next nodes)")
for k in args.k:
    kmers = [seq[i:i + k] for i in range(len(seq) - k + 1)]
    out = defaultdict(set)
    for km in kmers:
        out[km[:-1]].add(km[1:])
    forks = [f"{node} -> {{{', '.join(sorted(nxt))}}}" for node, nxt in sorted(out.items()) if len(nxt) > 1]
    print(f"{k}\t{len(kmers)}\t{len(set(kmers))}\t{'; '.join(forks) if forks else 'none (one path)'}")
