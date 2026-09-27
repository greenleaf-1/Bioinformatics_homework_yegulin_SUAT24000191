# EMP-Web 课程项目报告

会话 ID: JJOOtTNvizA2mhGb5bKCxeLG
生成时间: 2026-09-27 14:51:23

## 视频测验进度
已通过 5 个步骤测验。

## 科学解读与假设

## 任务反思

- **course_transcriptomics / s1_import**
  基因 ID 类型为 Gene Symbol，无需进行 ID 转换。colData 中的样本 ID 与 count 矩阵的列名一一对应，样本顺序和分组信息匹配。

- **course_transcriptomics / s2_prepare**
  DESeq2 必须使用原始整数 count，因为它通过负二项分布估计基因的均值—方差关系和离散度，并利用 size factor 校正文库大小。TPM 已按基因长度和文库大小转换为相对量，不能保留 DESeq2 建模所需的原始计数信息。低表达基因通过“至少在 3 个样本中 count ≥10”的规则过滤，以减少低计数噪声和多重检验负担。如果元数据中存在 batch 且它与实验组别不完全混杂，应使用 ~ batch + Group；当前数据没有 batch 列，因此不能凭空加入批次变量，只能将其作为实验局限说明。

- **course_transcriptomics / s3_analysis**
  本次结果表实际导出的对比方向为 DMSO vs DMSO+LIPUS，未纳入其他协变量。因此 log2FC > 0 表示基因在 DMSO 组表达更高，log2FC < 0 表示在 DMSO+LIPUS 组表达更高。使用 FDR < 0.05 控制多重检验错误，并用 |log2FC| ≥ 1 筛选表达变化至少两倍的候选基因。

- **course_transcriptomics / s4_visualization**
  本次检验的 14,238 个基因中，没有基因同时满足 FDR < 0.05 和 |log2FC| ≥ 1，因此目前没有证据支持存在显著差异表达基因，也不能把任何基因称为显著差异基因。若根据 |log2FC| 和已知功能选择三个基因继续观察，它们只能称为探索性候选基因，仍需更多样本或独立实验验证。

- **course_transcriptomics / s5_interpretation**
  当前同步结果中没有可核验的富集结果表，因此暂时不能报告某条通路显著富集。正式解读时，我会检查校正后的 p 值、富集所使用的背景基因集以及每条通路中的重叠基因。ORA 富集只能说明候选基因在某个功能集合中出现得比随机预期更多，不能单独证明该通路被激活、抑制或由 LIPUS 直接调控。我使用 AI 帮助解释分析概念和润色文字，但人工核对了对比方向、padj、log2FoldChange、背景基因集和富集表，并将 AI 生成的因果性表述修改为“统计关联”或“提示可能相关”。最终科学判断由我根据实际统计结果完成。

## Learning Trace 摘要
共 56 条事件。

