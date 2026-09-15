---
name: entropy-review
description: Review software designs, implementation plans, and implemented changes from an agile perspective to determine whether their software entropy is proportionate to current goals. Identify scope creep, overengineering, excessive defensive design, over-abstraction and platformization driven by non-functional requirements (NFRs), premature generalization, and hard-to-maintain mechanisms whose costs outweigh their value; provide smaller, more reversible alternatives with faster feedback. Use when the user asks for an entropy review, design simplification, complexity control, an overengineering review, or whether a mechanism is worth introducing, retaining, or expanding.
---

# Entropy Review

## Objective

Review whether a software design, implementation plan, or implemented change introduces software
entropy proportionate to the problem it solves.

Do not optimize for the fewest lines of code, and do not reject architecture, testing, or
defensive design. Distinguish between:

- Essential complexity inherent in the problem and its hard constraints.
- Accidental complexity introduced by implementation, technology, or representation choices rather
  than by the problem itself. Pay particular attention to speculation, a drive for completeness,
  premature planning, and mechanism-first thinking.

Protect working software, fast feedback, reversible evolution, and long-term comprehensibility.

Treat software entropy as the tendency of accumulated concepts, structures, state, and rules to
make a system increasingly difficult to understand, verify, and change.

Seek the minimum sufficient complexity for the current goal. Preserve necessary structure without
letting completeness or robustness become reasons for unrelated mechanisms.

Evaluate total system complexity, not only the local complexity added by the current change.
Successive symptom patches can each be small while their concepts, exceptions, state, coupling, and
verification obligations accumulate. Abstraction is not entropy by itself. A minimum sufficient
abstraction that owns a demonstrated stable responsibility, semantic, module, or variation boundary
can add local structure while reducing and stabilizing total system complexity. Necessary abstraction
is not over-abstraction; it becomes excessive only when its scope or continuing obligations exceed
the demonstrated need.

## Workflow

### 1. Pin the Current Goal

Establish:

- What specific problem must be solved now?
- What facts prove that the problem exists?
- What observable outcome proves that the problem is solved?
- Which hard constraints must not be violated?
- Which adjacent problems are explicitly out of scope?

Mark judgments without evidence as assumptions. Do not use assumptions as reasons to expand the
solution.

### 2. Describe the Minimum Sufficient Solution

Describe the smallest end-to-end solution that satisfies the current goal:

- Cover only currently specified behavior.
- Reuse existing concepts, structures, and paths where possible.
- Produce observable and verifiable results early.
- Preserve hard constraints.
- Do not require one change to solve future stages.

Use this solution as a comparison baseline, not as a predetermined final answer.

### 3. Inventory New Obligations

Identify every concept, layer, state, rule, exception, process, and maintenance duty introduced by
the design, plan, or change.

Include obligations accumulated across earlier local fixes when they remain part of the current
design, even if the current change adds little local complexity. Inventory the resulting system, not
only the current diff.

Ask for each one:

1. Which current goal, requirement, hard constraint, actual consumer, or demonstrated loss requires
   it?
2. What current evidence shows that it is needed now and at this scope?
3. Which specified behavior or constraint would break if it were removed?
4. Is there a smaller, more direct, or more reversible alternative?
5. Can it be deferred until more feedback is available?
6. Does it exist only to support another newly introduced mechanism?
7. What ongoing understanding, validation, change, compatibility, operation, and maintenance costs
   does it create?

Do not retain mechanisms by default when these questions cannot be answered.

### 4. Identify Sources of Entropy

Check:

- **Scope creep**: Does the change solve problems outside the current acceptance scope?
- **Concept proliferation**: Do new terms or abstractions add more cognitive cost than value?
- **Needless indirection**: Do added layers exceed what the problem requires?
- **Duplicated state**: Must multiple representations of one fact remain synchronized?
- **Special cases**: Do a few exceptions impose broad, persistent rules?
- **Change amplification**: Does a simple change require disproportionate knowledge, steps, or
  coordination?
- **Speculative generality**: Are certain costs paid now for benefits that depend on unverified
  future assumptions?
- **Symptom-patch accumulation**: Do individually small local fixes leave a responsibility, semantic,
  module, or variation boundary unresolved while accumulated concepts, exceptions, state, coupling,
  and verification obligations increase total system complexity?
