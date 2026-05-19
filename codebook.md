Yes — split them. The journal-policy coding and article-contribution coding are doing different jobs, and keeping them together will blur the method.

The *Philosophical Review* example also shows why the journal codebook needs an **absence/opacity** design. There may be almost nothing about architectonic work directly. But that is itself a finding if coded properly. The policy gives process detail, review structure, acceptance rates, and some rejection reasons, but it does **not** give a rich taxonomy of contribution-types. It explicitly names originality, relevant literature, general-reader interest, and sufficient philosophical content as initial-review concerns. That is usable evidence, even if the policy says nothing about synthesis, frameworks, architecture, field-mapping, or methodological reconstruction.

Below are two separated codebooks.

---

# Journal Policy Codebook

## 1. Purpose

The journal-policy codebook evaluates how journals publicly make philosophical contribution reviewable.

It does **not** assume that journals explicitly reject architectonic work. It asks whether public documentation gives visible criteria for recognizing different contribution-types, including synthetic, architectonic, methodological, framework-building, or field-mapping work.

A journal may be formally open while still providing little public guidance about how nonstandard contribution-types are evaluated.

## 2. Unit of Analysis

**Primary unit:** one journal.

**Evidence unit:** one excerpt from a journal policy page, author guideline, submission page, reviewer instruction, editorial policy, article-type description, or related documentation.

## 3. Journal Eligibility Fields

### `language_status`

* `english_primary`
* `multilingual_english_available`
* `non_english_primary`
* `unclear_language_status`

### `activity_status`

* `active`
* `inactive`
* `unclear_activity`

### `peer_review_status`

* `peer_reviewed`
* `not_peer_reviewed`
* `unclear_peer_review`

### `research_article_status`

* `publishes_research_articles`
* `no_ordinary_research_articles`
* `unclear_article_status`

### `inclusion_status`

* `included`
* `excluded_language`
* `excluded_inactive`
* `excluded_no_peer_review`
* `excluded_no_research_articles`
* `excluded_insufficient_information`
* `flagged_unclear`

---

## 4. Documentation Availability

### `documentation_availability`

How much public documentation exists?

* `extensive`: multiple relevant documents available.
* `moderate`: some useful documentation available.
* `minimal`: sparse documentation only.
* `absent`: no usable public documentation found.

### `documentation_orientation`

What is the documentation mostly about?

* `process_oriented`: mainly review process, anonymity, timelines, acceptance rates.
* `criteria_oriented`: gives substantive evaluation criteria.
* `scope_oriented`: mainly describes journal scope.
* `article_type_oriented`: mainly describes accepted article genres.
* `mixed`
* `unclear`

The *Philosophical Review* example would likely be `process_oriented` with some `criteria_oriented` content.

---

## 5. Review Process Transparency

### `review_process_transparency`

* `high`: review process is described in detail.
* `moderate`: process is described generally.
* `low`: minimal process information.
* `absent`: no review process information.

### `reviewer_criteria_visibility`

* `public_specific`: referee criteria are public and specific.
* `public_generic`: referee criteria are public but generic.
* `not_public`: referee criteria are not public.
* `unclear`

### `desk_review_transparency`

* `specific`: gives specific reasons manuscripts may fail initial review.
* `generic`: mentions editorial screening but gives little detail.
* `absent`: no desk-review information.
* `unclear`

The *Philosophical Review* example would likely be `specific` here because it gives reasons such as insufficient originality, insufficient grounding in relevant literature, excessive specialization, and too much history/exegesis without enough philosophical content.

---

## 6. Contribution Criteria

These codes track whether the journal publicly says what counts as a contribution.

Each is coded:

* `absent`
* `weak`
* `moderate`
* `strong`
* `unclear`

### `originality_language`

Does the journal emphasize originality, novelty, original contribution, or new research?

### `literature_grounding_language`

Does the journal require grounding in relevant literature?

### `debate_entry_language`

Does the journal frame contribution as entering, advancing, or intervening in a recognized debate?

### `general_interest_language`

Does the journal require interest beyond a narrow specialist readership?

