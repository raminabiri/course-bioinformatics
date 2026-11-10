<div dir="rtl">

# درس (مسیر ویندوز): آمپلیکون 16S با QIIME 2، بی لینوکس

**بخش:** `06_Metagenomics` · **ماژول:** `04_16S_Amplicon` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [آماده کردن ویندوز](../../windows/README.md) (پایتون)؛ مفهوم‌ها از درس‌های [۱](01_lesson_qiime_dada2.md) و [۲](02_lesson_taxonomy_diversity.md) · **زمان:** حدود ۹۰ دقیقه (بیشترش انتظار برای Galaxy) · **ابزار:** QIIME 2 در Galaxy؛ QIIME 2 View (وب)؛ Python 3 (`get_16s_data.py`، `qza_peek.py`) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** ‏`get_16s_data.py` روی سرور دوره **اجرا شد** (2026-11-10؛ هر ۶ فایل با MD5 درست، ۲۰۳ ثانیه) و `qza_peek.py` و یک‌سطری‌های پایتون روی **خروجی‌های QIIME 2 درس اصلی** اجرا شدند؛ خروجی‌شان واقعی است. گام‌های Galaxy و QIIME 2 View از **مستندات** نوشته شده‌اند و آزموده نشده‌اند.

---

## در یک نگاه

‏QIIME 2 روی ویندوز تنها از راه WSL یا Docker نصب می‌شود؛ مسیر ما بی WSL است. پس **اجرا** در Galaxy است، و **خواندن نتیجه‌ها** روی ویندوز خودتان: فایل‌های `.qzv` در مرورگر (QIIME 2 View) و فایل‌های `.qza` با پایتون، چون هر دو در اصل **فایل zip** هستند.

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`download.sh` (curl + md5sum) | ‏[`get_16s_data.py`](../../windows/get_16s_data.py) (گام ۰) |
| ‏`qiime tools import`، `demux emp-paired`، `dada2 denoise-paired` | همان ابزارهای **QIIME 2 در Galaxy** (usegalaxy.eu؛ گام‌های ۱ و ۲) |
| ‏`train_classifier.sh` (۵٫۵ گیگابایت حافظه) | در Galaxy (حافظه‌ی سرور Galaxy)، یا طبقه‌بند آماده (گام ۳) |
| ‏`qiime tools export` | ‏[`qza_peek.py`](../../windows/qza_peek.py) (گام ۴) |
| کشیدن `.qzv` روی https://view.qiime2.org | **همان**؛ در ویندوز هم کار می‌کند |

**پیش از خواندن:** از درس ۱ بخش‌های **۱ و ۲** (داستان؛ ASV، DADA2، EMP) و از درس ۲ بخش **۱** را بخوانید.

---

## ۱. گام ۰: داده

<div dir="ltr">

```powershell
mkdir $HOME\amplicon; cd $HOME\amplicon
$W = "$HOME\course-bioinformatics-main\windows"
py $W\get_16s_data.py
```

</div>

**خروجی واقعی** (سرور دوره؛ چند سطر پایانی):

<div dir="ltr">

```text
raw/barcodes.fastq.gz: OK
downloading sample_metadata.tsv ...
sample_metadata.tsv: OK
downloading db/silva-138-99-seqs-515-806.qza ...
db/silva-138-99-seqs-515-806.qza: OK
downloading db/silva-138-99-tax-515-806.qza ...
db/silva-138-99-tax-515-806.qza: OK
Done: data\raw, data\sample_metadata.tsv, data\db
```

</div>

هر ۶ فایل با همان MD5 فایل `download.sh` (ستون `OK`). ‏`sample_metadata.tsv` را در Excel باز کنید (جداکننده Tab)؛ همان جدول درس ۱، بخش ۳.

---

## ۲. گام ۱ و ۲: وارد کردن، جدا کردن نمونه‌ها و DADA2 در Galaxy

✍️ از مستندات Galaxy (ابزارهای QIIME 2 در **usegalaxy.eu** هستند؛ نام هر ابزار با `qiime2` آغاز می‌شود):

1. ‏**Upload** ← `forward.fastq.gz`، `reverse.fastq.gz`، `barcodes.fastq.gz` (نوع **fastqsanger.gz**) و `sample_metadata.tsv` (نوع **tabular**).
2. ‏**qiime2 tools import** ← نوع `EMPPairedEndSequences` ← سه فایل FASTQ را به جای forward / reverse / barcodes بدهید.
3. ‏**qiime2 demux emp-paired** ← metadata: `sample_metadata.tsv`، ستون `barcode-sequence`؛ گزینه‌ی **Golay error correction** و **rev-comp-mapping-barcodes** همانند درس ۱ (بخش ۴).
4. ‏**qiime2 demux summarize** ← یک `.qzv`. آن را دانلود کنید و روی https://view.qiime2.org بکشید: نمودار کیفیت درس ۱ (بخش ۵) را می‌بینید.
5. ‏**qiime2 dada2 denoise-paired** ← همان پارامترهای درس ۱ (بخش ۶): `trim-left` ‏۱۳ و ۱۳، `trunc-len` ‏۱۵۰ و ۱۵۰.

