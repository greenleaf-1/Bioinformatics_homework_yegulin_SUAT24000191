# Week 4 作业互动记录

- 学生：叶顾霖
- 学号：SUAT24000191
- 开始日期：2026-09-19
- 记录原则：保留学生原始回答；AI 反馈和修正单独记录，不覆盖原话。

## Q1 理解检查 1：多组学证据能否直接证明因果

**问题**

如果某个区域表现为 ATAC-seq 信号升高、H3K27ac 增强，并且与 Gene X 启动子的 Hi-C 接触增强，我们能否直接断定它导致了 Gene X 上调？为什么？

**学生原始回答**

> 不能，只能判断该区域开放程度较高，但也可能是受远端调控或正在发生转录

**AI 反馈（与原始回答分开）**

核心判断正确：这些结果只能支持候选增强子，不能直接证明因果。更精确地说，ATAC-seq 支持染色质开放，H3K27ac 支持活跃调控元件相关状态，Hi-C 支持空间接近。三者仍可能是共同上游调控、细胞组成差异或疾病状态的伴随结果。需要 CRISPRi、增强子删除等扰动实验，观察 Gene X 表达是否随之改变，才能获得更强的因果证据。

## Q1 个人初步判断 1：首选 assay

**问题**

如果目前只能先做一项实验，你会选择哪一种 assay 来调查 Gene X 上调的原因？为什么？

**学生原始回答**

> 我会先选择ATAC-seq，判断该区域的基因表达上调是由染色质的结构状态导致的，还是受其他调控因素的影响

**AI 反馈（与原始回答分开）**

选择 ATAC-seq 作为第一项筛查实验是合理的，前提是当前优先检验的假设为疾病组与对照组之间存在染色质可及性差异。表述需要修正：ATAC-seq 直接测量开放染色质或染色质可及性，不直接测量 Gene X 的表达，也不能仅凭可及性差异判断染色质变化是表达上调的原因。若疾病组在 Gene X 启动子或候选调控元件附近出现更强的 ATAC-seq 信号，只能说明该区域更加开放并与表达变化相关；因果关系仍需其他调控组学和扰动实验验证。

**学生第一次修订**

> 我首先选择 ATAC-seq，比较疾病组和健康对照组中 Gene X 启动子及候选调控区域的染色质可及性，判断 Gene X 上调是否是由局部调控区域开放程度的变化导致的，还是由其他调控元件的影响

**对修订的反馈**

已经明确比较组别、检测区域和检测对象，但“由……导致”仍超出了 ATAC-seq 的证据范围。ATAC-seq 可以判断 Gene X 上调是否伴随局部开放性变化，并定位候选调控区域；不能单独区分局部开放性是原因、结果，还是由其他调控因素共同造成。

**知识点确认回答**

> 疾病组出现更强的ATAC-seq peak,最直接说明该区域染色质开放程度更高，可及性更强，但不能说明该变化导致Gene X 上调

**判定**

通过。该回答准确区分了染色质可及性这一直接观察与 Gene X 上调的因果解释。

## Q1 理解检查 2：活跃调控元件相关修饰

**问题**

如果 ATAC-seq 找到一个疾病组特异开放的上游区域，而下一步想判断它是否具有活跃增强子相关的组蛋白修饰，应选择什么实验并检测什么标记？

**学生原始回答**

> 使用ChIP-seq或CUT&Tag判断该区域是否存在与组蛋白乙酰化有关的活跃启动子或增强子

**AI 反馈（与原始回答分开）**

技术选择正确，但应明确检测标记为 H3K27ac。更准确的表述是：使用 H3K27ac ChIP-seq 或 CUT&Tag，判断候选区域是否富集与活跃启动子或增强子相关的 H3K27ac 修饰。该证据支持活跃调控元件状态，但仍不能证明该区域调控 Gene X。

## Q1 理解检查 3：三维接触证据

**问题**

如果 Hi-C 显示疾病组中候选区域与 Gene X 启动子的接触增强，这项结果能支持什么，又不能证明什么？

**学生原始回答**

> 显示该区域与Gene X在空间结构上接触较近，但不能证明二者之间存在调控关系

**判定**

通过。Hi-C/Micro-C 的直接证据是空间接触频率或邻近关系；接触增强可以支持潜在调控联系，但不能单独证明功能性调控或因果作用。

