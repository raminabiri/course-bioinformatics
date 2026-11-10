<div dir="rtl">

# درس (مسیر ویندوز): اسکریپت‌های R در یک خط لوله‌ی PowerShell

**بخش:** `04_R_Packages` · **ماژول:** `04_R_in_Pipelines` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۲](../02_Run_Rscript/00_lesson_windows.md) (`$LASTEXITCODE`، `Start-Process`) · **زمان:** حدود ۴۵ دقیقه، همراه [درس اصلی](01_lesson.md) · **ابزار:** R 4.6، PowerShell، اسکریپت [`run_all.ps1`](../99_scripts_data/04_R_in_Pipelines/scripts/run_all.ps1) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** اسکریپت‌های R و نسخه‌ی Bash خط لوله (`run_all.sh`) روی سرور دوره **اجرا شدند** (2026-11-10) و خروجی‌شان واقعی است. **`run_all.ps1` و همه‌ی فرمان‌های PowerShell این درس از مستندات نوشته شده‌اند و هنوز روی ویندوز آزموده نشده‌اند**؛ خروجی‌هایی که برایشان آمده «انتظار» است، از روی اجرای واقعی `run_all.sh`. اگر جایی فرق داشت، گزارش کنید.

---

## در یک نگاه

درس اصلی یک خط لوله‌ی **Bash** (`run_all.sh`) می‌سازد که برای هر نمونه یک اسکریپت R را اجرا می‌کند، گزارش هر گام را در `logs/` می‌نویسد و با نخستین شکست **می‌ایستد** (`set -euo pipefail`). Bash در ویندوز نیست. همین کار را با یک اسکریپت **PowerShell** می‌کنیم: [`run_all.ps1`](../99_scripts_data/04_R_in_Pipelines/scripts/run_all.ps1)، کنار `run_all.sh`.

| درس اصلی (Bash) | مسیر ویندوز (PowerShell) |
| :--- | :--- |
| ‏`set -euo pipefail` | ‏`$ErrorActionPreference = "Stop"` **و** وارسی کد خروج هر `Rscript` (بخش ۲) |
| ‏`for s in $(cut -f1 f \| tail -n +2 \| sort -u)` | ‏``Import-Csv f -Delimiter "`t" \| ForEach-Object { $_.sample } \| Sort-Object -Unique`` |
| ‏`realpath "$1"` | ‏`(Resolve-Path $Table).Path` |
| ‏`$(dirname "$(realpath "$0")")` | ‏`$PSScriptRoot` |
| ‏`> log 2>&1` | ‏`Start-Process … -RedirectStandardOutput x.out -RedirectStandardError x.log` (دو فایل) |
| ‏`bash run_all.sh a b` | ‏`powershell -ExecutionPolicy Bypass -File run_all.ps1 a b` |
| ‏`grep -l "Error" logs/*.log` | ‏`Select-String -Path logs\*.log -Pattern "Error" -List` |

**پیش از خواندن:** از درس اصلی بخش‌های **۱ (داستان)** و **۲ (کد خروج، چراغ سبز و قرمز)** را بخوانید.

---

## ۱. گام ۰: پوشه

<div dir="ltr">

```powershell
$env:Path += ";C:\Program Files\R\R-4.6.1\bin"
mkdir $HOME\r_practice\pipeline; cd $HOME\r_practice\pipeline
Copy-Item $HOME\course-bioinformatics-main\01_Linux\99_scripts_data\data\ground_truth.tsv .
$P = "$HOME\course-bioinformatics-main\04_R_Packages\99_scripts_data"
$R02 = "$P\02_Run_Rscript\scripts"
```

</div>

---

## ۲. حلقه، و خطری که پنهان می‌ماند (بخش ۳ درس اصلی)

نام نمونه‌ها از خود جدول:

<div dir="ltr">

