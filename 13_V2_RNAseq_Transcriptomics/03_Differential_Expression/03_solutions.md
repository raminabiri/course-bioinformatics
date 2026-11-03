<div dir="rtl">

# پاسخ تشریحی: بیان افتراقی

همه‌ی خروجی‌ها واقعی‌اند (R 4.5.3، DESeq2 1.50.2؛ روی سرور دوره، 2026-10-28).

---

## پاسخ ۱: دو تکرار به جای سه

<div dir="ltr">

```r
suppressMessages(library(DESeq2))
ct <- as.matrix(read.delim("gene_counts_salmon.tsv", row.names = 1))[, c("ctrl_1", "ctrl_2", "dex_1", "dex_2")]
cd <- data.frame(condition = factor(c("ctrl", "ctrl", "dex", "dex")), row.names = colnames(ct))
res <- results(DESeq(DESeqDataSetFromMatrix(ct, cd, ~ condition), quiet = TRUE), alpha = 0.05)
cat("2 vs 2: padj < 0.05:", sum(res$padj < 0.05, na.rm = TRUE), "\n"); print(rownames(res)[which(res$padj < 0.05)])
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
2 vs 2: padj < 0.05: 8 
[1] "NR3C1"    "FKBP5"    "TSC22D3"  "ZBTB16"   "PER1"     "DUSP1"    "KLF15"   
[8] "CRISPLD2"
```

</div>

هر **هشت** ژن، با دو تکرار. ولی این **نمی‌گوید** دو تکرار بس است: تغییرهای شبیه‌سازی‌شده بسیار بزرگ‌اند (۲ تا ۳۴ برابر) و پراکندگی کم (۰٫۰۵). در داده‌ی واقعی بیشتر ژن‌های جالب تغییر ۱٫۵ تا ۲ برابری دارند و پراکندگی میان افراد بیشتر است؛ آن‌جا دو تکرار بسیاری را از دست می‌دهد (13/01، Schurch و همکاران). و با دو تکرار، یک نمونه‌ی خراب را نمی‌توان شناخت.

---

## پاسخ ۲: هم‌سان‌سازی با ژن‌های خانه‌دار

<div dir="ltr">

```r
suppressMessages(library(DESeq2))
ct <- as.matrix(read.delim("gene_counts_salmon.tsv", row.names = 1))
cd <- data.frame(condition = factor(rep(c("ctrl", "dex"), each = 3)), row.names = colnames(ct))
dds <- DESeqDataSetFromMatrix(ct, cd, ~ condition)
hk <- which(rownames(dds) %in% c("ACTB", "GAPDH", "TBP", "HPRT1", "PGK1", "B2M", "PPIA", "RPLP0", "TUBB", "EEF1A1", "YWHAZ", "SDHA"))
dds <- estimateSizeFactors(dds, controlGenes = hk); print(round(sizeFactors(dds), 3))
res <- as.data.frame(results(DESeq(dds, quiet = TRUE), alpha = 0.05))
print(signif(res[c("NR3C1", "FKBP5", "ZBTB16", "GAPDH", "TUBB", "EEF1A1"), c("log2FoldChange", "padj")], 3))
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ctrl_1 ctrl_2 ctrl_3  dex_1  dex_2  dex_3 
 0.972  1.071  0.974  1.023  1.035  0.899 
       log2FoldChange     padj
NR3C1         -1.2000 1.91e-06
FKBP5          3.1900 5.26e-26
ZBTB16         4.4300 3.28e-19
GAPDH          0.2960 3.32e-01
TUBB          -0.1500 9.28e-01
EEF1A1         0.0362 9.67e-01
```

</div>

