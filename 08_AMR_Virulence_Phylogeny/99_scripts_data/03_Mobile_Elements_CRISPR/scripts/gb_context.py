#!/usr/bin/env python3
"""Mobile elements of a plasmid record and the genes next to them, from the annotation alone
(part 08, module 03; Windows route; the Linux lesson uses AMRFinderPlus + gene_context.py instead).

Usage:
  python3 gb_context.py RECORD.gb                     # list mobile_element features (IS, transposons)
  python3 gb_context.py RECORD.gb DIST GENE [GENE...] # CDS whose /gene is GENE, and elements within DIST bp

RECORD may be GenBank (.gb, .gbk) or EMBL (.embl). Gene names are those of the record's annotation
(case-insensitive), which may be older than the names AMRFinderPlus uses (for example oxa1 = blaOXA-1).
A GENE that occurs in several CDS (such as bla) gives one block per CDS.
Output (tab-separated): gene, product, gene_pos, element, element_pos, distance (0 = overlapping).
Needs Biopython; works the same on Windows (py gb_context.py ...) and Linux.
"""
import sys

from Bio import SeqIO

if len(sys.argv) < 2:
    sys.exit(__doc__)
path = sys.argv[1]
fmt = "embl" if path.lower().endswith(".embl") else "genbank"
record = SeqIO.read(path, fmt)


def span(feature):
    return int(feature.location.start) + 1, int(feature.location.end)     # 1-based, as in the record


elements = []
for f in record.features:
    if f.type == "mobile_element":
        name = f.qualifiers.get("mobile_element_type", ["?"])[0].split(":")[-1]
        elements.append((*span(f), name))

if len(sys.argv) < 4:
    print("start\tend\telement")
    for start, end, name in elements:
        print(f"{start}\t{end}\t{name}")
    sys.exit()

dist = int(sys.argv[2])
wanted = [g.lower() for g in sys.argv[3:]]
print("gene\tproduct\tgene_pos\telement\telement_pos\tdistance")
for f in record.features:
    gene = f.qualifiers.get("gene", [""])[0]
    if f.type != "CDS" or gene.lower() not in wanted:
        continue
    g_start, g_end = span(f)
    product = f.qualifiers.get("product", ["-"])[0]
    for e_start, e_end, name in elements:
        d = max(0, e_start - g_end, g_start - e_end)
        if d <= dist:
            print(f"{gene}\t{product}\t{g_start}-{g_end}\t{name}\t{e_start}-{e_end}\t{d}")
