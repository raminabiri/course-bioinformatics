<div dir="rtl">

# پاسخ تشریحی: بازتولید یک یافته‌ی منتشرشده

همه‌ی خروجی‌ها واقعی‌اند (Snakemake 9.25.2، R 4.5.3، DESeq2 1.50.2، Python 3.15 و pandas؛ روی سرور دوره، 2026-10-28).

---

## پاسخ ۱: ‏Snakemake چه چیزی را دوباره می‌زند؟

<div dir="ltr">

```bash
rm results/paper_check.txt
snakemake -s $P/04_Reuse_Public_Data/workflow/Snakefile --cores 1 -n --config scripts=$P | grep -A6 "^Job stats"
snakemake -s $P/04_Reuse_Public_Data/workflow/Snakefile --cores 1 --config scripts=$P > /dev/null 2>&1   # bring it back
snakemake -s $P/04_Reuse_Public_Data/workflow/Snakefile --cores 1 -n --forcerun deseq2 --config scripts=$P | grep -A7 "^Job stats"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
Job stats:
job            count
-----------  -------
all                1
paper_check        1
total              2

Job stats:
job            count
-----------  -------
all                1
deseq2             1
paper_check        1
total              3
```

</div>

- (الف) تنها `paper_check` (و قاعده‌ی جمع‌کننده‌ی `all`). ‏Snakemake از خروجی‌های خواسته‌شده **رو به عقب** می‌رود و تنها گام‌هایی را می‌زند که خروجی‌شان نیست یا کهنه است.
- (ب) ‏`deseq2` و هر گامی که به خروجی آن **وابسته** است (`paper_check`). ‏`check_labels` به deseq2 وابسته نیست (مستقیم از `data/` می‌خواند)، پس دست نمی‌خورد. ‏`download` هم پیش از deseq2 است، نه پس از آن.

---

## پاسخ ۲: امتیاز گلوکوکورتیکوئید را بخوانید

<div dir="ltr">

```bash
column -t -s$'\t' results/labels.tsv
```

</div>

جدول همان است که در درس دیدید (ستون‌ها یک خانه جابه‌جا نشان داده می‌شوند، چون سطر سرخط نام سطر ندارد). برای پرسش ۲، تغییر log2 CPM هر ژن نشانگر نسبت به نمونه‌ی بی‌تیمار همان فرد را با pandas گرفتیم:

<div dir="ltr">

```python
import pandas as pd, numpy as np
c = pd.read_csv("data/counts.tsv.gz", sep="\t", index_col=0); c.index = c.index.astype(str)
l = np.log2(c / c.sum() * 1e6 + 1)
m = {"2289": "FKBP5", "1831": "TSC22D3", "7704": "ZBTB16", "5187": "PER1",
     "28999": "KLF15", "83716": "CRISPLD2", "1843": "DUSP1"}
pairs = {"N61311_Alb": ("GSM1275864", "GSM1275862"), "N061011_Alb": ("GSM1275876", "GSM1275874"),
         "N052611_AlbDex": ("GSM1275869", "GSM1275866"), "N080611_AlbDex": ("GSM1275873", "GSM1275870")}
d = pd.DataFrame({k: (l.loc[list(m), a] - l.loc[list(m), b]).values for k, (a, b) in pairs.items()}, index=m.values())
print(d.round(2).to_string())
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
          N61311_Alb  N061011_Alb  N052611_AlbDex  N080611_AlbDex
FKBP5           0.08         0.02            1.45            0.45
TSC22D3         0.20        -0.06            0.74            0.34
ZBTB16          0.23         0.27            3.06            2.31
PER1            0.53         1.20            1.75            0.94
KLF15          -0.02         0.48            1.57            1.00
CRISPLD2       -0.12         0.29            1.27            0.49
DUSP1          -0.20        -0.13            0.29            0.61
```

</div>

۱. در فردهای جور، امتیاز آلبوترول از **PER1** می‌آید (۰٫۵۳ و ۱٫۲۰): ‏PER1 با cAMP هم روشن می‌شود و آلبوترول cAMP را بالا می‌برد (12/06). ژن‌های دیگر نزدیک صفرند. امتیاز میانگین هفت ژن است، پس یک ژن آن را کمی بالا می‌برد.

