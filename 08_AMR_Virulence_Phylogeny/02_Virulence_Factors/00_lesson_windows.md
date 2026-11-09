<div dir="rtl">

# درس (مسیر ویندوز): عامل‌های بیماری‌زایی، بی لینوکس

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `02_Virulence_Factors` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۱](../01_AMR_Resistance_Genes/00_lesson_windows.md) (پوشه‌ی `$HOME\amr` با ژنوم K-12 و `genomes\isoA` تا `isoC`)؛ داستان و مفهوم‌ها از [درس ۱](01_lesson_virulence_amrfinder.md) و [درس ۲](02_lesson_vfdb_heatmap.md) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** Python 3 (کتابخانه‌ی استاندارد)، BLAST+ 2.17.0 (نسخه‌ی ویندوزی)، Excel، VirulenceFinder (وب) · **آخرین بازبینی:** 2026-11-05

> ✍️ **وضعیت:** گام‌های ۱ تا ۴ (پایتون و BLAST+) روی سرور دوره **اجرا شدند** و خروجی‌شان واقعی است (2026-11-05)؛ همین کدها روی ویندوز یکسان کار می‌کنند. گام ۵ (VirulenceFinder در مرورگر) و رنگ‌آمیزی Excel از **مستندات** نوشته شده‌اند و تنها **پاسخ معلوم** را برای سنجیدن می‌دهند. روی ویندوز آزموده نشده است.

---

## در یک نگاه

این درس همان کار درس‌های ۱ و ۲ را **روی ویندوز** انجام می‌دهد. ‏AMRFinderPlus، stxtyper و ABRicate نسخه‌ی ویندوزی ندارند؛ به جایشان:

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏AMRFinderPlus `--plus` و stxtyper (درس ۱) | ‏BLAST+ با ژن‌های معلوم (گام ۲) و **VirulenceFinder** وب (گام ۵) |
| ‏VFDB با `makeblastdb` و `blastn` (درس ۲) | همان دستورها در PowerShell (گام ۳) |
| ‏`awk`، `sort`، `uniq` (درس ۲) | اسکریپت پایتون `vfdb_summary.py` (گام ۴) |
| نقشه‌ی حرارتی با R (درس ۲) | جدول در Excel با رنگ‌آمیزی شرطی (گام ۴) |

**در پایان این درس می‌توانید:**
1. دو ژنوم شبیه‌سازی‌شده‌ی isoD (شبیه STEC) و isoE (شبیه ExPEC) را با پایتون بسازید.
2. ژن‌های بیماری‌زایی و مقاومت را با BLAST+ بیابید و جدول «ژن × ایزوله» بسازید.
3. ‏VFDB را با BLAST+ روی ویندوز بجویید و ژن‌های **ویژه**ی هر ایزوله را از ژن‌های عمومی K-12 جدا کنید.
4. همان ژنوم‌ها را به VirulenceFinder بدهید و نتیجه را با پاسخ معلوم بسنجید.

**پیش از خواندن:** از درس ۱، بخش **۲ (عامل بیماری‌زایی، پاتوتیپ‌ها، داده‌ی این درس)** و بخش **۶ («بودن ژن» در برابر «بیماری‌زا بودن»)**؛ از درس ۲، بخش **۲ (VFDB: ‏setA و setB)**. این درس آن‌ها را تکرار نمی‌کند.

**پاسخ معلوم** (درس ۱، بخش ۲.۳):

| ایزوله | contig | ژن‌ها |
| :--- | :--- | :--- |
| ‏isoD (شبیه STEC) | ‏`isoD_island`، `isoD_phage`، `isoD_pO157` | ‏eae (اینتیمین گاما)؛ اپرون stx2a ‏(stxA2 + stxB2)؛ ehxA |
| ‏isoE (شبیه ExPEC، مقاوم) | ‏`isoE_PAI`، `isoE_pE` | ‏papC، sat، cnf1؛ iutA و blaCTX-M-15 |
| ‏isoC | ـــ | هیچ (K-12، کنترل منفی) |

---

## ۱. گام ۰: پوشه (PowerShell)

