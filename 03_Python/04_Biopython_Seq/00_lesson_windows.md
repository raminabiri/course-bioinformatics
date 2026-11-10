<div dir="rtl">

# درس (مسیر ویندوز): Biopython روی ویندوز؛ توالی، ترجمه، FASTA و FASTQ

**بخش:** `03_Python` · **ماژول:** `04_Biopython_Seq` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۳](../03_Python_Functions_Files/00_lesson_windows.md)؛ [آماده کردن ویندوز](../../windows/README.md) (Biopython و ژنوم K-12) · **زمان:** حدود ۲۰ دقیقه، و سپس [درس اصلی](01_lesson.md) · **ابزار:** Python 3 (ویندوز)، Biopython، PowerShell · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** اسکریپت دانلود، دو اسکریپت درس و همه‌ی کدهای پایتون روی سرور دوره **اجرا شدند** (2026-11-10، Biopython 1.87) و خروجی‌شان واقعی است. فرمان‌های PowerShell و پیام خطای ویژه‌ی ویندوز (بخش ۴) از **مستندات** و شبیه‌سازی‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

‏`Seq`، `translate(table=11, cds=True)`، `SeqIO` و `SeqRecord` در ویندوز همان‌اند. فرق‌ها:

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`conda activate bioinfo_course` | ‏Biopython را یک بار با `py -m pip install biopython` نصب کرده‌اید |
| ‏`fastq/*.fastq.gz` از `download.sh` | اسکریپت [`get_part01_data.py`](../../windows/get_part01_data.py) (گام ۰) |
| ‏`python3 $P/…` | ‏`py $P\…` |
| ‏`seqkit stats good.fastq` | یک سطر پایتون (بخش ۲) |
| ‏`head -n 3 rpoB.faa` | ‏`Get-Content rpoB.faa -TotalCount 3` |
| خطای `.gz` بی `gzip`: ‏`'utf-8' codec …` | در ویندوز: ‏`'charmap' codec …` (بخش ۴) |

---

## ۱. گام ۰: Biopython و داده‌ی FASTQ

در PowerShell:

<div dir="ltr">

```powershell
py -c "import Bio; print(Bio.__version__)"
cd $HOME\course
py $HOME\course-bioinformatics-main\windows\get_part01_data.py
$P = "$HOME\course-bioinformatics-main\03_Python\99_scripts_data\04_Biopython_Seq\scripts"
```

</div>

اگر سطر یکم `No module named 'Bio'` داد، نخست `py -m pip install biopython` ([آماده کردن ویندوز](../../windows/README.md)). نسخه‌ی شما ممکن است 1.87 یا تازه‌تر باشد. درس اصلی با 1.88 و این درس با 1.87 اجرا شد، با خروجی یکسان.

**خروجی واقعی `get_part01_data.py`** (سرور دوره، ۲۷ ثانیه):

<div dir="ltr">

```text
downloading fastq/minigut_R1.fastq.gz ...
10691078950a63150244e7517ded803d  fastq/minigut_R1.fastq.gz  (3,323,528 bytes)
downloading fastq/minigut_R2.fastq.gz ...
090cf62530b6874f7fc746ed550bd6bf  fastq/minigut_R2.fastq.gz  (3,398,619 bytes)
downloading fastq/minigut_sample2_R1.fastq.gz ...
1d088537e5180930578097a999d2ca72  fastq/minigut_sample2_R1.fastq.gz  (1,599,430 bytes)
downloading fastq/minigut_sample2_R2.fastq.gz ...
83a9588a59325f3798fc2f8d8ef1f3ea  fastq/minigut_sample2_R2.fastq.gz  (1,806,457 bytes)
downloading host_chr21_region.fa ...
68b50cfb970f4c490bf87388b7f43b3f  host_chr21_region.fa  (510,011 bytes)
copied ground_truth.tsv
```

</div>

