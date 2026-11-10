#!/usr/bin/env python3
"""A drug's ChEMBL record and mechanism of action (Windows route; stdlib only).

Same information as the two `curl … | python3 -c` commands of module 09/02.
Usage:
    py chembl_info.py <preferred name>        e.g.  py chembl_info.py rifampin
ChEMBL's preferred names are INN/USAN names in upper case (RIFAMPIN, not rifampicin); the search ignores case.
The ChEMBL API is sometimes slow: the script waits up to 3 minutes per request.
"""
import json
import sys
import urllib.parse
import urllib.request

API = "https://www.ebi.ac.uk/chembl/api/data"
if len(sys.argv) != 2:
    sys.exit(__doc__)
name = urllib.parse.quote(sys.argv[1])
found = json.load(urllib.request.urlopen(f"{API}/molecule.json?pref_name__iexact={name}", timeout=180))["molecules"]
if not found:
    sys.exit(f"no ChEMBL molecule with preferred name {sys.argv[1]!r}")
m = found[0]
print(m["molecule_chembl_id"], m["pref_name"], "max_phase", m["max_phase"], "first_approval", m["first_approval"],
      "ATC", m["atc_classifications"], "oral", m["oral"])
p = m["molecule_properties"]
print({k: p[k] for k in ["full_mwt", "alogp", "hbd", "hba", "rtb", "psa", "num_ro5_violations"]})
mech = json.load(urllib.request.urlopen(f"{API}/mechanism.json?molecule_chembl_id={m['molecule_chembl_id']}", timeout=180))
for x in mech["mechanisms"]:
    print(x["mechanism_of_action"], x["target_chembl_id"], x["action_type"])
