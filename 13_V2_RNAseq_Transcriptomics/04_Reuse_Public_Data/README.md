<div dir="rtl">

# ماژول ۰۴: بازتولید یک یافته‌ی منتشرشده (Reproducing a published result) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `13_V2_RNAseq_Transcriptomics` |
| **پیش‌نیاز** | ماژول [13/03](../03_Differential_Expression/) (اسکریپت‌های DESeq2)؛ Snakemake ([05](../../05_Reproducible_Work/))؛ PubMed ([11/06](../../11_V2_NCBI_Databases/06_Literature_PubMed_PMC/)) |
| **زمان تقریبی** | ۲٫۵ ساعت (یک درس، نزدیک به ۸۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏Snakemake 9.25.2 (محیط `workflow`)، R 4.5.3 و DESeq2 1.50.2 (`envs/rnaseq.yml`)، Python و pandas |
| **داده** | ‏GSE52778 (Himes و همکاران، ۲۰۱۴، PMID 24926665)؛ گردش کار خودش دانلود می‌کند |
| **منابع رایانه** | کل گردش کار ۶۵ ثانیه؛ بیشینه‌ی حافظه نزدیک به ۱ گیگابایت با `--cores 1` |
| **وضعیت** | ✅ اجرا شده (2026-10-28) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ادعاهای یک مقاله را به پرسش‌های سنجیدنی برگردانید.
2. با Snakemake از دانلود تا نتیجه یک گردش کار تکرارپذیر بسازید.
3. نتیجه را با مقاله بسنجید و تفاوت‌ها را توضیح دهید.
4. برچسب نمونه‌ها را با خود داده بیازمایید (این‌جا: جابه‌جایی احتمالی در دو فرد).

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ چکیده‌ی مقاله، Snakefile، سنجش با مقاله، امتیاز گلوکوکورتیکوئید.
2. ‏[02_exercises.md](02_exercises.md): ۶ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** [`workflow/Snakefile`](../99_scripts_data/04_Reuse_Public_Data/workflow/Snakefile)؛ [`check_labels.R`](../99_scripts_data/04_Reuse_Public_Data/scripts/check_labels.R)؛ [`paper_check.py`](../99_scripts_data/04_Reuse_Public_Data/scripts/paper_check.py)؛ اسکریپت‌های 13/03.
- **خروجی:** `results/de_dex_deseq2.tsv`، `results/labels.tsv`، `results/paper_check.txt`، تصویرها و `logs/`.

## یافته‌ی ماژول
هر هفت ژن نام‌برده در مقاله بازتولید شد (۴۷۴۳ ژن در برابر ۳۱۶ مقاله). در دو فرد، برچسب «آلبوترول» و «آلبوترول + دگزامتازون» به‌احتمال زیاد جابه‌جاست؛ همین ناهمخوانی 12/06 (Expression Atlas) را توضیح می‌دهد. نویسندگان آن را تأیید نکرده‌اند.

</div>
