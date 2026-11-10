<div dir="rtl">

# مسیر ویندوز: یادگیری بی لینوکس

این صفحه برای کسی است که **تنها ویندوز** دارد و نمی‌خواهد (یا نمی‌تواند) لینوکس یا WSL نصب کند. بیشتر کارهای این دوره را می‌شود با سه گونه ابزار روی خود ویندوز انجام داد:

1. **سرورهای وب و Galaxy:** تحلیل روی سرور دیگران، با مرورگر (ResFinder، CARD، BV-BRC، InterPro، UCSC، cBioPortal…).
2. **برنامه‌هایی که نسخه‌ی ویندوزی دارند:** BLAST+، IGV، MEGA، MAFFT، IQ-TREE، UGENE، PyMOL، Cytoscape و…
3. **پایتون و R روی ویندوز:** اسکریپت‌های پایتون این دوره (با Biopython، pandas و requests) روی ویندوز همان خروجی لینوکس را می‌دهند.

## ساختار

- هر ماژولی که مسیر ویندوز دارد، یک فایل **`00_lesson_windows.md`** دارد. آن را **پیش از** درس‌های لینوکسی همان ماژول بخوانید.
- داستان، مفهوم‌ها، داده و **پاسخ معلوم** همان درس لینوکسی است. فایل ویندوزی آن‌ها را تکرار نمی‌کند و به بخش درستشان پیوند می‌دهد. تنها **گام‌ها** فرق دارند.
- تمرین‌ها مشترک‌اند. زیر هر تمرین، کنار راهنمایی لینوکسی، یک راهنمایی **«ویندوز»** هست.
- پس از مسیر ویندوز، اگر خواستید، درس لینوکسی همان ماژول را بخوانید: همان کار را با خط فرمان، تکرارپذیر و برای داده‌ی بزرگ انجام می‌دهید و به همان عددها می‌رسید.

> ✍️ **وضعیت آزمون:** گام‌هایی که تنها روی ویندوز یا در وب انجام می‌شوند (نصب برنامه‌ها، فرستادن فایل به ResFinder و…) از **مستندات** نوشته شده‌اند و روی ویندوز آزموده **نشده‌اند**. هر جا خروجی واقعی آمده، از اجرای همان کد پایتون یا همان برنامه (BLAST+) روی سرور دوره است. این کدها روی ویندوز یکسان کار می‌کنند. اگر جایی روی ویندوز فرق داشت، آن را گزارش کنید.

## آماده کردن ویندوز (یک بار)

✍️ **از مستندات هر برنامه:**

| برنامه | نصب | سنجیدن (در PowerShell) |
| :--- | :--- | :--- |
| ‏**PowerShell** | در ویندوز ۱۰ و ۱۱ هست: منوی Start ← «PowerShell» | ـــ |
| ‏**Python 3** | ‏https://www.python.org/downloads/windows/ ؛ در نصب‌کننده گزینه‌ی **Add python.exe to PATH** را بزنید | ‏`py --version` |
| ‏Biopython، pandas، requests | ‏`py -m pip install biopython pandas requests` | ‏`py -c "import Bio; print(Bio.__version__)"` |
| ‏**BLAST+** | ‏`ncbi-blast-2.17.0+-win64.exe` از https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/LATEST/ ؛ راهنمای NCBI: https://www.ncbi.nlm.nih.gov/books/NBK52637/ | ‏`blastn -version` (در پنجره‌ی **تازه**ی PowerShell) |
| ‏**IGV** (ماژول 12/03) | ‏https://igv.org/download | ـــ |
| ‏**R** و RStudio (بخش ۰۴) | ‏https://cran.r-project.org و https://posit.co/download/rstudio-desktop/ | ـــ |
| ‏**7-Zip** (برای فایل‌های `.gz`) | ‏https://www.7-zip.org (ویندوز ۱۱ تازه خودش برخی فایل‌های فشرده را باز می‌کند) | ـــ |

**چند فرق با درس‌های لینوکسی:**
- به جای `python3` بنویسید **`py`** (یا `python`).
- مسیر پوشه‌ها با `\` است (`genomes\isoA.fna`)؛ پایتون هر دو `\` و `/` را می‌پذیرد.
- دستور بلند را **در یک سطر** بنویسید. `\` پایان سطر در لینوکس در PowerShell کار نمی‌کند (آن‌جا نویسه‌ی ادامه `` ` `` است).
- فایل‌های جدولی (`.tsv`) را با **Excel** باز کنید: Data ← From Text/CSV، جداکننده Tab.
- ابزارهای `grep`، `awk`، `cut` و `sort` در ویندوز نیستند. همان کار را با Excel (فیلتر و مرتب‌سازی) یا با چند خط پایتون انجام می‌دهیم.

## داده‌ی پایه: ژنوم *E. coli* K-12

بسیاری از ماژول‌ها ژنوم K-12 بخش ۰۱ را می‌خواهند. در لینوکس آن را `download.sh` با `curl` و `gunzip` می‌گیرد. در ویندوز، اسکریپت پایتون [`get_k12_genome.py`](get_k12_genome.py) همان دو فایل را می‌گیرد و باز می‌کند. فرض این است که دوره را از GitHub (دکمه‌ی **Code ← Download ZIP**) گرفته و در پوشه‌ی خانه‌تان باز کرده‌اید، همانند `~/course-bioinformatics-main` در درس‌های لینوکسی:

<div dir="ltr">

```powershell
mkdir $HOME\course; cd $HOME\course
py $HOME\course-bioinformatics-main\windows\get_k12_genome.py
```

</div>

**خروجی واقعی** (اجرا روی سرور دوره، 2026-10-27؛ ۱۱ ثانیه):

<div dir="ltr">

