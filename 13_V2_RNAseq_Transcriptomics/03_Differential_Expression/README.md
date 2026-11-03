<div dir="rtl">

# ماژول ۰۳: بیان افتراقی (DESeq2, edgeR, limma-voom) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `13_V2_RNAseq_Transcriptomics` |
| **پیش‌نیاز** | ماژول [13/02](../02_Alignment_Quantification/) (`gene_counts_salmon.tsv`)؛ GSE52778 ([11/04](../../11_V2_NCBI_Databases/04_GEO/))؛ Expression Atlas ([12/06](../../12_V2_Global_Databases_Browsers/06_Expression_Cancer_Portals/))؛ `Rscript` ([04](../../04_R_Packages/)) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏R 4.5.3، DESeq2 1.50.2، apeglm 1.32.0، edgeR 4.10.7، limma 3.68.5 (`envs/rnaseq.yml`) |
| **داده** | جدول شمارش شبیه‌سازی‌شده (پاسخ معلوم)؛ GSE52778 واقعی (۸ نمونه، ۴ فرد) با [`download.sh`](../99_scripts_data/03_Differential_Expression/data/download.sh) |
| **منابع رایانه** | شبیه‌سازی ۶ ثانیه؛ GSE52778 ‏۱۹ ثانیه و نزدیک به ۱ گیگابایت حافظه (بارگذاری DESeq2 خود ۵۹۰ مگابایت) |
| **وضعیت** | ✅ اجرا شده (2026-10-28) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. هم‌سان‌سازی، پراکندگی و آزمون DESeq2 را به زبان ساده بگویید و فرض آن را بشناسید.
2. فرمول طراحی بنویسید و سطح مرجع را درست بگذارید.
3. ‏log2FC، padj و shrinkage را بخوانید؛ PCA، MA و volcano بسازید.
4. نتیجه را با پاسخ معلوم، edgeR، limma-voom و Expression Atlas بسنجید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ DESeq2 روی داده‌ی شبیه‌سازی‌شده و GSE52778، فرمول طراحی، PCA، روش‌های دیگر.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** `gene_counts_salmon.tsv` (13/02)؛ داده‌ی GSE52778؛ اسکریپت‌های [`de_simulated.R`](../99_scripts_data/03_Differential_Expression/scripts/de_simulated.R)، [`de_gse52778.R`](../99_scripts_data/03_Differential_Expression/scripts/de_gse52778.R)، [`compare_methods.R`](../99_scripts_data/03_Differential_Expression/scripts/compare_methods.R) (R ساده؛ روی ویندوز هم).
- **خروجی:** `de_dex_deseq2.tsv` (ورودی بخش ۱۴، غنی‌سازی)؛ تصویرهای PCA، MA و volcano.

</div>
