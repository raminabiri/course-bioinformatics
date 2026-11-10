<div dir="rtl">

# درس (مسیر ویندوز): نخستین گام‌ها در پایتون روی ویندوز

**بخش:** `03_Python` · **ماژول:** `01_Python_Start` · **مسیر:** ویندوز خالص (بی WSL) · **پیش‌نیاز:** [آماده کردن ویندوز](../../windows/README.md) (نصب پایتون) · **زمان:** حدود ۳۰ دقیقه، و سپس [درس اصلی](01_lesson.md) · **ابزار:** Python 3 (ویندوز)، PowerShell، IDLE · **آخرین بازبینی:** 2026-11-10

> ✍️ **وضعیت:** خود پایتون روی ویندوز و لینوکس **یکسان** است. کدهای این درس و درس اصلی روی سرور دوره **اجرا شدند** (2026-11-10) و خروجی‌شان واقعی است. گام‌هایی که تنها به ویندوز مربوط‌اند (پنجره‌ی PowerShell، IDLE، Notepad و پیام‌های ویژه‌ی ویندوز) از **مستندات** نوشته شده‌اند و روی ویندوز آزموده نشده‌اند.

---

## در یک نگاه

این درس کوتاه است. **همه‌ی آموزش پایتون در [درس اصلی](01_lesson.md) است.** این‌جا تنها چیزهایی را می‌گوییم که در ویندوز فرق دارند. پس از آن، درس اصلی را بخوانید و هر جا `python3` دیدید، `py` بنویسید.

| درس اصلی (لینوکس) | مسیر ویندوز |
| :--- | :--- |
| ‏`conda activate bioinfo_course` | لازم نیست؛ پایتون ویندوز را یک بار نصب کرده‌اید (گام ۰) |
| ترمینال با اعلان `$` | ‏**PowerShell** با اعلان `PS C:\Users\…>` |
| ‏`python3` | ‏**`py`** |
| بیرون آمدن: `exit()` یا `Ctrl+D` | ‏`exit()` یا **`Ctrl+Z` و سپس Enter** |
| ‏`nano first.py` | ‏**IDLE** (پیشنهادی) یا Notepad |
| ‏`python3 first.py` | ‏`py first.py`، یا در IDLE کلید **F5** |

**در پایان می‌توانید:** پایتون را در ویندوز باز کنید، اعلان PowerShell را از اعلان پایتون جدا کنید، یک اسکریپت `.py` را درست ذخیره و اجرا کنید، و خطاهای ویژه‌ی ویندوز را بشناسید.

---

## ۱. گام ۰: آیا پایتون نصب است؟

پایتون را در [آماده کردن ویندوز](../../windows/README.md) نصب کرده‌اید. اگر نصب نکرده‌اید، همان‌جا بروید و فراموش نکنید گزینه‌ی **Add python.exe to PATH** را بزنید.

منوی Start را باز کنید، «PowerShell» بنویسید و آن را باز کنید. اعلان چیزی شبیه این است:

<div dir="ltr">

```text
PS C:\Users\Sara>
```

</div>

این اعلان **PowerShell** است، همان کاری که `$` در لینوکس می‌کرد. بنویسید:

<div dir="ltr">

```powershell
py --version
```

</div>

✍️ باید چیزی مانند `Python 3.13.x` ببینید (عدد آخر برای شما فرق دارد).

| اگر دیدید… | یعنی | چاره |
| :--- | :--- | :--- |
| ‏`py : The term 'py' is not recognized…` | پایتون نصب نیست، یا نصب‌کننده `py` را نگذاشته | پایتون را از python.org دوباره نصب کنید |
| با نوشتن `python` یا `python3` **فروشگاه مایکروسافت (Microsoft Store)** باز شد | ویندوز یک «میان‌بر» ساختگی به نام python دارد | ‏`py` بنویسید، یا در تنظیمات ویندوز: Settings ← Apps ← Advanced app settings ← **App execution aliases** و دو گزینه‌ی python را خاموش کنید |

> 📺 **فیلم:** *Python Tutorial for Beginners 1: Install and Setup for Mac and Windows*: https://www.youtube.com/watch?v=YYXdXT2l-Gg (Corey Schafer)
> 📄 **مرجع:** Python documentation, *Using Python on Windows*: https://docs.python.org/3/using/windows.html

---

## ۲. پایتون تعاملی: `py`

در PowerShell بنویسید:

<div dir="ltr">

```powershell
py
```

</div>

✍️ چیزی شبیه این می‌بینید:

<div dir="ltr">

