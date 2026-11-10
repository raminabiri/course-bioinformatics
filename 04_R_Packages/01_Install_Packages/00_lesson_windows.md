<div dir="rtl">

# درس (مسیر ویندوز): R و بسته‌هایش روی ویندوز؛ نصب و وارسی

**بخش:** `04_R_Packages` · **ماژول:** `01_Install_Packages` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز بخش ۰۳](../../03_Python/01_Python_Start/00_lesson_windows.md) (PowerShell) · **زمان:** حدود ۴۵ دقیقه (بیشترش زمان دانلود)، و سپس [درس اصلی](01_lesson.md) · **ابزار:** R 4.6 (ویندوز)، RStudio (اختیاری)، PowerShell · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** دستورهای R و اسکریپت `check_packages.R` روی سرور دوره (R 4.6.1) **اجرا شدند** و خروجی‌شان واقعی است. نصب R در ویندوز، پیام‌های نصب بسته‌های **باینری** ویندوز، مسیرهای ویندوزی و رفتار PowerShell از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

درس اصلی R را با **conda** نصب می‌کند. conda در ویندوز هم هست، ولی بسته‌های **bioconda** (مانند `bioconductor-deseq2`) نسخه‌ی ویندوزی **ندارند**. پس در ویندوز راه ساده‌تر و رایج‌تر را می‌رویم: **R از CRAN**، و بسته‌ها با `install.packages` و `BiocManager::install`. خبر خوب: در ویندوز این بسته‌ها **آماده (باینری)** می‌آیند و کامپایل نمی‌خواهند، پس نصبشان از لینوکس **ساده‌تر** است.

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`conda env create -f envs/r_packages.yml` | نصب R از CRAN و سپس یک دستور نصب بسته‌ها (گام‌های ۱ و ۳) |
| ‏`conda activate r_packages` | افزودن پوشه‌ی R به PATH (گام ۲) |
| ‏`Rscript -e 'packageVersion("DESeq2")'` | ‏`Rscript -e "packageVersion('DESeq2')"`؛ **کوتیشن‌ها جابه‌جا** (بخش ۴) |
| ‏`* installing *source* package` | ‏`package '…' successfully unpacked and MD5 sums checked` (باینری) |
| ‏`which Rscript` | ‏`Get-Command Rscript` |
| کتابخانه در `envs/r_packages/lib/R/library` | ‏`C:\Users\…\AppData\Local\R\win-library\4.6` |

**پیش از خواندن:** از درس اصلی بخش‌های **۱ (داستان)** و **۲ (گوشی و برنامه‌ها)** را بخوانید.

---

## ۱. گام ۱: نصب R (و اگر خواستید RStudio)

1. ‏https://cran.r-project.org ← **Download R for Windows** ← **base** ← **Download R-4.6.x for Windows**.
2. نصب‌کننده را اجرا کنید و همه‌ی گزینه‌های پیش‌فرض را بپذیرید. R در `C:\Program Files\R\R-4.6.x` نصب می‌شود.
3. **اختیاری:** ‏RStudio Desktop از https://posit.co/download/rstudio-desktop/. درس R را در این دوره نمی‌آموزیم و همه‌ی کارها از PowerShell شدنی است، ولی RStudio برای دیدن نمودارها و ماژول 08/04 سودمند است.

> ‏💡 **Rtools لازم نیست.** Rtools ابزار کامپایل بسته‌ها از **کد منبع** در ویندوز است. بسته‌های این دوره باینری ویندوزی دارند. اگر روزی بسته‌ای پیام `Rtools is required to build R packages` داد، Rtools هم‌نسخه‌ی R خود را از https://cran.r-project.org/bin/windows/Rtools/ نصب کنید.

---

## ۲. گام ۲: `Rscript` در PowerShell

نصب‌کننده‌ی R **پوشه‌ی خود را به PATH نمی‌افزاید**. پس اگر در PowerShell بنویسید `Rscript`، پیام `Rscript : The term 'Rscript' is not recognized…` می‌گیرید. در هر پنجره‌ی تازه‌ی PowerShell:

<div dir="ltr">

