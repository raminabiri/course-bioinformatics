# PROGRESS — Bioinformatics course (Persian, for biologists new to bioinformatics)

Short handoff file. The full narrative of every session (decisions, problems, verified numbers) is in **SESSION_LOG.md** (Persian) — keep it updated; the user wants complete reports. Memory: `course-roadmap-2026-10.md`, `windows-route.md`, `interactive-app-idea.md`.

## 1. Current goal
Write course **v2** (parts 11–22, `NN_V2_…`, plan in `V2_ROADMAP.md`) in STYLE_GUIDE.md format: real dated outputs, known-answer data, ≥5 exercises with «راهنمایی» + solutions, 📺 + 📄 under every technique, منابع = paper + book + Coursera + edX + YouTube (DOIs via Crossref, videos via noembed). Run `_tools/rtl_wrap.py`, `_tools/persian_words.py`, `_tools/check_internal_links.py`. Commit + push every 3 modules / end of part.
**Now (2026-11-09):** part 13 ✅ pushed (`6018e1c`). Windows route: 08/01 ✅, 08/02 ✅ (`ab8e162`), 08/03 ✅ (2026-11-09); **next 08/04**, then 07, 06, 09, 03, 04, 11, 12, 13; then part 14. Restructure (parts 11–12 before Linux?) deferred to the end of v2.

**Standing rules:** <1 GB RAM runs only (heavier = ✍️ "از مستندات"); never touch `/data/1/genomepipe` or `genomepipe_tools`; never put `$NCBI_API_KEY`, machine email or server IP in lessons/commits; never send the user's email anywhere; never commit `Bioinformatics_Course_ColorCoded.xlsx`, `advanced.odt`; commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; plain Persian (§8); no shell functions in lessons; Windows route = pure Windows, Windows first, ✍️ for untested Windows steps. User wants very short answers (yes/no when possible).

## 2. Done so far
- v1 parts 00–09 ✅ (07 written, not run). v2 parts 11 ✅, 12 ✅ (details in SESSION_LOG).
- Windows 08/03 ✅ (2026-11-09): `00_lesson_windows.md` (pEK499 via `py` urllib/efetch; BLAST known genes → blaCTX-M-15 100%, tet(A) 98%; ResFinder web ✍️; PlasmidFinder db via jsDelivr, 14 rows, 90/60 filter in Excel → IncFIA + IncFII; `gb_context.py` on NCBI .gb: 11 IS, old 2008 names, catB4/TEM boundaries run into IS (distance 0) vs AMRFinderPlus PARTIALX — teaching point; cas genes via `py -c` csv one-liner; `find_crispr.py` 2 arrays / 18 spacers; CRISPRCasFinder web ✍️), new `scripts/gb_context.py`, Windows hints + answers, README rows. genepi.dk unreachable from server (timeout).
- Windows 08/02 ✅: `00_lesson_windows.md`, new `scripts/vfdb_summary.py`, Windows hints + answers; VFDB via jsDelivr mirror (raw.githubusercontent.com throttled).
- Windows pilot 08/01 ✅ (`a86c5af`): `windows/README.md`, `windows/get_k12_genome.py`, `00_lesson_windows.md`, `check_qrdr.py`.
- Part 13 (`b58e594`, `30462bf`, pushed):
  - 01 design/QC, 02 alignment/quantification (shared simulated data, `envs/rnaseq.yml`).
  - 03 DESeq2/edgeR/limma: simulated 8/8 genes, 0 FP; GSE52778 `~cell+dex` 4,743 genes, Atlas r = 0.893.
  - 04 Snakemake reproduction of Himes 2014: 7/7 named genes, 4,743 vs 316; **likely label swap** Albuterol ↔ Alb+Dex in donors N052611, N080611 (combination 421 → 3,593 genes). ZBTB16 up 2.3–3.1 in the "Alb+Dex" samples of those donors → not pure albuterol; left open in lesson.
  - 12/06 solution 2 now points to the 13/04 evidence.
  - 05 ✅ (exercises + solutions 2026-11-05, real reruns; same MD5/output as lesson): `simulate_bacterial.py` (K-12 RefSeq GCF_000005845.2, 6 × 400k SE 75 bp, dUTP, seed 13, SOS up, S10 operon −1.5, rRNA 6–15%), `de_bacterial.R`, `data/make_data.sh`, `05_Bacterial_RNAseq/01_lesson.md`. Results: Bowtie2 100% (10.5% multi), `-s 2` correct (s=1: 1,161 assigned), DESeq2 21 genes, all 12 SOS genes, 18/25 known, 3 FP (yagP, cmoM, yiiS), 867 MB, 6 s.

## 3. Files changed (this session)
- `13_V2_RNAseq_Transcriptomics/03_Differential_Expression/{README,01_lesson,02_exercises,03_solutions}.md`, `99_scripts_data/03_Differential_Expression/{scripts,data,images}`.
- `13_V2_RNAseq_Transcriptomics/04_Reuse_Public_Data/{README,01_lesson,02_exercises,03_solutions}.md`, `99_scripts_data/04_Reuse_Public_Data/{workflow/Snakefile,scripts/check_labels.R,scripts/paper_check.py}`.
- `13_V2_RNAseq_Transcriptomics/05_Bacterial_RNAseq/{README,01_lesson,02_exercises,03_solutions}.md`, `99_scripts_data/05_Bacterial_RNAseq/{scripts/simulate_bacterial.py,scripts/de_bacterial.R,data/make_data.sh}`.
- `12_V2_Global_Databases_Browsers/06_Expression_Cancer_Portals/03_solutions.md` (solution 2).
- 08/03 Windows: `08_AMR_Virulence_Phylogeny/03_Mobile_Elements_CRISPR/{00_lesson_windows,03_exercises,04_solutions,README}.md`, `99_scripts_data/03_Mobile_Elements_CRISPR/scripts/gb_context.py`, `windows/README.md`, `SESSION_LOG.md`.
- 08/02 Windows: `08_AMR_Virulence_Phylogeny/02_Virulence_Factors/{00_lesson_windows,03_exercises,04_solutions,README}.md`, `99_scripts_data/02_Virulence_Factors/scripts/vfdb_summary.py`, `windows/README.md`.
- Part 13 README status, `V2_ROADMAP.md`, main `README.md`, `SESSION_LOG.md`, memory updated for 03–05.
- Scratch (may be wiped): `scratchpad/{bact,win08}` (session 83497dd9); BLAST+ is in env `bio` (`~/miniforge3/envs/bio/bin`), not `amr`; run helper `export PATH=~/miniforge3/envs/rnaseq/bin:~/miniforge3/envs/snakemake/bin:$PATH`.

