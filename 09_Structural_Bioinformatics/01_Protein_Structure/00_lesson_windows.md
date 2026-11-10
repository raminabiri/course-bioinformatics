<div dir="rtl">

# درس (مسیر ویندوز): ساختار پروتئین روی ویندوز؛ PDB، gemmi، PyMOL و AlphaFold

**بخش:** `09_Structural_Bioinformatics` · **ماژول:** `01_Protein_Structure` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [آماده کردن ویندوز](../../windows/README.md)؛ مفهوم‌ها از درس‌های [۱](01_lesson_pdb.md) و [۲](02_lesson_alphafold.md) · **زمان:** حدود ۴۵ دقیقه (و ۱۵ دقیقه نصب، یک بار برای همه‌ی بخش ۰۹) · **ابزار:** Miniforge (conda برای ویندوز)، gemmi، PyMOL متن‌باز، Python 3 · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** کدهای پایتون این درس (`struct_info.py` با gemmi 0.7.5، و [`zgrep.py`](../../windows/zgrep.py)) روی سرور دوره **اجرا شدند** (2026-11-10) و همان خروجی درس اصلی را دادند. وجود نسخه‌ی ویندوزی (win-64) همه‌ی بسته‌های محیط در conda-forge در همان روز **وارسی شد**؛ ولی نصب Miniforge و ساختن محیط روی ویندوز از **مستندات** است و آزموده نشده است.

---

## در یک نگاه

**خبر خوب بخش ۰۹:** همه‌ی ابزارهای آن (gemmi، PyMOL، RDKit، Open Babel، pdbfixer، OpenMM، mdtraj) در **conda-forge نسخه‌ی ویندوزی** دارند. conda ابزاری ویندوزی است و WSL نمی‌خواهد. پس در ویندوز همان محیط درس را می‌سازید و **همان اسکریپت‌ها** را اجرا می‌کنید. تنها استثنا AutoDock Vina است (ماژول ۰۳).

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`conda env create -f envs/structural.yml` | ‏**Miniforge برای ویندوز** + `envs\structural_windows.yml` (گام ۰) |
| ‏`curl -sS -O https://files.rcsb.org/…` | یک سطر پایتون (گام ۱) |
| ‏`zcat X.cif.gz \| grep …` | ‏[`zgrep.py`](../../windows/zgrep.py) (گام ۱) |
| ‏`python3 …/struct_info.py` | ‏`python …\struct_info.py` (در محیط conda نام برنامه `python` است) |
| ‏`pymol -cq script.pml` | همان، یا PyMOL با پنجره (گام ۳) |

---

## ۱. گام ۰: Miniforge و محیط `structural` (یک بار)

✍️ از مستندات Miniforge:

1. ‏https://github.com/conda-forge/miniforge ← **Miniforge3-Windows-x86_64.exe**. نصب برای **Just Me**؛ مسیر پیش‌فرض (`C:\Users\<شما>\miniforge3`) را بپذیرید.
2. از منوی Start، ‏**Miniforge Prompt** را باز کنید و یک بار بزنید:

<div dir="ltr">

```text
conda init powershell
```

</div>

