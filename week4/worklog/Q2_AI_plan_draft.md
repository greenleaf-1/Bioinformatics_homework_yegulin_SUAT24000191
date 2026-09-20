# Q2 AI-generated plan draft for student review

## Scope and assumptions

- Assay: paired-end Illumina human WGS.
- Teaching data: S01 contains only 120 synthetic read pairs and is suitable for FASTQ-format/QC interpretation only.
- Reference assembly: GRCh38; the exact FASTA source, release, checksum, contig naming, and compatible annotation resources must be recorded.
- This is a workflow-design exercise. Do not run a production whole-genome alignment or variant-calling pipeline on S01.

## Proposed workflow

| Step | Purpose | Input | Proposed action | Output / checkpoint |
|---|---|---|---|---|
| 0. Manifest and design audit | Prevent sample swaps and confounding | Sample manifest and metadata | Confirm unique sample IDs, R1/R2 pairing, assay, condition, library/batch fields, and balanced/randomized batches | Audited manifest; unresolved metadata listed |
| 1. Raw-read QC | Diagnose technical problems before modification | Raw paired FASTQ | Verify file integrity; run FastQC/MultiQC or interpret the supplied snapshot; inspect per-base quality, GC, adapters, duplication, overrepresented sequences, N content, and length | QC report and evidence-based decision on trimming |
| 2. Conditional trimming and re-QC | Remove demonstrated adapter/terminal artifacts without unnecessary information loss | Raw FASTQ plus QC evidence | For S01, test paired-end adapter/3′ quality trimming with recorded software version and parameters; preserve raw files; do not delete identical FASTQ reads as “duplicates” | Trimmed paired FASTQ; post-trim QC; read retention/length report |
| 3. Reference preparation | Keep all coordinates and resources consistent | GRCh38 FASTA and metadata | Record exact assembly/resource bundle and checksum; build aligner index; ensure known-sites and annotation resources use the same assembly and chromosome naming | Indexed reference and provenance record |
| 4. Alignment | Place each read pair on the genome | QC-passed R1/R2 and GRCh38 | Align with BWA-MEM2 using read-group fields for sample/library/platform; convert to BAM and collect mapping statistics | BAM plus alignment rate, proper-pair rate, MAPQ, insert-size and coverage metrics |
| 5. Mapped-read processing | Prepare reliable, queryable alignment evidence | Alignment BAM | Coordinate-sort; mark PCR/optical duplicates; apply BQSR only when compatible known-sites resources and workflow assumptions are satisfied; index final BAM | Processed BAM/BAI and post-processing QC |
| 6. WGS variant calling | Infer SNVs and small indels from read evidence | Processed BAM and GRCh38 | For a real cohort, use a validated germline workflow such as per-sample GVCF followed by joint genotyping; apply validated filtering appropriate to cohort size | Filtered VCF and variant-level QC; not run as production analysis on S01 |
| 7. Annotation | Add gene, transcript, consequence, frequency, and evidence context | Filtered VCF | Annotate with an assembly-matched tool/resource such as Ensembl VEP; record transcript/resource versions | Annotated VCF/table; consequence is kept separate from pathogenicity |
| 8. Visualization and interpretation | Inspect raw support and state evidence limits | BAM/BAI, VCF, reference and annotation | Review important candidates in IGV for depth, strand balance, read-end bias, base quality, MAPQ and local complexity; integrate population, clinical and functional evidence | Candidate report separating technical evidence, biological inference, clinical interpretation, uncertainty, and validation needs |

## Proposed AI recommendations for audit

These are intended as realistic recommendations to verify, modify, accept, or reject.

1. Use paired-end fastp trimming for the demonstrated adapter/3′ quality issue, but record the detected adapter, software version, parameters, retained read fraction, and post-trim QC instead of trusting defaults blindly.
2. Preserve raw FASTQ files and mark duplicates after alignment; reject deletion of identical reads in raw FASTQ as a universal WGS de-duplication strategy.
3. Use GRCh38 only after recording the exact FASTA/resource bundle, checksum, contig naming, and compatibility of known-sites and VEP resources; reject the vague instruction to “use the latest human reference.”
4. Treat BQSR as conditional on a compatible known-sites resource and a validated workflow; do not include it as an unexplained mandatory black box.
5. Treat `FILTER=PASS` and consequence annotations as technical/functional evidence, not proof of pathogenicity; retain IGV review and independent validation for important candidates.

## Verification targets

- FastQC documentation for the interpreted modules and warning/failure meaning.
- GRCh38 source/release documentation and resource compatibility.
- BWA-MEM2 documentation for paired-end input and read-group handling.
- SAM/BAM/VCF specifications and samtools/GATK documentation for sorting, indexing, duplicate marking, BQSR and variant calling.
- Ensembl VEP documentation for assembly/transcript/resource versions.
- IGV documentation for loading indexed BAM/VCF and locus review.

## Decisions reserved for the student

- Whether to accept or modify the proposed fastp trimming strategy.
- Whether BQSR belongs in the final teaching workflow and under what conditions.
- Which recommendations are accepted, modified, or rejected in the AI-audit table.
- Final wording of uncertainty and analyst responsibility.
