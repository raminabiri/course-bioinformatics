#!/usr/bin/env python3
"""Data for module 06/04 (16S amplicon), like 06_Metagenomics/99_scripts_data/04_16S_Amplicon/data/download.sh,
with Python only (Windows route; stdlib only). About 53 MB.

Reads: QIIME 2 "Atacama soil microbiome" tutorial, 1% subsample (EMP paired-end, 16S V4, 515F/806R).
Reference: SILVA 138 (99%) trimmed to 515F/806R, prepared by the QIIME 2 team.
Usage (in the folder where you want ./data, e.g. $HOME\\amplicon):
    py get_16s_data.py
"""
import hashlib
import os
import urllib.request

Q = "https://data.qiime2.org/2024.10"
FILES = {
    "raw/forward.fastq.gz": (f"{Q}/tutorials/atacama-soils/1p/forward.fastq.gz", "b5ee4718605158e5db91ef906fb61f62"),
    "raw/reverse.fastq.gz": (f"{Q}/tutorials/atacama-soils/1p/reverse.fastq.gz", "2ac4ca47f39ebc9f517396c051257342"),
    "raw/barcodes.fastq.gz": (f"{Q}/tutorials/atacama-soils/1p/barcodes.fastq.gz", "df32df8dc627319d7bc1d9ce49b89849"),
    "sample_metadata.tsv": (f"{Q}/tutorials/atacama-soils/sample_metadata.tsv", "380b04ad294f043b283ada11f42c011f"),
    "db/silva-138-99-seqs-515-806.qza": (f"{Q}/common/silva-138-99-seqs-515-806.qza", "a914837bc3f8964b156a9653e2420d22"),
    "db/silva-138-99-tax-515-806.qza": (f"{Q}/common/silva-138-99-tax-515-806.qza", "e2c40ae4c60cbf75e24312bb24652f2c"),
}

bad = 0
for rel, (url, md5) in FILES.items():
    out = os.path.join("data", *rel.split("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        print(f"downloading {rel} ...")
        req = urllib.request.Request(url, headers={"User-Agent": "course-download"})
        with urllib.request.urlopen(req, timeout=300) as response, open(out, "wb") as fh:
            fh.write(response.read())
    got = hashlib.md5(open(out, "rb").read()).hexdigest()
    status = "OK" if got == md5 else "FAILED (delete the file and run again)"
    bad += got != md5
    print(f"{rel}: {status}")
print("Done: data\\raw, data\\sample_metadata.tsv, data\\db" if not bad else f"{bad} file(s) failed the check")
