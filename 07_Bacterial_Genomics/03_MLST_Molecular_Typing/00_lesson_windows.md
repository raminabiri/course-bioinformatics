<div dir="rtl">

# درس (مسیر ویندوز): تعیین توالی‌گونه (MLST)، بی لینوکس

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `03_MLST_Molecular_Typing` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز 07/01](../01_Assembly_Quality/00_lesson_windows.md) (ژنوم K-12 و `ideal_contigs.fna` در `$HOME\genomes`)؛ مفهوم‌ها از [درس اصلی](01_lesson.md) · **زمان:** حدود ۴۵ دقیقه · **ابزار:** PubMLST (وب و REST API)، Python 3 ([`pubmlst_type.py`](../../windows/pubmlst_type.py)) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** ‏`pubmlst_type.py` روی سرور دوره **اجرا شد** (2026-11-10، با اینترنت) روی ژنوم K-12 و روی ۵۰ کانتیگ `ideal_contigs.fna`؛ برای سنجش، برنامه‌ی **`mlst` 2.23.0** هم روی سرور اجرا شد. هر دو **ST10** با همان هفت آلل دادند؛ خروجی‌ها واقعی است. فرم وب PubMLST از **مستندات** نوشته شده است.

---

## در یک نگاه

برنامه‌ی `mlst` (درس اصلی) نسخه‌ی ویندوزی ندارد. ولی کار MLST ساده است: هفت ژن را در ژنوم بیاب، شماره‌ی آلل هر کدام را از **پایگاه PubMLST** بگیر، ST را از ترکیب بخوان. PubMLST خودش همین کار را **روی وب** و از راه **REST API** انجام می‌دهد.

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`mlst contigs.fa` | ‏`py pubmlst_type.py contigs.fa` (گام ۱)، یا فرم وب PubMLST (گام ۲) |
| ‏`mlst --list` | ‏`py pubmlst_type.py --list` |
| ‏`mlst --scheme NAME` | ورودی دوم: نام پایگاه، برای نمونه `pubmlst_saureus_seqdef` |
| ‏`mlst --nopath assemblies/*.fa > mlst.tsv` | یک حلقه‌ی PowerShell (گام ۳) |
| ‏`cut \| sort \| uniq -c` روی جدول | ‏Excel (PivotTable) یا pandas |

**پیش از خواندن:** از درس اصلی بخش‌های **۱ و ۲** (داستان؛ هفت ژن، ST، کمپلکس کلونال، تفکیک MLST) را بخوانید.

---

## ۱. گام ۱: یک ژنوم با `pubmlst_type.py`

<div dir="ltr">

```powershell
cd $HOME\genomes
$W = "$HOME\course-bioinformatics-main\windows"
py $W\pubmlst_type.py ecoli_k12.fna
py $W\pubmlst_type.py ideal_contigs.fna
```

</div>

**خروجی واقعی** (سرور دوره؛ هر کدام حدود ۲ دقیقه، بیشترش انتظار برای پاسخ PubMLST):

<div dir="ltr">

```text
ecoli_k12.fna	pubmlst_ecoli_achtman_seqdef	10	adk(10)	fumC(11)	gyrB(4)	icd(8)	mdh(8)	purA(8)	recA(2)	ST10 Cplx
ideal_contigs.fna	pubmlst_ecoli_achtman_seqdef	10	adk(10)	fumC(11)	gyrB(4)	icd(8)	mdh(8)	purA(8)	recA(2)	ST10 Cplx
```

</div>

برای سنجش، برنامه‌ی `mlst` 2.23.0 روی سرور:

<div dir="ltr">

```text
ideal_contigs.fna	ecoli_achtman_4	10	adk(10)	fumC(11)	gyrB(4)	icd(8)	mdh(8)	purA(8)	recA(2)
```

</div>

**یکسان:** ‏ST10، با پروفایل `10-11-4-8-8-8-2`، همان پروفایل بخش ۲.۱ درس اصلی. PubMLST کمپلکس کلونال (`ST10 Cplx`) را هم می‌گوید.

| ستون | معنی (همان `mlst`) |
| :--- | :--- |
| ۱ | نام فایل |
| ۲ | پایگاه (در `mlst`: نام طرح) |
| ۳ | ‏ST؛ `-` اگر ترکیب در پایگاه نیست |
| ۴ تا ۱۰ | ژن و شماره‌ی آلل |
| آخر | کمپلکس کلونال (تنها PubMLST) |

**فرق مهم با `mlst`:** ‏`pubmlst_type.py` **تنها جور دقیق** را گزارش می‌کند. `mlst` نشانه‌هایی هم دارد (`~10` آلل تازه‌ی نزدیک، `10?` جور ناقص، `-` نبود؛ درس اصلی، بخش ۳). اگر ژنی در اسمبلی شما ناقص یا تازه باشد، `pubmlst_type.py` آن ژن را **نمی‌نویسد** و ST را `-` می‌گوید؛ آن‌گاه فرم وب (گام ۲) جزئیات را نشان می‌دهد.

‏`pubmlst_type.py` گونه را **خودش تشخیص نمی‌دهد** (برخلاف `mlst`). پیش‌فرض *E. coli* (طرح Achtman) است. برای گونه‌ی دیگر:

<div dir="ltr">

```powershell
py $W\pubmlst_type.py --list
py $W\pubmlst_type.py my_staph.fasta pubmlst_saureus_seqdef
```

