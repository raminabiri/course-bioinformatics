<div dir="rtl">

# درس (مسیر ویندوز): پلاسمید، IS و CRISPR، بی لینوکس

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `03_Mobile_Elements_CRISPR` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۱](../01_AMR_Resistance_Genes/00_lesson_windows.md) (پوشه‌ی `$HOME\amr` با `ecoli_k12.gff`، `acquired_genes.fna` و `genomes\isoA` تا `isoC`)؛ داستان و مفهوم‌ها از [درس ۱](01_lesson_plasmids_is.md) و [درس ۲](02_lesson_crispr.md) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** Python 3 + Biopython 1.87، BLAST+ 2.17.0 (نسخه‌ی ویندوزی)، Excel، ResFinder و PlasmidFinder و CRISPRCasFinder (وب) · **آخرین بازبینی:** 2026-11-09

> ✍️ **وضعیت:** گام‌های ۱ تا ۴، ۵ و ۶ (پایتون و BLAST+) روی سرور دوره **اجرا شدند** و خروجی‌شان واقعی است (2026-11-09)؛ همین کدها روی ویندوز یکسان کار می‌کنند. ابزارهای وب (ResFinder، PlasmidFinder، CRISPRCasFinder)، فیلتر Excel و `Select-String` از **مستندات** نوشته شده‌اند و تنها **پاسخ معلوم** را برای سنجیدن می‌دهند. روی ویندوز آزموده نشده است.

---

## در یک نگاه

این درس همان کار درس‌های ۱ و ۲ را **روی ویندوز** انجام می‌دهد. ‏AMRFinderPlus و MOB-suite نسخه‌ی ویندوزی ندارند؛ به جایشان:

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`curl` برای گرفتن pEK499 (درس ۱، گام ۱) | یک سطر پایتون (گام ۱) |
| ساختن isoF با `sed` | لازم نیست: BLAST را مستقیم روی `pEK499.fna` می‌زنیم |
| ‏AMRFinderPlus روی isoF (درس ۱، گام ۲) | ‏BLAST+ با ژن‌های معلوم، و **ResFinder** وب (گام ۲) |
| ‏PlasmidFinder با BLAST و `awk`/`sort` (درس ۱، گام ۳) | همان BLAST، فیلتر در Excel، و **PlasmidFinder** وب (گام ۳) |
| ‏`awk` روی GenBank و `gene_context.py` (درس ۱، گام ۴) | اسکریپت پایتون **`gb_context.py`** (گام ۴) |
| ‏`awk` روی GFF برای ژن‌های cas (درس ۲، گام ۱) | یک سطر پایتون (گام ۵) |
| ‏`find_crispr.py` (درس ۲، گام ۲) | همان اسکریپت، بی تغییر (گام ۶) |
| ‏MOB-suite، MinCED | نسخه‌ی ویندوزی ندارند؛ به جای MinCED، ‏CRISPRCasFinder وب (گام ۷) |

**در پایان این درس می‌توانید:**
1. یک رکورد GenBank را با پایتون از NCBI بگیرید.
2. ژن‌های مقاومت و رپلیکون‌های یک پلاسمید واقعی را با BLAST+ و ابزارهای وب CGE بیابید.
3. با `gb_context.py` ببینید کدام IS کنار کدام ژن مقاومت است.
4. ژن‌های cas و آرایه‌ی CRISPR را در K-12 پیدا کنید.

**پیش از خواندن:** از درس ۱، بخش **۲ (عنصرهای ژنتیکی متحرک)**؛ از درس ۲، بخش **۲ (CRISPR به زبان ساده)**. این درس آن‌ها را تکرار نمی‌کند.

**پاسخ معلوم** (از درس‌های لینوکسی و مقاله‌ی Woodford و همکاران، 2009):

| پرسش | پاسخ |
| :--- | :--- |
| ‏pEK499 | ‏EU935739.1، ‏۱۱۷٬۵۳۶ باز، از *E. coli* ‏ST131 |
| رپلیکون‌ها | ‏IncFII و IncFIA |
| ژن‌های مقاومت | ‏۱۲ ژن، همه میان باز ۳۹٬۸۶۴ و ۷۵٬۷۳۲ (درس ۱، گام ۲) |
| ‏IS | ‏۱۱ عنصر، هفت تا IS26 |
| ‏CRISPR در K-12 | نوع I-E؛ ۸ ژن cas؛ دو آرایه با ۱۲ و ۶ spacer |

