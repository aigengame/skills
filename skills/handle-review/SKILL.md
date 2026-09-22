---
name: handle-review
description: Analyze, evaluate, and handle pull request review feedback before changing code. Verify each comment against the current PR head, requirements, product support scope, project constraints, and runtime evidence; distinguish technical truth from requirement standing; then decide with evidence whether to fully adopt, partially adopt, not adopt, or request an owner decision. Prevent review findings and suggested mechanisms from turning unsupported cases into product promises, scope inflation, symptom-patch loops, non-functional requirement (NFR)-driven platformization, disproportionate complexity, rigid processes, or regressions. Use when addressing PR review comments, evaluating findings, implementing accepted feedback, or drafting a reviewer reply.
---

# Handle Review

## Objective

Treat review feedback as engineering input to verify, not commands to execute.

A review can reveal a real problem while relying on an inaccurate premise, overstating its severity,
or suggesting the wrong solution. Judge separately:

- Whether the reported problem exists.
- Whether the affected input or behavior has requirement standing.
- Whether it is worth addressing now.
- Whether the suggested change is an appropriate and sufficiently small solution.

**Requirement standing** is current authority that the product owes a behavior, such as a recorded
user outcome, approved acceptance criterion, accepted compatibility obligation, current public
promise, or hard safety, integrity, or interoperability constraint. A probe, current behavior,
review finding, or regression test can prove a fact without establishing that the current goal must
support it. A published contract or demonstrated external dependency can still create a real
compatibility obligation, so missing original authority does not authorize automatic rejection or
removal.

Protect correctness, existing working results, fast feedback, reversible changes, and long-term
comprehensibility. Do not introduce disproportionate software entropy merely to close a review,
eliminate a minor inconsistency, or satisfy an abstract idea of completeness.

## Core Principles

- Analyze and evaluate before making changes.
- Verify the problem and the suggested solution separately.
- Do not infer that a suggested solution is correct merely because it identifies a real local
  problem; a reviewer does not gain default authority to redesign the whole approach.
- Do not treat severity labels, forceful wording, or reviewer identity as evidence.
- Judge technical truth and requirement standing independently. A true finding without established
  standing is an observation for a support decision, not an automatic fix or regression obligation.
- Use consistency to reduce comprehension cost, not to justify new abstractions or global
  mechanisms.
- Preserve existing test, performance, compatibility, and architecture results unless evidence
  shows they should change, but do not treat current code or tests as standalone authority over
  product support scope.
- Keep complexity required to fix the current problem. Require credible risk to justify additional
  layers, state, rules, processes, or defensive mechanisms.
- Do not manufacture work so that every comment produces a change.

## Workflow

### 1. Establish the Review Baseline

Before handling feedback, confirm:

- The PR's exact current head, current base tip, merge base, and merge-base-to-head diff.
- The current issue, the originating requirement for the slice, the record that introduced the
  disputed behavior, acceptance criteria, design decisions, and project rules.
- Supported inputs and behaviors, explicit exclusions, current public promises, and demonstrated
  compatibility dependencies.
- Current observable behavior and tests that already pass.
- The baseline, target, and measurements for performance changes.
- Work explicitly outside the current PR.

Do not change code from an old head, stale documentation, or assumptions detached from the current
diff.

A second review round on the same slice, or any review response that materially expands input forms
or public contract surface, is an authority-refresh trigger. Re-read the originating requirement and
the record that introduced the disputed behavior before another patch. This is not a fixed diagnosis
threshold.

### 2. Separate Each Comment into Claims

For every review comment, identify:

1. **Problem claim**: What does the reviewer say is wrong?
2. **Evidence**: Which code, test, specification, measurement, or project rule supports the claim?
3. **Impact**: What observable consequence occurs if it remains unchanged?
4. **Requirement standing**: Which current user outcome, acceptance criterion, compatibility
   obligation, public promise, or hard constraint requires the affected input or behavior, and who
   owns an unresolved support decision?
5. **Suggested solution, if any**: What change does the reviewer propose?
6. **Uncertainty**: Which parts remain assumptions or require verification?

A comment can identify a real problem while proposing an excessive or incorrect solution.

### 3. Verify Whether the Problem Exists

Choose the minimum sufficient evidence for the type of claim:

- **Correctness or contract**: Reproduce the behavior and compare it with requirements, public
  interfaces, or the authoritative specification.
- **Testing**: Check the exercised path, assertion strength, isolation, and failure behavior.
- **Performance**: Compare repeatable before-and-after measurements and the critical path; do not
  infer performance from structure alone.
- **Architecture**: Confirm the current change boundary, dependency direction, and maintenance cost.
- **Standards**: Check the currently authoritative rule; do not treat history as a current
  requirement automatically.
- **Naming or style**: Confirm that the difference creates real comprehension or maintenance cost,
  rather than merely using near-synonyms.

Treat a failure to reproduce as unverified, not disproved. Seek alternative evidence or run a
risk-proportionate, bounded investigation before deciding. Do not convert a claim into a change
when it lacks current evidence or depends on future assumptions.

