---
name: artifact-review
description: Review project documents such as issues, ADRs, architecture documents, specifications, plans, and documentation changes for correctness, requirement provenance and authority, explicit scope boundaries, usability, consistency, completeness, orthogonality, DRY, terminology accuracy, and clear prose. Distinguish technical facts from product commitments and identify requirement drift or unsupported scope before implementation. Use only when the user explicitly asks for a review of such a document or a re-review of claimed fixes to one.
---

# Artifact Review

## Goal

Decide whether a project document fulfills its purpose with accurate, coherent,
sufficiently complete, and non-duplicative content, so its intended readers can
understand it, make decisions, or act on it reliably.

Review both content and language:

- Is the content correct, usable, and clearly bounded?
- Do requirements, decisions, constraints, and product commitments have current
  standing, non-circular provenance, and scope bounded by the recorded user outcome?
- Are terms accurate, stable, and consistent with project or domain usage?
- Is the prose concrete and natural, and does it express conceptual relationships
  accurately?

Report evidence-backed, actionable problems that affect factual accuracy,
understanding, decisions, implementation, maintenance, terminology, or clarity.
Terminology misuse, changes in a concept's meaning, and prose that materially
impedes understanding are findings in their own right. Do not report personal
stylistic preferences.

Scale the review to the artifact's size, risk, and purpose.

Treat terminology and prose as a required review pass. Do not conclude **Pass**
until this pass is complete and its result is reported.

## Workflow

### 1. Inspect Relevant Materials

- Read the complete artifact. For a change, inspect both the full current artifact
  and the relevant change.
- Include status, labels, version, or other attached information when it changes the
  artifact's meaning.
- Trace key facts, constraints, and references to the nearest authoritative source.
  Read only material relevant to the artifact's purpose or the change under review.
- For an implementation-oriented artifact, pin the originating requirement,
  recorded user outcome, or explicit owner decision that defines the need
  independently of the disputed observation, together with later owner decisions
  that changed its scope. Establish the user problem, current acceptance criteria,
  hard constraints, explicit exclusions, and the decision owner for unresolved
  scope. Compare added or changed obligations with that baseline.
- Do not treat a downstream artifact as proof of independent product need merely
  because it is current, tested, published, or marked accepted. Verify that the
  designated owner explicitly authorized any added product scope.
- Distinguish observations, proposals, accepted decisions, and current requirements.
  Do not infer authority from an artifact type, a test, or polished prose alone.
- Inspect code, configuration, scripts, project state, or external-system behavior
  when a claim depends on them.
- Base conclusions on the artifact, the user's request, and observable evidence. Do
  not infer unwritten author intent.

Relevant material may include:

- For an issue: its goal, constraints, acceptance criteria, related work, and the
  current implementation state.
- For an ADR: its context, decision, rationale, consequences, alternatives, and later
  amendments.
- For an architecture document: the boundaries, responsibilities, dependency
  directions, interfaces, and current system structure it describes.
- For a specification or plan: its requirements, constraints, deliverables, and
  validation approach.

These are examples of relevant evidence, not mandatory templates for every
artifact.

### 2. Review the Artifact

#### Correctness and Usability

- Facts, technical descriptions, domain claims, and terminology agree with
  verifiable sources.
- Decisions, requirements, constraints, and guidance support the judgment or action
  the artifact is meant to enable.
- When the artifact contains procedures, their order, inputs, outputs, and required
  capabilities are workable.
- When the artifact defines behavior or an implementation process, it covers
  important assumptions, boundaries, and failure paths.
- Detail and constraint match risk and purpose: constrain fragile operations while
  preserving judgment when several approaches are valid.
- Validate critical, non-obvious claims with a representative check. Disclose what
  was not tested when validation is impractical.

#### Requirement Authority and Scope

- Judge technical truth and requirement standing separately. **Requirement
  standing** is current authority that the product owes a behavior, such as a
  recorded user outcome, approved acceptance criterion, accepted compatibility
  obligation, current public promise, or hard safety, integrity, or interoperability
  constraint.
- **Non-circular provenance** traces that obligation to an actual product need or hard
  constraint without relying on the artifact under review or downstream claims
  derived from the same observation. Requirement standing alone does not prove that
  need or authorize retaining or expanding scope. For scope approval, require a
  recorded user outcome, an explicit decision by the designated owner to address a
  demonstrated need or loss for an actual consumer, or a hard safety, integrity, or
  interoperability constraint.
- A probe, current behavior, implementation limit, review finding, or regression test
  can prove a fact. It does not by itself establish that the product must support the
  observed input or behavior.
- For each new or changed requirement, acceptance criterion, compatibility rule,
  public promise, or non-functional requirement (NFR), trace a non-circular provenance
  chain to the actual product need or hard constraint that requires it. Do not use
  the artifact under review, or a downstream issue, ADR, test, schema, or description
  derived from the same observation, as its own authority. A discovered technical
  fact can trigger a product decision, but it must not become a requirement,
  acceptance criterion, regression obligation, or public promise without an explicit
  decision by the designated owner. Until that decision exists, report the fact as
  an observation and identify the authority gap.
