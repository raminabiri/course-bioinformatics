<div dir="rtl">

# درس (مسیر ویندوز): آنوتیشن ژنوم، بی لینوکس

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `02_Genome_Annotation` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز 07/01](../01_Assembly_Quality/00_lesson_windows.md) (ژنوم K-12 در `$HOME\genomes`)؛ مفهوم‌ها از درس‌های [۱](01_lesson_prokaryote.md)، [۲](02_lesson_phage_virus.md) و [۳](03_lesson_eukaryote.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** Pyrodigal (پایتون، pip)؛ Bakta، tRNAscan-SE و geNomad (وب)؛ barrnap در Galaxy · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** Pyrodigal 3.7.1، `compare_genecalls.py` و یک‌سطری‌های پایتون این درس روی سرور دوره **اجرا شدند** (2026-11-10) و **همان عددهای سه درس اصلی** را دادند. نصب Pyrodigal با pip روی ویندوز و سرورهای وب از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

خبر خوب این ماژول: **Pyrodigal** (پیش‌بینی ژن) یک بسته‌ی **پایتون** است و روی ویندوز با pip نصب می‌شود. پس هسته‌ی سه درس، یعنی پیش‌بینی ژن و سنجیدن با مرجع، در ویندوز **همان** است.

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`conda activate bacterial_genomics` | ‏`py -m pip install pyrodigal` |
| ‏`pyrodigal -i … -g 11 -f gff -o … -a …` | ‏`py -m pyrodigal -i … -g 11 -f gff -o … -a …` |
| ‏`compare_genecalls.py` | **همان** با `py` |
| ‏barrnap، ARAGORN، tRNAscan-SE | ‏barrnap در Galaxy؛ **tRNAscan-SE وب** (✍️) |
| ‏Bakta و Prokka | ‏**Bakta وب** (https://bakta.computational.bio؛ ✍️) |
| ‏geNomad، CheckV، Pharokka | ‏geNomad و Pharokka در Galaxy یا وب (✍️) |
| ‏`curl` برای ژنوم‌های SARS-CoV-2 و مخمر | یک سطر پایتون (گام ۴) |
| ‏`awk`، `grep` روی GFF | یک‌سطری‌های پایتون |
| ‏RepeatModeler، funannotate، BUSCO | تنها بخوانید (درس ۳ هم تنها «از مستندات» است) |

**پیش از خواندن:** از درس ۱ بخش‌های **۱ و ۲** (داستان؛ ORF، کدون آغاز، RBS) را بخوانید.

---

## ۱. گام ۰: نصب Pyrodigal

<div dir="ltr">

```powershell
py -m pip install pyrodigal
py -m pyrodigal --version
cd $HOME\genomes
mkdir annotation
$S = "$HOME\course-bioinformatics-main\07_Bacterial_Genomics\99_scripts_data\02_Genome_Annotation\scripts"
```

</div>

‏✍️ pip برای ویندوز بسته‌ی **آماده** (wheel) دارد، پس کامپایلر لازم نیست. روی سرور: `pyrodigal v3.7.1`. ‏`py -m pyrodigal` را به کار ببرید، نه `pyrodigal` تنها، چون پوشه‌ی برنامه‌های pip شاید در PATH نباشد.

---

## ۲. گام ۱: پیش‌بینی ژن و سنجیدن با RefSeq (درس ۱)

<div dir="ltr">

```powershell
py -m pyrodigal -i ecoli_k12.fna -g 11 -f gff -o annotation\pyrodigal.gff -a annotation\pyrodigal.faa
py -c "print(sum(1 for l in open('annotation/pyrodigal.gff') if not l.startswith('#')))"
py $S\compare_genecalls.py ecoli_k12.gff annotation\pyrodigal.gff
```

</div>

**خروجی واقعی** (سرور دوره؛ Pyrodigal ‏۱٫۳ ثانیه، ۲۱۴ مگابایت):

<div dir="ltr">

```text
4319
reference CDS: 4300 with 4290 distinct stops  (+ 18 pseudogene CDS)   predicted CDS: 4319
same stop:                 4119  (96.0% of reference)
  ... and same start:      3889  (94.4% of matched)
  ... different start:     230
      predicted longer: 89   shorter: 141
reference only (missed):   171
predicted only:            200  (of which on a reference pseudogene: 11)
missed genes by length:    {'<100 aa': 157, '>=100 aa': 14}
shortest missed: baxL (8 aa), yhgP (9 aa), evgL (9 aa), ybgV (10 aa), ykfO (10 aa)
longest missed:  yoeF (118 aa), yfdG (120 aa), mbiA (161 aa), yzcX (161 aa), dnaX (430 aa)
largest start disagreements: stfR (1365 nt), fdnG (636 nt), fdoG (636 nt), insK (486 nt), fdhF (468 nt)
```

</div>

**درست همان خروجی درس ۱** (بخش ۳): ‏۴٬۳۱۹ ژن، ۹۶٪ با همان کدون پایان، و ژن‌های گمشده بیشتر زیر ۱۰۰ اسیدآمینه. تفسیر را همان‌جا بخوانید.

---

## ۳. گام ۲: RNAها و آنوتیشن کامل در وب (درس ۱، بخش‌های ۴ و ۵)

✍️ از مستندات:

| کار | ابزار ویندوزی | چه بدهید |
| :--- | :--- | :--- |
| ‏tRNA | ‏**tRNAscan-SE وب**: https://lowelab.ucsc.edu/tRNAscan-SE/ | ‏`ecoli_k12.fna`؛ Sequence source: **Bacterial**؛ Genetic code: Universal |
| ‏rRNA | ‏**barrnap** در Galaxy | ‏`ecoli_k12.fna`؛ Kingdom: Bacteria |
| آنوتیشن کامل (ژن، RNA، نام و کارکرد) | ‏**Bakta وب**: https://bakta.computational.bio | ‏`contigs.fa` یا `ecoli_k12.fna`؛ نام جنس و گونه |

**انتظار** (درس ۱، خروجی خط فرمان): ‏tRNAscan-SE **۸۹** tRNA (RefSeq ‏۸۶؛ سه تای افزوده تکه‌های tRNA در مرز پروفاژها هستند) و barrnap **۲۲** ژن rRNA (هفت اپرون؛ *rrnD* یک 5S افزوده دارد)، دقیقاً برابر RefSeq. نسخه‌ی وب tRNAscan-SE شاید کمی فرق کند. خروجی Bakta وب همان پوشه‌ی خروجی Bakta خط فرمان است (GFF3، GenBank، FAA، جدول TSV)؛ آن را با Excel و `compare_genecalls.py` بخوانید.

---

## ۴. گام ۳: پروفاژهای خفته‌ی K-12 (درس ۲، بخش ۳)

به جای دو `awk` و یک `grep`:

<div dir="ltr">

```powershell
py -c "import re; [print(c[3], c[4], int(c[4]) - int(c[3]) + 1, re.search(r'Note=([^;]+)', c[8]).group(1)) for c in (l.split('\t') for l in open('ecoli_k12.gff')) if len(c) > 8 and c[2] == 'sequence_feature' and 'cryptic prophage' in c[8]]"
```

</div>

**خروجی واقعی** (چهار سطر نخست از ۱۲):

<div dir="ltr">

```text
262898 297205 34308 cryptic prophage CP4-6
564755 586056 21302 cryptic prophage DLP12
1196209 1211412 15204 cryptic prophage e14
1411899 1434958 23060 cryptic prophage Rac
```

</div>

همان ۱۲ ناحیه‌ی درس ۲. geNomad و CheckV (بخش ۴ درس ۲) ویندوزی ندارند و پایگاه چند گیگابایتی می‌خواهند؛ ✍️ geNomad وب‌سرور دارد (https://portal.nersc.gov/genomad/) و Pharokka در Galaxy هست.

---

## ۵. گام ۴: ابزار باکتریایی روی ویروس و مخمر (درس ۲، بخش ۴.۴؛ درس ۳، بخش ۲)

‏`virus_demo.sh` و `yeast_demo.sh` دو ژنوم را با `curl` می‌گیرند. با پایتون:

<div dir="ltr">

```powershell
mkdir annotation\sarscov2, annotation\yeast
py -c "import urllib.request as u; E = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&rettype=fasta&retmode=text&id='; V = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.cgi?db=nuccore&report=gff3&id='; [(u.urlretrieve(E + a, f'{d}/{n}.fna'), u.urlretrieve(V + a, f'{d}/{n}.gff3')) for a, d, n in [('NC_045512.2', 'annotation/sarscov2', 'sc2'), ('NC_001133.9', 'annotation/yeast', 'chrI')]]"
py -m pyrodigal -i annotation\sarscov2\sc2.fna -p meta -g 1 -f gff -o annotation\sarscov2\pyrodigal.gff
py $S\compare_genecalls.py annotation\sarscov2\sc2.gff3 annotation\sarscov2\pyrodigal.gff
py -m pyrodigal -i annotation\yeast\chrI.fna -g 1 -f gff -o annotation\yeast\pyrodigal.gff
py $S\compare_genecalls.py annotation\yeast\chrI.gff3 annotation\yeast\pyrodigal.gff
```

</div>

**خروجی واقعی** (سطرهای کلیدی):

<div dir="ltr">

```text
reference CDS: 12 with 12 distinct stops  (+ 0 pseudogene CDS)   predicted CDS: 9
same stop:                 9  (75.0% of reference)
reference only (missed):   3
missed genes by length:    {'<100 aa': 3}
reference CDS: 94 with 94 distinct stops  (+ 0 pseudogene CDS)   predicted CDS: 159
same stop:                 84  (89.4% of reference)
predicted only:            75  (of which on a reference pseudogene: 0)
```

</div>

همان درس‌های ۲ و ۳: روی SARS-CoV-2، ‏۹ از ۱۲ CDS (سه ژن کوتاه گم، و ORF1ab با جابه‌جایی چارچوب ریبوزوم دیده نمی‌شود)؛ روی کروموزوم I مخمر، ۷۵ «ژن» اضافی و ژن‌های اینترون‌دار بریده. **ابزار باکتریایی برای ویروس و یوکاریوت ساخته نشده است.** (بخش‌های سه ژن اینترون‌دار در `yeast_demo.sh` با `awk` است؛ همان را در پایتون یا Excel روی `chrI.gff3` ببینید: سطرهای CDS با `gene=EFB1;`، `gene=SNC1;` و `gene=TFC3;`.)

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| ‏`pyrodigal` تنها | ‏`not recognized` | ‏`py -m pyrodigal` |
| فراموش کردن `-g 1` برای مخمر و ویروس | کدون پایان TGA نادرست خوانده می‌شود | جدول ترجمه را با ژنوم جور کنید (درس ۲) |
| ‏`-p meta` برای ژنوم کامل باکتری | آموزش مدل از ژنوم خود انجام نمی‌شود؛ دقت کمتر | تنها برای توالی کوتاه یا متاژنوم |
| بارگذاری ژنوم چند مگابایتی در وب‌سرور در ساعت شلوغ | صف طولانی | صبور باشید، یا Galaxy |

✍️ پیام‌های این جدول از مستندات‌اند.

---

## ۷. جمع‌بندی

- ‏Pyrodigal با pip روی ویندوز؛ `py -m pyrodigal` همان خروجی لینوکس (۴٬۳۱۹ ژن، ۹۶٪ هم‌خوانی).
- ‏tRNA و rRNA و آنوتیشن کامل: tRNAscan-SE وب، barrnap در Galaxy، Bakta وب.
- پروفاژها و دانلودها با یک سطر پایتون؛ درس‌های ویروس و مخمر با همان Pyrodigal.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| نصب | ‏`py -m pip install pyrodigal` |
| پیش‌بینی ژن باکتری | ‏`py -m pyrodigal -i g.fna -g 11 -f gff -o g.gff -a g.faa` |
| توالی کوتاه / متاژنوم | ‏`py -m pyrodigal -i x.fna -p meta -g 1 -f gff -o x.gff` |
| سنجیدن با مرجع | ‏`py $S\compare_genecalls.py ref.gff pred.gff` |
| آنوتیشن کامل | ‏https://bakta.computational.bio |

---

## منابع

### مقاله
- ‏Larralde M (2022). *Pyrodigal: Python bindings and interface to Prodigal, an efficient method for gene prediction in prokaryotes.* Journal of Open Source Software 7:4296. https://doi.org/10.21105/joss.04296
- ‏Schwengers O, et al. (2021). *Bakta: rapid and standardized annotation of bacterial genomes via alignment-free sequence identification.* Microbial Genomics 7:000685. https://doi.org/10.1099/mgen.0.000685
- ‏Chan PP, Lin BY, Mak AJ, Lowe TM (2021). *tRNAscan-SE 2.0: improved detection and functional classification of transfer RNA genes.* Nucleic Acids Research 49:9077–9096. https://doi.org/10.1093/nar/gkab688

### راهنما و درس رایگان
- ‏Pyrodigal (نصب و راهنما): https://pyrodigal.readthedocs.io
- همه‌ی منابع سه درس اصلی.

### فیلم‌های آموزشی
همان فیلم‌های سه درس اصلی.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. Pyrodigal و کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. pip روی ویندوز و وب‌سرورها از مستندات‌اند (✍️).

</div>