✍️ همان پوشه‌ی مسیر ویندوز ماژول ۰۱ را باز کنید. اگر آن را ندارید، نخست [گام ۰ و ۱ آن درس](../01_AMR_Resistance_Genes/00_lesson_windows.md) را اجرا کنید.

<div dir="ltr">

```powershell
cd $HOME\amr
$C = "$HOME\course-bioinformatics-main"
$S = "$C\08_AMR_Virulence_Phylogeny\99_scripts_data"
copy $S\data\virulence_genes.fna .
```

</div>

‏`$S` تنها برای کوتاه کردن دستورهای بعدی است. ‏`virulence_genes.fna` هفت توالی دارد: اپرون stx2a (از رکورد X07865.1، فاژ 933W) و شش ژن از پایگاه AMRFinderPlus.

---

## ۲. گام ۱: ساختن isoD و isoE با پایتون

همان اسکریپت درس ۱ (گام ۱) است و تنها کتابخانه‌ی استاندارد پایتون را می‌خواهد:

<div dir="ltr">

```powershell
py $S\02_Virulence_Factors\scripts\make_virulence_isolates.py ecoli_k12.fna virulence_genes.fna acquired_genes.fna genomes
dir genomes
```

</div>

**خروجی واقعی** (همان اسکریپت روی سرور دوره، 2026-11-05):

<div dir="ltr">

```
Done: genomes
```

</div>

پوشه‌ی `genomes` حالا پنج ژنوم (`isoA.fna` تا `isoE.fna`) و دو جدول پاسخ معلوم دارد. ‏`ground_truth_vir.tsv` را در Excel باز کنید (Data ← From Text/CSV): همان جدول پاسخ معلوم بالا است.

---

## ۳. گام ۲: ژن‌های معلوم با BLAST+

**چرا؟** در درس ۱، ‏AMRFinderPlus ژن‌های بیماری‌زایی را با `--plus` یافت. این‌جا همان کار ماژول ۰۱ (گام ۲ مسیر ویندوز) را می‌کنیم: ژن‌های مرجع را در هر ژنوم می‌جوییم. این بار دو فایل ژن را یکی می‌کنیم و هر پنج ایزوله را می‌آزماییم:

<div dir="ltr">

