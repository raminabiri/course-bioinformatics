<div dir="rtl">

# درس (مسیر ویندوز): اسمبلی ژنوم باکتری و سنجش کیفیت آن، بی لینوکس

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `01_Assembly_Quality` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [آماده کردن ویندوز](../../windows/README.md) (پایتون با Biopython)؛ مفهوم‌ها از درس‌های [۱](01_lesson_assembly.md) و [۲](02_lesson_assembly_qc.md) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** Python 3 (Biopython 1.87)؛ Galaxy، WebQUAST (وب) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** گام‌های ۱، ۲، ۳ و ۵ (پایتون) روی سرور دوره **اجرا شدند** (2026-11-10) و خروجی‌شان واقعی است. همین کدها روی ویندوز یکسان کار می‌کنند. گام‌های ۴ و ۶ (Galaxy و WebQUAST در مرورگر) از **مستندات** نوشته شده‌اند. عددهای آن‌ها از آموزش رسمی Galaxy است، نه از اجرای ما. روی ویندوز آزموده نشده است.

---

## در یک نگاه

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| نمونه‌ی کوچک de Bruijn (درس ۱، بخش ۲.۲) | ‏`debruijn_toy.py` (گام ۱) |
| ‏`repeat_report.py` | همان اسکریپت با `py`، و این بار کانتیگ‌های «اسمبلی بی‌نقص» را هم می‌نویسد (گام ۲) |
| ‏`seqkit stats` برای پوشش | یک سطر پایتون (گام ۳) |
| ‏SPAdes و Shovill | نسخه‌ی ویندوزی ندارند ← **Shovill در Galaxy** (گام ۴، ✍️) |
| ‏`seqkit stats -a`، ‏`grep … \| sed` | ‏`asm_stats.py` (گام ۵) |
| ‏QUAST و CheckM2 | ‏**WebQUAST** و CheckM2 در Galaxy (گام ۶، ✍️) |
| ‏Bowtie2 و samtools روی اسمبلی | تنها در Galaxy (گام ۶) |

**در پایان می‌توانید:** ببینید تکرار چگونه گراف را دوشاخه می‌کند؛ سقف اسمبلی Illumina را برای یک ژنوم برآورد کنید؛ پوشش را حساب کنید؛ یک ایزوله را در Galaxy اسمبل کنید؛ N50، NG50 و GC را بسنجید و دام N50 را ببینید.

**پیش از خواندن:** از درس ۱ بخش‌های **۱ (داستان)** و **۲ (گراف de Bruijn)**، و از درس ۲ بخش **۲ (N50 با دست)** را بخوانید. این درس آن‌ها را تکرار نمی‌کند.

---

## ۱. گام ۰: پوشه و ژنوم K-12

پایتون و Biopython را در [آماده کردن ویندوز](../../windows/README.md) نصب کرده‌اید. در PowerShell:

<div dir="ltr">

```powershell
mkdir $HOME\genomes; cd $HOME\genomes
py $HOME\course-bioinformatics-main\windows\get_k12_genome.py
$S = "$HOME\course-bioinformatics-main\07_Bacterial_Genomics\99_scripts_data\01_Assembly_Quality\scripts"
```

</div>

‏`get_k12_genome.py` همان دو فایل بخش ۰۱ (`ecoli_k12.fna` و `ecoli_k12.gff`) را با همان MD5 می‌گیرد ([آماده کردن ویندوز](../../windows/README.md)، «داده‌ی پایه»).

---

## ۲. گام ۱: یک گراف de Bruijn کوچک

مفهوم در درس ۱، بخش ۲.۲. این‌جا همان جدول را خودتان می‌سازید:

<div dir="ltr">

```powershell
py $S\debruijn_toy.py
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
sequence: ATGCGTACGTTAGCGTACGA  (20 bases)
k	kmers	distinct	forks (node -> next nodes)
4	17	13	ACG -> {CGA, CGT}; CGT -> {GTA, GTT}
6	15	13	GTACG -> {TACGA, TACGT}
8	13	13	GCGTACG -> {CGTACGA, CGTACGT}
9	12	12	none (one path)
```

</div>

| ستون | معنی |
| :--- | :--- |
| ‏`kmers` / `distinct` | همه‌ی k-merها / k-merهای جدا |
| ‏`forks` | گره‌هایی ((k−1) بازی) که بیش از یک راه پس از خود دارند؛ اسمبلر همان‌جا کانتیگ را می‌بُرد |