### `specialist_legibility_language`

Does the journal emphasize relevance to specialists or experts?

### `philosophical_content_language`

Does the journal distinguish “philosophical content” from history, exegesis, exposition, or other forms?

### `anti_expository_language`

Does the journal discourage work that is primarily expository, historical, reconstructive, or survey-like?

### `argument_centrality_language`

Does the journal frame good work primarily in terms of argument, thesis, objection, reply, or defense?

---

## 7. Architectonic Recognition

These codes ask whether the journal explicitly recognizes work whose contribution lies in organization, synthesis, reconstruction, framework-building, or field mapping.

Each is coded:

* `absent`
* `weak`
* `moderate`
* `strong`
* `unclear`

### `synthesis_recognition`

Does the journal explicitly welcome synthesis or integration of literatures?

### `field_mapping_recognition`

Does the journal explicitly welcome field maps, state-of-field papers, research agendas, or review essays?

### `framework_recognition`

Does the journal explicitly welcome frameworks, models, schemas, methods, typologies, or systematic reconstructions?

### `methodological_recognition`

Does the journal explicitly welcome work on method, conceptual engineering, metaphilosophy, theory construction, or structure of inquiry?

### `interdisciplinary_recognition`

Does the journal explicitly welcome work crossing disciplinary or subfield boundaries?

### `architectonic_vocabulary`

Does the journal use language that explicitly recognizes domain-level organization, systematic architecture, structural synthesis, or field-level reconstruction?

Important rule:

> Absence of restriction is not evidence of recognition.

If a journal says “we publish work in all areas of philosophy,” but says nothing about synthesis, frameworks, field mapping, or architectonic work, code scope openness separately from architectonic recognition.

---

## 8. Scope Openness

### `scope_openness`

* `broad_explicit`: explicitly welcomes a wide range of areas, methods, traditions, or approaches.
* `broad_generic`: says “all areas of philosophy” or similar, but gives little detail.
* `moderate_scope`: has a recognizable range but not narrow.
* `specialist_scope`: focused on a subfield, tradition, topic, or method.
* `unclear_scope`

### `formal_openness_to_nonstandard_work`

* `explicitly_open`: explicitly welcomes synthesis, frameworks, methodological work, review essays, field maps, or interdisciplinary work.
* `implicitly_open`: language appears broad enough but does not name such work.
* `not_indicated`: no evidence.
* `formally_restrictive`: explicitly restricts or discourages relevant genres.
* `unclear`

---

## 9. Policy Opacity

Opacity should be a first-class result, not a leftover category.

### Opacity dimensions

Score each dimension:

* `0`: specific and public
* `1`: generic or partial
* `2`: absent, unavailable, or unclear

| Dimension                       | Question                                                                                   |
| ------------------------------- | ------------------------------------------------------------------------------------------ |
| `reviewer_criteria_opacity`     | Are referee criteria publicly available?                                                   |
| `contribution_criteria_opacity` | Are contribution standards specific?                                                       |
| `article_type_opacity`          | Are accepted article genres clearly described?                                             |
| `desk_review_opacity`           | Are initial rejection criteria visible?                                                    |
| `nonstandard_work_opacity`      | Is there guidance for synthetic, framework, review, methodological, or field-mapping work? |
| `scope_opacity`                 | Is the journal’s scope specific?                                                           |
| `decision_process_opacity`      | Is the decision process described?                                                         |

### Derived field: `policy_opacity_level`

* `low_opacity`
* `moderate_opacity`
* `high_opacity`

You can set thresholds after pilot coding.

---

## 10. Journal Reviewability Profile

Each journal receives one derived profile.

### `local_novelty_oriented`

Use when documentation emphasizes originality, literature grounding, debate-entry, argument centrality, or sufficient philosophical content, while architectonic recognition is weak or absent.

### `broad_but_generic`

Use when the journal is formally broad but offers little explicit contribution-type guidance.

### `architectonic_friendly`

Use when the journal explicitly recognizes synthesis, frameworks, field mapping, methodological work, review essays, or interdisciplinary architecture.

