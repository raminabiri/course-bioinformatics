#!/usr/bin/env python3
"""Build the "spiked" test sample of module 06/02 without wgsim/seqkit (Windows route; stdlib only).

minigut (trimmed) + N simulated human read pairs from each human FASTA region given.
Read names start with the source (HUMAN_chr21_..., HUMAN_chr1_...), so every read's origin is known.
This is a simple simulator (random fragments, fixed insert size spread, uniform base errors), not wgsim:
the idea and the known answer are the same as in the Linux lesson, the exact numbers differ a little.

Usage:
    py spike_human.py <minigut_R1.fastq.gz> <minigut_R2.fastq.gz> <out_prefix> chr21=<fasta> chr1=<fasta> [N]
Example:
    py spike_human.py qc\\trimmed\\minigut_R1.fastq.gz qc\\trimmed\\minigut_R2.fastq.gz host\\spiked\\minigut_spiked \\
       chr21=host\\ref\\host_chr21_region.fa chr1=host\\ref\\human_chr1_region.fa 5000
Writes <out_prefix>_R1.fastq.gz and _R2.fastq.gz (seed 42: the same file for everyone).
"""
import gzip
import io
import random
import shutil
import sys

READ_LEN, INSERT, SPREAD, ERROR = 126, 350, 50, 0.002
COMP = str.maketrans("ACGTN", "TGCAN")


def read_fasta(path):
    """One-sequence FASTA -> upper-case string."""
    with open(path) as fh:
        return "".join(line.strip() for line in fh if not line.startswith(">")).upper()


def mutate(seq, rng):
    """Uniform sequencing errors at rate ERROR."""
    out = list(seq)
    for i, base in enumerate(out):
        if rng.random() < ERROR:
            out[i] = rng.choice([b for b in "ACGT" if b != base])
    return "".join(out)


if len(sys.argv) < 6:
    sys.exit(__doc__)
r1_in, r2_in, prefix = sys.argv[1:4]
regions = [a.split("=", 1) for a in sys.argv[4:6]]
n_pairs = int(sys.argv[6]) if len(sys.argv) > 6 else 5000
rng = random.Random(42)

outs = [prefix + "_R1.fastq.gz", prefix + "_R2.fastq.gz"]
for src, dst in zip([r1_in, r2_in], outs):          # 1. copy the microbial reads
    with gzip.open(src, "rb") as fi, gzip.GzipFile(dst, "wb", mtime=0) as fo:   # mtime=0: same bytes every run
        shutil.copyfileobj(fi, fo)

qual = "I" * READ_LEN
with gzip.GzipFile(outs[0], "ab", mtime=0) as g1, gzip.GzipFile(outs[1], "ab", mtime=0) as g2:
    o1, o2 = io.TextIOWrapper(g1, newline="\n"), io.TextIOWrapper(g2, newline="\n")
    for name, path in regions:                         # 2. add human pairs
        genome = read_fasta(path)
        made = 0
        while made < n_pairs:
            size = max(READ_LEN, int(rng.gauss(INSERT, SPREAD)))
            start = rng.randrange(0, len(genome) - size)
            frag = genome[start:start + size]
            if frag.count("N") > size * 0.1:           # skip gaps of the assembly
                continue
            if rng.random() < 0.5:                     # fragment from either strand
                frag = frag.translate(COMP)[::-1]
            a = mutate(frag[:READ_LEN], rng)
            b = mutate(frag[-READ_LEN:].translate(COMP)[::-1], rng)
            rid = f"HUMAN_{name}_{made}"
            o1.write(f"@{rid}/1\n{a}\n+\n{qual}\n")
            o2.write(f"@{rid}/2\n{b}\n+\n{qual}\n")
            made += 1
    o1.flush(); o2.flush()
print(f"wrote {outs[0]} and {outs[1]}: microbial reads + {n_pairs} human pairs from each of",
      ", ".join(n for n, _ in regions))
