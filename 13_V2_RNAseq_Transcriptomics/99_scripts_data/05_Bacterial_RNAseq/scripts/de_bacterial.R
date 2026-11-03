# DESeq2 on the simulated E. coli experiment (ciprofloxacin vs no drug) and comparison with the known answer.
# Part 13, module 05.
# Usage:   Rscript de_bacterial.R gene_counts.txt genes.tsv truth.tsv
#   gene_counts.txt   featureCounts output (-t gene -g locus_tag), columns 7-12: ctrl_1..3, cip_1..3
#   genes.tsv, truth.tsv   from simulate_bacterial.py
# Writes de_cip.tsv (all genes: locus_tag, name, biotype, baseMean, log2FC, padj) in the current folder.
suppressMessages(library(DESeq2))
args <- commandArgs(trailingOnly = TRUE)

fc <- read.delim(args[1], comment.char = "#", row.names = 1, check.names = FALSE)
counts <- as.matrix(fc[, 6:11])
colnames(counts) <- sub("\\.bam$", "", basename(colnames(counts)))
genes <- read.delim(args[2], row.names = 1)
truth <- read.delim(args[3], row.names = 1)

# ---- 1. rRNA and tRNA out ----
bt <- genes[rownames(counts), "biotype"]
cat("== share of counted reads per biotype (%)\n")
print(round(100 * t(rowsum(counts, bt)) / colSums(counts), 1))
counts <- counts[bt %in% c("protein_coding", "ncRNA"), ]
cat("\ngenes kept (protein_coding + ncRNA):", nrow(counts), "\n")

# ---- 2. DESeq2 ----
cd <- data.frame(condition = factor(sub("_[0-9]$", "", colnames(counts)), levels = c("ctrl", "cip")),
                 row.names = colnames(counts))
dds <- DESeq(DESeqDataSetFromMatrix(counts, cd, design = ~ condition), quiet = TRUE)
cat("\n== size factors\n"); print(round(sizeFactors(dds), 3))
res <- results(dds, alpha = 0.05)
sig <- rownames(res)[which(res$padj < 0.05)]
cat("\n== padj < 0.05:", length(sig), "genes (", sum(res[sig, "log2FoldChange"] > 0), "up,",
    sum(res[sig, "log2FoldChange"] < 0), "down )\n")

# ---- 3. comparison with the known answer ----
truth$log2FC <- round(res[rownames(truth), "log2FoldChange"], 2)
truth$padj <- signif(res[rownames(truth), "padj"], 3)
truth$baseMean <- round(res[rownames(truth), "baseMean"])
cat("\n== genes with a known change\n")
print(truth[order(truth$operon, -truth$log2fc_true), ])
fp <- setdiff(sig, rownames(truth))
cat("\nfound:", length(intersect(sig, rownames(truth))), "of", nrow(truth), "known genes;",
    "false positives:", length(fp), "\n")
if (length(fp) > 0) print(data.frame(name = genes[fp, "name"], log2FC = round(res[fp, "log2FoldChange"], 2),
                                     padj = signif(res[fp, "padj"], 3), row.names = fp))

out <- data.frame(locus_tag = rownames(res), name = genes[rownames(res), "name"],
                  biotype = genes[rownames(res), "biotype"], baseMean = round(res$baseMean, 1),
                  log2FC = round(res$log2FoldChange, 3), padj = res$padj)
write.table(out, "de_cip.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
