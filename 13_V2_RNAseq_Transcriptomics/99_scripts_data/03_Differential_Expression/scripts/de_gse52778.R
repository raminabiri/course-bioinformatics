# Differential expression on real data: GSE52778 (airway smooth muscle, 4 donors, dexamethasone), part 13/03.
# Usage (in ~/rnaseq/gse):
#   Rscript de_gse52778.R GSE52778_series_matrix.txt.gz counts.tsv.gz geneid2ens.tsv e52778.tsv
# Inputs: GEO series matrix and NCBI raw counts (11/04), NCBI GeneID -> symbol/Ensembl table, Expression Atlas
# analytics file (12/06). The albuterol+dexamethasone contrast is in module 13/04 (check_labels.R).
# Writes PNG plots and de_dex_deseq2.tsv in the current folder.
# edgeR and limma-voom are in compare_methods.R (kept apart so that each script needs < 1 GB RAM).
# Plain R: runs the same in R/RStudio on Windows.
suppressMessages(library(DESeq2))
args <- commandArgs(trailingOnly = TRUE)

# ---- 1. sample table from the series matrix ----
lines <- readLines(gzfile(args[1]))
field <- function(prefix) {
  x <- strsplit(grep(prefix, lines, value = TRUE, fixed = TRUE), "\t")
  lapply(x, function(v) gsub('"', "", v[-1]))
}
gsm <- field("!Sample_geo_accession")[[1]]
ch <- field("!Sample_characteristics_ch1")
get <- function(key) { v <- ch[[which(sapply(ch, function(z) startsWith(z[1], key)))]]; sub(".*: ", "", v) }
coldata <- data.frame(cell = factor(get("cell line")), treatment = factor(get("treatment")), row.names = gsm)

counts <- as.matrix(read.delim(gzfile(args[2]), row.names = 1, check.names = FALSE))[, gsm]
genes <- read.delim(args[3], header = FALSE, col.names = c("geneid", "symbol", "ensembl"))
sym <- setNames(genes$symbol, genes$geneid)

# ---- 2. dexamethasone vs untreated, paired by donor ----
keep_s <- coldata$treatment %in% c("Untreated", "Dexamethasone")
cd <- droplevels(coldata[keep_s, ])
cd$dex <- relevel(factor(ifelse(cd$treatment == "Dexamethasone", "dex", "untrt")), ref = "untrt")
ct <- counts[, keep_s]
ct <- ct[rowSums(ct >= 10) >= 4, ]                     # keep genes with >= 10 reads in >= 4 samples
cat("== samples and genes kept:", ncol(ct), "x", nrow(ct), "\n")
print(cd[, c("cell", "dex")])

dds <- DESeqDataSetFromMatrix(ct, cd, design = ~ cell + dex)
dds <- DESeq(dds, quiet = TRUE)
res <- results(dds, name = "dex_dex_vs_untrt", alpha = 0.05)
cat("\n== DESeq2 ~ cell + dex\n"); summary(res)
shr <- lfcShrink(dds, coef = "dex_dex_vs_untrt", type = "apeglm", quiet = TRUE)

tab <- data.frame(symbol = sym[rownames(res)], baseMean = round(res$baseMean),
                  log2FC = round(res$log2FoldChange, 2), log2FC_shrunk = round(shr$log2FoldChange, 2),
                  padj = res$padj, row.names = rownames(res))
tab <- tab[order(tab$padj), ]
show <- function(x) transform(x, padj = signif(padj, 3))
cat("\n== top 10 by padj\n"); print(show(head(tab, 10)))
ours <- c("2908", "2289", "1831", "7704", "5187", "1843", "28999", "83716")
cat("\n== the 8 genes of 11/04\n"); print(show(tab[ours, ]))
write.table(tab, "de_dex_deseq2.tsv", sep = "\t", quote = FALSE)

# ---- 3. the same without the donor term ----
dds0 <- DESeqDataSetFromMatrix(ct, cd, design = ~ dex)
dds0 <- DESeq(dds0, quiet = TRUE)
res0 <- results(dds0, name = "dex_dex_vs_untrt", alpha = 0.05)
cat("\n== padj < 0.05: with donor (~ cell + dex):", sum(res$padj < 0.05, na.rm = TRUE),
    "  without donor (~ dex):", sum(res0$padj < 0.05, na.rm = TRUE), "\n")

# ---- 4. PCA on variance-stabilised counts ----
vsd <- vst(dds, blind = TRUE)
pc <- plotPCA(vsd, intgroup = c("cell", "dex"), returnData = TRUE)
cat("\n== PCA: percent variance PC1, PC2:", round(100 * attr(pc, "percentVar")[1:2], 1), "\n")
print(data.frame(cell = pc$cell, dex = pc$dex, PC1 = round(pc$PC1, 1), PC2 = round(pc$PC2, 1), row.names = rownames(pc)))
png("pca_gse52778.png", width = 500, height = 400)
plot(pc$PC1, pc$PC2, col = ifelse(pc$dex == "dex", "red", "blue"), pch = as.integer(pc$cell) + 14, cex = 1.6,
     xlab = "PC1", ylab = "PC2", main = "GSE52778: PCA of vst counts (red = dex, shape = donor)")
invisible(dev.off())
png("ma_gse52778.png", width = 500, height = 400); plotMA(shr, ylim = c(-5, 5), main = "MA plot (apeglm)"); invisible(dev.off())
sig <- !is.na(res$padj) & res$padj < 0.05
png("volcano_gse52778.png", width = 500, height = 400)
plot(res$log2FoldChange, -log10(res$pvalue), pch = 20, cex = 0.4, col = ifelse(sig, "red", "grey"),
     xlab = "log2 fold change", ylab = "-log10 p", main = "Volcano (red = padj < 0.05)")
invisible(dev.off())

# ---- 5. Expression Atlas re-analysis (12/06) ----
atlas <- read.delim(args[4], check.names = FALSE)
ens <- setNames(genes$ensembl, genes$geneid)
d <- !is.na(res$padj) & res$padj < 0.05
m <- data.frame(ens = ens[rownames(res)], lfc = res$log2FoldChange, sig = d)
m <- merge(m, atlas[, c(1, 7, 8)], by.x = "ens", by.y = 1)
colnames(m)[4:5] <- c("atlas_p", "atlas_lfc")
m <- m[!is.na(m$atlas_lfc) & !is.na(m$lfc), ]
cat("\n== vs Expression Atlas: genes matched", nrow(m),
    " correlation of log2FC", round(cor(m$lfc, m$atlas_lfc), 3),
    "  significant in both", sum(m$sig & m$atlas_p < 0.05, na.rm = TRUE), "of ours", sum(m$sig), "\n")