```text
Python 3.13.x (tags/v3.13.x:…, …) [MSC v.19xx 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

</div>

‏`[MSC …] on win32` یعنی این پایتون برای ویندوز ساخته شده است (حتی در ویندوز ۶۴ بیتی همین `win32` را می‌نویسد). اکنون اعلان **`>>>`** است و هر چه بنویسید را پایتون اجرا می‌کند، درست مانند [درس اصلی، بخش ۲](01_lesson.md#۲-پایتون-تعاملی-یک-ماشین‌حساب-هوشمند).

**بیرون آمدن:** `exit()` و Enter. میان‌بر لینوکس (`Ctrl+D`) در ویندوز کار **نمی‌کند**. میان‌بر ویندوز **`Ctrl+Z` و سپس Enter** است.

⚠️ **دو اعلان را با هم اشتباه نکنید:**

| اعلان | چه کسی می‌خواند؟ | چه بنویسید؟ |
| :--- | :--- | :--- |
| ‏`PS C:\Users\…>` | ‏PowerShell | ‏`py`، `cd`، `dir`، `py first.py` |
| ‏`>>>` | پایتون | ‏`len(dna)`، `dna[0:3]`، `exit()` |

✍️ اگر کد پایتون را در PowerShell بنویسید (برای نمونه `len(dna)`)، PowerShell پیامی قرمز با `is not recognized as the name of a cmdlet` می‌دهد. اگر `py first.py` را درون `>>>` بنویسید، پایتون `SyntaxError: invalid syntax` می‌دهد. در هر دو حالت به اعلان نگاه کنید.

### راه دوم: IDLE

پایتون ویندوز برنامه‌ای به نام **IDLE** هم دارد (منوی Start ← «IDLE»). پنجره‌ی نخست آن، **Shell**، همان `>>>` است، با رنگ‌آمیزی کد. هر کدام را خواستید به کار ببرید. خروجی یکی است.

---

## ۳. اکنون درس اصلی را بخوانید

بخش‌های **۲ تا ۵** [درس اصلی](01_lesson.md) (حساب، متغیر، رشته‌ی DNA، f-string) را در `>>>` همراه درس بنویسید. هیچ فرقی با لینوکس ندارند. نمونه‌ای از آن‌ها که روی سرور دوره دوباره اجرا شد:

<div dir="ltr">

```python
>>> dna = "ATGGTTTACTCCTATACCGAGAAAAAACGTATTCGTAAGGATTTTGGTAAACGTCCACAA"
>>> len(dna), dna[:3], round((dna.count("G") + dna.count("C")) / len(dna) * 100, 1)
(60, 'ATG', 36.7)
```

</div>

همان ۶۰ باز، همان `ATG` و همان GC برابر ۳۶٫۷٪ درس اصلی.

سپس به بخش ۴ همین درس برگردید. بخش ۶ درس اصلی (اسکریپت) در ویندوز چند فرق دارد.

---

## ۴. اسکریپت در ویندوز

### ۴.۱ یک پوشه‌ی کار

در PowerShell:

<div dir="ltr">

```powershell
mkdir $HOME\python_course
cd $HOME\python_course
```

</div>

‏`$HOME` پوشه‌ی خانه‌ی شماست (برای نمونه `C:\Users\Sara`)، همانند `~` در لینوکس. همه‌ی اسکریپت‌های بخش ۰۳ را در همین پوشه بگذارید.

### ۴.۲ نوشتن با IDLE (پیشنهادی)

1. ‏IDLE را باز کنید ← منوی **File ← New File**.
2. کد `first.py` را از [درس اصلی، بخش ۶](01_lesson.md#۶-اسکریپت-پایتون) بنویسید (یا کپی کنید).
3. ‏**File ← Save As**، پوشه‌ی `python_course` را بیابید (درون `C:\Users\نام شما`)، نام را `first.py` بگذارید.
4. ‏**Run ← Run Module** یا کلید **F5**. خروجی در پنجره‌ی Shell می‌آید.

**خروجی واقعی** (همان کد، اجرا روی سرور دوره، 2026-11-10):

<div dir="ltr">

```text
length: 60
first codon: ATG
GC content: 36.7%
```

</div>

### ۴.۳ اجرا از PowerShell

اسکریپتی که ذخیره شده، از PowerShell هم اجرا می‌شود. نخست به پوشه‌اش بروید:

<div dir="ltr">

```powershell
cd $HOME\python_course
py first.py
```

</div>

همان سه سطر بالا. فرمان `dir` (همانند `ls` لینوکس) فایل‌های پوشه را نشان می‌دهد.

### ۴.۴ اگر با Notepad می‌نویسید: دام `.txt`

‏Notepad هر فایلی را به‌طور پیش‌فرض با پسوند `.txt` ذخیره می‌کند. ویندوز هم پسوندها را پنهان می‌کند. پس فایلی که نامش را `first.py` می‌بینید، شاید در اصل **`first.py.txt`** باشد. آن‌گاه `py first.py` این خطا را می‌دهد:

<div dir="ltr">

```text
…\python.exe: can't open file 'C:\\Users\\Sara\\python_course\\first.py': [Errno 2] No such file or directory
```

</div>

(همین خطا را روی سرور دوره با نام `first.py.txt` ساختیم. پیام لینوکس همین است، تنها با نشانی لینوکسی.) چاره:
- در Notepad، هنگام **Save As**، گزینه‌ی **Save as type** را روی **All files (\*.\*)** بگذارید و Encoding را **UTF-8** نگه دارید.
- در File Explorer: منوی **View ← Show ← File name extensions** را روشن کنید تا پسوندها را ببینید.
- یا با `dir` در PowerShell نام کامل فایل را ببینید.

> 💡 به همین دلیل IDLE را پیشنهاد می‌کنیم: همیشه `.py` ذخیره می‌کند و رنگ‌آمیزی و تورفتگی خودکار دارد. بعدها اگر خواستید، VS Code هم گزینه‌ی خوبی است.

---

## ۵. خطاهای پایتون: همان پیام‌ها

بخش ۷ [درس اصلی](01_lesson.md#۷-سه-اشتباه-رایج-با-پیام-واقعی) را بخوانید. `NameError`، `TypeError` و `IndexError` در ویندوز همان پیام را دارند. تنها نشانی فایل در Traceback ویندوزی است، برای نمونه `File "C:\Users\Sara\python_course\err.py", line 1`. خط آخر را بخوانید.

---

## ۶. اشتباه‌های رایج در ویندوز

| اشتباه | نشانه | چاره |
| :--- | :--- | :--- |
| نوشتن `python3` | فروشگاه مایکروسافت باز می‌شود، یا `not recognized` | ‏`py` بنویسید (گام ۰) |
| ‏`Ctrl+D` برای بیرون آمدن | چیزی رخ نمی‌دهد | ‏`exit()`، یا `Ctrl+Z` و Enter |
| فایل `first.py.txt` | ‏`can't open file … [Errno 2]` | ‏Save as type: All files؛ پسوندها را نمایان کنید (۴.۴) |
| اجرای `py first.py` در پوشه‌ی نادرست | همان `[Errno 2]` | نخست `cd $HOME\python_course`؛ با `dir` ببینید فایل هست |
| ‏`py first.py` درون `>>>` | ‏`SyntaxError` | نخست `exit()` |

