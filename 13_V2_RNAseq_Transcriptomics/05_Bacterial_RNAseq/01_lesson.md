<div dir="rtl">

# درس: ‏RNA-seq باکتری؛ پاسخ SOS اشریشیا کلی به سیپروفلوکساسین

**بخش:** `13_V2_RNAseq_Transcriptomics` · **ماژول:** `05_Bacterial_RNAseq` · **پیش‌نیاز:** ماژول‌های [13/02](../02_Alignment_Quantification/) و [13/03](../03_Differential_Expression/)؛ کینولون‌ها و QRDR ([08/01](../../08_AMR_Virulence_Phylogeny/01_AMR_Resistance_Genes/)) · **زمان:** حدود ۸۰ دقیقه · **ابزار:** Bowtie2 2.5.5، samtools 1.25، featureCounts 2.1.1، R 4.5.3 و DESeq2 1.50.2 (محیط `rnaseq`) · **آخرین بازبینی:** 2026-10-28

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-28). داده ۱۹ ثانیه، ایندکس ۲ ثانیه، هم‌ترازی شش نمونه ۲۵ ثانیه، DESeq2 ‏۶ ثانیه با ۸۶۷ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. تفاوت‌های RNA-seq باکتری و یوکاریوت را بگویید و پیامد هر کدام را در تحلیل بدانید.
2. ریدهای باکتری را با **Bowtie2** هم‌تراز و با **featureCounts** روی GFF شمارش کنید.
3. سهم **rRNA** مانده و ریدهای **چندجایی** را بسنجید.
4. با DESeq2 پاسخ **SOS** را بیابید و **اپرون‌ها** را در نتیجه ببینید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate rnaseq
P=~/course-bioinformatics-main/13_V2_RNAseq_Transcriptomics/99_scripts_data
bash $P/05_Bacterial_RNAseq/data/make_data.sh ~/rnaseq/ecoli
cd ~/rnaseq/ecoli
```

</div>

---

## ۱. داستان

سیپروفلوکساسین (یک کینولون) آنزیم‌های DNA gyrase و topoisomerase IV را روی DNA قفل می‌کند و DNA می‌شکند. در 08/01 دیدید جهش در **QRDR** ژن‌های gyrA و parC مقاومت می‌سازد. ولی باکتری حساس چه می‌کند؟ پروتئین **RecA** روی DNA تک‌رشته‌ای می‌نشیند و سرکوبگر **LexA** را به خودشکنی وامی‌دارد. LexA که از جعبه‌ی SOS پیش‌برها کنار برود، ده‌ها ژن ترمیم DNA روشن می‌شوند: **پاسخ SOS** (Courcelle و همکاران ۲۰۰۱؛ Cirz و همکاران ۲۰۰۵).

**پاسخ معلوم (شبیه‌سازی‌شده، با الهام از این مقاله‌ها):** سه نمونه بی دارو (`ctrl`) و سه نمونه با سیپروفلوکساسین (`cip`)، هر کدام ۴۰۰٬۰۰۰ رید تک‌سر ۷۵ بازی:

| ژن‌ها | ‏log2FC واقعی | نکته |
| :--- | :---: | :--- |
| ‏sulA، tisB | ۴ | ‏sulA تقسیم سلول را می‌ایستاند؛ tisB تنها ۹۰ باز است |
| ‏recN، umuD-umuC | ۳٫۵ | ‏umuDC یک **اپرون** است |
| ‏recA-recX، dinI، yebG | ۳ | ‏recAX اپرون |
| ‏lexA-dinF، dinB | ۲٫۵ | ‏lexA خودش را هم سرکوب می‌کند |
| ‏uvrA، uvrB | ۲ | |
| اپرون S10 (۱۱ ژن پروتئین ریبوزومی، rpsJ تا rpsQ) | ‎−۱٫۵ | رشد کندتر |

۲۵ ژن تغییرکرده از ۴۳۹۷ ژن، و ۶ تا ۱۵٪ رید از rRNA مانده.

---

## ۲. مفهوم به زبان ساده: باکتری چه فرقی دارد؟

| | یوکاریوت (13/02) | باکتری | پیامد در تحلیل |
| :--- | :--- | :--- | :--- |
| اینترون | دارد | **ندارد** | هم‌ترازکننده‌ی ساده (Bowtie2، BWA)؛ نیازی به HISAT2 یا STAR نیست |
| دم poly(A) | دارد | **ندارد** | برداشت mRNA با poly(A) ممکن نیست؛ باید **rRNA را برداشت** (rRNA بیش از ۹۰٪ RNA است) |
| ژن در هر RNA | یکی | گاهی چند (**اپرون**) | ژن‌های یک اپرون با هم بالا و پایین می‌روند؛ رید میان ژن‌ها هم هست |
| تراکم ژن | کم | نزدیک به ۸۸٪ ژنوم کدکننده است | ژن‌ها رو یا کنار هم‌اند؛ **جهت‌دار بودن** کتابخانه بسیار مهم است |
| ‏RNA کوچک (sRNA) | | فراوان، ۵۰ تا ۲۵۰ باز | شمار رید کم؛ توان آماری کم |
| آنوتیشن | GTF (Ensembl) | **GFF** (NCBI RefSeq) | ‏featureCounts با `-t gene -g locus_tag` |

> 📺 **فیلم:** *Regulator for SOS Response: LexA-DNA Complex* (nomunak): https://www.youtube.com/watch?v=2cOoYTooBFA
> 📄 **مرجع:** Creecy JP, Conway T (2015). *Quantitative bacterial transcriptomics with RNA-seq.* Curr Opin Microbiol 23:133–140. https://doi.org/10.1016/j.mib.2014.11.011

---

## ۳. گام ۱: هم‌ترازی با Bowtie2

<div dir="ltr">

```bash
mkdir -p bam
bowtie2-build --threads 2 ref/ecoli.fa ref/ecoli > ref/build.log
for s in ctrl_1 ctrl_2 ctrl_3 cip_1 cip_2 cip_3; do
  bowtie2 -p 2 -x ref/ecoli -U reads/$s.fastq.gz 2> bam/$s.bowtie2.log | samtools sort -@2 -o bam/$s.bam -
  samtools index bam/$s.bam