```powershell
Get-Content acquired_genes.fna, virulence_genes.fna | Set-Content known_genes.fna
foreach ($i in "isoA", "isoB", "isoC", "isoD", "isoE") { blastn -query known_genes.fna -subject genomes\$i.fna -outfmt "6 qseqid sseqid pident qcovs" -evalue 1e-20 -out hits_$i.tsv }
Get-Content hits_*.tsv | Set-Content known_hits.tsv
Get-Content known_hits.tsv
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`Get-Content a, b \| Set-Content c` | دو فایل را پشت هم در یک فایل بنویس (همان `cat a b > c` لینوکس) |
| ‏`-out hits_$i.tsv` | خروجی هر ایزوله در فایل خودش |
| ‏`Get-Content hits_*.tsv` | همه‌ی فایل‌هایی که نامشان با `hits_` آغاز می‌شود |

> چرا `-out` و نه `>`؟ در Windows PowerShell 5.1 (پیش‌فرض ویندوز ۱۰)، `>` فایل را با کدگذاری UTF-16 می‌نویسد و برخی برنامه‌ها آن را بد می‌خوانند. ‏`-out` خود BLAST و `Set-Content` این گرفتاری را ندارند.

**خروجی واقعی** (BLAST+ 2.17.0 روی سرور دوره، 2026-11-05):

<div dir="ltr">

```
blaCTX-M-15	isoA_pA	100.000	100
tet(A)	isoB_pB	100.000	50
blaNDM-1	isoB_pB	100.000	100
stx2a_operon	isoD_phage	100.000	100
ehxA	isoD_pO157	100.000	100
eae_gamma	isoD_island	100.000	100
blaCTX-M-15	isoE_pE	100.000	100
cnf1	isoE_PAI	100.000	100
iutA	isoE_pE	100.000	100
sat	isoE_PAI	100.000	100
papC	isoE_PAI	100.000	100
```

</div>

**توضیح خروجی:**
- هر ۸ ژن افزوده‌ی isoD و isoE با یکسانی و پوشش ۱۰۰٪ یافته شدند، هر کدام روی همان contig پاسخ معلوم. ✅ ‏isoC هیچ سطری ندارد. ✅
- ‏isoA و isoB همان نتیجه‌ی ماژول ۰۱ را دارند (tet(A) با پوشش ۵۰٪).
- ‏**papC** این‌جا ۱۰۰٪ است. در گام ۳ (VFDB) همین ژن گم می‌شود. فرقش این است که این‌جا توالی مرجع **همان** آللی است که در ژنوم گذاشتیم.
- **آنچه BLAST نمی‌گوید:** زیرنوع stx (stx2a یا stx2c…) و نوع اینتیمین (گاما). ‏stxtyper و AMRFinderPlus در درس ۱ آن‌ها را از تفاوت‌های اسید آمینه‌ای می‌خوانند. در ویندوز، VirulenceFinder (گام ۵) زیرنوع stx را گزارش می‌کند.

**جدول ژن × ایزوله در Excel (✍️):** `known_hits.tsv` را باز کنید. فایل سرخط ندارد: با کلیک راست روی سطر ۱ ← Insert یک سطر بیفزایید و بنویسید `gene`، `contig`، `pident`، `qcovs` و `isolate`. در خانه‌ی E2 با فرمول `=LEFT(B2, 4)` نام ایزوله را از نام contig بگیرید (`isoD_phage` ← `isoD`) و آن را تا پایین بکشید. سپس Insert ← PivotTable: ‏Rows = ستون A (ژن)، Columns = ستون E (ایزوله)، Values = Count. این همان جدول `amr_vir_matrix.tsv` درس ۲ است، بی جهش‌های gyrA و parC (آن‌ها را `check_qrdr.py` ماژول ۰۱ داد).

---

## ۴. گام ۳: ‏VFDB با BLAST+

**چرا؟** درس ۲، بخش ۲ را ببینید. ‏VFDB هر ژنی را که در **یک** سویه‌ی بیماری‌زا نقش داشته می‌آورد، حتی ژن‌های عمومی همه‌ی *E. coli*ها. پس K-12 هم ژن‌های VFDB «دارد».

نخست فایل VFDB setA را بگیرید (همان نسخه‌ای که ABRicate نگه می‌دارد؛ ۶٫۶ مگابایت):

<div dir="ltr">

```powershell
mkdir vfdb
py -c "import urllib.request as u; u.urlretrieve('https://cdn.jsdelivr.net/gh/tseemann/abricate@master/db/vfdb/sequences', 'vfdb/vfdb_setA.fna')"
makeblastdb -in vfdb\vfdb_setA.fna -dbtype nucl -out vfdb\vfdb_setA
```

</div>

> درس ۲ همین فایل را از `raw.githubusercontent.com` می‌گیرد. در 2026-11-05 آن نشانی از سرور دوره بسیار کند بود (۳۹ کیلوبایت در دو دقیقه)، و نشانی بالا (jsDelivr، آینه‌ی همان مخزن GitHub) همان فایل را در ۹ ثانیه داد: ‏۶٬۵۷۲٬۱۴۹ بایت، ۴۵۹۲ توالی، درست همانند درس ۲. اگر یکی کار نکرد، دیگری را بیازمایید، یا نشانی را در مرورگر باز کنید و با **Save as** در `vfdb\vfdb_setA.fna` ذخیره کنید.

**خروجی واقعی** (`makeblastdb`):

<div dir="ltr">

```
Building a new DB, current time: 11/05/2026 09:51:32
New DB title:  vfdb/vfdb_setA.fna
Sequence type: Nucleotide
Adding sequences from FASTA; added 4592 sequences in 0.07008 seconds.
```

</div>

اکنون `blastn` روی سه ژنوم، **در یک سطر** (همان گزینه‌های درس ۲، بخش ۴):

<div dir="ltr">

```powershell
foreach ($i in "isoC", "isoD", "isoE") { blastn -query genomes\$i.fna -db vfdb\vfdb_setA -perc_identity 80 -max_target_seqs 10000 -num_threads 2 -outfmt "6 qseqid qstart qend pident length slen stitle" -out "$i.vfdb.tsv" }
dir *.vfdb.tsv
```

</div>

هر اجرا کمتر از یک ثانیه و نزدیک به ۱۹۰ مگابایت حافظه گرفت. سه فایل ۸۷، ۹۲ و ۱۰۲ سطری‌اند (درست همانند درس ۲). معنای ستون‌ها و دام `-max_target_seqs` را در درس ۲، بخش ۴ ببینید.

> 📺 **فیلم:** *Antimicrobial Resistance Genes Detection using ABRicate tutorial* (همین منطق BLAST روی پایگاه ژن): https://www.youtube.com/watch?v=cmhuWRorCTg
> 📄 **مرجع:** Liu B, et al. (2022). *VFDB 2022: a general classification scheme for bacterial virulence factors.* Nucleic Acids Res 50:D912–D917. https://doi.org/10.1093/nar/gkab1107

---

## ۵. گام ۴: فیلتر ۸۰٪ و ژن‌های ویژه با پایتون

در درس ۲ این کار را چند دستور `awk`، `sort` و `uniq` کرد که در ویندوز نیستند. اسکریپت **`vfdb_summary.py`** همان کار را می‌کند: هم‌ترازی‌های با پوشش (`length / slen`) دست‌کم ۰٫۸ را نگه می‌دارد، نام ژن را (تکه‌ی دوم سرآیند، با جداکننده‌ی `~~~`) برمی‌دارد و ژن‌های هر ایزوله را با فایل **نخست** (مرجع؛ این‌جا isoC) می‌سنجد:

<div dir="ltr">

```powershell
py $S\02_Virulence_Factors\scripts\vfdb_summary.py isoC.vfdb.tsv isoD.vfdb.tsv isoE.vfdb.tsv
```

</div>

**هسته‌ی اسکریپت:**

<div dir="ltr">

```python
f = line.rstrip("\n").split("\t")
if int(f[4]) / int(f[5]) < mincov:        # coverage = alignment length / gene length
    continue
