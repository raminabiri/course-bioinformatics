<div dir="rtl">

# درس (مسیر ویندوز): تابع و فایل روی ویندوز؛ خواندن GFF و FASTA

**بخش:** `03_Python` · **ماژول:** `03_Python_Functions_Files` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول‌های ۰۱ و ۰۲](../01_Python_Start/00_lesson_windows.md)؛ [آماده کردن ویندوز](../../windows/README.md) (ژنوم K-12) · **زمان:** حدود ۳۰ دقیقه، و سپس [درس اصلی](01_lesson.md) · **ابزار:** Python 3 (ویندوز)، PowerShell، IDLE، Excel · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** هر سه اسکریپت درس و همه‌ی کدهای پایتون روی سرور دوره **اجرا شدند** (2026-11-10) و خروجی‌شان واقعی است. فرمان‌های PowerShell (`Get-Content`، `Select-String`)، IDLE و Excel از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

تابع، `open`، `split` و `write` در ویندوز همان‌اند. در این ماژول ولی پای **فایل** به میان می‌آید، و ویندوز سه فرق دارد: **مسیر** فایل‌ها، **پوشه‌ی کار** هنگام اجرا، و ابزارهای `head` و `grep` که ویندوز ندارد.

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`cd ~/course-bioinformatics-main/01_Linux/99_scripts_data/data` | ‏`cd $HOME\course` (ژنوم K-12 از [آماده کردن ویندوز](../../windows/README.md)) |
| ‏`host_chr21_region.fa` از `download.sh` | ‏`get_part01_data.py` (گام ۰) |
| ‏`P=~/…/scripts` و `python3 $P/gff_genes.py` | ‏`$P = "…\scripts"` و `py $P\gff_genes.py` |
| ‏`head -n 4 genes.tsv` | ‏`Get-Content genes.tsv -TotalCount 4` |
| ‏`grep -P '^gyrA\t' genes.tsv` | ‏`Select-String`، یا Excel |
| مسیر با `/` | مسیر با `\`؛ **درون رشته‌ی پایتون** مراقب `\` باشید (بخش ۴) |

---

## ۱. گام ۰: پوشه، داده و نشانی اسکریپت‌ها

ژنوم K-12 را در [آماده کردن ویندوز](../../windows/README.md) (بخش «داده‌ی پایه») در `$HOME\course` گرفته‌اید. اگر نه، همان‌جا بروید. در PowerShell:

<div dir="ltr">

```powershell
cd $HOME\course
py $HOME\course-bioinformatics-main\windows\get_part01_data.py
$P = "$HOME\course-bioinformatics-main\03_Python\99_scripts_data\03_Python_Functions_Files\scripts"
dir
```

</div>

| سطر | کار |
| :--- | :--- |
| ‏`get_part01_data.py` | داده‌ی بخش ۰۱ را می‌گیرد: فایل ۵۰۰ کیلوبازی کروموزوم ۲۱ انسان، و ریدهای FASTQ برای ماژول بعد. همان کار `download.sh` با پایتون ([آماده کردن ویندوز](../../windows/README.md)) |
| ‏`$P = "…"` | یک **متغیر PowerShell** برای پوشه‌ی اسکریپت‌ها؛ همانند `P=…` در Bash. در PowerShell نام متغیر همیشه با `$` است، حتی هنگام ساختن |
| ‏`dir` | باید `ecoli_k12.fna`، `ecoli_k12.gff`، `host_chr21_region.fa`، `ground_truth.tsv` و پوشه‌ی `fastq` را ببینید |

فایل گرفته‌شده روی سرور دوره همان MD5 فایل بخش ۰۱ را داشت (`68b50cfb970f4c490bf87388b7f43b3f`).

‏⚠️ ‏`$P` تنها در **همین پنجره‌ی** PowerShell هست. اگر پنجره را بستید، سطرهای `cd` و `$P` را دوباره بزنید.

---

## ۲. اجرای اسکریپت‌های درس

بخش‌های ۲ و ۳ [درس اصلی](01_lesson.md) (تابع، خواندن خط‌به‌خط، `split`) را در `>>>` بخوانید و بنویسید. سپس سه اسکریپت درس را این‌گونه اجرا کنید:

<div dir="ltr">

```powershell
py $P\gff_genes.py ecoli_k12.gff
py $P\gene_table.py ecoli_k12.gff genes.tsv
py $P\fasta_gc.py ecoli_k12.fna host_chr21_region.fa
```

</div>

**خروجی واقعی** (سرور دوره، 2026-11-10):

<div dir="ltr">

```text
genes: 4506
strands: {'+': 2216, '-': 2290}
mean length: 897.4
rpo genes start at: [2709437, 2866559, 3213047, 3344717, 3440040, 3599929, 3822106, 4181245, 4185350]
wrote 4506 genes to genes.tsv
ecoli_k12.fna	NC_000913.3	4641652	50.79
host_chr21_region.fa	chr21part	500000	40.05
```

</div>

همان عددهای درس اصلی و بخش ۰۱. **پوشه‌ی کار** `$HOME\course` است، پس نام فایل‌های داده (`ecoli_k12.gff`) بی مسیر کافی است. تنها اسکریپت‌ها با `$P\` از پوشه‌ی دیگری می‌آیند.

### ۲.۱ دیدن `genes.tsv`: به جای `head` و `grep`

<div dir="ltr">

```powershell
Get-Content genes.tsv -TotalCount 4
Select-String -Path genes.tsv -Pattern "^gyrA\t"
```

</div>

✍️ انتظار (از خروجی واقعی همان فایل روی سرور):

<div dir="ltr">

```text
name	start	end	strand	length
thrL	190	255	+	66
thrA	337	2799	+	2463
thrB	2801	3733	+	933