done
cat bam/ctrl_1.bowtie2.log
```

</div>

**خروجی واقعی (2026-10-28):**

<div dir="ltr">

```
400000 reads; of these:
  400000 (100.00%) were unpaired; of these:
    10 (0.00%) aligned 0 times
    357994 (89.50%) aligned exactly 1 time
    41996 (10.50%) aligned >1 times
100.00% overall alignment rate
```

</div>

- ‏`-U`: ریدهای تک‌سر (unpaired). برای جفت‌سر `-1` و `-2`.
- ساختن ایندکس ژنوم ۴٫۶ مگابازی **۲ ثانیه** و ۱۰۷ مگابایت حافظه؛ هم‌ترازی هر نمونه چهار ثانیه.
- **‏۱۰٫۵٪ چندجایی:** ‏E. coli هفت اپرون rRNA کمابیش یکسان دارد (rrnA تا rrnH)، و چند نسخه‌ی عنصر IS. ریدی که دو جای یکسان دارد، Bowtie2 یکی را به تصادف برمی‌گزیند و کیفیت هم‌ترازی (MAPQ) پایین می‌دهد. گام ۳ را ببینید.

> 📄 **مرجع:** Langmead B, Salzberg SL (2012). *Fast gapped-read alignment with Bowtie 2.* Nat Methods 9:357–359. https://doi.org/10.1038/nmeth.1923

---

## ۴. گام ۲: شمارش و جهت کتابخانه

ابتدا جهت را بیازمایید (همان کار 13/02، این‌جا با featureCounts):

<div dir="ltr">

```bash
mkdir -p counts
for st in 0 1 2; do
  featureCounts -T 2 -s $st -t gene -g locus_tag -a ref/ecoli.gff -o counts/s$st.txt bam/ctrl_1.bam > /dev/null 2>&1
  echo "s=$st $(grep -E '^Assigned|^Unassigned_NoFeatures|^Unassigned_Ambiguity' counts/s$st.txt.summary | tr '\t' ' ' | tr '\n' ' ')"
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
s=0 Assigned 395938 Unassigned_NoFeatures 982 Unassigned_Ambiguity 3070 
s=1 Assigned 1161 Unassigned_NoFeatures 398800 Unassigned_Ambiguity 29 
s=2 Assigned 397098 Unassigned_NoFeatures 992 Unassigned_Ambiguity 1900 
```

</div>

- ‏`-s 2` (reverse، کتابخانه‌ی dUTP) درست است: ‏`-s 1` تنها ۱۱۶۱ رید می‌دهد.
- ‏`-s 0` (بی‌جهت) هم کمابیش همه را می‌شمارد، ولی **Ambiguity** آن ۳۰۷۰ است در برابر ۱۹۰۰: در باکتری ژن‌های **رو به روی هم** روی دو رشته فراوان‌اند و بی جهت، ریدِ جای همپوشانی به هر دو می‌خورد.
- ‏`-t gene -g locus_tag`: در GFF سطرهای `gene` را بشمار و نام را از ویژگی `locus_tag` (مانند `b2699`) بگیر. ‏locus_tag یکتا است؛ نام ژن (recA) گاهی تکراری یا تهی است.

اکنون همه‌ی نمونه‌ها:

<div dir="ltr">

```bash
featureCounts -T 2 -s 2 -t gene -g locus_tag -a ref/ecoli.gff -o counts/gene_counts.txt bam/{ctrl,cip}_{1,2,3}.bam > counts/fc.log 2>&1
```

</div>

> 📄 **مرجع:** Liao Y, Smyth GK, Shi W (2014). *featureCounts.* Bioinformatics 30:923–930. https://doi.org/10.1093/bioinformatics/btt656

---

## ۵. گام ۳: ‏DESeq2 و پاسخ معلوم

اسکریپت `de_bacterial.R` نخست سهم هر نوع ژن را نشان می‌دهد، rRNA و tRNA را کنار می‌گذارد، سپس DESeq2 را با `~ condition` می‌زند و با پاسخ معلوم می‌سنجد:

<div dir="ltr">

```bash
Rscript $P/05_Bacterial_RNAseq/scripts/de_bacterial.R counts/gene_counts.txt reads/genes.tsv reads/truth.tsv
```

</div>

**خروجی واقعی (2026-10-28):**

<div dir="ltr">

```
== share of counted reads per biotype (%)
       ncRNA other protein_coding rRNA tRNA
