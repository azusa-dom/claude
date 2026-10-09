# Figure contract

Core conclusion: The review figures should distinguish what cine-CMR observes, what an estimator infers, and what external validation can establish, while making attribute-specific failure modes visually explicit.

Results-level question: What evidence is required to support regional or focal cine-CMR strain claims, and where can the measurement chain fail?

Figure archetype: Schematic-led figure sequence with quantitative and analytic validation panels.

Target/output: Journal manuscript figures at the existing 160 mm main-text and 166 mm supplement widths; editable SVG/PDF plus high-resolution PNG previews.

Backend: Existing Python/Matplotlib plotting sources, with existing Typst/CeTZ retained for non-plot schematic assets.

Evidence hierarchy:

- Hero evidence: measurement-chain logic, analytic counterexample, attribute-specific validation.
- Validation evidence: method timeline, MRXCAT2.0 example, staged programme.
- Controls/robustness: strain-definition traps, error-attribute taxonomy, training-vs-inference control.

Palette semantics (derived from 沈香墨 #8D6449, 素绢白 #F8F3E7, 檀木棕 #C0997F, 棠梨绯 #E7A49A; checked with the dataviz palette validator on every colour pair that co-occurs in a figure):

- observed/input and neutral context: warm grey `#8E857D` on 素绢白 `#F8F3E7`;
- inferred/estimated: deepened 棠梨绯 `#C0584A` (tint `#F8E0DA`);
- reference/validation: deepened 沈香墨 `#7A4720` (tint `#EFE2D3`, light 檀木棕);
- secondary categorical distinction (Fig 3 downstream label, Fig 4 scar): `#CC5F4F`;
- weakest evidence class in Fig 3: intentional neutral `#B2AAA2`;
- supported / held: muted grey-green `#4E7470` (kept off the warm axis so it separates from error red);
- error / loss: `#A33A2E`, lines and symbols only;
- text: ink `#33261F` and muted `#776A62`, never a series colour;
- canvas: white.

Reviewer risks: colour must not be the sole carrier of meaning; tiny text, math scripts, dense timeline labels, and schematic arrows require final-size inspection; the scientific classifications and source-derived numbers are preserved rather than reinterpreted.
