<div dir="rtl">

# درس (مسیر ویندوز): مولکول‌های کوچک روی ویندوز؛ PubChem، ChEMBL و RDKit

**بخش:** `09_Structural_Bioinformatics` · **ماژول:** `02_Small_Molecules` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز 09/01](../01_Protein_Structure/00_lesson_windows.md) (Miniforge و محیط `structural`)؛ مفهوم‌ها از [درس اصلی](01_lesson.md) · **زمان:** حدود ۳۰ دقیقه · **ابزار:** RDKit (در محیط conda)، Python 3 ([`pubchem_csv.py`](../../windows/pubchem_csv.py)، [`chembl_info.py`](../../windows/chembl_info.py)) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** ‏`pubchem_csv.py` و `mol_props.py` (RDKit 2026.03.1) روی سرور دوره **اجرا شدند** (2026-11-10): `rif.csv` **بایت‌به‌بایت** همان فایل حلقه‌ی `curl` بود و جدول ویژگی‌ها همان جدول درس. ‏**ChEMBL در همان روز از سرور پاسخ نداد** (یک بار timeout و یک بار `HTTP Error 500`)، پس `chembl_info.py` آزموده نشده است؛ خروجی آن را از درس اصلی بخوانید.

---

## در یک نگاه

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| حلقه‌ی `for` با `curl` روی PubChem | ‏`python $W\pubchem_csv.py rif.csv نام۱ نام۲ …` (گام ۱) |
| ‏`curl … ChEMBL \| python3 -c "…"` (دو بار) | ‏`python $W\chembl_info.py rifampin` (گام ۲) |
| ‏`python3 mol_props.py … \| column -t -s$'\t'` | ‏`python mol_props.py … \| ConvertFrom-Csv -Delimiter "`t" \| Format-Table` (گام ۳) |

پیش از آغاز، در PowerShell: `conda activate structural`، `cd $HOME\struct`، و `$P` و `$W` گام ۱ [مسیر ویندوز 09/01](../01_Protein_Structure/00_lesson_windows.md).

---

## ۱. گام ۱: هشت دارو از PubChem

<div dir="ltr">

```powershell
python $W\pubchem_csv.py rif.csv rifampicin rifabutin rifapentine rifaximin "rifamycin SV" ciprofloxacin trimethoprim ampicillin
Get-Content rif.csv | ForEach-Object { $_.Substring(0, [Math]::Min(60, $_.Length)) }
```

</div>

**خروجی واقعی** (سرور دوره):

<div dir="ltr">

```text
wrote rif.csv
name,CID,SMILES,MolecularFormula
"rifampicin",135398735,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C(=C3C(=
"rifabutin",135415564,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C3=C(C4=C
"rifapentine",135403821,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C(=C3C(
"rifaximin",6436173,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C3=C(C4=C(C
"rifamycin SV",6324616,"C[C@H]1/C=C/C=C(\C(=O)NC2=CC(=C3C(=C
"ciprofloxacin",2764,"C1CC1N2C=C(C(=O)C3=CC(=C(C=C32)N4CCNCC
"trimethoprim",5578,"COC1=CC(=CC(=C1OC)OC)CC2=CN=C(N=C2N)N",
"ampicillin",6249,"CC1([C@@H](N2[C@H](S1)[C@@H](C2=O)NC(=O)[
```

</div>

سطر دوم PowerShell جای `cut -c1-70` است (۶۰ نویسه‌ی نخست هر سطر). `pubchem_csv.py` میان درخواست‌ها ۰٫۳ ثانیه صبر می‌کند، همان `sleep 0.3` درس (PubChem بیش از ۵ درخواست در ثانیه نمی‌پذیرد).

---

## ۲. گام ۲: ChEMBL

<div dir="ltr">

```powershell
python $W\chembl_info.py rifampin
```

</div>

✍️ انتظار (خروجی درس اصلی، 2026-10-24؛ همان دو درخواست، همان چاپ):

<div dir="ltr">

