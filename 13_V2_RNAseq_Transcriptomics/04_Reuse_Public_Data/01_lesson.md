<div dir="rtl">

# درس: بازتولید یک یافته‌ی منتشرشده؛ از GEO تا ژن‌ها با Snakemake، و یک برچسب جابه‌جا

**بخش:** `13_V2_RNAseq_Transcriptomics` · **ماژول:** `04_Reuse_Public_Data` · **پیش‌نیاز:** ماژول [13/03](../03_Differential_Expression/) (اسکریپت‌های DESeq2)؛ Snakemake ([05](../../05_Reproducible_Work/))؛ PubMed با E-utilities ([11/06](../../11_V2_NCBI_Databases/06_Literature_PubMed_PMC/)) · **زمان:** حدود ۸۰ دقیقه · **ابزار:** Snakemake 9.25.2 (محیط `workflow` از بخش ۰۵) + R 4.5.3 و DESeq2 1.50.2 (محیط `rnaseq`) · **آخرین بازبینی:** 2026-10-28

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-28). کل گردش کار از پوشه‌ی خالی ۶۵ ثانیه، با بیشینه‌ی حافظه‌ی نزدیک به ۱ گیگابایت (با `--cores 1`).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ادعاهای یک مقاله را دقیق بخوانید و آن‌ها را به پرسش‌های **سنجیدنی** برگردانید.
2. با **Snakemake** یک گردش کار بسازید که از دانلود داده تا جدول نتیجه را خودکار و تکرارپذیر انجام دهد.
3. نتیجه‌ی خود را با مقاله بسنجید و تفاوت‌ها را **توضیح** دهید، نه پنهان.
4. **برچسب نمونه‌ها** را با خود داده بیازمایید و یک **جابه‌جایی** احتمالی را بیابید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate workflow && conda activate --stack rnaseq
mkdir -p ~/rnaseq/himes && cd ~/rnaseq/himes
P=~/course-bioinformatics-main/13_V2_RNAseq_Transcriptomics/99_scripts_data
which snakemake Rscript
```

</div>

‏`conda activate --stack` محیط دوم را **روی** محیط نخست می‌گذارد: `snakemake` از `workflow` (بخش ۰۵) و `Rscript` با DESeq2 از `rnaseq` می‌آید. (کوشیدیم Snakemake را در خود `rnaseq` نصب کنیم؛ conda با ناسازگاری نسخه‌ی پایتون نپذیرفت. پشته‌کردن دو محیط ساده‌تر بود.)

---

## ۱. داستان

داده‌ی GSE52778 را از 11/04 تا 13/03 بارها دیدید. اکنون پرسش بزرگ‌تر: **آیا یافته‌ی مقاله‌ی Himes و همکاران (۲۰۱۴) از داده‌ی عمومی بازتولید می‌شود؟** این کار هر پژوهشگری است که پیش از ساختن روی کار دیگران، می‌خواهد مطمئن شود. و چنان‌که خواهید دید، گاهی چیزی می‌یابد که در مقاله نیست.

**پاسخ معلوم (از چکیده‌ی مقاله، گام ۱):** ‏۳۱۶ ژن با p تصحیح‌شده‌ی Benjamini–Hochberg کمتر از ۰٫۰۵؛ ژن‌های نام‌برده: DUSP1، KLF15، PER1، TSC22D3، C7، CCDC69، CRISPLD2.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ بازتولید یا تکرار؟

| | بازتولید (reproduce) | تکرار (replicate) |
| :--- | :--- | :--- |
| داده | **همان** داده | داده‌ی **تازه** (آزمایش دوباره) |
| پرسش | آیا تحلیل درست است؟ | آیا یافته در جهان واقعی پابرجاست؟ |
| این درس | ✅ | ‏(CRISPLD2 در مقاله با qPCR و وسترن تکرار شد) |

### ۲.۲ چرا گردش کار؟

اگر همین کار را با ده دستور دستی انجام دهید، شش ماه بعد نمی‌دانید کدام فایل از کدام دستور آمد. **Snakemake** (بخش ۰۵) هر گام را یک **قاعده** (rule) با ورودی، خروجی و دستور می‌نویسد؛ ترتیب را خودش از وابستگی‌ها می‌سازد، تنها گام‌های لازم را دوباره می‌زند، و گزارش هر گام را نگه می‌دارد.

<div dir="ltr">

```text
download ──> deseq2 ──> paper_check
    └──────> check_labels
