<div dir="rtl">

# درس (مسیر ویندوز): دینامیک مولکولی با OpenMM روی ویندوز

**بخش:** `09_Structural_Bioinformatics` · **ماژول:** `04_Molecular_Dynamics_Intro` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز 09/01](../01_Protein_Structure/00_lesson_windows.md) (Miniforge و محیط `structural`)؛ مفهوم‌ها از [درس اصلی](01_lesson.md) · **زمان:** حدود ۳۰ دقیقه، و ۳ تا ۱۰ دقیقه برای هر شبیه‌سازی · **ابزار:** OpenMM، mdtraj، matplotlib (محیط conda) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** ‏`md_run.py` و `md_analysis.py` پایتون‌اند و OpenMM 8.6.1 و mdtraj در conda-forge **نسخه‌ی ویندوزی** دارند (وارسی شد، 2026-11-10). ولی عددهای MD حتی روی یک کامپیوتر رقم‌به‌رقم تکرار نمی‌شوند (بخش ۳)؛ آنچه باید همان باشد، الگوهای درس اصلی است. روی ویندوز آزموده نشده است.

---

## در یک نگاه

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`export OPENMM_CPU_THREADS=2` | ‏`$env:OPENMM_CPU_THREADS = 2` |
| ‏`curl -sS -O https://files.rcsb.org/download/1L2Y.pdb` | یک سطر پایتون |
| ‏`python3 md_run.py …`، `md_analysis.py …` | ‏`python …` (همان) |
| ‏`head -3 trpcage_log.csv` | ‏`Get-Content trpcage_log.csv -TotalCount 3` |
| ‏`awk`، `sort -k2,2g` در تمرین‌ها | ‏`Import-Csv` و `Sort-Object`، یا Excel |
| ‏GROMACS (از مستندات) | نسخه‌ی ویندوزی دارد ولی ساختنش دشوار است؛ تنها بخوانید |

---

## ۱. گام ۰ و ۱: شبیه‌سازی Trp-cage

<div dir="ltr">