خروجی‌ها: `table.qza`، `rep-seqs.qza`، `denoising-stats.qza`. هر سه را دانلود کنید و در `$HOME\amplicon` ذخیره کنید.

---

## ۳. گام ۳: نام‌گذاری ASVها

درس ۲ (بخش ۲) یک طبقه‌بند Naive Bayes را **خودش** با SILVA آموزش می‌دهد (۵٫۵ گیگابایت حافظه)، چون طبقه‌بند باید با نسخه‌ی scikit-learn همان QIIME 2 بخواند. در Galaxy:

- ‏✍️ ‏**qiime2 feature-classifier fit-classifier-naive-bayes** ← `silva-138-99-seqs-515-806.qza` و `silva-138-99-tax-515-806.qza` (از `data\db`). حافظه را سرور Galaxy می‌دهد.
- سپس **qiime2 feature-classifier classify-sklearn** ← طبقه‌بند و `rep-seqs.qza` ← `taxonomy.qza`.
- ‏**qiime2 taxa barplot** ← `.qzv` برای QIIME 2 View.

---

## ۴. گام ۴: درون `.qza` را با پایتون ببینید

یک `.qza` فایل zip است: `<uuid>/metadata.yaml`، `<uuid>/data/…` (خود داده) و `<uuid>/provenance/…` (تاریخچه‌ی همه‌ی گام‌ها). `qza_peek.py` بی QIIME 2 درونش را نشان می‌دهد:

<div dir="ltr">

```powershell
py $W\qza_peek.py taxonomy.qza
py $W\qza_peek.py taxonomy.qza taxonomy.tsv 3
py $W\qza_peek.py denoising-stats.qza stats.tsv 5
py $W\qza_peek.py rep-seqs.qza dna-sequences.fasta 0 rep-seqs.fasta
```

</div>

**خروجی واقعی** (روی `taxonomy.qza`، `denoising-stats.qza` و `rep-seqs.qza` درس اصلی):

<div dir="ltr">

```text
uuid: d57d0aab-81ab-4a2e-8cee-2b387d588ab9
type: FeatureData[Taxonomy]
format: TSVTaxonomyDirectoryFormat
data-size: 61.8 KiB
      63,265  taxonomy.tsv
Feature ID	Taxon	Confidence
f3b015e043182ca0ab424c5577060a60	d__Bacteria; p__Planctomycetota; c__Planctomycetes; o__Pirellulales; f__Pirellulaceae; g__uncultured	0.9725880350728275
f5cfb950631a0fc8c1d8f4931f15e2bb	d__Bacteria; p__Planctomycetota; c__Planctomycetes; o__Pirellulales; f__Pirellulaceae; g__uncultured	0.9966445040746815
sample-id	input	filtered	percentage of input passed filter	denoised	merged	percentage of input merged	non-chimeric	percentage of input non-chimeric
#q2:types	numeric	numeric	numeric	numeric	numeric	numeric	numeric	numeric
BAQ1370.1.3	6	0	0	0	0	0	0	0
BAQ1370.3	1	0	0	0	0	0	0	0
BAQ1552.1.1	2	2	100	2	0	0	0	0
saved 108,597 bytes to rep-seqs.fasta
```

</div>

‏`rep-seqs.fasta` یک FASTA معمولی است: در BLAST وب یا SILVA ACT بچسبانید، یا با Biopython بخوانید.

**یافته‌های درس، با پایتون:**

<div dir="ltr">

