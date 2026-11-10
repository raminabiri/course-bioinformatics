<div dir="rtl">

# درس (مسیر ویندوز): DESeq2، vegan و ggtree روی ویندوز

**بخش:** `04_R_Packages` · **ماژول:** `03_Bioc_Examples` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول‌های ۰۱ و ۰۲](../02_Run_Rscript/00_lesson_windows.md) (R، بسته‌ها، `$LASTEXITCODE`)؛ پایتون با pandas ([بخش ۰۳](../../03_Python/06_Pandas/00_lesson_windows.md)) · **زمان:** حدود ۴۵ دقیقه، همراه سه درس اصلی · **ابزار:** R 4.6 (DESeq2، vegan، ape، ggtree)، Python 3 (pandas)، PowerShell، Excel · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** همه‌ی اسکریپت‌های R و پایتون این ماژول و همه‌ی یک‌سطری‌های پایتون این درس روی سرور دوره **اجرا شدند** (2026-11-10؛ R 4.6.1، DESeq2 1.52.0) و خروجی‌شان واقعی است. فرمان‌های PowerShell و Excel از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

این ماژول سه درس اصلی دارد. خود اسکریپت‌ها (`run_deseq2.R`، `diversity.R`، `make_tree.R`، `plot_tree.R`، `make_counts.py`، `compare_truth.py`) در ویندوز **همان‌اند** و همان عددها را می‌دهند. فرق تنها در فرمان‌هایی است که درس‌ها برای **خواندن جدول‌های خروجی** به کار می‌برند: `awk`، `cut`، `grep`، `column`. در ویندوز آن‌ها را با **pandas** (یک سطر پایتون) یا **Excel** جایگزین می‌کنیم.

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`python3 …` / `Rscript …` | ‏`py …` / `Rscript …` (R در PATH؛ [ماژول ۰۱](../01_Install_Packages/00_lesson_windows.md)) |
| ‏`awk -F'\t' '… $7 < 0.05 …' f \| wc -l` | ‏pandas: `r[r["padj"] < 0.05]` (بخش ۲)، یا فیلتر Excel |
| ‏`cut -f1,2,3,7 f \| head -6` | ‏pandas: `r.iloc[:5, [0, 1, 2, 6]]` |
| ‏`grep -w b1609 f` | ‏`Select-String -Path f -Pattern "\bb1609\b"` |
| ‏`column -t f` / `cat f` | ‏`Import-Csv f -Delimiter "`t" \| Format-Table` / `Get-Content f` |
| ‏`2>/dev/null` | ‏`2>$null` |
| ‏`printf '…\n' > f.nwk` | ‏`Set-Content f.nwk "…"` |

---

## ۱. درس ۱ (DESeq2): گام‌ها

در PowerShell:

<div dir="ltr">

```powershell
$env:Path += ";C:\Program Files\R\R-4.6.1\bin"
mkdir $HOME\r_practice\deseq2; cd $HOME\r_practice\deseq2
$P = "$HOME\course-bioinformatics-main\04_R_Packages\99_scripts_data"
py $P\03_Bioc_Examples\scripts\make_counts.py $HOME\course\ecoli_k12.gff
Rscript $P\03_Bioc_Examples\scripts\run_deseq2.R counts.tsv samples.tsv WT deseq2
```

</div>

‏(‏`ecoli_k12.gff` را در [آماده کردن ویندوز](../../windows/README.md) در `$HOME\course` گرفته‌اید.) **خروجی واقعی** (سطرهای کلیدی؛ سرور دوره):

<div dir="ltr">

```text
wrote counts.tsv (4290 genes x 6 samples), samples.tsv, truth.tsv (100 changed genes)
…
saved deseq2_results.tsv deseq2_MA.png deseq2_PCA.png 
```

</div>

