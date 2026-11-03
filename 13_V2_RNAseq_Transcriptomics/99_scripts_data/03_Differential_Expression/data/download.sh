#!/usr/bin/env bash
# Real data for modules 13/03 and 13/04: GSE52778 (Himes et al. 2014), about 9 MB.
# Usage:   bash download.sh ~/rnaseq/gse
#   GSE52778_series_matrix.txt.gz  sample table (GEO, as in 11/04)
#   counts.tsv.gz                   NCBI raw counts per Gene ID (GEO, as in 11/04)
#   geneid2ens.tsv                  NCBI Gene ID -> symbol -> Ensembl ID (from NCBI gene_info)
#   e52778.tsv                      Expression Atlas re-analysis of the same experiment (12/06)
set -euo pipefail
OUT=${1:-$HOME/rnaseq/gse}
mkdir -p "$OUT" && cd "$OUT"
curl -sS -O https://ftp.ncbi.nlm.nih.gov/geo/series/GSE52nnn/GSE52778/matrix/GSE52778_series_matrix.txt.gz
curl -sS -L -o counts.tsv.gz "https://www.ncbi.nlm.nih.gov/geo/download/?type=rnaseq_counts&acc=GSE52778&format=file&file=GSE52778_raw_counts_GRCh38.p13_NCBI.tsv.gz"
curl -sS https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/Homo_sapiens.gene_info.gz \
  | gunzip -c | awk -F'\t' 'NR > 1 {n = split($6, x, "|"); e = "-"; for (i = 1; i <= n; i++) if (x[i] ~ /^Ensembl:/) e = substr(x[i], 9); print $2 "\t" $3 "\t" e}' > geneid2ens.tsv
curl -sS -o e52778.tsv "https://www.ebi.ac.uk/gxa/experiments-content/E-GEOD-52778/resources/DifferentialSecondaryDataFiles.RnaSeq/analytics"
wc -l geneid2ens.tsv e52778.tsv
zcat counts.tsv.gz | awk -F'\t' 'NR == 1 {n = NF} END {print "columns:", n, " genes:", NR - 1}'
