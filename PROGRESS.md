# PROGRESS — Bioinformatics course (Persian, for biologists new to bioinformatics)

Short handoff file. The full narrative of every session (decisions, problems, verified numbers) is in **SESSION_LOG.md** (Persian) — keep it updated; the user wants complete reports. Memory: `course-roadmap-2026-10.md`, `windows-route.md`, `interactive-app-idea.md`, `reply-in-persian.md`.

## 1. Current goal
Write course **v2** (parts 11–22, `NN_V2_…`, plan in `V2_ROADMAP.md`) in STYLE_GUIDE.md format: real dated outputs, known-answer data, ≥5 exercises with «راهنمایی» + solutions, 📺 + 📄 under every technique, منابع = paper + book + Coursera + edX + YouTube (DOIs via Crossref, videos via noembed). Run `_tools/rtl_wrap.py`, `_tools/persian_words.py`, `_tools/check_internal_links.py`. Commit + push every 3 modules / end of part.
**Now (2026-11-10):** part 13 ✅ pushed (`6018e1c`). Windows route ✅ and pushed: 08/01–08/04, 07/01, **all of part 03 (03/01–03/06) and part 04 (04/01–04/04)**. **Order (user, 2026-11-10): lowest incomplete part first → next 06, then 07/02–05, 09, 11, 12, 13; then part 14.** Parts 03/04 Windows files are short (differences only) and link to the Linux lessons. Restructure (parts 11–12 before Linux?) deferred to the end of v2.

**Standing rules:** ALWAYS reply in Persian (user protested English replies). <1 GB RAM runs only (heavier = ✍️ "از مستندات"); never touch `/data/1/genomepipe` or `genomepipe_tools`; never put `$NCBI_API_KEY`, machine email or server IP in lessons/commits; never send the user's email anywhere; never commit `Bioinformatics_Course_ColorCoded.xlsx`, `advanced.odt`, `02_derivative_concept.md`; commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; plain Persian (§8); no shell functions in lessons; Windows route = pure Windows, Windows first, ✍️ for untested Windows steps. User wants very short answers.

## 2. Done so far
- v1 parts 00–09 ✅ (07 written, not run). v2 parts 11 ✅, 12 ✅, 13 ✅ (details in SESSION_LOG).
- **Windows 03/01–03/06 and 04/01–04/04 ✅ (2026-11-10, pushed):** short `00_lesson_windows.md` per module + Windows hints/answers + README rows; Python/R outputs real (server), PowerShell/IDLE/Excel ✍️. Key Windows pitfalls taught: `py` vs `python3`, `.txt` trap, TabError, `"C:\Users"` unicodeescape, `\r\n` changes MD5, cp1252 `'charmap'` error, PS 5.1 quote stripping in `Rscript -e`, `$LASTEXITCODE`, `>` writes UTF-16, ExecutionPolicy.
- **Windows 08/04 ✅ (2026-11-09/10, uncommitted):** `00_lesson_windows.md` complete (§1–5 setup, MAFFT, NJ, IQ-TREE on CTX-M, rooting with `edgelabel = TRUE`; §6 outbreak tree; §7 IQ-TREE on outbreak data; §8 mistakes; summary; refs). Verified on server (MAFFT 7.526, R 4.6.1/ape 5.8.1/ggtree 4.2.0, IQ-TREE 3.1.3 `-T 2 --seed 2026`, Python 3.13):
  - CTX-M: same NJ tree as lesson 1; ML `TN+F+G4`, deep nodes `6.4/42`, `30.5/61`, RF vs NJ 4.
  - Outbreak: same 3 MD5s (core_full.aln `10e36244…`); `outbreak_tree.R` 1.4 s/237 MB; STa ≤ 7 SNP, nearest non-STa 852, 9 close H1–H2 pairs, RF 4, H1-01↔H2-05 1512.
  - ML full aln → JC, 2.7 s/30 MB; STa stem 352.3 (true 350), STb 421.3 (420), H2 `89.3/92`, total 8942 (8890).
  - SNP-only: no correction 382.4; `MFP+ASC` → F81+ASC+R2 0.4 (scale collapses); `-fconst 22896,22692,22752,22770` → 352.3, H2 `89.6/92`.
  - Windows hints under exercises 1–6, "پاسخ‌های مسیر ویندوز" section, module README (status, IQ-TREE 3.1.3, Windows row, step 0), row in `windows/README.md`.