```

</div>

### ۲.۳ فراداده هم داده است

برچسب «دگزامتازون» روی یک نمونه را **انسان** نوشته است: در آزمایشگاه، روی لوله، در جدول، در فرم GEO. هر گام می‌تواند خطا داشته باشد. پژوهش‌های بزرگ نشان داده‌اند **جابه‌جایی نمونه‌ها** در داده‌های ژنومی رایج است و با خود داده (برای نمونه بیان ژن‌های شناخته‌شده) شناختنی است (Westra و همکاران، ۲۰۱۱). پس پیش از تحلیل، بپرسید: **آیا داده با برچسب‌هایش جور است؟**

---

## ۳. گام ۱: ادعاهای مقاله، دقیق

<div dir="ltr">

```bash
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
id=$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=pubmed --data-urlencode "term=10.1371/journal.pone.0099625[doi]" | grep -oE '<Id>[0-9]+' | cut -d'>' -f2)
echo "PMID $id"
curl -sS "$B/efetch.fcgi?db=pubmed&id=$id&rettype=abstract&retmode=text" | grep -A4 "Benjamini"
```

</div>

**خروجی واقعی (2026-10-28):**

<div dir="ltr">

```
PMID 24926665
synthetic glucocorticoid (1 µM for 18 hours). Based on a Benjamini-Hochberg 
corrected p-value <0.05, we identified 316 differentially expressed genes, 
including both well known (DUSP1, KLF15, PER1, TSC22D3) and less investigated 
(C7, CCDC69, CRISPLD2) glucocorticoid-responsive genes. CRISPLD2, which encodes 
a secreted protein previously implicated in lung development and endotoxin 
```

</div>

‏`--data-urlencode` لازم است چون `[doi]` و `/` در نشانی معنای ویژه دارند (بی آن `curl` پیام `bad range in URL` داد). سه ادعای سنجیدنی: (۱) ‏۳۱۶ ژن، (۲) هفت ژن نام‌برده، (۳) دگزامتازون **۱ میکرومولار، ۱۸ ساعت**. مقاله تنها دگزامتازون را گزارش کرده؛ نمونه‌های آلبوترول در GEO هستند ولی در این چکیده نه.

---

## ۴. گام ۲: گردش کار

‏`Snakefile` در `$P/04_Reuse_Public_Data/workflow/` است. دو قاعده‌ی آن:

<div dir="ltr">

```python
rule download:
    output:
        matrix = "data/GSE52778_series_matrix.txt.gz",
        counts = "data/counts.tsv.gz",
        genes = "data/geneid2ens.tsv",
        atlas = "data/e52778.tsv"
    log: "logs/download.log"
    shell: "bash {P}/03_Differential_Expression/data/download.sh data > {log} 2>&1"

rule deseq2:
    input:
        matrix = "data/GSE52778_series_matrix.txt.gz",
        counts = "data/counts.tsv.gz",
        genes = "data/geneid2ens.tsv",
        atlas = "data/e52778.tsv"
    output:
        table = "results/de_dex_deseq2.tsv",
        pca = "results/pca_gse52778.png"
    log: "logs/deseq2.log"
    shell:
        "cd results && Rscript {P}/03_Differential_Expression/scripts/de_gse52778.R "
        "../{input.matrix} ../{input.counts} ../{input.genes} ../{input.atlas} > ../{log} 2>&1"
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`output: matrix = …` | خروجی‌های **نام‌دار**؛ در دستور با `{output.matrix}` |
| ‏`input:` در deseq2 | همان فایل‌ها؛ Snakemake از این‌جا می‌فهمد deseq2 پس از download است |
| ‏`log:` | گزارش هر گام در `logs/` |
| ‏`{P}` | پوشه‌ی اسکریپت‌ها، از `--config scripts=…` |
| ‏`cd results &&` | اسکریپت 13/03 فایل‌ها را در پوشه‌ی کنونی می‌نویسد |

ما نخست `input: rules.download.output` نوشتیم (همه‌ی خروجی‌های download، کوتاه). Snakemake با پیام `'InputFiles' object has no attribute 'matrix'` ایستاد: نام‌ها با این روش منتقل نمی‌شوند. پس ورودی‌ها را با نام نوشتیم.

