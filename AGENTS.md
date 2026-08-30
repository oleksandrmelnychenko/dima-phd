# Workspace editing rules

* All paths in this file are relative to the repository root.
* Make changes only in:

  * `my/**`;
  * `memory/**`;
  * `.agents/skills/dissertation-memory/**`;
  * `.codex/agents/memory-auditor.toml`;
  * `.agents/skills/use-academic-ontologies/**`, when creating, validating, or maintaining the project ontology skill;
  * `AGENTS.md`, and only when the user explicitly requests project-instruction changes.
* Treat every other repository path as read-only.
* Treat `suport_info/**` as immutable source material. Never create, edit, move, rename, delete, or silently repair files there unless a later explicit user instruction changes this policy.
* Store generated documents, normalized data, reports, dissertation drafts, revised sections, audit reports, and proposed ontology extensions only under `my/`.
* Preserve unrelated existing user changes.

# Dissertation memory

* Before dissertation drafting, rewriting, or review, read `memory/README.md` and `memory/MEMORY.md` and use `$dissertation-memory`.
* When subagents are available, run `memory_auditor` as an independent read-only check; the main agent is the only writer.
* Log new feedback as `Очікує рішення`. Promote it to `Погоджено` or `Уникати` only after the author's explicit decision.
* Do not change dissertation text before the author approves the proposed wording.

# Instruction priority

When instructions conflict, use this priority order:

1. Direct instruction from the user for the current task.
2. Explicit project-specific normative materials designated by the user.
3. Verified facts, experimental results, formulas, source materials, and established project decisions.
4. This `AGENTS.md`.
5. Applicable project skills.
6. Generic academic-writing conventions.

Never allow a generic skill recommendation to override verified project facts or an explicit user requirement.

# Skill routing

## Dissertation work

* Before substantive work involving the dissertation, use `$doctoral-dissertation` from:

  * `.agents/skills/doctoral-dissertation/SKILL.md`.
* Treat `$doctoral-dissertation` as the primary workflow skill for:

  * dissertation architecture;
  * chapter, section, subsection, paragraph, and sentence organization;
  * drafting or revising dissertation sections;
  * literature review synthesis;
  * theoretical and methodological sections;
  * methods, results, and discussion;
  * scientific claims and their evidence;
  * research-question closure;
  * scientific contribution and novelty formulation;
  * consistency between chapters;
  * dissertation-wide audits;
  * preparation for submission or defense.
* When `$doctoral-dissertation` refers to supporting files under its own directory, read the relevant `tasks`, `references`, and `examples` before performing the corresponding task.
* Do not mechanically apply generic dissertation structures when the current project already contains an approved or user-defined structure.
* Existing project structure, direct user instructions, verified research materials, and task-specific requirements take priority over generic examples in the skill.
* Never import cases, samples, variables, methods, datasets, chapter names, scientific claims, conclusions, numerical values, or examples from another dissertation or from examples contained in the skill.
* Reuse only workflow, reasoning, audit, evidence-control, and writing rules from the skill.

## Dissertation TikZ figures

* Before creating, materially revising, or visually auditing a block diagram, architecture diagram, process diagram, or flowchart in TikZ, use `$tikz-flowchart` from:

  * `.agents/skills/tikz-flowchart/SKILL.md`.
* Use `$doctoral-dissertation` and `$tikz-flowchart` together for dissertation figures:

  * `$doctoral-dissertation` governs the scientific function of the figure, its evidence relationship, textual introduction, caption, interpretation, and place in the dissertation argument;
  * `$tikz-flowchart` governs node layout, orthogonal connector routing, side-anchor selection, grouping, label concision, rendering, and visual review.
* For an existing dissertation figure, treat the established project TikZ styles as the figure's theme. Do not restyle an existing figure with the bundled Material-like or Anthropic theme unless the author explicitly requests that change.
* For a new figure without an approved project style, choose one theme as required by `$tikz-flowchart`; do not mix visual systems within one figure.
* Plan the layout before writing or changing `\node`, `\draw`, or `\path` commands.
* Render the actual figure and run an independent visual review by a subagent before presenting it as complete. The main agent remains the only writer and must synthesize the review.
* Apply the project-specific `Dissertation figure preparation rules` below even if a bundled theme or example permits a different connector style.

