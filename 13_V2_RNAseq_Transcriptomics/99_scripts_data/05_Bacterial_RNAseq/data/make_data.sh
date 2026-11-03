#!/usr/bin/env bash
# Data of module 13/05: E. coli K-12 MG1655 genome + annotation (NCBI RefSeq GCF_000005845.2) and 6 simulated
# stranded single-end RNA-seq samples (ctrl_1..3, cip_1..3) with a known answer (SOS response).
# Usage (inside conda activate rnaseq):   bash make_data.sh ~/rnaseq/ecoli
# Output: ref/ecoli.fa, ref/ecoli.gff   reads/<sample>.fastq.gz (400 000 reads each), reads/truth.tsv, reads/genes.tsv
# About 30 MB; seed 13, so everybody gets the same reads.
set -euo pipefail
OUT=${1:-$HOME/rnaseq/ecoli}
HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$OUT/ref" && cd "$OUT"
B=https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2
curl -sS -o ref/genomic.fna.gz "${B}_genomic.fna.gz"
curl -sS -o ref/genomic.gff.gz "${B}_genomic.gff.gz"
python3 "$HERE/../scripts/simulate_bacterial.py" ref/genomic.fna.gz ref/genomic.gff.gz reads
gunzip -c ref/genomic.fna.gz > ref/ecoli.fa
gunzip -c ref/genomic.gff.gz > ref/ecoli.gff
md5sum reads/truth.tsv; gunzip -c reads/ctrl_1.fastq.gz | md5sum     # content (the .gz header holds a date)
echo "Done: $OUT/ref and $OUT/reads"
