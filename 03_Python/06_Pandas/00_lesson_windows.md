<div dir="rtl">

# درس (مسیر ویندوز): pandas و نمودار روی ویندوز

**بخش:** `03_Python` · **ماژول:** `06_Pandas` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول‌های ۰۳ و ۰۴](../04_Biopython_Seq/00_lesson_windows.md) (داده در `$HOME\course`) · **زمان:** حدود ۲۰ دقیقه، و سپس [درس اصلی](01_lesson.md) · **ابزار:** Python 3 (ویندوز)، pandas، matplotlib، Excel · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** دو اسکریپت درس و همه‌ی کدهای پایتون روی سرور دوره **اجرا شدند** (2026-11-10؛ pandas 3.0.5، matplotlib 3.11.1) و خروجی‌شان واقعی است. نصب با pip در ویندوز، باز کردن تصویر، پنجره‌ی `plt.show()` و Excel از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

‏pandas و matplotlib در ویندوز همان‌اند و `read_csv`، `groupby`، `sort_values` و `savefig` همان خروجی را می‌دهند. فرق‌ها:

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏pandas و matplotlib در محیط `bioinfo_course` | ‏`py -m pip install pandas matplotlib openpyxl` (یک بار) |
| ‏`cd …/data` و `genes.tsv` با `gene_table.py` | ‏`$HOME\course`؛ `genes.tsv` را در [ماژول ۰۳](../03_Python_Functions_Files/00_lesson_windows.md) ساخته‌اید |
| «فایل را با دوبار کلیک باز کنید» | همان، یا `Start-Process gene_lengths.png` |
| ‏`cat` و `head` | ‏`Get-Content` |
| جدول در ترمینال | افزون بر آن: **Excel** با `to_csv` یا `to_excel` (بخش ۴) |

---

## ۱. گام ۰: نصب و آماده کردن

در PowerShell:

<div dir="ltr">

```powershell
py -m pip install pandas matplotlib openpyxl
py -c "import pandas, matplotlib; print(pandas.__version__, matplotlib.__version__)"
cd $HOME\course
$P3 = "$HOME\course-bioinformatics-main\03_Python\99_scripts_data\03_Python_Functions_Files\scripts"
$P = "$HOME\course-bioinformatics-main\03_Python\99_scripts_data\06_Pandas\scripts"
py $P3\gene_table.py ecoli_k12.gff genes.tsv
```

</div>

| سطر | کار |
| :--- | :--- |
| ‏`py -m pip install …` | سه کتابخانه را از اینترنت نصب کن: pandas، matplotlib و openpyxl (برای نوشتن فایل Excel). همانند `conda install` |
| ‏`py -c "…"` | نسخه‌ها؛ روی سرور دوره `3.0.5 3.11.1` بود. نسخه‌ی تازه‌تر هم درست کار می‌کند |
| ‏`gene_table.py` | ‏`genes.tsv` را دوباره بساز (اگر از ماژول ۰۳ دارید، لازم نیست): `wrote 4506 genes to genes.tsv` |

✍️ اگر `pip` گفت `WARNING: … is not on PATH` نگران نباشید؛ با `py -m pip` کار می‌کند. اگر `Permission denied` گفت، `py -m pip install --user pandas matplotlib openpyxl` بزنید.

---

## ۲. اجرای اسکریپت‌ها و دیدن نمودار

بخش‌های ۲ تا ۵ [درس اصلی](01_lesson.md) را در `>>>` یا فایل IDLE (کنار `genes.tsv`) بنویسید. سپس:

<div dir="ltr">

```powershell
py $P\gene_lengths.py genes.tsv gene_lengths.png
py $P\composition.py ground_truth.tsv minigut_sample2 composition.png
Start-Process gene_lengths.png
```

</div>

خروجی متنی همان درس اصلی است و در پایان `saved gene_lengths.png` و `saved composition.png` (خروجی واقعی؛ هر کدام کمتر از یک ثانیه و حدود ۱۵۰ مگابایت حافظه). ‏`ground_truth.tsv` را `get_part01_data.py` در [ماژول ۰۴](../04_Biopython_Seq/00_lesson_windows.md) کنار داده گذاشته است.

‏`Start-Process file.png` فایل را با برنامه‌ی پیش‌فرض ویندوز (Photos) باز می‌کند؛ همانند دوبار کلیک در File Explorer. نمودارها همان تصویرهای درس اصلی‌اند.

### ‏`plt.show()`: پنجره به جای فایل

✍️ در ویندوز، اگر در اسکریپت یا IDLE به جای (یا پس از) `fig.savefig(…)` بنویسید `plt.show()`، نمودار در یک **پنجره** باز می‌شود. می‌توانید بزرگ‌نمایی کنید و با دکمه‌ی 💾 ذخیره کنید. اسکریپت تا بستن پنجره منتظر می‌ماند. در سرور لینوکس بی صفحه‌نمایش این کار نمی‌شود؛ برای همین درس اصلی `savefig` را به کار برده است، که در هر دو جا کار می‌کند.

---

## ‏۳. ‏`cat` و `head` در ویندوز

در تمرین‌ها، جدول‌های کوچکی را که pandas می‌نویسد، با `Get-Content` ببینید:

<div dir="ltr">

```powershell
Get-Content minigut_genus.tsv
Get-Content rpo_genes.tsv -TotalCount 3
```

</div>

