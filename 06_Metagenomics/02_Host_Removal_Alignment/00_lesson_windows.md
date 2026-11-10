<div dir="rtl">

# درس (مسیر ویندوز): برداشتن DNA میزبان، بی لینوکس

**بخش:** `06_Metagenomics` · **ماژول:** `02_Host_Removal_Alignment` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۱](../01_Read_QC_Trimming/00_lesson_windows.md) (ریدهای بریده از Galaxy)؛ مفهوم‌ها از [درس اصلی](01_lesson.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** Python 3؛ Bowtie2 و samtools در Galaxy · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** اسکریپت‌های پایتون این درس (`spike_human.py`، `read_origins.py`) روی سرور دوره **اجرا شدند** (2026-11-10)، و برای عددهای گام ۴، **Bowtie2 2.5.5 روی سرور** با همان تنظیمی که در Galaxy می‌دهید اجرا شد؛ خروجی‌ها واقعی‌اند. گام‌های Galaxy از **مستندات** نوشته شده‌اند و آزموده نشده‌اند.

---

## در یک نگاه

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`curl` برای دو ناحیه‌ی انسانی | یک سطر پایتون (گام ۰) |
| ‏`bowtie2-build`، `bowtie2`، `samtools` | **نسخه‌ی ویندوزی ساده ندارند** ← ‏**Bowtie2 و samtools در Galaxy** (گام‌های ۲ و ۴) |
| ‏`make_spiked_sample.sh` (wgsim + seqkit) | ‏[`spike_human.py`](../../windows/spike_human.py) (گام ۳) |
| ‏`samtools view -f 12 … \| samtools fastq` | گزینه‌ی **unaligned reads** در Bowtie2ی Galaxy (همان `--un-conc`) |
| ‏`zcat \| awk \| sed \| sort \| uniq -c` | ‏[`read_origins.py`](../../windows/read_origins.py) (گام ۵) |

**پیش از خواندن:** از درس اصلی بخش‌های **۱ و ۲** (داستان؛ ایده، شاخص، FLAG) را بخوانید.

---

## ۱. گام ۰: دو ناحیه‌ی انسانی

<div dir="ltr">

```powershell
cd $HOME\meta
mkdir host\ref, host\spiked, host\clean
$W = "$HOME\course-bioinformatics-main\windows"
Copy-Item $HOME\course\host_chr21_region.fa host\ref\
py -c "import urllib.request; urllib.request.urlretrieve('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000001.11&rettype=fasta&retmode=text&seq_start=100000001&seq_stop=100300000', 'host/ref/human_chr1_region.fa')"
```

</div>

| فایل | چیست (همان درس اصلی) |
| :--- | :--- |
| ‏`host_chr21_region.fa` | ‏۵۰۰ کیلوباز کروموزوم ۲۱؛ **شاخص میزبان** از همین ساخته می‌شود (از `get_part01_data.py`) |
| ‏`human_chr1_region.fa` | ‏۳۰۰ کیلوباز کروموزوم ۱؛ در شاخص **نیست** (آزمونِ «انسانی که میزبان نمی‌شناسد») |

---

## ۲. گام ۱ و ۲: Bowtie2 در Galaxy روی `minigut`

✍️ از مستندات Galaxy:

1. ‏**Upload** ← `host_chr21_region.fa` (نوع **fasta**). ریدهای بریده‌ی `minigut` از ماژول ۰۱ در همان تاریخچه‌اند.
2. ابزار **Bowtie2** (*map reads against reference genome*):

| در درس (خط فرمان) | در فرم Galaxy |
| :--- | :--- |
| ‏`bowtie2-build host_chr21_region.fa …` | ‏**Will you select a reference genome from your history or use a built-in index?** ← Use a genome from the history and build index؛ `host_chr21_region.fa` |
| ‏`-1 … -2 …` | ‏**Is this single or paired library** ← Paired-end؛ R1 و R2 |
| ‏`--very-sensitive` | ‏**Select analysis mode** ← 1: Default setting only ← **Very sensitive end-to-end** |
| ‏`samtools view -b -f 12 … \| samtools fastq` | ‏**Write unaligned reads (in fastq format) to separate file(s)** ← Yes |
| گزارش `2> …bowtie2.log` | ‏**Save the bowtie2 mapping statistics to the history** ← Yes |

3. ‏**Run**. خروجی‌ها: یک BAM مرتب‌شده، جفت‌های **هم‌تراز نشده** (پاک)، و گزارش آماری.

**انتظار** (درس اصلی، بخش ۴): برای `minigut` نزدیک به هیچ ریدی بر chr21 نمی‌نشیند (نمونه‌ی ما انسانی نیست). گزارش آماری Galaxy همان قالب گزارش `bowtie2` درس است.

برای `samtools flagstat` (بخش ۶ درس): ابزار **Samtools flagstat** روی BAM خروجی.

---

## ۳. گام ۳: نمونه‌ی آزمایشی، بی wgsim

درس اصلی با `wgsim` ریدهای انسانی **با مبدأ معلوم** می‌سازد و به `minigut` می‌افزاید. `wgsim` در ویندوز نیست. [`spike_human.py`](../../windows/spike_human.py) همین کار را با پایتون (تنها کتابخانه‌ی استاندارد) می‌کند: از هر ناحیه ۵٬۰۰۰ جفت رید ۱۲۶ بازی، با قطعه‌های ~۳۵۰ بازی، خطای ۰٫۲٪، و نامی که مبدأ را می‌گوید (`HUMAN_chr21_…`، `HUMAN_chr1_…`).

ریدهای بریده‌ی `minigut` را از Galaxy (ماژول ۰۱) در `qc\trimmed` دانلود کرده باشید (`minigut_R1.fastq.gz`، `minigut_R2.fastq.gz`). سپس:

<div dir="ltr">

```powershell
py $W\spike_human.py qc\trimmed\minigut_R1.fastq.gz qc\trimmed\minigut_R2.fastq.gz host\spiked\minigut_spiked chr21=host\ref\host_chr21_region.fa chr1=host\ref\human_chr1_region.fa 5000
py $W\read_origins.py host\spiked\minigut_spiked_R1.fastq.gz
```

</div>

**خروجی واقعی** (سرور دوره، روی ریدهای بریده‌ی درس اصلی؛ ۸ ثانیه، ۱۵ مگابایت):

<div dir="ltr">

```text
wrote host\spiked\minigut_spiked_R1.fastq.gz and host\spiked\minigut_spiked_R2.fastq.gz: microbial reads + 5000 human pairs from each of chr21, chr1
== host\spiked\minigut_spiked_R1.fastq.gz
    5000 HUMAN_chr1
    5000 HUMAN_chr21
   21018 NC_000913.3
   28827 NC_006347.1
```

</div>

**پاسخ معلوم:** ۱۰٬۰۰۰ جفت انسانی (نیمی در شاخص، نیمی نه) و ۴۹٬۸۴۵ جفت میکروبی؛ همان ترکیب درس اصلی. (اگر ریدهای بریده‌ی شما از Galaxy کمی فرق دارند، دو سطر `NC_` هم کمی فرق می‌کنند.)

> ‏`spike_human.py` با بذر ثابت (`42`) کار می‌کند، پس برای یک ورودی **همیشه همان فایل** را می‌سازد (روی سرور دو اجرا، MD5 یکسان). ولی شبیه‌ساز ساده‌تری از `wgsim` است (بی جهش و indel ژنومی، کیفیت یکنواخت). پس عددهای گام ۴ کمی با درس اصلی فرق دارند؛ **ایده و نتیجه‌گیری همان است.**

---

## ۴. گام ۴ و ۵: برداشتن میزبان از نمونه‌ی آزمایشی

‏`host\spiked\minigut_spiked_R1.fastq.gz` و `_R2` را به Galaxy بفرستید (Upload، نوع fastqsanger.gz) و همان Bowtie2 گام ۲ را رویشان اجرا کنید. جفت‌های **unaligned** را دانلود کنید و با نام `host\clean\minigut_spiked_R1.fastq.gz` و `_R2` ذخیره کنید. سپس:

<div dir="ltr">

```powershell
py $W\read_origins.py host\clean\minigut_spiked_R1.fastq.gz
```

</div>

**خروجی واقعی** (Bowtie2 2.5.5 روی سرور با `--very-sensitive` و `--un-conc-gz`، همان کار گزینه‌ی Galaxy):

<div dir="ltr">

```text
8.51% overall alignment rate
== host\clean\minigut_spiked_R1.fastq.gz
    4963 HUMAN_chr1
       4 HUMAN_chr21
   21018 NC_000913.3
   28827 NC_006347.1
```

</div>

| مبدأ | در ورودی | پس از برداشتن | یعنی |
| :--- | --: | --: | :--- |
| ‏`HUMAN_chr21` | ‏۵٬۰۰۰ | ‏**۴** | ‏۹۹٫۹٪ ریدهای انسانیِ **درون شاخص** برداشته شدند |
| ‏`HUMAN_chr1` | ‏۵٬۰۰۰ | ‏**۴٬۹۶۳** | نزدیک به همه **ماندند**: میزبانی که در شاخص نیست، دیده نمی‌شود |
| ‏میکروبی | ‏۴۹٬۸۴۵ | ‏۴۹٬۸۴۵ | هیچ رید میکروبی از دست نرفت |

**همان درس درس اصلی (بخش ۷):** برداشتن میزبان تنها به اندازه‌ی **کامل بودن شاخص** خوب است. در درس اصلی با wgsim ‏۴٬۷۲۵ رید chr1 ماند و هیچ رید chr21؛ این‌جا ۴٬۹۶۳ و ۴. فرق‌ها از شبیه‌ساز (wgsim جهش و indel هم می‌افزاید و برخی ریدهای chr1 به تکرارهای مشترک chr21 می‌نشینند) و از قاعده‌ی گزینش است: درس اصلی تنها جفت‌هایی را نگه می‌دارد که **هر دو** رید هم‌تراز نشده‌اند (`-f 12`)؛ گزینه‌ی Galaxy (`--un-conc`) جفت‌هایی را که **هم‌تراز هماهنگ** (concordant) نشده‌اند.

---

## ۵. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| شاخص Galaxy از ژنوم کامل انسان (hg38 داخلی) به جای chr21 | نزدیک به همه‌ی ریدهای chr1 هم برداشته می‌شوند | برای این آزمایش، شاخص را از `host_chr21_region.fa` تاریخچه بسازید (در کار واقعی، ژنوم **کامل** میزبان درست است) |
| دانلود BAM به جای جفت‌های unaligned | ‏`read_origins.py` چیزی نمی‌شمارد یا خطای gzip | خروجی «unaligned reads» را بگیرید |
| نام فایل‌های Galaxy (`Galaxy7-[…].fastqsanger.gz`) | ‏`No such file or directory` | پس از دانلود، نام را عوض کنید |
| ‏`spike_human.py` روی ریدهای **خام** | شمار میکروبی ۵۰٬۰۰۰ به جای ۴۹٬۸۴۵ | ریدهای **بریده** ماژول ۰۱ را بدهید (یا بدانید که عددها فرق می‌کنند) |

✍️ پیام‌های این جدول از مستندات‌اند.

---

## ۶. جمع‌بندی

- ‏Bowtie2 و samtools در ویندوز: Galaxy؛ شاخص از FASTA تاریخچه، `--very-sensitive`، و خروجی unaligned.
- نمونه‌ی آزمایشی با پاسخ معلوم: `spike_human.py`؛ شمارش مبدأ: `read_origins.py`.
- نتیجه، همان درس اصلی: ریدهای انسانیِ درون شاخص نزدیک به همه برداشته می‌شوند؛ آن‌هایی که در شاخص نیستند، می‌مانند.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| ساختن نمونه‌ی آزمایشی | ‏`py $W\spike_human.py R1 R2 out chr21=… chr1=… 5000` |
| شمردن ریدها بر پایه‌ی مبدأ | ‏`py $W\read_origins.py reads.fastq.gz` |
| برداشتن میزبان | ‏Galaxy ← Bowtie2 ← Write unaligned reads: Yes |
| آمار BAM | ‏Galaxy ← Samtools flagstat |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏unaligned / unmapped | ریدی که بر مرجع ننشست؛ این‌جا همان رید «پاک» |
| ‏concordant | جفتی که هر دو رید با جهت و فاصله‌ی درست بر مرجع نشستند |
| بذر (seed) | عدد آغاز مولد تصادفی؛ بذر ثابت = نتیجه‌ی یکسان |

---

## منابع

### مقاله
- ‏Langmead B, Salzberg SL (2012). *Fast gapped-read alignment with Bowtie 2.* Nature Methods 9:357–359. https://doi.org/10.1038/nmeth.1923

### راهنما و درس رایگان
- ‏Galaxy Training — *Mapping*: https://training.galaxyproject.org/training-material/topics/sequence-analysis/tutorials/mapping/tutorial.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#منابع)؛ آموزش Galaxy بالا فیلم همراه دارد.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌های پایتون و Bowtie2 (برای عددهای گام ۴) در 2026-11-10 روی سرور دوره اجرا شدند. گام‌های Galaxy از مستندات‌اند (✍️).

</div>