</div>

> ‏📝 *Klebsiella pneumoniae* و چند گونه‌ی دیگر طرحشان را در **BIGSdb پاستور** (https://bigsdb.pasteur.fr) دارند، نه PubMLST. فرم وب آن‌جا همانند گام ۲ است.

---

## ۲. گام ۲: فرم وب PubMLST

✍️ از مستندات PubMLST:

1. ‏https://pubmlst.org/organisms/escherichia-spp ← **Typing** ← *E. coli* (Achtman) ← **Sequence query** (پرس‌وجوی توالی).
2. فایل `ideal_contigs.fna` را بارگذاری کنید (یا توالی را بچسبانید). **Locus/scheme**: MLST.
3. ‏**Submit**. جدول: هر ژن، شماره‌ی آلل، و اگر جور دقیق نبود، **نزدیک‌ترین آلل** با شمار ناجوری‌ها. در پایان ST و کمپلکس کلونال.

همان API که `pubmlst_type.py` صدا می‌زند، این‌جا با پنجره است. برای یک یا دو ژنوم فرم وب ساده‌تر است؛ برای ده‌ها ژنوم، اسکریپت.

---

## ۳. گام ۳: چند ژنوم در یک جدول

جای `mlst --nopath assemblies/*.fa > mlst.tsv`:

<div dir="ltr">

```powershell
Get-ChildItem assemblies\*.fa | ForEach-Object { py $W\pubmlst_type.py $_.FullName } | Set-Content mlst.tsv
Get-Content mlst.tsv
```

</div>

✍️ برای هر ژنوم یک سطر. ‏`Set-Content` فایل را بی UTF-16 می‌نویسد ([مسیر ویندوز 04/02](../../04_R_Packages/02_Run_Rscript/00_lesson_windows.md)). شمار هر ST (تمرین ۴، جای `cut -f3 | sort | uniq -c`): ‏`mlst.tsv` را در Excel باز کنید (جداکننده Tab؛ سرستون ندارد)، ستون C را برگزینید و Insert ← **PivotTable**؛ یا:

<div dir="ltr">

```powershell
Import-Csv mlst.tsv -Delimiter "`t" -Header file, db, ST | Group-Object ST | Select-Object Count, Name
```

</div>

> ⚖️ **ادب در به کار بردن API:** PubMLST رایگان است و برای پژوهشگران همه‌ی دنیا. ده‌ها ژنوم را یکی‌یکی بفرستید (حلقه‌ی بالا همین است)، نه هم‌زمان. برای صدها ژنوم، `mlst` در Galaxy (ابزار **MLST**) یا روی لینوکس بهتر است.

---

## ۴. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| پایگاه نادرست (گونه‌ی دیگر) | ‏ST `-` و هیچ آللی؛ پیام `no exact allele match` | ‏`--list`؛ پایگاه گونه‌ی خودتان |
| نام پایگاه بی `_seqdef` | ‏`PubMLST said 404` | نام کامل، مانند `pubmlst_ecoli_achtman_seqdef` |
| اسمبلی ناقص (یک ژن روی مرز دو کانتیگ) | یکی از هفت ژن نیست؛ ST `-` | فرم وب (گام ۲) برای جزئیات؛ همان «`-`» درس اصلی |
| بی اینترنت | ‏`URLError` | این راه اینترنت می‌خواهد |

✍️ سطرهای اول تا سوم از رفتار اسکریپت و API است (سطر یکم و دوم روی سرور دیده شد: پاسخ 404 برای طرح نادرست).

---

## ۵. جمع‌بندی

- ‏MLST در ویندوز: **PubMLST**، با فرم وب یا با `pubmlst_type.py` (REST API)؛ همان ST10 و همان آلل‌های `mlst`.
- گونه را خودتان بگویید (`--list`)؛ تنها جور دقیق گزارش می‌شود.
- چند ژنوم: حلقه‌ی PowerShell و شمارش با Excel یا `Group-Object`.
- تفسیر ST برای پرسش شیوع (بخش ۴ درس اصلی) وابسته به سیستم‌عامل نیست: ST یکسان **لازم** است، **بس نیست**.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| ‏ST یک ژنوم *E. coli* | ‏`py $W\pubmlst_type.py genome.fasta` |
| گونه‌ی دیگر | ‏`py $W\pubmlst_type.py genome.fasta pubmlst_saureus_seqdef` |
| فهرست پایگاه‌ها | ‏`py $W\pubmlst_type.py --list` |
| چند ژنوم | ‏`Get-ChildItem *.fa \| ForEach-Object { py $W\pubmlst_type.py $_.FullName } \| Set-Content mlst.tsv` |
| جزئیات آلل‌های ناقص | فرم وب PubMLST ← Sequence query |

---

## منابع

### مقاله
- ‏Jolley KA, Bray JE, Maiden MCJ (2018). *Open-access bacterial population genomics: BIGSdb software, the PubMLST.org website and their applications.* Wellcome Open Research 3:124. https://doi.org/10.12688/wellcomeopenres.14826.1

### راهنما و درس رایگان
- ‏PubMLST REST API: https://bigsdb.readthedocs.io/en/latest/rest.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. `pubmlst_type.py` و `mlst` در 2026-11-10 روی سرور دوره اجرا شدند. فرم وب از مستندات است (✍️).

</div>