3. ‏PowerShell را باز کنید. اگر پیام قرمز `… profile.ps1 cannot be loaded because running scripts is disabled on this system` دیدید، یک بار بزنید `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (پاسخ: `Y`) و PowerShell را ببندید و دوباره باز کنید. اکنون آغاز اعلان `(base)` است.
4. محیط را بسازید (چند دقیقه؛ نزدیک به یک گیگابایت):

<div dir="ltr">

```powershell
cd $HOME\course-bioinformatics-main
conda env create -f envs\structural_windows.yml
conda activate structural
python -c "import gemmi, rdkit, openmm; print(gemmi.__version__, rdkit.__version__, openmm.__version__)"
```

</div>

‏[`structural_windows.yml`](../../envs/structural_windows.yml) همان `structural.yml` درس است، **بی vina** (conda-forge برای vina نسخه‌ی ویندوزی ندارد؛ ماژول ۰۳). نسخه‌های win-64 که روی conda-forge وارسی شدند (2026-11-10): gemmi 0.7.5، pymol-open-source 3.1.0، rdkit 2026.09.2، openbabel 3.2.1، openmm 8.6.1، mdtraj 1.11.2.

> ⚠️ از این پس، **پیش از هر کار بخش ۰۹**، در PowerShell بزنید `conda activate structural`. در این محیط، پایتون را با `python` صدا بزنید، نه `py` (`py` پایتون جدای ویندوز را باز می‌کند که gemmi ندارد).

---

## ۲. گام ۱: دانلود و نگاه نخست (درس ۱، بخش ۳)

<div dir="ltr">

```powershell
mkdir $HOME\struct; cd $HOME\struct
$P = "$HOME\course-bioinformatics-main\09_Structural_Bioinformatics\99_scripts_data"
$W = "$HOME\course-bioinformatics-main\windows"
python -c "import urllib.request as u; [u.urlretrieve(f'https://files.rcsb.org/download/{i}.cif.gz', f'{i}.cif.gz') for i in ['5UAC', '5UAL']]"
dir *.cif.gz
python $W\zgrep.py "^ATOM" 5UAC.cif.gz -m 2
python $W\zgrep.py "^HETATM.*RFP" 5UAC.cif.gz -m 2
python $W\zgrep.py "^ATOM|^HETATM" 5UAC.cif.gz -c
python $W\zgrep.py "^_refine.ls_d_res_high|_refine.ls_R_factor_R_free " 5UAC.cif.gz
```

</div>

**خروجی واقعی** (سرور دوره، 2026-11-10):

<div dir="ltr">

```text
ATOM   1     N  N   . PHE A 1 8    ? 79.257  -0.040   50.820   1.00 157.65 ? 8    PHE A N   1 
ATOM   2     C  CA  . PHE A 1 8    ? 79.676  1.063    49.964   1.00 155.06 ? 8    PHE A CA  1 
HETATM 54985 C  C1  . RFP M 6 .    ? 116.718 26.886   -8.554   1.00 159.40 ? 3001 RFP C C1  1 
HETATM 54986 C  C2  . RFP M 6 .    ? 115.495 26.476   -8.055   1.00 157.57 ? 3001 RFP C C2  1 
55049
_refine.ls_d_res_high                            3.800 
_refine.ls_R_factor_R_free                       0.2955 
```

</div>

همان خروجی‌های `zcat | grep` درس: ‏۵۵٬۰۴۹ اتم، وضوح ۳٫۸ Å، R-free ‏۰٫۲۹۵۵.

| ورودی `zgrep.py` | همانند |
| :--- | :--- |
| ‏`"الگو" فایل` | ‏`zcat فایل \| grep -E "الگو"` (فایل `.gz` یا ساده) |
| ‏`-m 2` | ‏`grep -m 2` |
| ‏`-c` | ‏`grep -c` |

---

## ۳. گام ۲ و ۳: gemmi و PyMOL (درس ۱، بخش‌های ۴ و ۵)

<div dir="ltr">

```powershell
python $P\01_Protein_Structure\scripts\struct_info.py 5UAC.cif.gz RFP 4
python $P\01_Protein_Structure\scripts\struct_info.py 5UAL.cif.gz RFP 4
pymol -cq $P\01_Protein_Structure\scripts\rif_pocket.pml
Start-Process rif_pocket.png
```

</div>

‏`struct_info.py` روی سرور همان خروجی درس را داد (سطر نخست: `entry: 5UAC  method: X-RAY DIFFRACTION  resolution: 3.8 A  models: 1`؛ واقعی). ✍️ `pymol -cq` (بی پنجره) در ویندوز هم کار می‌کند و تصویر را کنار ساختار می‌سازد. برای کار با موس، `pymol` را بی گزینه بزنید: پنجره‌ی PyMOL باز می‌شود؛ در خط فرمان پایین آن `@` و نشانی اسکریپت را بنویسید تا همان دستورها اجرا شوند.

> 💡 اسکریپت `.pml` فایل `5UAC.cif.gz` را از **پوشه‌ی کار** می‌خواند؛ پس در `$HOME\struct` باشید (همان قاعده‌ی [مسیر ویندوز 03/03](../../03_Python/03_Python_Functions_Files/00_lesson_windows.md)).

---

## ۴. گام ۴: مدل AlphaFold (درس ۲)

<div dir="ltr">

```powershell
python -c "import gzip, shutil; shutil.copyfileobj(gzip.open(r'$P\data\AF-P0A8V2-F1_from_RCSB-CSM.pdb.gz'), open('AF-P0A8V2-F1.pdb', 'wb'))"
python $W\zgrep.py "^ATOM" AF-P0A8V2-F1.pdb -m 3
python $P\01_Protein_Structure\scripts\af_compare.py AF-P0A8V2-F1.pdb 5UAC.cif.gz C 509,510,512,513,514,516,526,529,531,533,540,564,572,687
```

</div>

سطر یکم جای `zcat … > AF-P0A8V2-F1.pdb` است (`r'…'` رشته‌ی خام پایتون است تا `\` در نشانی ویندوزی دردسر نسازد؛ [مسیر ویندوز 03/03، بخش ۴](../../03_Python/03_Python_Functions_Files/00_lesson_windows.md)). خروجی `af_compare.py` همان درس ۲ (بخش ۴) است: همان کد پایتون، همان فایل‌ها.

---

## ۵. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| فراموش کردن `conda activate structural` | ‏`ModuleNotFoundError: No module named 'gemmi'` | آغاز هر جلسه |
| ‏`py` به جای `python` در محیط conda | همان `No module named 'gemmi'` | در محیط conda: `python` |
| ‏ExecutionPolicy | ‏`profile.ps1 cannot be loaded …`؛ `conda` شناخته نمی‌شود | ‏`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| ساختن محیط با `structural.yml` (لینوکسی) | ‏`PackagesNotFoundError: vina` | ‏`structural_windows.yml` |
| اجرای `.pml` در پوشه‌ی دیگر | ‏PyMOL فایل `5UAC.cif.gz` را نمی‌یابد | ‏`cd $HOME\struct` |

