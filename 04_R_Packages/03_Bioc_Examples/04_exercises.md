<div dir="rtl">

# تمرین‌ها: DESeq2، vegan و ggtree

پیش از آغاز، درس‌های ۱ تا ۳ را اجرا کرده باشید تا فایل‌های `~/r_practice/deseq2`، `~/r_practice/vegan` و `~/r_practice/tree` آماده باشند.

<div dir="ltr">

```bash
conda activate r_packages
P=~/course-bioinformatics-main/04_R_Packages/99_scripts_data

> **مسیر ویندوز:** نخست [مسیر ویندوز](00_lesson_windows.md) را بخوانید؛ پوشه‌ها `$HOME\r_practice\deseq2`، `…\vegan` و `…\tree`. به جای `awk` و `cut`، یک سطر pandas یا فیلتر Excel؛ به جای `grep`، ‏`Select-String`؛ به جای `2>/dev/null`، ‏`2>$null`. زیر راهنمایی هر تمرین یک بند **ویندوز** آمده است. پاسخ‌های ویندوزی در پایان [پاسخ‌ها](05_solutions.md) هستند.
```

</div>

---

## تمرین ۱: خلاصه‌ی DESeq2
> **راهنمایی:** درس ۱، بخش ۴ (خلاصه) و بخش ۵ (گزینش با awk). ستون ۷ = padj، ستون ۳ = log2FoldChange.
> **ویندوز:** سطر pandas بخش ۲ [مسیر ویندوز](00_lesson_windows.md) همین شمارش‌ها را می‌دهد؛ یا فیلتر Excel روی ستون‌های `padj` و `log2FoldChange`.

در `~/r_practice/deseq2`: (الف) چند ژن در RifR معنادار **بیشتر** بیان شده‌اند؟ (ب) چند ژن معنادارند و دست‌کم **۴ برابر کاهش** یافته‌اند؟

---

## تمرین ۲: یک ژن را دنبال کنید
> **راهنمایی:** درس ۱، بخش ۵. `grep -w` برای یافتن واژه‌ی کامل (بخش ۰۱). جدول بخش ۲ برای ترجمه‌ی log2FoldChange.
> **ویندوز:** ‏`Select-String -Path deseq2_results.tsv -Pattern "\bb3357\b"`، همین برای `counts.tsv`، و `Select-String -Path truth.tsv -Pattern "\bcrp\b"`.

ژن **crp** (locus tag: `b3357`) را در `deseq2_results.tsv` و `counts.tsv` پیدا کنید. (الف) log2FoldChange و padj آن چیست؟ معنادار است؟ (ب) کمابیش چند برابر شده است؟ (ج) این ژن در `truth.tsv` هست؟ تغییر واقعی‌اش چقدر بود و DESeq2 چقدر نزدیک شد؟

---

## تمرین ۳: rpoB چه شد؟
> **راهنمایی:** locus tag ژن rpoB را از GFF بخش ۰۱ بگیرید (`grep -w rpoB … | grep -o "locus_tag=b[0-9]*"`). کادر هشدار آغاز درس ۱ را دوباره بخوانید.
> **ویندوز:** ‏`Select-String -Path $HOME\course\ecoli_k12.gff -Pattern "Name=rpoB;" | Select-Object -First 1` و در سطر، `locus_tag=b…` را بخوانید.

آیا در این داده، بیان خود **rpoB** در سویه‌ی مقاوم تغییر کرده است؟ از این پاسخ چه نتیجه‌ی **زیستی** می‌توان گرفت؟

---

## تمرین ۴: آستانه‌ی سخت‌گیرانه‌تر
> **راهنمایی:** درس ۱، کادر کنجکاوها؛ ماژول ۰۲، بخش ۶ (کپی + `sed -i`). `compare_truth.py` ورودی سوم اختیاری برای آستانه دارد.
> **ویندوز:** ‏`Copy-Item` و سپس `(Get-Content my_deseq2.R) -replace 'padj_cutoff <- 0.05', 'padj_cutoff <- 0.01' | Set-Content my_deseq2.R`؛ اجرا با `2>$null | Select-String -Pattern "adjusted" -Context 0,3`؛ سپس `py $P\03_Bioc_Examples\scripts\compare_truth.py strict_results.tsv truth.tsv 0.01`.

