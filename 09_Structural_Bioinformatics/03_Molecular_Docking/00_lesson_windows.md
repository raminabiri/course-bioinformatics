<div dir="rtl">

# درس (مسیر ویندوز): داکینگ مولکولی با AutoDock Vina روی ویندوز

**بخش:** `09_Structural_Bioinformatics` · **ماژول:** `03_Molecular_Docking` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز 09/01](../01_Protein_Structure/00_lesson_windows.md) (Miniforge، محیط `structural`، `5UAC.cif.gz` و `5UAL.cif.gz`)؛ مفهوم‌ها از [درس اصلی](01_lesson.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** AutoDock Vina (فایل ویندوزی)، Open Babel، pdbfixer، gemmi، RDKit، PyMOL (محیط conda) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** این درس **از مستندات** نوشته شده و روی ویندوز آزموده نشده است. اسکریپت‌های پایتون (`prep_complex.py`، `rmsd_pdbqt.py`) و Open Babel، pdbfixer و PyMOL همان برنامه‌های درس اصلی‌اند (در محیط conda ویندوزی)، پس خروجی‌ها همان خروجی‌های واقعی درس اصلی است. Vina ویندوزی از GitHub می‌آید؛ نسخه‌ی آن ممکن است با درس (1.2.7) فرق کند.

---

## در یک نگاه

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`vina` در محیط conda | ‏**`vina.exe`** از GitHub (گام ۰)؛ conda-forge برای vina نسخه‌ی ویندوزی ندارد |
| ‏`SMI=$(curl … /TXT)` | ‏`$SMI = python -c "…"` (گام ۱) |
| ‏`grep -c`، `grep "active torsions"` | ‏`python $W\zgrep.py … -c`، `Select-String` |
| ‏`C5="--center_x … --size_z 24"` و `$C5` | ‏**آرایه**: `$C5 = @("--center_x", "-111.796", …)` (بخش ۳) |
| ‏`\` پایان سطر | ‏`` ` `` (بک‌تیک)، یا همه در یک سطر |
| ‏`\| tee 5UAC_vina.log` | ‏`\| Tee-Object 5UAC_vina.log` |

---

## ۱. گام ۰: vina.exe

✍️ از صفحه‌ی https://github.com/ccsb-scripps/AutoDock-Vina/releases، فایل ویندوزی تازه‌ترین نسخه (نامش `win` یا `windows` دارد و به `.exe` پایان می‌یابد) را بگیرید، نامش را به `vina.exe` تغییر دهید و در `$HOME\tools` بگذارید. سپس در PowerShell:

<div dir="ltr">

```powershell
conda activate structural
$VINA = "$HOME\tools\vina.exe"
& $VINA --version
```

</div>

‏`& $VINA` برنامه‌ای را اجرا می‌کند که نشانی‌اش در متغیر است ([مسیر ویندوز 08/04](../../08_AMR_Virulence_Phylogeny/04_Phylogenetic_Trees/00_lesson_windows.md)). درس اصلی با Vina 1.2.7 اجرا شد.

---

## ۲. گام ۱: آماده‌سازی گیرنده و لیگاند (درس اصلی، گام ۱ و ۲)

<div dir="ltr">

```powershell
mkdir $HOME\struct\dock; cd $HOME\struct\dock
$P = "$HOME\course-bioinformatics-main\09_Structural_Bioinformatics\99_scripts_data"
$W = "$HOME\course-bioinformatics-main\windows"
Copy-Item ..\5UAC.cif.gz, ..\5UAL.cif.gz .
$SMI = python -c "import urllib.request as u; print(u.urlopen('https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/rifampicin/property/SMILES/TXT').read().decode().strip())"
python $P\03_Molecular_Docking\scripts\prep_complex.py 5UAC.cif.gz C RFP "$SMI" 5UAC
pdbfixer 5UAC_rec.pdb --add-atoms=all --keep-heterogens=none --replace-nonstandard --ph=7.0 --output=5UAC_rec_H.pdb
obabel 5UAC_rec_H.pdb -xr -O 5UAC_rec.pdbqt
obabel 5UAC_lig.mol -O 5UAC_lig.pdbqt
python $W\zgrep.py "^ATOM" 5UAC_rec.pdb 5UAC_rec_H.pdb 5UAC_rec.pdbqt -c
Select-String -Path 5UAC_lig.pdbqt -Pattern "active torsions"
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`$SMI = python -c "…"` | خروجی یک برنامه را در یک متغیر PowerShell بگذار؛ همان `SMI=$(…)` |
| ‏`"$SMI"` | ‏SMILES را **در دوکوتیشن** بدهید؛ نویسه‌هایی مانند `(` و `@` بیرون از کوتیشن برای PowerShell معنای دیگری دارند |
| ‏`pdbfixer`، `obabel` | همان برنامه‌های درس، از محیط conda |

انتظار: همان شمار اتم‌ها و همان شمار پیوندهای چرخان درس اصلی (گام ۲).

---

## ۳. گام ۲: داکینگ (درس اصلی، گام ۳)

دستور بلند را در **یک سطر** بنویسید، یا هر سطر را با بک‌تیک `` ` `` پایان دهید:

<div dir="ltr">

```powershell
& $VINA --receptor 5UAC_rec.pdbqt --ligand 5UAC_lig.pdbqt `
     --center_x 114.680 --center_y 29.079 --center_z -8.026 `
     --size_x 24 --size_y 24 --size_z 24 `
     --exhaustiveness 8 --seed 42 --out 5UAC_docked.pdbqt | Tee-Object 5UAC_vina.log
python $P\03_Molecular_Docking\scripts\rmsd_pdbqt.py 5UAC_lig.pdbqt 5UAC_docked.pdbqt
pymol -cq $P\03_Molecular_Docking\scripts\dock_view.pml
Start-Process dock_view.png
```

</div>

**انتظار** (خروجی واقعی درس اصلی با Vina 1.2.7): RMSD بهترین pose با بلور **۱٫۵۵ Å** (موفق، زیر ۲ Å). با همان `--seed 42` و همان نسخه‌ی Vina باید همان عدد را ببینید؛ با نسخه‌ی دیگر شاید کمی فرق کند.

> ⚠️ **دام PowerShell، گزینه‌ها در یک متغیر.** درس اصلی می‌نویسد `C5="--center_x -111.796 … --size_z 24"` و سپس `vina … $C5`. در PowerShell یک **رشته** به برنامه‌ی بیرونی **یک** آرگومان است، پس Vina همه را یک گزینه‌ی نامفهوم می‌بیند. در PowerShell **آرایه** بسازید؛ آرایه به چند آرگومان باز می‌شود:

<div dir="ltr">

```powershell
$C5 = @("--center_x", "-111.796", "--center_y", "-28.977", "--center_z", "-7.824", "--size_x", "24", "--size_y", "24", "--size_z", "24")
python $P\03_Molecular_Docking\scripts\prep_complex.py 5UAL.cif.gz C RFP "$SMI" 5UAL
pdbfixer 5UAL_rec.pdb --add-atoms=all --keep-heterogens=none --replace-nonstandard --ph=7.0 --output=5UAL_rec_H.pdb
obabel 5UAL_rec_H.pdb -xr -O 5UAL_rec.pdbqt
obabel 5UAL_lig.mol -O 5UAL_lig.pdbqt
& $VINA --receptor 5UAL_rec.pdbqt --ligand 5UAL_lig.pdbqt $C5 --score_only | Select-String "Estimated Free"
```

</div>

انتظار (درس اصلی): `Estimated Free Energy of Binding   : -5.498 (kcal/mol)` برای 5UAL، در برابر `-7.528` برای 5UAC.

---

## ۴. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| ‏`conda install vina` | ‏`PackagesNotFoundError` | ‏`vina.exe` از GitHub (گام ۰) |
| گزینه‌ها در یک رشته (`$C5 = "--center_x …"`) | ‏Vina گزینه را نمی‌شناسد | آرایه‌ی `@(…)` |
| ‏`\` پایان سطر | ‏PowerShell سطر بعد را دستوری جدا می‌خواند | بک‌تیک `` ` `` یا یک سطر |
| ‏SMILES بی کوتیشن | خطای PowerShell روی `(` یا `@` | ‏`"$SMI"` |
| نشانی `vina.exe` با فاصله بی `&` | ‏`Unexpected token` | ‏`& $VINA …` |

✍️ همه‌ی پیام‌های این جدول از مستندات‌اند.

---

## ۵. جمع‌بندی

- ‏Vina در ویندوز: فایل `.exe` از GitHub، اجرا با `& $VINA`؛ بقیه‌ی ابزارها از محیط conda.
- گزینه‌های چندتایی در متغیر: **آرایه**؛ دستور بلند: بک‌تیک.
- اعتبارسنجی همان است: RMSD redocking زیر ۲ Å (درس: ۱٫۵۵ Å).

---

## منابع

### مقاله
- ‏Eberhardt J, Santos-Martins D, Tillack AF, Forli S (2021). *AutoDock Vina 1.2.0: new docking methods, expanded force field, and Python bindings.* Journal of Chemical Information and Modeling 61:3891–3898. https://doi.org/10.1021/acs.jcim.1c00203

### راهنما و درس رایگان
- ‏AutoDock Vina (دانلود و راهنما): https://autodock-vina.readthedocs.io
- ‏Microsoft Learn — *about_Splatting* (آرایه‌ها به‌عنوان آرگومان): https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_splatting
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. این درس از مستندات است (✍️)؛ عددهای «انتظار» از اجرای واقعی درس اصلی‌اند.

</div>
