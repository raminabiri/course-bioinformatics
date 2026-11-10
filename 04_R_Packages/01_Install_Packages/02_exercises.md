<div dir="rtl">

# تمرین‌ها: نصب و وارسی بسته‌های R

پیش از آغاز:

<div dir="ltr">

```bash
conda activate r_packages
P=~/course-bioinformatics-main/04_R_Packages/99_scripts_data

> **مسیر ویندوز:** نخست [مسیر ویندوز](00_lesson_windows.md) را بخوانید. به جای دو سطر بالا، در PowerShell: `$env:Path += ";C:\Program Files\R\R-4.6.1\bin"` و `$P = "$HOME\course-bioinformatics-main\04_R_Packages\99_scripts_data"`. در `Rscript -e` **بیرون دوکوتیشن و درون تک‌کوتیشن** بنویسید. زیر راهنمایی هر تمرین یک بند **ویندوز** آمده است. پاسخ‌های ویندوزی در پایان [پاسخ‌ها](03_solutions.md) هستند.
```

</div>

---

## تمرین ۱: کدام نصب است؟
> **راهنمایی:** بخش ۴ درس، اسکریپت `check_packages.R` با نام بسته‌ها به‌عنوان ورودی.
> **ویندوز:** ‏`Rscript $P\01_Install_Packages\scripts\check_packages.R vegan edgeR ape phyloseq dada2`.

با یک دستور، وضعیت این پنج بسته را بگیرید: `vegan`، `edgeR`، `ape`، `phyloseq`، `dada2`. کدام‌ها در محیط شما نصب‌اند و نسخه‌ی `vegan` چیست؟

---

## تمرین ۲: سه دستور خراب
> **راهنمایی:** بخش ۳ (کوتیشن‌ها)، بخش ۴ (املای نام) و بخش ۵ (CRAN یا Bioconductor). نخست هر دستور را اجرا کنید و پیام خطا را بخوانید.
> **ویندوز:** در PowerShell 5.1 دستور دوم هم خراب می‌شود، چون دوکوتیشن‌های درونی دور ریخته می‌شوند ([مسیر ویندوز، بخش ۴](00_lesson_windows.md)). نسخه‌ی درست هر سه را به شکل ویندوزی بنویسید: `Rscript -e "packageVersion('vegan')"`.

هر سه دستور زیر خطا می‌دهند. علت هر کدام را بگویید و نسخه‌ی درستش را بنویسید و اجرا کنید (دستور سوم را تنها بنویسید؛ اگر DESeq2 نصب است، اجرای درستش تنها هشدار «پیش‌تر نصب است» می‌دهد).

<div dir="ltr">

```bash
Rscript -e "packageVersion("vegan")"
Rscript -e 'packageVersion("Ggplot2")'
Rscript -e 'install.packages("DESeq2", repos = "https://cran.r-project.org")'
```

</div>

---

## تمرین ۳: فروشگاه درست
> **راهنمایی:** بخش ۵، «از کجا بفهمم بسته در CRAN است یا Bioconductor؟». نام هر بسته را در مرورگر جست‌وجو کنید.
> **ویندوز:** همان؛ در مرورگر.

برای هر بسته بگویید از CRAN است یا Bioconductor، و نام آن در conda (با کانال) چیست:
`phyloseq`، `pheatmap`، `dada2`، `ape`، `edgeR`، `vegan`.

---

## تمرین ۴: خواندن گزارش نصب
> **راهنمایی:** بخش ۵، راه ۲، جدول زیر خروجی `install.packages`.
> **ویندوز:** گزارش بالا از لینوکس است (کامپایل از کد منبع). در ویندوز به جای خط‌های `*source*` تنها `successfully unpacked and MD5 sums checked` می‌بینید؛ پرسش‌ها همان‌اند.

گزارش زیر خروجی واقعی نصب بسته‌ی `permute` است. به سه پرسش پاسخ دهید: (الف) حجم فایل دانلودشده چقدر بود؟ (ب) بسته از کد منبع ساخته شد یا باینری آماده بود؟ (ج) کدام خط نشان می‌دهد نصب **موفق** بود؟

<div dir="ltr">

```text
trying URL 'https://cran.r-project.org/src/contrib/permute_0.9-10.tar.gz'
Content type 'application/x-gzip' length 120438 bytes (117 KB)
==================================================
downloaded 117 KB

* installing *source* package ‘permute’ ...
** this is package ‘permute’ version ‘0.9-10’
** package ‘permute’ successfully unpacked and MD5 sums checked
** using staged installation
** R
** data
** inst
** byte-compile and prepare package for lazy loading
** help
*** installing help indices
** building package indices
** installing vignettes
** testing if installed package can be loaded from temporary location
** testing if installed package can be loaded from final location
** testing if installed package keeps a record of temporary installation path
* DONE (permute)
```

</div>

---

## تمرین ۵: پیام‌ها یا خطا؟
> **راهنمایی:** بخش ۵، «باز کردن بسته: `library`». دنبال واژه‌ی `Error` بگردید.
> **ویندوز:** همان؛ پیام‌های بارگذاری در ویندوز همان‌اند.

این دستور را اجرا کنید:

<div dir="ltr">

```bash
Rscript -e 'library(vegan); cat("ok\n")'
```

</div>

(الف) خروجی چند خط است و آیا خطایی در آن هست؟ (ب) خط `Loading required package: permute` چه می‌گوید؟ (ج) از کجا مطمئن می‌شوید که دستور تا پایان اجرا شد؟

---

## تمرین ۶ (فکری): «نصب کردم، ولی پیدا نمی‌شود!»
> **راهنمایی:** بخش ۴ («بسته‌ها کجا نصب می‌شوند؟») و اشتباه رایج ۳.
> **ویندوز:** به جای `which Rscript`: ‏`Get-Command Rscript`؛ و `Rscript -e ".libPaths()"`. در ویندوز علت محتمل: دو نسخه‌ی R، یا پنجره‌ی تازه‌ای که PATH آن R دیگری را می‌شناسد.

همکارتان می‌گوید: «دیروز `conda install bioconductor-phyloseq` را در محیط `r_packages` زدم و نصب شد. امروز `Rscript -e 'library(phyloseq)'` می‌گوید `there is no package called ‘phyloseq’`.» دو دستوری را بنویسید که به او می‌گویید برای یافتن علت بزند، و علت محتمل را توضیح دهید.

---

## تمرین ۷ (فکری): افزودن یک بسته به فایل محیط
> **راهنمایی:** بخش ۵، راه ۱، و تجربه‌ی ggtree 1.2.12.
> **ویندوز:** فکری؛ ولی یادتان باشد bioconda ویندوز ندارد. همتای ویندوزی «فایل محیط» یک فایل `.R` با یک `install.packages(...)` و یک `BiocManager::install(...)` است (گام ۳ مسیر ویندوز).

می‌خواهید `phyloseq` (نسخه‌ی کنونی در Bioconductor: 1.5x) را به `envs/r_packages.yml` بیفزایید. خطی که می‌نویسید چیست و چرا `>=` می‌گذارید؟ پیش از ساختن واقعی محیط، با کدام گزینه‌ی conda می‌بینید چه نسخه‌ای برگزیده می‌شود؟

</div>
