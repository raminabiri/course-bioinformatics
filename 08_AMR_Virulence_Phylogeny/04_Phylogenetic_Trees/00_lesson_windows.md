<div dir="rtl">

# درس (مسیر ویندوز): درخت‌های فیلوژنتیک روی ویندوز

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `04_Phylogenetic_Trees` · **مسیر:** ویندوز خالص · **پیش‌نیاز:** [آماده کردن ویندوز](../../windows/README.md)؛ مفهوم‌ها از درس‌های [۱](01_lesson_msa_nj.md)، [۲](02_lesson_ml_iqtree.md) و [۳](03_lesson_outbreak_tree.md) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** MAFFT 7.526، R 4.6.1 (ape 5.8.1، ggtree 4.2.0)، IQ-TREE 3.1.3، Python 3 · **آخرین بازبینی:** 2026-11-09

> ✍️ **وضعیت:** خروجی‌ها واقعی‌اند: همین برنامه‌ها روی سرور دوره اجرا شدند (2026-11-09). هر سه برنامه نسخه‌ی ویندوزی دارند. نصب و دستورهای PowerShell از مستندات‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏MAFFT و IQ-TREE با conda | نسخه‌ی ویندوزی هر دو (گام ۰) |
| ‏`mafft --auto in > out` | ‏`--out` به جای `>` (گام ۱) |
| ‏`Rscript -e '…'` | همان کد R در کنسول **RStudio** |
| ‏IQ-TREE (درس ۲، تنها از مستندات) | ‏IQ-TREE **اجرا شده** (گام‌های ۳ و ۶) |
| ‏Gubbins | نسخه‌ی ویندوزی ندارد |

**در پایان می‌توانید:** با MAFFT هم‌ردیفی بسازید؛ درخت NJ و ML بسازید و بسنجید؛ درخت را درست ریشه‌دار کنید؛ درخت شیوع را بسازید.

---

## ۱. گام ۰: نصب و پوشه (✍️)

1. ‏**MAFFT:** نسخه‌ی Windows را از https://mafft.cbrc.jp/alignment/software/windows.html بگیرید و در `$HOME\tools` باز کنید. فایل اجرایی `mafft.bat` است.
2. ‏**IQ-TREE:** نسخه‌ی Windows را از https://iqtree.github.io بگیرید و در `$HOME\tools` باز کنید. فایل اجرایی `bin\iqtree3.exe` است.
3. ‏**R و RStudio:** [آماده کردن ویندوز](../../windows/README.md). سپس در کنسول RStudio یک بار:

<div dir="ltr">

```r
install.packages(c("ape", "ggplot2", "BiocManager"))
BiocManager::install("ggtree")
```

</div>

در PowerShell مسیر هر برنامه را در یک متغیر بگذارید. **مسیرها را با پوشه‌ای که خودتان باز کرده‌اید جور کنید** (نام پوشه‌ها شماره‌ی نسخه دارند):

<div dir="ltr">

```powershell
mkdir $HOME\phylo; cd $HOME\phylo
$S = "$HOME\course-bioinformatics-main\08_AMR_Virulence_Phylogeny\99_scripts_data"
$MAFFT = "$HOME\tools\mafft-win\mafft.bat"
$IQ = "$HOME\tools\iqtree-3.1.3-Windows\bin\iqtree3.exe"
$R = "C:\Program Files\R\R-4.6.1\bin\Rscript.exe"
copy $S\data\ctxm_alleles.fna .
```

</div>

‏`& $IQ …` برنامه‌ای را اجرا می‌کند که مسیرش در متغیر است.

در RStudio هم پوشه‌ی کار را بگذارید. **‏`~` در R ویندوزی پوشه‌ی Documents است**، پس:

<div dir="ltr">

```r
setwd(file.path(Sys.getenv("USERPROFILE"), "phylo"))
```

</div>

---

