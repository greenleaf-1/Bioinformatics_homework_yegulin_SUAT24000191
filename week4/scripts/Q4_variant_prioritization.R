# Week 4 Q4: transparent filtering of the synthetic teaching variants.
# The thresholds and ranking rules were defined before running this script.

args <- commandArgs(trailingOnly = FALSE)
script_arg <- grep("^--file=", args, value = TRUE)
script_path <- normalizePath(sub("^--file=", "", script_arg[1]))
week4_dir <- dirname(dirname(script_path))

input_path <- file.path(
  dirname(dirname(week4_dir)),
  "课程主页-Bioinformatics_SUAT_2026_FALL", "Week 4", "Homework",
  "for_student", "data", "variants_q4.tsv"
)
results_dir <- file.path(week4_dir, "results")
dir.create(results_dir, recursive = TRUE, showWarnings = FALSE)

variants <- read.delim(
  input_path,
  comment.char = "#",
  stringsAsFactors = FALSE,
  check.names = FALSE
)

# Student-defined hard filters for the main reliable candidate set.
min_dp <- 20
min_gq <- 30
max_af <- 0.001
impact_consequences <- c(
  "stop_gained", "frameshift_variant", "splice_acceptor_variant",
  "splice_donor_variant", "missense_variant"
)

variants$PASS_FILTER <- variants$FILTER == "PASS"
variants$PASS_DP <- variants$DP >= min_dp
variants$PASS_GQ <- variants$GQ >= min_gq
variants$PASS_AF <- variants$AF <= max_af
variants$PASS_CONSEQUENCE <- variants$CONSEQUENCE %in% impact_consequences
variants$MAIN_FILTER_PASS <- with(
  variants, PASS_FILTER & PASS_DP & PASS_GQ & PASS_AF & PASS_CONSEQUENCE
)

# Scores rank variants only after hard technical/frequency/consequence filters.
# No phenotype was supplied, so gene name or fame receives no score.
consequence_score <- c(
  splice_acceptor_variant = 5,
  splice_donor_variant = 5,
  stop_gained = 5,
  frameshift_variant = 5,
  missense_variant = 3,
  synonymous_variant = 1,
  intron_variant = 0,
  intergenic_variant = 0
)
clinical_score <- c(
  Pathogenic = 4,
  Conflicting_interpretations_of_pathogenicity = 3,
  Uncertain_significance = 2,
  Likely_benign = 1,
  Benign = 0
)

variants$CONSEQUENCE_SCORE <- unname(consequence_score[variants$CONSEQUENCE])
variants$CLINICAL_SCORE <- unname(clinical_score[variants$CLINVAR_SIG])
variants$CONSEQUENCE_SCORE[is.na(variants$CONSEQUENCE_SCORE)] <- 0
variants$CLINICAL_SCORE[is.na(variants$CLINICAL_SCORE)] <- 0
variants$TOTAL_SCORE <- variants$CONSEQUENCE_SCORE + variants$CLINICAL_SCORE

failure_reason <- function(i) {
  reasons <- character()
  if (!variants$PASS_FILTER[i]) reasons <- c(reasons, paste0("FILTER=", variants$FILTER[i]))
  if (!variants$PASS_DP[i]) reasons <- c(reasons, paste0("DP<", min_dp))
  if (!variants$PASS_GQ[i]) reasons <- c(reasons, paste0("GQ<", min_gq))
  if (!variants$PASS_AF[i]) reasons <- c(reasons, paste0("AF>", max_af))
  if (!variants$PASS_CONSEQUENCE[i]) reasons <- c(reasons, "lower-priority consequence")
  if (length(reasons) == 0) "retained" else paste(reasons, collapse = "; ")
}
variants$FILTER_DECISION <- vapply(seq_len(nrow(variants)), failure_reason, character(1))

ranked <- variants[variants$MAIN_FILTER_PASS, ]
ranked <- ranked[order(-ranked$TOTAL_SCORE, ranked$AF), ]
ranked$RANK <- seq_len(nrow(ranked))

# High-impact calls failing technical thresholds are retained for confirmation,
# not interpreted as reliable biological candidates.
high_impact <- variants$CONSEQUENCE %in% c(
  "stop_gained", "frameshift_variant", "splice_acceptor_variant", "splice_donor_variant"
)
validation_queue <- variants[high_impact & !variants$MAIN_FILTER_PASS, ]

write.table(
  variants, file.path(results_dir, "Q4_filter_audit.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE, na = "."
)
write.table(
  ranked, file.path(results_dir, "Q4_ranked_candidates.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE, na = "."
)
write.table(
  validation_queue, file.path(results_dir, "Q4_technical_validation_queue.tsv"),
  sep = "\t", row.names = FALSE, quote = FALSE, na = "."
)

cat("Main-filter candidates:", nrow(ranked), "\n")
print(ranked[, c(
  "RANK", "CHROM", "POS", "REF", "ALT", "DP", "GQ", "AF", "GENE",
  "CONSEQUENCE", "CLINVAR_SIG", "TOTAL_SCORE"
)], row.names = FALSE)
cat("\nHigh-impact calls requiring technical validation:", nrow(validation_queue), "\n")
print(validation_queue[, c(
  "CHROM", "POS", "GENE", "CONSEQUENCE", "FILTER", "DP", "GQ",
  "FILTER_DECISION"
)], row.names = FALSE)