```powershell
Import-Csv ground_truth.tsv -Delimiter "`t" | ForEach-Object { $_.sample } | Sort-Object -Unique
```

</div>

✍️ انتظار: `minigut` و `minigut_sample2` (همان خروجی `cut | tail | sort -u`).

| تکه | یعنی |
| :--- | :--- |
| ‏``Import-Csv f -Delimiter "`t"`` | جدول را بخوان؛ سرستون نام‌ها را می‌دهد، پس `tail -n +2` لازم نیست |
| ‏`ForEach-Object { $_.sample }` | از هر سطر (`$_`) ستون `sample` را بردار؛ همان `cut -f1` |
| ‏`Sort-Object -Unique` | مرتب و یکتا؛ همان `sort -u` |

حلقه با نام نادرست `minigut3`:

<div dir="ltr">

```powershell
foreach ($s in "minigut", "minigut_sample2", "minigut3") {
    Rscript $R02\composition.R ground_truth.tsv $s "$s.png" *> "$s.log"
    "${s}: exit $LASTEXITCODE"
}
```

</div>

✍️ انتظار (از کدهای خروج واقعی همین اسکریپت R روی سرور):

<div dir="ltr">

```text
minigut: exit 0
minigut_sample2: exit 0
minigut3: exit 1
```

</div>

همان درس اصلی: حلقه **تا پایان رفت**، با آنکه `minigut3` شکست خورد. PowerShell هم مانند Bash پس از شکست یک برنامه‌ی بیرونی دستور بعدی را اجرا می‌کند.

| تکه | یعنی |
| :--- | :--- |
| ‏`*> "$s.log"` | **همه‌ی** جریان‌ها در یک فایل؛ همان `> $s.log 2>&1` (در PowerShell 5.1 فایل UTF-16 است؛ برای خواندن با `Get-Content` مشکلی نیست) |
| ‏`"${s}: exit …"` | ‏`${s}` با آکولاد، چون `$s:` بی آکولاد برای PowerShell معنای دیگری دارد (نام «درایو») |

> ‏⚠️ **`$ErrorActionPreference = "Stop"` جای `set -e` را برای `Rscript` نمی‌گیرد.** این تنظیم تنها خطای **فرمان‌های خود PowerShell** را می‌ایستاند. شکست برنامه‌ی بیرونی (Rscript با کد ۱) را نمی‌بیند. پس در خط لوله، کد خروج هر `Rscript` را **خودتان** باید بسنجید. (در PowerShell 7.4 تنظیم تازه‌ای به نام `$PSNativeCommandUseErrorActionPreference` این کار را می‌کند، ولی در PowerShell 5.1 ویندوز نیست.)

---

## ۳. اسکریپت خط لوله: `run_all.ps1`

‏[`run_all.ps1`](../99_scripts_data/04_R_in_Pipelines/scripts/run_all.ps1) را در Notepad باز کنید و کنار `run_all.sh` بخوانید. سه گام همان‌اند (نسخه‌ها، یک نمودار برای هر نمونه، تنوع همه‌ی نمونه‌ها). بخش تازه، تابعی است که هر `Rscript` را اجرا و کد خروجش را وارسی می‌کند:

<div dir="ltr">

```powershell
function Invoke-R([string]$Arguments, [string]$OutFile, [string]$ErrFile) {
    $p = Start-Process -FilePath "Rscript" -ArgumentList $Arguments -WorkingDirectory $work `
        -RedirectStandardOutput (Join-Path $work $OutFile) -RedirectStandardError (Join-Path $work $ErrFile) `
        -NoNewWindow -Wait -PassThru
    if ($p.ExitCode -ne 0) {
        Write-Host "FAILED (exit $($p.ExitCode)); see $ErrFile"
        exit 1
    }
}
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`function Invoke-R(…) { … }` | یک **تابع**: کدی که نام دارد و چند بار صدا زده می‌شود (همانند `def` در پایتون) |
| ‏`-PassThru` | ‏`Start-Process` شیء برنامه را برگرداند، تا `$p.ExitCode` را بخوانیم |
| ‏`if ($p.ExitCode -ne 0)` | اگر کد خروج **برابر نیست** (`-ne`) با ۰ … |
| ‏`exit 1` | کل اسکریپت را با کد ۱ پایان بده؛ همان کار `set -e` |
| بک‌تیک `` ` `` در پایان سطر | ادامه‌ی دستور در سطر بعد؛ همان `\` در Bash |

**گزارش‌ها:** برای هر گام دو فایل: `logs\<نمونه>_composition.log` (پیام‌ها و خطاهای R، همان چیزی که درس اصلی در `.log` می‌خواند) و `.out` (خروجی جدول). در Bash هر دو در یک فایل بودند.

### اجرا

<div dir="ltr">

```powershell
powershell -ExecutionPolicy Bypass -File $P\04_R_in_Pipelines\scripts\run_all.ps1 ground_truth.tsv results
"exit=$LASTEXITCODE"
dir results, results\logs
Get-Content results\versions.txt
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`powershell -File x.ps1 a b` | یک PowerShell تازه که اسکریپت را با دو ورودی اجرا می‌کند؛ همان `bash x.sh a b` |
| ‏`-ExecutionPolicy Bypass` | ویندوز به‌طور پیش‌فرض اجرای فایل‌های `.ps1` را **می‌بندد** (پیام `running scripts is disabled on this system`). این گزینه تنها برای همین یک اجرا آن را باز می‌کند |