## Q1 理解检查 4：DNA 甲基化与反向因果

**问题**

如果疾病组中 Gene X 启动子的甲基化降低，同时 Gene X 表达升高，我们能否直接说启动子去甲基化导致了 Gene X 上调？为什么？

**学生原始回答**

> 不能，甲基化降低也可能是转录活跃的结果或由细胞类型本身差异导致的，

**判定**

通过。该回答正确提出了反向因果和细胞组成混杂两种替代解释；低甲基化与高表达的同时出现首先属于关联证据。

## Q1 理解检查 5：远端调控变异的测序选择

**问题**

如果怀疑 Gene X 上游约 100 kb 的远端增强子中存在调控变异，应优先选择 WGS 还是 WES？为什么？

**学生原始回答**

> 应该选择WGS，因为启动子、增强子等调控元件不属于外显子，无法被WES检测出来，

**判定**

通过。WGS 可系统覆盖编码区和非编码调控区，更适合寻找远端增强子变异。严格来说，WES 偶尔可能产生非目标区域 reads，但不设计为可靠覆盖远端增强子，不能替代 WGS 完成这一任务。

## Q1 理解检查 6：转录起始位点

**问题**

如果 RNA-seq 已经表明 Gene X 总表达量升高，而我们想判断疾病组是否启用了新的转录起始位点或替代启动子，应选择什么实验？

**学生原始回答**

> 可以使用CAGE或RAMPAGE，精确定位转录起始位点

**判定**

通过。CAGE/RAMPAGE 富集 RNA 5′ 端信号，适合定位转录起始位点并比较启动子使用情况。

## Q1 理解检查 7：MPRA 与原生位点验证

**问题**

如果一个候选区域在 MPRA 中能增强报告基因表达，但在原生细胞中进行 CRISPRi 后 Gene X 表达没有变化，应怎样解释？

**学生澄清问题**

> GeneX 表达没有变化指的是没有增强还是保持增强

**条件澄清**

这里指 CRISPRi 后 Gene X 相对于 non-targeting sgRNA 对照没有显著变化；若实验前处于高表达，则仍保持原有高表达。

**学生原始回答**

> 表明该区域可能是潜在的增强调控区域，但在原位条件下，该区域并没有发挥作用或者作用对象不是Gene X

**判定**

通过。MPRA 支持序列在人工报告系统中的潜在增强活性；CRISPRi 阴性结果提示该区域在所测原生细胞状态下可能不是 Gene X 表达所必需，可能调控其他基因，也需检查 CRISPRi 效率、细胞状态和冗余增强子等技术或生物学解释。

## Q1 个人工作流决策 2：连接候选区域与目标基因

**问题**

如果 ATAC-seq 和 H3K27ac 检测均得到阳性结果，下一步先做 Hi-C/Micro-C，还是直接进行 CRISPRi？为什么？

**学生原始回答**

> Hi-C/Micro-C,确认该区域是否与GeneX 在空间上存在接触

**AI 反馈（与原始回答分开）**

该顺序合理。Hi-C/Micro-C 可先判断候选区域是否与 Gene X 启动子存在空间接触，从而为候选区域与目标基因的配对提供证据。但接触阳性仍不足以证明功能关系，下一步需要原生位点扰动实验。

## Q1 个人工作流决策 3：因果验证

**问题**

在 Hi-C/Micro-C 也支持空间接触后，选择 CRISPRi 还是 enhancer deletion 进行因果验证？什么实验结果会支持这个区域调控 Gene X？

**学生原始回答**

> CRISPRi ,如果Gene X 表达下调，则证明该结论

**AI 反馈（与原始回答分开）**

选择 CRISPRi 及预期 Gene X 下调的方向正确。科学表述应由“证明”调整为“提供强因果支持”：CRISPRi 可能存在脱靶效应、抑制范围扩散、扰动效率不足或细胞状态改变。需要 non-targeting sgRNA、多条独立 sgRNA、扰动效率、邻近基因表达和细胞活性等对照；必要时增加正交验证。

**因果边界确认回答**

> 因为可能产生脱靶效应、或者扩散作用或细胞损伤

**判定**

通过。CRISPRi 后 Gene X 下调属于强因果支持，但脱靶、局部抑制扩散和细胞损伤等替代解释仍需通过对照排除。

