# cine-CMR 综述 v10 图件(按 `review/11_图件重新设计方案.md` 重新绘制)

本目录是 `azusa-dom/academic_PhD_task` 稿件 v10 的全套新图:主文 5 张、graphical abstract 1 张、补充 3 张,共 9 张。所有图都是原创的概念、解析或数值示意图,不含真实患者影像,也不复制任何已发表论文的图像。原有六图和稿件源文件均未改动。新图在本仓库生成,因为本会话对稿件仓库只有读取权限。

## 文件

`out/` 里每张图都有 PDF、SVG 和 600 dpi PNG(GA 为 2600 × 1000 px)。`src/` 是生成脚本:Fig 2、3、4、S1、S2 用 matplotlib,Fig 1、5、S3 和 GA 用 Typst + CeTZ。`style/` 统一定义配色、字体、字号和尺寸,并含两个审计脚本(面板对齐、字号)。`qa/` 是每次构建的审计结果和总览图。`FIGURE_CONTRACT.md` 写明每张图的主张、证据层级和配色语义。`data/table_s3_methods.csv` 是 Fig 3 的数据,每行写了证据类型的判定理由和 `supplement.tex` 行号;`data/mrxcat2_values.csv` 是 Fig 4 的全部数值,每个数都附了 MRXCAT2.0 原文的原句。`captions_and_alt_text.md` 是英文图注和 alt text 草稿。运行 `./build.sh` 可从源码重建全部图件并自动跑审计,依赖版本见 `requirements.txt`。

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

Elsevier 官方 artwork sizing 页面规定单栏 90 mm、1.5 栏 140 mm、双栏 190 mm,普通文字以 7 pt 为准,只有上下标可低到 6 pt;academic-figures 预设里的 "6–8 pt" 把下限说宽了。稿件 `main.tex` 版心为 160 mm,`supplement.tex` 为 166 mm,图在稿件中按 `width=\textwidth` 插入。如果按方案的 175–180 mm 或 Elsevier 的 190 mm 绘制,在投稿 PDF 中会被缩小到约 84%,7.5 pt 将变成 6.3 pt。因此主文图按 160 mm、补充图按 166 mm 绘制,图内文字 7.2–10 pt(标签 7.2–7.5 pt、面板小标题 9 pt、面板字母 10 pt),数学上下标不低于 6 pt;排版时放大到 190 mm 双栏后字号只会变大。

已实际核查的内容如下。每个 PDF 的页面尺寸都与上表一致。字体全部嵌入:标签为 Liberation Sans,数学为 Liberation Serif;这两款开源字体与 Arial、Times New Roman 字宽完全一致,环境里没有微软字体。matplotlib 导出的 SVG 保留可编辑文字,字体声明为 `'Arial', 'Liberation Sans'`,在装有 Arial 的电脑上会直接显示 Arial。Typst 导出的 SVG 把文字转成了轮廓,所以 Fig 1、5、S3 和 GA 要改字时请用 PDF 或 `.typ` 源码。每张图都在实际尺寸下渲染后逐张目检,重叠、裁切、溢出已全部修正。

