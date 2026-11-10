#!/usr/bin/env python3
"""Download the small read data of part 01 (two simulated gut samples) and the human chr21 region.

The same files that 01_Linux/99_scripts_data/data/download.sh gets with curl, but with Python only,
so it works on Windows without Linux tools. Run get_k12_genome.py for the E. coli genome.

Usage (in the folder where you want the files, e.g. $HOME\\course):
    py get_part01_data.py
Writes fastq\\minigut_R1.fastq.gz, ..._R2, minigut_sample2_R1/R2 and host_chr21_region.fa,
copies ground_truth.tsv from the course folder if it can find it, and prints MD5 checksums.
"""
import hashlib
import os
import shutil
import urllib.request

MIRRORS = ["https://raw.githubusercontent.com/nf-core/test-datasets/mag/",
           "https://cdn.jsdelivr.net/gh/nf-core/test-datasets@mag/"]

FILES = [(f"test_data/test_{s}_{r}.fastq.gz", os.path.join("fastq", f"{s}_{r}.fastq.gz"))
         for s in ["minigut", "minigut_sample2"] for r in ["R1", "R2"]]
FILES.append(("host_reference/genome.hg38.chr21_10000bp_region.fa", "host_chr21_region.fa"))


def download(path, out):
    """Try each mirror in turn; return True when the file was saved."""
    for base in MIRRORS:
        try:
            with urllib.request.urlopen(base + path, timeout=120) as response:
                data = response.read()
            with open(out, "wb") as fh:
                fh.write(data)
            return True
        except OSError as err:
            print(f"  {base} failed: {err}")
    return False


os.makedirs("fastq", exist_ok=True)
for path, out in FILES:
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        print(f"downloading {out} ...")
        if not download(path, out):
            print(f"could not download {out}; try again later")
            continue
    md5 = hashlib.md5(open(out, "rb").read()).hexdigest()
    print(f"{md5}  {out}  ({os.path.getsize(out):,} bytes)")

# ground_truth.tsv is part of the course itself (01_Linux/99_scripts_data/data)
here = os.path.dirname(os.path.abspath(__file__))
truth = os.path.join(here, "..", "01_Linux", "99_scripts_data", "data", "ground_truth.tsv")
if os.path.exists(truth) and not os.path.exists("ground_truth.tsv"):
    shutil.copy(truth, "ground_truth.tsv")
    print("copied ground_truth.tsv")