- Establish the actual product need independently of the proposed mechanism before
  evaluating mechanism-led criteria. Do not infer a product requirement from the
  existence, technical correctness, reuse value, or consistency of a helper,
  registry, field, abstraction, single authority, or other mechanism. Report any
  mechanism, supported input, or contract surface that exceeds the recorded product
  outcome and hard constraints as scope inflation.
- Treat an NFR as a platformization candidate whenever it promotes a bounded quality
  concern into reusable infrastructure and creates continuing variant, extension,
  lifecycle, compatibility, registration, synchronization, operation, or maintenance
  obligations. This classification does not depend on requirement standing. Always
  route the candidate to `entropy-review` for the deeper proportionality assessment.
- Independently require an authorized and bounded acceptance scenario, together with
  a demonstrated consumer, loss, or hard constraint, for the NFR and its proposed
  scope. A product-requirement label or quality word is not sufficient authority. If
  this authority is missing, report the gap and do not approve the dependent platform
  obligations. If standing is established, record it without treating it as proof
  that the platform obligations are proportionate.
- When published text and behavior conflict, trace the authority and history of both.
  Do not assume that the text is stale or make an accidental behavior authoritative
  only by documenting, testing, or making it consistent.
- Do not approve an unsupported obligation as current scope. If it might become a new
  product decision, name the decision owner and keep dependent implementation paused
  until the owner decides its support scope.

#### Consistency and Completeness

- Use one term for each concept and one meaning for each term.
- Claims, definitions, requirements, constraints, and conclusions agree internally
  and with the material on which they depend.
- Descriptions of current state, existing behavior, or proposed change match the
  relevant sources.
- Cover the first practical questions raised by the artifact's purpose. Do not omit
  information readers need to understand or use it.
- For an implementation-oriented artifact, readers can determine what must be done,
  what constrains the work, and how completion will be established.
- For a decision record, readers can determine what was decided, why, where it
  applies, and its important consequences.
- Do not add speculative cases or detail merely to appear complete.

#### Orthogonality and DRY

- Give each rule, fact, or decision one authoritative home. Elsewhere, keep only the
  reminder or reference needed for understanding or use.
- Organize the artifact around a coherent purpose. Split unrelated concerns only
  when they obstruct understanding, ownership, or independent change.
- Remove recaps, filler, and repeated constraints that add no decision, action, or
  necessary context.
- Include enough context to understand the core conclusion without copying an
  authoritative source in full.
- Extract shared material only when it has the same meaning and the same reason to
  change at every use site.
- Do not fragment content that must be read together merely to remove surface-level
  repetition.

#### Terminology and Prose — Required Pass

- Review terminology and prose independently of content findings. Do not limit this
  pass to passages already selected for correctness findings.
- Search the complete artifact for established terms, alternate names, undefined
  terms, and changes in meaning. For short artifacts, inspect all prose. For long
  artifacts, inspect every changed passage and every passage that states a
  requirement, decision, or procedure; sample each remaining major section.

- Prefer established project and domain terms. Do not introduce a second name for
  an existing concept.
- Introduce a new term only when existing language cannot express the concept
  accurately, and define it at first use.
- When a local convention broadens an established term, state the convention and its
  practical effects.
- Use ASD-STE100 Simplified Technical English as the default reference for technical
  prose unless the project specifies another writing standard. Preserve established
  project and domain terms as technical nouns or technical verbs.
- Unless the project specifies another writing standard, check word choice and
  meaning, technical nouns and verbs, and sentence structure against ASD-STE100.
  Apply its procedural or descriptive writing rules according to the artifact.
  Record the checks performed.
- Prefer plain, concrete prose. Remove formulaic wording, abstract noun chains,
  slogans, empty bullets, and legal or procurement language.
- Check that sentences express causal, dependency, scope, and ordering relationships
  accurately.
- Keep examples that explain a non-obvious distinction; remove examples that merely
  restate a rule.
- Describe observable text, state, and behavior. Do not speculate about who or what
  produced the prose.

### 3. Validate When Applicable

Choose the smallest sufficient validation for the artifact's actual claims:

- Open cited material and confirm that it supports the claim.
- Compare normative claims with the originating requirement, accepted decisions, and
  current support scope. Confirm whether each cited source proves a technical fact,
  independently authorizes a product obligation, or does both. Do not accept a source
  that only repeats the downstream claim as independent authority for that claim.
- Compare claims with current implementation, configuration, project documentation,
  or issue-tracker state.
- Search for conflicting or drifting terminology, responsibilities, relationships,
  or prior decisions.
- Run document checks, link checks, scripts, or tests directly relevant to a claim.
- For a versioned change, identify the reviewed revision, relevant baseline, and
  actual scope of the change.
- When an artifact bounds work by a count of texts, schema fields, help entries, or
  similar surfaces, inventory the underlying fact by meaning across the relevant
  contract surfaces. Do not accept a literal-text search as proof of complete scope.
- When the artifact cites CI, validation results, or runtime evidence, verify that the
  evidence supports the stated conclusion.
