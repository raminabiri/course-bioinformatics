#!/usr/bin/env python3
"""Compare our DESeq2 result for GSE52778 with the claims of Himes et al. 2014 (PLoS ONE 9:e99625).

The abstract reports 316 differentially expressed genes (Benjamini-Hochberg p < 0.05) and names seven:
DUSP1, KLF15, PER1, TSC22D3 (known) and C7, CCDC69, CRISPLD2 (less investigated).

Usage:   python3 paper_check.py de_dex_deseq2.tsv > report.txt
"""
import sys

import pandas as pd

PAPER_N = 316
PAPER_GENES = ["DUSP1", "KLF15", "PER1", "TSC22D3", "C7", "CCDC69", "CRISPLD2"]

tab = pd.read_csv(sys.argv[1], sep="\t", index_col=0).dropna(subset=["padj"])
tab = tab.sort_values("padj")
tab["rank"] = range(1, len(tab) + 1)
sig = tab[tab["padj"] < 0.05]

print(f"paper: {PAPER_N} genes with BH p < 0.05")
print(f"ours:  {len(sig)} genes with padj < 0.05 "
      f"({len(sig[sig['log2FC'].abs() > 1])} with |log2FC| > 1)")
print(f"padj of our {PAPER_N}th gene (a list as long as the paper's):",
      f"{tab['padj'].iloc[PAPER_N - 1]:.2e}")
print("\nthe seven genes named in the abstract:")
print(tab[tab["symbol"].isin(PAPER_GENES)][["symbol", "log2FC", "padj", "rank"]].to_string())
found = tab[tab["symbol"].isin(PAPER_GENES) & (tab["padj"] < 0.05)]
print(f"\nreproduced: {len(found)} of {len(PAPER_GENES)} named genes; "
      f"in our top {PAPER_N}: {int((found['rank'] <= PAPER_N).sum())}")
