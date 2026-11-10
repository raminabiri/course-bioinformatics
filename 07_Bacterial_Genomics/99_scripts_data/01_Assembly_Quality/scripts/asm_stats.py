#!/usr/bin/env python3
"""Assembly statistics without seqkit or QUAST (part 07, module 01).

Summary: contigs, total length, largest, N50, L50, GC%, and NG50/LG50 when --gsize is given.
Per-contig table (--table): name, length, GC%, and coverage if the header has it
(Shovill "cov=32.7" or SPAdes "NODE_1_length_263154_cov_8.9"). Open the table in Excel.

Usage: python3 asm_stats.py contigs.fa [--minlen 500] [--gsize 4641652] [--table contigs.tsv]
Standard library only (runs the same on Windows: py asm_stats.py ...).
"""
import argparse
import re


def read_fasta(path):
    name, parts = None, []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(parts)
                name, parts = line[1:], []
            elif line:
                parts.append(line.upper())
    if name is not None:
        yield name, "".join(parts)


def nx(lengths, target):
    """Length and rank of the contig at which the running sum reaches target (N50 / NG50)."""
    run = 0
    for i, x in enumerate(sorted(lengths, reverse=True), 1):
        run += x
        if run >= target:
            return x, i
    return 0, 0  # assembly shorter than half the genome: NG50 undefined


def gc(s):
    acgt = sum(s.count(b) for b in "ACGT")
    return 100 * (s.count("G") + s.count("C")) / acgt if acgt else 0.0


def coverage(header):
    m = re.search(r"cov[=_]([0-9.]+)", header)
    return m.group(1).rstrip(".") if m else ""


ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("fasta")
ap.add_argument("--minlen", type=int, default=0, help="ignore contigs shorter than this (QUAST default: 500)")
ap.add_argument("--gsize", type=int, help="expected genome size in bases, for NG50")
ap.add_argument("--table", help="write a per-contig TSV (name, length, GC, cov)")
args = ap.parse_args()

contigs = [(h, s) for h, s in read_fasta(args.fasta) if len(s) >= args.minlen]
lengths = [len(s) for _, s in contigs]
total = sum(lengths)
n50, l50 = nx(lengths, total / 2)
print(f"file: {args.fasta}  minlen: {args.minlen}")
print(f"contigs: {len(lengths)}  total: {total}  largest: {max(lengths)}  N50: {n50}  L50: {l50}  "
      f"GC%: {gc(''.join(s for _, s in contigs)):.2f}")
if args.gsize:
    ng50, lg50 = nx(lengths, args.gsize / 2)
    print(f"genome size: {args.gsize}  assembly/genome: {total / args.gsize:.3f}  NG50: {ng50}  LG50: {lg50}")
if args.table:
    with open(args.table, "w", newline="\n") as out:  # same bytes on Windows
        out.write("contig\tlength\tGC\tcov\n")
        for h, s in sorted(contigs, key=lambda c: -len(c[1])):
            out.write(f"{h.split()[0]}\t{len(s)}\t{gc(s):.1f}\t{coverage(h)}\n")
    print(f"written: {args.table}")