**اجرای آزمایشی** (`-n`: تنها نقشه را نشان بده):

<div dir="ltr">

```bash
snakemake -s $P/04_Reuse_Public_Data/workflow/Snakefile --cores 1 -n --config scripts=$P | grep -A8 "^Job stats"
```

</div>

<div dir="ltr">

```
Job stats:
job             count
------------  -------
download            1
check_labels        1
deseq2              1
paper_check         1
all                 1
total               5
```

</div>

**اجرای واقعی:**

<div dir="ltr">

```bash
snakemake -s $P/04_Reuse_Public_Data/workflow/Snakefile --cores 1 --config scripts=$P > snakemake.log 2>&1
grep -E "steps \(" snakemake.log | tail -1
ls results logs
```

</div>

<div dir="ltr">

```
5 of 5 steps (100%) done
logs:
check_labels.log
deseq2.log
download.log

results:
de_dex_deseq2.tsv
labels.tsv
ma_gse52778.png
paper_check.txt
pca_gse52778.png
volcano_gse52778.png
```

</div>

- **۶۵ ثانیه** از پوشه‌ی خالی تا همه‌ی نتیجه‌ها، با بیشینه‌ی حافظه‌ی نزدیک به ۱ گیگابایت.
- ‏**`--cores 1`** را عمداً گذاشتیم: دو گام R (deseq2 و check_labels) به هم وابسته نیستند و با `--cores 2` هم‌زمان اجرا می‌شوند، هر کدام نزدیک به ۱ گیگابایت. روی لپ‌تاپ با حافظه‌ی کم، این دو برابر می‌شود.
- دوباره زدن همان دستور: `Nothing to be done (all requested files are present and up to date).`

> 📺 **فیلم:** *An introduction to Snakemake tutorial for beginners (CC248)* (Riffomonas Project): https://www.youtube.com/watch?v=r9PWnEmz_tc
> 📄 **مرجع:** Mölder F, et al. (2021). *Sustainable data analysis with Snakemake.* F1000Research 10:33. https://doi.org/10.12688/f1000research.29032.2

---

## ۵. گام ۳: سنجش با مقاله

<div dir="ltr">

```bash
cat results/paper_check.txt
```

</div>

**خروجی واقعی (2026-10-28):**

<div dir="ltr">

```
paper: 316 genes with BH p < 0.05
ours:  4743 genes with padj < 0.05 (1064 with |log2FC| > 1)
padj of our 316th gene (a list as long as the paper's): 4.92e-19

the seven genes named in the abstract:
         symbol  log2FC           padj  rank
1843      DUSP1    2.95  1.863042e-124     3
28999     KLF15    4.40   1.822182e-85    15
5187       PER1    3.22   2.981768e-79    20
26112    CCDC69    2.94   1.037396e-72    27
83716  CRISPLD2    2.63   1.054229e-43    79
1831    TSC22D3    3.21   2.192917e-19   304
730          C7    3.20   3.134626e-13   549

reproduced: 7 of 7 named genes; in our top 316: 6
```

</div>

**توضیح خروجی:**
- **هر هفت** ژن نام‌برده بازتولید شدند، همه با همان جهت (بالا) و padj بسیار کوچک؛ شش تا در ۳۱۶ ژن برتر ما. ✅ یافته‌ی **کیفی** مقاله استوار است.
- **شمار ژن‌ها نه:** ما **۴۷۴۳** ژن یافتیم، ۱۵ برابر ۳۱۶. حتی با برش |log2FC| > ۱ هنوز ۱۰۶۴. چرا؟ چکیده روش آماری را نمی‌گوید، پس تنها می‌توانیم گمان‌های سنجیدنی بنویسیم: (الف) **ابزار و نسخه** (روش‌های ۲۰۱۴ و DESeq2 امروز توان گوناگونی دارند)؛ (ب) **طرح جفتی**: در 13/03 دیدید بی `cell` ‏۳۲٪ ژن‌ها گم می‌شوند؛ (ج) **آنوتیشن** و **فیلتر** ژن‌ها؛ (د) شاید آستانه‌ی **اندازه**ی تغییر هم داشته‌اند. بخش روش مقاله (متن کامل در PMC، 11/06) را برای پاسخ بخوانید.
- **درس:** «بازتولید» یعنی یافته‌ی **زیستی** (کدام ژن‌ها، چه جهتی، چه اندازه‌ای) استوار است، نه این‌که هر عدد یکی باشد. تفاوت‌ها را گزارش کنید و توضیح دهید.