۲. گمان نخست ما این بود که این هم اثر cAMP است. داده **نه** می‌گوید: ‏**ZBTB16**، ژنی که کمابیش تنها با گلوکوکورتیکوئید روشن می‌شود، در این دو نمونه ۳٫۰۶ و ۲٫۳۱ بالا رفته (در دگزامتازون کامل نزدیک به ۷؛ در آلبوترول فردهای جور ۰٫۲). پس در این نمونه‌ها **اندکی** اثر گلوکوکورتیکوئید هست. گمان‌های سنجیدنی: (الف) آلودگی اندک با دگزامتازون در کشت یا آمیختگی اندک RNA دو نمونه؛ (ب) کورتیزول در سرم محیط کشت؛ (ج) برچسب‌ها جابه‌جا نیستند و نمونه‌ی «ترکیب» به هر دلیلی دگزامتازون کمتری گرفته. ولی (ج) توضیح نمی‌دهد چرا نمونه‌ی «آلبوترول» امتیاز کامل دگزامتازون (۳٫۵۷ و ۲٫۸۶) دارد. پس جابه‌جایی همچنان ساده‌ترین توضیح برای آن دو نمونه است، و این نمونه‌ها داستانی دارند که تنها آزمایشگاه می‌داند. **درس:** گمان خود را با داده‌ی ریزتر بسنجید؛ ما خودمان در نسخه‌ی نخست درس گمان cAMP را نوشته بودیم و این بررسی آن را رد کرد.

۳. سطح پایه‌ی هر ژن از فرد به فرد فرق دارد (در 13/03 دیدید فرد ۲۶٫۶٪ گوناگونی را می‌سازد). عدد خام امتیاز، تفاوت **فردها** و **تیمار** را با هم می‌آمیزد؛ تفریق نمونه‌ی بی‌تیمار همان فرد، همان کار `~ cell + …` در DESeq2 است.

---

## پاسخ ۳: ‏۳۱۶ ژن برتر ما چه‌اند؟

<div dir="ltr">

```bash
tail -n +2 results/de_dex_deseq2.tsv | awk -F'\t' '$6 != "NA"' | sort -t$'\t' -k6,6g \
  | awk -F'\t' 'NR <= 316 {if ($4 > 0) up++; else down++; if ($4 > 1 || $4 < -1) big++} END {print "up", up, "down", down, "|log2FC|>1", big}'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
up 202 down 114 |log2FC|>1 280
```

</div>

‏۲۰۲ بالا و ۱۱۴ پایین؛ ‏۲۸۰ از ۳۱۶ (‏۸۹٪) تغییری بیش از دو برابر دارند. ژن‌های با کوچک‌ترین padj بیشتر تغییرهای **بزرگ** و پرشمارند؛ بالا رفتن بیشتر ژن‌ها با کار دگزامتازون (روشن کردن ژن از راه گیرنده‌ی گلوکوکورتیکوئید) جور است. اگر مقاله (۳۱۶ ژن) روشی محافظه‌کارتر داشته، چنین فهرستی شبیه فهرست آن است.

---

## پاسخ ۴: یک قاعده‌ی تازه

نخست با `head -20`:

<div dir="ltr">

```python
rule top_genes:
    input: "results/de_dex_deseq2.tsv"
    output: "results/top20_up.txt"
    shell:
        "tail -n +2 {input} | awk -F'\\t' '$6 < 0.05 && $5 > 0' | sort -t$'\\t' -k5,5gr | head -20 | cut -f2 > {output}"
```

</div>

**خروجی واقعی (خطا):**

<div dir="ltr">

```
Command 'set -euo pipefail;  tail -n +2 results/de_dex_deseq2.tsv | awk -F'\t' '$6 < 0.05 && $5 > 0' | sort -t$'\t' -k5,5gr | head -20 | cut -f2 > results/top20_up.txt' returned non-zero exit status 141.
```

</div>

‏Snakemake پیش از هر دستور `set -euo pipefail` می‌گذارد. ‏`head` پس از ۲۰ سطر بسته می‌شود؛ `sort` که هنوز می‌نویسد سیگنال SIGPIPE می‌گیرد (کد ۱۲۸ + ۱۳ = ۱۴۱)، و با `pipefail` کل لوله شکست‌خورده به شمار می‌آید. ‏Snakemake خروجی ناقص را هم پاک می‌کند. درست‌شده: `head -20` ← `awk 'NR <= 20'` (‏awk تا پایان می‌خواند).

<div dir="ltr">

```bash
snakemake -s Snakefile results/top20_up.txt --cores 1 --config scripts=$P > ex4.log 2>&1
tail -3 ex4.log | head -1; tr '\n' ' ' < results/top20_up.txt; echo
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
1 of 1 steps (100%) done
ALOX15B ZBTB16 LOC101928819 PRODH STEAP4 NA ANGPTL7 FAM107A LGI3 SPARCL1 RASL11B KLF15 TSPAN8 GUCY2D RMEL3 ADRA1B FKBP5 MARCHF10-AS1 SLC16A12 ITGA10 
```