## Q1 个人工作流决策 4：ATAC-seq 阴性分支

**问题**

如果 ATAC-seq 没有发现明显差异，优先调查哪一种替代机制，并使用什么实验？

**学生原始回答**

> 进行**Hi-C/Micro-C** ，筛选候选区域

**AI 反馈（与原始回答分开）**

该选择可以用于调查三维接触改变，但“筛选候选区域”需要更精确地表述为：以 Gene X 启动子为中心，识别疾病组与健康对照组之间接触频率发生变化的基因组区域。Hi-C/Micro-C 只能提供空间接触证据；接触区域是否为活跃增强子，仍需结合 H3K27ac、其他染色质证据和功能扰动。

## Q1 学生初始工作流摘要（AI 专项 critique 前）

1. 首先使用 ATAC-seq 比较疾病组与健康对照组中 Gene X 启动子及候选调控区域的染色质可及性。
2. 对疾病组特异开放区域检测 H3K27ac ChIP-seq/CUT&Tag，判断其是否具有活跃调控元件相关特征。
3. 使用 Hi-C/Micro-C 检查候选区域是否与 Gene X 启动子存在空间接触。
4. 使用 CRISPRi 抑制候选区域；若 Gene X 表达在多条独立 sgRNA 中一致下降，并通过相应对照排除脱靶、抑制扩散和细胞损伤，则为调控关系提供强因果支持。
5. 如果 ATAC-seq 未发现明显差异，使用 Hi-C/Micro-C 识别与 Gene X 启动子存在差异接触的区域，再结合调控状态和功能实验判断。

## Q1 AI critique 后的学生决定

**AI 建议**

在染色质主线之外，将 WGS、WGBS/EM-seq 和 CAGE/RAMPAGE 加入条件分支，以排查非编码变异、DNA 甲基化和替代启动子机制；不对所有样本机械地执行全部 assay。

**学生决定**

> 是的

**最终取舍**

接受该建议。保留 ATAC-seq → H3K27ac ChIP-seq/CUT&Tag → Hi-C/Micro-C → CRISPRi 的主线，并根据前一步证据有条件地增加 WGS、WGBS/EM-seq、CAGE/RAMPAGE 和 MPRA。

## Q2 理解检查 1：paired-end 与生物学重复

**问题**

为什么同一个样本的 R1 和 R2 不能算作两个生物学重复？

**学生原始回答**

> 因为他们来自同一个生物样本，但是提供了同一片段两个方向的信息

**判定**

通过。R1 与 R2 来自同一 DNA 片段和同一生物样本，只增加片段两端的序列与定位信息，没有增加独立的生物实验单位。

## Q2 理解检查 2：base quality 与 mapping quality

**问题**

如果一条 read 的所有碱基都达到 Q30，但它能同样好地比对到基因组中的五个重复区域，那么它的 base quality 和 mapping quality 分别应当是高还是低？为什么？

**学生原始回答**

> 高和低，因为虽然每个碱基的质量都很高，但是无法确认具体位置

**判定**

通过。测序仪对碱基判读有较高信心，因此 base quality 高；比对软件无法在多个相似位置中确定唯一来源，因此 mapping quality 低。

## Q2 FastQC 指标 1：Per base sequence quality

**题目快照**

约 15% 的 R1 在第 50 个 cycle 后出现 3′ 端质量下降，中位 Phred 约为 Q12，状态为 WARN。

**问题**

根据这项快照，S01 出现了什么质量问题，后续应该采取什么处理？

**学生原始回答**

> 不知道

**教学处理**

该回答记录为尚未掌握，不作为最终作业结论。后续将问题拆分为异常位置、错误风险和处理措施三个小步骤，再重新检查理解。

**拆分检查 1：异常位置**

> 3

**判定**

正确。质量下降发生在 read 的 3′ 端（第 50 个 cycle 以后）。

**拆分检查 2：处理后验证**

> 重新进行碱基质量检测

**判定**

正确。修剪后应重新运行 FastQC，核对 per-base sequence quality 和 adapter content 是否改善，同时检查 reads 保留数量和配对关系，避免修剪过度。

## Q2 FastQC 指标 2：Per sequence GC content

**题目快照**