```powershell
$env:Path += ";C:\Program Files\R\R-4.6.1\bin"
Rscript --version
```

</div>

**شماره‌ی نسخه را با پوشه‌ی خودتان جور کنید** (در File Explorer به `C:\Program Files\R` بروید و نام پوشه را ببینید). خروجی، همانند سرور دوره:

<div dir="ltr">

```text
Rscript (R) version 4.6.1 (2026-06-24)
```

</div>

| تکه | یعنی |
| :--- | :--- |
| ‏`$env:Path` | متغیر PATH در PowerShell: پوشه‌هایی که ویندوز برنامه‌ها را در آن‌ها می‌جوید؛ همان `$PATH` لینوکس |
| ‏`+= ";…\bin"` | یک پوشه به پایانش بیفزا؛ در ویندوز جداکننده `;` است (در لینوکس `:`) |

این تنها برای **همین پنجره** است، همانند `conda activate`. اگر می‌خواهید همیشگی شود: منوی Start ← «environment variables» ← **Edit environment variables for your account** ← ‏`Path` ← **New** ← ‏`C:\Program Files\R\R-4.6.1\bin`. سپس PowerShell را ببندید و دوباره باز کنید.

**کدام R را اجرا می‌کنم؟** (جای `which Rscript`):

<div dir="ltr">

```powershell
Get-Command Rscript
```

</div>

✍️ ستون `Source` باید `C:\Program Files\R\R-4.6.1\bin\Rscript.exe` باشد. اگر دو نسخه‌ی R نصب کرده‌اید، همانی اجرا می‌شود که نخست در PATH آمده است: همان «اشتباه ۳» درس اصلی، به شکل ویندوزی.

---

## ۳. گام ۳: نصب همه‌ی بسته‌های بخش ۰۴

جای `conda env create`، یک دستور. در PowerShell (پس از گام ۲):

<div dir="ltr">

```powershell
Rscript -e "install.packages(c('BiocManager', 'ggplot2', 'vegan', 'ape'), repos = 'https://cloud.r-project.org')"
Rscript -e "BiocManager::install(c('DESeq2', 'ggtree'), update = FALSE, ask = FALSE)"
```

</div>

✍️ چند دقیقه طول می‌کشد (چند صد مگابایت). برای هر بسته، پیامی مانند این می‌بینید:

<div dir="ltr">

```text
package 'vegan' successfully unpacked and MD5 sums checked
```

</div>

این همتای ویندوزی `* DONE (vegan)` در درس اصلی است: بسته‌ی **باینری** (`.zip`) گرفته، باز و وارسی شد. خط `*source* package` و کامپایل را **نمی‌بینید**. اگر پیامی با `Error` یا `had non-zero exit status` دیدید، کادر کنجکاوهای درس اصلی را ببینید.

| تکه | یعنی |
| :--- | :--- |
| ‏`repos = '…'` | نشانی CRAN؛ `cloud.r-project.org` خودش نزدیک‌ترین آینه را برمی‌گزیند |
| ‏`update = FALSE, ask = FALSE` | بسته‌های دیگر را به‌روز نکن و چیزی نپرس (در `Rscript` کسی نیست که پاسخ دهد) |

> 📝 **ویندوز و کتابخانه‌ی شخصی:** R نمی‌تواند در `C:\Program Files` بنویسد (اجازه‌ی مدیر لازم است). پس بار نخست می‌پرسد `Would you like to use a personal library instead?`. در `Rscript` پرسشی نمی‌شود و R خودش کتابخانه‌ی شخصی را در `C:\Users\<نام شما>\AppData\Local\R\win-library\4.6` به کار می‌برد. اگر خطای `'lib = "C:/Program Files/R/R-4.6.1/library"' is not writable` گرفتید، یک بار R یا RStudio را (نه به‌عنوان مدیر) باز کنید، `install.packages("ape")` بزنید و به پرسش **Yes** بگویید.

### وارسی همه با `check_packages.R`

<div dir="ltr">

```powershell
$P = "$HOME\course-bioinformatics-main\04_R_Packages\99_scripts_data"
Rscript $P\01_Install_Packages\scripts\check_packages.R
```

