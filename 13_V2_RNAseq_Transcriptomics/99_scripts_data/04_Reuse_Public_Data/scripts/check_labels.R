# Do the GEO treatment labels of GSE52778 agree with the data? (part 13, module 04)
# Usage:   Rscript check_labels.R GSE52778_series_matrix.txt.gz counts.tsv.gz OUT.tsv
# 1. A "glucocorticoid score" per sample: mean log2(CPM + 1) of 7 genes that dexamethasone switches on
#    (FKBP5, TSC22D3, ZBTB16, PER1, KLF15, CRISPLD2, DUSP1), minus the same score in the untreated sample
#    of the same donor. Samples that received dexamethasone should score high, the others near 0.
# 2. DESeq2 for "albuterol + dexamethasone vs untreated" with the labels as in GEO, and again after swapping
#    the two labels "Albuterol" <-> "Albuterol_Dexamethasone" in the donors whose scores disagree.
suppressMessages(library(DESeq2))
args <- commandArgs(trailingOnly = TRUE)

lines <- readLines(gzfile(args[1]))
field <- function(prefix) lapply(strsplit(grep(prefix, lines, value = TRUE, fixed = TRUE), "\t"),
                                 function(v) gsub('"', "", v[-1]))
gsm <- field("!Sample_geo_accession")[[1]]
ch <- field("!Sample_characteristics_ch1")
get <- function(key) sub(".*: ", "", ch[[which(sapply(ch, function(z) startsWith(z[1], key)))]])
cd <- data.frame(cell = get("cell line"), treatment = get("treatment"), row.names = gsm)
counts <- as.matrix(read.delim(gzfile(args[2]), row.names = 1, check.names = FALSE))[, gsm]

# ---- 1. glucocorticoid score ----
markers <- c("2289", "1831", "7704", "5187", "28999", "83716", "1843")
logcpm <- log2(t(t(counts) / colSums(counts)) * 1e6 + 1)
raw <- colMeans(logcpm[markers, ])
base <- sapply(cd$cell, function(c) raw[rownames(cd)[cd$cell == c & cd$treatment == "Untreated"]])
cd$gc_score <- round(raw - base, 2)
cat("== glucocorticoid score (log2, relative to the donor's untreated sample)\n")
print(reshape(cd[, c("cell", "treatment", "gc_score")], idvar = "cell", timevar = "treatment", direction = "wide"),
      row.names = FALSE)
gets_dex <- grepl("Dexamethasone", cd$treatment)
cd$label_ok <- ifelse(gets_dex, cd$gc_score > 1.5, cd$gc_score < 1.5)
cat("\n== samples whose label disagrees with the score\n")
print(cd[!cd$label_ok, c("cell", "treatment", "gc_score")])
write.table(cd, args[3], sep = "\t", quote = FALSE)

# ---- 2. albuterol + dexamethasone vs untreated, before and after swapping ----
de_combination <- function(meta) {
  keep <- meta$treatment %in% c("Untreated", "Albuterol_Dexamethasone")
  m <- meta[keep, ]; m$cell <- factor(m$cell)
  m$trt <- relevel(factor(m$treatment), ref = "Untreated")
  ct <- counts[, keep]; ct <- ct[rowSums(ct >= 10) >= 4, ]
  dds <- DESeq(DESeqDataSetFromMatrix(ct, m, design = ~ cell + trt), quiet = TRUE)
  res <- results(dds, name = "trt_Albuterol_Dexamethasone_vs_Untreated", alpha = 0.05)
  c(n_padj_0.05 = sum(res$padj < 0.05, na.rm = TRUE), FKBP5_log2FC = round(res["2289", "log2FoldChange"], 2),
    ZBTB16_log2FC = round(res["7704", "log2FoldChange"], 2))
}
swapped <- cd
bad_donors <- unique(cd$cell[!cd$label_ok])
for (d in bad_donors) {
  i_a <- which(swapped$cell == d & swapped$treatment == "Albuterol")
  i_ad <- which(swapped$cell == d & swapped$treatment == "Albuterol_Dexamethasone")
  swapped$treatment[c(i_a, i_ad)] <- swapped$treatment[c(i_ad, i_a)]
}
cat("\n== albuterol + dexamethasone vs untreated (~ cell + trt)\n")
print(rbind(labels_as_in_GEO = de_combination(cd), labels_swapped_in = de_combination(swapped)))
cat("donors swapped:", paste(bad_donors, collapse = ", "), "\n")