‏`Get-Content f` همانند `cat f`، و با `-TotalCount 3` همانند `head -n 3` است.

---

## ۴. جدول به Excel

در ویندوز، Excel راه آشنای دیدن جدول است. هر DataFrame را می‌توانید برای Excel بنویسید:

<div dir="ltr">

```python
>>> long = df[df["length"] > 5000]
>>> long.to_csv("long_genes.csv", index=False)
>>> long.to_excel("long_genes.xlsx", index=False)
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`to_csv(…, index=False)` | فایل CSV (جداکننده ویرگول)؛ `index=False` یعنی ستون شماره‌ی سطر را ننویس |
| ‏`to_excel(…)` | فایل واقعی Excel؛ به **openpyxl** نیاز دارد (گام ۰) |

‏`long_genes.csv` روی سرور دوره:

<div dir="ltr">

```text
name,start,end,strand,length
yeeJ,2044995,2052014,+,7020
```

</div>

تنها یک ژن بلندتر از ۵٬۰۰۰ باز است: **yeeJ** با ۷٬۰۲۰ باز، همان بلندترین ژن درس اصلی. سپس `Start-Process long_genes.xlsx` آن را در Excel باز می‌کند.

> ‏⚠️ **Excel نام برخی ژن‌ها را به تاریخ تبدیل می‌کند.** اگر فایل CSV یا TSV را با دوبار کلیک باز کنید، Excel نام‌هایی مانند `SEPT2` یا `MARCH1` (ژن‌های انسانی) را تاریخ می‌پندارد. این اشتباه در هزاران مقاله دیده شده است (Ziemann و همکاران، ۲۰۱۶). راه امن: Data ← From Text/CSV و نوع ستون نام را **Text** بگذارید، یا `to_excel` که نوع ستون‌ها را درست نگه می‌دارد. خود HGNC به همین دلیل این ژن‌ها را نام‌گذاری دوباره کرد (SEPTIN2، MARCHF1).

---

## ۵. اشتباه‌های رایج

سه اشتباه درس اصلی (`sep="\t"` فراموش‌شده، `KeyError: 'lenght'`، `.mean` بی پرانتز) در ویندوز همان‌اند. افزون بر آن‌ها:

| اشتباه | پیام | چاره |
| :--- | :--- | :--- |
| ‏pandas نصب نیست | ‏`ModuleNotFoundError: No module named 'pandas'` | ‏`py -m pip install pandas` |
| ‏`to_excel` بی openpyxl | ‏`ModuleNotFoundError: No module named 'openpyxl'` (یا `ImportError` با همین نام) | ‏`py -m pip install openpyxl` |
| فایل در Excel باز است و پایتون می‌خواهد آن را بنویسد | ‏`PermissionError: [Errno 13] Permission denied: 'long_genes.xlsx'` | فایل را در Excel ببندید؛ ویندوز فایل باز را قفل می‌کند |

✍️ دو پیام آخر از مستندات‌اند. قفل فایل باز ویژه‌ی ویندوز است؛ در لینوکس پیش نمی‌آید.

---

## ۶. جمع‌بندی

- ‏`py -m pip install pandas matplotlib openpyxl` یک بار.
- اسکریپت‌ها با `py $P\…`؛ نمودار با `Start-Process file.png`، یا پنجره با `plt.show()`.
- ‏`Get-Content` به جای `cat` و `head`.
- ‏`to_csv` و `to_excel` برای Excel؛ مراقب تبدیل نام ژن به تاریخ باشید.
- پیش از نوشتن دوباره، فایل را در Excel ببندید.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| نصب کتابخانه | ‏`py -m pip install pandas matplotlib openpyxl` |
| باز کردن تصویر یا فایل Excel | ‏`Start-Process file.png` |
| نمودار در پنجره | ‏`plt.show()` |
| دیدن یک جدول کوچک | ‏`Get-Content f.tsv` |
| نوشتن برای Excel | ‏`df.to_excel("f.xlsx", index=False)` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏pip | نصب‌کننده‌ی کتابخانه‌های پایتون؛ در ویندوز با `py -m pip` |
| ‏openpyxl | کتابخانه‌ای که pandas برای نوشتن و خواندن `.xlsx` به کار می‌برد |
| ‏`Start-Process` | فرمان PowerShell برای باز کردن فایل با برنامه‌ی پیش‌فرض |
| قفل فایل | ویندوز نمی‌گذارد فایلی که در برنامه‌ای باز است، دوباره نوشته شود |

---

## منابع

### راهنما و درس رایگان
- ‏pandas — *Installation* (pip روی ویندوز): https://pandas.pydata.org/docs/getting_started/install.html
- ‏pandas — *DataFrame.to_excel*: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html
- ‏Python Packaging User Guide — *Installing packages* (‏`py -m pip`): https://packaging.python.org/en/latest/tutorials/installing-packages/
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### مقاله
- ‏Ziemann M, Eren Y, El-Osta A (2016). *Gene name errors are widespread in the scientific literature.* Genome Biology 17:177. https://doi.org/10.1186/s13059-016-1044-7

### کتاب
- ‏McKinney W (2022). *Python for Data Analysis*, 3rd ed. O'Reilly. (فصل‌های pandas؛ نسخه‌ی رایگان وب: https://wesmckinney.com/book/)

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#فیلم‌های-آموزشی).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌ها و کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. نصب، Excel و پیام‌های ویژه‌ی ویندوز از مستندات‌اند (✍️).

</div>
