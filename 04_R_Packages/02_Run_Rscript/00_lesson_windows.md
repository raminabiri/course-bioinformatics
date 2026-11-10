<div dir="rtl">

# درس (مسیر ویندوز): اجرای اسکریپت آماده‌ی R روی ویندوز

**بخش:** `04_R_Packages` · **ماژول:** `02_Run_Rscript` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۱](../01_Install_Packages/00_lesson_windows.md) (R و بسته‌ها، `Rscript` در PATH) · **زمان:** حدود ۳۰ دقیقه، و سپس [درس اصلی](01_lesson.md) · **ابزار:** R 4.6 (ویندوز)، ggplot2، PowerShell · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** اسکریپت `composition.R`، پیام‌های خطا و کدهای کوتاه پایتون روی سرور دوره **اجرا شدند** (2026-11-10) و خروجی‌شان واقعی است. فرمان‌های PowerShell (`$LASTEXITCODE`، `Start-Process`، `-replace`، `Compare-Object`) از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

‏`Rscript script.R ورودی‌ها`، `commandArgs`، پیام‌های `Error` و `Calls:` و `sessionInfo()` در ویندوز همان‌اند. فرق‌ها در **PowerShell** است:

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`mkdir -p ~/r_practice && cd ~/r_practice` و `cp …` | ‏`mkdir`، `cd`، `Copy-Item` (گام ۰) |
| ‏`less script.R` | ‏Notepad یا RStudio |
| ‏`echo "exit=$?"` | ‏**`$LASTEXITCODE`** (بخش ۲) |
| ‏`> out 2> err` | ‏`Start-Process … -RedirectStandardOutput … -RedirectStandardError …` (بخش ۳) |
| ‏`sed -i 's/a/b/' f` | ‏`(Get-Content f) -replace 'a', 'b' \| Set-Content f`، یا ویرایش در Notepad (بخش ۴) |
| ‏`grep -n`، `head`، `cat`، `wc -c` | ‏`Select-String`، `Get-Content`، `(Get-Item f).Length` |
| ‏`file x.png` | یک سطر پایتون (بخش ۴) |
| ‏`diff a b` | ‏`Compare-Object (Get-Content a) (Get-Content b)` |

---

## ۱. گام ۰: پوشه‌ی تمرین

در PowerShell:

<div dir="ltr">

```powershell
$env:Path += ";C:\Program Files\R\R-4.6.1\bin"
mkdir $HOME\r_practice; cd $HOME\r_practice
Copy-Item $HOME\course-bioinformatics-main\01_Linux\99_scripts_data\data\ground_truth.tsv .
$P = "$HOME\course-bioinformatics-main\04_R_Packages\99_scripts_data"
```

</div>

(سطر یکم را با نسخه‌ی R خودتان جور کنید؛ اگر R را همیشگی به PATH افزوده‌اید، لازم نیست. [ماژول ۰۱، گام ۲](../01_Install_Packages/00_lesson_windows.md).)

**خواندن اسکریپت پیش از اجرا** (بخش ۲ درس اصلی): به جای `less`:

<div dir="ltr">

```powershell
notepad $P\02_Run_Rscript\scripts\composition.R
```

</div>

یا آن را در RStudio باز کنید (File ← Open File)؛ RStudio رنگ‌آمیزی دارد. **تنها بخوانید، ذخیره نکنید.**

اجرا (بخش ۳ درس اصلی):

<div dir="ltr">

```powershell
Rscript $P\02_Run_Rscript\scripts\composition.R ground_truth.tsv minigut_sample2 composition_R.png
Start-Process composition_R.png
```

</div>

خروجی، همان درس اصلی؛ سطر پایانی (خروجی واقعی، سرور دوره):

<div dir="ltr">

```text
saved minigut_sample2_genus_R.tsv and composition_R.png 
```

</div>

‏`dir` جای `ls` و `Get-Content minigut_sample2_genus_R.tsv -TotalCount 3` جای `head -3` است.

---

## ۲. کد خروج: `$LASTEXITCODE` به جای `$?`

درس اصلی پس از هر خطا `echo "exit=$?"` می‌زند. در PowerShell، `$?` تنها `True` یا `False` می‌دهد. **کد خروج عددی** برنامه‌ای مانند `Rscript` در `$LASTEXITCODE` است:

<div dir="ltr">

```powershell
Rscript composition.R ground_truth.tsv minigut x.png
"exit=$LASTEXITCODE"
```

</div>

<div dir="ltr">

```text
Fatal error: cannot open file 'composition.R': No such file or directory
exit=2
```

</div>

(همان پیام و همان کد ۲ روی سرور دوره؛ اشتباه «هـ» درس اصلی.) در PowerShell یک رشته‌ی تنها در دوکوتیشن (`"exit=$LASTEXITCODE"`) خودش چاپ می‌شود؛ `echo` لازم نیست ولی کار هم می‌کند.