✍️ پیام‌های این جدول از مستندات‌اند.

---

## ۶. جمع‌بندی

- بخش ۰۹ در ویندوز: **Miniforge** و محیط `structural` (بی vina)؛ همان اسکریپت‌ها، همان خروجی‌ها.
- ‏`zgrep.py` جای `zcat | grep`؛ دانلودها با یک سطر پایتون.
- ‏PyMOL با `-cq` (تصویر بی پنجره) یا با پنجره.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز (PowerShell، پس از `conda activate structural`) |
| :--- | :--- |
| دانلود از PDB | ‏`python -c "import urllib.request as u; u.urlretrieve('https://files.rcsb.org/download/5UAC.cif.gz', '5UAC.cif.gz')"` |
| جستجو در فایل `.gz` | ‏`python $W\zgrep.py "^ATOM" X.cif.gz -m 2` |
| شمار سطرها | ‏`python $W\zgrep.py "^ATOM\|^HETATM" X.cif.gz -c` |
| تصویر با PyMOL | ‏`pymol -cq script.pml` |

---

## منابع

### راهنما و درس رایگان
- ‏Miniforge (نصب روی ویندوز): https://github.com/conda-forge/miniforge
- ‏conda — *conda init* (PowerShell): https://docs.conda.io/projects/conda/en/latest/commands/init.html
- ‏PyMOL Wiki — *Running scripts*: https://pymolwiki.org/index.php/Running_Scripts
- همه‌ی منابع درس‌های [۱](01_lesson_pdb.md) و [۲](02_lesson_alphafold.md).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. نصب روی ویندوز از مستندات است (✍️).

</div>