```powershell
py -c "from collections import Counter; from Bio import SeqIO; L = Counter(len(r) for r in SeqIO.parse('rep-seqs.fasta', 'fasta')); print(sum(L.values()), L.most_common(3))"
py -c "import zipfile, collections; z = zipfile.ZipFile('taxonomy.qza'); n = [x for x in z.namelist() if x.endswith('data/taxonomy.tsv')][0]; rows = [r.split('\t') for r in z.read(n).decode().splitlines()[1:]]; c = collections.Counter(t.split('; ')[1] if '; ' in t else t for _, t, _ in rows); print(len(rows), c.most_common(5)); print(sum(1 for _, t, _ in rows if t.startswith('d__Archaea')))"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```text
414 [(227, 372), (228, 26), (226, 9)]
414 [('p__Actinobacteriota', 170), ('p__Proteobacteria', 65), ('p__Chloroflexi', 39), ('p__Acidobacteriota', 28), ('p__Gemmatimonadota', 25)]
13
```

</div>

همان یافته‌های درس اصلی: **۴۱۴ ASV**، ۳۷۲ تا دقیقاً **۲۲۷ باز** (درس ۱، بخش ۶)؛ شاخه‌ها **Actinobacteriota ۱۷۰**، Proteobacteria ۶۵، … و **۱۳ ASV آرکی** (درس ۲، بخش ۳). ✍️ با خروجی‌های Galaxy خودتان، اگر نسخه‌ی QIIME 2 یا DADA2 فرق داشته باشد، عددها شاید کمی فرق کنند.

---

## ۵. گام ۵: تنوع و آزمون گروه‌ها

✍️ در Galaxy، به ترتیب درس ۲ (بخش‌های ۴ تا ۷):

| درس | ابزار Galaxy |
| :--- | :--- |
| ‏`phylogeny align-to-tree-mafft-fasttree` | ‏**qiime2 phylogeny align-to-tree-mafft-fasttree** |
| ‏`diversity core-metrics-phylogenetic` | ‏**qiime2 diversity core-metrics-phylogenetic** (همان ژرفای rarefaction درس) |
| ‏`alpha-group-significance` / `beta-group-significance` | ابزارهای هم‌نام |
| ‏`diversity adonis` | ‏**qiime2 diversity adonis** با فرمول `elevation+vegetation` |

هر `.qzv` را در https://view.qiime2.org باز کنید. **مهم‌ترین درس ماژول (بخش ۷ درس ۲، درهم‌آمیختگی ارتفاع و پوشش گیاهی)** وابسته به سیستم‌عامل نیست: آن را همان‌جا بخوانید.

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| باز کردن `.qza` با دوبار کلیک | ویندوز برنامه‌ای نمی‌شناسد | ‏`qza_peek.py`، یا نام را به `.zip` تغییر دهید و با File Explorer باز کنید |
| نوع داده‌ی Galaxy نادرست برای metadata | ابزار demux ستون‌ها را نمی‌بیند | نوع **tabular** (یا qiime2.tabular) |
| نسخه‌ی طبقه‌بند و QIIME 2 ناجور | خطای scikit-learn در classify-sklearn | طبقه‌بند را **در همان Galaxy** آموزش دهید (گام ۳)؛ همان درس بخش ۲ درس ۲ |
| ‏`.qzv` در Excel یا Notepad | فایل بی‌معنی | ‏https://view.qiime2.org |

✍️ پیام‌های این جدول از مستندات‌اند.

---

## ۷. جمع‌بندی

- ‏QIIME 2 در ویندوز بی WSL: ابزارهای QIIME 2 در **Galaxy**.
- ‏`.qzv` در **QIIME 2 View** (مرورگر)؛ `.qza` یک zip است و `qza_peek.py` داده‌اش را بیرون می‌کشد.
- همان یافته‌ها با پایتون: ۴۱۴ ASV، ۲۲۷ باز، Actinobacteriota چیره، ۱۳ آرکی.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| داده‌ی ماژول | ‏`py $W\get_16s_data.py` |
| درون یک `.qza` | ‏`py $W\qza_peek.py x.qza` |
| چند سطر از یک فایل درون آن | ‏`py $W\qza_peek.py x.qza taxonomy.tsv 5` |
| بیرون کشیدن یک فایل | ‏`py $W\qza_peek.py rep-seqs.qza dna-sequences.fasta 0 out.fasta` |
| دیدن `.qzv` | ‏https://view.qiime2.org |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏artifact (`.qza`) | داده‌ی QIIME 2 همراه نوع و تاریخچه‌اش، در یک zip |
| ‏visualization (`.qzv`) | نمودار و جدول QIIME 2، برای مرورگر، در یک zip |
| ‏provenance | تاریخچه‌ی همه‌ی گام‌هایی که یک artifact را ساخته‌اند |

---

## منابع

### مقاله
- ‏Bolyen E, et al. (2019). *Reproducible, interactive, scalable and extensible microbiome data science using QIIME 2.* Nature Biotechnology 37:852–857. https://doi.org/10.1038/s41587-019-0209-9

### راهنما و درس رایگان
- ‏QIIME 2 View: https://view.qiime2.org
- ‏Galaxy Training — *QIIME 2 Moving Pictures* (ابزارهای QIIME 2 در Galaxy): https://training.galaxyproject.org/training-material/topics/microbiome/tutorials/qiime2-moving-pictures/tutorial.html
- همه‌ی منابع درس‌های [۱](01_lesson_qiime_dada2.md) و [۲](02_lesson_taxonomy_diversity.md).

### فیلم‌های آموزشی
همان فیلم‌های درس‌های اصلی.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. Galaxy و QIIME 2 View از مستندات‌اند (✍️). نشانی آموزش Galaxy برای QIIME 2 وارسی نشده است.

</div>