---

## ۶. گام ۴: آیا برچسب‌ها با داده جورند؟

**چرا؟** در 12/06 دیدید Expression Atlas برای «آلبوترول + دگزامتازون» تنها ۸۳ ژن معنادار داد، در برابر ۲۱۴۲ برای دگزامتازون تنها؛ و DESeq2 خودمان (گام ۴ پایین) تنها ۴۲۱ ژن، در برابر ۴۷۴۳ (13/03). ولی آلبوترول به تنهایی کمابیش هیچ اثری نداشت (12/06: صفر ژن). پس ترکیب باید همانند دگزامتازون باشد. چیزی جور نیست.

اسکریپت `check_labels.R` برای هر نمونه یک **امتیاز گلوکوکورتیکوئید** حساب می‌کند: میانگین log2 CPM هفت ژنی که دگزامتازون روشن می‌کند (FKBP5، TSC22D3، ZBTB16، PER1، KLF15، CRISPLD2، DUSP1)، منهای همان امتیاز در نمونه‌ی **بی‌تیمار همان فرد**. نمونه‌هایی که دگزامتازون گرفته‌اند باید امتیاز بالا داشته باشند.

<div dir="ltr">

```bash
cat logs/check_labels.log
```

</div>

**خروجی واقعی (2026-10-28):**

<div dir="ltr">

```
== glucocorticoid score (log2, relative to the donor's untreated sample)
    cell gc_score.Untreated gc_score.Dexamethasone gc_score.Albuterol
  N61311                  0                   3.86               0.10
 N052611                  0                   3.63               3.57
 N080611                  0                   2.83               2.86
 N061011                  0                   3.87               0.30
 gc_score.Albuterol_Dexamethasone
                             3.93
                             1.45
                             0.88
                             4.03

== samples whose label disagrees with the score
              cell               treatment gc_score
GSM1275868 N052611               Albuterol     3.57
GSM1275869 N052611 Albuterol_Dexamethasone     1.45
GSM1275872 N080611               Albuterol     2.86
GSM1275873 N080611 Albuterol_Dexamethasone     0.88

== albuterol + dexamethasone vs untreated (~ cell + trt)
                  n_padj_0.05 FKBP5_log2FC ZBTB16_log2FC
labels_as_in_GEO          421         2.92          6.08
labels_swapped_in        3593         4.11          7.44
donors swapped: N052611, N080611 
```

</div>

**خواندن خروجی:**
- در دو فرد (N61311 و N061011) همه‌چیز جور است: دگزامتازون و ترکیب ~۴، آلبوترول ~۰.
- در دو فرد دیگر (N052611 و N080611) نمونه‌ی **«آلبوترول»** امتیاز دگزامتازونی دارد (۳٫۶ و ۲٫۹) و نمونه‌ی **«آلبوترول + دگزامتازون»** امتیاز پایین (۱٫۴ و ۰٫۹). درست وارونه‌ی انتظار.
- اگر این دو برچسب را در این دو فرد **جابه‌جا** کنیم، مقایسه‌ی ترکیب ‏**۳۵۹۳** ژن می‌دهد (به جای ۴۲۱)، و log2FC ‏FKBP5 و ZBTB16 (‏۴٫۱۱ و ۷٫۴۴) درست همانند دگزامتازون تنها (‏۴٫۰۳ و ۷٫۴۳ در 13/03) می‌شود.
- امتیاز پایین «ترکیب» در این دو فرد صفر نیست (۱٫۴ و ۰٫۹)، و از آلبوترول در فردهای جور (۰٫۱ و ۰٫۳) بیشتر است. تمرین ۲ ژن به ژن نشان می‌دهد این تنها اثر cAMP نیست: ZBTB16 هم کمی بالا رفته است. پس داستان شاید از یک جابه‌جایی ساده پیچیده‌تر باشد. این را باز می‌گذاریم.

**آیا فراداده‌ی GEO خودش ناسازگار است؟**

<div dir="ltr">

```bash
zcat data/GSE52778_series_matrix.txt.gz | grep -E '^!Sample_(title|geo_accession)' | cut -f8-9
```