For each finding, decide technical truth and requirement standing separately. A counterexample can
disprove the proposed mechanism without establishing that the product must support a broader input,
platform, mode, or lifecycle. Before generalizing, identify the approved outcome that requires the
broader behavior.

When published text and behavior conflict, trace the authority and history of both. Do not assume
that the text is stale or that current behavior is intended. A documentation-only repair can ratify
an accidental behavior and expand the contract instead of correcting the implementation.

### 4. Evaluate the Entropy Cost of the Suggested Change

Ask:

- Does the change directly solve the verified problem?
- Which current behavior or hard constraint would fail without it?
- Is there a smaller, more direct, or more reversible fix? Would a merely local fix duplicate stable
  mechanics or preserve the condition that caused earlier patches?
- Does it introduce new concepts, layers, state, synchronization rules, exceptions, or ongoing
  maintenance duties?
- Does it establish a permanent mechanism for a one-time minor inconsistency?
- Does it expand into adjacent problems outside the PR?
- Does it add support for new inputs, platforms, modes, lifecycle states, or error semantics, then
  require tests, schemas, help, or documentation to preserve that expanded contract?
- Does an NFR such as identity, portability, auditability, safety, or observability create general
  variant, registration, compatibility, synchronization, operation, or maintenance obligations
  without a concrete acceptance scenario?
- Does proposed reuse share stable mechanics, or import a neighboring feature's public policy and
  unrelated semantics?
- Does it weaken existing test, performance, or maintainability results?
- Does the new mechanism require further mechanisms to explain, verify, or maintain it?

When the suggested solution costs substantially more than the problem, preserve the valid problem
claim but choose the minimum sufficient solution or do not adopt the suggestion. Compare total
system complexity, not only the current diff. A focused abstraction can be necessary when present
consumers demonstrate one stable mechanism; whole-contract reuse or a general platform is not
justified by similar-looking policy alone.

### 5. Decide How to Handle Each Claim

Choose one primary decision for every independent claim or recommendation. Group them at the
comment level only when their evidence and decision match. When using **Partially Adopt** for a
mixed comment, identify the adopted and unadopted parts explicitly.

#### Fully Adopt

Fully adopt when all of the following are true:

- Current evidence confirms the problem.
- The affected input or behavior has requirement standing, or the designated product or support
  decision owner has authorized that support in this PR.
- The problem should be addressed in this PR.
- When the reviewer suggests a solution, it is direct, sufficient, and free of material excess
  complexity.
- The change does not break a higher-priority constraint or an existing result.

State the supporting evidence, the change location, and the validation method.

#### Partially Adopt

Partially adopt when the problem is valid but the proposed scope is too broad, the implementation is
too heavy, or the suggestion contains a false premise.

Preserve the valid goal and use a smaller alternative. For example:

- Make a local correction instead of establishing a global mechanism.
- Correct the supported case without generalizing the fix to review-discovered inputs that lack
  requirement standing.
- Share the lowest stable mechanism when concrete consumers need it, while keeping their distinct
  public policies separate.
- Isolate the actual source of contamination instead of disabling a shared optimized path.
- After resolving authority, correct the documentation or implementation without ratifying an
  accidental behavior or restoring an obsolete standing process.
- Preserve a measured design while fixing its demonstrated defect.

State what is adopted, what is not adopted, and why.

#### Decision Required

Use **Decision Required** when the technical finding is confirmed or plausible but requirement
standing, compatibility treatment, acceptable cost, or the next action under unresolved evidence
still needs an authorized decision. Route support scope and compatibility promises to the designated
product or support decision owner. Route the implementation, current PR action, and acceptable
engineering cost to the maintainer. One person can hold both roles. If no owner is designated,
follow the project's governance or ask the user. State the known facts, the authority gap, the effects
of support and non-support, simpler options, a recommendation, the decision owner, and the dependent
work to pause. Options can include deliberate support, compatibility-preserving deprecation, refusal
through an existing channel, or no change. Do not implement the broadest case by default.

**Decision Required** takes precedence over **Do Not Adopt** while a current public promise,
demonstrated external dependency, or hard constraint leaves compatibility treatment or follow-up
work unresolved.

#### Do Not Adopt

Do not adopt when:

- Current evidence disproves the claim, or a bounded investigation finds no supporting evidence
  and the residual risk does not justify a change.
- The designated product or support decision owner has explicitly excluded the affected input or
  behavior, compatibility treatment is resolved, neither a current public promise nor a demonstrated
  external dependency nor a hard constraint requires further work, and the retained behavior does
  not silently corrupt data or report false success.
- The suggestion solves a problem outside the current scope.
- A minor difference creates no material comprehension or maintenance cost.
- The change would introduce substantially greater software entropy.
- The change would regress performance, coverage, compatibility, or architecture.

Do not adopt silently. Provide the evidence, explain what remains unchanged, and disclose any known
residual risk.

After making the decisions, confirm the authorized next action. Stop after evaluation when the
request is read-only. Run steps 6–8 only when changes are authorized. Run step 9 only when the user
requests a reply draft or authorizes an external response; post replies or resolve threads only with
explicit authorization.

