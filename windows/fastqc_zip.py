#!/usr/bin/env python3
"""Read FastQC .zip reports without unzip/grep (Windows route, works on any system).

Usage:
    py fastqc_zip.py summary <folder>                      every line that is not PASS, per report
    py fastqc_zip.py module <report.zip> "<module>" [N]    first N data lines of one module (default all)

Examples:
    py fastqc_zip.py summary qc\\fastqc_raw
    py fastqc_zip.py module qc\\fastqc_raw\\minigut_R1_fastqc.zip "Per base sequence quality" 5
Same output as  unzip -p X_fastqc.zip X_fastqc/summary.txt | grep -v PASS
and             unzip -p X_fastqc.zip X_fastqc/fastqc_data.txt | grep -A N '>>Module'
"""
import glob
import os
import sys
import zipfile


def read_member(zip_path, member):
    """Text of one file inside a FastQC zip (the zip holds one folder named like the zip)."""
    name = os.path.basename(zip_path)[:-4]
    return zipfile.ZipFile(zip_path).read(f"{name}/{member}").decode()


if len(sys.argv) >= 3 and sys.argv[1] == "summary":
    for z in sorted(glob.glob(os.path.join(sys.argv[2], "*_fastqc.zip"))):
        print("==", os.path.basename(z)[:-4])
        for line in read_member(z, "summary.txt").splitlines():
            if not line.startswith("PASS"):
                print(line)
elif len(sys.argv) >= 4 and sys.argv[1] == "module":
    wanted = ">>" + sys.argv[3]
    limit = int(sys.argv[4]) if len(sys.argv) > 4 else None
    shown, inside = 0, False
    for line in read_member(sys.argv[2], "fastqc_data.txt").splitlines():
        if line.startswith(wanted):
            inside = True
        elif inside and line.startswith(">>END_MODULE"):
            break
        if inside:
            print(line)
            if not line.startswith(">>") and not line.startswith("#"):
                shown += 1
                if limit is not None and shown >= limit:
                    break
else:
    sys.exit(__doc__)