</div>

<div dir="ltr">

```
!Sample_title	"N052611_Alb"	"N052611_Alb_Dex"
!Sample_geo_accession	"GSM1275868"	"GSM1275869"
```

</div>

نه: نام نمونه (title) و ویژگی treatment در GEO هم‌سازند. اگر جابه‌جایی رخ داده، **پیش** از ثبت در GEO بوده است (در آزمایشگاه یا هنگام آماده کردن فایل‌ها).

**نتیجه‌گیری درست:** داده **به‌شدت** نشان می‌دهد برچسب آلبوترول و آلبوترول + دگزامتازون در دو فرد جابه‌جاست. ولی این **اثبات** نیست؛ تنها نویسندگان یا آزمایش دوباره می‌توانند آن را تأیید کنند. کار درست: (۱) در گزارش خود بنویسید چه دیدید و تحلیل را با هر دو برچسب‌گذاری نشان دهید؛ (۲) به نویسندگان یا GEO خبر دهید؛ (۳) برای پرسش اصلی مقاله (دگزامتازون تنها) این مشکل اثری ندارد، چون آن نمونه‌ها جور بودند. همین یافته پاسخ ناهمخوانی 12/06 ‏(Expression Atlas) است.

> 📄 **مرجع:** Westra HJ, et al. (2011). *MixupMapper: correcting sample mix-ups in genome-wide datasets increases power to detect small genetic effects.* Bioinformatics 27:2104–2111. https://doi.org/10.1093/bioinformatics/btr323

---

## ۷. سه اشتباه رایج

1. **«بازتولید نشد» چون عددها یکی نیستند.** ‏۳۱۶ در برابر ۴۷۴۳ با هفت از هفت ژن یکسان یعنی یافته استوار و **روش** متفاوت است. و حتی دو اجرای خود ما (13/03 و این گردش کار) در **رقم‌های آخر** padj فرق داشتند (بیشینه ۲×۱۰⁻⁶) و همان ۴۷۴۳ ژن را دادند: محاسبه‌ی عددی همیشه بیت به بیت یکسان نیست.
2. **باور کورکورانه به فراداده.** برچسب‌ها را با خود داده بسنجید: ژن‌های شناخته‌شده‌ی تیمار، جنس (XIST و ژن‌های Y)، و PCA (13/03). یک جابه‌جایی، مقایسه را از ۳۵۹۳ ژن به ۴۲۱ رساند.
3. ‏**‏Snakemake و `head` در لوله.** ‏Snakemake هر دستور را با `set -euo pipefail` می‌زند. در تمرین ۴ دیدید `sort … | head -20` با کد خروج ۱۴۱ (SIGPIPE) شکست می‌خورد: `head` پس از ۲۰ سطر لوله را می‌بندد و `sort` خطا می‌گیرد. به جایش `awk 'NR <= 20'`.

---

## 📘 برای کنجکاوها

- ‏**‏`--forcerun` و پاک کردن خروجی:** ‏`snakemake … --forcerun deseq2 -n` نشان می‌دهد deseq2 و هر گام پس از آن (paper_check) دوباره زده می‌شوند. پاک کردن `results/paper_check.txt` تنها همان یک گام را برمی‌گرداند. ‏Snakemake ‏۹ تصمیم دوباره زدن را بر پایه‌ی سابقه‌ی خودش می‌گیرد: ما ورودی را با `touch` تازه کردیم و Snakemake باز هم «Nothing to be done» گفت.
- **محیط برای هر قاعده:** ‏`conda: "env.yml"` در هر قاعده و `--use-conda`، هر گام را در محیط خودش می‌زند (بخش ۲۰).
- ‏**‏Expression Atlas** و **recount3**، هزاران آزمایش GEO را با یک خط لوله بازتحلیل کرده‌اند؛ این بازتحلیل‌ها برای بازتولید سریع سودمندند، ولی چنان‌که دیدیم از خطای فراداده در امان نیستند.

---

## جمع‌بندی

