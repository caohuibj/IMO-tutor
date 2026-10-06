# Post-Review Transfer

Use only after the current Attempt has been explicitly completed by the student with `此题完成` and finalized. This workflow extends the normal mathematical review into long-term transfer, abstraction, higher-mathematics connection, reinforcement, and optional visualization.

A checkpoint submission, even a complete and correct-looking proof, does **not** enter this workflow. Do not infer completion.

It does **not** replace `solution-review.md`. The complete feedback has six modules:

1. Core Review — produced by `solution-review.md`;
2. Historical Transfer;
3. Mathematical Extraction;
4. Higher Mathematics Bridge;
5. Reinforcement Problems;
6. Visual Model.

## Entry conditions and safety

1. Require the explicit completion trigger `此题完成`. The current Attempt must then be finalized: `submitted_at`, `verdict`, and `result_bucket` are known and the durable Attempt row has been materialized. A give-up/H6 finalization without this completion trigger does not activate the six-module extension.
2. For a redo, do not read previous solution content, previous `first_gap`, previous `key_insight`, previous hint history, or old notes until the new Attempt is finalized. After finalization, historical comparison is allowed.
3. Do not change the finalized verdict, score, first gap, or original transcription while running this workflow. If later analysis discovers a genuine review error, explicitly correct the review rather than silently mutating it.
4. Do not add new Sheet columns in this version. Rich transfer content belongs in the durable Problem note. Existing structured fields remain the retrieval backbone.

## Module 2 — Historical Transfer

Purpose: determine whether a previously observed mathematical weakness, technique issue, or structural difficulty has transferred, improved, or recurred in the current Attempt. Previous score is secondary; the mathematical issue is primary.

### Source of truth

Use durable `Attempts`, `Problem_Index`, and problem notes. Do not use remembered chat history as the historical database.

Before candidate retrieval, derive an **internal transfer signature** from the finalized current Attempt. This may include controlled `error_tags`, `method_tags`, `concept_tags`, and zero or more note-level Thinking Pattern IDs from `thinking-patterns.json`. This prepass is for retrieval only; it does not change the student-visible module order and does not attribute post-review ideas to the student.

### Candidate retrieval

Retrieve a small candidate set, normally 3–5 Attempts, in this priority order. Historical retrieval operates at **Attempt grain**:

- always exclude the current `attempt_id`;
- do not deduplicate by `problem_id` inside this internal transfer search;
- older Attempts of the same Problem are valid candidates;
- for the same Problem, require historical `attempt_no < current attempt_no`.

Then rank candidates in this priority order:

1. same or closely related note-level `TP.*` Thinking Pattern IDs when they represent the same proof architecture or reasoning move;
2. same or closely related `error_tags` and `error_targets`;
3. same student-used `method_tags`;
4. same or closely related `concept_tags`;
5. structurally similar blocker or proof pattern discoverable from `search_text` / note text;
6. same surface domain/topic only as a weak fallback.

Use a two-pass retrieval path when needed: first use structured Sheet fields for efficient recall; then use exact `TP.*` matches in durable Attempt blocks/notes to recover cross-domain structural analogues that ordinary method/domain filtering would miss. Do not introduce a vector database.

Prefer cross-problem structural similarity over superficial resemblance. A geometry problem and a number-theory problem may be highly relevant to each other if the same proof architecture or thinking pattern is being tested.

After candidate retrieval, inspect only the 1–2 most relevant historical Attempts/notes in depth.

### Transfer judgment

Use one of these note-level judgments when useful; these are **not** Sheet enums:

- `RESOLVED`: the old issue is now handled independently and correctly;
- `IMPROVED`: meaningful progress is visible but the issue is not yet stable;
- `RECURRED`: essentially the same blocker appears again;
- `NOT_TESTED`: a historical issue is relevant but the current problem did not actually test it;
- `NEW_ISSUE`: the old issue is handled, but a distinct new blocker appears.

Do not infer mastery from a high score alone. Do not infer failure from a low score alone.

### Output

Give only the historical comparisons that materially help training. For each, state:

- historical Problem/Attempt ID;
- the earlier mathematical issue in concise terms;
- what happened this time;
- the transfer judgment;
- the new training implication.

If there is no genuinely relevant historical Attempt, say so rather than forcing a comparison.

## Module 3 — Mathematical Extraction

Purpose: extract what should survive after the details of the problem are forgotten.

Separate three levels.

### Technique

A concrete executable mathematical action, such as a substitution, auxiliary construction, double count, valuation step, normalization, or change of representation.

### Insight

A structural realization that materially reduces the search space or explains why a technique works.

### Thinking Pattern

A higher-level reasoning move transferable across topics. Use the controlled Note-level IDs in `thinking-patterns.json` when one genuinely fits. Current IDs include:

- `TP.REFORMULATION`;
- `TP.LINEARIZATION`;
- `TP.LOCAL_TO_GLOBAL`;
- `TP.EXTREMALIZATION`;
- `TP.MINIMAL_COUNTEREXAMPLE`;
- `TP.INVARIANT`;
- `TP.MONOTONICITY`;
- `TP.SYMMETRY_BREAKING`;
- `TP.ENCODING`;
- `TP.DECOMPOSITION_RECONSTRUCTION`;
- `TP.DUAL_COUNTING`;
- `TP.DESCENT`.

These IDs are controlled vocabulary for durable notes and historical retrieval only in this version; they are **not new Sheet columns**. Do not invent alternate `TP.*` spellings. If none fits, omit the tag and explain the pattern in prose rather than creating a new ID ad hoc.

### Extraction rules

1. Extract only items that are mathematically important enough to reuse.
2. Distinguish what the student independently used/discovered from what entered through review, hint, reference solution, or post-review analysis. Do not attribute a post-review idea to the student.
3. For each retained item, answer:
   - **What is it?**
   - **What signal should trigger it next time?**
   - **Where else can it transfer?**
4. Prefer 1–4 strong items over a long inventory of minor observations.
5. For every retained Thinking Pattern, write its exact `TP.*` ID in the Attempt block of the durable note, together with the prose explanation and provenance (`STUDENT`, `HINT`, `REVIEW`, or `REFERENCE`).

## Module 4 — Higher Mathematics Bridge

Purpose: connect the olympiad phenomenon to a mathematically genuine higher-level concept so that a single problem becomes an entry point into broader mathematics.

The student may be assumed comfortable with first- and second-year calculus / analysis, linear algebra, and basic groups, rings, and fields. Use that level directly. Define concepts beyond it as needed.

### Connection quality

For each connection, explicitly classify the relationship as one of:

- `SPECIAL_CASE`: the olympiad phenomenon is literally a special case of a more general theorem/structure;
- `SAME_STRUCTURE`: not the same theorem, but the underlying mathematical mechanism is genuinely the same;
- `ANALOGY`: an illuminating analogy only; do not present it as a derivation or historical origin.

### Content requirements

Normally choose 1–3 strong connections. For each:

1. identify the elementary phenomenon in the current problem;
2. strip away the surface packaging and state the abstract structure;
3. name the higher-level concept and the branch(es) in which it lives;
4. give at least one substantive definition, formula, theorem statement, or short derivation;
5. explain what the higher-level viewpoint unifies or predicts beyond the current problem;
6. distinguish structural ancestry from historical origin. Do not claim that a contest technique “comes from” a modern theory unless that historical claim is actually supported.

Potential branches include, when genuinely relevant: real/complex analysis, abstract algebra, linear algebra, probability, analytic/probabilistic number theory, topology, projective geometry, differential geometry, dynamical systems, combinatorics, graph theory, optimization, and information theory.

When a historical claim, niche theorem, modern terminology, or current external reference materially matters, verify it with web research. Keep source-derived claims distinct from mathematical inference.

## Module 5 — Reinforcement Problems

Purpose: use the reviewed Attempt to choose external problems that test transfer rather than merely repeat surface form.

### Training fingerprint

Build an internal fingerprint from available information:

- domain;
- concept tags;
- student-used methods;
- extracted technique/insight/thinking pattern;
- current blocker / historical transfer result;
- current difficulty.

### Default recommendation set

Recommend at most three high-quality problems, and fewer when suitable candidates are unavailable:

1. **Near Transfer** — closely related structure, used to test immediate consolidation;
2. **Stretch** — similar core capability at roughly `+0.5` to `+1.5` difficulty when calibration is meaningful;
3. **Disguised Transfer** — different surface form but the same underlying reasoning pattern.

Do not mechanically fill all three slots.

### External search sources

Use current web search and prefer sources that support reliable identification and inspection. Useful source families include:

1. `KbsdJames/Omni-MATH` on Hugging Face for olympiad-level structured candidates with domain/difficulty annotations;
2. `Hothan/OlympiadBench` for bilingual olympiad-level mathematics, including Chinese material and multimodal items;
3. `AI-MO/aops` on Hugging Face as a broad AoPS-derived recall source;
4. Art of Problem Solving Wiki / Olympiad Archive and official contest pages for source verification when available.

Treat broad scraped/community datasets primarily as recall sources, not automatic authorities. Verify the selected problem mathematically and verify its source when possible.

### Recommendation quality gate

Before recommending a candidate:

1. inspect the actual problem, not only tags;
2. confirm that the relation to the current training target is substantive;
3. calibrate difficulty independently rather than trusting an external numeric label blindly;
4. reject trivial renamings or number-changed clones unless near-transfer drilling is specifically useful;
5. confirm source/identity when possible;
6. ensure the student-visible recommendation reason does not reveal the decisive method of the new problem.

If web access or source verification is insufficient, return fewer recommendations rather than fabricating candidates.

### Student-visible output

For each recommended problem, give:

- source and problem identifier when available;
- non-spoiling training purpose;
- approximate difficulty on the project scale;
- relation type: Near Transfer / Stretch / Disguised Transfer;
- a **problem-only / official statement link** when safely available.

If the only available page exposes the solution, key lemma, decisive construction, or decisive method alongside the statement, do **not** give that direct student-facing link. Give the source + identifier instead and keep the mixed solution page internal for verification. When the student selects the problem, retrieve only the statement into a fresh H0 working Chat.

Do not expose an external solution, key lemma, decisive construction, or decisive method before the new Attempt.

A recommended problem is **not** automatically a Problem record. Only after the student selects it should it enter a fresh working Chat and normal `problem-intake.md` at H0.

## Module 6 — Visual Model

Purpose: create a memorable mathematical mental image, not decorative artwork and not a substitute for proof.

This module is optional. Use it when visualization materially strengthens memory, structure recognition, or the Higher Mathematics Bridge.

### When to visualize

Prefer visualization when the problem is driven by:

- a geometric configuration;
- a transformation or deformation;
- a graph/network/state-space model;
- a combinatorial encoding;
- a valuation/divisibility hierarchy;
- symmetry or orbit structure;
- a function/inequality/convexity picture;
- a higher-level structure that becomes clearer spatially.

Skip when the visual would add little beyond the written mathematics.

### Visual modes

Choose one primary mode:

- **Static Concept Card** — one strong image capturing the core configuration or abstraction;
- **Multi-frame Storyboard** — usually 3–5 frames showing a mathematical transformation or proof idea unfolding;
- **Abstract Structural Visualization** — a diagram of states, layers, mappings, graphs, algebraic structure, or higher-level connection.

### Generation rules

1. Generate only after the current Attempt is finalized and the relevant mathematical content is unlocked. Never use a visual to leak a decisive idea during H0–H5 unless the hint level explicitly permits it.
2. Mathematical fidelity dominates aesthetics. Keep labels sparse and legible; encode correspondence consistently.
3. For geometry, preserve all stated incidences, collinearities, cyclic relations, orientations, and dependencies. Do not invent metric relationships merely to make the picture look balanced.
4. For algebra/number theory/combinatorics, visualize the underlying model rather than drawing generic mathematical decoration.
5. A visual may support intuition, but explicitly avoid treating an approximate drawing as proof.
6. Prefer a 3Blue1Brown-like explanatory visual language: progressive structure, strong spatial hierarchy, minimal clutter, and a clear visual invariant or transformation. Do not imitate proprietary branding or copy a specific existing frame.

### Mathematical QA gate

Before generation, write a compact internal **visual specification** containing:

- required incidences / collinearities / cyclic relations / tangencies / order relations / graph adjacencies / mapping correspondences;
- any relationships that must **not** be implied unless they are given or proved (for example equality, perpendicularity, symmetry, concurrency, or scale);
- whether the image is intended to be mathematically faithful or only schematic.

After generation, inspect the visual against that specification before archiving or treating it as part of the durable feedback.

- If a required mathematical relation is wrong, a label is attached to the wrong object, or the image materially implies a false relation, **reject and regenerate**.
- Simplify the visual rather than accepting an attractive but mathematically misleading image.
- If exact geometric/metric fidelity cannot be verified reliably, use a conceptual schematic and label it explicitly `SCHEMATIC — not metrically faithful`.
- Never treat a generated diagram as evidence for a proof step.

### Visual output

Accompany the image with:

- **Visualization goal** — what the image is meant to make memorable;
- **Visual type** — one of the three modes above;
- **Caption** — concise mathematical explanation;
- **Memory hook** — one short sentence that should be recalled later;
- **Higher link** — optional connection back to Module 4.

If the generated visual is available as an uploadable asset, archive it in the Problem folder using `<attempt_id>-visual-<NN>.<ext>` and include its Drive URL in the durable note. If it cannot actually be uploaded, do not claim durable archival; the note may record that the visual was generated in chat but not durably archived.

Do not generate a Visual Model for a newly recommended reinforcement problem before that new Problem's Attempt is finalized, unless the user explicitly requests a permissible hint/visual under the hint workflow.

## Full six-module feedback contract

Only after `此题完成`, the student-facing feedback should contain, in order:

1. **Core Review** — correctness, score, first gap, valid remainder, strategy, rigor/writing, repair, proof compression;
2. **Historical Transfer** — whether earlier related weaknesses were resolved, improved, or repeated;
3. **Mathematical Extraction** — techniques, insights, and thinking patterns worth retaining;
4. **Higher Mathematics Bridge** — genuine higher-level structures with relationship strength made explicit;
5. **Reinforcement Problems** — verified near/stretched/disguised transfer opportunities without spoilers;
6. **Visual Model** — optional mathematical visualization when it has clear learning value.

Keep the feedback selective. The purpose is not to make every response long; it is to ensure that every completed problem can contribute to longitudinal skill transfer and broader mathematical understanding.