‏`run_deseq2.R` روی سرور ۴٫۶ ثانیه و **۸۸۹ مگابایت** حافظه گرفت؛ روی هر لپ‌تاپ با ۴ گیگابایت حافظه اجرا می‌شود. نمودارها: `Start-Process deseq2_MA.png`.

‏`head -4 counts.tsv` و `cat samples.tsv` ← `Get-Content counts.tsv -TotalCount 4` و `Get-Content samples.tsv`. ‏`head -7 run_deseq2.R` ← `Get-Content $P\03_Bioc_Examples\scripts\run_deseq2.R -TotalCount 7`.

---

## ۲. درس ۱: خواندن `deseq2_results.tsv` بی `awk`

درس اصلی (بخش ۵) با `awk` می‌شمارد چند ژن `padj < 0.05` دارند. ستون ۳ `log2FoldChange` و ستون ۷ `padj` است. همان سه شمارش با pandas، در یک سطر:

<div dir="ltr">

```powershell
py -c "import pandas as pd; r = pd.read_csv('deseq2_results.tsv', sep='\t'); s = r[r['padj'] < 0.05]; print(len(s), (s['log2FoldChange'] > 0).sum(), (s['log2FoldChange'] < -2).sum(), r['padj'].isna().sum())"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```text
93 47 29 2
```

</div>

| عدد | یعنی | همان دستور درس اصلی |
| :-: | :--- | :--- |
| ‏۹۳ | ژن‌های معنادار (`padj < 0.05`) | ‏`awk '… $7 < 0.05' \| wc -l` |
| ‏۴۷ | از آن‌ها، بیشتر بیان‌شده در RifR | ‏`… && $3 > 0` |
| ‏۲۹ | بیش از ۴ برابر کمتر بیان‌شده (`log2FC < -2`) | ‏`… && $3 < -2` |
| ‏۲ | ژن‌هایی که `padj` آن‌ها `NA` است | ‏`grep -P "\tNA"` |

‏`NA` نکته‌ی ظریفی است: در `awk` باید آن را جدا رد کنید (`$7 != "NA"`). pandas `NA` را «عدد نامعلوم» می‌خواند و `NA < 0.05` را خودش **نادرست** می‌شمارد. پس همان ۹۳.

**نخستین سطرها** (جای `cut -f1,2,3,7 deseq2_results.tsv | head -6`):

<div dir="ltr">

```powershell
py -c "import pandas as pd; print(pd.read_csv('deseq2_results.tsv', sep='\t').iloc[:5, [0, 1, 2, 6]])"
```

</div>

‏`iloc[:5, [0, 1, 2, 6]]` یعنی «۵ سطر نخست، ستون‌های ۱، ۲، ۳ و ۷» (pandas از ۰ می‌شمارد).

**راه Excel:** `deseq2_results.tsv` را با Data ← From Text/CSV (جداکننده Tab) باز کنید، Home ← **Sort & Filter ← Filter**، و روی ستون `padj` ← Number Filters ← **Less Than** ← `0.05`. شمار سطرها در پایین پنجره می‌آید (۹۳). ✍️ Excel عددهای علمی مانند `3.9e-29` را درست می‌خواند. `NA` را متن می‌بیند و در فیلتر عددی کنار می‌گذارد.

**یک ژن** (جای `grep -w b1609 counts.tsv`):

<div dir="ltr">

```powershell
Select-String -Path counts.tsv -Pattern "\bb1609\b"
```

</div>

‏`\b` «مرز واژه» است؛ همان `-w` در `grep`: `b16090` جور نمی‌شود.

**سنجیدن با پاسخ معلوم** (بخش ۷ درس اصلی) همان است:

<div dir="ltr">

```powershell
py $P\03_Bioc_Examples\scripts\compare_truth.py deseq2_results.tsv truth.tsv
Import-Csv missed.tsv -Delimiter "`t" | Select-Object -First 7 | Format-Table
```

</div>

‏`Import-Csv … | Format-Table` جای `column -t` است: جدول را با ستون‌های هم‌تراز نشان می‌دهد. ‏`` "`t" `` در PowerShell یعنی Tab (نویسه‌ی ویژه‌ی PowerShell بک‌تیک است، نه `\`).