- Record the terminology sources, writing reference, inspected scope, and prose
  checks used in the review. For technical prose, the reference must be ASD-STE100 or
  the project-specified alternative.

A passing format check or green CI proves only that its checks passed; it does not by
itself establish that the content, terminology, or prose is correct.

Disclose important validation that was not performed and could affect the conclusion.

### 4. Report

Start with one conclusion:

- **Pass**: no substantive content, terminology, or prose issue prevents the artifact
  from fulfilling its purpose, and the required terminology and prose pass is
  complete and reported.
- **Changes required**: substantive issues must be resolved, but the artifact's
  purpose can still serve the authorized goal after bounded corrections.
- **Decline**: the artifact's central premise or essential acceptance scope lacks
  non-circular support from a recorded user outcome, explicit owner decision, or
  hard constraint, or contradicts one of them. Correcting it would replace the
  proposed work. Do not use this artifact to approve or guide implementation.
  Recommend a redraft or replacement grounded in confirmed authority and bounded
  scope.

Use **Decline** only when the proposed purpose cannot survive a bounded correction.
Finding count and severity do not decide the verdict. An open support decision does
not let the reviewer cancel an accepted compatibility obligation or public promise.
Identify its decision owner and pause dependent work.

Always include a **Terminology and prose assessment**, even when it produces no
finding. State:

- The project or domain terminology sources used.
- The writing reference used. For technical prose, name ASD-STE100 or the
  project-specified alternative.
- The scope inspected and prose checks performed.
- The result and the location of any related findings.
- Important checks that were not performed.

If no substantive terminology or prose issue was found, say so explicitly. The
assessment documents review coverage; it does not require a finding.

Group actionable findings under **Required changes** or **Minor** as appropriate.
For **Decline**, put the findings that invalidate the artifact's premise under
**Reasons for decline**. Classify by impact, not by issue type. A terminology or
prose problem that affects accuracy, understanding, decisions, or use is substantive
and must not be downgraded to wording feedback.

For each finding, give:

- The location.
- Verifiable evidence.
- For a requirement or scope finding, the current requirement standing, including any
  accepted compatibility obligation or current public promise; the actual product need
  or hard constraint; the non-circular provenance chain or its first unsupported link;
  and the exact behavior, input, contract surface, or continuing obligation added
  beyond, removed from, or changed relative to that need.
- The impact on accuracy, understanding, or use.
- The smallest practical alternative that serves the authorized goal.

For **Decline**, cite the recorded user outcome, accepted owner decision, or hard
constraint that bounds the work. Identify the first unsupported premise or
contradiction and explain why bounded edits cannot restore the artifact's purpose.
State the known authorized outcome and scope boundary for a replacement, any useful
evidence to retain, and any open support decision and its owner. This verdict rejects
the current artifact, not the observed facts or an existing product obligation; it
does not itself close or replace the artifact.

Report only actionable issues. Keep optional improvements separate from required
changes and include them only when they materially help.

If new context invalidates a proposed fix but not the underlying problem, revise the
fix rather than dropping the finding.

If an implementation-oriented artifact presents an unresolved product decision as
approved scope, report **Changes required** when bounded corrections can preserve
its purpose, or **Decline** when that assumption defines its purpose or acceptance
scope. Identify the decision owner and dependent work that must pause. An artifact
whose purpose is to frame that decision can pass when it labels the proposal,
authority gap, owner, and open decision accurately.

If there are no substantive findings, report **Pass**, identify the reviewed target,
include the required **Terminology and prose assessment**, and summarize the main
content checks in one or two sentences. Mention important validation that was not
performed, then stop.

Return the review in the medium the user requested. Edit files, post comments, or
perform other remote writes only when the user explicitly authorizes them.

## Re-review

- Pin the previous and current versions.
- Verify every claimed fix in the artifact and relevant evidence; a reply is not
  evidence by itself.
- Repeat the terminology and prose pass for changed text and report its assessment,
  even when prior findings concerned only content.
- Review scope added or changed since the previous review.
- Verify that a fix did not turn an observation into a requirement, add an unsupported
  obligation, or restore rejected scope under a new name.
- For an option excluded by an accepted decision, verify that the constraint,
  rationale, and necessary mitigations appear in the appropriate authoritative
  material.
- Use the same conclusion and finding format as the initial review.

## Relationship to Other Review Skills

- Use this skill to review an artifact's correctness, requirement authority, and
  explicit scope boundaries, especially before implementation. Identify
  disproportionate mechanisms or repeated repair as routing signals; do not reproduce
  the deeper workflows below.
- Use `entropy-review` to determine whether a design, plan, or implementation adds
  mechanisms and continuing obligations proportionate to the approved goal.
- Use `handle-review` to decide whether and how to adopt pull request feedback without
  turning a review finding into an unsupported product commitment.
- Use `backtrace-review` when repeated fixes or review rounds expand the contract or
  move failures across boundaries without progress toward acceptance.
- After an accepted requirement, decision, scope, or term changes, use `reconcile` to
  find and repair stale dependent artifacts.