found.add(f[6].split("~~~")[1])           # gene name
...
extra = sorted(found - genes[ref])        # genes of this isolate that K-12 does not have
```

</div>

‏`found - genes[ref]` **تفاضل دو مجموعه** در پایتون است: ژن‌هایی که در این ایزوله هست و در مرجع نیست. همان کاری که در درس ۲ با `cat isoC isoC isoD | sort | uniq -u` کردیم، ولی خواناتر.

**خروجی واقعی** (روی سرور دوره، 2026-11-05؛ ۰٫۰۱ ثانیه):

<div dir="ltr">

```
== genes with coverage >= 0.8 (written to <isolate>.vf.txt)
isoC	65
isoD	69
isoE	68

== categories of isoC hits (rows, not unique genes)
   23  Adherence (VFC0001)
   18  Nutritional/Metabolic factor (VFC0272)
   17  Effector delivery system (VFC0086)
    7  Motility (VFC0204)
    4  Invasion (VFC0083)
    3  Regulation (VFC0301)
    2  Immune modulation (VFC0258)
    1  Antimicrobial activity/Competitive advantage (VFC0325)

== genes not in isoC
isoD	eae, hlyA, stx2A, stx2B
isoE	cnf1, iutA, sat

written: vf_specific_matrix.tsv
```

</div>

**توضیح خروجی:** درست همان عددهای درس ۲ (۶۵، ۶۹، ۶۸ و همان هفت ژن ویژه):
- ‏**K-12 ‏۶۵ ژن VFDB دارد**: چسبیدن، آهن‌گیری، فلاژل… ژن‌های عمومی *E. coli*. پاسخ داستان درس ۲: VFDB می‌گوید «این ژن در جایی به بیماری‌زایی کمک کرده»، نه «این سویه بیماری‌زاست».
- **نام‌ها فرق دارند:** ‏`ehxA` گام ۲ این‌جا `hlyA` است و `stxA2` این‌جا `stx2A` (تمرین ۵).
- ‏**papC در isoE گم شد**، با آن‌که در گام ۲ پوشش ۱۰۰٪ داشت. ‏BLAST هم‌ترازی را سه تکه کرده و هیچ تکه‌ای به‌تنهایی از ۸۰٪ نمی‌گذرد (درس ۲، بخش ۴؛ تمرین ۴). با `--mincov 0.6` پیدا می‌شود:

<div dir="ltr">

```powershell
py $S\02_Virulence_Factors\scripts\vfdb_summary.py --mincov 0.6 isoC.vfdb.tsv isoD.vfdb.tsv isoE.vfdb.tsv
```

</div>

<div dir="ltr">

```
isoE	cnf1, iutA, papC, sat
```

</div>

(این دستور فایل‌های `.vf.txt` را با آستانه‌ی ۰٫۶ بازنویسی می‌کند؛ برای ادامه، دستور بی `--mincov` را دوباره بزنید.)

**نقشه‌ی حرارتی در Excel (✍️):** `vf_specific_matrix.tsv` را باز کنید. خانه‌های ۰ و ۱ را برگزینید، سپس Home ← **Conditional Formatting** ← Color Scales (برای نمونه سفید تا قرمز). ستون isoC سراسر سفید است، و isoD و isoE هر کدام ژن‌های خودشان را دارند. همان پیام نقشه‌ی R درس ۲.

<div dir="ltr">

```
gene	isoC	isoD	isoE
eae	0	1	0
hlyA	0	1	0
stx2A	0	1	0
stx2B	0	1	0
cnf1	0	0	1
iutA	0	0	1
sat	0	0	1
```

</div>

---

## ۶. گام ۵: ‏VirulenceFinder در مرورگر (✍️)

**چرا؟** گام ۲ تنها ژن‌هایی را جست که از پیش داشتیم، و گام ۳ ژن‌های عمومی K-12 را هم آورد. ‏**VirulenceFinder** (مرکز اپیدمیولوژی ژنومی، دانمارک؛ همان سازنده‌ی ResFinder ماژول ۰۱) پایگاه ویژه‌ی *E. coli* و چند گونه‌ی دیگر را دارد و **زیرنوع stx** را هم می‌گوید. همتای وب AMRFinderPlus با `--plus` و stxtyper در درس ۱.

✍️ **گام‌ها (از راهنمای CGE):**
1. ‏https://genepi.dk/virulencefinder را باز کنید (نشانی پیشین cge.food.dtu.dk/services/VirulenceFinder به این‌جا می‌رود).
2. گونه یا پایگاه را ***Escherichia coli*** بگذارید و نوع داده را ژنوم اسمبل‌شده (contigها).
3. آستانه‌های یکسانی و طول را ببینید و یادداشت کنید (همانند ResFinder در ماژول ۰۱).
4. فایل `genomes\isoD.fna` را بارگذاری و **Submit** کنید. جدول نتیجه: نام ژن، کارکرد، درصد یکسانی، طول هم‌ترازی / طول ژن، contig و جای آن.
5. همین را برای isoE و isoC تکرار کنید.

**با پاسخ معلوم بسنجید** (این‌ها **انتظار** است، نه خروجی دیده‌شده):

| ایزوله | باید ببینید | نکته‌ی سنجیدنی |
| :--- | :--- | :--- |
| ‏isoD | ‏eae، ehxA، و stx2 با **زیرنوع a** (زیرواحدهای A و B) | ‏stx2a + eae = نشانگر STEC/EHEC، هشدار HUS (درس ۱، بخش ۴) |
| ‏isoE | ‏papC، sat، cnf1، iutA | ‏blaCTX-M-15 این‌جا **نیست**؛ ابزار مقاومت ResFinder است (ماژول ۰۱) |
| ‏isoC | شاید چند ژن عمومی K-12 (بسته به نسخه‌ی پایگاه؛ نسخه‌های تازه ژن‌های ExPEC بیشتری دارند) | شمارش بسیار کمتر از ۶۵ ژن VFDB: پایگاه گونه‌ویژه است |

نام ژن‌ها را با جدول گام ۲ و گام ۴ بسنجید: هر ابزار نام خودش را دارد (تمرین ۵).

> 📺 **فیلم:** *Bacterial virulence factors: an introduction*: https://www.youtube.com/watch?v=XBTkgu8peEY
> 📄 **مرجع:** Joensen KG, et al. (2014). *Real-time whole-genome sequencing for routine typing, surveillance, and outbreak detection of verotoxigenic Escherichia coli.* J Clin Microbiol 52:1501–1510. https://doi.org/10.1128/JCM.03617-13 · Malberg Tetzschner AM, et al. (2020). *In silico genotyping of Escherichia coli isolates for extraintestinal virulence genes by use of whole-genome sequencing data.* J Clin Microbiol 58:e01269-20. https://doi.org/10.1128/JCM.01269-20

---

## ۷. سه اشتباه رایج (مسیر ویندوز)

1. **‏`>` در PowerShell.** در Windows PowerShell 5.1 فایل UTF-16 می‌سازد. برای خروجی BLAST از `-out` و برای پیوستن فایل‌ها از `Set-Content` بهره ببرید.
2. **آستانه‌ی پایین برای همه.** ‏`--mincov 0.6` ‏papC را برمی‌گرداند، ولی در ژنوم واقعی ژن‌های ناقص و خویشاوندهای دور را هم «بودن» می‌شمارد. پیش از گفتن «ندارد»، خروجی خام (`isoE.vfdb.tsv` در Excel، فیلتر روی papC) را ببینید.
3. **شمار VFDB را «خطر» خواندن.** ‏۶۵ ژن در K-12. همیشه ایزوله را با یک کنترل بی‌خطر (isoC) بسنجید و ژن‌های **ویژه** را گزارش کنید.

---

## جمع‌بندی

| یافته | ‏BLAST+ و پایتون (ویندوز، اجرا شده) | ‏AMRFinderPlus و VFDB (درس‌های ۱ و ۲، لینوکس) | ‏VirulenceFinder (وب، ✍️) |
| :--- | :--- | :--- | :--- |
| ‏isoD ‏eae، stx2، ehxA | ✅ ‏۱۰۰٪ | ✅ ‏EXACTX؛ stxtyper ‏STX2A | انتظار: ✅ با زیرنوع stx2a |
| ‏isoE ‏papC، sat، cnf1، iutA | ✅ ‏۱۰۰٪ | ✅ ‏EXACTX (`--plus`) | انتظار: ✅ |
| ‏VFDB، K-12 | ‏۶۵ ژن | ‏۶۵ ژن | ـــ |
| ‏VFDB، ژن‌های ویژه | ‏۷ (papC گم) | ‏۷ (papC گم) | ـــ |

اکنون اگر خواستید، [درس ۱](01_lesson_virulence_amrfinder.md) و [درس ۲](02_lesson_vfdb_heatmap.md) را بخوانید: همان نتیجه با AMRFinderPlus، ABRicate و R.

---

## منابع

- ‏Joensen KG, et al. (2014). J Clin Microbiol 52:1501–1510. https://doi.org/10.1128/JCM.03617-13
- ‏Malberg Tetzschner AM, et al. (2020). J Clin Microbiol 58:e01269-20. https://doi.org/10.1128/JCM.01269-20
- ‏Liu B, et al. (2022). *VFDB 2022.* Nucleic Acids Res 50:D912–D917. https://doi.org/10.1093/nar/gkab1107
- ‏Camacho C, et al. (2009). *BLAST+: architecture and applications.* BMC Bioinformatics 10:421. https://doi.org/10.1186/1471-2105-10-421
- ‏VirulenceFinder (کد و پایگاه): https://github.com/genomicepidemiology/virulencefinder
- کتاب، Coursera، edX و فیلم‌های بیشتر: بخش منابع [درس ۱](01_lesson_virulence_amrfinder.md) و [درس ۲](02_lesson_vfdb_heatmap.md).

<sub>گام‌های ۱ تا ۴ با همان کد (Python 3، BLAST+ 2.17.0) روی سرور لینوکسی دوره در 2026-11-05 اجرا شدند و همان عددهای درس‌های لینوکسی را دادند؛ روی ویندوز آزموده نشده‌اند. گام ۵، رنگ‌آمیزی و PivotTable در Excel، و رفتار `>` در PowerShell از مستندات نوشته شده‌اند (✍️). DOIها با Crossref وارسی شدند.</sub>

</div>