**گروه مرجع وارونه** (بخش «اشتباه» درس اصلی): به جای `2>/dev/null | grep -A2 "adjusted"`:

<div dir="ltr">

```powershell
Rscript $P\03_Bioc_Examples\scripts\run_deseq2.R counts.tsv samples.tsv RifR flipped 2>$null | Select-String -Pattern "adjusted" -Context 0,2
```

</div>

‏`2>$null` پیام‌ها را دور می‌ریزد (همان `2>/dev/null`) و `-Context 0,2` دو سطر پس از هر سطر جور را هم نشان می‌دهد (همان `-A2`).

---

## ۳. درس ۲ (vegan)

<div dir="ltr">

```powershell
mkdir $HOME\r_practice\vegan; cd $HOME\r_practice\vegan
Copy-Item $HOME\course-bioinformatics-main\01_Linux\99_scripts_data\data\ground_truth.tsv .
Rscript $P\03_Bioc_Examples\scripts\diversity.R ground_truth.tsv diversity
Import-Csv diversity_alpha.tsv -Delimiter "`t" | Format-Table
Get-Content diversity_bray.tsv
```

</div>

**خروجی واقعی** جدول تنوع آلفا (از pandas روی سرور؛ `Format-Table` همین ستون‌ها را نشان می‌دهد):

<div dir="ltr">

```text
            sample  reads  richness  shannon  simpson  evenness
0          minigut  50000         2    0.681    0.488     0.982
1  minigut_sample2  24993        21    1.608    0.572     0.528
```

</div>

همان عددهای درس اصلی. هشدار `most observed count data have counts 1, but smallest count is 24` هم همان است (درس اصلی می‌گوید چرا بی‌خطر است).

‏`grep -i "escherichia" ground_truth.tsv | cut -f1,4` ← ‏`Select-String -Path ground_truth.tsv -Pattern "escherichia"` (‏`Select-String` به‌طور پیش‌فرض بزرگی و کوچکی حرف را نادیده می‌گیرد، همان `-i`). در سطح جنس: `Rscript $P\03_Bioc_Examples\scripts\diversity.R ground_truth.tsv diversity_genus genus 2>$null`.

---

## ۴. درس ۳ (ggtree)

<div dir="ltr">

```powershell
mkdir $HOME\r_practice\tree; cd $HOME\r_practice\tree
Rscript $P\03_Bioc_Examples\scripts\make_tree.R woodmouse.nwk
Get-Content woodmouse.nwk
Rscript $P\03_Bioc_Examples\scripts\plot_tree.R woodmouse.nwk woodmouse_tree.png
Start-Process woodmouse_tree.png
```

</div>

**خروجی واقعی:** `alignment: 15 sequences x 965 bp`، `saved woodmouse.nwk` و `saved woodmouse_tree.png`؛ همان درس اصلی.

‏**Newick خراب** (جای `printf '((A:1,B:1):1,C:2\n' > broken.nwk`):

<div dir="ltr">

```powershell
Set-Content broken.nwk "((A:1,B:1):1,C:2"
Rscript $P\03_Bioc_Examples\scripts\plot_tree.R broken.nwk b.png
```

</div>

<div dir="ltr">

```text
  argument "X" is missing, with no default