```
downloading ecoli_k12.fna ...
92c997bcd88e983ffdb21b2712ed3736  ecoli_k12.fna  (4,699,745 bytes)
downloading ecoli_k12.gff ...
837628601d3bbf74c218716d7ea2df86  ecoli_k12.gff  (2,314,238 bytes)
```

</div>

دو عدد MD5 درست همان فایل‌های بخش ۰۱ لینوکسی است: داده یکی است.

**ریدهای بخش ۰۱** (دو نمونه‌ی شبیه‌سازی‌شده‌ی روده، ۴ فایل `fastq\*.fastq.gz`)، ناحیه‌ی کروموزوم ۲۱ انسان و `ground_truth.tsv` را اسکریپت [`get_part01_data.py`](get_part01_data.py) در همان پوشه می‌گیرد (حدود ۱۰ مگابایت؛ روی سرور دوره ۲۷ ثانیه، همان MD5های `download.sh`):

<div dir="ltr">

```powershell
cd $HOME\course
py $HOME\course-bioinformatics-main\windows\get_part01_data.py
```

</div>

## ماژول‌هایی که مسیر ویندوز دارند

| ماژول | فایل ویندوزی | ابزارها |
| :--- | :--- | :--- |
| ‏03/01 آغاز پایتون | [00_lesson_windows.md](../03_Python/01_Python_Start/00_lesson_windows.md) | پایتون (`py`)، PowerShell، IDLE |
| ‏03/02 فهرست، حلقه و دیکشنری | [00_lesson_windows.md](../03_Python/02_Python_Lists_Loops/00_lesson_windows.md) | پایتون (`py`)، IDLE |
| ‏03/03 تابع و فایل؛ GFF و FASTA | [00_lesson_windows.md](../03_Python/03_Python_Functions_Files/00_lesson_windows.md) | پایتون (`py`)، PowerShell (`Get-Content`، `Select-String`)، IDLE، Excel |
| ‏03/04 ‏Biopython (۱)؛ توالی، FASTA و FASTQ | [00_lesson_windows.md](../03_Python/04_Biopython_Seq/00_lesson_windows.md) | پایتون (Biopython)، `get_part01_data.py`، PowerShell |
| ‏03/05 ‏Biopython (۲)؛ GenBank و Entrez | [00_lesson_windows.md](../03_Python/05_Biopython_GenBank/00_lesson_windows.md) | پایتون (Biopython، `Bio.Entrez`)، PowerShell |
| ‏03/06 جدول و نمودار با pandas | [00_lesson_windows.md](../03_Python/06_Pandas/00_lesson_windows.md) | پایتون (pandas، matplotlib، openpyxl)، Excel |
| ‏04/01 نصب و وارسی بسته‌های R | [00_lesson_windows.md](../04_R_Packages/01_Install_Packages/00_lesson_windows.md) | R (CRAN)، `install.packages`، BiocManager، PowerShell |
| ‏04/02 اجرای اسکریپت آماده‌ی R | [00_lesson_windows.md](../04_R_Packages/02_Run_Rscript/00_lesson_windows.md) | R، PowerShell (`$LASTEXITCODE`، `Start-Process`، `-replace`، `Compare-Object`) |
| ‏04/03 ‏DESeq2، vegan و ggtree | [00_lesson_windows.md](../04_R_Packages/03_Bioc_Examples/00_lesson_windows.md) | ‏R (DESeq2، vegan، ggtree)، پایتون (pandas)، Excel، PowerShell |
| ‏04/04 اسکریپت‌های R در خط لوله | [00_lesson_windows.md](../04_R_Packages/04_R_in_Pipelines/00_lesson_windows.md) | ‏R، PowerShell (`run_all.ps1`؛ ✍️ آزموده‌نشده) |
| ‏07/01 اسمبلی و کیفیت ژنوم | [00_lesson_windows.md](../07_Bacterial_Genomics/01_Assembly_Quality/00_lesson_windows.md) | پایتون (`debruijn_toy.py`، `repeat_report.py`، `asm_stats.py`)، Galaxy (Shovill، QUAST، CheckM2)، WebQUAST |
| ‏08/01 ژن‌ها و جهش‌های مقاومت | [00_lesson_windows.md](../08_AMR_Virulence_Phylogeny/01_AMR_Resistance_Genes/00_lesson_windows.md) | پایتون (Biopython)، BLAST+، ResFinder و CARD RGI (وب) |
| ‏08/02 عامل‌های بیماری‌زایی | [00_lesson_windows.md](../08_AMR_Virulence_Phylogeny/02_Virulence_Factors/00_lesson_windows.md) | پایتون، BLAST+ و VFDB، Excel، VirulenceFinder (وب) |
| ‏08/03 عنصرهای متحرک و CRISPR | [00_lesson_windows.md](../08_AMR_Virulence_Phylogeny/03_Mobile_Elements_CRISPR/00_lesson_windows.md) | پایتون (Biopython)، BLAST+ و PlasmidFinder، Excel، ResFinder و CRISPRCasFinder (وب) |
| ‏08/04 درخت‌های فیلوژنتیک | [00_lesson_windows.md](../08_AMR_Virulence_Phylogeny/04_Phylogenetic_Trees/00_lesson_windows.md) | ‏MAFFT، IQ-TREE، R در RStudio (ape، ggtree)، پایتون؛ iTOL و MEGA (اختیاری) |

ماژول‌های دیگر (بخش‌های ۰۳، ۰۴، ۰۶ تا ۰۹، ۱۱، ۱۲ و بخش‌های تازه‌تر) به‌تدریج افزوده می‌شوند. بخش‌های ۰۱ (لینوکس)، ۰۲ (بایولینوکس)، Snakemake و بخش ۲۰ (خط لوله و HPC) مسیر ویندوز ندارند.

</div>