主峰约为 41% GC，同时在约 78% GC 处出现高 GC 肩峰；约 10% 的 reads 为人为加入的高 GC 污染，状态为 WARN。

**问题**

S01 在约 78% GC 处出现额外肩峰，首先提示文库中可能存在什么问题？

**学生原始回答**

> 存在外源序列污染的问题

**判定**

通过。本题的数据说明明确将高 GC 肩峰设置为污染信号。真实数据中还需通过序列比对或污染筛查确认来源，不能只根据 GC 偏高直接删除 reads。

## Q2 FastQC 指标 3：Adapter content

**题目快照**

约 15% 的 read pairs 在 3′ 端出现 Illumina-like `AGATCGGAAGAGC` 接头，状态为 FAIL；同一片段也出现在 overrepresented sequences 中。

**问题**

发现约 15% 的 read pairs 含有 3′ 端接头后，下一步应该怎样处理？

**学生原始回答**

> 修剪接头

**判定**

正确。应使用明确的接头序列进行 trimming，保持 R1/R2 配对，并重新运行 FastQC，检查 adapter content、末端质量和 reads 保留情况。

## Q2 FastQC 指标 4：Sequence duplication levels

**题目快照**

R1 中一条模板序列重复出现，约占 15%，状态为 WARN。

**问题**

为什么不能仅凭 FastQC 显示 duplication WARN，就直接删除所有重复序列？

**学生原始回答**

> 因为只能说明可能存在异常情况，但也可能是真实情况，需要进一步验证

**判定**

通过。重复 reads 可能来自 PCR/optical duplicates，也可能来自真实高覆盖或实验设计。WGS 中通常在比对后结合坐标识别并标记 duplicates，保留可追溯信息，而非依据 FastQC 结果盲目删除。

## Q1 学生提出的设计质疑：能否直接进行 CRISPRi

**学生问题**

> 如果直接CRISPR i ，得到阳性结果，能说明问题吗，逻辑上是否存在漏洞

**记录的判断**

直接 CRISPRi 是合理的功能筛查路线。若抑制候选区域后 Gene X 表达发生可重复、方向一致的变化，可以支持该区域在所测细胞状态下对 Gene X 表达具有功能必要性。但是，单一 CRISPRi 阳性不能单独证明该区域是通过直接的 enhancer-promoter 接触调控 Gene X；还需排除 off-target、抑制效应扩散、邻近基因或非编码 RNA 的间接作用、细胞毒性及其他局部染色质改变。Hi-C/Micro-C 可补充物理接触证据，但本身也不证明因果。

**学生进一步质疑**

> 那直接CRISPR i 不就行了吗，为什么还要做前面那么多assay

**设计修正**

该质疑成立：若已有定位明确的候选区域，CRISPRi 可以前移作为功能筛查，不必机械执行所有 assay。但 Q1 只给出 Gene X 上调，没有提供可直接靶向的候选区域；同时要求判断调控变异、可及性、转录因子或组蛋白修饰、甲基化、三维接触等哪种机制更可能。CRISPRi 阳性主要支持目标区域的功能必要性，不能单独识别上述具体机制。因此最终方案应采用分阶段决策树：先用与假设相符的发现型 assay 定位候选区域，再用 CRISPRi 筛查功能；其余 assay 按阳性结果和待解释机制选择，而不是全部无条件串行执行。
### Q2 — Reference genome selection

- **Knowledge check:** If reads are aligned to GRCh38 but the VCF is annotated directly against a GRCh37/hg19 coordinate database, what may happen?
- **Student answer:** “变异可能被定位到错误基因、错误功能区域，甚至无法匹配数据库。”
- **Assessment:** Correct. The answer identifies misannotation and failed database matching caused by assembly mismatch. Also verify chromosome naming and REF/ALT alleles after any coordinate conversion.
### Q2 — Alignment

- **Knowledge check:** For paired-end human WGS, would you choose BWA-MEM2 or STAR, and why?
- **Student answer:** “BWA-MEM2，适合短读长 DNA 测序，能够利用双端信息确定片段位置。”
- **Assessment:** Correct. BWA-MEM2 matches short-read DNA/WGS data; the final workflow should also specify paired R1/R2 input, GRCh38, read-group metadata, SAM/BAM output, and post-alignment QC.
### Q2 — Mapped-read processing

