<div dir="rtl">

# درس (مسیر ویندوز): پروفایل تاکسونومیک با Kraken2 و Bracken، بی لینوکس

**بخش:** `06_Metagenomics` · **ماژول:** `03_Taxonomic_Functional_Profiling` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [مسیر ویندوز ماژول ۰۲](../02_Host_Removal_Alignment/00_lesson_windows.md) (ریدهای پاک در Galaxy)؛ مفهوم‌ها از درس‌های [۱](01_lesson_kraken.md) و [۲](02_lesson_evaluation.md) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** Kraken2 و Bracken در Galaxy؛ Pavian (وب)؛ Python 3 (`evaluate_profile.py`) · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** ‏`evaluate_profile.py` و یک‌سطری‌های پایتون این درس روی سرور دوره **اجرا شدند** (2026-11-10)، روی خروجی‌های Kraken2 و Bracken درس اصلی؛ خروجی‌شان واقعی است. گام‌های Galaxy و Pavian از **مستندات** نوشته شده‌اند. **پایگاه داده‌ی Galaxy با پایگاه تمرینی درس فرق دارد**، پس عددهای شما فرق خواهند کرد (بخش ۴).

---

## در یک نگاه

| درس لینوکسی | مسیر ویندوز |
| :--- | :--- |
| ‏`build_practice_db.sh` (پایگاه تمرینی ۲۲ ژنومی) | ساختن پایگاه Kraken2 در ویندوز شدنی نیست ← پایگاه‌های **آماده‌ی Galaxy** (بزرگ‌تر و واقعی‌تر) |
| ‏`kraken2 --paired --report …` | ‏**Kraken2** در Galaxy (گام ۱) |
| ‏`bracken -r 125 -l S -t 10` | ‏**Bracken** در Galaxy (گام ۲) |
| ‏`awk` روی `.kraken` و `.kreport` | یک سطر پایتون (گام ۳) |
| ‏`evaluate_profile.py` | **همان اسکریپت** با `py` (گام ۴) |
| ‏Krona / نمودار | ‏**Pavian** در مرورگر، یا Krona در Galaxy (گام ۵) |
| ‏MetaPhlAn و HUMAnN (معرفی) | در Galaxy هست؛ این‌جا تنها بخوانید |

**پیش از خواندن:** از درس ۱ بخش‌های **۱ تا ۳** (داستان؛ k-mer و LCA؛ چرا Bracken) را بخوانید.

---

## ۱. گام ۱: Kraken2 در Galaxy

✍️ از مستندات Galaxy (usegalaxy.eu فهرست بلندتری از پایگاه‌های Kraken2 دارد):

1. ریدهای **پاک** `minigut` (خروجی unaligned ماژول ۰۲) در تاریخچه‌اند.
2. ابزار **Kraken2**:

| در درس (خط فرمان) | در فرم Galaxy |
| :--- | :--- |
| ‏`--paired R1 R2` | ‏**Single or paired reads** ← Paired؛ R1 و R2 |
| ‏`--db profile/kraken2_practice_db` | ‏**Select a Kraken2 database** ← یک پایگاه آماده، برای نمونه **Standard-8** یا **PlusPF-8** (نسخه‌ی تازه) |
| ‏`--confidence 0` | ‏**Confidence** ← 0 (و بار دوم 0.1، درس ۲) |
| ‏`--report …kreport` | ‏**Print a report with aggregrate counts/clade to file** ← Yes |

3. ‏**Run**. دو خروجی: جدول هر رید (`.kraken`) و **گزارش** (`.kreport`). هر دو را دانلود کنید و در `$HOME\meta\profile\kraken` با نام `minigut_c0.kraken` و `minigut_c0.kreport` ذخیره کنید.

---

## ۲. گام ۲: Bracken در Galaxy

ابزار **Bracken** (*Estimate Abundance at Taxonomic Level*):

| در درس | در فرم Galaxy |
| :--- | :--- |
| ‏`-i …kreport` | گزارش Kraken2 گام ۱ |
| ‏`-d DB` و `-r 125` | ‏**Select a kmer distribution** ← همان پایگاه گام ۱، با طول رید نزدیک به ریدهای شما (۱۰۰ یا ۱۵۰) |
| ‏`-l S` | ‏**Level** ← Species |
| ‏`-t 10` | ‏**Threshold** ← 10 |