## ۲. گام ۱: هم‌ردیفی با MAFFT

<div dir="ltr">

```powershell
& $MAFFT --auto --out ctxm_aln.fna ctxm_alleles.fna
Get-FileHash -Algorithm MD5 ctxm_aln.fna
```

</div>

‏`--out` فایل را خود MAFFT می‌نویسد. با `>` در PowerShell 5.1 فایل UTF-16 می‌شود (ماژول‌های پیشین). روی سرور، `--out` و `>` همان فایل را دادند.

**خروجی واقعی** (MAFFT 7.526):

<div dir="ltr">

```
Strategy:
 L-INS-i (Probably most accurate, very slow)
4d9cacc6b63a90e5c344338cc1718130  ctxm_aln.fna
```

</div>

همان روش و همان هم‌ردیفی ۸۷۸ ستونی درس ۱، بخش ۳. ‏`Get-FileHash` همین عدد را با حروف بزرگ نشان می‌دهد.

---

## ۳. گام ۲: درخت NJ

<div dir="ltr">

```powershell
& $R $S\04_Phylogenetic_Trees\scripts\nj_tree.R ctxm_aln.fna TEM-1 ctxm_nj
Get-Content ctxm_nj.nwk
```

</div>

**خروجی واقعی** (۰٫۲ ثانیه، ۹۸ مگابایت):

<div dir="ltr">

```
sequences: 15  alignment length: 878 
model: TN93  bootstrap replicates: 100 
written: ctxm_nj.nwk ctxm_nj.png 
```

</div>

درخت Newick **تا آخرین رقم** همان درخت درس ۱، بخش ۵ است (پنج گروه CTX-M، KLUC-1 کنار گروه ۱، گره‌های ژرف ۳۴ و ۴۷). ‏`ctxm_nj.png` را باز کنید.

یک‌سطری‌های `Rscript -e` درس ۱ (ماتریس فاصله) را در کنسول RStudio بزنید، بی `Rscript -e` و گیومه‌های بیرونی.

---

## ۴. گام ۳: درخت ML با IQ-TREE

مفهوم‌ها در درس ۲، بخش ۲. این‌جا همان دستور درس ۲ را اجرا می‌کنیم؛ `--seed` نتیجه را تکرارپذیر می‌کند:

<div dir="ltr">

```powershell
& $IQ -s ctxm_aln.fna -m MFP -B 1000 -alrt 1000 -T 2 --seed 2026 --prefix ctxm_ml
Select-String -Path ctxm_ml.iqtree -Pattern "Best-fit model"
```

</div>

**خروجی واقعی** (IQ-TREE 3.1.3؛ ‏۳٫۴ ثانیه، ۲۵ مگابایت):

<div dir="ltr">

```
Best-fit model according to BIC: TN+F+G4
```

</div>

- ‏`TN+F+G4`: همان TN93 درس ۱، با فراوانی بازها از داده و سرعت ناهمسان جایگاه‌ها.
- برچسب گره‌ها در `ctxm_ml.treefile` به شکل `SH-aLRT/UFBoot` است (مانند `100/97`). آستانه‌ها: ۸۰ و ۹۵ (درس ۲، بخش ۲.۳).
- درخت IQ-TREE **بی‌ریشه** است؛ گام بعد.

---

## ۵. گام ۴: ریشه‌دار کردن درست، و NJ در برابر ML

در کنسول RStudio:

<div dir="ltr">

```r
library(ape)
ml <- root(read.tree("ctxm_ml.treefile"), "TEM-1", resolve.root = TRUE, edgelabel = TRUE)
write.tree(ml, "ctxm_ml_rooted.nwk")
plot(ml, show.node.label = TRUE, cex = 0.8)
dist.topo(unroot(ml), unroot(read.tree("ctxm_nj.nwk")))
```

</div>

**خروجی واقعی:** فاصله‌ی Robinson-Foulds = **4**.