- ادعاهای سنجیدنی مقاله: ‏۳۱۶ ژن، هفت ژن نام‌برده، دگزامتازون ۱ µM / ۱۸ ساعت.
- گردش کار Snakemake: download ← deseq2 ← paper_check، و check_labels؛ ‏۶۵ ثانیه، `--cores 1` برای حافظه.
- بازتولید: هفت از هفت ژن (شش در ۳۱۶ برتر)؛ ولی ۴۷۴۳ ژن به جای ۳۱۶، که با روش و طرح توضیح‌پذیر است.
- برچسب‌ها: در دو فرد، «آلبوترول» و «آلبوترول + دگزامتازون» به‌احتمال زیاد جابه‌جا‌اند؛ با جابه‌جایی، ترکیب ۳۵۹۳ ژن (به جای ۴۲۱) و همان log2FC دگزامتازون.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
conda activate workflow && conda activate --stack rnaseq            # snakemake + Rscript/DESeq2
snakemake -s Snakefile --cores 1 -n --config scripts=$P            # dry run (job stats)
snakemake -s Snakefile --cores 1 --config scripts=$P               # run
snakemake -s Snakefile TARGET --cores 1 --config scripts=$P        # one target (targets BEFORE --config)
snakemake -s Snakefile --cores 1 -n --forcerun RULE --config scripts=$P
Rscript check_labels.R GSE52778_series_matrix.txt.gz counts.tsv.gz labels.tsv
python3 paper_check.py results/de_dex_deseq2.tsv
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| بازتولید (reproduce) | رسیدن به همان نتیجه از همان داده |
| تکرار (replicate) | رسیدن به همان نتیجه با آزمایش تازه |
| گردش کار (workflow) | زنجیره‌ی گام‌های تحلیل، نوشته‌شده و خودکار |
| قاعده (rule) | یک گام در Snakemake با ورودی، خروجی و دستور |
| اجرای آزمایشی (dry run) | نشان دادن گام‌هایی که اجرا خواهند شد، بی اجرا |
| پشته‌کردن محیط (`--stack`) | فعال کردن یک محیط conda روی دیگری |
| فراداده | داده درباره‌ی داده: برچسب نمونه، تیمار، فرد |
| جابه‌جایی نمونه (sample swap) | برچسب دو نمونه به اشتباه با هم عوض شده |
| امتیاز گلوکوکورتیکوئید | میانگین بیان ژن‌های نشانگر پاسخ، نسبت به شاهد همان فرد |
| ‏SIGPIPE (کد ۱۴۱) | خطای برنامه‌ای که در لوله می‌نویسد پس از بسته شدن خواننده |

---

## منابع

**مقاله و مستند**
- ‏Himes BE, et al. (2014). *RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells.* PLoS ONE 9:e99625. https://doi.org/10.1371/journal.pone.0099625 (PMID 24926665، PMC4057123)
- ‏Mölder F, et al. (2021). *Sustainable data analysis with Snakemake.* F1000Research 10:33. https://doi.org/10.12688/f1000research.29032.2
- ‏Westra HJ, et al. (2011). *MixupMapper.* Bioinformatics 27:2104–2111. https://doi.org/10.1093/bioinformatics/btr323
- ‏Freedman LP, Cockburn IM, Simcoe TS (2015). *The Economics of Reproducibility in Preclinical Research.* PLoS Biol 13:e1002165. https://doi.org/10.1371/journal.pbio.1002165
- راهنمای Snakemake: https://snakemake.readthedocs.io

**کتاب**
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱: پژوهش تکرارپذیر؛ فصل ۱۲: خط لوله‌ها)
- ‏Holmes S, Huber W (2019). *Modern Statistics for Modern Biology.* Cambridge University Press. https://www.huber.embl.de/msmb/

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioconductor for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/bioconductor
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *An introduction to Snakemake tutorial for beginners (CC248)* (Riffomonas Project): https://www.youtube.com/watch?v=r9PWnEmz_tc
- ‏YouTube: *Snakemake #1 Writing your first Snakefile* (actually scientist): https://www.youtube.com/watch?v=Gg0SsEs16Jc

<sub>همه‌ی دستورها در 2026-10-28 روی سرور دوره اجرا شدند (Snakemake 9.25.2 از محیط بخش ۰۵ + محیط `rnaseq`). فیلم‌ها در بخش ۰۵ با noembed وارسی شده بودند؛ DOIها با Crossref. نشانه‌های جابه‌جایی برچسب از داده است و نویسندگان آن را تأیید نکرده‌اند.</sub>

</div>