Fig 4 的数值已用 PubMed Central 全文(PMC10116689,[doi:10.1186/s12968-023-00934-z](https://doi.org/10.1186/s12968-023-00934-z))逐个核对:EF 51/34/41/49%;梗死例远端/瘢痕的径向、纵向、周向应变为 0.95/0.30、−0.18/−0.17、−0.18/0.01;Dice 0.82;位移误差 1.0 ± 0.9 mm;周向误差 0.02 ± 0.04;径向误差 −0.24 ± 0.21,梗死例 −0.20 ± 0.21。以上均与稿件 §4.1 一致。

## 需要你决定或核实的事项

Fig 4 和稿件正文之间有三处出入。第一,§4.1 第二段写的是 "underestimating radial strain in every case",但原文正文只写了 "a general underestimation of radial strains";逐例是否都低估,只能从原文的图(检索到的文本不含图)判断。因此图和图注都用了 "generally",建议你查原文 Fig. 14,再决定是否改正文。第二,"three mid-ventricular short-axis slices" 在检索到的全文里没有找到(原文只说限于 mid-ventricular 2D 短轴),图内没有写层数。第三,原文应变记号在文本提取中丢失了下标,究竟是工程应变还是 Green–Lagrange 应变需要回原文确认,图里只标 "peak systolic strain"。

Fig 3 的证据分类是我依据 Table S3 各单元格做的判断,而这些单元格本身是摘要级阅读,CSV 里逐行写了理由。有几处边界情况请你过目:Vigneault/Puyol-Antón 归为下游标签(依据是 HCM 与对照的分组),Low-rank GW 归为未报告,DENSE-rotation 归为材料敏感参照(检索记录中无数据),3D tagging nets 归为已知运动(摘要级),MyoNet 归为方法间一致性。另外,图例比方案改了一处:方案没有"有已知运动但无病理"这一类,所以把合成已知运动并入"材料敏感参照、无预设局灶缺损"(深沈香棕),棕底墨边菱形只用于唯一一次预设局灶缺损测试。DeepStrain 画了两个点:2021 年自身评估(灰)和 2023 年 MRXCAT2.0 独立测试(菱形),这样不会把两篇文献的证据混在一起。3D tagging nets 在 Table S3 里但不在方案的名单中,已纳入;boundary feature tracking 没有单一年份,未画,图注中已说明。按 Table S3 统计:mask/landmark 类 19 个、下游标签 7 个、材料敏感参照 9 个、未报告 3 个、预设局灶测试 1 次,共 38 个方法。

Fig 4c 的四个属性状态(magnitude 部分保住、location 与 extent 未报告、timing 未检视)也是我的判读,依据是原文正文和稿件 §4.1 的限定语。

## 配色(依据你给的色卡)

色卡是沈香墨 `#8D6449`、素绢白 `#F8F3E7`、檀木棕 `#C0997F`、棠梨绯 `#E7A49A`。这四个颜色饱和度很低、色相相近,原样用作数据色时,用 dataviz skill 的配色校验器检查,色盲模拟和正常视觉下都分不开(例如檀木棕与灰色 ΔE 只有 10.4,檀木棕对白底的对比度只有 2.6:1)。所以在同一色系里取了加深版,并按"同一张图里实际同时出现的颜色"逐组校验:

| 角色 | 色值 | 来源 |
|---|---|---|
| 推断 / 估计 | `#C0584A`,浅底 `#F8E0DA` | 棠梨绯加深、浅化 |
| 参照 / 验证 | `#7A4720`,浅底 `#EFE2D3` | 沈香墨加深;浅底取自檀木棕 |
| 观测 / 中性 | `#8E857D`,浅底 `#F8F3E7` | 素绢白原色作分组底色 |
| 次级类别(Fig 3 下游标签、Fig 4 瘢痕) | `#CC5F4F` | 棠梨绯 |
| Fig 3 最弱证据类 | `#B2AAA2` | 有意使用的中性灰 |
| 支持 / 保住 | `#4E7470` | 低饱和灰青绿 |
| 误差 / 丢失 | `#A33A2E` | 只用于线条和符号 |
| 文字 | `#33261F`,次要 `#776A62` | 墨色 |

校验结果:Fig 3 三个有色类别,色盲模拟 ΔE ≥ 13.3,正常视觉 ≥ 18.1;Fig 4b 的"保住"与"误差",色盲模拟 9.1,正常视觉 18.5;推断色与参照色,色盲模拟 10.7,正常视觉 15.3,均过线。沈香墨 `#8D6449` 原色与棠梨绯在色盲模拟下几乎重合(ΔE 0.8),所以参照色用了更深的 `#7A4720`。"支持"没有用暖色:暖色系里没有哪种颜色能和误差红分开,改用低饱和灰青绿,也符合 CLAUDE.md 的"低饱和绿系"。未过的检查只剩饱和度下限:中性灰是有意的,深沈香棕的饱和度 0.088,略低于 0.10,这是色系本身的特点。灰色对白底对比度偏低,但 Fig 3 的每个点都有文字标签。画布保持纯白,素绢白只作框内底色。

按 skill 的硬性规则做了两处修改:文字一律用墨色,不跟数据系列同色(原来 Fig 4 的数值、Fig 2 的曲线标签、Fig 5a 的"能证明"列都用了系列色);S1 d 里"推断"色和"误差"色原本同框,改为一条用墨色虚线。

## 版式重设计(文字密集的框图)

Fig 1、Fig 5、S3 原来把每条信息装进带边框、带底色的卡片,长句直接压在彩色底上,读起来像一面表格墙。现在改成"颜色只做点缀、文字一律放在白底上"的轻量版式,用字号、粗细和灰度区分层级,不再靠框线分隔。科学内容一项未删,精简掉的说明句都在图注里。

- Fig 1:五个步骤改成一条带编号站点的流程线,站点颜色区分观测、推断和参照;三个失败点放在对应站点正下方,用同色编号圈对应,不再画穿过文字的连线;原来的归因长段改成三行"现象 → 归因"小表;结论用一条绿色色条引出。
- Fig 5:a 改成三线表,"能证明"列前加对勾,"不能单独证明"列前加叉号并用灰字;b 的漏斗改成竖向编号步骤线,资源改成细线胶囊标签,与各阶段对齐;c 去掉外框。
- S3:两种控制改成上下两条并行流程线,在右侧汇合后指向底部的"共享评估"带,评估条件做成一排胶囊标签。
- Fig 4c:四张属性卡片去掉边框,改用细竖线分隔,说明文字改为次要灰。

另外关闭了 Typst 的自动断词,避免 "re-imaging" 这类词被拆到两行。

## 与 Codex 修订版的合并

Codex 版本在我的源码上做了样式修订和 QA,源码改动保留如下:Fig 3 去掉穿过方法名的整列网格线,泳道分隔线在断轴处断开;"下游标签"不再借用"推断"的颜色;Fig 4 瘢痕柱改为斜纹而不用误差红;S1 几处标签位置微调;Fig 1 的转置号改用 `ᵀ` 字形;面板对齐审计 `style/audit_panel_alignment.py` 接入 `save()`,严格模式,不通过就中断构建。它的 CSF3 提交脚本里写死了个人路径,运行日志也属于它的环境,这两样都没有并入。

Codex 报告中留下的问题已修:Fig 2 和 S1 的数学上下标只有 5.04 pt,低于 Elsevier 对上下标 6 pt 的下限。现在 Fig 2 的 θ′ 改为 θ ↦ 写法,不再有上标;λθ 和 e² 所在公式行放大到 8.6 pt,上下标实测 6.02 pt。

## QA(每次 `./build.sh` 自动执行,结果在 `qa/`)

- 面板对齐(Codex 引入的审计,严格模式):Fig 2、3、4、S1、S2 全部通过。
- 字号(`style/audit_font_sizes.py`,从 PDF 逐字读取,旋转文字按包围盒校正):9 张全部通过;正文最小 7.2 pt,上下标最小 6.02 pt。
- 渲染质量(scientific-figure-skills 的 `audit_render_quality.py`,三种格式齐全、分辨率、非空白、matplotlib 图的 SVG 必须保留可编辑文字):9 张全部通过。Fig 1、5、S3 和 GA 各有一条警告,是 Typst 导出的 SVG 文字为轮廓,这几张图的可编辑文字在 PDF 里。
- 配色(dataviz skill 的 `validate_palette.js`):结果见上节。
- 目检:按实际尺寸逐张检查,总览图为 `qa/contact-sheet.png`。

## 尚未完成

稿件源文件没有改动:`body.tex` 和 `supplement.tex` 中的 `\includegraphics` 文件名、图注、交叉引用(主文图从 3 张增加到 5 张,旧 S1 并入新 Fig 5a,新 S1 改为应变定义),以及 AI 声明中的图件段落,都需要在稿件仓库里更新并重新编译,之后逐页检查。图注中的 `[tool statement]` 也要换成作者认可的工具声明。科学内容验证、作者批准和期刊接受都还没有发生。