درست همان جدول درس ۱. تکرار ۷ بازی است و تنها با k = 9 (یعنی ۷ + ۲) حل می‌شود.

<details>
<summary>✋ امتحان کن: توالی <code>GGACGTCAAAACGTCTT</code> تکرار ۵ بازی <code>ACGTC</code> را دو بار دارد. کمترین k بی دوشاخه چند است؟</summary>

<div dir="ltr">

```powershell
py $S\debruijn_toy.py GGACGTCAAAACGTCTT --k 4 5 6 7
```

</div>

<div dir="ltr">

```
4	14	12	AAA -> {AAA, AAC}; GTC -> {TCA, TCT}
5	13	12	CGTC -> {GTCA, GTCT}
6	12	12	ACGTC -> {CGTCA, CGTCT}
7	11	11	none (one path)
```

</div>

‏**k = 7** (یعنی ۵ + ۲)، همان قاعده‌ی k ≥ R + 2. در k = 4 دوشاخه‌ی دیگری هم هست: `AAA -> {AAA, AAC}`. چهار A پشت سر هم (`AAAA`) خودش یک تکرار کوتاه است. توالی‌های تک‌بازی (homopolymer) در ژنوم واقعی هم گراف را گره می‌زنند.

</details>

> 📺 **فیلم:** *de Bruijn graph assembly for DNA sequences*: https://www.youtube.com/watch?v=OY9Q_rUCGDw
> 📄 **مرجع:** Compeau PEC, Pevzner PA, Tesler G (2011). *How to apply de Bruijn graphs to genome assembly.* Nat Biotechnol 29:987–991. https://doi.org/10.1038/nbt.2023

---

## ۳. گام ۲: تکرارهای K-12 و سقف اسمبلی Illumina

مفهوم در درس ۱، بخش ۳. همان اسکریپت، با گزینه‌ی تازه‌ی `--out`: کانتیگ‌هایی را که یک اسمبلر **بی‌نقص** می‌ساخت، در یک فایل FASTA می‌نویسد. این فایل در گام ۵ یک «اسمبلی با پاسخ معلوم» است.

<div dir="ltr">

```powershell
py $S\repeat_report.py ecoli_k12.fna ecoli_k12.gff --out ideal_contigs.fna
Get-FileHash -Algorithm MD5 ideal_contigs.fna
```

</div>

**خروجی واقعی** (۷٫۸ ثانیه، ۵۳۳ مگابایت؛ MD5 با `md5sum` روی سرور، که `Get-FileHash` با حروف بزرگ نشان می‌دهد):

<div dir="ltr">

```
== k-mer view
k	positions_in_repeated_kmers_%
21	2.83
55	2.21
77	2.04
127	1.79
== annotation view (cut at rRNA operons + IS elements; genome treated as linear)
repeat blocks: 49  (87394 bp)
contigs: 50  total: 4554258  largest: 360732  N50: 173810  L50: 10
written: ideal_contigs.fna
3b57dbb192436936a1157bcb34bee76b  ideal_contigs.fna
```

</div>

همان عددهای درس ۱. **سقف اسمبلی Illumina برای این ژنوم: ۵۰ کانتیگ و N50 ‏۱۷۴ کیلوباز.** تفسیر کامل در درس ۱، بخش ۳.

‏`ideal_contigs.fna` را در Notepad باز کنید. سرآیند هر کانتیگ جای آن را در ژنوم می‌گوید (`>ideal01 pos=1-…`).

---

## ۴. گام ۳: پوشش، پیش از اسمبلی

فرمول در درس ۱، بخش ۴. برای ۲ میلیون **جفت** رید ۱۵۰ بازی و ژنوم ۵ مگابازی:

<div dir="ltr">

```powershell
py -c "print(2_000_000 * 2 * 150 / 5_000_000, 'x')"
```

</div>

<div dir="ltr">

```
120.0 x
```

</div>

برای فایل‌های FASTQ واقعی، شمار بازها را این سطر پایتون می‌شمارد (به جای `seqkit stats`؛ هر رکورد FASTQ چهار سطر است و سطر دوم توالی است). نام فایل‌ها و اندازه‌ی ژنوم (`5.5e6`) را با داده‌ی خودتان جور کنید:

<div dir="ltr">

