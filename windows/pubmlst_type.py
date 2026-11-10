#!/usr/bin/env python3
"""MLST typing of an assembly through the PubMLST REST API (Windows route; stdlib only).

Sends the FASTA (one genome: all its contigs) to PubMLST, which finds exact allele matches
and the sequence type (ST). The output line looks like the one of the `mlst` program.
Internet needed; one genome takes about 1-2 minutes for a 5 Mb genome.

Usage:
    py pubmlst_type.py <genome.fasta> [database]
    py pubmlst_type.py --list            seqdef databases that have an MLST scheme
Default database: pubmlst_ecoli_achtman_seqdef (E. coli, Achtman 7-gene scheme).
Examples of other databases: pubmlst_saureus_seqdef, pubmlst_abaumannii_seqdef, pubmlst_campylobacter_seqdef.
"""
import json
import os
import sys
import urllib.error
import urllib.request

API = "https://rest.pubmlst.org/db"


def get(url):
    try:
        with urllib.request.urlopen(url, timeout=120) as r:
            return json.load(r)
    except urllib.error.HTTPError as err:
        sys.exit(f"PubMLST said {err.code} for {url} (check the database name with --list)")


if len(sys.argv) < 2:
    sys.exit(__doc__)
if sys.argv[1] == "--list":
    for group in get(API):
        for db in group["databases"]:
            if db["name"].endswith("_seqdef"):
                print(f"{db['name']:45s} {db['description']}")
    sys.exit(0)

fasta, db = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "pubmlst_ecoli_achtman_seqdef")
schemes = get(f"{API}/{db}/schemes")["schemes"]
mlst = [s for s in schemes if s["description"].upper() == "MLST"] or schemes
scheme_url = mlst[0]["scheme"]
text = open(fasta).read()
req = urllib.request.Request(scheme_url + "/sequence", data=json.dumps({"sequence": text}).encode(),
                             headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=600) as r:
        result = json.load(r)
except urllib.error.HTTPError as err:
    sys.exit(f"PubMLST said {err.code}: {err.read()[:300].decode(errors='replace')}")

alleles = []
for locus, hits in sorted(result.get("exact_matches", {}).items()):
    short = locus.split("_")[-1]
    alleles.append(f"{short}({','.join(h['allele_id'] for h in hits)})")
st = result.get("fields", {}).get("ST", "-")
cc = result.get("fields", {}).get("clonal_complex", "")
print("\t".join([os.path.basename(fasta), db, st] + alleles + ([cc] if cc else [])))
if not alleles:
    print("no exact allele match: check the database, or the assembly may be partial", file=sys.stderr)
