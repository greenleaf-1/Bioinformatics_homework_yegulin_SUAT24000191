#!/usr/bin/env Rscript

# Week 5 RNA-seq differential-expression analysis
# Approved inputs: count matrix and sample metadata only. The instructor key is
# intentionally excluded from the analysis and is never read by this script.

suppressPackageStartupMessages({
  library(DESeq2)
  library(apeglm)
  library(ggplot2)
  library(ggrepel)
})

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) == 1L) {
  normalizePath(sub("^--file=", "", file_arg), mustWork = TRUE)
} else {
  normalizePath("week5_deseq2_analysis.R", mustWork = TRUE)
}
output_dir <- dirname(script_path)

default_source_dir <- file.path(
  output_dir, "..", "..", "课程主页-Bioinformatics_SUAT_2026_FALL",
  "Week 5", "Homework", "for_student"
)
source_dir <- Sys.getenv("WEEK5_SOURCE_DIR", unset = default_source_dir)
source_dir <- normalizePath(source_dir, mustWork = TRUE)

input_names <- c(
  counts = "Week5_Homework_Count_Matrix.csv",
  metadata = "Week5_Homework_Sample_Metadata.csv"
)
input_paths <- file.path(source_dir, input_names)
if (!all(file.exists(input_paths))) {
  stop("Missing approved input file(s): ", paste(input_paths[!file.exists(input_paths)], collapse = ", "))
}

raw_dir <- file.path(output_dir, "data_raw")
dir.create(raw_dir, recursive = TRUE, showWarnings = FALSE)
copied <- file.copy(input_paths, file.path(raw_dir, input_names), overwrite = TRUE)
if (!all(copied)) stop("Failed to copy one or more approved inputs into data_raw/.")

counts_path <- file.path(raw_dir, input_names[["counts"]])
metadata_path <- file.path(raw_dir, input_names[["metadata"]])

counts <- read.csv(counts_path, row.names = 1, check.names = FALSE)
metadata <- read.csv(metadata_path, row.names = 1, check.names = FALSE)

record_check <- function(check_id, status, observed, expected, evidence_or_action) {
  data.frame(
    check_id = check_id,
    status = if (isTRUE(status)) "PASS" else "FAIL",
    observed = as.character(observed),
    expected = as.character(expected),
    evidence_or_action = as.character(evidence_or_action),
    stringsAsFactors = FALSE
  )
}

checks <- list()
checks[[length(checks) + 1L]] <- record_check(
  "count_matrix_dimensions", identical(dim(counts), c(1000L, 12L)),
  paste(dim(counts), collapse = " x "), "1000 genes x 12 samples",
  "Read from the approved count-matrix CSV copied to data_raw/."
)
checks[[length(checks) + 1L]] <- record_check(
  "metadata_rows", nrow(metadata) == 12L, nrow(metadata), "12 samples",
  "Read from the approved sample-metadata CSV copied to data_raw/."
)
checks[[length(checks) + 1L]] <- record_check(
  "unique_gene_ids", !anyDuplicated(rownames(counts)),
  length(unique(rownames(counts))), nrow(counts), "Gene identifiers must be unique."
)
checks[[length(checks) + 1L]] <- record_check(
  "unique_sample_ids", !anyDuplicated(rownames(metadata)),
  length(unique(rownames(metadata))), nrow(metadata), "Sample identifiers must be unique."
)
checks[[length(checks) + 1L]] <- record_check(
  "sample_correspondence", identical(colnames(counts), rownames(metadata)),
  paste(colnames(counts), collapse = ","), paste(rownames(metadata), collapse = ","),
  "Column order in the count matrix must exactly match metadata row order."
)

count_matrix <- as.matrix(counts)
storage.mode(count_matrix) <- "numeric"
valid_counts <- all(is.finite(count_matrix)) && all(count_matrix >= 0) &&
  all(count_matrix == round(count_matrix))