| کد | یعنی (همان درس اصلی) |
| :--- | :--- |
| ‏`0` | درست تمام شد (هشدار هم شاید داشت) |
| ‏`1` | ‏`Error` در اسکریپت؛ `Execution halted` (برای نمونه نام نمونه‌ی نادرست `minigut3`: کد ۱ روی سرور) |
| ‏`2` | ‏Rscript خود فایل اسکریپت را نیافت |

✍️ در PowerShell 5.1، پیام‌های stderr برنامه‌های بیرونی گاهی **قرمز** و با سرآیندی مانند `Rscript : Error …` و `+ CategoryInfo : NotSpecified` نشان داده می‌شوند. این خطای PowerShell نیست، همان پیام R است که PowerShell بسته‌بندی کرده. خط `Error` خود R را بخوانید.

---

## ۳. جدا کردن خروجی و پیام‌ها: به جای `> out 2> err`

بخش ۵ درس اصلی خروجی را با `> m.out 2> m.err` جدا می‌کند. در **PowerShell 5.1** دو دام دارد: فایل‌ها با کدگذاری **UTF-16** نوشته می‌شوند (اندازه دو برابر، و برخی برنامه‌ها آن‌ها را بد می‌خوانند)، و پیام‌های stderr بسته‌بندی PowerShell را هم می‌گیرند. راه تمیز:

<div dir="ltr">

```powershell
Start-Process -FilePath Rscript -ArgumentList "$P\02_Run_Rscript\scripts\composition.R ground_truth.tsv minigut m.png" -RedirectStandardOutput m.out -RedirectStandardError m.err -NoNewWindow -Wait
Get-Content m.out
Get-Content m.err
(Get-Item m.out).Length; (Get-Item m.err).Length
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`-ArgumentList "…"` | همه‌ی ورودی‌های Rscript در یک رشته (اگر نشانی پوشه‌تان فاصله دارد، کار را در پوشه‌ای بی‌فاصله بکنید) |
| ‏`-RedirectStandardOutput m.out` | ‏stdout به فایل؛ همان `>` |
| ‏`-RedirectStandardError m.err` | ‏stderr به فایل؛ همان `2>` |
| ‏`-NoNewWindow -Wait` | در همین پنجره اجرا کن و تا پایان صبر کن |
| ‏`(Get-Item f).Length` | اندازه به بایت؛ همان `wc -c` |

‏✍️ ‏`m.out` جدول را دارد و `m.err` پیام‌های بارگذاری و `saved …`؛ همان تقسیم درس اصلی. راه ساده‌تر: کار را در **RStudio** بکنید، که خروجی و پیام‌ها را با رنگ‌های جدا نشان می‌دهد.

---

## ۴. عوض کردن یک تنظیم: به جای `sed -i`

بخش ۶ درس اصلی. کپی کنید و نسخه‌ی خودتان را عوض کنید:

<div dir="ltr">

```powershell
Copy-Item $P\02_Run_Rscript\scripts\composition.R my_composition.R
Select-String -Path my_composition.R -Pattern "seagreen"
(Get-Content my_composition.R) -replace 'seagreen', 'steelblue' | Set-Content my_composition.R
Select-String -Path my_composition.R -Pattern "steelblue"
Rscript my_composition.R ground_truth.tsv minigut_sample2 blue.png
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`(Get-Content f)` | همه‌ی سطرهای فایل را بخوان؛ پرانتز یعنی «نخست کامل بخوان، سپس فایل را رها کن» |
| ‏`-replace 'a', 'b'` | در هر سطر، `a` را با `b` جایگزین کن؛ همان `s/a/b/g` (همه‌ی رخدادها) |
| ‏`\| Set-Content f` | نتیجه را در همان فایل بنویس؛ همان `-i` |

✍️ انتظار: `Select-String` سطر ۳۶ را با `seagreen` و سپس با `steelblue` نشان می‌دهد (`my_composition.R:36:  geom_col(fill = "steelblue") +`)، و نمودار آبی است.

**راه ساده‌تر:** ‏`notepad my_composition.R`، با Ctrl+H (Replace) `seagreen` را `steelblue` کنید و ذخیره کنید. برای چند تغییر، همین بهتر است.

> ‏⚠️ ‏`-replace` یک **عبارت باقاعده** می‌گیرد، همانند `sed`. پس `.` یعنی «هر نویسه». برای متن‌هایی مانند `width = 7` مشکلی نیست.

**اندازه‌ی PNG** (جای `file x.png`): Properties ← Details در File Explorer، یا یک سطر پایتون که سرآیند PNG را می‌خواند:

<div dir="ltr">

```powershell
py -c "import struct; d = open('composition_R.png', 'rb').read(24); print(struct.unpack('>II', d[16:24]))"
```

</div>

<div dir="ltr">

```text
(840, 720)
```

</div>

(خروجی واقعی؛ `file` روی سرور هم `840 x 720` گفت.) پهنا ۸۴۰ و بلندی ۷۲۰ پیکسل. ‏`width = 7` اینچ × ۱۲۰ نقطه در اینچ = ۸۴۰.

---

## ۵. ثبت نسخه‌ها و سنجیدن دو فایل

**نسخه‌ها** (بخش ۵ درس اصلی): به یاد قاعده‌ی کوتیشن ویندوز ([ماژول ۰۱، بخش ۴](../01_Install_Packages/00_lesson_windows.md)):

