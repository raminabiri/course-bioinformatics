<div dir="rtl">

# درس (مسیر ویندوز): Biopython روی ویندوز؛ GenBank، ویژگی‌ها و Entrez

**بخش:** `03_Python` · **ماژول:** `05_Biopython_GenBank` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۴](../04_Biopython_Seq/00_lesson_windows.md) · **زمان:** حدود ۲۰ دقیقه، و سپس [درس اصلی](01_lesson.md) · **ابزار:** Python 3 (ویندوز)، Biopython، PowerShell · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** سه اسکریپت درس (از جمله گرفتن رکورد از NCBI با `Bio.Entrez`) و همه‌ی کدهای پایتون روی سرور دوره **اجرا شدند** (2026-11-10) و خروجی‌شان واقعی است. فرمان‌های PowerShell (`Copy-Item`، `Get-FileHash`) و رفتار پایان سطر در ویندوز از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

‏`SeqIO.read(…, "genbank")`، `features`، `qualifiers`، `.extract()` و `Entrez.efetch` در ویندوز همان‌اند. فرق‌ها:

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| کار درون پوشه‌ی `…/05_Biopython_GenBank/data` و `G=…` برای ژنوم | همه در `$HOME\course`؛ `rpo_region.gb` را یک بار کپی کنید (گام ۰) |
| ‏`nano fetch_region.py` برای گذاشتن ایمیل | کپی اسکریپت و ویرایش در IDLE (بخش ۲) |
| ‏`cmp a b && echo same` | یک سطر پایتون؛ **نه** `Get-FileHash` (بخش ۳) |
| ‏`grep … \| grep -oE 'transl_except=…'` | یک سطر پایتون با `re` (بخش ۴) |

---

## ۱. گام ۰: پوشه و فایل GenBank

‏`rpo_region.gb` (ناحیه‌ی ۱۵ کیلوبازی rpoB و rpoC) همراه دوره است. آن را کنار ژنوم K-12 بگذارید:

<div dir="ltr">