## Academic ontology work

* Before substantive work involving a scientific publication, scientific article, publication structure, bibliography, publication ethics, hypothesis, scientific novelty, or a working program of an academic discipline, use `$use-academic-ontologies` from:

  * `.agents/skills/use-academic-ontologies/SKILL.md`.
* Treat both ontology files in `suport_info` as incomplete draft context, not as formal schemas or universal normative standards.
* Do not invent concepts, relations, requirements, cardinalities, or exceptions that are absent from the applicable ontology reference.
* Keep ontology-supported facts, user-provided content, external additions, and proposed ontology extensions explicitly separate.
* If required information is missing or contradictory, identify the gap instead of silently assuming an answer.
* Use external domain knowledge only when the user explicitly permits it, and label it separately from ontology-backed content.
* Give direct user instructions and user-designated task-specific normative materials priority over the ontology; do not attribute those additions to the ontology.
* For a working program, apply the first source block as the shared `base`; use `base` for a mandatory discipline and `base + explicit elective overrides` for an elective discipline. For an elective-only conflict, the explicit elective rule wins.

## Using both skills

* When a dissertation task also concerns concepts covered by the academic ontologies, use both `$doctoral-dissertation` and `$use-academic-ontologies`.
* Their responsibilities are different:

  * `$doctoral-dissertation` governs dissertation workflow, structure, argumentation, evidence-to-claim alignment, section functions, revision, scientific interpretation, and dissertation-wide consistency;
  * `$use-academic-ontologies` governs interpretation and use of concepts represented in the project ontology materials.
* Do not allow one skill to silently override the factual constraints of the other.
* If the skills appear to conflict:

  1. follow the user's direct instruction;
  2. follow explicit project-specific normative materials;
  3. preserve verified project facts and evidence;
  4. preserve ontology-backed meaning for ontology-governed concepts;
  5. use `$doctoral-dissertation` for organization, reasoning, evidence control, and presentation.
* A workflow recommendation from `$doctoral-dissertation` must not be presented as an ontology requirement.
* An ontology relation must not be presented as a mandatory dissertation-writing convention unless the project materials explicitly establish it.

# Dissertation evidence rules

* Treat the dissertation as an evidence-controlled research manuscript, not as a prose-generation task.
* Evidence and verified project facts have priority over expected results, old outlines, draft conclusions, or stylistic convenience.

## Before substantial drafting or restructuring

Determine:

* the scientific function of the target chapter, section, or subsection;
* the research question or problem it addresses;
* the scientific statement that must be established;
* the available evidence;
* the expected scholarly conclusion supported by that evidence;
* its relationship to preceding and following sections;
* whether changes may affect formulas, terminology, figures, tables, conclusions, or other chapters.

For major dissertation work, apply the `$doctoral-dissertation` evidence chain:

`research facts → evidence → research questions → chapter functions → section judgments → paragraph reasoning → precise prose`

Every central scientific claim must have an identifiable evidence anchor, such as:

* a verified scientific source;
* a formula or formal model;
* an algorithm;
* a table;
* a figure;
* an experimental result;
* a dataset;
* a validated software artifact;
* another explicit project source.

If a strong claim has no sufficient evidence anchor:

* do not invent support;
* downgrade the claim;
* mark the evidence gap;
* or omit the claim.

Never fabricate:

* citations;
* bibliographic metadata;
* numerical results;
* experiments;
* datasets;
* formulas;
* metrics;
* statistical significance;
* scientific novelty;
* validation results;
* software behavior;
* causal mechanisms;
* comparison results;
* advantages not supported by evidence.

Distinguish clearly between:

* verified project facts;
* observations;
* formal definitions;
* technical implementation facts;
* experimental results;
* scientific interpretation;
* assumptions;
* hypotheses;
* proposed changes;
* generalized conclusions;
* missing evidence.