## 4. Key decisions and rejected approaches
- DESeq2 GSE52778 script kept DESeq2-only (~1.0 GB; loading DESeq2 alone 590 MB); edgeR/limma and the combination contrast moved to separate scripts. Memory stated honestly.
- Snakemake not installed into `rnaseq` (conda conflict) → `conda activate workflow && conda activate --stack rnaseq`.
- Snakefile: explicit named inputs (rejected `input: rules.download.output` → `'InputFiles' object has no attribute 'matrix'`); `--cores 1` so two ~1 GB R jobs don't run together.
- Teach deleting an output / `--forcerun` for reruns (rejected `touch`: Snakemake 9 still said "Nothing to be done").
- GEO annotation file blocked (reCAPTCHA/404) → NCBI `gene_info` FTP for symbols.
- Label swap reported as "likely", not proven; GEO title and characteristics agree, so swap (if any) predates submission. First guess (cAMP explains partial scores) rejected by per-gene data.
- 13/05: first run at 150k reads gave lexA baseMean 1 → 400k reads and SOS genes at median baseline. Operons simulated as one transcript (shared noise → S10 genes all ≈ −1.1, only 6/11 significant; taught as "11 genes ≠ 11 independent evidence").
- `make_data.sh` checks md5 of uncompressed reads (gzip header contains a date).
- YouTube search from server returns nothing → WebSearch + noembed. No VirulenceFinder video found → module videos + 2 papers.
- Windows 08/02: AMRFinderPlus/stxtyper/ABRicate have no Windows build → BLAST+ on known genes + VFDB, `vfdb_summary.py` (stdlib) replaces awk/sort/uniq, Excel PivotTable/conditional formatting replaces R heatmap, VirulenceFinder web (✍️). Use `-out`/`Set-Content`, not `>` (PS 5.1 writes UTF-16).
- Windows 08/03 plan: skip building isoF on Windows (BLAST pEK499.fna directly), ResFinder/PlasmidFinder web ✍️, PlasmidFinder BLAST rows filtered in Excel (no new script), `gb_context.py` instead of AMRFinderPlus table, `find_crispr.py` runs as is, cas genes via `py -c` one-liner.

## 5. Known bugs and caveats (exact messages)
- raw.githubusercontent.com throttled (`curl: (28) Operation timed out after 120002 milliseconds with 39282 out of 6572149 bytes received`) → `https://cdn.jsdelivr.net/gh/tseemann/abricate@master/db/...` (same 6,572,149 bytes).
- Two tool calls (pEK499 FASTA conversion / ENA download) were stopped by a safety classifier; don't repeat them — use NCBI files from the retry loop.
- 2026-11-05: NCBI (ftp/eutils/datasets) timed out twice from server ~1 h (`curl: (28) Failed to connect to ftp.ncbi.nlm.nih.gov:443`); a background retry loop worked.
- Snakemake shell + `head`: `returned non-zero exit status 141` under `set -euo pipefail` → `awk 'NR <= 20'`.
- Snakemake CLI: targets must come before `--config` (otherwise swallowed as config values).
- `curl` PubMed search without `--data-urlencode`: `bad range in URL`.
- Download script: SIGPIPE in `zcat | head` under pipefail → awk.
- tximport needs jsonlite → `dropInfReps=TRUE`; `round()` on DESeq2 results fails → `as.data.frame` first.
- FastQC 0.13: `-o` rejected → `--outdir`. Salmon 2.8: `expected_format IU` while fragments are ISR (reported in 13/02).
- 41 significant GSE52778 genes have symbol NA (retired GeneIDs, e.g. 102724788 → replaced by 5625 PRODH).
- 2026-11-09: repo renamed to `raminabiri/course-bioinformatics`; `origin` updated and all paths changed to `~/course-bioinformatics-main` (zip top folder verified).
- Older caveats (Ensembl 500/503, BioMart GET only, UCSC Turnstile, EDirect SSL stderr with API key, remote BLAST queue, `pgrep -f` self-match, ugrep) → see SESSION_LOG.

## 6. Next steps (priority order, one session each)
1. **Windows route roll-out:** 08/04 (next), then 07, 06, 09, 03, 04, 11, 12, 13 — one `00_lesson_windows.md` each; add a Windows marker (🪟) wherever a module can be done on pure Windows (user agreed 2026-11-03; some steps still need a few PowerShell/Python lines).
2. v2 part 14 (enrichment; input `de_dex_deseq2.tsv` from 13/03).
3. Later: real runs of v1 part 07 (needs user approval); plan separate courses (`/data/Education/new/`); course-end link/video/book checks with the user's VPN; decide restructure; interactive installable app (see memory `interactive-app-idea`, only when user asks).
