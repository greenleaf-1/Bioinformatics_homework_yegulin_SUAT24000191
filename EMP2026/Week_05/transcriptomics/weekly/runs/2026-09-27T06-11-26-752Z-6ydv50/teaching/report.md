# EMP-Web 课程项目报告

会话 ID: JJOOtTNvizA2mhGb5bKCxeLG
生成时间: 2026-09-27 14:11:28

## 视频测验进度
已通过 5 个步骤测验。

## 科学解读与假设

## 任务反思

- **course_transcriptomics / s1_import**
  基因 ID 类型为 Gene Symbol，无需进行 ID 转换。colData 中的样本 ID 与 count 矩阵的列名一一对应，样本顺序和分组信息匹配。

- **course_transcriptomics / s2_prepare**
  DESeq2 必须使用原始整数 count，因为它通过负二项分布估计基因的均值—方差关系和离散度，并利用 size factor 校正文库大小。TPM 已按基因长度和文库大小转换为相对量，不能保留 DESeq2 建模所需的原始计数信息。低表达基因通过“至少在 3 个样本中 count ≥10”的规则过滤，以减少低计数噪声和多重检验负担。如果元数据中存在 batch 且它与实验组别不完全混杂，应使用 ~ batch + Group；当前数据没有 batch 列，因此不能凭空加入批次变量，只能将其作为实验局限说明。

- **course_transcriptomics / s3_analysis**
  我将 DMSO 设为参考组，比较 DMSO+LIPUS 与 DMSO。正的 log2FoldChange 表示基因在 DMSO+LIPUS 组中表达较高，负值表示表达较低。当前元数据只提供 Group，因此设计公式为 ~ Group；若存在可靠的批次信息，则应改为 ~ batch + Group。差异基因阈值设为 padj < 0.05 且 |log2FoldChange| ≥ 1：前者用于控制多重检验的假发现率，后者表示表达变化至少达到约 2 倍。两个条件同时满足，才能兼顾统计可信度和效应大小。

- **course_transcriptomics / s4_visualization**
  我采用 padj < 0.05 且 |log2FoldChange| ≥ 1 作为候选差异基因的统计标准，并从热图中优先关注 Cxcl5、Fn1 和 Acta2。Cxcl5 与炎症反应及免疫细胞募集有关；Fn1 编码纤连蛋白，与细胞黏附和细胞外基质重塑有关；Acta2 与细胞骨架、收缩表型及成纤维细胞活化有关。但是，当前同步结果中没有保存可核验的 log2FoldChange 和 padj 数值，因此这三个基因目前只能称为待核验的候选基因。热图颜色代表相对表达模式，不能单独证明统计显著性、调控机制或因果关系。

- **course_transcriptomics / s5_interpretation**
  当前同步结果中没有可核验的富集结果表，因此暂时不能报告某条通路显著富集。正式解读时，我会检查校正后的 p 值、富集所使用的背景基因集以及每条通路中的重叠基因。ORA 富集只能说明候选基因在某个功能集合中出现得比随机预期更多，不能单独证明该通路被激活、抑制或由 LIPUS 直接调控。我使用 AI 帮助解释分析概念和润色文字，但人工核对了对比方向、padj、log2FoldChange、背景基因集和富集表，并将 AI 生成的因果性表述修改为“统计关联”或“提示可能相关”。最终科学判断由我根据实际统计结果完成。

## Learning Trace 摘要
共 47 条事件。