### 6. Order the Accepted Changes

Resolve requirement standing before treating a technically true inconsistency as a public-contract
problem. Safety, security, and data-integrity constraints still apply even when ordinary product
support is absent.

Handle accepted feedback in this order:

1. Correctness, security, data integrity, and public-contract problems.
2. Problems that fail acceptance or weaken test evidence.
3. Design problems with current maintenance cost.
4. Naming, documentation, and consistency problems that have a local fix.

Separate independent scope from the current PR. Do not use review fixes as an opportunity to
refactor the entire module.

### 7. Implement the Minimum Sufficient Change

- Change only the parts covered by an explicit decision.
- Reuse the lowest stable mechanisms and test paths; do not import a neighboring feature's complete
  public policy merely because its implementation looks similar.
- Add or adjust tests for approved behavior changes. Do not turn a review-discovered case into a
  regression obligation before its support scope is decided.
- When documentation and implementation disagree, resolve their authority first. Do not rewrite
  documentation merely to describe accidental behavior.
- Do not introduce permanent artifacts merely to prove that the review was handled.
- Do not turn non-blocking advice into a new mandatory process.

### 8. Check for Regressions Caused by the Review Fix

After making changes, compare again:

- Is the original problem solved?
- Do the tests and contracts still hold?
- Are performance results preserved or improved?
- Did the diff expand unexpectedly?
- Did the change add unnecessary concepts, state, rules, or maintenance paths?
- Did fixing the review suggestion create a chain of fixes for the new mechanism?
- Did the fix add support for a new input, platform, mode, lifecycle, or public contract without
  requirement standing?
- Did a regression test or published description turn an observation into an implicit promise?
- Are successive review fixes adding mechanisms, exceptions, or caveats without clearer progress
  toward the original acceptance criteria?

For performance-related changes, compare before-and-after measurements. Revert a review-driven
change that worsens the target result unless it protects a higher-priority hard constraint.

Use independent re-review when risk or change size justifies it. Do not make independent re-review a
mandatory ritual for every small correction.

Handle one comment's evidence and adoption decision here. Use `entropy-review` when a suggested
architecture or module needs a deeper proportionality assessment. When repeated review fixes expand
the contract or move failures across boundaries without acceptance progress, pause the patch path
and use `backtrace-review` to reconstruct the causal history. Do not reproduce either full workflow
inside this skill.

### 9. Reply to the Review

Explain the decisions and evidence instead of merely saying that the comments were addressed.

Report each independently evaluated claim in this form:

| Claim | Decision | Evidence and requirement standing | Change or retained behavior | Validation |
| --- | --- | --- | --- | --- |
| Brief problem statement | Fully Adopt / Partially Adopt / Do Not Adopt / Decision Required | Current evidence and authority or gap | Commit, file, unchanged behavior, or paused work | Tests, CI, measurements, or residual risk |

Also report:

- The current exact-head commit.
- Relevant tests and CI status.
- Anything not yet verified.
- Open support, cost, or next-action decisions and their designated owners.

Do not claim that an inline thread was resolved when no such thread exists. A comment with no
valuable change can be closed with evidence; it does not need a commit.

## Output Contract

Provide:

1. **Review baseline**: Exact head, current base tip, merge base, merge-base-to-head diff,
   originating requirements, supported and unsupported scope, constraints, and verified facts.
2. **Decision for each claim**: Fully Adopt, Partially Adopt, Do Not Adopt, or Decision Required,
   with technical evidence, requirement standing and authority or gap, and the decision owner when
   applicable.
3. **Change plan**: Only the minimum sufficient changes for adopted feedback. Identify dependent
   work paused by a Decision Required result.
4. **Validation**: Tests, CI, performance comparisons, and unverified items.
5. **Reviewer reply draft, when requested**: A concise response ready to send.

Report only findings that can change a decision or implementation approach. If no feedback warrants
a change, still provide the review baseline and a decision for every claim. For each **Do Not
Adopt** decision, state the evidence, retained behavior, and residual risk. Report that the change
plan is empty, record the validation and unverified items, and then stop. Do not manufacture
modifications.

## Boundaries

- Do not use entropy control to dismiss demonstrated correctness, security, data-integrity, or
  public-contract problems.
- Do not treat the reviewer's suggested implementation as the only solution.
- Do not introduce global abstractions, caches, manifests, protocols, gates, or standing processes
  for local consistency.
- Do not force another local patch when evidence demonstrates a stable shared mechanism or
  responsibility boundary; introduce only the minimum sufficient abstraction that owns it.
- Do not use missing original authority alone to reject behavior that a current public contract or
  demonstrated external dependency requires.
- Do not preserve a design disproved by evidence merely because work has already been invested in
  it.
- Do not replace verification with argument; declining feedback also requires evidence.
- Do not expand into a comprehensive review or architectural rewrite unrelated to the current
  feedback.
- Leave support scope and compatibility promises to the designated product or support decision
  owner. Leave implementation, PR action, and engineering cost to the maintainer. One person can
  hold both roles; review supplies input and feedback.