</div>

**خروجی واقعی روی سرور دوره** (نسخه‌های شما شاید تازه‌تر باشند):

<div dir="ltr">

```text
R: R version 4.6.1 (2026-06-24) 
BiocManager  1.30.27
ggplot2      4.0.3
vegan        2.7.6
ape          5.8.1
DESeq2       1.52.0
ggtree       4.2.0
```

</div>

هیچ `NOT installed` نباید بماند. اکنون بخش‌های ۳ تا ۵ [درس اصلی](01_lesson.md) را بخوانید، با فرق بخش بعد.

---

## ۴. دام PowerShell: کوتیشن‌ها در `Rscript -e`

درس اصلی (بخش ۳) می‌گوید: «بیرون تک‌کوتیشن و درون دوکوتیشن»: `Rscript -e 'packageVersion("DESeq2")'`. در **PowerShell 5.1** (همانی که همراه ویندوز ۱۰ و ۱۱ است)، دوکوتیشن‌های **درون** آرگومان برنامه‌های بیرونی بی‌صدا **دور ریخته می‌شوند**. پس R این را می‌گیرد: `packageVersion(DESeq2)`. روی سرور همین ورودی را به R دادیم:

<div dir="ltr">

```text
Error: object 'DESeq2' not found
Execution halted
```

</div>

(خروجی واقعی.) R، `DESeq2` بی کوتیشن را نام یک متغیر پنداشت. همین خطا را در ویندوز با دستوری می‌گیرید که در لینوکس درست است.

**قاعده‌ی مسیر ویندوز: بیرون دوکوتیشن، درون تک‌کوتیشن.** R هر دو گونه کوتیشن را برای متن می‌پذیرد:

<div dir="ltr">

```powershell
Rscript -e "packageVersion('DESeq2')"
```

</div>

<div dir="ltr">

```text
[1] ‘1.52.0’
```

</div>

(خروجی واقعی روی سرور، با همین شکل کوتیشن.)

⚠️ **یک دام دیگر:** درون دوکوتیشن PowerShell، نشانه‌ی `$` یک متغیر PowerShell است. پس `"df$length"` خراب می‌شود. برای کد R با `$`، آن را در یک فایل `.R` بنویسید و با `Rscript file.R` اجرا کنید، یا در کنسول RStudio بزنید.

| جا | درست |
| :--- | :--- |
| لینوکس (Bash) | ‏`Rscript -e 'cat("hi\n")'` |
| ویندوز (PowerShell) | ‏`Rscript -e "cat('hi\n')"` |
| کنسول RStudio یا R | ‏`cat("hi\n")` (بی `Rscript -e` و بی کوتیشن بیرونی) |

✍️ در PowerShell 7.3 و تازه‌تر، دوکوتیشن‌های درونی درست فرستاده می‌شوند؛ ولی قاعده‌ی بالا در هر دو نسخه کار می‌کند.

---

## ۵. کتابخانه‌ها در ویندوز

بخش ۴ درس اصلی (`.libPaths()`):

<div dir="ltr">

```powershell
Rscript -e ".libPaths()"
```

</div>

✍️ انتظار در ویندوز:

<div dir="ltr">

```text
[1] "C:/Users/Sara/AppData/Local/R/win-library/4.6"
[2] "C:/Program Files/R/R-4.6.1/library"
```

</div>

یکم کتابخانه‌ی **شخصی** شماست (بسته‌هایی که نصب کردید)، دوم کتابخانه‌ی **پایه‌ی** خود R. R مسیرها را با `/` نشان می‌دهد، حتی در ویندوز. `AppData` پوشه‌ای پنهان است؛ در File Explorer از View ← Show ← **Hidden items** آن را نمایان کنید.