- **NFR-driven abstraction and platformization screening**: Does a non-functional requirement (NFR)
  introduce an abstraction or platformization candidate that requires proportionality review?
  - **Over-abstraction finding**: Conclude NFR-driven over-abstraction only when evidence shows that
    the NFR introduced or generalized a model, interface, policy layer, extension point,
    configuration surface, or abstraction owner whose scope or continuing obligations exceed what a
    demonstrated consumer, stable responsibility or variation boundary, or evidenced root cause
    requires.
  - **Platformization candidate**: An NFR promotes a bounded quality concern into general
    infrastructure and creates continuing variant, extension, lifecycle, compatibility,
    registration, synchronization, operation, or maintenance obligations.

Assess abstraction proportionality and platformization independently. An abstraction can be
proportionate while platformization is present, and an over-abstraction finding can apply without
platformization. Do not report NFR-driven over-abstraction until evidence establishes both that the
NFR drove the abstraction or generalization and that its scope or continuing obligations exceed the
demonstrated need. A technically possible, narrow, or low-frequency condition does not by itself
create a product support obligation. Treat every identified or suspected instance of NFR-driven
platformization as a high-risk entropy signal. Keep it under review until evidence establishes the
relevant facts and minimum sufficient obligations, and any required human-in-the-loop (HITL) decision
resolves support scope, acceptable cost, or the next action under unresolved evidence.
Screen it even when the NFR is an explicit product requirement or protects a hard constraint; an
established support obligation does not exempt the candidate from this proportionality review. Use
these dimensions to find problems. Do not turn them into a mechanical score.

When an abstraction replaces repeated local fixes, verify that the fixes demonstrate the stated
root cause or stable responsibility or variation boundary. Then verify that the abstraction remains
focused on that boundary.

### 5. Distinguish Essential from Accidental Complexity

For suspected symptom-patch accumulation, compare the total cost of continued local fixes with the
smallest root-cause solution. When evidence demonstrates a missing stable boundary, include the
one-time and continuing cost of the minimum sufficient abstraction. Include all affected concepts,
exceptions, state, coupling, and understanding, validation, change, operation, and maintenance
obligations. A smaller current diff is not evidence of lower total entropy.

Keep complexity that:

- Directly supports behavior that must be delivered now.
- Protects a hard constraint.
- Prevents a significant loss demonstrated by current evidence.
- Remains necessary after a smaller solution has been shown to be insufficient.
- Reduces overall duplication, divergence, or long-term maintenance burden despite being locally
  complex.
- Preserves an explicit product NFR or an evidence-backed hard constraint while keeping only the
  minimum platform obligations required to satisfy it.
- Uses the minimum sufficient abstraction when repeated local fixes demonstrate a stable
  responsibility or variation boundary, the abstraction resolves an evidenced root cause, and
  current capabilities are insufficient.

Simplify, defer, or remove complexity that:

- Is justified mainly by “we may need it later.”
- Treats completeness, sophistication, or convention as evidence.
- Builds general capability for one concrete use case.
- Expands an NFR beyond its evidenced scope into unnecessary variants, extension mechanisms, or
  continuing obligations.
- Creates more defenses to explain, verify, or maintain a defense.
- Solves adjacent problems instead of the current goal.
- Plans future stages before the first working result exists.

If any uncertainty remains about the NFR, its need, scope, consumers, continuing obligations, or
acceptable cost, tell the user and use **HITL decision-making** before selecting
an action. Present known facts, gaps, the effects of support and non-support, smaller alternatives,
and a recommendation. Ask the designated human decision owner, or the user if no owner has been
designated, to decide support scope, acceptable cost, or the next action under unresolved evidence,
as applicable.

If HITL selects a bounded investigation, keep the platformization candidate under review and repeat
the proportionality screen after validation. Do not treat the consultation itself as evidence that
the obligations are necessary.

For example, a check for one current artifact can grow into a bounded cross-platform inventory with
traversal, hashing, caps, truncation, and compatibility rules while still failing to prove complete
content identity. Keep the check that serves the current outcome; remove or independently justify
the identity work.

By contrast, repeated local fixes can demonstrate one stable responsibility with no clear owner. A
focused abstraction that owns that responsibility and replaces the patches is necessary design.
Report over-abstraction only when its scope or continuing obligations exceed the demonstrated need.