```text
CHEMBL374478 RIFAMPIN max_phase 4.0 first_approval 1971 ATC ['J04AB02'] oral True
{'full_mwt': '822.95', 'alogp': '4.34', 'hbd': 6, 'hba': 15, 'rtb': 4, 'psa': '220.15', 'num_ro5_violations': 3}
Bacterial DNA-directed RNA polymerase inhibitor CHEMBL2364672 INHIBITOR
```

</div>

اگر `TimeoutError` یا `HTTP Error 500` گرفتید، ChEMBL شلوغ است (روز نوشتن همین درس هم چنین بود)؛ چند دقیقه بعد دوباره بزنید. نام در ChEMBL نام رسمی آمریکایی است: **rifampin**، نه rifampicin.

---

## ۳. گام ۳: ویژگی‌ها و شباهت با RDKit

<div dir="ltr">

```powershell
python $P\02_Small_Molecules\scripts\mol_props.py rif.csv rifampicin rif3d.sdf | ConvertFrom-Csv -Delimiter "`t" | Format-Table
```

</div>

**خروجی واقعی** (سرور دوره، RDKit 2026.03.1؛ جدول خام پیش از `Format-Table`):

<div dir="ltr">

```text
name	MW	cLogP	HBD	HBA	RotB	TPSA	Ro5_violations	Tanimoto_to_rifampicin
rifampicin	823.0	4.34	6	15	4	220.1	3	1.00
rifabutin	847.0	4.75	5	14	4	209.0	2	0.66
rifapentine	877.0	5.65	6	15	5	220.1	4	0.87
rifaximin	785.9	6.16	5	12	2	198.4	3	0.65
rifamycin SV	697.8	4.75	6	12	2	201.3	3	0.70
ciprofloxacin	331.3	1.58	2	4	3	74.6	0	0.09
trimethoprim	290.3	1.26	2	7	5	105.5	0	0.05
ampicillin	349.4	0.32	3	5	4	112.7	0	0.10
```

</div>

همان جدول درس اصلی. ‏`ConvertFrom-Csv -Delimiter "`t"` خروجی جدولی (با Tab) را به جدول PowerShell می‌برد و `Format-Table` آن را هم‌تراز نشان می‌دهد (جای `column -t`). برای Excel: `python … > props.tsv` **نه**؛ `… | Set-Content props.tsv` ([چرا](../../04_R_Packages/02_Run_Rscript/00_lesson_windows.md)).

‏`rif3d.sdf` (ساختارهای سه‌بعدی) را در PyMOL باز کنید: `pymol rif3d.sdf`.

---

## ۴. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| ‏`rifamycin SV` بی کوتیشن | دو نام جدا: `rifamycin` و `SV` | نام‌های فاصله‌دار را در `"…"` بگذارید |
| ‏`rifampicin` در ChEMBL | ‏`no ChEMBL molecule with preferred name 'rifampicin'` | ‏`rifampin` |
| ‏`python` بیرون از محیط conda | ‏`No module named 'rdkit'` | ‏`conda activate structural` |

✍️ پیام سطر دوم از رفتار `chembl_info.py` است (آزموده نشده، چون ChEMBL پاسخ نداد).

---

## ۵. جمع‌بندی

- ‏PubChem: `pubchem_csv.py` (همان فایل `curl`)؛ ChEMBL: `chembl_info.py` (گاهی کند)؛ RDKit: همان `mol_props.py`، همان جدول.
- جدول‌های Tab-دار در PowerShell: `ConvertFrom-Csv -Delimiter "`t" | Format-Table`.

---

## منابع

### راهنما و درس رایگان
- ‏PubChem PUG REST: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest
- ‏ChEMBL web services: https://chembl.gitbook.io/chembl-interface-documentation/web-services
- ‏RDKit (نصب با conda روی ویندوز): https://www.rdkit.org/docs/Install.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. `pubchem_csv.py` و `mol_props.py` در 2026-11-10 روی سرور دوره اجرا شدند؛ ChEMBL پاسخ نداد (✍️).

</div>
