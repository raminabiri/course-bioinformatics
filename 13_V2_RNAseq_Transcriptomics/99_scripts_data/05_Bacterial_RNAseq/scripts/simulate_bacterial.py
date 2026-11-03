#!/usr/bin/env python3
"""Simulate a stranded single-end RNA-seq experiment of E. coli K-12 MG1655 under ciprofloxacin, with a KNOWN answer
(part 13, module 05).

Usage:
    python3 simulate_bacterial.py GENOME.fna.gz GENOME.gff.gz OUTDIR [READS_PER_SAMPLE]

Design: 6 samples, ctrl_1..3 (no drug) and cip_1..3 (ciprofloxacin), 400 000 reads of 75 bp per sample.
Known answer (log2 fold change, cip vs ctrl), inspired by the SOS response to DNA damage:
  up:   recA-recX, lexA-dinF, umuD-umuC (operons, one value per operon), sulA, recN, dinI, dinB, uvrA, uvrB,
        yebG, tisB
  down: the S10 ribosomal protein operon (rpsJ ... rpsQ, b3311-b3321): slower growth
Operons are simulated as ONE transcript from the first to the last gene, so their genes change together and
reads also fall between the genes. Every other gene is its own transcript.
Expression level: per gene, log-normal (ribosomal protein genes 8 times higher; the changed SOS genes start at
the median level, as lexA keeps them on at a low level); per sample the number of fragments
is drawn from a negative binomial (dispersion 0.05). rRNA left over after depletion: 6-15% of reads per sample.
Library type: stranded, dUTP ("reverse"): the read is the reverse complement of the transcript. Errors 0.2%.
Writes OUTDIR/<sample>.fastq.gz, OUTDIR/truth.tsv (genes with a known change) and OUTDIR/genes.tsv
(locus_tag, name, biotype, length of every gene). Random seed 13.
"""
import gzip
import os
import sys

import numpy as np

fna, gff, outdir = sys.argv[1:4]
n_reads = int(sys.argv[4]) if len(sys.argv) > 4 else 400_000
os.makedirs(outdir, exist_ok=True)
rng = np.random.default_rng(13)
COMP = str.maketrans("ACGT", "TGCA")
READ_LEN, FRAG_MEAN, FRAG_SD, DISPERSION, ERROR = 75, 200, 40, 0.05, 0.002

UP = {"recA": 3.0, "lexA": 2.5, "umuD": 3.5, "sulA": 4.0, "recN": 3.5, "dinI": 3.0, "dinB": 2.5,
      "uvrA": 2.0, "uvrB": 2.0, "yebG": 3.0, "tisB": 4.0}
OPERONS = {"recA": ["recA", "recX"], "lexA": ["lexA", "dinF"], "umuD": ["umuD", "umuC"],
           "S10": [f"b{n}" for n in range(3311, 3322)]}          # S10 operon by locus tag
DOWN = {"S10": -1.5}
RRNA_FRAC = {"ctrl_1": 0.08, "ctrl_2": 0.12, "ctrl_3": 0.06, "cip_1": 0.15, "cip_2": 0.10, "cip_3": 0.07}

genome = "".join(l.strip() for l in gzip.open(fna, "rt") if not l.startswith(">"))
genes = []                                     # (locus_tag, name, biotype, start, end, strand)
for line in gzip.open(gff, "rt"):
    f = line.rstrip("\n").split("\t")
    if len(f) < 9 or f[2] != "gene":
        continue
    a = dict(kv.split("=", 1) for kv in f[8].split(";"))
    genes.append((a["locus_tag"], a["Name"], a["gene_biotype"], int(f[3]), int(f[4]), f[6]))
by_key = {g[0]: g for g in genes} | {g[1]: g for g in genes}

# transcripts: operons first, then every gene not in an operon
units, in_operon = [], set()
for op, members in OPERONS.items():
    gs = [by_key[m] for m in members]
    in_operon.update(g[0] for g in gs)
    units.append((op, [g[0] for g in gs], min(g[3] for g in gs), max(g[4] for g in gs), gs[0][5], "protein_coding"))
for g in genes:
    if g[0] not in in_operon and g[2] in ("protein_coding", "ncRNA", "tRNA", "rRNA"):
        units.append((g[1], [g[0]], g[3], g[4], g[5], g[2]))

lengths = np.array([u[3] - u[2] + 1 for u in units], dtype=float)
level = rng.lognormal(mean=0.0, sigma=1.5, size=len(units))
for i, u in enumerate(units):
    if u[0] == "S10" or by_key[u[1][0]][1].startswith(("rps", "rpl", "rpm")):
        level[i] *= 8
    if u[0] in UP:
        level[i] = 1.0
    if u[5] == "tRNA":
        level[i] *= 0.1                        # mostly lost in size selection
log2fc = np.array([UP.get(u[0], DOWN.get(u[0], 0.0)) for u in units])
is_rrna = np.array([u[5] == "rRNA" for u in units])


def unit_seq(u):
    s = genome[u[2] - 1:u[3]]
    return s.translate(COMP)[::-1] if u[4] == "-" else s


seqs = [unit_seq(u) for u in units]
for s_i, sample in enumerate(RRNA_FRAC):
    treated = sample.startswith("cip")
    mu = level * lengths * (2.0 ** log2fc if treated else 1.0)
    mu = np.where(is_rrna, 0.0, mu)
    lam = rng.gamma(shape=1 / DISPERSION, scale=mu * DISPERSION + 1e-12)
    n_rrna = int(n_reads * RRNA_FRAC[sample])
    counts = rng.multinomial(n_reads - n_rrna, lam / lam.sum())
    counts += rng.multinomial(n_rrna, np.where(is_rrna, lengths, 0.0) / lengths[is_rrna].sum())
    with gzip.open(os.path.join(outdir, f"{sample}.fastq.gz"), "wt", compresslevel=6) as out:
        k = 0
        for i in np.repeat(np.arange(len(units)), counts):
            s = seqs[i]
            frag = int(min(len(s), max(READ_LEN, rng.normal(FRAG_MEAN, FRAG_SD))))
            start = rng.integers(0, len(s) - frag + 1)
            read = list(s[start:start + frag].translate(COMP)[::-1][:READ_LEN])   # dUTP: antisense read
            for j in np.nonzero(rng.random(len(read)) < ERROR)[0]:
                read[j] = "ACGT"[(("ACGT".index(read[j]) if read[j] in "ACGT" else 0) + rng.integers(1, 4)) % 4]
            k += 1
            out.write(f"@{sample}.{k}\n{''.join(read)}\n+\n{'I' * len(read)}\n")
    print(f"{sample}: {k} reads ({n_rrna} rRNA)")

with open(os.path.join(outdir, "truth.tsv"), "w") as t:
    t.write("locus_tag\tname\toperon\tlog2fc_true\n")
    for u, fc in zip(units, log2fc):
        if fc != 0:
            for lt in u[1]:
                t.write(f"{lt}\t{by_key[lt][1]}\t{u[0] if len(u[1]) > 1 else '-'}\t{fc}\n")
with open(os.path.join(outdir, "genes.tsv"), "w") as t:
    t.write("locus_tag\tname\tbiotype\tlength\n")
    for g in genes:
        t.write(f"{g[0]}\t{g[1]}\t{g[2]}\t{g[4] - g[3] + 1}\n")