Calls: xlim ... <Anonymous> -> reorder -> reorder.default -> tapply
Execution halted
```

</div>

(خروجی واقعی روی سرور، هم با پایان سطر لینوکسی و هم با `\r\n` ویندوزی که `Set-Content` می‌نویسد: پیام یکی است.) ‏`Set-Content` خودش پایان سطر را می‌افزاید؛ `\n` لازم نیست.

---

## ۵. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| ‏`awk`، `cut`، `column` | ‏`… is not recognized as the name of a cmdlet` | ‏pandas یا Excel (بخش ۲) |
| ‏`"\t"` در PowerShell | جداکننده‌ی نادرست؛ همه در یک ستون | در PowerShell ``"`t"``؛ درون کد پایتون `'\t'` |
| ‏`2>/dev/null` | ‏`Could not find a part of the path '…\dev\null'` | ‏`2>$null` |
| باز کردن `deseq2_results.tsv` با دوبار کلیک | همه در یک ستون Excel | ‏Data ← From Text/CSV |
| گزینش دستی سطرها در Excel (با چشم) | ژن‌های `NA` هم شمرده می‌شوند | فیلتر عددی **Less Than**؛ `NA` خودش بیرون می‌ماند |

✍️ پیام‌های این جدول از مستندات‌اند.

---

## ۶. جمع‌بندی

- اسکریپت‌های R و پایتون ماژول در ویندوز همان عددها را می‌دهند (۹۳ / ۴۷ / ۲۹ ژن؛ شانون ۰٫۶۸۱ و ۱٫۶۰۸؛ درخت ۱۵ برگی).
- گزینش و شمارش جدول‌ها: یک سطر pandas یا فیلتر Excel، به جای `awk`.
- ‏`Select-String` (با `\b` برای واژه‌ی کامل و `-Context` برای سطرهای پس از آن)، `Import-Csv … | Format-Table`، ‏`2>$null`، ‏`Set-Content`.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| شمار سطرهای معنادار | ‏`py -c "import pandas as pd; r = pd.read_csv('f.tsv', sep='\t'); print((r['padj'] < 0.05).sum())"` |
| چند ستون از چند سطر نخست | ‏`py -c "import pandas as pd; print(pd.read_csv('f.tsv', sep='\t').iloc[:5, [0, 2, 6]])"` |
| جدول هم‌تراز | ‏``Import-Csv f.tsv -Delimiter "`t" \| Format-Table`` |
| واژه‌ی کامل | ‏`Select-String -Path f -Pattern "\bb1609\b"` |
| سطر جور و دو سطر پس از آن | ‏`… \| Select-String -Pattern "x" -Context 0,2` |
| دور ریختن پیام‌ها | ‏`2>$null` |
| نوشتن یک سطر در فایل | ‏`Set-Content f.nwk "…"` |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏`Import-Csv` | خواندن جدول CSV/TSV در PowerShell؛ هر سطر یک شیء با نام ستون‌ها |
| ‏`Format-Table` | نمایش هم‌تراز یک جدول در PowerShell |
| ‏`iloc` | گزینش سطر و ستون با **شماره** در pandas |
| ‏`$null` | «هیچ» در PowerShell؛ همانند `/dev/null` |

---

## منابع

### راهنما و درس رایگان
- ‏Microsoft Learn — *Import-Csv*: https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/import-csv
- ‏Microsoft Learn — *Select-String* (‏`-Context`): https://learn.microsoft.com/powershell/module/microsoft.powershell.utility/select-string
- ‏pandas — *Indexing and selecting data*: https://pandas.pydata.org/docs/user_guide/indexing.html
- ‏Bioconductor — *DESeq2* (نصب روی ویندوز با BiocManager): https://bioconductor.org/packages/DESeq2/
- همه‌ی منابع سه درس اصلی.

### کتاب
- ‏McKinney W (2022). *Python for Data Analysis*, 3rd ed. O'Reilly. (گزینش داده با pandas؛ رایگان: https://wesmckinney.com/book/)

### فیلم‌های آموزشی
همان فیلم‌های سه درس اصلی.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. اسکریپت‌ها و یک‌سطری‌های پایتون در 2026-11-10 روی سرور دوره اجرا شدند. فرمان‌های PowerShell و Excel از مستندات‌اند (✍️).

</div>