```powershell
conda activate structural
mkdir $HOME\struct\md; cd $HOME\struct\md
$P = "$HOME\course-bioinformatics-main\09_Structural_Bioinformatics\99_scripts_data"
$env:OPENMM_CPU_THREADS = 2
python -c "import urllib.request as u; u.urlretrieve('https://files.rcsb.org/download/1L2Y.pdb', '1L2Y.pdb')"
python $P\04_Molecular_Dynamics_Intro\scripts\md_run.py 1L2Y.pdb trpcage 100 1
Get-Content trpcage_log.csv -TotalCount 3
python $P\04_Molecular_Dynamics_Intro\scripts\md_analysis.py trpcage_start.pdb trpcage.dcd trpcage_log.csv trpcage
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`$env:OPENMM_CPU_THREADS = 2` | یک متغیر **محیطی** برای همین پنجره؛ همان `export`. OpenMM تنها دو هسته‌ی CPU را به کار می‌برد تا کامپیوتر کند نشود |
| ‏`md_run.py 1L2Y.pdb trpcage 100 1` | ساختار، پیشوند خروجی، ۱۰۰ پیکوثانیه، seed ‏۱ |

**انتظار** (درس اصلی، اجرای واقعی روی سرور): نزدیک به **۱۹۰ ثانیه** و ۳۳۶ مگابایت حافظه برای ۱۰۰ پیکوثانیه. روی لپ‌تاپ شما شاید کندتر یا تندتر. نمودارهای `trpcage_*.png` را با `Start-Process` باز کنید.

---

## ۲. گام ۲ و ۳: سه اجرا

همان دستورهای درس اصلی (بخش ۶)، با `python`:

<div dir="ltr">

```powershell
python $P\04_Molecular_Dynamics_Intro\scripts\md_run.py 1L2Y.pdb trpcage_s2 100 2
python $P\04_Molecular_Dynamics_Intro\scripts\md_analysis.py trpcage_s2_start.pdb trpcage_s2.dcd trpcage_s2_log.csv trpcage_s2
python $P\04_Molecular_Dynamics_Intro\scripts\md_run.py 1L2Y.pdb trpcage_s1b 100 1
python $P\04_Molecular_Dynamics_Intro\scripts\md_analysis.py trpcage_s1b_start.pdb trpcage_s1b.dcd trpcage_s1b_log.csv trpcage_s1b
```

</div>

---

## ۳. انتظار درست از عددها

درس اصلی (بخش ۵) نشان داد که حتی **همان seed** روی همان سرور **همان** مسیر را نمی‌دهد (RMSD نیمه‌ی دوم ۲٫۱۲ در برابر ۲٫۳۰ Å): محاسبه‌ی موازی روی CPU نیروها را همیشه به یک ترتیب جمع نمی‌کند و MD این فرق‌های ریز را بزرگ می‌کند. ✍️ روی ویندوز هم همین است، و پردازنده‌ی دیگر و ساخت دیگری از OpenMM فرق‌ها را بیشتر هم می‌کند. پس:

- عددهای شما **رقم‌به‌رقم** با جدول درس یکی **نخواهند بود**؛ این خطا نیست.
- آنچه باید **همان** باشد، الگوهایی است که درس در هر سه اجرا دید: دو سر زنجیره (ASN1 و SER20) متحرک‌ترین‌اند، RMSD زیر ۴ Å و Rg پیرامون ۷ Å می‌ماند، و دما پیرامون ۳۰۰ K است.

---

## ۴. تمرین‌ها بی `awk` و `sort`

<div dir="ltr">

```powershell
Import-Csv trpcage_rmsf.tsv -Delimiter "`t" | Sort-Object { [double]$_.($_.PSObject.Properties.Name[1]) } | Select-Object -First 3
```

</div>

✍️ ستون دوم (RMSF) را **عددی** مرتب می‌کند (`[double]`؛ بی آن، مرتب‌سازی متنی است و «10» پیش از «2» می‌نشیند؛ همان دام `sort` بی `-g`). برای ترتیب وارونه `-Descending` بیفزایید. ساده‌تر: فایل را در Excel باز کنید و ستون را مرتب کنید.

---

## ۵. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| ‏`export OPENMM_CPU_THREADS=2` | ‏`export : The term 'export' is not recognized` | ‏`$env:OPENMM_CPU_THREADS = 2` |
| بستن پنجره در میانه‌ی شبیه‌سازی | ‏`.dcd` ناقص؛ `md_analysis.py` خطا می‌دهد | صبر کنید (۳ تا ۱۰ دقیقه) یا اجرا را دوباره آغاز کنید |
| سنجیدن رقم‌به‌رقم با درس | «عددهای من فرق دارند!» | بخش ۳: الگو را بسنجید، نه رقم‌ها را |
| ویندوز به خواب رفتن لپ‌تاپ | شبیه‌سازی می‌ایستد | ‏Settings ← Power ← Sleep: Never، تا پایان کار |

✍️ پیام‌های این جدول از مستندات‌اند.

---

## ۶. جمع‌بندی

- ‏OpenMM و mdtraj در محیط conda ویندوزی؛ همان اسکریپت‌ها با `python`.
- ‏`$env:OPENMM_CPU_THREADS = 2` جای `export`.
- تکرارپذیری در MD روی CPU: نه رقم‌ها، تنها **الگوها** (همان درس اصلی، بخش ۵).

---

## منابع

### مقاله
- ‏Eastman P, et al. (2024). *OpenMM 8: Molecular Dynamics Simulation with Machine Learning Potentials.* The Journal of Physical Chemistry B 128:109–116. https://doi.org/10.1021/acs.jpcb.3c06662

### راهنما و درس رایگان
- ‏OpenMM — *Installing OpenMM* (ویندوز با conda): http://docs.openmm.org/latest/userguide/application/01_getting_started.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. این درس از مستندات است (✍️)؛ «انتظار»ها از اجرای واقعی درس اصلی‌اند.

</div>
