# Week 5 AI use and independent verification log

## AI-assisted step

I asked an AI assistant to draft a reproducible DESeq2 workflow for the supplied count matrix and metadata. The requested workflow used `~ batch + condition`, set `control` as the reference, filtered genes with counts of at least 10 in at least 3 samples, inspected `resultsNames(dds)`, applied `apeglm` shrinkage, made PCA and volcano plots, and exported all required artifacts.

## What I independently verified

1. Input dimensions were checked directly: 1,000 genes by 12 samples, with 12 metadata rows.
2. Count-matrix columns exactly matched metadata row names and order; gene and sample identifiers were unique.
3. Counts were finite, non-negative integers; the design matrix was full rank.
4. `control` was explicitly the reference and `resultsNames(dds)` contained `condition_treated_vs_control` before shrinkage.
5. The prefilter retained 989 genes. The final threshold yielded 60 genes: 36 upregulated and 24 downregulated.
6. I visually inspected both PNG figures. PCA separated control and treated samples on PC1; the volcano plot used the stated fold-change and FDR cutoffs.
7. I reran the script from the submission directory, reloaded the saved DESeq2 object, and checked the CSV row and column structure.

Machine-readable evidence for checks 1–4 is in `design_and_checks.tsv`; result counts and PCA variance are in `analysis_summary.tsv`.

## Corrections and boundaries

- The first run showed that fewer than the default 1,000 features remained after filtering, so the PCA transformation was changed from `vst()` to DESeq2's recommended `varianceStabilizingTransformation()` for this data size. The model and DE results were unchanged.
- The file `Week5_Homework_Gene_Annotation_Instructor_Key.csv` was deliberately excluded. Its `truth_log2FC_for_instructor` field was not read or used to generate, select, annotate, or validate results.
- The AI-proposed biological interpretation was constrained after checking the inputs: synthetic gene IDs do not support pathway or gene-function claims.
- Package build-version warnings were recorded during execution; the analysis nevertheless completed, the object reloaded successfully, and package/runtime versions are preserved in `session_info.txt`.