- **Fixed inconsistency (+ASC):** lesson 2 §4 rewritten with real 4-way table (now marked ✅ run), objectives/mistakes/summary/card/glossary (`-fconst`); exercise 6(b); solution 6 (a+b real numbers); lesson 3 command card.
- `simulate_outbreak.py` writes LF (`newline='\n'`) → same MD5 on Windows (uncommitted).
- **Windows 07/01 ✅ (2026-11-10, uncommitted):** `00_lesson_windows.md` (de Bruijn toy, repeats + ideal assembly, coverage one-liner, Shovill in Galaxy ✍️ with GTN MRSA expectations 30 contigs/2,911,349/GC 32.77, `asm_stats.py`, WebQUAST/CheckM2 ✍️). New scripts `debruijn_toy.py`, `asm_stats.py` (stdlib), `repeat_report.py --out` (ideal_contigs.fna MD5 `3b57dbb1…`, 50 contigs, N50 173810; 7.8 s/533 MB). `asm_stats` = seqkit 2.13.0; `--minlen 20000` → N50 178129, NG50 173810 unchanged. Windows hints ex. 1–6, Windows answers, README rows, `windows/README.md` row. WebQUAST (cab.cc.spbu.ru) DNS-unreachable from server.
- Windows 08/03 ✅, 08/02 ✅, 08/01 pilot ✅ (see SESSION_LOG).

## 3. Files changed
- All Windows-route work up to 2026-11-10 is committed and pushed (see git log). Not committed on purpose: `Bioinformatics_Course_ColorCoded.xlsx`, `advanced.odt`, `02_derivative_concept.md`.
- New shared helpers: `windows/get_part01_data.py` (part 01 FASTQ + chr21 + ground_truth, same MD5s), `04_R_Packages/99_scripts_data/04_R_in_Pipelines/scripts/run_all.ps1` (✍️ untested).
- Scratch (may be wiped): `scratchpad/w03`, `scratchpad/w04`, helper `scratchpad/winmod.py` (adds hints/answers/README rows from a JSON spec; inserts README "0." line after "## ترتیب مطالعه"). System R 4.6.1 = `/usr/bin/Rscript` (has DESeq2 1.52.0, ggtree, vegan); env `bio` Python 3.12 has Biopython 1.87, pandas 3.0.5, matplotlib 3.11.1, openpyxl.

