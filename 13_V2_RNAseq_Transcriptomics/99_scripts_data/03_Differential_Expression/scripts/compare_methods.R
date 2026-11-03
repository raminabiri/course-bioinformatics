# edgeR and limma-voom on the same GSE52778 comparison as de_gse52778.R (dexamethasone vs untreated, ~ cell + dex).
# Usage (in ~/rnaseq/gse, after de_gse52778.R):   Rscript compare_methods.R GSE52778_series_matrix.txt.gz counts.tsv.gz
# Reads de_dex_deseq2.tsv (DESeq2 result) and counts genes with FDR < 0.05 in each method and in all three.
suppressMessages({library(edgeR); library(limma)})
args <- commandArgs(trailingOnly = TRUE)

lines <- readLines(gzfile(args[1]))
field <- function(prefix) lapply(strsplit(grep(prefix, lines, value = TRUE, fixed = TRUE), "\t"),
                                 function(v) gsub('"', "", v[-1]))
gsm <- field("!Sample_geo_accession")[[1]]
ch <- field("!Sample_characteristics_ch1")
get <- function(key) sub(".*: ", "", ch[[which(sapply(ch, function(z) startsWith(z[1], key)))]])
cd <- data.frame(cell = factor(get("cell line")), treatment = get("treatment"), row.names = gsm)
cd <- cd[cd$treatment %in% c("Untreated", "Dexamethasone"), ]
cd$dex <- relevel(factor(ifelse(cd$treatment == "Dexamethasone", "dex", "untrt")), ref = "untrt")
cd$cell <- droplevels(cd$cell)

ct <- as.matrix(read.delim(gzfile(args[2]), row.names = 1, check.names = FALSE))[, rownames(cd)]
ct <- ct[rowSums(ct >= 10) >= 4, ]                     # same filter as de_gse52778.R
design <- model.matrix(~ cell + dex, data = cd)

y <- normLibSizes(DGEList(ct))                         # TMM normalisation
y <- estimateDisp(y, design)
qlf <- glmQLFTest(glmQLFit(y, design), coef = "dexdex")
fdr_edger <- p.adjust(qlf$table$PValue, method = "BH")

v <- voom(y, design)                                   # log-CPM with precision weights
fit <- eBayes(lmFit(v, design))
fdr_limma <- topTable(fit, coef = "dexdex", number = Inf, sort.by = "none")$adj.P.Val

deseq <- read.delim("de_dex_deseq2.tsv")
fdr_deseq <- deseq[rownames(ct), "padj"]
d <- !is.na(fdr_deseq) & fdr_deseq < 0.05; e <- fdr_edger < 0.05; l <- fdr_limma < 0.05
cat("genes:", nrow(ct), "\n")
cat("FDR < 0.05   DESeq2:", sum(d), "  edgeR:", sum(e), "  limma-voom:", sum(l), "\n")
cat("in all three:", sum(d & e & l), "  only DESeq2:", sum(d & !e & !l), "  only edgeR:", sum(e & !d & !l),
    "  only limma:", sum(l & !d & !e), "\n")
