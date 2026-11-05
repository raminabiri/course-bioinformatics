#!/usr/bin/env python3
"""Summarise blastn hits against VFDB setA without awk/sort/uniq (part 08, module 02; Windows route).

Input: one or more tables from
    blastn ... -outfmt "6 qseqid qstart qend pident length slen stitle" -out ISOLATE.vfdb.tsv
The first table is the REFERENCE (for example isoC = K-12).

For every table the script keeps hits with  length / slen >= MINCOV  (each hit on its own, as in the Linux
lesson), takes the gene name (2nd field of the "~~~"-separated title) and writes ISOLATE.vf.txt.
It then prints:
  1. the number of genes per isolate,
  2. the virulence categories (VFC) of the reference hits,
  3. the genes found in each isolate but NOT in the reference,
and writes vf_specific_matrix.tsv (1/0 table of those genes; open it in Excel).

Usage:  python3 vfdb_summary.py [--mincov 0.8] isoC.vfdb.tsv isoD.vfdb.tsv isoE.vfdb.tsv
Works the same on Windows (py vfdb_summary.py ...) and Linux. Standard library only.
"""
import os
import re
import sys
from collections import Counter

args = sys.argv[1:]
mincov = 0.8
if args[:1] == ["--mincov"]:
    mincov, args = float(args[1]), args[2:]
if not args:
    sys.exit(__doc__)

genes, categories = {}, {}
for path in args:
    name = os.path.basename(path).split(".")[0]
    found, cats = set(), Counter()
    for line in open(path, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if int(f[4]) / int(f[5]) < mincov:
            continue
        found.add(f[6].split("~~~")[1])
        m = re.search(r" - ([^\]]*\(VFC\d+\))\]", f[6])
        if m:
            cats[m.group(1)] += 1
    genes[name], categories[name] = found, cats
    with open(os.path.join(os.path.dirname(path), name + ".vf.txt"), "w", encoding="utf-8") as out:
        out.write("".join(g + "\n" for g in sorted(found)))

ref = list(genes)[0]
print(f"== genes with coverage >= {mincov:g} (written to <isolate>.vf.txt)")
for name, found in genes.items():
    print(f"{name}\t{len(found)}")

print(f"\n== categories of {ref} hits (rows, not unique genes)")
for cat, n in categories[ref].most_common():
    print(f"{n:5d}  {cat}")

specific = []
print(f"\n== genes not in {ref}")
for name, found in genes.items():
    if name == ref:
        continue
    extra = sorted(found - genes[ref])
    print(f"{name}\t{', '.join(extra) if extra else '-'}")
    specific += [g for g in extra if g not in specific]

with open("vf_specific_matrix.tsv", "w", encoding="utf-8") as out:
    out.write("gene\t" + "\t".join(genes) + "\n")
    for g in specific:
        out.write(g + "\t" + "\t".join("1" if g in genes[n] else "0" for n in genes) + "\n")
print("\nwritten: vf_specific_matrix.tsv")