‏**‏`edgelabel = TRUE` مهم است.** پشتیبانی مال یک شاخه است، ولی ape آن را روی گره نگه می‌دارد. با ریشه‌ی تازه، بی این گزینه برچسب‌ها روی گره‌های دیگر می‌نشینند. روی سرور ما، بی آن، گره‌ای با پشتیبانی واقعی `6.4/42`، ‏`100/91` نشان داده شد، **بی هیچ هشداری**.

| گروه | ‏NJ (bootstrap) | ‏ML (SH-aLRT/UFBoot) |
| :--- | :---: | :---: |
| گروه ۱ | 100 | 99.9/100 |
| گروه ۱ + KLUC-1 | 78 | 100/91 |
| گروه‌های ۲، ۹، ۸ | 100، 100، 100 | 100/93، 100/97، 100/99 |
| گروه ۸ + ۲۵ | 99 | 100/97 |
| گره ژرف ۱ | گروه ۲ + ۹: 34 | گروه ۲ + (۱ + KLUC-1): 6.4/42 |
| گره ژرف ۲ | (۲ + ۹) + (۸ + ۲۵): 47 | گروه ۹ + (۸ + ۲۵): 30.5/61 |

**توضیح:**
- گروه‌های اصلی در هر دو روش هستند.
- گره‌های ژرف در دو روش **فرق دارند** (همین، RF ‏۴ است)، ولی هر دو روش به آن‌ها پشتیبانی **پایین** داده‌اند. پس تناقض نیست: داده ترتیب جدا شدن گروه‌ها را نمی‌گوید (همان پیام درس ۱).
- شاخه‌ی TEM-1 در ML ‏۴٫۲۱ است و در NJ ‏۰٫۸۴. برای توالی‌های بسیار دور، طول شاخه بسیار به مدل وابسته است (`+G4` جهش‌های پنهان بیشتری برآورد می‌کند).