# Dissertation writing rules

* Respond in Ukrainian by default and preserve the canonical Ukrainian entity names.
* Write dissertation prose in mature formal Ukrainian academic style appropriate for a doctoral dissertation.
* Preserve established project terminology consistently across chapters.
* Prefer precise Ukrainian scientific and technical terminology where an established equivalent exists.
* Avoid unnecessary Anglicisms, literal English calques, conversational expressions, journalistic wording, promotional wording, and generic AI-style filler.
* Do not write meta-commentary inside dissertation prose about:

  * generation of the text;
  * editing process;
  * prompts;
  * reasoning process;
  * manuscript revision history;
  * what the author initially intended to write.
* The dissertation body must present the completed scientific work rather than the drafting process.
* Match the strength of every scientific statement to the strength of its evidence.
* Do not systematically weaken well-supported conclusions with excessive hedging.
* Do not use strong formulations such as `доведено`, `гарантує`, `забезпечує перевагу`, `однозначно підтверджує`, or equivalent wording unless the available evidence justifies them.
* Do not artificially increase textual complexity merely to make the prose appear more scientific.
* Prefer semantic precision over lexical complexity.

## Evidence-based scientific and academic strengthening

* Do not limit substantive rewriting to grammar, terminology, and stylistic polishing. Where the available project evidence permits, strengthen the scientific and academic quality of the text by making its research function, central scholarly judgment, logical relationship to the surrounding argument, evidence anchor, scientific interpretation, and justified local conclusion more explicit.
* Scientific and academic strengthening means improving analytical depth, precision, evidence-to-claim alignment, and the explanatory connection between facts, methods, results, and conclusions while preserving the established scientific content and the original direction of the argument.
* Do not interpret strengthening as permission to intensify claim wording, add unsupported causality, generalize beyond the evidence, introduce new scientific entities, or replace clear language with decorative complexity.
* If the source material does not support a stronger scientific judgment or the required interpretation, preserve the justified claim strength and identify the evidence or reasoning gap instead of concealing it through academic-sounding prose.

# Academic-professorial writing style

Every substantive dissertation paragraph must read as part of a mature scientific manuscript written by a domain specialist.

Academic-professorial style means:

* terminological precision;
* mature scientific interpretation;
* logically complete reasoning;
* restrained and objective wording;
* clear relationships between concepts;
* justified causal or functional statements;
* stable terminology;
* natural Ukrainian syntax;
* absence of conversational wording;
* absence of advertising or journalistic expressions;
* absence of unnecessary foreign terminology;
* absence of decorative scientism;
* absence of vague phrases that do not add scientific information.

## Ukrainian terminology and Anglicisms

* Before retaining an English-derived term, determine whether an established Ukrainian scientific or technical equivalent exists.
* If a clear established Ukrainian equivalent exists and preserves the intended meaning, use it.
* Retain an English term when:

  * it is a proper name;
  * it is an established model, algorithm, protocol, standard, library, technology, or software name;
  * it is a standardized abbreviation;
  * no sufficiently precise Ukrainian equivalent exists;
  * the original term is required for reproducibility or identification.
* When an English term must be retained, introduce it consistently and do not alternate arbitrarily between variants.
* Avoid literal translation of English academic syntax.
* Rewrite constructions that are grammatically Ukrainian but clearly preserve English sentence structure.
* Do not replace one established Ukrainian term with multiple synonyms merely to avoid lexical repetition.
* One scientific concept should normally have one stable canonical term throughout the dissertation.
* Technical names may remain unchanged when translation would reduce precision.

## Words and patterns requiring restraint

Avoid or use only when scientifically justified:

* `сучасний`;
* `у контексті`;
* `файл`, when a more precise Ukrainian term is appropriate;
* `плагін`;
* `ефективність`, unless a criterion or metric is defined;
* `продуктивність`, unless the measured property is actually performance;
* `оптимальний`, unless optimization has been established;
* `унікальний`;
* `інноваційний`;
* `очевидно`;
* `безумовно`;
* `варто зазначити`;
* `слід наголосити`;
* `необхідно відзначити`;
* `як відомо`;
* `можна зробити висновок`, when the evidence relationship can be stated directly.