### `process_transparent_criteria_thin`

Use when the journal gives clear review-process information but little substantive contribution-type guidance.

This is probably useful for *The Philosophical Review*.

### `opaque`

Use when public documentation is too sparse to determine much about reviewability norms.

### `mixed`

Use when several profiles plausibly apply.

---

## 11. Evidence Requirements

Evidence excerpts are required for:

* any `strong` code;
* any `architectonic_friendly` profile;
* any `local_novelty_oriented` profile;
* any high-opacity score;
* any ambiguous or disputed classification.

Evidence rows should include:

```text
evidence_id
journal_id
document_id
code_supported
quoted_text
location_or_section
interpretive_note
confidence
```

---

# Article Contribution Codebook

## 1. Purpose

The article codebook classifies the contribution-function of published articles.

It does not ask whether an article is good. It asks what kind of epistemic work the article presents itself as doing.

The main goal is to determine how often published articles appear as local, relational, architectonic, operational, interpretive, applied, or survey-like contributions.

## 2. Unit of Analysis

**Primary unit:** one published article.

**Evidence unit:** article title, abstract, keywords, introduction, conclusion, section headings, or explicit contribution statement.

## 3. Article Eligibility

### `article_type`

* `ordinary_research_article`
* `review_essay`
* `book_review`
* `symposium_article`
* `critical_notice`
* `reply`
* `discussion_note`
* `editorial`
* `introduction`
* `other`

### `included_in_main_article_audit`

* `yes`
* `no`
* `flagged`

Default: include ordinary research articles. Catalogue everything else separately so you can test whether architectonic work is displaced into review essays, symposia, or special issues.

---

## 4. Primary Contribution Function

Assign exactly one primary contribution type.

### `local_argumentative`

Advances a local thesis, objection, defense, or reply within a bounded debate.

### `objection_reply`

Primarily responds to a specific existing argument, paper, objection, or named position.

### `interpretive_historical`

Centers historical, textual, or interpretive reconstruction.

### `relational`

Clarifies relations among concepts, debates, positions, or literatures without fully reorganizing a broader domain.

### `architectonic`

Primary contribution lies in organizing or reorganizing a domain, field, theory-space, problem-space, or cross-domain landscape.

### `architectonic_object`

Introduces or develops a concept, distinction, or category whose main value lies in reorganizing a broader field of relations.

This category is important because some contributions blur object and architecture.

### `operational_formalizing`

Produces a model, schema, method, procedure, criteria set, formalization, or diagnostic tool.

### `applied_problem_focused`

Addresses a concrete practical, institutional, technological, legal, ethical, medical, environmental, political, or social problem.

### `survey_state_of_field`

Maps a literature, debate, research program, or field state.

### `pedagogical_reconstructive`

Clarifies, reconstructs, or systematizes material primarily for uptake, teaching, or conceptual ordering.

### `other`

Use only when no category fits. Notes required.

---

## 5. Secondary Contribution Function

Assign one secondary contribution type if textually supported.

If none is clear, use:

```text
none
```

This avoids forcing hybrid papers into one false category.

---

## 6. Scope Level

### `local`

Narrow claim, objection, reply, or interpretive issue.

### `subfield`

Contribution remains inside a recognizable subfield or debate cluster.

### `domain`

Contribution organizes a broader domain within a subfield or topic area.

### `cross_domain`

Contribution connects or reorganizes multiple domains, subfields, methods, or literatures.

### `field_wide`

Contribution addresses philosophy broadly, philosophical method, or a very large field segment.

### `unclear`

Insufficient basis.

---

## 7. Architectonic Strength

This scale distinguishes ordinary structure from strong architectonic contribution.

### `0_minimal_argument_structure`

The article has ordinary argumentative or expository structure only. Architecture is not the contribution.

### `1_local_structural`

The article organizes a local debate or limited conceptual relation, but does not offer domain-level architecture.

### `2_domain_architectonic`

The article explicitly organizes or reorganizes a domain, problem-space, or substantial literature.