ctrl_1   0.3     0           91.7  8.1    0
ctrl_2   0.3     0           87.6 12.1    0
ctrl_3   0.3     0           93.7  6.0    0
cip_1    0.3     0           84.6 15.1    0
cip_2    0.3     0           89.6 10.1    0
cip_3    0.3     0           92.6  7.0    0

genes kept (protein_coding + ncRNA): 4397 

== size factors
ctrl_1 ctrl_2 ctrl_3  cip_1  cip_2  cip_3 
 1.019  1.020  1.040  0.979  1.004  1.047 

== padj < 0.05: 21 genes ( 15 up, 6 down )

== genes with a known change
      name operon log2fc_true log2FC     padj baseMean
b0958 sulA      -         4.0   4.61 1.11e-28      108
b4618 tisB      -         4.0   3.98 9.71e-06       16
b2616 recN      -         3.5   3.44 1.04e-31      253
b1061 dinI      -         3.0   3.39 1.78e-09       32
b1848 yebG      -         3.0   3.14 1.14e-08       30
b0231 dinB      -         2.5   3.04 7.25e-19       91
b0779 uvrB      -         2.0   1.90 3.71e-10      118
b4058 uvrA      -         2.0   2.00 9.54e-10      172
b4043 lexA   lexA         2.5   2.59 1.02e-08       40
b4044 dinF   lexA         2.5   2.61 2.92e-13      120
b2699 recA   recA         3.0   2.97 7.10e-18      106
b2698 recX   recA         3.0   3.44 8.38e-14       52
b3311 rpsQ    S10        -1.5  -0.98 9.97e-01       26
b3312 rpmC    S10        -1.5  -1.31 6.78e-01       17
b3313 rplP    S10        -1.5  -1.04 6.45e-01       50
b3314 rpsC    S10        -1.5  -1.06 3.69e-02       94
b3315 rplV    S10        -1.5  -1.13 6.71e-01       46
b3316 rpsS    S10        -1.5  -1.06 7.62e-01       37
b3317 rplB    S10        -1.5  -1.36 8.46e-04      114
b3318 rplW    S10        -1.5  -0.83 9.97e-01       39
b3319 rplD    S10        -1.5  -1.20 2.02e-02       76
b3320 rplC    S10        -1.5  -1.31 3.46e-03       85
b3321 rpsJ    S10        -1.5  -1.28 9.88e-01       16
b1183 umuD   umuD         3.5   3.31 4.78e-11       37
b1184 umuC   umuD         3.5   3.68 1.50e-29      194