genes.tsv:2289:gyrA	2336793	2339420	-	2628
```

</div>

| فرمان | همانند | یعنی |
| :--- | :--- | :--- |
| ‏`Get-Content f -TotalCount 4` | ‏`head -n 4 f` | چهار سطر نخست |
| ‏`Select-String -Path f -Pattern "…"` | ‏`grep -n` | سطرهایی که با الگو جورند، با **نام فایل و شماره‌ی سطر** در آغاز (`2289` یعنی سطر ۲۲۸۹) |

‏`^gyrA\t` یعنی «آغاز سطر، `gyrA`، و سپس Tab»؛ همان الگوی درس. بی `\t`، نام‌هایی مانند `gyrAB` هم می‌آمدند.

**راه دیگر:** `genes.tsv` را در **Excel** باز کنید (Data ← From Text/CSV، جداکننده Tab)، و با فیلتر ستون `name` ژن `gyrA` را بیابید. برای جدول‌های بزرگ‌تر، پایتون و pandas (ماژول ۰۶) بهترند.

---

## ۳. اسکریپت‌های خودتان: کجا ذخیره کنید؟

در تمرین‌ها اسکریپت می‌نویسید که `open("ecoli_k12.gff")` دارد. پایتون این نام را در **پوشه‌ی کار** می‌جوید. پس:

- **از این ماژول به بعد، اسکریپت‌هایتان را کنار داده در `$HOME\course` ذخیره کنید.**
- ✍️ کلید **F5** در IDLE، پوشه‌ی کار را **پوشه‌ی خود اسکریپت** می‌کند. اگر اسکریپت کنار داده باشد، `open("ecoli_k12.gff")` کار می‌کند. اگر در پوشه‌ی دیگری باشد، `FileNotFoundError` می‌گیرید.
- به همین دلیل اسکریپت‌های درس (در `$P`) را با F5 اجرا **نکنید**، از PowerShell اجرا کنید (بخش ۲).

### ورودی دادن به اسکریپت: `sys.argv` در ویندوز

اسکریپت‌هایی که `sys.argv[1]` دارند، نام فایل را از خط فرمان می‌گیرند:

<div dir="ltr">

```powershell
py ex2.py ecoli_k12.gff
```

</div>

✍️ در IDLE، F5 ورودی نمی‌دهد و `sys.argv[1]` نیست، پس `IndexError: list index out of range` می‌گیرید (همان اشتباه ۲ درس، خروجی واقعی روی سرور). در IDLE به جای F5 از منوی **Run ← Run… Customized** (`Shift+F5`) بزنید و در کادر باز شده بنویسید `ecoli_k12.gff`.

---

## ۴. دام ویندوز: `\` درون رشته‌ی پایتون

اگر نشانی کامل یک فایل را در پایتون بنویسید:

<div dir="ltr">

```python
f = open("C:\Users\Sara\new.gff")
```

</div>

پایتون حتی اجرا نمی‌کند:

<div dir="ltr">

```text
    f = open("C:\Users\Sara\new.gff")
             ^^^^^^^^^^^^^^^^^^^^^^^
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
```

</div>

(خروجی واقعی روی سرور دوره؛ پایتون لینوکس هم همین رشته را همین‌گونه می‌خواند.)

چرا؟ در رشته‌ی پایتون، `\` آغاز یک **نویسه‌ی ویژه** است: `\t` یعنی Tab و `\n` یعنی پایان خط (درس اصلی، بخش ۳). `\U` آغاز یک کد یونیکد است و `\Users` کد درستی نیست. اگر هم خطا ندهد، بدتر است: `\new.gff` بی‌صدا به «پایان خط + ew.gff» تبدیل می‌شود.

| راه | نمونه |
| :--- | :--- |
| ‏**`/` به جای `\`** (پیشنهادی؛ پایتون ویندوز آن را می‌پذیرد) | ‏`open("C:/Users/Sara/new.gff")` |
| رشته‌ی **خام** با `r` | ‏`open(r"C:\Users\Sara\new.gff")` |
| دو `\` | ‏`open("C:\\Users\\Sara\\new.gff")` |
| هیچ‌کدام: اسکریپت کنار داده، نام بی مسیر | ‏`open("new.gff")` (بخش ۳) |

این دام تنها **درون کد پایتون** است. در PowerShell (`py $P\gff_genes.py …`) و در ورودی‌های `sys.argv`، `\` بی‌خطر است.

---

## ۵. یک نکته درباره‌ی فایل‌هایی که می‌نویسید

‏✍️ ‏`open(…, "w")` در ویندوز در پایان هر سطر دو نویسه می‌نویسد (`\r\n`، شیوه‌ی ویندوز)، نه یک نویسه (`\n`، شیوه‌ی لینوکس). پس `genes.tsv` شما چند هزار بایت بزرگ‌تر از فایل لینوکسی است و MD5 آن فرق دارد. **محتوا یکی است**: Excel، پایتون و pandas هر دو را درست می‌خوانند. اگر روزی فایل را به لینوکس بردید و ابزاری `\r` را بد خواند، در پایتون `open(path, "w", newline="\n")` بنویسید.

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | پیام | چاره |
| :--- | :--- | :--- |
| ‏F5 روی اسکریپتی که `sys.argv[1]` دارد | ‏`IndexError: list index out of range` | ‏Run ← Run… Customized، یا `py ex.py ecoli_k12.gff` در PowerShell |
| اسکریپت در پوشه‌ای جدا از داده، با F5 | ‏`FileNotFoundError: [Errno 2] No such file or directory: 'ecoli_k12.gff'` | اسکریپت را در `$HOME\course` ذخیره کنید |
| ‏`"C:\Users\…"` درون کد | ‏`SyntaxError: (unicode error) 'unicodeescape' …` | ‏`/` یا `r"…"` |
| پنجره‌ی تازه‌ی PowerShell | ‏`$P` خالی است؛ `py \gff_genes.py` فایل را نمی‌یابد | سطرهای گام ۰ را دوباره بزنید |
| نوشتن `head` یا `grep` | ‏`… is not recognized as the name of a cmdlet` | ‏`Get-Content -TotalCount`، `Select-String` |

---

## ۷. جمع‌بندی

- داده در `$HOME\course`؛ اسکریپت‌های درس با `py $P\name.py`، و اسکریپت‌های خودتان **کنار داده**.
- ‏`Get-Content -TotalCount` به جای `head`، و `Select-String` به جای `grep`. یا Excel.
- ‏F5 در IDLE پوشه‌ی کار را پوشه‌ی اسکریپت می‌کند و ورودی نمی‌دهد. برای ورودی: **Run… Customized**.
- درون کد پایتون مسیر را با `/` یا `r"…"` بنویسید.
- فایل‌های نوشته‌شده در ویندوز `\r\n` دارند: محتوا یکی، MD5 نه.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| متغیر PowerShell برای پوشه | ‏`$P = "$HOME\…\scripts"` |
| اجرای اسکریپت درس | ‏`py $P\gff_genes.py ecoli_k12.gff` |
| چند سطر نخست | ‏`Get-Content f -TotalCount 4` |
| جستجو با شماره‌ی سطر | ‏`Select-String -Path f -Pattern "^gyrA\t"` |
| ‏F5 با ورودی در IDLE | ‏Run ← Run… Customized (`Shift+F5`) |
| مسیر درون کد | ‏`"C:/Users/…"` یا `r"C:\Users\…"` |
| نوشتن با پایان سطر لینوکسی | ‏`open(p, "w", newline="\n")` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| پوشه‌ی کار (working directory) | پوشه‌ای که پایتون نام‌های بی مسیر را در آن می‌جوید |
| متغیر PowerShell | نامی با `$` (مانند `$P`) که تنها در همان پنجره هست |
| ‏`Get-Content` / `Select-String` | فرمان‌های PowerShell برای دیدن و جستجوی فایل |
| رشته‌ی خام (raw string) | ‏`r"…"`؛ رشته‌ای که `\` در آن معنای ویژه ندارد |
| ‏`\r\n` | پایان سطر به شیوه‌ی ویندوز؛ در لینوکس تنها `\n` |

---

## منابع

### راهنما و درس رایگان
- ‏Python documentation — *Using Python on Windows* (مسیرها): https://docs.python.org/3/using/windows.html
- ‏Python documentation — *String and Bytes literals* (رشته‌ی خام و `\`): https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
- ‏Python documentation — *IDLE* (Run… Customized): https://docs.python.org/3/library/idle.html
- ‏Microsoft Learn — *Select-String*: https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/select-string
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (فصل فایل‌ها)

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#فیلم‌های-آموزشی)؛ فیلم Corey Schafer درباره‌ی فایل‌ها (درس اصلی، بخش ۳) روی ویندوز هم همان است.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌ها و کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. فرمان‌های PowerShell، IDLE و Excel از مستندات‌اند (✍️).

</div>