</div>

- ‏`NA`: ‏Gene ID این سطر در جدول `gene_info` امروز نیست. در کل جدول، ‏**۴۱** ژن معنادار نام `NA` دارند. داده‌ی GEO با آنوتیشن سال‌ها پیش ساخته شده و NCBI از آن پس برخی شناسه‌ها را بازنشسته یا ادغام کرده است.
- نمونه: GeneID 102724788 (‏LOC102724788) در NCBI Gene اکنون «replaced» است با **5625** یعنی **PRODH**. پس این سطر و سطر PRODH شاید یک ژن باشند که دو بار شمرده شده‌اند.
- ‏`LOC…`: ژن‌هایی که هنوز نام رسمی ندارند (11/02).
- ‏FKBP5، ZBTB16 و KLF15 در فهرست‌اند، همان ژن‌های شناخته‌شده.

**درس:** آنوتیشن هم مانند برچسب‌ها کهنه می‌شود؛ پیش از تفسیر، شناسه‌های NA و جایگزین‌شده را بازبینی کنید (برای نمونه با `gene_history` در FTP همان NCBI).

---

## پاسخ ۵ (فکری): نامه به نویسندگان

یک نمونه (به انگلیسی، چون نامه به آن‌ها می‌رود):

> Dear Dr. Himes,
> While reanalysing GSE52778, we noticed that in donors N052611 and N080611 the samples labelled "Albuterol" (GSM1275868, GSM1275872) show a strong glucocorticoid response (mean log2 change of seven GR target genes vs the donor's untreated sample: 3.57 and 2.86, similar to the dexamethasone samples), while the samples labelled "Albuterol + Dexamethasone" (GSM1275869, GSM1275873) show a weak one (1.45 and 0.88). In the other two donors the pattern is as expected. Swapping the two labels in these donors raises the number of DE genes for the combination from 421 to 3,593. We cannot tell from the data alone whether this is a labelling issue; could you check the lab records? The dexamethasone-only results of the paper are not affected. Our code is available at [link].

- **چه می‌آوریم:** شناسه‌ی دقیق نمونه‌ها، عددها، روش (چند جمله)، مقایسه با فردهای جور، کد.
- **چه نمی‌گوییم:** «شما اشتباه کرده‌اید» یا «داده نادرست است». ما **ناهمخوانی** دیده‌ایم، نه علت را. نامه نیز می‌گوید یافته‌ی اصلی مقاله دست نخورده است.
- **چگونه بسنجند:** دفتر آزمایشگاه، برچسب لوله‌ها، و در صورت داشتن RNA مانده، qPCR برای FKBP5 یا ZBTB16 در آن چهار نمونه.
- ‏GEO برای اصلاح فراداده، از نویسنده‌ی ثبت‌کننده‌ی سری می‌خواهد؛ پس نامه نخست به نویسندگان می‌رود.

---

## پاسخ ۶ (فکری): ‏۳۱۶ یا ۴۷۴۳؟

- **به «مقاله اشتباه است»:** نه. هر هفت ژن نام‌برده بازتولید شدند، با همان جهت. شمار کمتر یعنی روش **محافظه‌کارتر** (یا کم‌توان‌تر)، نه یافته‌ی نادرست. ‏۳۱۶ ژن برتر ما همه padj کمتر از ۵×۱۰⁻¹⁹ دارند؛ این ژن‌ها را هر روشی می‌یابد.
- **به «تحلیل تو اشتباه است»:** نه به این آسانی. سه روش (DESeq2، edgeR، limma) در 13/03 ‏۴۷۰۰ تا ۵۶۰۰ ژن دادند و ۴۶۲۶ مشترک. با هشت نمونه و طرح جفتی، هزاران ژن با تغییر **کوچک** ولی مطمئن یافتنی‌اند. «معنادار» یعنی تغییر صفر نیست، نه این‌که بزرگ است.
- **آزمایش‌ها روی همین داده:** (۱) ‏`~dex` به جای `~cell+dex` (در 13/03: ‏۳۲۲۰)؛ (۲) ‏`lfcThreshold = 1` در `results` (آزمون «تغییر بیش از دو برابر»)؛ (۳) فیلتر سخت‌تر ژن‌های کم‌بیان؛ (۴) روش و نسخه‌ی ابزار ۲۰۱۴، اگر بخش روش مقاله آن را نام برده (متن کامل در PMC4057123)؛ (۵) آنوتیشن کهنه‌تر. هر کدام را جدا عوض کنید و ببینید شمار چقدر به ۳۱۶ نزدیک می‌شود. این همان روش «یک متغیر در هر بار» در آزمایشگاه است.

</div>