خروجی را با نام `profile\bracken\minigut_c0.bracken` دانلود کنید. ستون‌هایش همان ستون‌های درس است: `name`، `taxonomy_id`، `taxonomy_lvl`، `kraken_assigned_reads`، `added_reads`، `new_est_reads`، `fraction_total_reads`.

---

## ۳. گام ۳: خواندن خروجی‌ها بی `awk`

درس ۱ (بخش ۵) می‌پرسد ریدهای *E. coli* (نام رید `NC_000913…`) به کدام taxid رسیدند. در ویندوز:

<div dir="ltr">

```powershell
cd $HOME\meta
py -c "from collections import Counter; c = Counter(l.split('\t')[2] for l in open('profile/kraken/minigut_c0.kraken') if l.split('\t')[1].startswith('NC_000913')); [print(n, t) for t, n in c.most_common(8)]"
```

</div>

**خروجی واقعی** (روی خروجی Kraken2 درس اصلی، پایگاه تمرینی):

<div dir="ltr">

```text
8981 562
4909 543
2241 624
1672 623
1312 620
770 564
765 0
300 561
```

</div>

همان خروجی `awk | sort | uniq -c | sort -rn` درس: ‏562 = *E. coli*، ‏543 = Enterobacteriaceae، ‏624 و 623 = *Shigella*… (جدول درس ۱، بخش ۵). ستون ۲ هر سطر `.kraken` نام رید و ستون ۳ taxid است.

**ردیف‌های یک تاکسون در `.kreport`** (جای `awk '$6 ~ /Escherichia|Shigella/'`):

<div dir="ltr">

```powershell
Select-String -Path profile\kraken\minigut_c0.kreport -Pattern "Escherichia|Shigella|Enterobacteriaceae"
```

</div>

‏`Select-String` عبارت باقاعده می‌گیرد؛ `|` همان «یا» است. **یا:** `.kreport` را در Excel باز کنید (جداکننده Tab)؛ ستون ۶ نام، ستون ۱ درصد، ستون ۲ شمار ریدهای آن شاخه است.

---

## ۴. گام ۴: ارزیابی با پاسخ معلوم

‏`evaluate_profile.py` پایتون ساده است و در ویندوز همان‌گونه کار می‌کند:

<div dir="ltr">

```powershell
Copy-Item $HOME\course-bioinformatics-main\06_Metagenomics\99_scripts_data\data\ground_truth_species.tsv .
$S = "$HOME\course-bioinformatics-main\06_Metagenomics\99_scripts_data\03_Taxonomic_Functional_Profiling\scripts"
py $S\evaluate_profile.py profile\bracken\minigut_c0.bracken minigut
```

</div>

**خروجی واقعی روی Bracken درس اصلی** (پایگاه تمرینی، `--confidence 0`):

<div dir="ltr">

```text
species                                  truth  estimate  status
Bacteroides fragilis                    57.83%    54.06%  TP
Escherichia coli                        42.17%    27.25%  TP
Shigella sonnei                          0.00%     8.10%  FP
Shigella flexneri                        0.00%     5.53%  FP
Phocaeicola dorei                        0.00%     3.21%  FP
Escherichia fergusonii                   0.00%     1.68%  FP
Klebsiella pneumoniae                    0.00%     0.08%  FP
Salmonella enterica                      0.00%     0.06%  FP
Bacteroides thetaiotaomicron             0.00%     0.03%  FP

species predicted=9  TP=2  FP=7  FN=0
precision=0.222  recall=1.000  F1=0.364  Bray-Curtis=0.187
```

</div>

**با Bracken از Galaxy چه می‌بینید؟** ✍️ پایگاه Galaxy (Standard یا PlusPF) **هزاران** گونه دارد، نه ۲۲. پس انتظار داشته باشید:
- ‏**FP بیشتر**، بیشترشان با درصد بسیار کم (زیر ۰٫۱٪)؛ همان «دم بلند» درس ۲. گزینه‌ی `--min-frac 0.01` (درس ۲، بخش ۵) بیشترشان را کنار می‌گذارد.
- ‏*Shigella* باز هم می‌آید: *E. coli* و *Shigella* از دید ژنوم یک گونه‌اند (درس ۱، بخش ۶). این یافته‌ی اصلی درس، با هر پایگاهی، **می‌ماند**.
- ‏*B. fragilis* و *E. coli* (TP) باید هر دو دیده شوند (recall = ۱).

