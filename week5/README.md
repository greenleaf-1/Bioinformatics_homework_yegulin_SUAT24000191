# Week 5 submission

## Homework 1: DESeq2

- `week5_deseq2_analysis.R`: reproducible analysis; reads only approved count and metadata inputs.
- `data_raw/`: traceable copies of the two approved inputs. The instructor key is intentionally absent.
- `week5_deseq2_results.csv`: complete apeglm-shrunken result table.
- `week5_top20_results.csv`: top 20 results ranked by adjusted p-value; no unapproved annotation was added.
- `week5_pca.png` and `week5_de_plot.png`: PCA and volcano plots.
- `week5_deseq2_object.rds`: fitted DESeq2 object.
- `session_info.txt`: reproducibility environment.
- `design_and_checks.tsv`: input, reference-level, design-rank, filter, and coefficient checks.
- `analysis_summary.tsv`: compact machine-readable result summary.
- `week5_interpretation.md`: 100–150 word English interpretation.
- `week5_AI_verification_log.md`: AI-assisted step, independent verification, correction, and evidence boundary.
- `RNA_specific_extension.md`: falsifiable circRNA-aware follow-up plan.

Run from the homework repository root with:

```bash
Rscript week5/week5_deseq2_analysis.R
```

Homework 2 export/sync evidence will be added only after EasyMultiProfiler-Web and GitHub remote verification are complete.

