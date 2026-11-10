#!/usr/bin/env python3
"""Get CID, SMILES and formula of compounds by name from PubChem PUG REST, into a CSV (Windows route; stdlib only).

Same file as the curl loop of module 09/02 (name,CID,SMILES,MolecularFormula), with a 0.3 s pause between
requests (PubChem asks for at most 5 requests per second).
Usage:
    py pubchem_csv.py out.csv "name 1" "name 2" ...
Example:
    py pubchem_csv.py rif.csv rifampicin rifabutin rifapentine rifaximin "rifamycin SV" ciprofloxacin trimethoprim ampicillin
"""
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name"
if len(sys.argv) < 3:
    sys.exit(__doc__)
out_file, names = sys.argv[1], sys.argv[2:]
with open(out_file, "w", newline="\n") as out:
    out.write("name,CID,SMILES,MolecularFormula\n")
    for n in names:
        url = f"{PUG}/{urllib.parse.quote(n)}/property/SMILES,MolecularFormula/CSV"
        try:
            rows = urllib.request.urlopen(url, timeout=60).read().decode().splitlines()[1:]
        except urllib.error.HTTPError as err:
            print(f"{n}: PubChem said {err.code} (name not found?)", file=sys.stderr)
            continue
        for r in rows:
            out.write(f'"{n}",{r}\n')
        time.sleep(0.3)
print(f"wrote {out_file}")
