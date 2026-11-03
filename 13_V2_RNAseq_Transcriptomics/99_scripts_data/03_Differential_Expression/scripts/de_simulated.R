# DESeq2 on the simulated counts of module 13/02, checked against the known log2 fold changes.
# Usage (in ~/rnaseq):   Rscript de_simulated.R gene_counts_salmon.tsv reads/truth_counts.tsv
# Plain R: runs the same in R/RStudio on Windows.
suppressMessages(library(DESeq2))

args <- commandArgs(trailingOnly = TRUE)
counts <- as.matrix(read.delim(args[1], row.names = 1))
truth <- read.delim(args[2], row.names = 1)

coldata <- data.frame(condition = factor(c("ctrl", "ctrl", "ctrl", "dex", "dex", "dex"),
                                         levels = c("ctrl", "dex")),
                      row.names = colnames(counts))
dds <- DESeqDataSetFromMatrix(counts, coldata, design = ~ condition)
dds <- DESeq(dds, quiet = TRUE)

cat("size factors:\n"); print(round(sizeFactors(dds), 3))
res <- results(dds, contrast = c("condition", "dex", "ctrl"), alpha = 0.05)
shr <- lfcShrink(dds, coef = "condition_dex_vs_ctrl", type = "apeglm", quiet = TRUE)

out <- data.frame(true_lfc = truth[rownames(res), "log2fc_true"],
                  baseMean = round(res$baseMean),
                  lfc = round(res$log2FoldChange, 2),
                  lfc_shrunk = round(shr$log2FoldChange, 2),
                  padj = signif(res$padj, 3),
                  row.names = rownames(res))
out <- out[order(out$padj), ]
print(out)

called <- !is.na(out$padj) & out$padj < 0.05
truly <- out$true_lfc != 0
cat("\ncalled DE (padj < 0.05):", sum(called),
    " true positives:", sum(called & truly),
    " false positives:", sum(called & !truly),
    " missed:", sum(!called & truly), "\n")