**نکته‌ی نسخه:** کتابخانه‌ی شخصی پوشه‌ی `4.6` دارد. اگر روزی R 4.7 نصب کنید، پوشه‌ی تازه‌ی `4.7` خالی است و باید بسته‌ها را دوباره نصب کنید (گام ۳). این همان جفت بودن نسخه‌ی R و Bioconductor در درس اصلی است.

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | پیام | چاره |
| :--- | :--- | :--- |
| ‏R به PATH افزوده نشده | ‏`Rscript : The term 'Rscript' is not recognized…` | گام ۲ |
| کوتیشن‌های لینوکسی در PowerShell 5.1 | ‏`Error: object 'DESeq2' not found` | ‏`"packageVersion('DESeq2')"` (بخش ۴) |
| ‏`$` در کد R درون دوکوتیشن PowerShell | نتیجه‌ی بی‌معنی یا `Error: unexpected …` | فایل `.R` یا RStudio |
| نصب در `C:\Program Files` | ‏`… is not writable` | کتابخانه‌ی شخصی (کادر گام ۳) |
| ‏R 4.6 و 4.7 با هم | ‏`there is no package called 'DESeq2'` در یکی از آن‌ها | ‏`Get-Command Rscript`؛ بسته‌ها را برای نسخه‌ی تازه دوباره نصب کنید |
| تلاش برای `conda install bioconductor-deseq2` در ویندوز | ‏`PackagesNotFoundError` | ‏bioconda ویندوز ندارد؛ `BiocManager::install` |

✍️ همه‌ی پیام‌های این جدول به جز سطر دوم از مستندات‌اند.

---

## ۷. جمع‌بندی

- در ویندوز: R از CRAN، بسته‌ها با `install.packages` و `BiocManager::install`؛ باینری، بی کامپایل، بی Rtools.
- ‏`$env:Path += ";C:\Program Files\R\R-4.6.1\bin"` در هر پنجره، یا PATH همیشگی.
- ‏`Rscript -e "…'…'…"`: بیرون دوکوتیشن، درون تک‌کوتیشن؛ کد با `$` در فایل یا RStudio.
- کتابخانه‌ی شخصی در `AppData\Local\R\win-library\4.6`؛ با هر نسخه‌ی تازه‌ی R، نصب دوباره.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز (PowerShell) |
| :--- | :--- |
| ‏Rscript در این پنجره | ‏`$env:Path += ";C:\Program Files\R\R-4.6.1\bin"` |
| کدام R؟ | ‏`Get-Command Rscript` |
| نسخه‌ی یک بسته | ‏`Rscript -e "packageVersion('vegan')"` |
| نصب از CRAN | ‏`Rscript -e "install.packages('vegan', repos = 'https://cloud.r-project.org')"` |
| نصب از Bioconductor | ‏`Rscript -e "BiocManager::install('DESeq2', update = FALSE, ask = FALSE)"` |
| کتابخانه‌ها | ‏`Rscript -e ".libPaths()"` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| بسته‌ی باینری (binary) | بسته‌ی آماده و کامپایل‌شده برای یک سیستم‌عامل؛ در ویندوز فایل `.zip` |
| ‏Rtools | ابزار کامپایل بسته‌های R از کد منبع در ویندوز |
| ‏PATH | فهرست پوشه‌هایی که ویندوز برنامه‌ها را در آن‌ها می‌جوید |
| کتابخانه‌ی شخصی | پوشه‌ای در `AppData` که بسته‌های نصب‌شده‌ی شما در آن است |

---

## منابع

### راهنما و درس رایگان
- ‏CRAN — *R for Windows FAQ*: https://cran.r-project.org/bin/windows/base/rw-FAQ.html
- ‏CRAN — *Rtools*: https://cran.r-project.org/bin/windows/Rtools/
- ‏Bioconductor — *Install*: https://www.bioconductor.org/install/
- ‏Microsoft Learn — *about_Parsing* (فرستادن آرگومان به برنامه‌های بیرونی): https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_parsing
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع).

### کتاب
- ‏Wickham H, Bryan J (2023). *R Packages*, 2nd ed. O'Reilly. (فصل نصب و کتابخانه‌ها؛ رایگان: https://r-pkgs.org)

### فیلم‌های آموزشی
همان فیلم‌های [درس اصلی](01_lesson.md#منابع).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. دستورهای R در 2026-11-10 روی سرور دوره اجرا شدند. نصب و رفتار ویندوز از مستندات‌اند (✍️).

</div>