✍️ انتظار (از اجرای واقعی `run_all.sh` روی سرور، با همان اسکریپت‌های R):

<div dir="ltr">

```text
composition: minigut
composition: minigut_sample2
diversity: all samples
done; outputs in results
exit=0
```

</div>

و در `results`: ‏`diversity_alpha.tsv`، `diversity_bray.tsv`، `diversity_rarecurve.png`، دو نمودار و دو جدول `*_genus_R.tsv`، `versions.txt` و پوشه‌ی `logs`. در `logs` افزون بر `.log`ها، فایل‌های `.out` هم هست.

---

## ۴. وقتی یک گام شکست می‌خورد (بخش ۵ درس اصلی)

جدول خراب (به جای `sed '1s/read_pairs/reads/'`):

<div dir="ltr">

```powershell
$t = Get-Content ground_truth.tsv
$t[0] = $t[0] -replace 'read_pairs', 'reads'
Set-Content broken.tsv $t
Get-Content broken.tsv -TotalCount 1
powershell -ExecutionPolicy Bypass -File $P\04_R_in_Pipelines\scripts\run_all.ps1 broken.tsv results_broken
"exit=$LASTEXITCODE"
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`$t = Get-Content f` | همه‌ی سطرها در یک فهرست؛ `$t[0]` سطر یکم (شماره از ۰، مانند پایتون) |
| ‏`$t[0] -replace …` | تنها در سطر یکم جایگزین کن؛ همان `1s/…/…/` |

✍️ انتظار:

<div dir="ltr">

```text
sample	reads	accession	organism
composition: minigut
FAILED (exit 1); see logs\minigut_composition.log
exit=1
```

</div>

خط لوله در نخستین شکست **ایستاد**، همانند `set -e`. سپس گزارش مشکل‌دار را پیدا کنید (جای `grep -l` و `cat`):

<div dir="ltr">

```powershell
Select-String -Path results_broken\logs\*.log -Pattern "Error" -List | ForEach-Object { $_.Path }
Get-Content results_broken\logs\minigut_composition.log
```

</div>

‏✍️ ‏`-List` تنها نخستین جور هر فایل را می‌دهد، پس هر فایل یک بار نام برده می‌شود (همان `grep -l`). پیام R همان درس اصلی است (واقعی، از سرور):

<div dir="ltr">

```text
Error in `$<-.data.frame`(`*tmp*`, percent, value = numeric(0)) : 
  replacement has 0 rows, data has 2