**دیدن درخت (✍️، اختیاری):** `ctxm_ml_rooted.nwk` را در iTOL (https://itol.embl.de) بارگذاری کنید. نرم‌افزار ویندوزی **MEGA** (https://www.megasoftware.net) هم NJ و bootstrap را با پنجره و دکمه می‌سازد.

> 📺 **فیلم:** *IQ-TREE Tutorial*: https://www.youtube.com/watch?v=It72loV3Fs8
> 📄 **مرجع:** Minh BQ, et al. (2020). *IQ-TREE 2.* Mol Biol Evol 37:1530–1534. https://doi.org/10.1093/molbev/msaa015

---

## ۶. گام ۵: درخت شیوع

مفهوم‌ها و داستان در درس ۳ است: ‏۲۰ ایزوله از سه بیمارستان، روی یک درخت **دانسته** شبیه‌سازی شده‌اند. سه پرسش داریم: آیا سویه‌ای میان H1 و H2 جابه‌جا شده؟ آیا در H3 شیوع محلی هست؟ ‏`blaKPC` در H2-05 از کجا آمده؟

### ۶.۱ ساختن داده

<div dir="ltr">

```powershell
py $S\04_Phylogenetic_Trees\scripts\simulate_outbreak.py outbreak
Get-FileHash -Algorithm MD5 outbreak\*
```

</div>

**خروجی واقعی** (روی سرور؛ MD5ها با `md5sum`. ‏`Get-FileHash` همین عددها را در جدولی با حروف بزرگ نشان می‌دهد):

<div dir="ltr">

```
isolates: 21  alignment length: 100000  SNP sites used: 8890
Done: outbreak
10e3624419efe4a40a271a557a8404b9  outbreak/core_full.aln
0e19ef0652f9d6ae0e101e738a24cb4a  outbreak/metadata.tsv
11134bb9a43ab06be7d59b1fbef26706  outbreak/true_tree.nwk
```

</div>

اسکریپت فایل‌ها را با پایان سطر لینوکسی (LF) می‌نویسد. پس روی ویندوز هم همین سه MD5 را می‌گیرید. اگر MD5 فرق داشت، پیش از ادامه پوشه‌ی دوره را تازه کنید.

### ۶.۲ درخت NJ روی SNPها

<div dir="ltr">

```powershell
& $R $S\04_Phylogenetic_Trees\scripts\outbreak_tree.R outbreak\core_full.aln outbreak\metadata.tsv Ref outbreak_nj
```

</div>

**خروجی واقعی** (۱٫۴ ثانیه، ۲۳۷ مگابایت؛ پیش از آن چند سطر هشدار ggtree درباره‌ی `size`/`linewidth` می‌آید که بی‌اثر است):

<div dir="ltr">

```
isolates: 21  alignment length: 100000  SNP sites: 8890 
written: outbreak_nj_snps.fasta outbreak_nj_snp_dist.tsv outbreak_nj.nwk outbreak_nj.png 
```

</div>

‏`outbreak_nj.png` را باز کنید. همان تصویر درس ۳، بخش ۴ است: خوشه‌ی شش‌تایی **STa** (H1 و H2، همه `blaKPC`)، خوشه‌ی پنج‌تایی **STb** (همه H3، همه `iuc`)، و ۹ ایزوله‌ی پراکنده با شاخه‌های بلند. ‏H2-05 هم `blaKPC` دارد، ولی بیرون از STa است.

### ۶.۳ فاصله‌ها و سنجش با درخت درست

باقی کار در کنسول RStudio است (پوشه‌ی کار را در گام ۰ گذاشتیم). این همان سه یک‌سطری درس ۳، بخش‌های ۵ و ۶ است، سطر به سطر:

<div dir="ltr">

```r
library(ape)
d <- as.matrix(read.delim("outbreak_nj_snp_dist.tsv", row.names = 1, check.names = FALSE))
A <- c("H1-01", "H1-02", "H1-03", "H2-01", "H2-02", "H2-03")
d[A, A]
min(d["H1-01", !colnames(d) %in% A])
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
      H1-01 H1-02 H1-03 H2-01 H2-02 H2-03
H1-01     0     3     3     5     4     6
H1-02     3     0     4     6     5     7
H1-03     3     4     0     4     3     5
H2-01     5     6     4     0     1     3
H2-02     4     5     3     1     0     2
H2-03     6     7     5     3     2     0
[1] 852
```

</div>

همه‌ی جفت‌های STa **۷ SNP یا کمتر** فاصله دارند، از جمله جفت‌های میان دو بیمارستان (H1-03 و H2-02: ‏۳ SNP). نزدیک‌ترین ایزوله‌ی بیرون از STa، ‏۸۵۲ SNP دور است.

جفت‌های نزدیک (≤ ۱۰ SNP) بر پایه‌ی بیمارستان:

<div dir="ltr">

```r
i <- which(d <= 10 & upper.tri(d), arr.ind = TRUE)
table(substr(rownames(d)[i[, 1]], 1, 2), substr(colnames(d)[i[, 2]], 1, 2))
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
    
     H1 H2 H3
  H1  3  9  0
  H2  0  3  0
  H3  0  0 10
```

</div>

**۹ جفت نزدیک میان H1 و H2**؛ هیچ جفت نزدیکی میان H3 و دیگران نیست.

حالا درخت ساخته‌شده را با درخت درست می‌سنجیم:

<div dir="ltr">

```r
t  <- read.tree("outbreak_nj.nwk")
tt <- read.tree("outbreak/true_tree.nwk")
B  <- paste0("H3-0", 1:5)
H2 <- c("H2-01", "H2-02", "H2-03")
sapply(list(STa = A, STb = B, H2 = H2),
       function(x) c(built = is.monophyletic(t, x), true = is.monophyletic(tt, x)))
cat("Robinson-Foulds:", dist.topo(unroot(t), unroot(tt)), "\n")
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
       STa  STb   H2
built TRUE TRUE TRUE
true  TRUE TRUE TRUE
Robinson-Foulds: 4 
```

</div>

**توضیح:**
- هر سه گروه (STa، STb، زیرگروه H2) در هر دو درخت هستند. زیرگروه H2 با پشتیبانی **۸۷** درون تنوع H1 نشسته است، و ایزوله‌های H1 زودترند (ماه ۲ تا ۴ در برابر ۵ تا ۶). این با **انتقال از H1 به H2** همخوان است.
- ‏RF ‏۴ از چندشاخگی‌های درخت درست است که NJ دلبخواه حل می‌کند؛ پشتیبانی همان گره‌ها پایین است (۱۹، ۳۰، ۳۶، ۴۰). توضیح کامل در درس ۳، بخش ۶.
- ‏H2-05 تا H1-01 ‏۱۵۱۲ SNP فاصله دارد (`d["H1-01", "H2-05"]`): سویه‌ی دیگر، پس `blaKPC` آن به احتمال زیاد از راه **پلاسمید** آمده است.

پاسخ کامل سه پرسش: جدول درس ۳، بخش ۷.

> 📺 **فیلم:** دوره‌ی DTU در Coursera (کاربرد WGS در پایش و شیوع): https://www.coursera.org/learn/wgs-bacteria
> 📄 **مرجع:** Yu G, et al. (2017). *ggtree: an R package for visualization and annotation of phylogenetic trees with their covariates and other associated data.* Methods Ecol Evol 8:28–36. https://doi.org/10.1111/2041-210X.12628

---

## ۷. گام ۶: ‏IQ-TREE روی داده‌ی شیوع

درس ۳ درخت شیوع را با NJ ساخت. این‌جا همان داده را به IQ-TREE می‌دهیم و دو پرسش داریم: آیا ML همان گروه‌ها را می‌دهد؟ و طول شاخه‌ها را چگونه به **شمار SNP** برگردانیم؟

### ‏۷.۱ ‏ML روی هم‌ردیفی کامل

<div dir="ltr">

```powershell
& $IQ -s outbreak\core_full.aln -m MFP -B 1000 -alrt 1000 -T 2 --seed 2026 --prefix outbreak_ml
Select-String -Path outbreak_ml.iqtree -Pattern "Best-fit model", "Total tree length", "near-zero"
```

</div>

**خروجی واقعی** (IQ-TREE 3.1.3؛ ‏۲٫۷ ثانیه، ۳۰ مگابایت؛ تنها متن سطرها):

<div dir="ltr">

```
Best-fit model according to BIC: JC
Total tree length (sum of branch lengths): 0.0894
WARNING: 4 near-zero internal branches (<0.0000) should be treated with caution
```

</div>

- **ساده‌ترین مدل (JC) برنده شد.** درست است: شبیه‌سازی هر باز را با شانس برابر به باز دیگر تبدیل کرده است. در داده‌ی واقعی مدل پیچیده‌تری برنده می‌شود.
- **۴ شاخه‌ی نزدیک به صفر:** همان چندشاخگی‌های درخت درست (درس ۳، بخش ۶). IQ-TREE خودش هشدار می‌دهد که این گره‌ها را جدی نگیرید.
- طول درخت **۰٫۰۸۹۴ جانشینی در هر جایگاه** است، نه شمار SNP. گام بعد آن را برمی‌گرداند.

### ۷.۲ ریشه، طول شاخه به SNP، و سنجش با درخت درست

در کنسول RStudio. طول شاخه × ۱۰۰٬۰۰۰ (طول هم‌ردیفی) = شمار SNP:

<div dir="ltr">

```r
library(ape)
ml <- root(read.tree("outbreak_ml.treefile"), "Ref", resolve.root = TRUE, edgelabel = TRUE)
ml$edge.length <- ml$edge.length * 100000
write.tree(ml, "outbreak_ml_rooted.nwk")
tt <- read.tree("outbreak/true_tree.nwk")
A  <- c("H1-01", "H1-02", "H1-03", "H2-01", "H2-02", "H2-03")
B  <- paste0("H3-0", 1:5)
H2 <- c("H2-01", "H2-02", "H2-03")
stem <- function(tr, x) tr$edge.length[tr$edge[, 2] == getMRCA(tr, x)]
lab  <- function(tr, x) tr$node.label[getMRCA(tr, x) - Ntip(tr)]
sapply(list(STa = A, STb = B, H2 = H2), function(x)
  c(mono = is.monophyletic(ml, x), support = lab(ml, x), stem_SNP = round(stem(ml, x), 1), true = stem(tt, x)))
cat("tree length (SNPs):", round(sum(ml$edge.length), 1), " true:", sum(tt$edge.length), "\n")
cat("Robinson-Foulds vs true:", dist.topo(unroot(ml), unroot(tt)), "\n")
```

</div>

‏`stem` طول شاخه‌ای را می‌دهد که به نیای مشترک گروه می‌رسد؛ `lab` برچسب پشتیبانی همان گره را.

**خروجی واقعی:**

<div dir="ltr">

```
         STa       STb       H2       
mono     "TRUE"    "TRUE"    "TRUE"   
support  "100/100" "100/100" "89.3/92"
stem_SNP "352.3"   "421.3"   "2"      
true     "350"     "420"     "2"      
tree length (SNPs): 8942.2  true: 8890 
Robinson-Foulds vs true: 4 
```

</div>

**توضیح:**
- هر سه گروه در درخت ML هستند. زیرگروه H2 (درون تنوع H1) پشتیبانی `89.3/92` دارد: بالای ۸۰، ولی زیر ۹۵ برای UFBoot. ‏NJ برای همین گره ۸۷ داده بود. پس هر دو روش «انتقال از H1 به H2» را با پشتیبانی **خوب ولی نه قطعی** نشان می‌دهند.
- طول‌ها **کمی بیشتر** از درست‌اند (۳۵۲٫۳ در برابر ۳۵۰؛ کل درخت ۰٫۶٪ بیشتر). ‏JC فرض می‌کند برخی جایگاه‌ها دو بار جهش گرفته‌اند و آن‌ها را می‌افزاید. شبیه‌سازی ما هر SNP را در جایگاهی تازه گذاشته است، پس این افزوده این‌جا لازم نبود. در شیوع (چند SNP میان ایزوله‌ها) این فرق ناچیز است.
- ‏RF ‏۴: همان عدد NJ و از همان چندشاخگی‌ها.

### ۷.۳ دام: تنها SNPها به IQ-TREE

چرا ۱۰۰ هزار باز را دادیم و نه `outbreak_nj_snps.fasta` (تنها ۸۸۹۰ ستون متغیر)؟ بیازمایید:

<div dir="ltr">

```powershell
& $IQ -s outbreak_nj_snps.fasta -m JC -T 2 --seed 2026 --prefix outbreak_snp_jc
& $IQ -s outbreak_nj_snps.fasta -m MFP+ASC -T 2 --seed 2026 --prefix outbreak_asc
```

</div>

همان کد بخش ۷.۲ را برای هر `.treefile` بزنید، ولی این بار طول‌ها را × ۸۸۹۰ کنید (طول این هم‌ردیفی). **نتیجه‌ی واقعی** برای شاخه‌ی STa (درست: ۳۵۰):

| ورودی | مدل | شاخه‌ی STa (SNP) |
| :--- | :--- | :---: |
| هم‌ردیفی کامل | ‏JC (بخش ۷.۱) | 352.3 |
| تنها SNPها | ‏JC، بی تصحیح | 382.4 |
| تنها SNPها | ‏`MFP+ASC` → `F81+ASC+R2` | 0.4 |

- **بی تصحیح:** IQ-TREE نمی‌داند جایگاه‌های ثابت را برداشته‌ایم. همه‌ی ستون‌ها متغیرند، پس واگرایی را بیش از اندازه می‌بیند و جهش‌های پنهان می‌افزاید: ۹٪ بیشتر.
- **با `+ASC`** (تصحیح سوگیری گزینش؛ Lewis 2001): مدل می‌داند تنها جایگاه‌های متغیر را می‌بیند. ولی این‌جا مقیاس طول‌ها **فروریخت** (طول کل درخت ۰٫۰۰۱۱) و ۱۸ شاخه‌ی نزدیک به صفر هشدار داده شد. گروه‌بندی همان است، ولی عدد SNP بی‌معناست.
- **پیام:** برای شمار SNP، یا هم‌ردیفی کامل بدهید، یا تنها SNPها همراه با **شمار جایگاه‌های ثابت** هر باز (گزینه‌ی `-fconst`). شمارها را در RStudio بگیرید:

<div dir="ltr">

```r
a <- read.dna("outbreak/core_full.aln", format = "fasta")
table(as.character(a[1, -seg.sites(a)]))
```

</div>

<div dir="ltr">

```
    a     c     g     t 
22896 22692 22752 22770 
```

</div>

<div dir="ltr">

```powershell
& $IQ -s outbreak_nj_snps.fasta -fconst 22896,22692,22752,22770 -m MFP -B 1000 -alrt 1000 -T 2 --seed 2026 --prefix outbreak_fconst
```

</div>

**نتیجه‌ی واقعی:** مدل JC، شاخه‌ی STa **۳۵۲٫۳** (× ۱۰۰٬۰۰۰)، زیرگروه H2 `89.6/92`: همان درخت هم‌ردیفی کامل. فاصله‌ی دقیق SNP میان دو ایزوله را هم از ماتریس گام ۵ بخوانید، نه از درخت.

> 📺 **فیلم:** *Creating an Visualizing a phylogenetic tree in Galaxy and Microreact*: https://www.youtube.com/watch?v=jQVNsyAnDMo
> 📄 **مرجع:** Lewis PO (2001). *A likelihood approach to estimating phylogeny from discrete morphological character data.* Syst Biol 50:913–925. https://doi.org/10.1080/106351501753462876 · Minh BQ, et al. (2020). *IQ-TREE 2.* Mol Biol Evol 37:1530–1534. https://doi.org/10.1093/molbev/msaa015

---

## ۸. سه اشتباه رایج (مسیر ویندوز)

1. **‏`>` در PowerShell.** در Windows PowerShell 5.1 فایل UTF-16 می‌سازد و R و IQ-TREE آن را بد می‌خوانند. برای MAFFT از `--out` بهره ببرید (گام ۱).
2. **ریشه‌دار کردن بی `edgelabel = TRUE`.** پشتیبانی‌ها روی گره‌های دیگر می‌نشینند، **بی هیچ هشداری** (گام ۴: گره‌ای با `6.4/42`، ‏`100/91` نشان داده شد). هر جا `root()` روی درختی با پشتیبانی می‌زنید، این گزینه را بگذارید.
3. ‏**‏SNPها بی جایگاه‌های ثابت به IQ-TREE.** شکل درخت درست می‌ماند، ولی طول شاخه‌ها به SNP نادرست است: ۹٪ بیشتر بی تصحیح، و با `+ASC` مقیاس فرو می‌ریزد (گام ۶). هم‌ردیفی کامل یا `-fconst` بدهید.

---

## جمع‌بندی

| یافته | ویندوز (این درس) | لینوکس (درس‌های ۱ تا ۳) |
| :--- | :--- | :--- |
| هم‌ردیفی CTX-M | ‏MAFFT ویندوزی، `--out`؛ ‏۸۷۸ ستون، MD5 ‏`4d9cacc6…` | همان (`mafft … >`) |
| درخت NJ | ‏`nj_tree.R` با Rscript؛ تا آخرین رقم همان | همان |
| درخت ML CTX-M | ‏`TN+F+G4`؛ گره‌های ژرف `6.4/42` و `30.5/61`؛ RF با NJ ‏= ۴ | از مستندات (درس ۲) |
| داده‌ی شیوع | ‏`py simulate_outbreak.py`؛ همان سه MD5 | همان (`python3`) |
| درخت شیوع NJ | ‏STa ≤ ۷ SNP، ‏۹ جفت نزدیک H1–H2، زیرگروه H2 ‏۸۷، RF ‏۴ | همان |
| درخت شیوع ML | ‏JC؛ STa ‏۳۵۲٫۳ (درست ۳۵۰)، H2 ‏`89.3/92` | درس ۲، بخش ۴ |
| ‏SNP-تنها | بی تصحیح ۳۸۲٫۴؛ `+ASC` ‏۰٫۴؛ `-fconst` ‏۳۵۲٫۳ | همان (درس ۲، بخش ۴) |
| بازترکیبی (Gubbins) | نسخه‌ی ویندوزی ندارد | از مستندات (درس ۲) |

**پیام اصلی:** NJ و ML گروه‌های اصلی را یکسان می‌دهند؛ هر جا با هم فرق دارند، هر دو پشتیبانی پایین داده‌اند. برای شیوع، فاصله‌ی SNP را از ماتریس بخوانید، و پشتیبانی را با طول شاخه اشتباه نگیرید.

اکنون اگر خواستید، درس‌های [۱](01_lesson_msa_nj.md)، [۲](02_lesson_ml_iqtree.md) و [۳](03_lesson_outbreak_tree.md) را بخوانید: همان نتیجه‌ها با bash و conda.

---

## منابع

- ‏Katoh K, Standley DM (2013). *MAFFT multiple sequence alignment software version 7.* Mol Biol Evol 30:772–780. https://doi.org/10.1093/molbev/mst010
- ‏Paradis E, Schliep K (2019). *ape 5.0.* Bioinformatics 35:526–528. https://doi.org/10.1093/bioinformatics/bty633
- ‏Minh BQ, et al. (2020). *IQ-TREE 2.* Mol Biol Evol 37:1530–1534. https://doi.org/10.1093/molbev/msaa015
- ‏Yu G, et al. (2017). *ggtree.* Methods Ecol Evol 8:28–36. https://doi.org/10.1111/2041-210X.12628
- ‏Lewis PO (2001). Syst Biol 50:913–925. https://doi.org/10.1080/106351501753462876
- ‏Robinson DF, Foulds LR (1981). *Comparison of phylogenetic trees.* Math Biosci 53:131–147. https://doi.org/10.1016/0025-5564(81)90043-2
- ‏MAFFT برای ویندوز: https://mafft.cbrc.jp/alignment/software/windows.html · IQ-TREE: https://iqtree.github.io · MEGA: https://www.megasoftware.net · iTOL: https://itol.embl.de
- کتاب، Coursera، edX و فیلم‌های بیشتر: بخش منابع درس‌های [۱](01_lesson_msa_nj.md)، [۲](02_lesson_ml_iqtree.md) و [۳](03_lesson_outbreak_tree.md).

<sub>گام‌های ۱ تا ۶ با همان برنامه‌ها (MAFFT 7.526، R 4.6.1 با ape 5.8.1 و ggtree 4.2.0، IQ-TREE 3.1.3، Python 3.13) روی سرور لینوکسی دوره در 2026-11-09 اجرا شدند و همان عددهای درس‌های لینوکسی را دادند. روی ویندوز آزموده نشده‌اند. نصب و دستورهای PowerShell از مستندات‌اند (✍️).</sub>

</div>
