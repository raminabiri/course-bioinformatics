<div dir="rtl">

# درس (مسیر ویندوز): کنترل کیفیت و بریدن ریدها، بی لینوکس

**بخش:** `06_Metagenomics` · **ماژول:** `01_Read_QC_Trimming` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [آماده کردن ویندوز](../../windows/README.md) (پایتون، داده‌ی بخش ۰۱ با `get_part01_data.py`)؛ مفهوم‌ها از درس‌های [۱](01_lesson_fastqc.md) و [۲](02_lesson_trimming.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** FastQC (ویندوز)، MultiQC (pip)، Python 3؛ fastp در Galaxy · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** اسکریپت‌های پایتون این درس (`fastq_stats.py`، `fastqc_zip.py`، خلاصه‌ی JSON) روی سرور دوره **اجرا شدند** (2026-11-10)، روی همان گزارش‌های FastQC و fastp درس اصلی؛ خروجی‌شان واقعی است. نصب FastQC و MultiQC در ویندوز و fastp در Galaxy از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`conda env create -f envs/metagenomics.yml` | ‏FastQC (برنامه‌ی ویندوزی) + `py -m pip install multiqc` |
| ‏`zcat … \| head`، `seqkit stats -a` | ‏[`fastq_stats.py`](../../windows/fastq_stats.py) (گام ۱) |
| ‏`fastqc -o …` در ترمینال | ‏**FastQC با پنجره** (گام ۲) |
| ‏`unzip -p … \| grep -v PASS` | ‏[`fastqc_zip.py`](../../windows/fastqc_zip.py) (گام ۳) |
| ‏`multiqc` | همان `multiqc`، با pip (گام ۴) |
| ‏fastp | **نسخه‌ی ویندوزی ندارد** ← ‏**fastp در Galaxy** (گام ۵، ✍️) |
| ‏`fastp_summary.py` روی JSON | همان کد پایتون، روی JSON که از Galaxy می‌گیرید (گام ۶) |
| ‏Snakefile ماژول (بخش ۷ درس ۲) | ‏Snakemake برای ویندوز پشتیبانی کامل ندارد؛ این بخش را تنها بخوانید |

**پیش از خواندن:** از درس ۱ بخش‌های **۱ تا ۳** (داستان، کیفیت Phred، نمودارهای FastQC) و از درس ۲ بخش‌های **۱ تا ۳** (چرا و چگونه بریدن) را بخوانید. این درس آن‌ها را تکرار نمی‌کند.

---

## ۱. گام ۰ و ۱: پوشه، داده و کارت شناسایی

داده همان ریدهای بخش ۰۱ است. اگر آن را در [ماژول 03/04](../../03_Python/04_Biopython_Seq/00_lesson_windows.md) گرفته‌اید، کپی کنید؛ وگرنه `get_part01_data.py` را اجرا کنید:

<div dir="ltr">

```powershell
mkdir $HOME\meta; cd $HOME\meta
$W = "$HOME\course-bioinformatics-main\windows"
Copy-Item -Recurse $HOME\course\fastq raw
py $W\fastq_stats.py raw\minigut_R1.fastq.gz raw\minigut_R2.fastq.gz raw\minigut_sample2_R1.fastq.gz raw\minigut_sample2_R2.fastq.gz
```

</div>

(اگر `$HOME\course\fastq` ندارید: `cd $HOME\meta`، `py $W\get_part01_data.py` و سپس `Rename-Item fastq raw`.)

**خروجی واقعی** (سرور دوره؛ ۱٫۷ ثانیه، ۱۱ مگابایت):

<div dir="ltr">

```text
file	reads	bases	min_len	avg_len	max_len	Q20(%)	Q30(%)	GC(%)
minigut_R1.fastq.gz	50000	6300000	126	126.0	126	96.10	92.29	46.79
minigut_R2.fastq.gz	50000	6300000	126	126.0	126	94.83	90.29	46.76
minigut_sample2_R1.fastq.gz	24993	3773943	151	151.0	151	97.60	96.27	40.51
minigut_sample2_R2.fastq.gz	24993	3773943	151	151.0	151	93.80	90.46	40.48
```

</div>

همان عددهای `seqkit stats -a` (seqkit 2.13.0 روی همین فایل‌ها: Q20 ‏۹۶ / ۹۵ / ۹۸ / ۹۴ و Q30 ‏۹۲ / ۹۰ / ۹۶ / ۹۰، گردشده). `fastq_stats.py` تنها کتابخانه‌ی استاندارد پایتون را به کار می‌برد.

برای دیدن یک رید (جای `zcat … | head -n 4`):

<div dir="ltr">

```powershell
py -c "import gzip; print(''.join(gzip.open('raw/minigut_R1.fastq.gz', 'rt').readlines()[:4]), end='')"
```

</div>

---

## ۲. گام ۲: FastQC با پنجره

‏FastQC برنامه‌ی **جاوا** است و نسخه‌ی ویندوزی دارد. ✍️ از مستندات:

1. ‏https://www.bioinformatics.babraham.ac.uk/projects/fastqc/ ← **FastQC v0.12.x (Win/Linux zip file)**. آن را در `$HOME\tools` باز کنید.
2. ‏FastQC به **Java** نیاز دارد. اگر `java -version` در PowerShell چیزی نگفت، Java را از https://adoptium.net (Temurin، نسخه‌ی LTS) نصب کنید.
3. ‏`run_fastqc.bat` را در پوشه‌ی FastQC دوبار کلیک کنید. پنجره‌ی FastQC باز می‌شود.
4. ‏**File ← Open** ← هر چهار فایل `raw\*.fastq.gz` را برگزینید (Ctrl+کلیک). FastQC برای هر فایل یک زبانه می‌سازد.
5. برای هر زبانه: **File ← Save report** ← در `$HOME\meta\qc\fastqc_raw` ذخیره کنید. هر بار یک `.html` و یک `.zip` ساخته می‌شود، **همان دو فایل** `fastqc -o` در لینوکس.

نمودارهای پنجره همان نمودارهای درس ۱ (بخش‌های ۴ تا ۷) است. نشانه‌های سبز / زرد / قرمز در فهرست سمت چپ همان PASS / WARN / FAIL است.

> 💡 در خط فرمان ویندوز هم می‌شود FastQC را اجرا کرد (`java -Xmx250m -cp "…" uk.ac.babraham.FastQC.FastQCApplication …`)، ولی دردسرش بیش از سودش است. برای ۴ فایل پنجره بس است. برای ۲۰۰ فایل، Galaxy (گام ۵) FastQC را هم دارد.

---

## ۳. گام ۳: خواندن گزارش‌ها بی `unzip` و `grep`

درس ۱ (بخش‌های ۵ و ۶) با `unzip -p … | grep -v PASS` همه‌ی آزمون‌های ناموفق را می‌بیند. در ویندوز:

<div dir="ltr">

```powershell
py $W\fastqc_zip.py summary qc\fastqc_raw
py $W\fastqc_zip.py module qc\fastqc_raw\minigut_R1_fastqc.zip "Per base sequence quality" 5
```

</div>

**خروجی واقعی** (روی گزارش‌های FastQC درس اصلی):

<div dir="ltr">

```text
== minigut_R1_fastqc
== minigut_R2_fastqc
== minigut_sample2_R1_fastqc
FAIL	Per sequence GC content	minigut_sample2_R1.fastq.gz
== minigut_sample2_R2_fastqc
FAIL	Per sequence GC content	minigut_sample2_R2.fastq.gz
>>Per base sequence quality	pass
#Base	Mean	Median	Lower Quartile	Upper Quartile	10th Percentile	90th Percentile
1	32.37272	33.0	33.0	33.0	33.0	33.0
2	32.43406	33.0	33.0	33.0	33.0	33.0
3	32.4528	33.0	33.0	33.0	33.0	33.0
4	32.42046	33.0	33.0	33.0	33.0	33.0
5	32.46712	33.0	33.0	33.0	33.0	33.0
```

</div>

همان خروجی حلقه‌ی `unzip … | grep -v PASS` و `grep -A` درس ۱: تنها یک «شکست» واقعی، GC نمونه‌ی ۲، که درس ۱ (بخش ۷) نشان می‌دهد **خطا نیست** (۲۱ ژنوم با GC گوناگون، یک قله‌ی هنجار نمی‌سازند).

| ورودی | کار |
| :--- | :--- |
| ‏`summary <پوشه>` | برای هر `*_fastqc.zip`، سطرهای غیر PASS از `summary.txt` |
| ‏`module <zip> "<نام>" [N]` | ‏N سطر داده‌ی نخست یک بخش از `fastqc_data.txt`؛ نام بخش همان عنوان نمودار است |

برای بخش ۷ درس ۱ (GC نمونه‌ی ۲): `py $W\fastqc_zip.py module qc\fastqc_raw\minigut_sample2_R1_fastqc.zip "Per sequence GC content"`.

---

## ۴. گام ۴: MultiQC

‏MultiQC برنامه‌ی پایتون است و با pip روی ویندوز نصب می‌شود:

<div dir="ltr">

```powershell
py -m pip install multiqc
py -m multiqc qc\fastqc_raw -o qc\multiqc_raw
Start-Process qc\multiqc_raw\multiqc_report.html
```

</div>

‏✍️ ‏`py -m multiqc` را به کار ببرید (نه تنها `multiqc`)، چون pip پوشه‌ی برنامه‌ها را همیشه به PATH نمی‌افزاید. گزارش همان گزارش درس ۱ (بخش ۸) است. جدول `general_stats` را در Excel باز کنید: `qc\multiqc_raw\multiqc_data\multiqc_general_stats.txt` (Data ← From Text/CSV، جداکننده Tab)؛ جای `cut -f 1-3,6`.

---

## ۵. گام ۵: بریدن با fastp در Galaxy

‏fastp نسخه‌ی ویندوزی ندارد. ✍️ از مستندات Galaxy:

1. ‏https://usegalaxy.org (یا usegalaxy.eu) ← یک حساب رایگان بسازید.
2. ‏**Upload** (بالا چپ) ← چهار فایل `raw\*.fastq.gz` را بفرستید. نوع (Type) را **fastqsanger.gz** بگذارید.
3. ابزار **fastp** را جست‌وجو کنید. تنظیم‌های درس ۲ (بخش ۲) را بدهید:

| در درس (خط فرمان) | در فرم Galaxy |
| :--- | :--- |
| ‏`-i … -I …` | ‏**Single-end or paired reads** ← Paired؛ R1 و R2 |
| ‏`--detect_adapter_for_pe` | ‏Adapter Trimming Options ← **Detect adapter for paired-end** |
| ‏`--cut_front --cut_tail --cut_mean_quality 20` | ‏Read Modification Options ← **Cut by quality in front (5')** و **in tail (3')**؛ mean quality ۲۰ |
| ‏`--length_required 50` | ‏Filter Options ← Length filtering ← **Length required** ۵۰ |
| ‏`-j … -h …` | ‏Output Options ← **Output JSON report** را روشن کنید |

4. ‏**Run**. پس از سبز شدن، ریدهای بریده و **JSON** را با آیکون 💾 دانلود کنید. JSON را با نام `qc\fastp\minigut.json` ذخیره کنید.

**انتظار** (از اجرای واقعی fastp در درس ۲؛ نسخه‌ی fastp در Galaxy شاید کمی فرق کند): از ۱۰۰٬۰۰۰ رید (۵۰٬۰۰۰ جفت)، **۹۹٬۶۹۰** می‌مانند.

---

## ۶. گام ۶: خلاصه‌ی JSON با پایتون

کد `fastp_summary.py` درس ۲ (بخش ۶) را در IDLE بنویسید و در `$HOME\meta` ذخیره کنید؛ در ویندوز هیچ فرقی ندارد. روی JSON درس اصلی (fastp لینوکسی) این خروجی را داد:

<div dir="ltr">

```text
dict_keys(['summary', 'filtering_result', 'duplication', 'insert_size', 'adapter_cutting', 'read1_before_filtering', 'read2_before_filtering', 'read1_after_filtering', 'read2_after_filtering', 'command'])
100000 99690 99.69
{'passed_filter_reads': 99690, 'low_quality_reads': 308, 'too_many_N_reads': 0, 'too_short_reads': 2, 'too_long_reads': 0}
```

</div>

با JSON که از Galaxy گرفته‌اید باید همین عددها، یا بسیار نزدیک به آن‌ها، را ببینید. ✍️ اگر Galaxy نسخه‌ی دیگری از fastp داشت، `dict_keys` شاید یکی دو کلید بیشتر یا کمتر داشته باشد. `summary` و `filtering_result` همیشه هست.

**شمار ریدهای بریده** (جای `zcat … | awk 'END {print NR/4}'`): `py $W\fastq_stats.py minigut_R1_trimmed.fastq.gz` (نام فایلی که از Galaxy گرفته‌اید).

---

## ۷. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| ‏Java نصب نیست | ‏`run_fastqc.bat` پنجره‌ای کوتاه باز و بسته می‌کند | ‏Java (Temurin) را نصب کنید |
| فایل `.gz` را با 7-Zip باز کردن پیش از FastQC | فایل‌های ۴ برابر بزرگ‌تر | لازم نیست؛ FastQC و پایتون `.gz` را خودشان می‌خوانند |
| نوع فایل در Galaxy `fastq.gz` (نه `fastqsanger.gz`) | ابزار fastp فایل را در فهرست نشان نمی‌دهد | ویرایش ویژگی‌ها (✏️) ← Datatype ← fastqsanger.gz |
| ‏`multiqc` در PowerShell | ‏`not recognized` | ‏`py -m multiqc` |
| ذخیره نکردن گزارش FastQC | ‏`fastqc_zip.py` هیچ نمی‌یابد | ‏File ← Save report برای **هر** زبانه |

✍️ پیام‌های این جدول از مستندات‌اند.

---

## ۸. جمع‌بندی

- آمار FASTQ با `fastq_stats.py`؛ همان عددهای seqkit.
- ‏FastQC روی ویندوز با پنجره کار می‌کند؛ گزارش‌ها همان `.html` و `.zip`.
- ‏`fastqc_zip.py` جای `unzip -p | grep`؛ MultiQC با `py -m pip install multiqc`.
- ‏fastp تنها در Galaxy؛ JSON را دانلود کنید و همان کد پایتون درس ۲ را روی آن اجرا کنید.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| آمار ریدها | ‏`py $W\fastq_stats.py (Get-ChildItem raw\*.fastq.gz).FullName` (PowerShell خودش `*` را برای برنامه‌های بیرونی باز نمی‌کند؛ `Get-ChildItem` فهرست را می‌سازد) |
| آزمون‌های ناموفق FastQC | ‏`py $W\fastqc_zip.py summary qc\fastqc_raw` |
| یک بخش از گزارش FastQC | ‏`py $W\fastqc_zip.py module X_fastqc.zip "Per base sequence quality" 5` |
| گزارش یکجا | ‏`py -m multiqc qc\fastqc_raw -o qc\multiqc_raw` |
| بریدن | ‏fastp در Galaxy، با JSON |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏Java | زبان و ماشین اجرایی‌ای که FastQC روی آن کار می‌کند |
| ‏Galaxy | سکوی وب رایگان برای اجرای ابزارهای بیوانفورماتیک بی نصب |
| ‏fastqsanger | نام Galaxy برای FASTQ با کیفیت Phred+33 (همه‌ی FASTQهای امروزی) |

---

## منابع

### مقاله
- ‏Chen S, et al. (2018). *fastp: an ultra-fast all-in-one FASTQ preprocessor.* Bioinformatics 34:i884–i890. https://doi.org/10.1093/bioinformatics/bty560
- ‏Ewels P, et al. (2016). *MultiQC: summarize analysis results for multiple tools and samples in a single report.* Bioinformatics 32:3047–3048. https://doi.org/10.1093/bioinformatics/btw354
- ‏The Galaxy Community (2024). *The Galaxy platform for accessible, reproducible, and collaborative data analyses: 2024 update.* Nucleic Acids Research 52:W83–W94. https://doi.org/10.1093/nar/gkae410

### راهنما و درس رایگان
- ‏FastQC (دانلود و راهنما): https://www.bioinformatics.babraham.ac.uk/projects/fastqc/
- ‏Galaxy Training — *Quality Control*: https://training.galaxyproject.org/training-material/topics/sequence-analysis/tutorials/quality-control/tutorial.html
- همه‌ی منابع درس‌های [۱](01_lesson_fastqc.md) و [۲](02_lesson_trimming.md).

### فیلم‌های آموزشی
همان فیلم‌های درس‌های اصلی؛ آموزش Galaxy بالا فیلم همراه دارد.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌های پایتون در 2026-11-10 روی سرور دوره اجرا شدند. FastQC و MultiQC ویندوز و Galaxy از مستندات‌اند (✍️).

</div>