## 4. Key decisions and rejected approaches
- 08/04 SNP-only: **rejected** old claim "SNP-only needs `+ASC`" — real run shows `+ASC` collapses branch-length scale on outbreak data (0.4 vs 350); teach full alignment or `-fconst` (identical to full aln). `JC+ASC` total 0.0075 is from an earlier session, not rerun.
- 08/04 Windows: Gubbins has no Windows build → stated, not replaced. MAFFT via `--out` (not `>`: PS 5.1 writes UTF-16). R one-liners → RStudio console lines. `root(..., edgelabel = TRUE)` mandatory (without it supports silently move: `6.4/42` shown as `100/91`).
- 08/04 §6 MD5 output shown as server `md5sum`, labelled so (Get-FileHash prints a table, uppercase).
- Video for §7: YouTube search from server returned nothing → used module-cited Galaxy/Microreact video (`jQVNsyAnDMo`, checked via noembed).
- DESeq2 GSE52778 script kept DESeq2-only (~1.0 GB); edgeR/limma separate. Snakemake in separate env stacked on `rnaseq`. Snakefile explicit named inputs; `--cores 1`. Label swap in GSE52778 reported as "likely". (More in SESSION_LOG.)
- Windows 07/01: SPAdes/Shovill/QUAST/CheckM2 have no Windows build → Galaxy (GTN MRSA tutorial, numbers quoted as GTN's, ✍️) + WebQUAST; light parts in Python. New stdlib scripts instead of seqkit/grep/sed (rejected: requiring seqkit Windows binary). `repeat_report.py --out` added (rejected: separate script) so learners get a known-answer assembly (N50 173810) to test `asm_stats.py`; Linux lessons unchanged.
- Windows 08/02–03: no Windows AMRFinderPlus/ABRicate/MOB-suite → BLAST+ + small stdlib/Biopython scripts, Excel filters, web tools ✍️; `-out`/`Set-Content` instead of `>`.

## 5. Known bugs and caveats (exact messages)
- Auto-mode classifier denied downloading PowerShell 7 (`pwsh` tarball from GitHub) to test `run_all.ps1` → PowerShell steps stay ✍️; don't retry, ask user if testing is wanted.
- PowerShell 5.1 strips inner double quotes in native-command args (`Rscript -e '…"…"…'` → `Error: object 'DESeq2' not found`); lessons teach outer double / inner single quotes.
- `grep -v 'div'` also hides lines with "diversity" — don't use it to skim lessons.
- YouTube search via `_tools/yt_search.sh` returns nothing from server (2026-11-09) → reuse cited videos / WebSearch + noembed.
- WebQUAST: `ccb.uni-saarland.de/quast/` → 302 to `http://cab.cc.spbu.ru/quast/`; that host fails from server (`curl` exit 6, could not resolve host) → check at course end.
- genepi.dk (ResFinder/PlasmidFinder/VirulenceFinder) unreachable from server (timeout 30 s) → check at course end.
- raw.githubusercontent.com throttled (`curl: (28) Operation timed out after 120002 milliseconds with 39282 out of 6572149 bytes received`) → jsDelivr mirror.
- Earlier: two write attempts on 08/04 lesson and two 08/03 tool calls were stopped by a safety classifier; don't repeat the same calls.
- NCBI timeouts (`curl: (28) Failed to connect to ftp.ncbi.nlm.nih.gov:443`) → retry loop.
- Snakemake + `head` under pipefail: `returned non-zero exit status 141` → `awk 'NR <= 20'`. Targets before `--config`.
- ggtree prints `size`/`linewidth` deprecation warnings + "Please report the issue at <https://github.com/YuLab-SMU/ggtree/issues>" — harmless.
- IQ-TREE `+ASC` on SNP-only outbreak data: `WARNING: 18 near-zero internal branches (<0.0001) should be treated with caution` (scale collapse, documented in lesson 2 §4).
- Older caveats (Ensembl 500/503, BioMart GET only, UCSC Turnstile, EDirect SSL stderr, remote BLAST queue, FastQC `--outdir`, Salmon ISR, tximport jsonlite) → SESSION_LOG.

## 6. Next steps (priority order, one session each)
1. Windows route part 06 (4 modules), then 07/02–05 (one `00_lesson_windows.md` + hints/answers + README rows + `windows/README.md` row each). Part 07 heavy tools → Galaxy/web ✍️; light steps with Python.
2. Windows route 09, 11, 12, 13 (one module per session); add 🪟 marker where a module is fully doable on Windows.
3. Optional: rerun `-m JC+ASC` on outbreak SNPs to confirm 0.0075 in lesson 2 §4.
4. v2 part 14 (enrichment; input `de_dex_deseq2.tsv` from 13/03).
5. Later: real runs of v1 part 07 (needs approval); separate courses (`/data/Education/new/`); course-end link/video/book checks with user's VPN; restructure decision; interactive app (memory `interactive-app-idea`, only when asked).