Do not prohibit a term mechanically when it is technically correct. Replace it only when the alternative is more precise and scientifically appropriate.

# Scientific interpretation requirement

Dissertation prose must not stop at technical description, enumeration of facts, presentation of a formula, or reporting of a numerical result when scientific interpretation is required.

For every scientifically meaningful result, dependency, model element, criterion, formula, or experimental observation, determine whether the reader needs an explanation of its scientific meaning.

Scientific interpretation should answer, where applicable:

* what the presented result means;
* what scientific property it characterizes;
* what dependency or regularity it reveals;
* why it is relevant to the research problem;
* which research question or task it addresses;
* how it relates to the proposed model, method, or information technology;
* what follows from it for the scientific argument;
* what limitation or boundary of inference applies;
* whether it supports, refines, or limits a hypothesis or prior conclusion.

Do not add interpretation mechanically after every sentence.

Interpretation must be included where it is necessary to understand the scientific significance of the presented material.

Scientific interpretation must be evidence-based.

Do not:

* invent causal explanations;
* present an assumption as an established mechanism;
* transform association into causation;
* infer generality from a limited experiment without justification;
* treat implementation success as validation of a scientific hypothesis.

When evidence supports only:

* correspondence;
* association;
* tendency;
* consistency;
* difference;
* observed dependence;

preserve that level of inference.

When introducing a formula, explain not only what it computes but, where scientifically relevant, what property, relationship, criterion, or process it formalizes.

When presenting an experimental result, explain not only whether a metric increased or decreased, but what the change means for:

* the tested research hypothesis;
* the scientific task;
* the proposed method;
* the analyzed property;
* the information technology;
* the boundary of applicability.

# Separation of technical description and scientific claims

Never treat technical implementation and scientific interpretation as the same type of statement.

Explicitly distinguish:

1. the scientific problem;
2. the proposed scientific model, method, criterion, or proposition;
3. its formalization;
4. the technical realization;
5. the experimental procedure;
6. the observed result;
7. the scientific interpretation;
8. the conclusion supported by the evidence.

Use the following reasoning chain when applicable:

`scientific problem → scientific proposition/model/method → formalization → technical realization → experiment → observed result → scientific interpretation → conclusion`

## Technical statements

Technical statements may describe:

* software components;
* programming languages;
* libraries;
* application programming interfaces;
* modules;
* classes;
* data structures;
* data-processing stages;
* storage mechanisms;
* network interactions;
* deployment;
* implementation architecture;
* computational procedures;
* technical parameters;
* software integration.

These statements describe how the research artifact is implemented.

## Scientific statements

Scientific statements concern:

* properties;
* relationships;
* regularities;
* formal models;
* methods;
* criteria;
* hypotheses;
* experimental dependencies;
* limitations;
* generalized conclusions;
* scientific contribution;
* scientific novelty;
* conditions of applicability.

The existence of a software implementation does not by itself establish:

* scientific novelty;
* correctness of a model;
* superiority of a method;
* effectiveness;
* robustness;
* generalizability;
* practical significance;
* validity of a hypothesis.

A technical implementation may realize a scientific model or method, but this relationship must be stated explicitly.

## Do not use implementation as proof

Avoid patterns equivalent to:

* `реалізовано модуль, що доводить...`;
* `створений компонент забезпечує ефективність методу...`;
* `використання бібліотеки підтверджує...`;
* `архітектура програмної системи доводить перевагу...`;
* `реалізація алгоритму підтверджує наукову новизну...`.

Prefer a separated structure:

* scientific proposition;
* implementation that operationalizes it;
* experiment that evaluates it;
* observed result;
* scientific interpretation supported by that result.

For example, use reasoning of the form:

`Для реалізації запропонованого методу розроблено...`

then:

`Експериментальне оцінювання реалізації показало...`

then:

`Отриманий результат характеризує...`

then, if justified:

`Наукове значення встановленої залежності полягає у...`

# Structural writing rules

Use the following functional hierarchy unless explicit project requirements specify otherwise:

* one chapter solves one major scientific problem;
* one section solves one class of subproblems;
* one subsection establishes one central scholarly judgment;
* one paragraph performs one reasoning move;
* one sentence carries one primary information function.

A scientific paragraph should normally follow this logic when applicable:

1. central scientific point;
2. evidence, formalization, explanation, or development;
3. scientific interpretation;
4. local conclusion or transition.

Do not create paragraphs that merely accumulate unrelated facts.

Do not create paragraphs consisting primarily of generic introductory statements without a clear scientific function.

Each paragraph must justify its presence in the argument.

# Paragraph continuity and contextual coherence

Never rewrite, generate, or substantially revise a dissertation paragraph in isolation when adjacent context is available.

Before rewriting a paragraph, read at minimum:

* the complete preceding paragraph;
* the target paragraph;
* the complete following paragraph, when it exists.

For substantial revision, read the entire containing subsection and, where needed, neighboring subsections.

A rewritten paragraph must be a natural continuation of the preceding scientific reasoning.

It must not read as an independently generated fragment.

## Determine the paragraph relation

Before rewriting, determine how the target paragraph relates to the preceding paragraph.

Possible relations include:

* continuation;
* specification;
* development;
* explanation;
* consequence;
* comparison;
* contrast;
* generalization;
* transition from problem to method;
* transition from model to formalization;
* transition from formalization to implementation;
* transition from implementation to experiment;
* transition from experiment to result;
* transition from result to scientific interpretation;
* transition from local conclusion to the next research issue.

The opening sentence of the rewritten paragraph must reflect the information already established before it.

Do not restart the discussion as if the preceding paragraph did not exist.

Do not unnecessarily repeat:

* definitions;
* abbreviations;
* already established facts;
* research objectives;
* model descriptions;
* conclusions from the immediately preceding paragraph.

Use the previous paragraph's conclusion as the starting condition for the next reasoning move.

## Incoming and outgoing coherence

A rewritten paragraph must preserve both:

* the incoming connection from the preceding paragraph;
* the outgoing connection to the following paragraph.

Do not rewrite a paragraph in a way that:

* makes the following paragraph redundant;
* anticipates and exhausts the following paragraph's argument;
* creates a contradiction with the following paragraph;
* introduces a new topic without a logical bridge;
* changes the level of abstraction abruptly;
* changes terminology without justification.

For every substantial paragraph rewrite, verify:

`previous paragraph → rewritten paragraph → following paragraph`

The three paragraphs should read as one continuous scientific argument.

## Semantic continuity

Maintain continuity of:

* scientific object;
* terminology;
* level of abstraction;
* cause-and-effect relations;
* assumptions;
* notation;
* research question;
* argument direction.

Pronouns and referential expressions must have clear antecedents.

Do not use a different term for the same object merely to vary style.

Do not introduce a new scientific object without explaining its relation to the previous one.

## Transition words

Do not use transition words merely to create the appearance of cohesion.

Use constructions such as:

* `водночас`;
* `отже`;
* `відповідно`;
* `разом із тим`;
* `з огляду на це`;
* `унаслідок цього`;
* `таким чином`;
* `при цьому`;

only when they accurately express the logical relationship.

Semantic continuity is more important than decorative linking words.

## Context-aware paragraph rewriting workflow

Before rewriting an existing paragraph:

1. Read the preceding paragraph.
2. Identify its final scientific statement, unresolved issue, limitation, or intermediate conclusion.
3. Determine what the target paragraph must add.
4. Identify the single scientific function of the target paragraph.
5. Read the following paragraph.
6. Determine what scientific point the target paragraph must prepare.
7. Rewrite the target paragraph.
8. Re-read the sequence:
   `previous → rewritten → following`.
9. Check terminology, argument direction, and evidence continuity.
10. Adjust the rewritten paragraph if it appears detachable from its local context.