Calls: $<- -> $<-.data.frame
Execution halted
```

</div>

**قاعده، همان درس اصلی:** وقتی خط لوله ایستاد، نخست فایلی که `Error` دارد را بیابید، سپس همان یک فایل را بخوانید.

---

## ۵. اشتباه‌های رایج در ویندوز

| اشتباه | پیام | چاره |
| :--- | :--- | :--- |
| اجرای `.\run_all.ps1` بی گزینه | ‏`… cannot be loaded because running scripts is disabled on this system` | ‏`powershell -ExecutionPolicy Bypass -File …` |
| تکیه بر `$ErrorActionPreference = "Stop"` برای Rscript | خط لوله با شکست R ادامه می‌دهد | کد خروج هر `Rscript` را بسنجید (`Invoke-R`) |
| ‏`"$s: exit"` | ‏`Variable reference is not valid. ':' was not followed by a valid variable name character` | ‏`"${s}: exit"` |
| ‏Rscript در PATH نیست | ‏`This command cannot be run due to the error: The system cannot find the file specified.` | ‏`$env:Path` ([ماژول ۰۱، گام ۲](../01_Install_Packages/00_lesson_windows.md)) |
| نشانی نسبی پس از `Set-Location` | ‏`cannot open file 'ground_truth.tsv'` | ‏`Resolve-Path` پیش از `Set-Location` (همان اشتباه ۲ درس اصلی) |

✍️ همه‌ی پیام‌های این جدول از مستندات‌اند.

---

## ۶. جمع‌بندی

- خط لوله‌ی ویندوزی: `run_all.ps1`، اجرا با `powershell -ExecutionPolicy Bypass -File`.
- ‏`$ErrorActionPreference = "Stop"` تنها برای فرمان‌های PowerShell است؛ کد خروج **Rscript** را خودتان با `-PassThru` و `.ExitCode` بسنجید و با `exit 1` بایستید.
- نام نمونه‌ها: `Import-Csv … | ForEach-Object { $_.sample } | Sort-Object -Unique`.
- ‏`Resolve-Path` جای `realpath`، `$PSScriptRoot` جای `dirname $0`.
- یافتن گزارش مشکل‌دار: `Select-String -Path logs\*.log -Pattern "Error" -List`.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | PowerShell |
| :--- | :--- |
| اجرای یک اسکریپت `.ps1` | ‏`powershell -ExecutionPolicy Bypass -File x.ps1 a b` |
| کد خروج برنامه‌ای که با `Start-Process` اجرا شد | ‏`$p = Start-Process … -Wait -PassThru; $p.ExitCode` |
| ایستادن اسکریپت با کد ۱ | ‏`exit 1` |
| یکتای یک ستون جدول | ‏``Import-Csv f -Delimiter "`t" \| ForEach-Object { $_.sample } \| Sort-Object -Unique`` |
| نشانی کامل | ‏`(Resolve-Path f).Path` |
| فایل‌هایی که یک واژه را دارند | ‏`Select-String -Path logs\*.log -Pattern "Error" -List` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏ExecutionPolicy | قاعده‌ی ویندوز درباره‌ی اجرای اسکریپت‌های `.ps1` |
| ‏`$PSScriptRoot` | پوشه‌ی اسکریپتی که در حال اجراست |
| ‏`-PassThru` | گزینه‌ای که شیء نتیجه را برمی‌گرداند (این‌جا: برنامه‌ی اجراشده) |
| ‏`$_` | سطر (شیء) کنونی در `ForEach-Object` |

---

## منابع

### راهنما و درس رایگان
- ‏Microsoft Learn — *about_Execution_Policies*: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_execution_policies
- ‏Microsoft Learn — *about_Preference_Variables* (‏`$ErrorActionPreference` و `$PSNativeCommandUseErrorActionPreference`): https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_preference_variables
- ‏Microsoft Learn — *about_Functions*: https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_functions
- ‏Microsoft Learn — *about_Scripts* (‏`$PSScriptRoot`، `param`): https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_scripts
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### کتاب
- ‏Holmes L (2021). *PowerShell Cookbook*, 4th ed. O'Reilly. (فصل‌های اسکریپت‌نویسی و برنامه‌های بیرونی)

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#منابع). برای آغاز PowerShell، صفحه‌ی آموزشی Microsoft Learn: https://learn.microsoft.com/training/modules/introduction-to-powershell/

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌های R و `run_all.sh` در 2026-11-10 روی سرور دوره اجرا شدند. `run_all.ps1` و فرمان‌های PowerShell از مستندات‌اند و آزموده نشده‌اند (✍️).

</div>