```powershell
py -c "import gzip; print(sum(len(l) - 1 for f in ['sample_R1.fastq.gz', 'sample_R2.fastq.gz'] for i, l in enumerate(gzip.open(f, 'rt')) if i % 4 == 1) / 5.5e6, 'x')"
```

</div>

روی سرور، همین سطر روی دو فایل `minigut` بخش ۰۱ همان عدد `seqkit stats` را داد (۲٫۲۹× برای ژنوم ۵٫۵ مگابازی؛ داده‌ی کوچک آموزشی، نه یک ایزوله).

---

## ۵. گام ۴: اسمبلی در Galaxy (✍️)

‏SPAdes و Shovill نسخه‌ی ویندوزی ندارند و به حافظه‌ی ۸ تا ۱۶ گیگابایتی نیاز دارند. **Galaxy** (https://usegalaxy.org یا https://usegalaxy.eu) آن‌ها را رایگان روی سرور خودش اجرا می‌کند؛ شما تنها مرورگر می‌خواهید.

بهترین راه، آموزش رسمی Galaxy (GTN) برای همین کار است: *Genome Assembly of a bacterial genome (MRSA) sequenced using Illumina MiSeq Data*:
https://training.galaxyproject.org/training-material/topics/assembly/tutorials/mrsa-illumina/tutorial.html

گام‌های آن، به گفته‌ی خود آموزش:
1. یک حساب رایگان بسازید و دو فایل ریدهای `DRR187559` را از Zenodo بارگذاری کنید (نشانی‌ها در آموزش).
2. کنترل کیفیت ریدها (Falco، fastp؛ بخش ۰۶، ماژول ۰۱).
3. ابزار **Shovill** با دو فایل بریده‌شده (همان گام‌های درس ۱، بخش ۶).
4. ابزار **QUAST** روی `Contigs`؛ و **Bandage** برای دیدن گراف.

**انتظار** (از خود آموزش GTN، نه اجرای ما): **۳۰ کانتیگ**، طول کل **۲٬۹۱۱٬۳۴۹** باز در برابر اندازه‌ی برآوردشده‌ی ژنوم ۲٬۹۱۴٬۵۶۷، و ‏GC **۳۲٫۷۷٪** (سویه‌ی MRSA HC1335: ‏۳۲٫۸۹٪).

‏`Contigs` را از Galaxy دانلود کنید (آیکون دیسک) و نامش را `mrsa_contigs.fasta` بگذارید؛ در گام ۵ آن را می‌سنجیم.

> 📺 **فیلم:** *GTN Tutorial: Genome Assembly of a bacterial genome (MRSA) sequenced using Illumina MiSeq*: https://www.youtube.com/watch?v=rRHH77qtZHg
> 📄 **مرجع:** Hiltemann S, et al. (2023). *Galaxy Training: A powerful framework for teaching!* PLoS Comput Biol 19:e1010752. https://doi.org/10.1371/journal.pcbi.1010752

---

## ۶. گام ۵: آمار اسمبلی با `asm_stats.py`

مفهوم N50، L50 و NG50 در درس ۲، بخش ۲. ‏`asm_stats.py` کار `seqkit stats -a` و `grep … | sed` درس‌های لینوکسی را انجام می‌دهد. نخست روی اسمبلی با پاسخ معلوم (گام ۲)، با اندازه‌ی ژنوم K-12:

<div dir="ltr">

```powershell
py $S\asm_stats.py ideal_contigs.fna --gsize 4641652 --table ideal.tsv
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
file: ideal_contigs.fna  minlen: 0
contigs: 50  total: 4554258  largest: 360732  N50: 173810  L50: 10  GC%: 50.76
genome size: 4641652  assembly/genome: 0.981  NG50: 173810  LG50: 10
written: ideal.tsv
```

</div>

- همان ۵۰ کانتیگ و N50 ‏۱۷۳٬۸۱۰ گام ۲. روی سرور، `seqkit stats -a` هم همین عددها را داد.
- ‏`assembly/genome` ‏۰٫۹۸۱: اسمبلی ۸۷ کیلوباز کوتاه‌تر از ژنوم است، چون نسخه‌های هر تکرار فشرده شده‌اند (درس ۱).
- ‏GC ‏۵۰٫۷۶٪: همان GC *E. coli* (≈ ۵۰٫۸٪).

‏`ideal.tsv` را در Excel باز کنید (Data ← From Text/CSV، جداکننده Tab): برای هر کانتیگ طول و GC. اگر سرآیند کانتیگ‌ها پوشش داشته باشد (Shovill: `cov=32.7`؛ SPAdes: `_cov_8.9`)، ستون `cov` هم پر می‌شود. با مرتب کردن این ستون در Excel، همان جدول «پوشش هر کانتیگ» درس ۲، بخش ۶ را می‌خوانید.

### ۶.۱ دام N50: برداشتن کانتیگ‌های کوتاه

<div dir="ltr">

```powershell
py $S\asm_stats.py ideal_contigs.fna --minlen 20000 --gsize 4641652
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
file: ideal_contigs.fna  minlen: 20000
contigs: 37  total: 4472082  largest: 360732  N50: 178129  L50: 9  GC%: 50.75
genome size: 4641652  assembly/genome: 0.963  NG50: 173810  LG50: 10
```

</div>

با کنار گذاشتن ۱۳ کانتیگ کوتاه، **N50 بالا رفت** (۱۷۳٬۸۱۰ ← ۱۷۸٬۱۲۹)، بی آنکه اسمبلی بهتر شده باشد: ۸۲ کیلوباز ژنوم را دور ریختیم. ولی **NG50 تغییر نکرد**، چون نیمه‌ی **ژنوم** را می‌گیرد، نه نیمه‌ی اسمبلی را. پس برای سنجیدن دو اسمبلی، NG50 را با همان اندازه‌ی ژنوم گزارش کنید (درس ۲، دام ۲).

### ۶.۲ اسمبلی Galaxy (✍️)

<div dir="ltr">

```powershell
py $S\asm_stats.py mrsa_contigs.fasta --gsize 2914567 --table mrsa.tsv
```

</div>

**انتظار** (از عددهای GTN، گام ۴): ۳۰ کانتیگ، ‏total ۲٬۹۱۱٬۳۴۹، ‏GC نزدیک ۳۲٫۸٪، و `assembly/genome` نزدیک ۰٫۹۹۹. ستون `cov` جدول را مرتب کنید: کانتیگ‌هایی با پوشش چند برابر بقیه پلاسمید یا تکرار فشرده‌اند (درس ۲، بخش ۶).

---

## ۷. گام ۶: ‏QUAST و CheckM2 در وب (✍️)

- ‏**WebQUAST:** ‏http://cab.cc.spbu.ru/quast/ (نشانی پیشین `ccb.uni-saarland.de/quast` به این‌جا می‌رود). ‏`ideal_contigs.fna` را بارگذاری کنید و `ecoli_k12.fna` را به‌عنوان مرجع بدهید. **انتظار:** ‏۵۰ کانتیگ، N50 ‏۱۷۳٬۸۱۰، و **بی misassembly**، چون هر کانتیگ تکه‌ای دست‌نخورده از همان مرجع است. ‏`Genome fraction` نزدیک **۹۸٪** (۴٬۵۵۴٬۲۵۸ از ۴٬۶۴۱٬۶۵۲)؛ کمی بیشتر شاید، چون QUAST یکی از نسخه‌های هر تکرار را روی مرجع می‌نشاند. سنجه‌ها در درس ۲، بخش ۴.
- ‏**CheckM2:** نسخه‌ی ویندوزی ندارد و پایگاهش ۳ گیگابایت است. در Galaxy ابزار **CheckM2** را روی `Contigs` اجرا کنید. برای ایزوله‌ی سالم: کامل بودن نزدیک ۱۰۰٪، آلودگی نزدیک ۰٪ (درس ۲، بخش ۵).
- ‏**نشاندن ریدها روی اسمبلی** (درس ۲، بخش ۶): در Galaxy، ابزارهای **Bowtie2** و **samtools coverage**.

> 📺 **فیلم:** *Module 18: Assembly Metrics w/ QUAST*: https://www.youtube.com/watch?v=eGlNmC6AuN8
> 📄 **مرجع:** Mikheenko A, Saveliev V, Hirsch P, Gurevich A (2023). *WebQUAST: online evaluation of genome assemblies.* Nucleic Acids Res 51:W601–W606. https://doi.org/10.1093/nar/gkad406

---

## ۸. سه اشتباه رایج (مسیر ویندوز)

1. **اسمبلی روی لپ‌تاپ ویندوزی.** SPAdes نسخه‌ی ویندوزی ندارد، و حتی در WSL یک ایزوله ۱۶ گیگابایت حافظه می‌خواهد. کار سنگین را به Galaxy بدهید و تنها خروجی را روی ویندوز بسنجید.
2. **گزارش N50 بی کمترین طول کانتیگ.** گام ۶.۱: با `--minlen 20000`، ‏N50 بالا رفت و ۸۲ کیلوباز ژنوم کنار رفت. همیشه `minlen` را بنویسید، و برای سنجیدن، NG50 را.
3. **سنجیدن دو عدد از دو ابزار با دو آستانه.** QUAST به‌طور پیش‌فرض کانتیگ‌های کوتاه‌تر از ۵۰۰ باز را نمی‌شمارد؛ `asm_stats.py` بی `--minlen` همه را می‌شمارد. برای سنجیدن با QUAST، `--minlen 500` بدهید.

---

## جمع‌بندی

| یافته | ویندوز (این درس) | لینوکس (درس‌های ۱ و ۲) |
| :--- | :--- | :--- |
| ‏de Bruijn کوچک | ‏`debruijn_toy.py`: دوشاخه تا k = 8، یک مسیر در k = 9 | همان جدول |
| تکرارهای K-12 | ‏۲٫۸۳٪ (k = 21) تا ۱٫۷۹٪ (k = 127) | همان (`python3`) |
| سقف اسمبلی | ‏۵۰ کانتیگ، N50 ‏۱۷۳٬۸۱۰؛ اکنون فایل `ideal_contigs.fna` | همان عددها |
| پوشش | یک سطر پایتون | ‏`seqkit stats` |
| اسمبلی | ‏Shovill در Galaxy (✍️؛ GTN: ‏۳۰ کانتیگ) | ‏SPAdes / Shovill (✍️ از مستندات) |
| آمار اسمبلی | ‏`asm_stats.py`؛ با `--minlen 20000`: ‏N50 ↑، NG50 ثابت | ‏`seqkit stats -a` |
| ‏QUAST / CheckM2 | ‏WebQUAST و Galaxy (✍️) | خط فرمان (✍️ از مستندات) |

اکنون اگر خواستید، [درس ۱](01_lesson_assembly.md) و [درس ۲](02_lesson_assembly_qc.md) را بخوانید: همان کار با SPAdes، Shovill، QUAST و CheckM2 در خط فرمان.

---

## منابع

- ‏Compeau PEC, Pevzner PA, Tesler G (2011). Nat Biotechnol 29:987–991. https://doi.org/10.1038/nbt.2023
- ‏Bankevich A, et al. (2012). *SPAdes.* J Comput Biol 19:455–477. https://doi.org/10.1089/cmb.2012.0021
- ‏Gurevich A, et al. (2013). *QUAST.* Bioinformatics 29:1072–1075. https://doi.org/10.1093/bioinformatics/btt086
- ‏Mikheenko A, et al. (2023). *WebQUAST.* Nucleic Acids Res 51:W601–W606. https://doi.org/10.1093/nar/gkad406
- ‏Chklovski A, et al. (2023). *CheckM2.* Nat Methods 20:1203–1212. https://doi.org/10.1038/s41592-023-01940-w
- ‏Hiltemann S, et al. (2023). *Galaxy Training.* PLoS Comput Biol 19:e1010752. https://doi.org/10.1371/journal.pcbi.1010752
- آموزش GTN (اسمبلی MRSA): https://training.galaxyproject.org/training-material/topics/assembly/tutorials/mrsa-illumina/tutorial.html · Galaxy: https://usegalaxy.org · WebQUAST: http://cab.cc.spbu.ru/quast/
- کتاب، Coursera، edX و فیلم‌های بیشتر: بخش منابع [درس ۱](01_lesson_assembly.md) و [درس ۲](02_lesson_assembly_qc.md).

<sub>گام‌های ۱، ۲، ۳ و ۵ با همان کد (Python 3.12، Biopython 1.87؛ `debruijn_toy.py` و `asm_stats.py` تنها کتابخانه‌ی استاندارد) روی سرور لینوکسی دوره در 2026-11-10 اجرا شدند. `asm_stats.py` با `seqkit stats -a` 2.13.0 وارسی شد (همان شمار، طول کل و N50). روی ویندوز آزموده نشده‌اند. Galaxy، WebQUAST و CheckM2 از مستندات‌اند (✍️). ‏WebQUAST از سرور دوره در دسترس نبود (DNS) و در وارسی پایان دوره سنجیده می‌شود.</sub>

</div>
