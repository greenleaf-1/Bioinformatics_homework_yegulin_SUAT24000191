# RNA-specific extension: circRNA-aware follow-up plan

## Biological question

Does treatment alter circular-RNA abundance independently of the host gene's linear transcript abundance?

## Why the current matrix is insufficient

The supplied matrix contains gene-level counts and cannot establish back-splice junctions. A conventional poly(A)-selected library would also deplete many circRNAs. Therefore, the Week 5 DESeq2 result must not be reinterpreted as circRNA evidence.

## Minimum falsifiable workflow

1. Generate or obtain rRNA-depleted total-RNA, paired-end FASTQ files with biological replicates in every treatment and batch.
2. Perform read-level QC and alignment, then call back-splice junctions with a circRNA-aware tool such as CIRI2/CIRIquant or an independently validated equivalent.
3. Require reproducible junction support across replicates and filter low-count candidates before testing abundance with a design that retains `batch + condition`.
4. Quantify the corresponding linear host-gene signal and test whether the circRNA change remains after accounting for host-gene expression.
5. Validate leading candidates with divergent primers spanning the back-splice junction, RNase R resistance, and junction sequencing. Include convergent-primer and no-RT controls.

## Decision rule

A candidate would be supported only if its junction is reproducible, statistically different after multiple-testing correction, and experimentally verified. Failure of junction-specific validation would falsify the circRNA interpretation even if host-gene expression changes.

