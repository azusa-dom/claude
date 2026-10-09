# Figure captions and alt text (draft for v10)

Captions follow the v10 figure plan, revised where the source check below required it. Panel letters are lowercase; no title appears inside any figure. Replace `[tool statement]` with the author-approved AI/tool disclosure, for example: "Drawn programmatically (Python/matplotlib and Typst/CeTZ) with AI assistance (Claude, Anthropic; [model/version]); no generative image model was used. Author verification is required before submission."

## Main text

**Figure 1 — `Figure_1_measurement_chain`** (190 × 117 mm)

From cine images to a regional strain report, and where the chain can fail. (a) Five links separate what routine cine observes (neutral) from what an estimator infers (rose) and what a validation target can establish (brown). (b) Three failure points map onto distinct links and can be tested separately: input sufficiency by re-imaging the same motion, estimation by varying the regularisation weight with images fixed, and representation capacity by projecting a known field onto the estimator's function space. (c) Validation should follow the finest claimed spatial and temporal scale. Conceptual schematic; no study data. [tool statement]

Alt text: Flow diagram of five linked boxes from image formation to validation target, with three test boxes beneath pointing by dashed arrows at the links where input information, estimation and representation can fail, and a highlighted sentence on validation scale.

**Figure 2 — `Figure_2_same_contours_analytic`** (190 × 64 mm)

Identical contours do not determine the same material correspondence. (a) Schematic of the information each acquisition supplies: routine cine provides boundaries and weak texture, tagging a prepared pattern, DENSE phase-encoded displacement. (b) Two material mappings between the same annular contours (r ↦ r): angular identity, θ ↦ θ, and θ ↦ θ + a sin θ with a = 0.5. Both give identical masks (Dice = 1, Hausdorff = 0). (c) Their circumferential stretch, λθ = 1 and λθ = 1 + a cos θ, differs; the latter ranges from 0.5 to 1.5 and preserves orientation for |a| < 1. This is an analytic counterexample, not a measurement of any estimator's error; the stretch ratio is not Green–Lagrange strain. [tool statement]

Alt text: Three schematic annuli showing cine, tagging and DENSE information; two annuli with identical outlines but differently distributed marker spokes; a plot of circumferential stretch versus angle contrasting a flat line with a cosine.

**Figure 3 — `Figure_3_method_timeline`** (190 × 147 mm)

Cine-CMR motion estimators by year and by the strongest validation evidence each cited source reports (Supplementary Table S3). Lanes group methods by family; marker fill encodes evidence type. Most cardiac-specific designs from 2018 to 2026 report mask or landmark agreement; material-sensitive references (known motion, DENSE or tagging) appear in 14 of 48 entries, in healthy or mixed cohorts or in simulation; a prescribed focal deficit appears in one independent synthetic evaluation (MRXCAT2.0 test of DeepStrain). Evidence classes were assigned from the Table S3 cells, which are abstract- or metadata-level readings; boundary feature tracking, a method family without a single year, is not plotted. Years 2001–2008 contain no entries and are compressed. [tool statement]

Alt text: Timeline from 1999 to 2026 with five horizontal lanes of labelled markers; marker colour shows whether each method was validated by mask agreement, a downstream label, a material-sensitive reference or prescribed focal motion; a bar legend counts 22, 8, 14, 1 and 3 entries.

**Figure 4 — `Figure_4_attribute_specific_recovery`** (190 × 107 mm)

Attribute-specific recovery in the one independent prescribed-focal test. (a) Ground-truth peak systolic strain in remote and scar tissue of the MRXCAT2.0 infarct case: radial and circumferential strain are largely abolished in the scar while longitudinal strain is almost unchanged, and ejection fraction remains 49%. (b) DeepStrain error across the four generated cases: circumferential strain error 0.02 ± 0.04, while radial strain is generally underestimated (−0.24 ± 0.21; infarct case −0.20 ± 0.21); per-case standard deviations overlap, so no case ordering is implied. Errors are case-level means over whole slices, not errors within the scar. (c) Status of the four abnormality attributes in this experiment. Values are as reported by the MRXCAT2.0 authors [mrxcat2023]; one scar geometry, one estimator, mid-ventricular short-axis slices; no new analysis. [tool statement]

Alt text: Grouped bar chart of ground-truth strain in remote versus scar tissue; three horizontal error bars for circumferential and radial estimator error; four labelled attribute boxes marked partial, not reported, not reported and not inspected.

**Figure 5 — `Figure_5_validation_targets_programme`** (190 × 141 mm)

What each validation target can establish, and a staged programme for regional or focal claims. (a) Five targets, the strongest claim each supports, and what each does not establish on its own. (b) Pre-specification followed by three stages, with the resources reviewed in Table 4 placed at the stage they can serve; counts denote resource units, not independent test participants. (c) Two fields with an equal global strain of −0.18 but different regional content: recovering the mean is not evidence of regional recovery. Conceptual synthesis; no study data. [tool statement]

Alt text: Top, a five-row table pairing validation targets with the claims they support and do not support; bottom left, a three-stage funnel from known-motion tests to clinical decisions with resource labels beside each stage; bottom right, a small plot of a uniform and a focal segmental strain profile sharing the same mean.

**Graphical abstract — `Graphical_abstract`** (2600 × 1000 px, 13:5)

Routine cine supports bounded regional strain claims; whether a focal abnormality's magnitude, location, extent and timing are recovered must be tested per attribute, per estimator and per acquisition.

## Supplement

**Supplementary Figure S1 — `Figure_S1_strain_definition_traps`** (190 × 124 mm)

The same motion gives different numbers under different definitions. (a) Engineering strain e and Green–Lagrange strain E = e + e²/2 differ by 0.02 at e = −0.20. (b) Endocardial, mid-wall and epicardial layers and local radial and circumferential axes. (c) One segmental curve read as peak systolic, end-systolic and post-systolic peak. (d) The minimum of a segment-mean curve differs from the mean of pointwise minima. Conceptual and analytic schematics with no measured scale. [tool statement]

**Supplementary Figure S2 — `Figure_S2_error_attributes_mapping_validity`** (190 × 109 mm)

Regional error attributes and mapping validity. (a) Reference and estimate profiles separating magnitude, location, extent and support errors. (b) Temporal magnitude and timing errors. (c) A smooth invertible mapping (det J > 0), which can still be wrong, and a folded mapping with det J ≤ 0 in the outlined cells. A single mean-squared error can hide each of these failures. Prescribed schematics with no measured scale. [tool statement]

**Supplementary Figure S3 — `Figure_S3_training_vs_inference_controls`** (190 × 67 mm)

Training-time versus inference-time controls. A training-loss weight requires matched retraining; a test-time parameter can be varied only when the implementation exposes it. Candidate models or outputs are compared on the same held-out cases under the same estimand, reference and attribute-specific losses. Conceptual schematic. [tool statement]