- **Knowledge check:** Why should a BAM file be coordinate-sorted and indexed?
- **Student answer:** “让变异检测工具和 IGV 能够高效、正确地访问指定基因组区域。”
- **Assessment:** Correct. Coordinate sorting groups nearby alignments, and the index permits random access to selected genomic intervals.
### Q2 — WGS downstream analysis

- **Knowledge check:** What information is stored in BAM and VCF files?
- **Student answer:** “BAM 保存 reads 在参考基因组上的比对位置和质量，VCF 记录染色体位置、REF、ALT、基因型、深度和质量等。”
- **Assessment:** Correct. BAM contains alignment evidence; VCF contains variant calls inferred from that evidence. A PASS record is not automatically biologically or clinically important.
### Q2 — Variant annotation

- **Knowledge check:** Can a VEP `missense_variant` annotation alone establish pathogenicity, and why?
- **Student answer:** “不能，只能表示发生了错义突变，但具体有什么功能或者后果需要后续确认。”
- **Assessment:** Correct. A predicted sequence consequence is not equivalent to functional damage or pathogenicity; population, clinical, segregation, and functional evidence may be needed.
### Q2 — Visualization and read-level review

- **Knowledge check:** How should a candidate supported only by a few low-MAPQ reads, with ALT bases concentrated at read ends, be judged?
- **Initial student answer:** “更可能是由测序时人为添加的末端接头导致的基因污染而不是真实变异。”
- **Feedback:** The false-positive judgment was sound, but adapter sequence is not “gene contamination.” Low terminal base quality, residual adapter, and ambiguous mapping can create sequencing or alignment artifacts.
- **Revised student answer:** “因为可能是末端测序质量低下或残留接头序列导致的测序或比对伪影。”
- **Assessment:** Correct after revision. Re-QC, trim if justified, realign, recall, and independently verify important candidates.
### Q2 — Interpretation

- **Knowledge check:** Does `FILTER=PASS` plus `missense_variant` establish that a variant causes disease?
- **Student answer:** “不能，只能说明在当前过滤条件下，可以认为发生了变异，但具体变异导致后果，需要后续实验验证。”
- **Assessment:** Correct in direction. More precisely, PASS means the candidate passed the current technical filters, and missense describes a predicted sequence consequence; neither alone proves that the call is real, functionally damaging, or pathogenic.
### Q2 — Experimental design and batch confounding

- **Knowledge check:** Can greater sequencing depth resolve complete confounding when every control is in batch A and every case is in batch B?
- **Student answer:** “不能，测序深度只能增加碱基的可靠性，但是批次差异还可能来源于样本的保存或处理流程等其他差异。”
- **Assessment:** Correct. Greater depth cannot separate biological condition from batch when they coincide completely; balanced/randomized processing and recorded batch metadata are required.
### Q2 — Student-designed eight-step workflow before task-specific AI critique

- **Student draft:** “首先进行FASTQ的质量检测，标记质量较低的碱基，排除测序伪影的干扰，确保碱基读数的可靠性，随后选取合适的参考基因组，确保使用正确相对坐标的参考序列，之后完成序列比对……接下来对序列进行比对，找到变异，并对变异进行注释、可视化、解释。”
- **Mapped-read processing follow-up:** The student first proposed “建立索引,” then added “标记重复、建立索引并进行BQSR.”
- **Teaching correction:** FastQC diagnoses rather than automatically removes low-quality bases. Coordinate sorting is also required before downstream random access and duplicate processing.
- **Consolidated student workflow after teaching:**
  1. FASTQ QC and evidence-based trimming/filtering, followed by re-QC.
  2. Select GRCh38 and keep assembly/naming consistent across resources.
  3. Align paired reads with BWA-MEM2 and retain read-group metadata.
  4. Coordinate-sort BAM, mark duplicates, apply BQSR when justified, and index the final BAM.
  5. Call and technically filter SNVs/indels for the WGS assay.
  6. Annotate variants with an assembly-matched resource such as VEP.
  7. Review candidate loci and read evidence in IGV.
  8. Interpret technical, biological, and clinical evidence separately and state uncertainty/validation needs.
### Q2 — Plan-first prompt development

