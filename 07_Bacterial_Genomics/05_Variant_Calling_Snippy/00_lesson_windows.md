<div dir="rtl">

# درس (مسیر ویندوز): فراخوانی واریانت با Snippy، بی لینوکس

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `05_Variant_Calling_Snippy` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز 07/03](../03_MLST_Molecular_Typing/00_lesson_windows.md)؛ [Galaxy در بخش ۰۶](../../06_Metagenomics/02_Host_Removal_Alignment/00_lesson_windows.md)؛ مفهوم‌ها از [درس اصلی](01_lesson.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** Snippy، snippy-core و Gubbins در Galaxy؛ Python 3 ([`snp_dists.py`](../../windows/snp_dists.py))؛ Excel · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** دانلود GenBank با پایتون و `snp_dists.py` روی سرور دوره **اجرا شدند** (2026-11-10). `snp_dists.py` روی هم‌ردیفی شیوع ماژول 08/04 همان فاصله‌ی `dist.dna` بسته‌ی ape را داد (H1-01 ↔ H2-05 = **۱۵۱۲**). درس اصلی Snippy را «از مستندات» آورده است؛ Snippy در Galaxy هم از **مستندات** نوشته شده و آزموده نشده است.

---

## در یک نگاه

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`curl … rettype=gbwithparts > ecoli_k12.gbk` | یک سطر پایتون (گام ۰) |
| ‏`snippy --ref … --R1 … --R2 …` | ‏**Snippy در Galaxy** (گام ۱) |
| ‏`grep -E 'gyrA\|parC\|rpoB' snps.tab` | ‏`Select-String` یا فیلتر Excel (گام ۲) |
| ‏`snippy-core` | ‏**snippy-core در Galaxy** (گام ۳) |
| ‏`snp-dists core.aln` | ‏`py snp_dists.py core.aln` (گام ۴)، یا snp-dists در Galaxy |
| ‏Gubbins، snp-sites، FastTree | ‏Gubbins در Galaxy؛ درخت با IQ-TREE ویندوزی ([مسیر ویندوز 08/04](../../08_AMR_Virulence_Phylogeny/04_Phylogenetic_Trees/00_lesson_windows.md)) |

**پیش از خواندن:** از درس اصلی بخش‌های **۱ و ۲** (داستان؛ با مرجع نه از صفر؛ کی یک واریانت باور می‌شود؛ برگزیدن مرجع) را بخوانید.

---

## ۱. گام ۰: مرجع GenBank

<div dir="ltr">

```powershell
mkdir $HOME\snippy; cd $HOME\snippy
py -c "import urllib.request; urllib.request.urlretrieve('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts&retmode=text', 'ecoli_k12.gbk')"
Get-Content ecoli_k12.gbk -TotalCount 1
```

</div>

**خروجی واقعی** (سرور دوره؛ ۱۵ ثانیه، ۱۱٫۵ مگابایت):

<div dir="ltr">

```text
LOCUS       NC_000913            4641652 bp    DNA     circular CON 02-SEP-2026
```

</div>

چرا GenBank و نه FASTA؟ Snippy از آنوتیشن GenBank نام ژن و اثر هر SNP را (برای نمونه `gyrA` و `S83L`) می‌گوید (درس اصلی، بخش ۳).

---

## ۲. گام ۱ و ۲: Snippy برای یک ایزوله در Galaxy

✍️ از مستندات Galaxy (ابزار **snippy** در usegalaxy.eu و usegalaxy.org):

1. ‏Upload ← `ecoli_k12.gbk` (نوع **genbank**) و ریدهای ایزوله (R1 و R2، نوع fastqsanger.gz).
2. ابزار **snippy** ← **Will you select a reference genome from your history** ← `ecoli_k12.gbk`؛ **Single or Paired-end reads** ← Paired؛ R1 و R2.
3. ‏**Output**: جدول SNPها (**snps.tab**)، VCF، و «*Output a directory of the files*» (برای snippy-core در گام ۳ لازم است) را روشن کنید.
4. ‏**Run**؛ `snps.tab` را دانلود کنید.

**خواندن `snps.tab`** (جای `grep -E 'gyrA|parC|rpoB' snps.tab`):

<div dir="ltr">

```powershell
Select-String -Path snps.tab -Pattern "gyrA|parC|rpoB"
```

</div>

یا در Excel: Data ← From Text/CSV (جداکننده Tab) ← فیلتر روی ستون `GENE`. ستون‌ها همان جدول بخش ۴ درس اصلی است (`CHROM`، `POS`، `TYPE`، `REF`، `ALT`، `EFFECT`، `GENE`، …). جهش‌های مقاومت را با جدول بخش ۵ درس بسنجید (*gyrA* ‏S83L و D87N؛ *rpoB* ‏H526Y و S531L).

---

## ۳. گام ۳: چند ایزوله و هسته‌ی SNP

✍️ برای هر ایزوله Snippy را اجرا کنید (Galaxy می‌تواند همه را با یک **collection** یکجا اجرا کند)، سپس ابزار **snippy-core** ← همه‌ی خروجی‌های «directory» گام ۱. خروجی‌ها همان‌های درس (بخش ۶): `core.aln` (تنها جایگاه‌های متغیر)، `core.full.aln` (کل هم‌ردیفی) و `core.txt` (آمار هر ایزوله). `core.aln` را دانلود کنید.

---

## ۴. گام ۴: ماتریس فاصله با `snp_dists.py`

<div dir="ltr">

```powershell
$W = "$HOME\course-bioinformatics-main\windows"
py $W\snp_dists.py core.aln | Set-Content distances.tsv
Import-Csv distances.tsv -Delimiter "`t" | Format-Table
```

</div>

‏`snp_dists.py` برای هر جفت ایزوله، جایگاه‌هایی را می‌شمارد که هر دو `A/C/G/T` دارند و فرق می‌کنند (`-` و `N` نادیده؛ همان رفتار پیش‌فرض `snp-dists`). ‏`| Set-Content` به جای `>` تا فایل UTF-16 نشود.

**آزمون روی داده‌ی معلوم** (هم‌ردیفی شیوع شبیه‌سازی‌شده‌ی [ماژول 08/04](../../08_AMR_Virulence_Phylogeny/04_Phylogenetic_Trees/03_lesson_outbreak_tree.md)، `core_full.aln`، ۲۱ ایزوله × ۱۰۰٬۰۰۰ جایگاه؛ ۰٫۱ ثانیه). دو سطر نخست (۱۸ ستون نخست):

<div dir="ltr">

```text
snp_dists.py	H1-01	H1-02	H1-03	H1-04	H1-05	H1-06	H2-01	H2-02	H2-03	H2-04	H2-05	H2-06	H3-01	H3-02	H3-03	H3-04	H3-05	H3-06
H1-01	0	3	3	1001	1383	1353	5	4	6	1164	1512	1475	853	852	857	855	855	1318	…
```

</div>

‏H1-01 ↔ H2-05 = **۱۵۱۲**، همان عددی که `dist.dna(model = "N")` بسته‌ی ape روی همین فایل داد (روی سرور سنجیده شد) و همان عدد درس 08/04. تفسیر فاصله‌ها برای پرسش انتقال (درس اصلی، بخش ۷) وابسته به سیستم‌عامل نیست: **آستانه‌ی SNP به گونه، نرخ جهش و زمان بستگی دارد** و تنها همراه داده‌ی همه‌گیرشناسی معنا دارد.

---

## ۵. بازترکیب و درخت

‏Gubbins نسخه‌ی ویندوزی ندارد ([مسیر ویندوز 08/04](../../08_AMR_Virulence_Phylogeny/04_Phylogenetic_Trees/00_lesson_windows.md) هم همین را گفت). ✍️ در Galaxy ابزار **Gubbins** روی `core.full.aln`؛ سپس هم‌ردیفی بی بازترکیب را با **IQ-TREE ویندوزی** درخت کنید (مسیر ویندوز 08/04، بخش ۷: همان دستور، همان `-fconst` برای هم‌ردیفی تنها-SNP).

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| مرجع FASTA به جای GenBank | ستون‌های `EFFECT` و `GENE` خالی | ‏`rettype=gbwithparts` (گام ۰) |
| ‏`snp_dists.py core.aln > d.tsv` در PowerShell 5.1 | فایل UTF-16؛ Excel نویسه‌های درهم | ‏`\| Set-Content d.tsv` |
| دادن `core.full.aln` به جای `core.aln` | کندتر (ولی همان عددها) | هر دو کار می‌کنند؛ `snp_dists.py` خودش تنها جایگاه‌های متغیر را نگه می‌دارد |
| خروجی «directory» در Snippy روشن نبود | ‏snippy-core ورودی نمی‌یابد | گام ۱، بند ۳ |

✍️ سطرهای یکم و چهارم از مستندات‌اند.

---

## ۷. جمع‌بندی

- ‏Snippy، snippy-core و Gubbins در ویندوز: Galaxy.
- جدول SNP: `Select-String` یا Excel؛ ماتریس فاصله: `snp_dists.py` (همان عدد ape: ۱۵۱۲).
- درخت: IQ-TREE ویندوزی (ماژول 08/04).

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| مرجع GenBank | ‏`py -c "import urllib.request; urllib.request.urlretrieve('…rettype=gbwithparts…', 'ref.gbk')"` |
| ژن‌های مقاومت در snps.tab | ‏`Select-String -Path snps.tab -Pattern "gyrA\|parC\|rpoB"` |
| ماتریس فاصله | ‏`py $W\snp_dists.py core.aln \| Set-Content distances.tsv` |

---

## منابع

### مقاله
- ‏Croucher NJ, et al. (2015). *Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins.* Nucleic Acids Research 43:e15. https://doi.org/10.1093/nar/gku1196

### راهنما و درس رایگان
- ‏Snippy (راهنما): https://github.com/tseemann/snippy
- ‏Galaxy Training — *Microbial Variant Calling*: https://training.galaxyproject.org/training-material/topics/variant-analysis/tutorials/microbial-variants/tutorial.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. دانلود GenBank و `snp_dists.py` در 2026-11-10 روی سرور دوره اجرا شدند. Galaxy از مستندات است (✍️).

</div>
