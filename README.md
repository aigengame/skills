# aigengame/skills

**Systems-thinking and agile-driven Agent Skills for delivering software in
complex, changing environments.**

[![Latest release](https://img.shields.io/github/v/release/aigengame/skills)](https://github.com/aigengame/skills/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

This catalog helps AI agents make better software decisions, control unnecessary
complexity, preserve project knowledge, and validate important changes with evidence.
Use one skill for a focused task or combine several across a longer workflow.

## Why these skills

Software projects are complex systems. Requirements change, design decisions interact,
and local improvements can create downstream costs. AI agents increase delivery speed,
but they can also amplify a wrong assumption or an overcomplicated direction.

These skills apply systems thinking, entropy management, and agile feedback to common
software-engineering work. They provide repeatable methods without replacing project
authority or human judgment.

- **Evidence before confidence.** Test important assumptions before treating a
  direction as settled.
- **Proportionate complexity.** Add architecture, process, and safeguards only when
  their value matches the current risk.
- **Fast feedback.** Use small, observable checks to learn and adapt early.
- **Clear authority.** Keep ownership, terminology, decisions, and project artifacts
  aligned as the system changes.

## Find the right skill

### Design under uncertainty

#### [`validation-driven-design`](skills/validation-driven-design/SKILL.md)

- **What:** Validates architecture direction through requirements, research,
  prototypes, real-world trials, and cross-artifact reconciliation.
- **Why:** Important decisions often become expensive before their assumptions have
  been tested.
- **When:** Use it for novel, disputed, broad, or difficult-to-reverse decisions.
- **How:** Ask: “Use validation-driven-design to compare these deployment options and
  recommend an evidence-backed direction.”

#### [`design-domain-modular-architecture`](skills/design-domain-modular-architecture/SKILL.md)

- **What:** Turns a domain model and project constraints into module boundaries,
  ownership, dependencies, communication, and evolution paths.
- **Why:** Technical folder boundaries often hide coupling instead of reflecting the
  system's real responsibilities.
- **When:** Use it when structuring a system, assigning responsibilities, reviewing
  coupling, or planning incremental modularization.
- **How:** Ask: “Use design-domain-modular-architecture to propose boundaries for this
  domain and explain the dependency direction.”

#### [`design-godot-modular-architecture`](skills/design-godot-modular-architecture/SKILL.md)

- **What:** Designs Godot projects around Add-ons, Systems, Content, and UI with
  directed dependencies and clear ownership.
- **Why:** Scenes, scripts, resources, and UI can become tightly coupled as a game
  grows.
- **When:** Use it for a new Godot structure, a modularization plan, or a review of
  where game assets and behavior belong.
- **How:** Ask: “Use design-godot-modular-architecture to place these scenes and
  systems in a structure that can evolve safely.”

#### [`design-verifiable-playtest`](skills/design-verifiable-playtest/SKILL.md)

- **What:** Designs a small player-facing Godot playtest around one balance or
  gameplay question.
- **Why:** A model or command-line experiment cannot show whether a mechanic is clear,
  readable, and convincing to a player.
- **When:** Use it when a gameplay or balance hypothesis needs direct player feedback,
  not for a general game or a CLI-only tutorial.
- **How:** Ask: “Use design-verifiable-playtest to turn this balance question into a
  focused playable experiment.”

#### [`entropy-review`](skills/entropy-review/SKILL.md)

- **What:** Reviews whether a design, plan, or implementation introduces complexity
  proportionate to the problem it solves.
- **Why:** Scope creep, premature generalization, and defensive mechanisms can make a
  solution harder to change before they deliver value.
- **When:** Use it when a proposal feels overengineered or when deciding whether a
  mechanism is worth adding, retaining, or expanding.
- **How:** Ask: “Use entropy-review to identify disproportionate complexity in this
  plan and propose a smaller reversible alternative.”

### Review and maintain coherence

#### [`artifact-review`](skills/artifact-review/SKILL.md)

- **What:** Reviews issues, ADRs, specifications, plans, and other project documents
  for correctness, usability, consistency, completeness, terminology, and prose.
- **Why:** A polished document can still contradict its evidence, omit a required
  decision, or give readers instructions they cannot use.
- **When:** Use it when you explicitly need a document review or a re-review of claimed
  fixes.
- **How:** Ask: “Use artifact-review to review this ADR against the implementation and
  its related decisions.”

#### [`skill-review`](skills/skill-review/SKILL.md)

- **What:** Reviews a skill's selection description, instructions, resources,
  terminology, and prose as one usable artifact.
- **Why:** A skill can pass structural checks while its trigger, workflow, or bundled
  material remains inaccurate or incomplete.
- **When:** Use it for a new or changed skill, a skill-focused pull request, or a
  re-review after fixes.
- **How:** Ask: “Use skill-review to verify that this skill can do its declared job
  with the smallest sufficient structure.”

#### [`handle-review`](skills/handle-review/SKILL.md)

- **What:** Verifies review feedback against the current change, requirements,
  constraints, and runtime evidence before applying it.
- **Why:** A review can identify a real problem but overstate its impact or recommend
  the wrong mechanism.
- **When:** Use it when responding to pull request feedback or deciding whether to
  adopt, adapt, or decline a finding.
- **How:** Ask: “Use handle-review to evaluate these comments, implement verified
  fixes, and explain any finding we should not adopt as written.”

#### [`reconcile`](skills/reconcile/SKILL.md)

- **What:** Finds and repairs drift among tracked work, requirements, decision records,
  glossaries, tests, and other authoritative artifacts.
- **Why:** A changed decision can leave several individually plausible documents that
  no longer agree.
- **When:** Use it after a requirement, scope, decision, responsibility, or term
  changes.
- **How:** Ask: “Use reconcile to find every artifact affected by this decision change
  and restore one consistent authority.”

### Execute reliably

#### [`state`](skills/state/SKILL.md)

- **What:** Rewrites a short `STATE.md` with the current milestone, completed work,
  reusable experience, next tasks, and unfinished backlog.
- **Why:** The next session should continue from known state instead of rediscovering
  project progress and losing pending work.
- **When:** Use it at the end of a working session or before handing work to another
  agent.
- **How:** Ask: “Use state to record today's outcome, the next recommended task, and
  the unfinished work that must survive this session.”

#### [`pitfalls`](skills/pitfalls/SKILL.md)

- **What:** Uses a project-level `PITFALLS.md` to prevent repeated environment, tool,
  permission, sandbox, and invocation failures.
- **Why:** Verified operational lessons are often lost, so later sessions repeat the
  same failed command or environment assumption.
- **When:** Use it before tool-heavy work, when a known pitfall may apply, or after
  confirming a reusable operational failure.
- **How:** Ask: “Use pitfalls before running the project tools, and record any new
  environment lesson only after it is verified.”

#### [`subagent-worktree-parallel`](skills/subagent-worktree-parallel/SKILL.md)

- **What:** Plans and orchestrates independent implementation slices in isolated Git
  worktrees, followed by ordered integration and validation.
- **Why:** Parallel work can move conflicts from implementation time to a risky,
  unplanned merge phase.
- **When:** Use it when several independent slices justify the coordination cost and
  parallel execution is authorized.
- **How:** Ask: “Use subagent-worktree-parallel to divide this work into independent
  slices and define a safe integration order.”

#### [`git-conventional-commits`](skills/git-conventional-commits/SKILL.md)

- **What:** Formulates a Conventional Commit message from the staged change and the
  target repository's own conventions.
- **Why:** A vague or inaccurate commit message weakens history and can trigger the
  wrong release effect.
- **When:** Use it when one atomic change is staged and ready to commit.
- **How:** Ask: “Use git-conventional-commits to inspect the staged change and create
  the precise commit message for it.”

## Install

You need a Node.js installation that includes `npx`.

Choose skills interactively:

```bash
npx skills add aigengame/skills
```

Install one skill:

```bash
npx skills add aigengame/skills --skill entropy-review
```

Install skills for the current user instead of one project:

```bash
npx skills add aigengame/skills --global
```

The installer lets you select the target agent and installation scope. For a
reproducible installation, select a version from
[GitHub Releases](https://github.com/aigengame/skills/releases) and append its tag to
the repository source, such as `aigengame/skills#v0.1.0`.

## Use a skill

Name the skill and the outcome you need in your request. For example:

```text
Use entropy-review to check whether this caching design is proportionate to
the current requirements.

Use artifact-review to review this ADR against the implementation and related
decisions.

Use state to record the current milestone, completed work, and next tasks.
```

Agents that support dedicated skill invocation can use their native syntax instead.
The linked `SKILL.md` for each catalog entry defines its complete workflow and
boundaries.

## Help and feedback

Use [GitHub Issues](https://github.com/aigengame/skills/issues) for defects, usage
questions, and proposals for reusable skills. Include the skill name, target agent,
what you expected, and what happened.

## Contributing

Want to improve an existing skill or propose a reusable one? Read
[CONTRIBUTING.md](CONTRIBUTING.md) for scope, validation, review, and release rules.

## License

This repository is available under the [MIT License](LICENSE).
