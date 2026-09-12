# Week 3 homework: count-matrix checks and a paired DESeq2 contrast

args_all <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args_all, value = TRUE)
script_dir <- if (length(file_arg) == 1L) {
  dirname(normalizePath(sub("^--file=", "", file_arg)))
} else {
  normalizePath("week3")
}
data_dir <- file.path(script_dir, "data_raw")

read_geo_counts <- function(filename, annotation_columns = 6L) {
  path <- file.path(data_dir, filename)
  stopifnot(file.exists(path))
  table <- read.delim(gzfile(path), check.names = FALSE, stringsAsFactors = FALSE)
  counts <- as.matrix(table[, seq.int(annotation_columns + 1L, ncol(table))])
  storage.mode(counts) <- "numeric"
  list(annotation = table[, seq_len(annotation_columns), drop = FALSE], counts = counts)
}

is_integer_matrix <- function(x) {
  all(is.finite(x)) && all(x >= 0) && all(x == floor(x))
}

# Part A: GSE146853
gse146853 <- read_geo_counts("GSE146853_GeneCount_raw.txt.gz")
cat("GSE146853 genes:", nrow(gse146853$counts), "\n")
cat("GSE146853 samples:", ncol(gse146853$counts), "\n")
cat("GSE146853 non-negative integer counts:", is_integer_matrix(gse146853$counts), "\n\n")

# Part B: GSE87487
gse87487 <- read_geo_counts("GSE87487_counts.20samples.txt.gz")
cat("GSE87487 genes:", nrow(gse87487$counts), "\n")
cat("GSE87487 samples:", ncol(gse87487$counts), "\n")
cat("GSE87487 non-negative integer counts:", is_integer_matrix(gse87487$counts), "\n")

sample_name <- sub("^Sample_", "", colnames(gse87487$counts))
sample_name <- sub("\\.bam$", "", sample_name)
subject <- sub("(?i)bx[12]$", "", gsub("-", "", sample_name), perl = TRUE)
stage <- ifelse(grepl("(?i)bx1$", sample_name, perl = TRUE), "pre", "post")

# IRI status was read from the GSE87487 GEO family metadata.
iri_positive_subjects <- c("RJ", "Pt9", "Pt10", "Pt12")
iri <- ifelse(subject %in% iri_positive_subjects, "positive", "negative")
sample_metadata <- data.frame(
  sample = sample_name,
  subject = factor(subject),
  stage = factor(stage, levels = c("pre", "post")),
  iri = factor(iri, levels = c("negative", "positive")),
  row.names = colnames(gse87487$counts)
)

pair_table <- table(sample_metadata$subject, sample_metadata$stage)
cat("Subjects:", nrow(pair_table), "\n")
cat("Every subject has one pre and one post sample:", all(pair_table == 1L), "\n")
cat("IRI-positive pairs:", length(unique(subject[iri == "positive"])), "\n")
cat("IRI-negative pairs:", length(unique(subject[iri == "negative"])), "\n\n")
print(sample_metadata)

# Specific contrast for the homework:
# within the four IRI-positive subjects, post-reperfusion versus pre-reperfusion,
# while including subject in the design to preserve pairing.
if (requireNamespace("DESeq2", quietly = TRUE)) {
  keep_samples <- sample_metadata$iri == "positive"
  counts_positive <- gse87487$counts[, keep_samples, drop = FALSE]
  metadata_positive <- droplevels(sample_metadata[keep_samples, , drop = FALSE])

  keep_genes <- rowSums(counts_positive) >= 10
  counts_positive <- round(counts_positive[keep_genes, , drop = FALSE])

  dds <- DESeq2::DESeqDataSetFromMatrix(
    countData = counts_positive,
    colData = metadata_positive,
    design = ~ subject + stage
  )
  dds <- DESeq2::DESeq(dds)
  result_post_vs_pre <- DESeq2::results(
    dds,
    contrast = c("stage", "post", "pre"),
    alpha = 0.05
  )
  result_post_vs_pre <- result_post_vs_pre[order(result_post_vs_pre$padj), ]
  print(summary(result_post_vs_pre))
} else {
  message("DESeq2 is not installed; all input and pairing checks completed, but differential expression was not run.")
}