If the rewritten paragraph can be moved to another part of the chapter without noticeably affecting the logic, its contextual connection is probably insufficient.

# Paragraph-level scientific quality check

Before considering a substantive paragraph complete, verify:

1. What is the paragraph's single central scientific function?
2. Does it logically continue the preceding paragraph?
3. Does it prepare the following paragraph?
4. Is the terminology consistent with adjacent text?
5. Are avoidable Anglicisms or English calques present?
6. Is technical implementation clearly distinguished from scientific interpretation?
7. Is evidence clearly distinguished from interpretation?
8. Does the interpretation follow from the evidence?
9. Is the strength of the claim justified?
10. Does the paragraph explain why the presented material matters scientifically?
11. Does it advance the dissertation argument rather than merely describe implementation?
12. Does it unnecessarily repeat something already established?
13. Can any sentence be removed without losing scientific information?
14. Does the paragraph read naturally as part of one author's continuous academic argument?

# Literature review rules

In literature reviews, organize material primarily by:

* research problem;
* concept;
* method;
* approach;
* model;
* limitation;
* contradiction;
* unresolved research gap.

Avoid turning a literature review into a sequential catalogue:

`Автор А запропонував... Автор Б дослідив... Автор В розробив...`

Use individual sources as evidence within a scientific synthesis rather than as the organizing principle.

For each meaningful group of studies, establish where applicable:

* what is already known;
* where approaches converge;
* where they differ;
* what methodological limitations remain;
* what problem is insufficiently solved;
* why this gap matters for the dissertation.

The literature review must lead logically toward the research problem, tasks, methods, or scientific propositions developed in the dissertation.

# Methods, results, and discussion separation

Keep methods, results, and discussion functionally distinct unless the approved dissertation structure explicitly combines them.

## Methods

Methods should explain:

* what was done;
* why the method is suitable;
* what is formalized;
* what assumptions apply;
* how reproducibility is ensured.

## Results

Results should report:

* verified observations;
* measured values;
* figures;
* tables;
* comparisons;
* statistical or computational outcomes.

Do not silently introduce unsupported explanations into the results description.

## Discussion and scientific interpretation

Discussion should explain:

* what the result means;
* how it relates to the research question;
* how it relates to the proposed method or model;
* whether it supports or limits a scientific proposition;
* what scientific implication follows;
* which boundaries remain.

Do not merely repeat numerical results in different words.

# Formula and notation rules

* Preserve the mathematical meaning of existing formulas unless the user explicitly requests a mathematical correction or modification.
* Before modifying notation, search its use across the relevant dissertation materials.
* Use letters of the Latin alphabet for alphabetic identifiers in formulas. Denote sets with uppercase Latin letters.
* Established Greek letters and special mathematical symbols may be retained when they have a conventional meaning or are already defined in the manuscript. Do not replace existing notation without searching all dependent uses and assessing the impact of the change.
* Apply the formula-formatting requirements of Order of the Ministry of Education and Science of Ukraine No. 40 of 12 January 2017 and SOU 207.01:2025 of Khmelnytskyi National University, clauses 5.13.1--5.13.10, within their stated scope.
* Place a displayed formula on a separate centered line immediately after the text that first mentions it. Keep at least one line of vertical space before and after the display.
* Number only formulas referenced in the text. In the main text, use either continuous Arabic numbering or the established chapter-based form `chapter.formula`; place the number in parentheses at the right edge. In appendices, use `APPENDIX-LETTER.formula`, for example `(А.3)`.
* Use LaTeX labels and cross-references for numbered formulas. Do not hard-code formula numbers in prose.
* Maintain consistent notation for:

  * scalars;
  * vectors;
  * matrices;
  * sets;
  * functions;
  * indices;
  * classes;
  * thresholds;
  * weighting coefficients.
* Introduce each formula in the text before presenting it.
* Explain what the formula determines, models, computes, or formalizes.
* When scientifically relevant, explain the property or relationship represented by the formula, not only the calculation it performs.
* Define newly introduced symbols directly below the formula in the order in which they appear. Begin the explanation on a new unindented line with:

  * `де ...`

  Do not place a colon after `де`.