### `3_cross_domain_architectonic`

The article explicitly organizes or reorganizes multiple domains, literatures, methods, or field-spaces.

For the target study, `2` and `3` count as strong architectonic contribution.

---

## 8. Architecture-Dependence

### `low`

The contribution stands without broader organizational framing.

### `medium`

The broader organization materially supports the contribution, but the contribution can still be described locally.

### `high`

The contribution depends on explicit reorganization, mapping, taxonomy, framework, or domain-level structure.

---

## 9. Carrier Form

How is the contribution carried?

### `prose_argument`

Standard prose argument.

### `conceptual_distinction`

A distinction or set of distinctions.

### `taxonomy`

Classification or typology.

### `schema_model`

Schema, model, diagram, structure, or framework.

### `formal_model`

Mathematical, logical, or formal apparatus.

### `case_matrix`

Case comparison or diagnostic matrix.

### `literature_map`

Mapping a literature or debate.

### `method_procedure`

Steps, procedures, method, or criteria.

### `mixed`

Multiple carrier forms central.

---

## 10. Operational Direction

Does the article point toward use?

### `none`

No clear operational direction.

### `conceptual_clarification`

Improves understanding but does not clearly support diagnosis or design.

### `diagnostic`

Provides categories useful for identifying failures, patterns, misapplications, or problem-structures.

### `normative_evaluative`

Provides standards for judgment, critique, or evaluation.

### `design_oriented`

Provides criteria, concepts, or procedures that could inform institutional, practical, technological, or policy design.

### `methodological`

Provides a method for inquiry or future philosophical work.

---

## 11. Confidence

### `high`

Clear textual evidence; classification unlikely to be disputed.

### `medium`

Plausible classification; at least one alternative also plausible.

### `low`

Ambiguous, mixed, or insufficient evidence.

---

## 12. Evidence Requirements

Evidence is required for:

* all `architectonic` classifications;
* all `architectonic_object` classifications;
* all `operational_formalizing` classifications;
* all low-confidence classifications;
* any article counted as strong architectonic contribution.

Evidence rows should include:

```text
evidence_id
article_id
code_supported
evidence_type
quoted_or_paraphrased_text
location
interpretive_note
confidence
```

---

## 13. Derived Variables

### `strong_architectonic_article`

Count as strong architectonic if:

* architectonic strength is `2` or `3`;
* architecture-dependence is `medium` or `high`;
* confidence is `medium` or `high`.

### `strict_architectonic_article`

Count as strict architectonic if:

* architectonic strength is `2` or `3`;
* architecture-dependence is `high`;
* confidence is `high`.

### `architectonic_or_operational_article`

Count if:

* primary or secondary code is `architectonic`, `architectonic_object`, or `operational_formalizing`;
* and confidence is `medium` or `high`.

---

## 14. Important Distinctions

### Minimal architectonicity vs architectonic contribution

All theoretical writing is architectonic in a minimal sense. This study reserves architectonic contribution for cases where architecture is doing the main epistemic work.

### Object contribution vs architectonic object

Some papers introduce a concept or distinction that functions as an organizing node for a broader domain. These are coded as `architectonic_object`, not merely local object contributions.

### Survey vs architectonic work

A survey maps existing work. Architectonic work reorganizes a problem-space in a way that produces new tractability, diagnosis, transfer, or inquiry pathways. Some papers may be both.

### Operational work vs mathematical formalization

`operational_formalizing` does not require mathematics. It includes schemas, procedures, criteria, models, diagnostic matrices, and non-mathematical structural renderings.

---

## 15. Sensitivity Analysis

Report three versions.

### Strict count

Only:

* architectonic strength `2` or `3`;
* architecture-dependence `high`;
* confidence `high`.

### Moderate count

* architectonic strength `2` or `3`;
* architecture-dependence `medium` or `high`;
* confidence `medium` or `high`.

### Broad structural count

* architectonic strength `1`, `2`, or `3`;
* architecture-dependence `medium` or `high`;
* confidence `medium` or `high`.

This allows the results to be tested under narrow and broad definitions.