found: 18 of 25 known genes; false positives: 3 
      name log2FC   padj
b0282 yagP   1.35 0.0369
b0921 cmoM  -1.07 0.0490
b3922 yiiS  -1.10 0.0181
```

</div>

**توضیح خروجی:**
- ‏**rRNA:** ‏۶ تا ۱۵٪ رید شمرده‌شده، و از نمونه‌ای به نمونه‌ی دیگر فرق دارد (کارایی برداشت rRNA هر بار فرق می‌کند). اگر در جدول بماند، اندازه‌ی کتابخانه‌ی mRNA را بیش از واقع نشان می‌دهد؛ پس کنار گذاشتیم. (در داده‌ی واقعی گاهی ۵۰٪ و بیشتر.)
- **همه‌ی ۱۲ ژن SOS یافته شدند،** با log2FC نزدیک به پاسخ (۱٫۹۰ تا ۴٫۶۱ در برابر ۲ تا ۴). حتی tisB نود بازی، با baseMean تنها ۱۶، چون تغییرش بزرگ است (۱۶ برابر).
- **اپرون‌ها:** ‏recA و recX (۲٫۹۷ و ۳٫۴۴)، lexA و dinF (۲٫۵۹ و ۲٫۶۱)، umuD و umuC (۳٫۳۱ و ۳٫۶۸): هر جفت با هم. در داده‌ی واقعی همین الگو به شما کمک می‌کند ژن کم‌بیانی را که با اپرونش بالا رفته باور کنید.
- **اپرون S10:** همه‌ی ۱۱ ژن پایین (‎−۰٫۸۳ تا ‎−۱٫۳۶، کمتر از ‎−۱٫۵ واقعی)، ولی تنها **۶** تا معنادار. چرا کمتر از ‎−۱٫۵؟ چون هر ۱۱ ژن روی **یک** RNA‌اند و از یک نمونه‌گیری تصادفی آمده‌اند؛ اگر آن نمونه‌گیری بد بیفتد، همه با هم بد می‌افتند. پس ۱۱ ژن یک اپرون، **۱۱ شاهد جدا نیستند** (تمرین ۴).
- **۳ مثبت کاذب** با padj میان ۰٫۰۲ و ۰٫۰۵ (۳ از ۲۱ = ۱۴٪). ‏FDR پنج درصدی **میانگین** است؛ در یک آزمایش با شمار کم یافته، می‌تواند بیشتر بیفتد. هر سه log2FC نزدیک به ۱ دارند و padj نزدیک مرز.

> 📄 **مرجع:** Courcelle J, et al. (2001). *Comparative gene expression profiles following UV exposure in wild-type and SOS-deficient Escherichia coli.* Genetics 158:41–64. https://doi.org/10.1093/genetics/158.1.41

---

## ۶. گام ۴: رید میان ژن‌های اپرون

‏recX درست پس از recA است (روی رشته‌ی منفی؛ فاصله ۶۸ باز، 2822640 تا 2822707). اگر هر دو روی یک RNA باشند، باید ریدهایی **میان** آن‌ها هم باشد. ‏sulA تنهاست؛ پیش از آن (سوی ۳′ رشته‌ی منفی) چیزی نیست:

<div dir="ltr">

```bash
for s in ctrl_1 cip_1; do
  echo "$s recA-recX gap: $(samtools view -c bam/$s.bam NC_000913.3:2822650-2822697)  sulA-upstream gap: $(samtools view -c bam/$s.bam NC_000913.3:1020950-1021000)"
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ctrl_1 recA-recX gap: 3  sulA-upstream gap: 0
cip_1 recA-recX gap: 28  sulA-upstream gap: 0
```

</div>

ریدهای میان recA و recX با دارو **۹ برابر** شده‌اند، همراه خود اپرون. ‏featureCounts این ریدها را `Unassigned_NoFeatures` می‌گذارد (نزدیک به ۱۰۰۰ رید در هر نمونه). در داده‌ی واقعی، پوشش پیوسته میان ژن‌ها در IGV (12/03) یکی از نشانه‌های اپرون است؛ فهرست اپرون‌های شناخته‌شده‌ی E. coli را **RegulonDB** و **EcoCyc** دارند.

> 📄 **مرجع:** Tierrafría VH, et al. (2022). *RegulonDB 11.0.* Microb Genom 8:000833. https://doi.org/10.1099/mgen.0.000833

---

## ۷. سه اشتباه رایج

1. **کتابخانه‌ی بی‌جهت یا `-s` نادرست.** در باکتری، ژن‌های رو در روی دو رشته فراوان‌اند؛ با `-s 1` به جای `-s 2` تنها ۰٫۳٪ ریدها شمرده شد. همیشه سه حالت را بیازمایید.
2. ‏**‏rRNA در جدول شمارش.** ‏۱۵٪ در cip_1 در برابر ۶٪ در ctrl_3: این تفاوت فنی است، نه زیستی. کنارش بگذارید و درصدش را گزارش کنید (کیفیت برداشت).
3. **بریدن ریدهای چندجایی بی فکر.** ‏`featureCounts -Q 10` ریدهای با MAPQ پایین را دور می‌ریزد: rRNA کمابیش همه‌اش می‌رود (خوب)، ولی ژن‌های دو نسخه‌ای مانند **tufA** و **tufB** (فاکتور طویل‌سازی) و عنصرهای IS هم (تمرین ۲). برای آن‌ها بدانید چه می‌خواهید.

---

## 📘 برای کنجکاوها

- ‏**‏tisB و persister:** سیپروفلوکساسین از راه SOS، سم TisB را روشن می‌کند که سلول را خاموش و در برابر دارو «پایدار» (persister) می‌سازد (Dörr و همکاران ۲۰۱۰). اثر جانبی خود دارو.
- **جهش‌زایی و مقاومت:** ‏UmuDC و DinB پلیمرازهای پرخطا‌اند؛ مهار برش LexA تکامل مقاومت به سیپروفلوکساسین را در موش کند کرد (Cirz و همکاران ۲۰۰۵). پیوند با بخش ۰۸.
- **ابزارهای ویژه‌ی باکتری:** ‏READemption و ProkSeq گردش کارهای آماده‌اند؛ ‏Rockhopper اپرون‌ها و sRNAهای تازه را هم پیشنهاد می‌کند. برای شمارش با Salmon (13/02) باید ترنسکریپتوم ساخت: در باکتری، توالی هر ژن.
- ‏**‏Dual RNA-seq:** باکتری و میزبان در یک نمونه؛ هر رید را باید به یکی از دو ژنوم داد.

---

## جمع‌بندی

- باکتری: بی اینترون (Bowtie2)، بی poly(A) (برداشت rRNA)، اپرون، ژن‌های فشرده (جهت کتابخانه حیاتی).
- ‏Bowtie2: ‏۱۰۰٪ هم‌ترازی، ۱۰٫۵٪ چندجایی (rRNA و IS). ‏featureCounts: `-s 2 -t gene -g locus_tag`.
- ‏rRNA: ‏۶ تا ۱۵٪، پیش از DESeq2 کنار گذاشته شد.
- ‏DESeq2: هر ۱۲ ژن SOS (۱۸ از ۲۵ ژن تغییرکرده)، ۳ مثبت کاذب نزدیک مرز؛ ژن‌های یک اپرون با هم، و پوشش میان ژن‌های اپرون.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
bash make_data.sh ~/rnaseq/ecoli                               # genome + GFF + simulated reads
bowtie2-build --threads 2 ref/ecoli.fa ref/ecoli               # index (2 s)
bowtie2 -p 2 -x ref/ecoli -U reads/S.fastq.gz 2> S.log | samtools sort -o S.bam -
featureCounts -s 2 -t gene -g locus_tag -a ref/ecoli.gff -o gene_counts.txt bam/*.bam
featureCounts ... -Q 10                                        # drop reads with MAPQ < 10
samtools view -c S.bam CHR:START-END                           # reads in a region
Rscript de_bacterial.R gene_counts.txt genes.tsv truth.tsv
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| پاسخ SOS | روشن شدن ژن‌های ترمیم DNA پس از آسیب، با برش LexA به کمک RecA |
| ‏LexA | سرکوبگری که روی جعبه‌ی SOS پیش‌بر ژن‌ها می‌نشیند |
| اپرون (operon) | چند ژن پشت سر هم که با هم روی یک RNA رونویسی می‌شوند |
| برداشت rRNA (rRNA depletion) | حذف RNA ریبوزومی پیش از ساخت کتابخانه |
| ‏sRNA | ‏RNA کوچک باکتری (۵۰ تا ۲۵۰ باز) که ژن‌های دیگر را تنظیم می‌کند |
| ‏locus_tag | شناسه‌ی یکتای ژن در آنوتیشن باکتری (مانند b2699) |
| ریدهای چندجایی (multi-mapping) | ریدهایی که به بیش از یک جای ژنوم به یک اندازه می‌خورند |
| ‏MAPQ | کیفیت هم‌ترازی؛ برای ریدهای چندجایی پایین |
| ‏persister | سلول خاموشی که دارو را تاب می‌آورد بی آن‌که مقاوم باشد |

---

## منابع

**مقاله و مستند**
- ‏Courcelle J, Khodursky A, Peter B, Brown PO, Hanawalt PC (2001). Genetics 158:41–64. https://doi.org/10.1093/genetics/158.1.41
- ‏Cirz RT, et al. (2005). *Inhibition of mutation and combating the evolution of antibiotic resistance.* PLoS Biol 3:e176. https://doi.org/10.1371/journal.pbio.0030176
- ‏Dörr T, Vulić M, Lewis K (2010). *Ciprofloxacin causes persister formation by inducing the TisB toxin in Escherichia coli.* PLoS Biol 8:e1000317. https://doi.org/10.1371/journal.pbio.1000317
- ‏Creecy JP, Conway T (2015). Curr Opin Microbiol 23:133–140. https://doi.org/10.1016/j.mib.2014.11.011
- ‏Langmead B, Salzberg SL (2012). Nat Methods 9:357–359. https://doi.org/10.1038/nmeth.1923
- ‏Liao Y, Smyth GK, Shi W (2014). Bioinformatics 30:923–930. https://doi.org/10.1093/bioinformatics/btt656
- ‏Tierrafría VH, et al. (2022). *RegulonDB 11.0.* Microb Genom 8:000833. https://doi.org/10.1099/mgen.0.000833
- ‏RegulonDB: https://regulondb.ccg.unam.mx · EcoCyc: https://ecocyc.org

**کتاب**
- ‏Snyder L, Peters JE, Henkin TM, Champness W (2013). *Molecular Genetics of Bacteria*, 4th ed. ASM Press. (فصل‌های ترمیم DNA و پاسخ SOS، و تنظیم رونویسی)
- ‏Holmes S, Huber W (2019). *Modern Statistics for Modern Biology.* Cambridge University Press. https://www.huber.embl.de/msmb/

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioconductor for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/bioconductor
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *Regulator for SOS Response: LexA-DNA Complex* (nomunak): https://www.youtube.com/watch?v=2cOoYTooBFA
- ‏YouTube: *Introduction to RNA-seq data analysis* (Chipster Tutorials): https://www.youtube.com/watch?v=fRKwj8igQ0U
- ‏YouTube: *Transcriptomics 1: Introduction to RNA-Seq* (OmicsLogic): https://www.youtube.com/watch?v=g0mmAgETTM8

<sub>همه‌ی دستورها در 2026-10-28 روی سرور دوره (محیط `rnaseq`) اجرا شدند. ژنوم و GFF از NCBI RefSeq ‏(GCF_000005845.2). داده شبیه‌سازی‌شده است؛ ژن‌ها و جهت تغییرشان از مقاله‌های بالا الهام گرفته، ولی اندازه‌ها از ما. DOIها با Crossref و فیلم‌ها با noembed وارسی شدند.</sub>

</div>