---

## ۷. جمع‌بندی

- در ویندوز به جای `python3` بنویسید **`py`**. بیرون آمدن با `exit()` یا `Ctrl+Z` و Enter است.
- ‏`PS C:\…>` یعنی PowerShell، و `>>>` یعنی پایتون.
- اسکریپت را با **IDLE** بنویسید و با **F5** اجرا کنید، یا در PowerShell `py first.py` بزنید.
- در Notepad مراقب پسوند پنهان `.txt` باشید.
- خود زبان پایتون و پیام‌های خطا در ویندوز و لینوکس یکسان‌اند. پس درس اصلی را بخوانید و به همان عددها می‌رسید.

---

## کارت دستورهای مسیر ویندوز

| می‌خواهم… | ویندوز |
| :--- | :--- |
| نسخه‌ی پایتون | ‏`py --version` |
| پایتون تعاملی / بیرون آمدن | ‏`py` / `exit()` (یا `Ctrl+Z` و Enter) |
| پوشه‌ی کار | ‏`mkdir $HOME\python_course` و `cd $HOME\python_course` |
| فهرست فایل‌ها | ‏`dir` |
| اجرای اسکریپت | ‏`py first.py`، یا F5 در IDLE |

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| ‏PowerShell | خط فرمان ویندوز؛ همانند ترمینال لینوکس |
| ‏`py` | برنامه‌ی آغازگر پایتون در ویندوز (Python Launcher) |
| ‏IDLE | ویرایشگر و Shell ساده‌ای که همراه پایتون نصب می‌شود |
| پسوند (extension) | بخش پایانی نام فایل، مانند `.py` یا `.txt` |
| ‏`$HOME` | پوشه‌ی خانه‌ی کاربر در PowerShell؛ همانند `~` |

---

## منابع

### راهنما و درس رایگان
- ‏Python documentation — *Using Python on Windows*: https://docs.python.org/3/using/windows.html
- ‏Python documentation — *IDLE*: https://docs.python.org/3/library/idle.html
- همه‌ی منابع [درس اصلی](01_lesson.md#منابع) (آموزش رسمی پایتون، Software Carpentry، Rosalind).

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (فصل‌های نخست: آغاز کار با پایتون)

### فیلم‌های آموزشی

**YouTube:**
- Corey Schafer — *Python Tutorial for Beginners 1: Install and Setup for Mac and Windows*: https://www.youtube.com/watch?v=YYXdXT2l-Gg

‏**Coursera و edX:** همان دوره‌های [درس اصلی](01_lesson.md#فیلم‌های-آموزشی).

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. کدهای پایتون در 2026-11-10 روی سرور دوره اجرا شدند. گام‌های ویژه‌ی ویندوز از مستندات‌اند (✍️).

</div>