> این فرق خودش درسی است: **پاسخ یک پروفایل به پایگاه داده بستگی دارد.** در بند روش‌های مقاله نام و تاریخ پایگاه را بنویسید (در Galaxy: آیکون ℹ️ خروجی).

---

## ۵. گام ۵: نمودار با Pavian یا Krona

- ‏✍️ ‏**Pavian** (برنامه‌ی وب برای گزارش‌های Kraken): https://fbreitwieser.shinyapps.io/pavian/ ← Upload ← یک یا چند `.kreport`. نمودار Sankey و جدول مقایسه‌ی نمونه‌ها. (اگر نشانی کار نکرد، Pavian بسته‌ی R هم هست و روی ویندوز با RStudio اجرا می‌شود؛ راهنمای GitHub آن: https://github.com/fbreitwieser/pavian.)
- ‏**Krona** در Galaxy: ابزار *Krona pie chart* روی خروجی `.kraken` (نوع ورودی: Tabular/Kraken). نمودار دایره‌ای تعاملی در مرورگر.

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| پایگاه Bracken با طول رید نادرست | درصدها کمی جابه‌جا | ‏k-mer distribution نزدیک به طول ریدهای شما |
| دادن `.kreport` به `evaluate_profile.py` | ‏`KeyError: 'taxonomy_id'` | خروجی **Bracken** (`.bracken`) را بدهید |
| سنجیدن عددهای Galaxy با عددهای درس | «درس اشتباه است!» | پایگاه‌ها فرق دارند (بخش ۴)؛ الگو را بسنجید، نه رقم‌ها را |
| نام فایل Galaxy با `[ ]` در PowerShell | ‏`Cannot find path` | پیش از کار نام فایل را ساده کنید (`[` و `]` در PowerShell نویسه‌ی ویژه‌اند) |

✍️ پیام‌های جدول جز سطر دوم از مستندات‌اند. سطر دوم: `evaluate_profile.py` ستون `taxonomy_id` را می‌خواهد که تنها در خروجی Bracken هست.

---

## ۷. جمع‌بندی

- ‏Kraken2 و Bracken در ویندوز: Galaxy، با پایگاه‌های آماده.
- خواندن خروجی‌ها: یک سطر پایتون (`Counter`)، `Select-String`، Excel.
- ارزیابی: همان `evaluate_profile.py`؛ با پایگاه بزرگ‌تر، FPهای کم‌درصد بیشتر و همان دام *Shigella*.
- نمودار: Pavian (وب) یا Krona (Galaxy).

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| ‏taxid ریدهای یک مبدأ | ‏`py -c "from collections import Counter; …"` (گام ۳) |
| ردیف‌های یک تاکسون | ‏`Select-String -Path s.kreport -Pattern "Escherichia\|Shigella"` |
| ارزیابی | ‏`py $S\evaluate_profile.py s.bracken minigut [--min-frac 0.01]` |
| نمودار | ‏Pavian (وب) / Krona (Galaxy) |

---

## منابع

### مقاله
- ‏Wood DE, Lu J, Langmead B (2019). *Improved metagenomic analysis with Kraken 2.* Genome Biology 20:257. https://doi.org/10.1186/s13059-019-1891-0
- ‏Lu J, Breitwieser FP, Thielen P, Salzberg SL (2017). *Bracken: estimating species abundance in metagenomics data.* PeerJ Computer Science 3:e104. https://doi.org/10.7717/peerj-cs.104
- ‏Breitwieser FP, Salzberg SL (2020). *Pavian: interactive analysis of metagenomics data for microbiome studies and pathogen identification.* Bioinformatics 36:1303–1304. https://doi.org/10.1093/bioinformatics/btz715

### راهنما و درس رایگان
- ‏Galaxy Training — *Taxonomic Profiling and Visualization of Metagenomic Data*: https://training.galaxyproject.org/training-material/topics/microbiome/tutorials/taxonomic-profiling/tutorial.html
- همه‌ی منابع درس‌های [۱](01_lesson_kraken.md) و [۲](02_lesson_evaluation.md).

### فیلم‌های آموزشی
همان فیلم‌های درس‌های اصلی؛ آموزش Galaxy بالا فیلم همراه دارد.

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. Galaxy و Pavian از مستندات‌اند (✍️).

</div>
