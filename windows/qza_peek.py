#!/usr/bin/env python3
"""Look inside QIIME 2 artifacts (.qza) and visualizations (.qzv) without QIIME 2.

A .qza/.qzv file is a zip archive: <uuid>/metadata.yaml, <uuid>/data/<files>, <uuid>/provenance/...
Windows route of the course (stdlib only; works on any system).

Usage:
    py qza_peek.py <file.qza>                  list the data files inside
    py qza_peek.py <file.qza> <name> [N]       print the first N lines (default 20) of data/<name>
    py qza_peek.py <file.qza> <name> 0 <out>   save data/<name> to the file <out>
Examples:
    py qza_peek.py taxonomy.qza
    py qza_peek.py taxonomy.qza taxonomy.tsv 5
    py qza_peek.py rep-seqs.qza dna-sequences.fasta 0 rep-seqs.fasta
"""
import sys
import zipfile

if len(sys.argv) < 2:
    sys.exit(__doc__)
z = zipfile.ZipFile(sys.argv[1])
data = [n for n in z.namelist() if "/data/" in n and not n.endswith("/")]
if len(sys.argv) == 2:
    uuid = z.namelist()[0].split("/")[0]
    meta = z.read(f"{uuid}/metadata.yaml").decode()
    print(meta.strip())
    for n in data:
        print(f"{z.getinfo(n).file_size:>12,}  {n.split('/data/', 1)[1]}")
    sys.exit(0)
name = sys.argv[2]
match = [n for n in data if n.split("/data/", 1)[1] == name]
if not match:
    sys.exit(f"no data/{name} in {sys.argv[1]}; run without a name to list the files")
text = z.read(match[0])
if len(sys.argv) > 4:
    with open(sys.argv[4], "wb") as fh:
        fh.write(text)
    print(f"saved {len(text):,} bytes to {sys.argv[4]}")
else:
    n_lines = int(sys.argv[3]) if len(sys.argv) > 3 else 20
    for line in text.decode().splitlines()[:n_lines]:
        print(line)