هر پنج MD5 درست همان فایل‌های بخش ۰۱ لینوکسی است. این اسکریپت همان کار `download.sh` را بی `curl` می‌کند و اگر GitHub کند بود، از آینه‌ی jsDelivr می‌گیرد. (در ویندوز `fastq/` با `\` نشان داده می‌شود؛ پایتون هر دو را می‌پذیرد.)

> 💡 **فایل `.gz` را باز نکنید.** ویندوز ۱۱ و 7-Zip می‌توانند `.gz` را باز کنند، ولی لازم نیست: درس اصلی آن‌ها را با `gzip.open` در خود پایتون می‌خواند.

---

## ۲. اجرای اسکریپت‌ها

بخش‌های ۲ تا ۴ [درس اصلی](01_lesson.md) (`Seq`، کدون GTG، `SeqIO.read`) را در `>>>` یا فایل IDLE (کنار داده در `$HOME\course`) بنویسید. سپس:

<div dir="ltr">

```powershell
py $P\fastq_quality.py fastq\minigut_sample2_R1.fastq.gz good.fastq 30
py -c "from Bio import SeqIO; L = [len(r) for r in SeqIO.parse('good.fastq', 'fastq')]; print(len(L), sum(L), min(L), max(L))"
py $P\extract_gene.py ecoli_k12.fna rpoB 4181245 4185273 +
py $P\extract_gene.py ecoli_k12.fna gyrA 2336793 2339420 -
Get-Content rpoB.faa -TotalCount 3
```

</div>

**خروجی واقعی** (سرور دوره، 2026-11-10؛ `fastq_quality.py` ‏۰٫۶ ثانیه و ۱۰۶ مگابایت حافظه):

<div dir="ltr">

```text
reads: 24993
bases: 3773943
mean read length: 151.0
reads with mean Q >= 30: 24820 (99.3%)
24820 3747820 151 151
rpoB: 4029 nt, 1342 aa, starts with MVYSYTEKKR
gyrA: 2628 nt, 875 aa, starts with MSDLAREITP
>rpoB translated with table 11, 1342 aa
MVYSYTEKKRIRKDFGKRPQVLDVPYLLSIQLDSFQKFIEQDPEGQYGLEAAFRSVFPIQ
SYSGNSELQYVSYRLGEPVFDVQECQIRGVTYSAPLRVKLRLVIYEREAPEGTVKDIKEQ
```

</div>

سطر پنجم جای `seqkit stats` است: ‏۲۴٬۸۲۰ رید، ۳٬۷۴۷٬۸۲۰ باز، کوتاه‌ترین و بلندترین ۱۵۱. همان عددهای جدول seqkit در درس اصلی. بقیه هم همان خروجی درس اصلی است.

‏`rpoB.faa` را می‌توانید با Notepad باز کنید و پروتئین را در BLAST وب (بخش ۰۰) بچسبانید.

---

## ۳. پوشه‌ی `fastq` در کد

در کدی که خودتان می‌نویسید، نشانی را همان‌گونه که درس اصلی نوشته بنویسید: `"fastq/minigut_R1.fastq.gz"`، با `/`. پایتون ویندوز `/` را می‌پذیرد و دام `\` ([ماژول ۰۳، بخش ۴](../03_Python_Functions_Files/00_lesson_windows.md)) پیش نمی‌آید. در PowerShell (ورودی اسکریپت‌ها) هر دو کار می‌کنند.

---

## ۴. اشتباه ۳ درس، در ویندوز پیام دیگری دارد

اشتباه ۳ درس اصلی: باز کردن `.gz` بی `gzip`:

<div dir="ltr">

```python
next(SeqIO.parse("fastq/minigut_sample2_R1.fastq.gz", "fastq"))
```

</div>

در لینوکس پیام `'utf-8' codec can't decode byte 0x8b …` بود. پایتون ویندوز فایل متنی را به‌طور پیش‌فرض با کدگذاری ویندوز (**cp1252**) می‌خواند، نه UTF-8. پس پیام فرق دارد. با همین کدگذاری روی سرور شبیه‌سازی کردیم:

<div dir="ltr">

```text
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 152: character maps to <undefined>
```

</div>

✍️ روی ویندوز (شبیه‌سازی، نه اجرا روی ویندوز). **معنی یکی است:** پایتون بایت‌های فشرده را مانند متن خواند. چاره همان است: `gzip.open(…, "rt")`.

> 📘 **برای کنجکاوها:** چون کدگذاری پیش‌فرض ویندوز UTF-8 نیست، اگر روزی فایل متنی با نویسه‌های غیرانگلیسی (برای نمونه نام فارسی) خواندید و حروف درهم دیدید، بنویسید `open(path, encoding="utf-8")`. فایل‌های FASTA، FASTQ و GFF این دوره تنها نویسه‌ی انگلیسی دارند و این مشکل را ندارند.

دو اشتباه دیگر درس (`TranslationError: First codon 'TTA' is not a start codon` و `More than one record found in handle`) در ویندوز همان‌اند.

---

## ۵. جمع‌بندی

- داده‌ی FASTQ بخش ۰۱ با `get_part01_data.py`؛ همان MD5ها.
- ‏`py $P\…` برای اسکریپت‌ها، `Get-Content -TotalCount` به جای `head`، یک سطر `SeqIO` به جای `seqkit stats`.
- در کد، نشانی با `/`.
- ‏`.gz` بی `gzip` در ویندوز خطای `'charmap' codec` می‌دهد؛ همان اشتباه، همان چاره.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| نسخه‌ی Biopython | ‏`py -c "import Bio; print(Bio.__version__)"` |
| داده‌ی FASTQ بخش ۰۱ | ‏`py …\windows\get_part01_data.py` |
| آمار ساده‌ی یک FASTQ | ‏`py -c "from Bio import SeqIO; L = [len(r) for r in SeqIO.parse('f.fastq', 'fastq')]; print(len(L), sum(L))"` |
| سه سطر نخست | ‏`Get-Content f -TotalCount 3` |
| خواندن متن با UTF-8 | ‏`open(p, encoding="utf-8")` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| کدگذاری (encoding) | قاعده‌ی تبدیل بایت‌ها به نویسه‌ها؛ مانند UTF-8 یا cp1252 |
| ‏cp1252 | کدگذاری پیش‌فرض ویندوز برای زبان‌های اروپایی |
| آینه (mirror) | نشانی دیگری که همان فایل را دارد |

---

## منابع

### راهنما و درس رایگان
- ‏Biopython Tutorial and Cookbook (نصب روی ویندوز با pip): https://biopython.org/DIST/docs/tutorial/Tutorial.html
- ‏Python documentation — *Using Python on Windows* (UTF-8 mode): https://docs.python.org/3/using/windows.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (فصل Biopython)

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#فیلم‌های-آموزشی).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌ها و کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. فرمان‌های PowerShell از مستندات‌اند و پیام بخش ۴ شبیه‌سازی است (✍️).

</div>