- **Student's original prompt:** “请你按照作业要求生成对我的流程进行检验并修正的计划。”
- **Student reflection:** “准确，但是我写不出来。”
- **AI feedback:** The intent to request a plan was present, but the prompt did not yet specify assay, inputs, checkpoints, assembly, or the teaching-demo limitation.
- **AI-assisted refined prompt, confirmed by the student:** “请先检查并修正我设计的人类双端 WGS 分析流程，只输出各步骤的目的、输入、输出、质量检查点和需要核实的官方文档，暂不执行命令；参考基因组采用 GRCh38，并注意 S01 只有 120 对合成 reads，仅用于格式和质控教学，不能当作真实全基因组数据运行生产流程。”
### Q2 — AI audit decision 1

- **AI recommendation:** Delete all duplicate FASTQ reads before alignment to obtain the cleanest data.
- **Student decision:** “拒绝，在 FASTQ 阶段，相同序列不一定都是 PCR 重复，也可能是真实的高丰度片段。”
- **Assessment:** Scientifically sound rejection. The replacement is to retain raw reads, align them, mark duplicates using alignment/paired-end evidence, and interpret duplicate rates in assay context.
### Q2 — Acceptance of AI-generated plan

- **Student decision:** “接受。”
- **Meaning for the audit:** The student accepted the complete plan after reviewing its scope, eight-step workflow, conditional BQSR, preservation of raw data, and the explicit restriction against treating S01 as a production WGS library. The earlier student rejection of raw-FASTQ de-duplication remains a specific rejected AI recommendation.
## Q3 — Preliminary integrated model before task-specific AI classification

**Student original response**

> 首先通过RNA-seq，判断Gene Y是否存在明显的过表达，再ATAC结果判断该区域的染色质开放性和可及性，通过H3K27ac ChIP-seq/CUT&Tag判断该区域的乙酰化程度，若甲基化程度较低、乙酰化程度和可及性较高，表明该区域存在较高的功能活性，Hi-C/Micro-C判断该区域与Gene Y在三维结构上是否接近，从而判断是否存在接触调控。但是以上只能间接支持该候选区域可能是Gene Y 的增强子，强的直接证据需要需要通过CRISPR i 或deletion来判断

**Assessment and teaching corrections**

- The student correctly integrated transcription, accessibility, H3K27ac, methylation, 3D contact, and perturbation, while distinguishing association from stronger causal evidence.
- RNA-seq requires a defined comparator before “overexpression/upregulation” can be claimed.
- H3K27ac is a specific active-regulatory-element-associated histone mark, not a measurement of total histone acetylation.
- Low methylation, high accessibility, H3K27ac enrichment, contact, and Gene Y upregulation would jointly support a candidate enhancer model, but would not by themselves establish Gene Y as the functional target.
- CRISPRi or deletion can provide stronger causal support when paired with efficiency, off-target, neighboring-gene, and cell-state controls.
### Q3 — Observation versus interpretation: ATAC-seq

- **Classification prompt:** (1) Candidate-region ATAC-seq signal is higher than control. (2) The region is an active Gene Y enhancer.
- **Student answer:** “1直接观察；2生物学解释。”
- **Assessment:** Correct. The second statement also overreaches the evidence because accessibility alone does not establish enhancer identity, target gene, or causality.
### Q3 — H3K27ac evidence boundary

- **Knowledge check:** Do coincident ATAC-seq and H3K27ac peaks prove that the region is a Gene Y enhancer?
- **Student answer:** “不能，只能证明该区域具有活跃启动子或增强子相关的染色质状态，但具体是哪一种调控元件，以及调控对象，无法确认。”
- **Assessment:** Correct. The combined evidence supports an active regulatory state but does not establish element class, target gene, or causality.
### Q3 — DNA methylation evidence boundary

- **Knowledge check:** If the candidate region is hypomethylated while Gene Y expression rises, can demethylation be said to have caused Gene Y upregulation?
- **Student answer:** “不能，只能说明该区域处于活跃状态，但是可能是转录活跃后的结果，且无法确认对Gene Y 的调控作用。”
- **Assessment:** Correct. Hypomethylation is compatible with an active regulatory state, but the temporal and causal direction remains unresolved; the observation also does not identify Gene Y as the functional target.
### Q3 — Hi-C/Micro-C evidence boundary