---

## ۱. گام ۰: پوشه (PowerShell)

✍️ همان پوشه‌ی مسیر ویندوز ماژول ۰۱ را باز کنید. اگر آن را ندارید، نخست [گام ۰ و ۱ آن درس](../01_AMR_Resistance_Genes/00_lesson_windows.md) را اجرا کنید.

<div dir="ltr">

```powershell
cd $HOME\amr
$C = "$HOME\course-bioinformatics-main"
$S = "$C\08_AMR_Virulence_Phylogeny\99_scripts_data"
```

</div>

---

## ۲. گام ۱: گرفتن pEK499 با پایتون

**چرا؟** درس ۱، گام ۱ را ببینید: به یک پلاسمید **واقعی** با رپلیکون و IS نیاز داریم. درس لینوکسی آن را با `curl` از E-utilities می‌گیرد. در ویندوز همان نشانی را به پایتون می‌دهیم: یک بار FASTA و یک بار GenBank.

<div dir="ltr">

```powershell
py -c "import urllib.request as u; E = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=EU935739.1&retmode=text&rettype='; u.urlretrieve(E + 'fasta', 'pEK499.fna'); u.urlretrieve(E + 'gb', 'pEK499.gb')"
Get-Content pEK499.fna -TotalCount 1
Get-Content pEK499.gb -TotalCount 1
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`E = '…rettype='` | نشانی efetch بی قالب پایانی |
| ‏`E + 'fasta'` / `E + 'gb'` | همان نشانی، یک بار با قالب FASTA و یک بار GenBank |
| ‏`Get-Content … -TotalCount 1` | سطر نخست فایل (همان `head -1` لینوکس) |

**خروجی واقعی** (همان کد روی سرور دوره، 2026-11-09):

<div dir="ltr">

```
>EU935739.1 Escherichia coli strain A plasmid pEK499, complete sequence
LOCUS       EU935739              117536 bp    DNA     circular BCT 06-APR-2020
```

</div>

‏`117536 bp` و `circular`: پلاسمید کامل و حلقوی. ✅

> اگر پیام `URLError` یا `Network is unreachable` دیدید، دستور را دوباره بزنید. در آزمون ما یک بار FASTA آمد و GenBank نیامد، و بار دوم آمد. فایل‌ها همان MD5 فایل‌های `curl` درس ۱ را داشتند. اگر باز هم نشد، https://www.ncbi.nlm.nih.gov/nuccore/EU935739.1 را باز کنید و از **Send to ← File** (قالب FASTA و GenBank) ذخیره کنید.

---

## ۳. گام ۲: ژن‌های مقاومت پلاسمید

### ۳.۱ ژن‌های معلوم با BLAST+ (اجرا شده)

**چرا؟** ‏`blaCTX-M-15` را در ماژول‌های ۰۱ و ۰۲ در isoA و isoE گذاشتیم. آیا همان ژن در این پلاسمید واقعی هست؟

<div dir="ltr">

```powershell
blastn -query acquired_genes.fna -subject pEK499.fna -outfmt "6 qseqid sseqid pident length qlen qcovs sstart send" -evalue 1e-20
```

</div>

**خروجی واقعی** (BLAST+ 2.17.0 روی سرور دوره، 2026-11-09):

<div dir="ltr">

```
blaCTX-M-15	EU935739.1	100.000	876	876	100	63828	62953
tet(A)	EU935739.1	100.000	1172	1200	98	53901	52730
```

</div>

**توضیح خروجی:**
- ‏**blaCTX-M-15** با یکسانی و پوشش ۱۰۰٪، روی رشته‌ی منفی (`sstart` بزرگ‌تر از `send`)، از ۶۲٬۹۵۳ تا ۶۳٬۸۲۸. درست همان جای درس ۱ (AMRFinderPlus: ‏62956–63828؛ سه باز فرق در آغاز، چون AMRFinderPlus کدون پایان را نمی‌شمارد).
- ‏**tet(A)** هم هست (پوشش ۹۸٪). ‏blaNDM-1 نیست.
- این جست‌وجو تنها **سه** ژن معلوم ما را می‌جوید. ۱۰ ژن دیگر درس ۱ را نمی‌بیند. برای همه‌ی ژن‌ها، ابزاری با پایگاه کامل لازم است: ResFinder.

### ‏۳.۲ ‏ResFinder در مرورگر (✍️)

همان گام‌های [مسیر ویندوز ماژول ۰۱](../01_AMR_Resistance_Genes/00_lesson_windows.md) (ResFinder): https://genepi.dk/resfinder را باز کنید، گونه را *Escherichia coli* بگذارید، `pEK499.fna` را بارگذاری و Submit کنید.

**با پاسخ معلوم بسنجید** (این‌ها **انتظار** است، نه خروجی دیده‌شده): ژن‌های درس ۱، گام ۲. نام‌ها شاید کمی فرق داشته باشند (برای نمونه `blaTEM-1B` به جای `blaTEM`، یا `aac(6')-Ib-cr` بی شماره‌ی آلل).

| ژن (AMRFinderPlus، درس ۱) | جا | نکته |
| :--- | :--- | :--- |
| ‏blaTEM | 39864–40670 | پوشش ۹۴٪ |
| ‏tet(A) | 52705–53901 | |
| ‏aac(6')-Ib-cr5 | 57401–57952 | |
| ‏blaOXA-1 | 58086–58913 | |
| ‏catB3 | 59054–59494 | **ناقص** (۷۰٪)؛ شاید ResFinder با آستانه‌ی پوشش پیش‌فرض آن را نیاورد |
| ‏blaCTX-M-15 | 62956–63828 | |
| ‏dfrA17، aadA5، qacEdelta1، sul1 | 66738–69513 | اینتگرون کلاس ۱؛ ‏qacEdelta1 (ضدعفونی‌کننده) شاید تنها در DisinFinder بیاید |
| ‏mrx(A)، mph(A) | 73595–75732 | |

---

## ۴. گام ۳: replicon typing با پایگاه PlasmidFinder

**چرا؟** درس ۱، بخش ۵ را ببینید. همان کار ماژول ۰۲ با VFDB، این بار با پایگاه رپلیکون‌ها. پایگاه را از jsDelivr (آینه‌ی مخزن ABRicate) می‌گیریم، همانند VFDB در [مسیر ویندوز ماژول ۰۲](../02_Virulence_Factors/00_lesson_windows.md):

<div dir="ltr">

```powershell
mkdir plasmidfinder
py -c "import urllib.request as u; u.urlretrieve('https://cdn.jsdelivr.net/gh/tseemann/abricate@master/db/plasmidfinder/sequences', 'plasmidfinder/plasmidfinder.fna')"
makeblastdb -in plasmidfinder\plasmidfinder.fna -dbtype nucl -out plasmidfinder\plasmidfinder
blastn -query pEK499.fna -db plasmidfinder\plasmidfinder -perc_identity 80 -max_target_seqs 10000 -outfmt "6 qseqid qstart qend pident length slen stitle" -out pEK499.pf.tsv
(Get-Content pEK499.pf.tsv).Count
```

</div>

**خروجی واقعی** (روی سرور دوره، 2026-11-09؛ دانلود ۷ ثانیه، ‏۴۴۶٬۸۴۶ بایت؛ ‏blastn ‏۰٫۱۶ ثانیه و ۸۵ مگابایت):

<div dir="ltr">

```
Adding sequences from FASTA; added 488 sequences in 0.012867 seconds.
14
```

</div>

همان ۴۸۸ توالی و همان ۱۴ هم‌ردیفی درس ۱.

### ۴.۱ فیلتر ۹۰/۶۰ در Excel (✍️)

درس ۱ این کار را با `awk` و `sort` کرد. در Excel:
1. ‏`pEK499.pf.tsv` را باز کنید (Data ← From Text/CSV، جداکننده Tab). یک سطر سرخط بیفزایید: `contig`، `qstart`، `qend`، `pident`، `length`، `slen`، `stitle`.
2. در H2 بنویسید `=E2/F2` (پوشش) و تا پایین بکشید؛ سرخط H را `cov` بگذارید.
3. ‏Data ← **Filter**. روی ستون `pident`: ‏Number Filters ← Greater Than Or Equal To ← ۹۰. روی ستون `cov`: بزرگ‌تر یا برابر ۰٫۶.
4. ‏Data ← **Sort**: نخست `qstart` (کوچک به بزرگ)، سپس `pident` (بزرگ به کوچک). برای هر `qstart` سطر نخست بهترین است.

**پاسخ معلوم** (همان فیلتر با `awk` روی همین فایل، 2026-11-09؛ نام رپلیکون تکه‌ی دوم `stitle` است، میان `~~~`ها):

<div dir="ltr">

```
qstart	qend	pident	length/slen	cov	replicon
2373	2760	99.742	388/388	1.00	IncFIA_1
2470	2760	91.065	291/295	0.99	FIA(pBK30683)_1
43354	43614	100.000	261/261	1.00	IncFII_1
43354	43614	93.916	263/259	1.02	IncFII(29)_1_pUTI89
43354	43614	93.893	262/262	1.00	IncFII(pCoo)_1_pCoo
43354	43614	93.561	264/264	1.00	IncFII(pSE11)_1_pSE11
```

</div>

**توضیح:** شش سطر از فیلتر می‌گذرند. بهترین سطر هر جایگاه: **IncFIA** (۲۳۷۳)، ‏`FIA(pBK30683)` (۲۴۷۰) و **IncFII** (۴۳۳۵۴). سطر `FIA(pBK30683)` جای آغاز دیگری دارد ولی **درون همان ناحیه‌ی** IncFIA است (۲۴۷۰ تا ۲۷۶۰ درون ۲۳۷۳ تا ۲۷۶۰) و همانندی کمتری دارد؛ پس رپلیکون سوم نیست. سه سطر IncFII دیگر خویشاوندهای ضعیف‌تر همان رپلیکون‌اند. نتیجه همان درس ۱: **IncF با دو رپلیکون FII و FIA**. (پوشش ۱٫۰۲ یعنی هم‌ترازی با یک شکاف از طول رپلیکون بلندتر شده است.)

### ‏۴.۲ ‏PlasmidFinder در مرورگر (✍️)

https://genepi.dk/plasmidfinder را باز کنید، پایگاه **Enterobacteriales** را برگزینید، `pEK499.fna` را بارگذاری و Submit کنید. **انتظار:** ‏IncFII و IncFIA، با آستانه‌های پیش‌فرض ۹۰٪ همانندی و ۶۰٪ پوشش (همان فیلتر بالا). ابزار وب خودش برای هر جایگاه یک سطر می‌دهد؛ ولی شاید ‏`IncFII(29)` یا نام دیگری به جای `IncFII` بیاید، اگر پایگاه وب تازه‌تر از نسخه‌ی ABRicate باشد.

> 📺 **فیلم:** *What Exactly Is a Plasmid*: https://www.youtube.com/watch?v=i4JEao2rQ64
> 📄 **مرجع:** Carattoli A, et al. (2014). *In silico detection and typing of plasmids using PlasmidFinder and plasmid multilocus sequence typing.* Antimicrob Agents Chemother 58:3895–3903. https://doi.org/10.1128/AAC.02412-14

---

## ۵. گام ۴: ژن مقاومت کنار کدام IS است؟ (`gb_context.py`)

**چرا؟** درس ۱، بخش ۶ را ببینید. در لینوکس، ‏`awk` ‏ISها را از GenBank برداشت و `gene_context.py` آن‌ها را با جدول AMRFinderPlus سنجید. در ویندوز جدول AMRFinderPlus نداریم؛ پس **`gb_context.py`** همه‌چیز را از خود رکورد GenBank می‌خواند (با Biopython، بخش 03/04): هم ISها و هم ژن‌ها.

### ۵.۱ فهرست ISها

<div dir="ltr">

```powershell
py $S\03_Mobile_Elements_CRISPR\scripts\gb_context.py pEK499.gb
```

</div>

**خروجی واقعی** (روی سرور دوره، 2026-11-09؛ ‏۰٫۳ ثانیه، ۴۴ مگابایت):

<div dir="ltr">

```
start	end	element
36287	37106	IS26
37107	38746	ISEcp1
40672	41439	IS1
56490	57309	IS26
59496	60315	IS26
63901	64720	IS26
71690	72569	IS6100
75802	76621	IS26
86629	87448	IS26
102302	103069	IS1
113193	115724	IS66
```

</div>

درست همان ۱۱ IS درس ۱ (هفت IS26). ✅

**هسته‌ی اسکریپت:**

<div dir="ltr">

```python
record = SeqIO.read(path, "genbank")
for f in record.features:
    if f.type == "mobile_element":
        name = f.qualifiers.get("mobile_element_type", ["?"])[0].split(":")[-1]
...
d = max(0, e_start - g_end, g_start - e_end)      # 0 = gene and element overlap
```

</div>

‏`f.qualifiers` همان سطرهای `/mobile_element_type="insertion sequence:IS26"` رکورد است؛ `split(":")[-1]` تنها `IS26` را نگه می‌دارد. فاصله‌ی **۰** یعنی ژن و IS روی هم افتاده‌اند.

### ۵.۲ ژن‌های کنار IS

به اسکریپت فاصله (۲۰۰۰ باز) و نام ژن‌ها را **همان‌گونه که در رکورد آمده** می‌دهیم:

<div dir="ltr">

```powershell
py $S\03_Mobile_Elements_CRISPR\scripts\gb_context.py pEK499.gb 2000 bla aacA4 oxa1 catB4 tetA dhfrVII aadA sulI "mph(A)" mrx
```

</div>

> ‏`"mph(A)"` را در گیومه بگذارید: پرانتز در PowerShell (و در bash) معنای ویژه دارد.

**خروجی واقعی:**

<div dir="ltr">

```
gene	product	gene_pos	element	element_pos	distance
bla	beta-lactamase TEM precursor	39948-40676	ISEcp1	37107-38746	1202
bla	beta-lactamase TEM precursor	39948-40676	IS1	40672-41439	0
aacA4	aminoglycoside N(6')-acetyltransferase	57263-57955	IS26	56490-57309	0
aacA4	aminoglycoside N(6')-acetyltransferase	57263-57955	IS26	59496-60315	1541
oxa1	beta-lactamase OXA-1 precursor	58041-58916	IS26	56490-57309	732
oxa1	beta-lactamase OXA-1 precursor	58041-58916	IS26	59496-60315	580
catB4	chloramphenicol acetyltransferase	59054-59602	IS26	56490-57309	1745
catB4	chloramphenicol acetyltransferase	59054-59602	IS26	59496-60315	0
bla	CTX-M-15	62953-63888	IS26	63901-64720	13
mrx	Mrx	73592-74830	IS6100	71690-72569	1023
mrx	Mrx	73592-74830	IS26	75802-76621	972
mph(A)	macrolide 2-phosphotransferase	74827-75732	IS26	75802-76621	70
```

</div>

**توضیح خروجی:** همان ساختار درس ۱ دیده می‌شود: ‏`aacA4` ← `oxa1` ← `catB4` میان **دو IS26** (۵۶۴۹۰ و ۵۹۴۹۶)، و CTX-M-15 در ۱۳ بازی یک IS26. ولی سه فرق مهم با درس ۱ هست:

1. **نام‌های کهنه.** آنوتیشن سال ۲۰۰۸ است و نام‌ها پیش از نام‌گذاری امروزی‌اند. ‏`tetA`، `dhfrVII`، `aadA` و `sulI` هیچ سطری ندارند، چون IS در ۲۰۰۰ بازیشان نیست.

| نام در رکورد (2008) | نام AMRFinderPlus (درس ۱) |
| :--- | :--- |
| ‏`bla` (TEM) / `bla` (CTX-M-15) | ‏blaTEM / blaCTX-M-15 (یک نام برای دو ژن؛ ستون product فرقشان را می‌گوید) |
| ‏`aacA4` | ‏aac(6')-Ib-cr5 |
| ‏`oxa1` | ‏blaOXA-1 |
| ‏`catB4` | ‏catB3 |
| ‏`tetA` | ‏tet(A) |
| ‏`dhfrVII` | ‏dfrA17 (خانواده‌ی dfrA7) |
| ‏`aadA` | ‏aadA5 |
| ‏`sulI` | ‏sul1 |
| ‏`mrx` | ‏mrx(A) |
| (بی CDS) | ‏qacEdelta1 |

2. **مرز ژن‌ها فرق دارد.** آنوتیشن `catB4` را تا **59602** می‌کشد، یعنی ۱۰۷ باز **درون** IS26 (فاصله ۰). ‏AMRFinderPlus در درس ۱ همین ژن را 59054–59494 و **PARTIALX** (۷۰٪) دید: ژن پیش از IS26 بریده شده است. آنوتیشن کهنه بریدگی را نشان نمی‌دهد؛ مقایسه با پایگاه امروزی نشان می‌دهد. همین برای `bla` (TEM) هم هست: رکورد تا ۴۰۶۷۶ و روی IS1، و AMRFinderPlus تا ۴۰۶۷۰ با پوشش ۹۴٪.
3. **آغاز ژن‌ها فرق دارد** (`aacA4` ‏57263 در برابر 57401؛ `oxa1` ‏58041 در برابر 58086): هر آنوتیشن کدون آغاز خود را برگزیده است.

**درس:** آنوتیشن یک رکورد کهنه‌ی GenBank را «پاسخ» نخوانید. برای نام‌های امروزی و ژن‌های ناقص، توالی را به یک ابزار با پایگاه تازه (ResFinder در ویندوز، AMRFinderPlus در لینوکس) بدهید.

### ۵.۳ اینتگرون کلاس ۱ (✍️)

جای اینتگراز را مانند `grep -B1` درس ۱ با `Select-String` بیابید:

<div dir="ltr">

```powershell
Select-String -Path pEK499.gb -Pattern '/gene="int"' -Context 1,0
```

</div>

**انتظار** (از `grep` روی همین فایل): دو جا پیدا می‌شود (ویژگی `gene` و ویژگی `CDS`)؛ سطر پیش از دومی `CDS complement(65567..66580)` است. پس ترتیب: **‏int (65567–66580، رشته‌ی منفی) ← dhfrVII (66537–67211) ← aadA (67342–68130) ← sulI (68590–69516)**؛ همان اینتگرون درس ۱ با نام‌های کهنه. در این آنوتیشن `int` و `dhfrVII` حتی ۴۴ باز روی هم افتاده‌اند (درس ۱ با AMRFinderPlus فاصله‌ی ۱۵۷ باز داد؛ تمرین ۴).

> 📺 **فیلم:** *Transposons Animation – DNA transposable elements*: https://www.youtube.com/watch?v=CroyUMRpbxg
> 📄 **مرجع:** Woodford N, et al. (2009). Antimicrob Agents Chemother 53:4472–4482. https://doi.org/10.1128/AAC.00688-09 · Cock PJA, et al. (2009). *Biopython.* Bioinformatics 25:1422–1423. https://doi.org/10.1093/bioinformatics/btp163

---

## ۶. گام ۵: ژن‌های cas در K-12

**چرا؟** درس ۲، گام ۱ را ببینید. درس لینوکسی سطرهای `gene` با `Name=cas` را با `awk` از GFF ‏K-12 برداشت. در ویندوز همین را با یک سطر پایتون می‌کنیم (`ecoli_k12.gff` در ماژول ۰۱ دانلود شد):

<div dir="ltr">

```powershell
py -c "import csv; [print(f[3], f[4], f[6], f[8].split('Name=')[1].split(';')[0]) for f in csv.reader(open('ecoli_k12.gff'), delimiter='\t') if len(f) == 9 and f[2] == 'gene' and 'Name=cas' in f[8]]"
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`csv.reader(…, delimiter='\t')` | هر سطر GFF را با Tab به ستون‌ها بشکن (`f[0]` = ستون ۱) |
| ‏`len(f) == 9` | سطرهای توضیح (`#`) را کنار بگذار |
| ‏`f[2] == 'gene' and 'Name=cas' in f[8]` | نوع `gene` و نامی که با `cas` آغاز شود (همان `$3=="gene" && $9 ~ /Name=cas/`) |
| ‏`f[8].split('Name=')[1].split(';')[0]` | تنها نام، از پس `Name=` تا نخستین `;` |

**خروجی واقعی** (روی سرور دوره، 2026-11-09):

<div dir="ltr">

```
2878569 2878853 - cas2
2878855 2879772 - cas1
2879788 2880387 - casE
2880374 2881048 - casD
2881051 2882142 - casC
2882155 2882637 - casB
2882630 2884138 - casA
2884553 2887219 - cas3
```

</div>

درست همان هشت ژن درس ۲: سامانه‌ی **نوع I-E**. معنای خروجی را در درس ۲، گام ۱ ببینید.

---

## ۷. گام ۶: آرایه‌ی CRISPR با `find_crispr.py`

اسکریپت `find_crispr.py` تنها کتابخانه‌ی استاندارد پایتون را می‌خواهد و بی تغییر روی ویندوز کار می‌کند. ‏spacerها را در فایل و خلاصه را روی صفحه می‌دهد:

<div dir="ltr">

```powershell
py $S\03_Mobile_Elements_CRISPR\scripts\find_crispr.py genomes\isoC.fna CGGTTTATCCCCGCTGGCGCGGGGAACTC 3 | Set-Content k12_spacers.fna
(Select-String -Path k12_spacers.fna -Pattern ">").Count
Get-Content k12_spacers.fna -TotalCount 4
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`\| Set-Content k12_spacers.fna` | ‏spacerها را در فایل بنویس (به جای `>`؛ بخش «سه اشتباه رایج») |
| ‏`(Select-String … ">").Count` | سطرهای `>` را بشمار (همان `grep -c ">"`) |

**خروجی واقعی** (روی سرور دوره، 2026-11-09؛ ‏۱٫۶ ثانیه، ۲۲ مگابایت):

<div dir="ltr">

```
isoC_chromosome	array1	2877701-2878463	strand +	repeats 13 (exact 10)	spacers 12
isoC_chromosome	array2	2904013-2904407	strand +	repeats 7 (exact 0)	spacers 6
18
>isoC_chromosome_array1_spacer1 len=32
CAGCGTCAGGCGTGAAATCTCACCGTCGTTGC
>isoC_chromosome_array1_spacer2 len=32
TCGGTTCAGGCGTTGCAAACCTGGCTACCGGG
```

</div>

درست همان دو آرایه و ۱۸ spacer درس ۲. ‏array1 درست پیش از `cas2` (۲٬۸۷۸٬۵۶۹) است. توضیح کامل در درس ۲، گام ۲.

---

## ۸. گام ۷: ابزارهای وب برای CRISPR و پلاسمید (✍️)

- ‏**CRISPRCasFinder** (وب): https://crisprcas.i2bc.paris-saclay.fr ‏ژنوم `genomes\isoC.fna` (نزدیک به ۴٫۷ مگابایت) را بارگذاری کنید. **انتظار:** دست‌کم array1 در نزدیکی ۲٬۸۷۷٬۷۰۰ با سطح اطمینان بالا، و ژن‌های cas نوع **I-E**. ‏array2 را با سطح اطمینان خودش بخوانید؛ این ابزار تکرار را از پیش نمی‌داند (درس ۲، بخش ۵).
- ‏**MOB-suite** نسخه‌ی ویندوزی ندارد. همتای نزدیک وب آن برای «این contig پلاسمید است؟» همان PlasmidFinder (گام ۳) است، با همان محدودیت: contig بی رپلیکون، دلیل کروموزومی بودن نیست (درس ۱، بخش ۵).

> 📺 **فیلم:** *Bacterial Adaptive Immunity with CRISPR/Cas9*: https://www.youtube.com/watch?v=MbJ7Hnc2K3Q
> 📄 **مرجع:** Couvin D, et al. (2018). *CRISPRCasFinder, an update of CRISRFinder…* Nucleic Acids Res 46:W246–W251. https://doi.org/10.1093/nar/gky425

---

## ۹. سه اشتباه رایج (مسیر ویندوز)

1. **‏`>` در PowerShell.** در Windows PowerShell 5.1 فایل UTF-16 می‌سازد و `find_crispr.py` یا BLAST فایل را بد می‌خوانند. از `| Set-Content` و `-out` بهره ببرید.
2. **نام‌های امروزی در رکورد کهنه.** ‏`gb_context.py pEK499.gb 2000 blaOXA-1` هیچ سطری نمی‌دهد، چون رکورد آن را `oxa1` نامیده. نخست نام‌های رکورد را ببینید (Ctrl+F در `pEK499.gb` با Notepad).
3. **باور مرز ژن در آنوتیشن.** ‏`catB4` رکورد روی IS26 است؛ در واقع ژن ناقص است. یک ژن که با IS «هم‌پوشانی» دارد، در بسیاری از موارد ژنی است که IS آن را بریده.

---

## جمع‌بندی

| یافته | ویندوز (این درس) | لینوکس (درس‌های ۱ و ۲) |
| :--- | :--- | :--- |
| ‏pEK499 | ‏۱۱۷٬۵۳۶ باز، حلقوی (پایتون) | همان (`curl`) |
| رپلیکون‌ها | ‏IncFIA، IncFII (BLAST + Excel؛ PlasmidFinder وب ✍️) | همان (BLAST + `awk`) |
| ژن‌های مقاومت | ‏blaCTX-M-15 و tet(A) با BLAST؛ ۱۲ ژن با ResFinder (✍️، انتظار) | ‏۱۲ ژن core (AMRFinderPlus) |
| ‏IS | ‏۱۱، هفت IS26 (`gb_context.py`) | همان (`awk`) |
| ژن بریده با IS26 | ‏`catB4` روی IS26 (فاصله ۰؛ مرز آنوتیشن کهنه) | ‏`catB3` ‏PARTIALX ۷۰٪، فاصله ۲ |
| ‏CRISPR در K-12 | ‏۸ ژن cas؛ ۲ آرایه، ۱۸ spacer | همان |

اکنون اگر خواستید، [درس ۱](01_lesson_plasmids_is.md) و [درس ۲](02_lesson_crispr.md) را بخوانید: همان نتیجه با AMRFinderPlus و `awk`.

---

## منابع

- ‏Woodford N, et al. (2009). *Complete nucleotide sequences of plasmids pEK204, pEK499, and pEK516…* Antimicrob Agents Chemother 53:4472–4482. https://doi.org/10.1128/AAC.00688-09
- ‏Carattoli A, et al. (2014). Antimicrob Agents Chemother 58:3895–3903. https://doi.org/10.1128/AAC.02412-14
- ‏Couvin D, et al. (2018). Nucleic Acids Res 46:W246–W251. https://doi.org/10.1093/nar/gky425
- ‏Cock PJA, et al. (2009). *Biopython.* Bioinformatics 25:1422–1423. https://doi.org/10.1093/bioinformatics/btp163
- ‏Camacho C, et al. (2009). *BLAST+: architecture and applications.* BMC Bioinformatics 10:421. https://doi.org/10.1186/1471-2105-10-421
- ‏PlasmidFinder (وب): https://genepi.dk/plasmidfinder · ResFinder (وب): https://genepi.dk/resfinder
- کتاب، Coursera، edX و فیلم‌های بیشتر: بخش منابع [درس ۱](01_lesson_plasmids_is.md) و [درس ۲](02_lesson_crispr.md).

<sub>گام‌های ۱ تا ۶ با همان کد (Python 3 + Biopython 1.87، BLAST+ 2.17.0) روی سرور لینوکسی دوره در 2026-11-09 اجرا شدند و همان عددهای درس‌های لینوکسی را دادند (pEK499 با همان MD5 دانلود `curl`؛ پایگاه PlasmidFinder از jsDelivr، ‏۴۸۸ توالی). روی ویندوز آزموده نشده‌اند. ابزارهای وب، فیلتر Excel و `Select-String` از مستندات‌اند (✍️). نشانی genepi.dk برای PlasmidFinder از روی الگوی ResFinder و VirulenceFinder نوشته شده و در وارسی پایان دوره سنجیده می‌شود.</sub>

</div>