checks[[length(checks) + 1L]] <- record_check(
  "raw_nonnegative_integer_counts", valid_counts,
  paste0("range=", paste(range(count_matrix), collapse = "..")),
  "finite non-negative integers", "DESeq2 requires untransformed integer counts."
)

metadata$condition <- factor(metadata$condition, levels = c("control", "treated"))
metadata$batch <- factor(metadata$batch)
checks[[length(checks) + 1L]] <- record_check(
  "condition_reference", identical(levels(metadata$condition), c("control", "treated")),
  paste(levels(metadata$condition), collapse = ","), "control,treated",
  "control is explicitly set as the reference level."
)
checks[[length(checks) + 1L]] <- record_check(
  "condition_batch_complete", !anyNA(metadata[, c("condition", "batch")]),
  sum(is.na(metadata[, c("condition", "batch")])), "0 missing values",
  "Both design variables are required for every sample."
)

design_matrix <- model.matrix(~ batch + condition, data = metadata)
checks[[length(checks) + 1L]] <- record_check(
  "design_full_rank", qr(design_matrix)$rank == ncol(design_matrix),
  paste0("rank=", qr(design_matrix)$rank, "; columns=", ncol(design_matrix)),
  "rank equals number of columns", "A full-rank design is required for coefficient estimation."
)

check_table <- do.call(rbind, checks)
if (any(check_table$status == "FAIL")) {
  write.table(
    check_table, file.path(output_dir, "design_and_checks.tsv"), sep = "\t",
    quote = FALSE, row.names = FALSE
  )
  stop("One or more input/design checks failed. See design_and_checks.tsv.")
}

dds <- DESeqDataSetFromMatrix(
  countData = round(count_matrix),
  colData = metadata,
  design = ~ batch + condition
)
keep <- rowSums(counts(dds) >= 10L) >= 3L
checks[[length(checks) + 1L]] <- record_check(
  "prefilter", sum(keep) > 0L, paste0(sum(keep), " of ", length(keep), " genes retained"),
  "count >= 10 in at least 3 samples", "Filtering rule specified in the homework instructions."
)
dds <- dds[keep, ]
dds <- DESeq(dds, quiet = TRUE)

coefficient_names <- resultsNames(dds)
target_coef <- "condition_treated_vs_control"
checks[[length(checks) + 1L]] <- record_check(
  "treated_vs_control_coefficient", target_coef %in% coefficient_names,
  paste(coefficient_names, collapse = ","), target_coef,
  "Coefficient inspected with resultsNames(dds) before extraction and shrinkage."
)
if (!(target_coef %in% coefficient_names)) {
  check_table <- do.call(rbind, checks)
  write.table(
    check_table, file.path(output_dir, "design_and_checks.tsv"), sep = "\t",
    quote = FALSE, row.names = FALSE
  )
  stop("Expected treated-vs-control coefficient was not found.")
}

res_unshrunken <- results(dds, contrast = c("condition", "treated", "control"), alpha = 0.05)
res <- lfcShrink(dds, coef = target_coef, type = "apeglm", res = res_unshrunken)

result_table <- data.frame(
  gene_id = rownames(res),
  baseMean = res$baseMean,
  log2FoldChange = res$log2FoldChange,
  lfcSE = res$lfcSE,
  pvalue = res$pvalue,
  padj = res$padj,
  stringsAsFactors = FALSE
)
result_table$significant <- !is.na(result_table$padj) & result_table$padj < 0.05 &
  abs(result_table$log2FoldChange) >= 1
result_table$direction <- ifelse(
  result_table$significant & result_table$log2FoldChange > 0, "up",
  ifelse(result_table$significant & result_table$log2FoldChange < 0, "down", "not_significant")
)
result_table <- result_table[order(result_table$padj, -abs(result_table$log2FoldChange), na.last = TRUE), ]
write.csv(result_table, file.path(output_dir, "week5_deseq2_results.csv"), row.names = FALSE)