### 6. Run the Agility Check

Check whether the design, plan, or change:

- Can deliver observable results in small increments.
- Obtains feedback about use, operation, or maintenance early.
- Allows local modification, reversal, or replacement.
- Makes decisions from current learning instead of trying to enumerate the future in advance.
- Focuses effort on working results, not support structures or out-of-scope work.

If testing the core judgment requires a long investment, split the work into smaller increments or
run an experiment first.

### 7. Decide What to Do

Choose one primary action for each mechanism:

- **Keep**: Keep mechanisms that are currently necessary and whose evidence is proportionate to
  their cost.
- **Simplify**: Simplify mechanisms whose goals are valid but whose implementation creates
  unnecessary obligations.
- **Reuse**: Reuse existing capabilities when the need is valid and current capabilities are
  sufficient.
- **Defer**: Defer decisions that may have value but lack current evidence.
- **Remove**: Remove mechanisms that drift from the goal or cost substantially more to maintain than
  their current value.
- **Experiment**: Test the key assumption cheaply before deciding whether to build the mechanism.

Do not merely label something “overdesigned.” Provide a smaller alternative that still satisfies
the current goal.

### 8. Order the Lean Implementation

Organize the work in this order:

1. Remove content that drifts from the current goal.
2. Define the minimum verifiable outcome.
3. Reuse existing capabilities.
4. Deliver the smallest end-to-end slice.
5. Obtain feedback and test key assumptions.
6. Add the next layer of complexity only after evidence appears.

Stop expanding when the current goal is satisfied and the next step is driven only by future
assumptions.

## Output Contract

Provide:

1. **Verdict**: Choose **Keep**, **Simplify**, or **Remove**. Explain the primary basis in one
   paragraph.
2. **Current goal and minimum sufficient solution**: State the problem, observable completion
   outcome, hard constraints, and minimum sufficient solution.
3. **Review findings**: For each actionable finding, state the mechanism, goal relationship,
   evidence, entropy cost, and action. For suspected symptom-patch accumulation, report the
   accumulated obligations, total-complexity effect, demonstrated boundary or evidence gap, and the
   comparison between continued local fixes and the minimum sufficient root-cause solution, including
   a necessary abstraction when a stable boundary is demonstrated. For every identified or suspected
   NFR-driven platformization, report the NFR, current evidence and gaps, continuing platform
   obligations, proportionality conclusion, and action. Report NFR-driven over-abstraction only after
   evidence establishes both that the NFR drove the abstraction or generalization and that its scope
   or continuing obligations are disproportionate; otherwise report the evidence gap without the
   finding. Report any remaining uncertainty and its HITL decision or open decision with its owner.
   For each actionable finding, provide a smaller alternative that preserves the observable outcome
   and every confirmed requirement and hard constraint.
4. **Essential complexity**: Identify what must remain and why.
5. **Lean implementation order**: Provide independently verifiable steps with fast feedback.
6. **Assumptions to test**: List unsupported assumptions and the cheapest way to test each one.

Report only findings that can change a decision or implementation approach, plus the bounded result
for each identified or suspected NFR-driven platformization. If no substantive issue or
platformization candidate exists, return **Keep** and stop; do not manufacture findings to fill the
format.

## Boundaries

- Preserve essential complexity and required checks. To simplify either one, first reduce or
  postpone what the design is expected to do.
- Treat architecture findings as advice. Leave approval, next steps, and changes to the agreed
  design to the designated human decision owner.
- When reviewing architecture, first clarify what the design must do and how it will be checked.
  Then compare its cost with simpler options.
- Do not use agility as a reason to ignore known risks, safety, integrity, or hard constraints.
- Do not require extra artifacts merely to prove that the review occurred.
- Do not expand this into a comprehensive correctness, security, or style review, or redesign the
  whole system unless the current goal requires it.
- Do not let the review cost exceed the scale of the decision being reviewed.
- Use this skill to identify and assess accumulated symptom-patch obligations as an entropy source
  and judge whether architecture or module-design obligations are proportionate. Use
  `backtrace-review` to reconstruct their causal history or determine whether symptom patching or
  NFR-driven platformization caused a non-converging task. The skills can be used independently; do
  not reproduce the complete workflow of one skill in the other.
