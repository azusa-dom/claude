# cine-CMR 综述 v10 图件(按 `review/11_图件重新设计方案.md` 重新绘制)

本目录是 `azusa-dom/academic_PhD_task` 稿件 v10 的全套新图:主文 5 张、graphical abstract 1 张、补充 3 张,共 9 张。所有图都是原创的概念、解析或数值示意图,不含真实患者影像,也不复制任何已发表论文的图像。原有六图和稿件源文件均未改动。新图在本仓库生成,因为本会话对稿件仓库只有读取权限。

## 文件

`out/` 里每张图都有 PDF、SVG 和 600 dpi PNG(GA 为 2600 × 1000 px)。`src/` 是生成脚本:Fig 2、3、4、S1、S2 用 matplotlib,Fig 1、5、S3 和 GA 用 Typst + CeTZ。`style/` 统一定义配色、字体、字号和尺寸。`data/table_s3_methods.csv` 是 Fig 3 的数据,每行写了证据类型的判定理由和 `supplement.tex` 行号;`data/mrxcat2_values.csv` 是 Fig 4 的全部数值,每个数都附了 MRXCAT2.0 原文的原句。`captions_and_alt_text.md` 是英文图注和 alt text 草稿。运行 `./build.sh` 可从源码重建全部图件,依赖版本见 `requirements.txt`。

| 图 | 文件名 | 尺寸 |
|---|---|---|
| Fig 1 测量链与三道失败点 | `Figure_1_measurement_chain` | 160 × 98 mm |
| Fig 2 同一轮廓、不同对应(解析反例) | `Figure_2_same_contours_analytic` | 160 × 58 mm |
| Fig 3 方法年表 1999–2026 | `Figure_3_method_timeline` | 160 × 131.6 mm |
| Fig 4 属性特异恢复(MRXCAT2.0) | `Figure_4_attribute_specific_recovery` | 160 × 92 mm |
| Fig 5 验证目标与三阶段方案 | `Figure_5_validation_targets_programme` | 160 × 146 mm |
| Graphical abstract | `Graphical_abstract` | 2600 × 1000 px |
| S1 应变定义陷阱 | `Figure_S1_strain_definition_traps` | 166 × 112 mm |
| S2 误差属性与映射有效性 | `Figure_S2_error_attributes_mapping_validity` | 166 × 100 mm |
| S3 训练期与推理期控制 | `Figure_S3_training_vs_inference_controls` | 166 × 69 mm |

## 规格依据与实际核查

Elsevier 官方 artwork sizing 页面规定单栏 90 mm、1.5 栏 140 mm、双栏 190 mm,普通文字以 7 pt 为准,只有上下标可低到 6 pt;academic-figures 预设里的 "6–8 pt" 把下限说宽了。稿件 `main.tex` 版心为 160 mm,`supplement.tex` 为 166 mm,图在稿件中按 `width=\textwidth` 插入。如果按方案的 175–180 mm 或 Elsevier 的 190 mm 绘制,在投稿 PDF 中会被缩小到约 84%,7.5 pt 将变成 6.3 pt。因此主文图按 160 mm、补充图按 166 mm 绘制,图内文字 7–10 pt(标签 7–7.5 pt、面板小标题 9 pt、面板字母 10 pt),全部不低于 7 pt;排版时放大到 190 mm 双栏后字号只会变大。

已实际核查的内容如下。每个 PDF 的页面尺寸都与上表一致。字体全部嵌入:标签为 Liberation Sans,数学为 Liberation Serif;这两款开源字体与 Arial、Times New Roman 字宽完全一致,环境里没有微软字体。matplotlib 导出的 SVG 保留可编辑文字,字体声明为 `'Arial', 'Liberation Sans'`,在装有 Arial 的电脑上会直接显示 Arial。Typst 导出的 SVG 把文字转成了轮廓,所以 Fig 1、5、S3 和 GA 要改字时请用 PDF 或 `.typ` 源码。每张图都在实际尺寸下渲染后逐张目检,重叠、裁切、溢出已全部修正。

Fig 4 的数值已用 PubMed Central 全文(PMC10116689,[doi:10.1186/s12968-023-00934-z](https://doi.org/10.1186/s12968-023-00934-z))逐个核对:EF 51/34/41/49%;梗死例远端/瘢痕的径向、纵向、周向应变为 0.95/0.30、−0.18/−0.17、−0.18/0.01;Dice 0.82;位移误差 1.0 ± 0.9 mm;周向误差 0.02 ± 0.04;径向误差 −0.24 ± 0.21,梗死例 −0.20 ± 0.21。以上均与稿件 §4.1 一致。

## 需要你决定或核实的事项

Fig 4 和稿件正文之间有三处出入。第一,§4.1 第二段写的是 "underestimating radial strain in every case",但原文正文只写了 "a general underestimation of radial strains";逐例是否都低估,只能从原文的图(检索到的文本不含图)判断。因此图和图注都用了 "generally",建议你查原文 Fig. 14,再决定是否改正文。第二,"three mid-ventricular short-axis slices" 在检索到的全文里没有找到(原文只说限于 mid-ventricular 2D 短轴),图内没有写层数。第三,原文应变记号在文本提取中丢失了下标,究竟是工程应变还是 Green–Lagrange 应变需要回原文确认,图里只标 "peak systolic strain"。

Fig 3 的证据分类是我依据 Table S3 各单元格做的判断,而这些单元格本身是摘要级阅读,CSV 里逐行写了理由。有几处边界情况请你过目:Vigneault/Puyol-Antón 归为下游标签(依据是 HCM 与对照的分组),Low-rank GW 归为未报告,DENSE-rotation 归为材料敏感参照(检索记录中无数据),3D tagging nets 归为已知运动(摘要级),MyoNet 归为方法间一致性。另外,图例比方案改了一处:方案没有"有已知运动但无病理"这一类,所以把合成已知运动并入橙色"材料敏感参照、无预设局灶缺损",橙底红边菱形只用于唯一一次预设局灶缺损测试。DeepStrain 画了两个点:2021 年自身评估(灰)和 2023 年 MRXCAT2.0 独立测试(菱形),这样不会把两篇文献的证据混在一起。3D tagging nets 在 Table S3 里但不在方案的名单中,已纳入;boundary feature tracking 没有单一年份,未画,图注中已说明。按 Table S3 统计:mask/landmark 类 19 个、下游标签 7 个、材料敏感参照 9 个、未报告 3 个、预设局灶测试 1 次,共 38 个方法。

Fig 4c 的四个属性状态(magnitude 部分保住、location 与 extent 未报告、timing 未检视)也是我的判读,依据是原文正文和稿件 §4.1 的限定语。

配色严格用了方案给的色值。方案里的青色 #2A7F9E 偏蓝,与 CLAUDE.md 要求的"低饱和绿系与陶土/桃色"有出入。如果你希望统一成绿系,只需改 `style/figstyle.py` 和 `style/theme.typ` 两处色值,再运行 `./build.sh`。

## 尚未完成

稿件源文件没有改动:`body.tex` 和 `supplement.tex` 中的 `\includegraphics` 文件名、图注、交叉引用(主文图从 3 张增加到 5 张,旧 S1 并入新 Fig 5a,新 S1 改为应变定义),以及 AI 声明中的图件段落,都需要在稿件仓库里更新并重新编译,之后逐页检查。图注中的 `[tool statement]` 也要换成作者认可的工具声明。科学内容验证、作者批准和期刊接受都还没有发生。