در یک کپی از `run_deseq2.R`، مقدار `padj_cutoff` را از `0.05` به `0.01` برسانید و با پیشوند `strict` اجرا کنید. (الف) خلاصه چند ژن up و down می‌دهد؟ (ب) با `compare_truth.py … 0.01` بسنجید: چند ژن درست، چند هشدار کاذب، چند از دست‌رفته؟ (ج) در برابر آستانه‌ی ۰٫۰۵، چه به دست آوردید و چه از دست دادید؟

---

## تمرین ۵: سطح طبقه‌بندی
> **راهنمایی:** درس ۲، بخش‌های ۴ و ۵.
> **ویندوز:** همان `Rscript … diversity.R` با `2>$null`؛ جدول‌ها با ``Import-Csv … -Delimiter "`t" | Format-Table``.

در `~/r_practice/vegan`، تنوع را یک بار در سطح موجود و یک بار در سطح جنس حساب کرده‌اید. (الف) کدام نمونه **یکنواخت‌تر** است و چرا؟ (ب) چرا غنای `minigut` در دو سطح یکی است ولی غنای `minigut_sample2` فرق دارد؟ (ج) چرا Bray–Curtis در سطح موجود دقیقاً ۱ شد؟

---

## تمرین ۶: نمونه‌ی همسان
> **راهنمایی:** درس ۲، بخش ۲ (معنای ۰ و ۱ در Bray–Curtis). دستور awk زیر یک کپی از `minigut` با نام تازه می‌سازد.
> **ویندوز:** به جای `awk`، این سطر پایتون همان `three.tsv` را می‌سازد (روی سرور بایت‌به‌بایت همان خروجی awk): `py -c "L = open('ground_truth.tsv').read().splitlines(); open('three.tsv', 'w', newline='\n').write(''.join(l + '\n' + (('minigut_copy' + l[7:] + '\n') if i and l.split('\t')[0] == 'minigut' else '') for i, l in enumerate(L)))"`. یا در Excel سطرهای `minigut` را کپی کنید، نام را `minigut_copy` بگذارید و با Save As ← **Text (Tab delimited)** ذخیره کنید.

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} {print} NR>1 && $1=="minigut" {$1="minigut_copy"; print}' \
    ground_truth.tsv > three.tsv
```

</div>

‏`diversity.R` را روی `three.tsv` در سطح جنس اجرا کنید. پیش از اجرا پیش‌بینی کنید: Bray–Curtis میان `minigut` و `minigut_copy` چند است؟ میان `minigut_copy` و `minigut_sample2`؟ سپس اجرا و بسنجید.

---

## تمرین ۷: درخت چهاربرگی
> **راهنمایی:** درس ۳، بخش ۲ (خواندن Newick) و بخش ۴ (اجرا).
> **ویندوز:** ‏`Set-Content four.nwk "(((A:1,B:1):1,C:2):1,D:3);"` و سپس `Rscript $P\03_Bioc_Examples\scripts\plot_tree.R four.nwk four.png 2>$null`.

این درخت را در فایل `four.nwk` بنویسید و رسم کنید:

<div dir="ltr">

```text
(((A:1,B:1):1,C:2):1,D:3);
```

</div>

(الف) اسکریپت چند برگ گزارش می‌کند؟ (ب) نزدیک‌ترین خویشاوند C کدام است؟ (ج) فاصله‌ی A تا D روی درخت چقدر است؟

---

## تمرین ۸ (فکری): «DESeq2 گفت تغییر نکرده»
> **راهنمایی:** درس ۱، بخش ۷ و نمودار MA.
> **ویندوز:** ‏`Select-String -Path $HOME\r_practice\deseq2\missed.tsv -Pattern "\bybiB\b"`.

همکارتان می‌گوید: «ژن ybiB در سویه‌ی مقاوم تغییری نکرده، چون padj آن ۰٫۱۶ است.» با نگاه به `missed.tsv`، به او چه پاسخی می‌دهید؟ دو راه برای اینکه آزمایش بعدی چنین ژن‌هایی را از دست ندهد پیشنهاد کنید.

</div>