<div dir="ltr">

```powershell
Rscript -e "library(ggplot2); sessionInfo()" | Set-Content versions.txt
Get-Content versions.txt -TotalCount 3
```

</div>

✍️ خط `Running under:` در ویندوز چیزی مانند `Windows 11 x64 (build …)` است، و بخش `locale` کدگذاری ویندوزی را نشان می‌دهد. برای بخش روش‌های مقاله همین سطرها لازم‌اند. ‏`| Set-Content` به جای `>` است، تا فایل UTF-16 نشود.

**سنجیدن دو فایل** (جای `diff`):

<div dir="ltr">

```powershell
Compare-Object (Get-Content minigut_sample2_genus_R.tsv) (Get-Content minigut_sample2_genus.tsv)
```

</div>

✍️ اگر یکی باشند، **هیچ** چاپ نمی‌شود. اگر نه، سطرهای ناهمسان با `<=` (تنها در یکم) و `=>` (تنها در دوم). روی سرور، `diff` این دو فایل (R و پایتون، تمرین ۶) یک سطر ناهمسان داشت: `Escherichia	2` در R و `Escherichia	2.0` در پایتون. `Compare-Object` همین دو سطر را نشان می‌دهد.

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| ‏`echo $?` | ‏`True` یا `False`، نه عدد | ‏`$LASTEXITCODE` |
| ‏`> out` در PowerShell 5.1 | فایل دو برابر بزرگ؛ نویسه‌های درهم در برنامه‌های دیگر | ‏`Start-Process -Redirect…` یا `\| Set-Content` |
| ‏`sed` یا `grep` | ‏`… is not recognized as the name of a cmdlet` | ‏`-replace`، `Select-String` |
| ویرایش خود اسکریپت دوره | اسکریپت اصلی دیگر کار درس را نمی‌کند | همیشه `Copy-Item` و سپس ویرایش کپی |
| پیام قرمز `NativeCommandError` | به نظر خطای PowerShell است | خط `Error` خود R را بخوانید؛ `$LASTEXITCODE` را ببینید |

---

## ۷. جمع‌بندی

- ‏`Rscript $P\…\script.R ورودی‌ها` همان است؛ اسکریپت را پیش از اجرا در Notepad یا RStudio بخوانید.
- کد خروج: `$LASTEXITCODE` (۰ درست، ۱ خطای R، ۲ اسکریپت پیدا نشد).
- جدا کردن stdout و stderr: `Start-Process -RedirectStandardOutput/-RedirectStandardError`.
- ‏`sed -i` ← `(Get-Content f) -replace 'a', 'b' | Set-Content f` یا Notepad.
- ‏`diff` ← `Compare-Object`؛ `file` ← سطر پایتون یا Properties.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز (PowerShell) |
| :--- | :--- |
| کد خروج آخرین برنامه | ‏`$LASTEXITCODE` |
| خروجی و پیام‌ها در دو فایل | ‏`Start-Process -FilePath Rscript -ArgumentList "…" -RedirectStandardOutput o -RedirectStandardError e -NoNewWindow -Wait` |
| جایگزینی متن در فایل | ‏`(Get-Content f) -replace 'a', 'b' \| Set-Content f` |
| جستجو با شماره‌ی سطر | ‏`Select-String -Path f -Pattern "…"` |
| اندازه‌ی فایل | ‏`(Get-Item f).Length` |
| سنجیدن دو فایل متنی | ‏`Compare-Object (Get-Content a) (Get-Content b)` |
| باز کردن تصویر | ‏`Start-Process f.png` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏`$LASTEXITCODE` | کد خروج آخرین برنامه‌ی بیرونی در PowerShell |
| ‏`Start-Process` | اجرای یک برنامه با گزینه‌هایی مانند جدا کردن خروجی‌ها |
| ‏`-replace` | جایگزینی متن با عبارت باقاعده در PowerShell |
| ‏`Compare-Object` | سنجیدن دو فهرست (برای نمونه سطرهای دو فایل) در PowerShell |
| ‏UTF-16 | کدگذاری‌ای که PowerShell 5.1 با `>` به کار می‌برد؛ هر نویسه دست‌کم دو بایت |

---

## منابع

### راهنما و درس رایگان
- ‏Microsoft Learn — *about_Automatic_Variables* (‏`$LASTEXITCODE` و `$?`): https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_automatic_variables
- ‏Microsoft Learn — *Start-Process*: https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process
- ‏Microsoft Learn — *about_Redirection* (کدگذاری `>`): https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_redirection
- ‏CRAN — *R for Windows FAQ* (اجرای Rscript): https://cran.r-project.org/bin/windows/base/rw-FAQ.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### کتاب
- ‏Wickham H, Çetinkaya-Rundel M, Grolemund G (2023). *R for Data Science*, 2nd ed. O'Reilly. (فصل اسکریپت‌ها؛ رایگان: https://r4ds.hadley.nz)

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت R و کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. فرمان‌های PowerShell از مستندات‌اند (✍️).

</div>