* For physical quantities, use notation consistent with DSTU ISO 80000-1:2016 and state the applicable measurement units. Leave a space between a numerical value and a unit except for plane-angle units conventionally written next to the value.
* Separate consecutive displayed formulas that have no intervening prose with commas.
* Treat every formula as part of its sentence and use the punctuation required by that sentence. Do not require a comma after every formula mechanically.
* Break a long formula only at an operation sign, repeat the sign at the end of the preceding line and at the start of the next line, use `\times` when a multiplication sign is needed at a break, and avoid breaking at a division colon.
* Keep subscripts, superscripts, and exponents consistently sized throughout the manuscript; they must remain smaller than the base symbol.
* Create formula symbols with LaTeX mathematical environments or another appropriate mathematical editor; do not insert formulas as raster images.
* Do not begin an explanatory sentence with `Формула`.
* When referring to a numbered formula:

  1. first establish the textual reference to the formula;
  2. then explain its meaning or use.
* Do not add mathematical expressions merely to make a section appear more scientific.
* Do not modify:

  * indices;
  * coefficients;
  * thresholds;
  * sets;
  * functions;
  * variable meanings;

  merely for stylistic consistency without checking their use across the project.
* If a proposed notation change has cross-chapter consequences, perform an impact scan before applying it.

# Dissertation figure preparation rules

Every dissertation figure must have a clear scientific function, a textual reference before its appearance, and a substantive interpretation in the surrounding text.

## Block diagrams and flowcharts

For every new or materially revised block diagram, architecture diagram, process diagram, or flowchart:

* use an editable vector source when practicable; prefer the existing TikZ workflow for figures under `title/figures_tex/` unless another format is justified by the task;
* plan the node layout before routing connectors;
* keep blocks, containers, labels, connectors, arrowheads, and annotations from overlapping or being clipped;
* use only horizontal and vertical connector segments; diagonal connectors are not permitted;
* form direction changes as 90-degree turns; a small corner radius may be used when it improves readability without obscuring the route;
* connect arrows to explicit side anchors so that they enter the block boundary perpendicularly and terminate at the boundary;
* do not route connectors through blocks, labels, captions, or unrelated containers;
* minimize connector crossings; if crossings remain, reposition blocks or reroute connectors before considering the figure complete;
* keep related blocks aligned and maintain consistent spacing, block sizes, typography, line widths, arrowheads, and visual hierarchy;
* use concise labels and ensure that all text remains readable at the actual dissertation page scale.

The orthogonal-connector rule applies to block-based diagrams. It does not prohibit scientifically meaningful curves, regression lines, plotted data, axes, geometric constructions, or other non-connector elements in data visualizations and scientific plots.

## Rendering and visual verification

Do not approve a figure by inspecting source code alone.

Before considering a new or revised figure complete:

1. compile or export the actual artifact;
2. inspect the resulting PDF or a high-resolution render at the intended page scale;
3. verify that no block, label, connector, arrowhead, legend, or annotation overlaps, is clipped, or extends outside the intended figure area;
4. verify that connectors follow the required routes and that arrow direction is unambiguous;
5. verify semantic agreement among the figure, its caption, its first textual reference, and the interpretation that follows;
6. after every geometry change, render and inspect the figure again because a local correction may introduce a new overlap or routing defect.

Photographs, screenshots, raster maps, heatmaps, and other inherently raster materials are not required to be converted into vector objects. For such materials, preserve an editable source or a reproducible generation procedure when available and verify resolution, legibility, and cropping at the final page scale.

# Terminology consistency

Maintain a canonical term for each core concept.

Before replacing a term:

1. search its current use across relevant dissertation materials;
2. determine whether it is a defined project term;
3. determine whether formulas, figures, tables, or classifications depend on it;
4. avoid creating competing synonyms.

Do not perform synonym rotation to avoid repetition when repetition is necessary for terminological precision.

Distinguish between:

* scientific terms;
* implementation terms;
* proper names;
* abbreviations;
* model names;
* protocol names;
* software identifiers.