| ژن | درست | همه‌ی ژن‌ها (درس) | تنها خانه‌دارها |
| :--- | :---: | :---: | :---: |
| ‏NR3C1 | ‏−۱٫۰ | ‏−۱٫۵۹ | ‏**−۱٫۲۰** |
| ‏FKBP5 | ‏۳٫۳ | ‏۲٫۸۱ | ‏**۳٫۱۹** |
| ‏ZBTB16 | ‏۵٫۱ | ‏۴٫۰۶ | ‏**۴٫۴۳** |
| ‏GAPDH | ‏۰ | ‏−۰٫۰۷ | ‏۰٫۳۰ |
| ‏TUBB | ‏۰ | ‏−۰٫۴۹ | ‏**−۰٫۱۵** |
| ‏EEF1A1 | ‏۰ | ‏−۰٫۳۴ | ‏**۰٫۰۴** |

ضریب‌های نمونه‌های dex دیگر بزرگ‌تر از شاهدها نیستند (۰٫۹ تا ۱٫۰۴ در برابر ۱٫۰۹ تا ۱٫۲۱ در درس). بیشتر log2FCها به مقدار درست نزدیک‌تر شدند، و این گمان درس را **تأیید** می‌کند: جابه‌جایی از ژن‌های بالارفته در محاسبه‌ی median-of-ratios بود. ولی همه بی‌خطا نشدند (GAPDH ‏۰٫۳۰): ژن‌های «خانه‌دار» هم نویز دارند و خود را در هم‌سان‌سازی می‌آورند. در داده‌ی واقعی، `controlGenes` تنها وقتی درست است که مطمئن باشید آن ژن‌ها تغییر نمی‌کنند (مانند spike-inها).

---

## پاسخ ۳: تغییر بزرگ و مطمئن

<div dir="ltr">

```bash
cd ~/rnaseq/gse
awk -F'\t' 'NR > 1 && $6 != "NA" && $6 < 0.05 {n++; if ($4 > 1 || $4 < -1) b++} END {print "padj<0.05:", n, " and |log2FC|>1:", b}' de_dex_deseq2.tsv
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
padj<0.05: 4743  and |log2FC|>1: 1064
```

</div>

‏**۱۰۶۴** ژن (۲۲٪ ژن‌های معنادار) بیش از دو برابر تغییر کرده‌اند. بیشتر ۴۷۴۳ ژن تغییرهای کوچک ولی مطمئن دارند. فرق با `lfcThreshold = 1`: آن‌جا آزمون خودش می‌پرسد «آیا |log2FC| **بیش از ۱** است؟» و ژنی با log2FC برآوردی ۱٫۱ ولی نامطمئن رد می‌شود. برش پس از آزمون (کار ما) چنین ژنی را نگه می‌دارد. پس `lfcThreshold` سخت‌گیرتر و از نظر آماری درست‌تر است و فهرست کوتاه‌تری می‌دهد.

---

## پاسخ ۴: ‏CRISPLD2 کجاست؟

<div dir="ltr">

```bash
tail -n +2 de_dex_deseq2.tsv | awk -F'\t' '$6 != "NA"' | sort -t$'\t' -k6,6g | awk -F'\t' '$2 == "CRISPLD2" {print "rank by padj:", NR}'
tail -n +2 de_dex_deseq2.tsv | awk -F'\t' '$6 != "NA" && $6 < 0.05' | sort -t$'\t' -k5,5gr | awk -F'\t' '$2 == "CRISPLD2" {print "rank by shrunk log2FC (up):", NR}'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
rank by padj: 79
rank by shrunk log2FC (up): 56
```

</div>

‏`sort -g` عددها را با نماد علمی (`1e-43`) درست مرتب می‌کند؛ `-k6,6` تنها ستون ۶. ‏CRISPLD2 ‏**۷۹**ـمین بر پایه‌ی padj و **۵۶**ـمین در میان ژن‌های بالارفته بر پایه‌ی اندازه است. مقاله‌ی Himes آن را برای **زیست‌شناسی**‌اش برگزید، نه رتبه: ژنی ناشناخته در ماهیچه‌ی راه هوایی که با گلوکوکورتیکوئید بالا می‌رود و در آزمایش‌های بعدی (خاموش کردن ژن) اثرش بر سایتوکین‌های التهابی دیده شد. رتبه‌ی آماری تنها **فهرست نامزدها** را می‌دهد؛ برگزیدن از میان آن‌ها دانش زیستی و آزمایش می‌خواهد.