```powershell
cd $HOME\course
$D = "$HOME\course-bioinformatics-main\03_Python\99_scripts_data\05_Biopython_GenBank"
Copy-Item $D\data\rpo_region.gb .
$P = "$D\scripts"
py $P\gb_genes.py rpo_region.gb
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`Copy-Item a .` | ‏`a` را به همین پوشه کپی کن؛ همانند `cp a .` |
| ‏`$P = "$D\scripts"` | یک متغیر PowerShell درون متغیر دیگر؛ مانند Bash |

**خروجی واقعی** (پنج سطر نخست، سرور دوره):

<div dir="ltr">

```text
NC_000913.3 15001 bp
CDS	coaA	1	27	-	316 aa	pantothenate kinase
tRNA	thrU	389	464	+	-	tRNA-Thr
tRNA	tyrU	473	557	+	-	tRNA-Tyr
tRNA	glyT	674	748	+	-	tRNA-Gly
```

</div>

همان جدول بخش ۴ درس اصلی. اکنون بخش‌های ۲ تا ۴ [درس اصلی](01_lesson.md) را بخوانید و کدها را در `>>>` یا فایل IDLE (کنار داده) بنویسید.

---

## ‏۲. Entrez: ایمیل خودتان را بگذارید

‏`fetch_region.py` یک سطر `Entrez.email = "your.name@example.org"` دارد. NCBI می‌خواهد ایمیل **شما** را بداند. فایل اصلی دوره را دست نزنید؛ یک کپی بسازید:

<div dir="ltr">

```powershell
Copy-Item $P\fetch_region.py .
```

</div>

‏`fetch_region.py` را در IDLE باز کنید (File ← Open)، ایمیل خودتان را به جای `your.name@example.org` بنویسید و ذخیره کنید. سپس (اینترنت لازم است):

<div dir="ltr">

```powershell
py fetch_region.py NC_000913.3 4175000 4190000 rpo_region2.gb
```

</div>

**خروجی واقعی** (سرور دوره، 2026-11-10):

<div dir="ltr">

```text
wrote 44417 characters to rpo_region2.gb
```

</div>

> 🔒 **ایمیل و کلید API را در فایلی که با دیگران به اشتراک می‌گذارید (GitHub، ایمیل به همکار) نگذارید.** همین کپی شخصی بس است.

---

## ۳. آیا دو فایل یکی‌اند؟ دام `\r\n`

درس اصلی با `cmp` نشان داد `rpo_region2.gb` بایت‌به‌بایت همان `rpo_region.gb` است. در ویندوز وسوسه می‌شوید MD5 دو فایل را با `Get-FileHash` بسنجید. ولی:

- ‏`rpo_region.gb` دوره در لینوکس ساخته شده و پایان هر سطرش `\n` است.
- ‏`fetch_region.py` در ویندوز با `open(…, "w")` می‌نویسد، پس پایان هر سطر `\r\n` است ([ماژول ۰۳، بخش ۵](../03_Python_Functions_Files/00_lesson_windows.md)).

پس MD5ها **فرق دارند، با آن‌که محتوا یکی است**. روی سرور یک نسخه‌ی `\r\n` از همان فایل ساختیم:

<div dir="ltr">

```text
9253adf761860dccdb38590b056930c5  rpo_region.gb
25b9dcf6b6a3aeda86bcfd1e2037b07f  crlf.gb        (same text, \r\n line endings)
```

</div>

برای سنجیدن **محتوا**، پایتون را به کار ببرید. پایتون هنگام خواندن متن، `\r\n` را به `\n` برمی‌گرداند:

<div dir="ltr">

```powershell
py -c "print(open('rpo_region.gb').read() == open('rpo_region2.gb').read())"
```

</div>

<div dir="ltr">

```text
True
```

</div>

(خروجی واقعی؛ همین سطر روی `crlf.gb` هم `True` داد.) **درس:** MD5 برای سنجیدن **فایل دانلودشده** عالی است (همان کار `get_k12_genome.py`)، ولی برای فایلی که خودتان در ویندوز **نوشته‌اید**، محتوا را بسنجید.

---

## ۴. یافته‌ی سلنوسیستئین: به جای `grep`

بخش ۶ درس اصلی را بخوانید. اسکریپت را این‌گونه اجرا کنید (ژنوم کنار شماست، پس `$G` لازم نیست):

<div dir="ltr">

```powershell
py $P\cds_check.py ecoli_k12.fna ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
CDS: 4300
start codons: {'ATG': 3876, 'GTG': 338, 'TTG': 80, 'ATT': 4, 'CTG': 2}
stop codons: {'TGA': 1242, 'TAA': 2753, 'TAG': 305}
CDS with an internal stop: ['fdnG', 'fdoG', 'fdhF']
```

</div>

(خروجی واقعی؛ ۰٫۳ ثانیه، ۶۱ مگابایت.) برای دیدن `transl_except` در GFF، به جای سه `grep` پشت سر هم، یک سطر پایتون:

<div dir="ltr">

```powershell
py -c "import re; [print(m) for l in open('ecoli_k12.gff') if '\tCDS\t' in l and 'gene=fdnG;' in l for m in re.findall(r'transl_except=[^;]+', l)]"
```

</div>

<div dir="ltr">

```text
transl_except=(pos:1547986..1547988%2Caa:Sec)
```

</div>

(خروجی واقعی.) همان پاسخ درس: کدون TGA در جایگاه ۱٬۵۴۷٬۹۸۶ سلنوسیستئین است.

| تکه | یعنی |
| :--- | :--- |
| ‏`'\tCDS\t' in l` | سطرهای CDS؛ همان `grep -P '\tCDS\t'` |
| ‏`'gene=fdnG;' in l` | تنها ژن fdnG؛ همان `grep 'gene=fdnG;'` |
| ‏`re.findall(r'…', l)` | هر تکه‌ای از سطر که با الگو جور است؛ همان `grep -oE` |

این سطر یک **فهرست‌سازی** (list comprehension) است: یک حلقه‌ی کوتاه در یک سطر. این‌جا تنها برای چاپ به کار رفته است؛ اگر سخت می‌نماید، همان را در یک فایل با `for` و `if` بنویسید.

---

## ۵. جمع‌بندی

- همه‌ی کار در `$HOME\course`؛ `rpo_region.gb` با `Copy-Item`.
- ایمیل را در یک **کپی** از `fetch_region.py` بگذارید، نه در فایل دوره.
- ‏MD5 فایلی که پایتون در ویندوز می‌نویسد با فایل لینوکسی فرق دارد (`\r\n`)؛ محتوا را با `open(a).read() == open(b).read()` بسنجید.
- ‏`grep -oE` در ویندوز: `re.findall` در پایتون.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| کپی فایل به همین پوشه | ‏`Copy-Item a .` |
| سنجیدن محتوای دو فایل متنی | ‏`py -c "print(open('a').read() == open('b').read())"` |
| ‏MD5 یک فایل دانلودشده | ‏`Get-FileHash a -Algorithm MD5` |
| تکه‌ی جور با الگو (`grep -o`) | ‏`re.findall(r'…', line)` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏`Copy-Item` | فرمان PowerShell برای کپی؛ همانند `cp` |
| ‏`Get-FileHash` | فرمان PowerShell برای MD5 یا SHA256 یک فایل؛ همانند `md5sum` |
| فهرست‌سازی (list comprehension) | ‏`[x for … if …]`؛ حلقه‌ی کوتاه در یک سطر |

---

## منابع

### راهنما و درس رایگان
- ‏Biopython Tutorial and Cookbook، فصل Entrez: https://biopython.org/DIST/docs/tutorial/Tutorial.html
- ‏Microsoft Learn — *Get-FileHash*: https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/get-filehash
- ‏Python documentation — *re* (عبارت‌های باقاعده): https://docs.python.org/3/library/re.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (فصل‌های Biopython و عبارت باقاعده)

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#فیلم‌های-آموزشی)؛ فیلم Entrez در بخش ۵ درس اصلی روی ویندوز هم همان است.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌ها و کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. فرمان‌های PowerShell از مستندات‌اند (✍️).

</div>