# Scientific novelty and contribution

Do not formulate scientific novelty merely from:

* implementation details;
* use of a particular programming language;
* integration of existing libraries;
* deployment architecture;
* software packaging;
* interface development.

Scientific novelty must be linked to a scientifically defensible contribution such as:

* a model;
* a method;
* a formalization;
* a criterion;
* a new relationship;
* a new integration principle;
* a validated scientific procedure;
* another explicitly supported contribution.

Do not invent novelty to fill a dissertation section.

When scientific novelty is discussed, use `$use-academic-ontologies` where applicable and preserve the distinction between:

* ontology-backed concepts;
* verified project contribution;
* user-approved formulations;
* proposed wording.

# Revision and audit workflow

Before editing an existing dissertation section:

1. Read the target section.
2. Read sufficient preceding and following material to understand its role.
3. Identify the scientific function of the section.
4. Identify relevant research questions.
5. Identify relevant formulas.
6. Identify relevant figures and tables.
7. Identify relevant citations.
8. Identify canonical terminology.
9. Identify dependencies on other chapters.
10. Determine whether the requested change is local or systemic.

For substantial revisions, check in this order:

1. factual integrity;
2. evidence completeness;
3. scientific correctness;
4. methodological correctness;
5. claim–evidence alignment;
6. scientific interpretation;
7. separation of scientific and technical statements;
8. chapter and section logic;
9. paragraph continuity;
10. terminology;
11. formulas and notation;
12. academic-professorial Ukrainian style;
13. Anglicisms and calques;
14. formatting.

Do not polish wording while leaving a known scientific, factual, methodological, or structural defect unresolved.

# Impact scan after material changes

After changing a central:

* term;
* formula;
* classification;
* research question;
* scientific claim;
* scientific novelty statement;
* contribution;
* method;
* experimental result;
* interpretation;
* model component;

perform an impact scan across affected dissertation materials.

Check whether the change affects:

* introduction;
* research tasks;
* theoretical sections;
* methodology;
* formulas;
* figures;
* tables;
* experimental sections;
* conclusions;
* scientific novelty;
* practical significance;
* abbreviations;
* terminology.

Do not rewrite unaffected sections merely for stylistic uniformity.

Preserve unrelated existing content and user changes.

# Rewriting rules

When the user asks to rewrite, improve, expand, shorten, or academically refine existing dissertation prose:

* preserve the scientific meaning unless semantic change is explicitly requested;
* preserve verified numerical values;
* preserve formulas;
* preserve evidence relationships;
* preserve citations unless a citation problem is identified;
* preserve canonical terminology;
* preserve the paragraph's role in the surrounding argument;
* read adjacent paragraphs before rewriting;
* do not create a stylistically polished paragraph that becomes logically disconnected from its context.

After rewriting, compare the new version against the original for:

* scientific meaning;
* claim strength;
* terminology;
* causal interpretation;
* evidence scope;
* relation to adjacent paragraphs.

# Completion reporting

After substantive dissertation work, report concisely:

* which files were changed;
* what substantive changes were made;
* whether scientific meaning changed;
* whether formulas changed;
* whether numerical values changed;
* whether citations changed;
* whether terminology changed;
* whether scientific claims changed;
* whether scientific interpretation changed;
* whether cross-section dependencies were checked;
* which evidence gaps or unresolved issues remain.

Do not describe a chapter, section, paragraph, or dissertation as:

* `final`;
* `verified`;
* `submission-ready`;
* `fully validated`;

unless the exact current artifact has actually undergone the relevant checks.

# Final quality principle

A dissertation fragment is complete only when it satisfies all applicable levels:

`scientific correctness`
→ `evidence support`
→ `scientific interpretation`
→ `separation of technical and scientific levels`
→ `logical structure`
→ `paragraph continuity`
→ `terminological consistency`
→ `academic-professorial Ukrainian style`
→ `formal correctness`

The final text must read as one coherent scientific work written by one author, not as a collection of independently generated or independently edited fragments.