top20 <- head(result_table[!is.na(result_table$padj), ], 20L)
top20$annotation_note <- "No biological annotation was provided in the approved homework inputs"
write.csv(top20, file.path(output_dir, "week5_top20_results.csv"), row.names = FALSE)

vsd <- varianceStabilizingTransformation(dds, blind = FALSE)
pca_data <- plotPCA(vsd, intgroup = c("condition", "batch"), returnData = TRUE)
percent_var <- round(100 * attr(pca_data, "percentVar"), 1)
pca_data$sample_id <- rownames(pca_data)
pca_plot <- ggplot(pca_data, aes(PC1, PC2, color = condition, shape = batch, label = sample_id)) +
  geom_point(size = 3.4) +
  geom_text_repel(size = 3, max.overlaps = Inf, show.legend = FALSE) +
  xlab(paste0("PC1: ", percent_var[1], "% variance")) +
  ylab(paste0("PC2: ", percent_var[2], "% variance")) +
  ggtitle("Week 5 RNA-seq PCA (VST counts)") +
  theme_classic(base_size = 12)
ggsave(file.path(output_dir, "week5_pca.png"), pca_plot, width = 7.2, height = 5.4, dpi = 300)

volcano_data <- result_table
volcano_data$minus_log10_padj <- -log10(pmax(volcano_data$padj, .Machine$double.xmin))
volcano_data$plot_class <- factor(
  ifelse(volcano_data$direction == "up", "Significant up",
    ifelse(volcano_data$direction == "down", "Significant down", "Not significant")
  ),
  levels = c("Significant up", "Significant down", "Not significant")
)
label_data <- head(volcano_data[volcano_data$significant, ], 10L)
de_plot <- ggplot(volcano_data, aes(log2FoldChange, minus_log10_padj, color = plot_class)) +
  geom_point(alpha = 0.72, size = 1.6, na.rm = TRUE) +
  geom_vline(xintercept = c(-1, 1), linetype = "dashed", color = "grey45") +
  geom_hline(yintercept = -log10(0.05), linetype = "dashed", color = "grey45") +
  geom_text_repel(data = label_data, aes(label = gene_id), size = 2.8, max.overlaps = Inf) +
  scale_color_manual(values = c("Significant up" = "#C43C39", "Significant down" = "#3976AF", "Not significant" = "grey72")) +
  labs(
    title = "Treated vs control differential expression",
    subtitle = "apeglm-shrunken effect sizes; padj < 0.05 and |log2FC| >= 1",
    x = "Shrunken log2 fold change", y = expression(-log[10](adjusted~p)), color = NULL
  ) +
  theme_classic(base_size = 12) +
  theme(legend.position = "top")
ggsave(file.path(output_dir, "week5_de_plot.png"), de_plot, width = 7.2, height = 5.4, dpi = 300)

saveRDS(dds, file.path(output_dir, "week5_deseq2_object.rds"))
capture.output(sessionInfo(), file = file.path(output_dir, "session_info.txt"))

check_table <- do.call(rbind, checks)
write.table(
  check_table, file.path(output_dir, "design_and_checks.tsv"), sep = "\t",
  quote = FALSE, row.names = FALSE
)

summary_values <- c(
  retained_genes = nrow(dds),
  tested_with_padj = sum(!is.na(result_table$padj)),
  significant_total = sum(result_table$significant),
  significant_up = sum(result_table$direction == "up"),
  significant_down = sum(result_table$direction == "down"),
  pca_pc1_percent = percent_var[1],
  pca_pc2_percent = percent_var[2]
)
write.table(
  data.frame(metric = names(summary_values), value = unname(summary_values)),
  file.path(output_dir, "analysis_summary.tsv"), sep = "\t", quote = FALSE, row.names = FALSE
)

message("Week 5 analysis completed successfully.")
message(paste(names(summary_values), summary_values, sep = "=", collapse = "; "))