---

## پاسخ ۵: سطح مرجع الفبایی

<div dir="ltr">

```r
suppressMessages(library(DESeq2))
ct <- as.matrix(read.delim("gene_counts_salmon.tsv", row.names = 1))
cd <- data.frame(treatment = factor(rep(c("untrt", "dex"), each = 3)), row.names = colnames(ct)); print(levels(cd$treatment))
dds <- DESeq(DESeqDataSetFromMatrix(ct, cd, ~ treatment), quiet = TRUE); print(resultsNames(dds))
print(signif(as.data.frame(results(dds))["FKBP5", c("log2FoldChange", "padj")], 3))
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
[1] "dex"   "untrt"
[1] "Intercept"              "treatment_untrt_vs_dex"
      log2FoldChange     padj
FKBP5          -2.81 1.48e-15
```

</div>

‏`factor` سطح‌ها را **الفبایی** می‌چیند: `dex` پیش از `untrt`. پس `dex` مرجع شد و نتیجه «untrt نسبت به dex» است (`treatment_untrt_vs_dex`). ‏FKBP5 ‏**−۲٫۸۱**: همان عدد درس با علامت **وارونه**. ‏padj یکسان است؛ تنها جهت عوض شد. اگر به نام ستون نگاه نکنید، گزارش می‌کنید «دگزامتازون FKBP5 را پایین می‌آورد». همیشه `resultsNames` را بخوانید و `relevel(…, ref = "untrt")` بزنید.

---

## پاسخ ۶ (فکری): خواندن یک سطر

- **ژن نخست** (baseMean ‏۱۵۰۰۰، log2FC ‏۰٫۱۸، padj ‏3e-12): **معنادار** و بسیار مطمئن، چون با این پوشش و چهار فرد هم‌سو حتی تغییر ۱۳٪ (‏2^0.18) دیده می‌شود. ولی تغییر ۱۳٪ در بیشتر موارد از نظر زیستی کوچک است. گام بعد: در فهرست کوتاه نیاورید مگر ژن کلیدی باشد (برای نمونه آنزیم سرعت‌گیر)؛ با `lfcThreshold` بیازمایید.
- **ژن دوم** (baseMean ‏۱۲، log2FC ‏۴٫۵، padj ‏۰٫۰۸): **معنادار نیست**، ولی تغییر برآوردی ۲۲ برابر است. با شمار کم، برآورد نامطمئن است (log2FC کوچک‌شده‌ی آن احتمالاً بسیار کمتر است). شاید ژن تنها در یک یا دو نمونه روشن است. گام بعد: شمارش هر نمونه را ببینید (`plotCounts`)؛ اگر ژن جالب است، با qPCR یا عمق بیشتر بیازمایید. «معنادار نبود» یعنی «نشان داده نشد»، نه «تغییر نکرد».

---

## پاسخ ۷ (فکری): ‏PCA عجیب

گروه‌بندی PC1 با تیمار هیچ ربطی ندارد و هر گروه هر دو تیمار را دارد؛ پس منبع بزرگ‌ترین گوناگونی چیز **دیگری** است. گمان‌ها: **دسته‌ی فنی** (روز استخراج RNA، دستگاه یا مسیر flow cell، کیت)؛ **جنس** موش‌ها (ژن‌های Xist و کروموزوم Y را ببینید)؛ **سن** یا **قفس**؛ **کیفیت RNA** (RIN، سهم rRNA یا اینترون، 13/01)؛ یا **نمونه‌های جابه‌جا** (13/04). در جدول نمونه‌ها هر ستون فنی و زیستی را با PC1 بسنجید. اگر عامل روشن شد و درهم‌آمیخته با تیمار **نیست** (این‌جا نیست: هر گروه هر دو تیمار را دارد)، آن را در فرمول بیاورید: `~ batch + treatment`. تیمار روی PC4 یعنی اثرش کوچک‌تر از آن عامل است؛ با کنار گذاشتن آن عامل در مدل، آزمون تیمار توان بیشتری می‌گیرد.

</div>