- **Knowledge check:** If Hi-C/Micro-C shows strong contact between the candidate region and the Gene Y promoter, can that confirm regulation of Gene Y?
- **Student answer:** “不能，只能证明该区域与Gene Y在空间上更靠近，具备发生接触调控的条件，但无法证明调控关系。”
- **Assessment:** Correct. Contact supports spatial opportunity for regulation, but does not establish direction, functional effect, or causality.
### Q3 — RNA-seq evidence boundary

- **Knowledge check:** If RNA-seq shows that Gene Y is significantly upregulated relative to a matched control, can that result alone prove that the candidate region is its enhancer?
- **Student answer:** “不能，无法确定该区域与GeneY 之间的调控关系。”
- **Assessment:** Correct. RNA-seq directly measures expression change but cannot assign that change to a particular regulatory element.
### Q3 — Integrated preliminary model

- **Integration prompt:** If the candidate region shows increased accessibility, H3K27ac enrichment, reduced DNA methylation, enriched contact with the Gene Y promoter, and Gene Y upregulation relative to matched controls, what is the strongest preliminary conclusion that avoids overclaiming?
- **Student answer:** “该区域是Gene Y的一个合理的候选增强子。”
- **Assessment:** Correct. In the final answer this will be written conditionally because the homework supplies the available data types but no numerical observations. Concordant multi-omics evidence supports a plausible candidate-enhancer model, not confirmed regulation or causality.
### Q3 — AI classification audit: absent observations

- **AI-audit prompt:** An AI-generated statement treated increased ATAC-seq and H3K27ac, reduced methylation, stronger Gene Y contact, and Gene Y upregulation as if they had been observed, even though the assignment provides no signal values.
- **Student decision:** “不要刻意假设。”
- **Assessment:** Correct rejection. The assignment establishes only which data types are available. It does not report any biological signal direction, so the submission must state that the current evidence is insufficient for a biological verdict, specify the observations that should be extracted, and keep any enhancer model conditional.
### Q3 — Alternative explanations

- **Assignment requirement:** Propose at least one alternative explanation for the candidate-region/Gene Y model.
- **Student answer:** “它调控的是另一个基因或观察到的变化来自细胞类型比例差异。”
- **Assessment:** Both are valid. Regulation of another gene is a direct alternative target model; cell-type composition is a confounding explanation that could produce coordinated chromatin and expression differences without within-cell regulation of Gene Y.
### Q3 — Completed functional design and final evidence boundary

- **Student direction:** “先把Q3完成。”
- **Final design based on the student's earlier choice:** Use endogenous-locus dCas9-KRAB CRISPRi with multiple independent sgRNAs, a non-targeting control, and a Gene Y promoter positive control; measure Gene Y, neighboring genes, perturbation efficiency, cell viability, and cell state.
- **Falsification logic:** Reproducible Gene Y reduction without matching neighboring-gene or cell-state abnormalities supports the Gene Y enhancer model. A change in another nearby gene without a Gene Y change supports the alternative-target model. Cell-composition confounding is addressed in the same purified cell type or at single-cell resolution.
- **Final evidence boundary:** Because the assignment supplies no actual omics signal values, the report makes no positive biological observation and presents the required final sentence explicitly as a testable hypothesis.

## Q4 — Filtering logic before task-specific AI workflow

### Q4 — Technical filter status

- **Knowledge check:** Should the main candidate shortlist require `FILTER=PASS`, and why?
- **Student answer:** “是的，需要排除其他的干扰。”
- **Assessment:** Accepted with a boundary correction. `PASS` reduces artifacts covered by the current caller/filter rules but does not eliminate all sequencing, alignment, or batch artifacts. High-impact non-PASS calls should be removed from the main reliable shortlist while retained in a separate technical-validation queue rather than declared absent.
### Q4 — Minimum depth

- **Proposed teaching-data rule:** Require `DP ≥ 20` for the main candidate shortlist; lower-depth high-impact calls remain in a technical-validation queue.
- **Student decision:** “接受，过低会导致该碱基的可靠性较低。”
- **Assessment:** Accepted. More precisely, low DP leaves insufficient read support for a reliable allele/genotype call at the locus; the threshold is justified by the clear DP gap in this synthetic table and is not a universal WGS rule.
### Q4 — Minimum genotype quality

