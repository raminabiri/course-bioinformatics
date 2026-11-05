<div dir="rtl">

# ماژول ۰۵: ‏RNA-seq باکتری (Bacterial RNA-seq) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `13_V2_RNAseq_Transcriptomics` |
| **پیش‌نیاز** | ماژول‌های [13/02](../02_Alignment_Quantification/) و [13/03](../03_Differential_Expression/)؛ کینولون‌ها و QRDR ([08/01](../../08_AMR_Virulence_Phylogeny/01_AMR_Resistance_Genes/)) |
| **زمان تقریبی** | ۲٫۵ ساعت (یک درس، نزدیک به ۸۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏Bowtie2 2.5.5، samtools 1.25، featureCounts 2.1.1، R 4.5.3 و DESeq2 1.50.2 (`envs/rnaseq.yml`) |
| **داده** | ژنوم و GFF ‏E. coli K-12 MG1655 از NCBI RefSeq ‏(GCF_000005845.2) و شش نمونه‌ی شبیه‌سازی‌شده با پاسخ معلوم (پاسخ SOS به سیپروفلوکساسین)؛ `make_data.sh` می‌سازد (نزدیک به ۳۰ مگابایت) |
| **منابع رایانه** | داده ۱۹ ثانیه، هم‌ترازی ۲۵ ثانیه، DESeq2 ‏۶ ثانیه؛ بیشینه‌ی حافظه ۸۶۷ مگابایت |
| **وضعیت** | ✅ اجرا شده (2026-10-28؛ تمرین‌ها 2026-11-05) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. تفاوت‌های RNA-seq باکتری و یوکاریوت (اینترون، poly(A)، اپرون، تراکم ژن) و پیامد هر کدام را بگویید.
2. ریدهای باکتری را با Bowtie2 هم‌تراز و با featureCounts روی GFF، با جهت درست، شمارش کنید.
3. سهم rRNA مانده و ریدهای چندجایی را بسنجید.
4. پاسخ SOS را با DESeq2 بیابید و اپرون‌ها را در نتیجه ببینید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ Bowtie2، جهت کتابخانه، rRNA، DESeq2، رید میان ژن‌های اپرون.
2. ‏[02_exercises.md](02_exercises.md): ۶ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** [`make_data.sh`](../99_scripts_data/05_Bacterial_RNAseq/data/make_data.sh)؛ [`simulate_bacterial.py`](../99_scripts_data/05_Bacterial_RNAseq/scripts/simulate_bacterial.py)؛ [`de_bacterial.R`](../99_scripts_data/05_Bacterial_RNAseq/scripts/de_bacterial.R).
- **خروجی:** `bam/*.bam`، `counts/gene_counts.txt`، `de_cip.tsv`.

## یافته‌ی ماژول
هر ۱۲ ژن SOS یافته شد (۱۸ از ۲۵ ژن تغییرکرده، ۳ مثبت کاذب نزدیک مرز). ژن‌های یک اپرون با هم بالا و پایین می‌روند، و ریدهای میان آن‌ها هم؛ پس ۱۱ ژن اپرون S10 یازده شاهد جدا نیستند.

</div>
