<div dir="rtl">

# درس (مسیر ویندوز): پن‌ژنوم، بی لینوکس

**بخش:** `07_Bacterial_Genomics` · **ماژول:** `04_Comparative_Pan_Genome` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز 07/02](../02_Genome_Annotation/00_lesson_windows.md)؛ [pandas در ویندوز](../../03_Python/06_Pandas/00_lesson_windows.md)؛ مفهوم‌ها از [درس اصلی](01_lesson.md) · **زمان:** حدود ۳۰ دقیقه · **ابزار:** Panaroo در Galaxy؛ Python 3 (pandas)، Excel · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** کد pandas درس (`pangenome_table.py`) روی سرور دوره **اجرا شد** (2026-11-10)، با یک `.Rtab` که پایان سطرهایش ویندوزی (`\r\n`) بود؛ خروجی واقعی است. درس اصلی هم Panaroo را «از مستندات» آورده است؛ Panaroo در Galaxy از **مستندات** نوشته شده و آزموده نشده است.

---

## در یک نگاه

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`panaroo -i *.gff -o results --clean-mode strict` | ‏**Panaroo در Galaxy** (گام ۱)؛ نسخه‌ی ویندوزی ندارد |
| ‏`cat results/summary_statistics.txt` | ‏`Get-Content` یا Notepad |
| ‏`nano gene_presence_absence.Rtab` | ‏Notepad (کلید Tab) یا Excel ← Save As «Text (Tab delimited)» (گام ۲) |
| ‏`python3 pangenome_table.py` | ‏`py pangenome_table.py`، یا IDLE ← F5 |

**پیش از خواندن:** از درس اصلی بخش‌های **۱ و ۲** (هسته، پوسته، ابر؛ پن‌ژنوم باز و بسته؛ چرا خطای آنوتیشن پن‌ژنوم را باد می‌کند) را بخوانید.

---

## ۱. گام ۱: Panaroo در Galaxy

✍️ از مستندات Galaxy (ابزار **Panaroo** در usegalaxy.eu):

1. ورودی Panaroo فایل‌های **GFF3 همراه توالی** است، همان خروجی Prokka یا **Bakta** (در Bakta وب: فایل `.gff3`). برای هر ژنوم یکی را Upload کنید (نوع gff3).
2. ابزار **Panaroo** ← همه‌ی GFFها ← **Clean mode**: strict (همان `--clean-mode strict` درس). برای هم‌ردیفی هسته: **Core alignment** ← core، با MAFFT.
3. خروجی‌ها همان جدول درس (بخش ۴): `summary_statistics.txt`، `gene_presence_absence.csv` و `.Rtab`، و اگر خواستید `core_gene_alignment.aln`.

‏`gene_presence_absence.csv` را در **Excel** باز کنید؛ هر سطر یک خوشه‌ی ژن و هر ستون یک ژنوم است. `summary_statistics.txt` را با `Get-Content` یا Notepad ببینید.

> 💡 هم‌ردیفی هسته (`core_gene_alignment.aln`) ورودی IQ-TREE است؛ IQ-TREE نسخه‌ی ویندوزی دارد ([مسیر ویندوز 08/04](../../08_AMR_Virulence_Phylogeny/04_Phylogenetic_Trees/00_lesson_windows.md)).

---

## ۲. گام ۲: ماتریس با pandas (بخش ۵ درس اصلی)

**ساختن فایل `.Rtab` فرضی درس:** در Notepad جدول بخش ۵ را بنویسید، میان ستون‌ها کلید **Tab** بزنید (در Notepad کلید Tab یک Tab واقعی می‌گذارد؛ همین را می‌خواهیم)، و با **Save as type: All files** و نام `gene_presence_absence.Rtab` ذخیره کنید ([دام `.txt`](../../03_Python/01_Python_Start/00_lesson_windows.md)). یا در Excel بنویسید و **File ← Save As ← Text (Tab delimited) (*.txt)**، سپس پسوند را به `.Rtab` تغییر دهید.

کد `pangenome_table.py` درس را در IDLE کنار همان فایل ذخیره و F5 بزنید (یا `py pangenome_table.py`).

**خروجی واقعی** (سرور دوره؛ فایل با پایان سطر `\r\n`، همانند فایلی که Notepad می‌سازد):

<div dir="ltr">

```text
Gene
dnaA         1.00
gyrA         1.00
fimH         0.75
group_101    0.25
blaKPC       0.50
group_207    0.50
dtype: float64
['blaKPC', 'group_207']
```

</div>

همان پاسخ درس: `blaKPC` و `group_207` ویژه‌ی دو ایزوله‌ی مقاوم‌اند. pandas پایان سطر ویندوزی را خودش درست می‌خواند. تفسیر (همراهی ≠ علیت) را در درس اصلی بخوانید.

**همان کار در Excel:** یک ستون تازه با فرمول `=SUM(B2:E2)/4` فراوانی هر خوشه را می‌دهد؛ فیلتر روی ستون‌های مقاوم (۱) و غیرمقاوم (۰) خوشه‌های ویژه‌ی مقاوم‌ها را. برای ۴۰ ژنوم و هزاران خوشه، pandas ساده‌تر است.

---

## ۳. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| فاصله به جای Tab در Notepad | ‏pandas یک ستون می‌بیند: `KeyError: 'isoR1'` | میان ستون‌ها Tab بزنید، یا Excel |
| ذخیره با پسوند پنهان `.txt` | ‏`FileNotFoundError: … 'gene_presence_absence.Rtab'` | ‏Save as type: All files |
| دادن GFF بی توالی به Panaroo | خطای Panaroo درباره‌ی FASTA | ‏GFF3 خروجی Bakta یا Prokka (توالی در پایان فایل) |

✍️ پیام سطر سوم از مستندات است. سطرهای یکم و دوم رفتار شناخته‌شده‌ی pandas و پایتون است ([مسیر ویندوز بخش ۰۳](../../03_Python/03_Python_Functions_Files/00_lesson_windows.md)).

---

## ۴. جمع‌بندی

- ‏Panaroo در ویندوز: Galaxy، با GFF3 خروجی Bakta.
- ماتریس حضور و نبود ژن: Excel برای نگاه، pandas برای حساب؛ همان کد درس، همان پاسخ.

---

## منابع

### مقاله
- ‏Tonkin-Hill G, et al. (2020). *Producing polished prokaryotic pangenomes with the Panaroo pipeline.* Genome Biology 21:180. https://doi.org/10.1186/s13059-020-02090-4

### راهنما و درس رایگان
- ‏Panaroo (راهنما): https://gtonkinhill.github.io/panaroo/
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. کد pandas در 2026-11-10 روی سرور دوره اجرا شد. Galaxy از مستندات است (✍️).

</div>