- **Proposed teaching-data rule:** Require `GQ ≥ 30` for the main candidate shortlist.
- **Student decision:** “支持，控制基因型判断出错的概率小于0.1%。”
- **Assessment:** Correct under the Phred model: GQ 30 corresponds to an estimated genotype-error probability of approximately 0.1%, assuming the score is calibrated and the alignment/model assumptions hold.
### Q4 — Population-frequency ceiling

- **Proposed teaching-data rule:** Require synthetic population-style `AF ≤ 0.001` for a generic rare, potentially high-penetrance variant screen.
- **Student decision:** “使用，该条件表示该等位基因在群体中出现的频率小于0.1%，属于罕见情况。”
- **Assessment:** Correct. This is a context-dependent teaching threshold; rarity prioritizes candidates but does not establish pathogenicity, and the absence of phenotype/inheritance information limits disease-specific interpretation.
### Q4 — Consequence ranking

- **Proposed rule:** Prioritize splice-acceptor/donor, stop-gained, and frameshift consequences above missense; retain technically reliable rare missense variants for later evidence ranking; down-rank rather than universally declare synonymous, intronic, and intergenic variants nonfunctional.
- **Student decision:** “接受。”
- **Assessment:** Accepted. Predicted loss-of-function consequences receive higher initial priority, but transcript choice and functional evidence still require verification; missense effects are heterogeneous and therefore remain candidates for evidence-based ranking.
### Q4 — ClinVar / clinical annotation ranking

- **Assignment boundary:** The homework asks the student to define a rule for “biological/clinical evidence”; the worksheet supplies a `ClinVar / clinical annotation` row, but it does not prescribe a fixed ClinVar ranking rule.
- **Proposed student-defined rule:** Prioritize `Pathogenic`; retain `Uncertain_significance` and `Conflicting_interpretations_of_pathogenicity` as secondary candidates; down-rank or exclude `Benign` and `Likely_benign`; verify shortlisted annotations against authoritative resources.
- **Student decision:** “接受。”
- **Assessment:** Accepted as the student's filtering rule. A ClinVar label contributes evidence but does not by itself prove that a variant explains the phenotype of the sample.
### Q4 — Gene / biology relevance

- **Knowledge check:** Can the `TP53` variant be declared the most biologically relevant variant solely from the gene name and its prominence?
- **Student answer:** “不能，可以为作为高概率候选基因，但需要直接的证据来证明。”
- **Assessment:** Correct. `TP53` may be prioritized as a candidate on the supplied technical, frequency, consequence, and annotation evidence, but this table lacks phenotype, inheritance, sample-source, and functional evidence needed to establish sample-specific disease relevance.
### Q4 — Final candidate selection before verification

- **Assignment requirement:** Prioritize one or two variants for further investigation.
- **Student choice:** “那就TP53把，splice accepter,影响后果最为严重。”
- **Assessment and wording correction:** Select `chr17:7673803 G>A` in `TP53`; the correct term is `splice_acceptor_variant`. It is a predicted high-impact consequence, but is not universally more severe than every stop-gained or frameshift variant. Its defensible priority comes from the combined evidence in this table: it passes the technical thresholds, is very rare in the synthetic AF field, has a splice-acceptor consequence, and carries a `Pathogenic` annotation.
### Q4 — Strongest false-lead concern

- **Assignment requirement:** Ask for the strongest reasons the top variant could be a false lead, then decide which concerns matter scientifically.
- **Student decision:** “题目没有提供表型和遗传模式，无法判断 `TP53` 是否与样本疾病相符。”
- **Assessment:** Correct. This is the strongest sample-specific biological limitation: the supplied fields can prioritize a variant for further investigation, but cannot establish a gene–phenotype match or the expected inheritance model. Additional limitations are that the consequence is predicted, the ClinVar entry is synthetic, the transcript is unspecified, and the call lacks orthogonal confirmation.
### Q4 — Experiment targeting the proposed mechanism

- **Knowledge check:** What material should be analyzed to test whether a splice-acceptor variant changes splicing?
- **Student answer:** “分析RNA转录本。”
- **Assessment:** Correct. RT-PCR across flanking exons followed by cDNA sequencing can test for exon skipping, intron retention, or cryptic splice-site use. Orthogonal genomic-DNA sequencing confirms that the call exists but does not by itself test the RNA-splicing mechanism.
