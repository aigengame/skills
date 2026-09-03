<!-- skills-readme-i18n: source=README.md sha256=31e76458ab20fa1420a1a374557fcb4301ddce839a1854984c8a549370768aa5 -->

# aigengame Agent Skills：在复杂多变的环境中，以证据驱动软件交付

**其他语言：** [English](../README.md) · **简体中文**

[![CI](https://img.shields.io/github/actions/workflow/status/aigengame/skills/validate.yml?branch=main&label=CI&logo=github)](https://github.com/aigengame/skills/actions/workflows/validate.yml)
[![Latest release](https://img.shields.io/github/v/release/aigengame/skills)](https://github.com/aigengame/skills/releases)
[![npx skills](https://img.shields.io/npm/v/skills?logo=npm&label=npx%20skills)](https://www.npmjs.com/package/skills)
[![Node.js 22.20+](https://img.shields.io/badge/Node.js-%3E%3D22.20.0-339933?logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)

## 为什么需要这些 Skills

[Cynefin Framework](https://thecynefin.co/about-us/about-cynefin-framework/)
把问题情境分为 Clear、Complicated、Complex 和 Chaotic。多数软件工作处在后两类情境中。

面对 Complex 或 Chaotic 问题，因果关系往往不清楚，不确定性也远高于可预测性。团队无法只靠事先分析找到答案，而要通过行动、试探、感知和回应建立反馈回路，在持续探索、实验、检查和调整中发现模式、建立秩序。

这种以反馈推进工作的方式，长期以来一直是软件开发的重要基础。

进入 agentic engineering 时代后，包括 SDD（spec-driven development）在内的一些方法，可能在真实行为证据不足时过度依赖计划和规格，最终重新落入瀑布式开发的困境。

> 计划是等待验证的假设，不是必须兑现的承诺。

## 这些 Skills 如何工作

软件项目是复杂系统：需求会变，设计决策相互影响，一个局部优化也可能把成本转移到下游。AI agent 提高了交付速度，也会更快放大错误假设和不必要的复杂度。

这组 Skills 按当前工作的主要问题分为四类：在不确定中设计、稳定执行、审查并维持一致性，以及沉淀项目经验。同时也为以领域为中心的设计、游戏开发和 Godot 提供专项支持。如果你关心 Godot 自动化，可进一步了解 [gda](https://github.com/aigengame/godot-agent)。

这些方法以系统思维、复杂度管理和快速反馈为基础，但不会取代项目自身的规则和人的判断。

### 先判断当前最需要解决的问题

四个板块是反馈回路中的不同入口，不是必须依次经过的开发阶段。

![根据当前工作的主要问题选择 Skill 板块：方向是否仍不确定，执行是否需要受到控制，质量和一致性是否需要审查，或者项目状态和经验是否需要沉淀。每个板块产生的证据都会继续指引下一步决策。](https://media.githubusercontent.com/media/aigengame/skills/3c31159c0bb4183be33310284018aac3b2c1caaa/assets/skill-selection-guide.png)

### 四个板块共同遵循的原则

- **先看证据，再谈信心。** 重要假设经过验证后，才能把方向视为已经确定。
- **管理复杂度。** 只有当架构、流程和保护机制与当前风险相称时，才值得引入。
- **快速获得反馈。** 先做范围小、结果明确的检查，尽早获得反馈，再据此调整方向。
- **明确权威来源。** 系统变化时，要同步责任边界、术语、决策和项目资料，避免各说各话。

## 找到适合的 Skill

<details>
<summary><strong>在不确定中设计</strong></summary>

#### [`validation-driven-design`](../skills/validation-driven-design/SKILL.md)

- **做什么：** 把架构方向当作待验证的假设，对照需求和研究进行判断，再从 prototype 和真实项目中收集证据，最后把结论同步回项目资料。
- **为什么：** 重要决策往往在关键假设得到验证前，就已经带来很高的变更成本。
- **何时使用：** 适合新颖、存在争议、影响范围大或难以逆转的决策。
- **怎么用：** “使用 validation-driven-design 比较这些部署方案，推荐证据最充分的方向，并指出还缺少哪些证据。”

#### [`design-domain-modular-architecture`](../skills/design-domain-modular-architecture/SKILL.md)

- **做什么：** 根据领域模型和项目约束，设计模块边界、职责归属、依赖方向、通信方式和演进路径。
- **为什么：** 只按技术目录划分模块，常常只是把耦合藏起来，并没有反映系统真正的职责边界。
- **何时使用：** 适合设计系统结构、划分职责、审查耦合，或规划渐进式模块化。
- **怎么用：** “使用 design-domain-modular-architecture 为这个领域划分模块，并说明依赖应该朝哪个方向流动。”

#### [`design-godot-modular-architecture`](../skills/design-godot-modular-architecture/SKILL.md)

- **做什么：** 围绕 Add-ons、Systems、Content 和 UI 组织 Godot 项目，建立清楚的职责与单向依赖。
- **为什么：** 随着游戏规模增长，场景、脚本、资源和 UI 很容易互相缠绕。
- **何时使用：** 适合搭建新的 Godot 项目结构、制定模块化方案，或判断游戏资产和行为应该归属哪里。
- **怎么用：** “使用 design-godot-modular-architecture 安排这些场景和系统，让项目能够安全演进。”

#### [`design-verifiable-playtest`](../skills/design-verifiable-playtest/SKILL.md)

- **做什么：** 围绕一个玩法或平衡性问题，基于持续维护的 `gda-balancing` 模型与实验资料，设计一个面向玩家的小型 Godot playtest。它建立在 [`design-godot-modular-architecture`](../skills/design-godot-modular-architecture/SKILL.md) 之上。
- **为什么：** 只在 CLI 中得到的证据，无法验证玩家在游戏中的真实体验。
- **何时使用：** 当 `gda-balancing` 中定义的玩法或平衡假设需要玩家直接反馈时使用。它不适合一般游戏开发任务，也不是 CLI 教程。
- **怎么用：** “使用 design-verifiable-playtest，针对 `gda-balancing` 中的这项假设，利用持续维护的模型和实验资料，设计一个目标明确的可玩实验。”

</details>

<details>
<summary><strong>稳定执行</strong></summary>

#### [`subagent-worktree-parallel`](../skills/subagent-worktree-parallel/SKILL.md)

- **做什么：** 把实现工作拆成彼此独立的切片，在隔离的 Git worktree 中并行推进，再按计划顺序集成和验证。
- **为什么：** 没有预先设计集成路径的并行工作，只会把冲突推迟到风险更高的合并阶段。
- **何时使用：** 当任务确实能拆成多个独立切片、并行收益足以覆盖协调成本，而且已经获得并行执行授权时使用。
- **怎么用：** “使用 subagent-worktree-parallel 把这项工作拆成独立切片，并制定安全的集成顺序。”

#### [`git-conventional-commits`](../skills/git-conventional-commits/SKILL.md)

- **做什么：** 根据暂存区中的实际变更和目标仓库的约定，生成准确的 Conventional Commit 提交说明。
- **为什么：** 含糊或失真的提交信息会削弱历史记录，也可能触发错误的发布行为。
- **何时使用：** 当一个原子变更已经完成暂存、准备提交时使用。
- **怎么用：** “使用 git-conventional-commits 检查暂存区，并为这次变更生成准确的提交信息。”

</details>

<details>
<summary><strong>审查并维持一致性</strong></summary>

#### [`artifact-review`](../skills/artifact-review/SKILL.md)

- **做什么：** 审查 issue、ADR、规格、计划和其他项目文档的正确性、可用性、一致性、完整性、术语和行文。
- **为什么：** 文档即使写得流畅，也可能与证据冲突、遗漏必要决策，或给出无法执行的说明。
- **何时使用：** 当你明确需要审查文档，或需要复核声称已经修复的问题时使用。
- **怎么用：** “使用 artifact-review，对照实现和相关决策审查这份 ADR。”

#### [`skill-review`](../skills/skill-review/SKILL.md)

- **做什么：** 把一个 Skill 的选择描述、操作说明、配套资源、术语和行文作为整体进行审查。
- **为什么：** Skill 通过结构检查，不代表它的触发条件、工作流程和配套材料已经准确、完整。
- **何时使用：** 适合审查新增或修改后的 Skill、以 Skill 为中心的 PR，或复核修订结果。
- **怎么用：** “使用 skill-review，确认这个 Skill 能以最小但充分的结构完成它声明的任务。”

#### [`entropy-review`](../skills/entropy-review/SKILL.md)

- **做什么：** 判断设计、计划或实现引入的复杂度，是否与它要解决的问题相称。
- **为什么：** 范围蔓延、过早泛化和过度防御，会在产生实际价值之前让方案变得难以修改。
- **何时使用：** 当一个方案显得过度设计，或需要判断某个机制是否值得加入、保留或扩大时使用。
- **怎么用：** “使用 entropy-review 找出这份计划中不成比例的复杂度，并给出更小、便于回退的方案。”

#### [`handle-review`](../skills/handle-review/SKILL.md)

- **做什么：** 在采纳审查意见前，先对照当前变更、需求、约束和运行证据验证这些意见。
- **为什么：** 审查意见可能指出了真实问题，却高估其影响，或给出不合适的解决机制。
- **何时使用：** 适合处理 PR 审查意见，或判断一条意见应该原样采纳、调整后采纳，还是拒绝。
- **怎么用：** “使用 handle-review 评估这些意见，落实经过验证的修改，并解释哪些意见不应按原方案采纳。”

#### [`reconcile`](../skills/reconcile/SKILL.md)

- **做什么：** 找出并修复任务记录、需求、决策文档、术语表、测试和其他权威资料之间的漂移。
- **为什么：** 一项决策发生变化后，多个单独看似合理的文档可能已经彼此矛盾。
- **何时使用：** 当需求、范围、决策、职责或术语发生变化后使用。
- **怎么用：** “使用 reconcile 找出这次决策变更影响的全部资料，确保每项事实都有唯一的权威来源，并同步更新依赖这些事实的其他资料。”

</details>

<details>
<summary><strong>沉淀项目经验</strong></summary>

#### [`state`](../skills/state/SKILL.md)

- **做什么：** 重写一份简短的 `STATE.md`，记录当前里程碑、已完成工作、可复用经验、下一步任务和未完成事项。
- **为什么：** 这样下一次工作便能从已知状态继续，不必重新梳理项目进展，也不会遗漏待办事项。
- **何时使用：** 适合在一次工作结束时，或把任务交给另一个 agent 之前使用。
- **怎么用：** “使用 state 记录今天的结果、建议的下一项任务，以及需要留到下次处理的事项。”

#### [`pitfalls`](../skills/pitfalls/SKILL.md)

- **做什么：** 通过项目级 `PITFALLS.md`，避免重复遇到已知的环境、工具、权限、sandbox 和调用问题。
- **为什么：** 经过验证的操作经验很容易丢失，后续工作可能再次运行同样的失败命令，或继续沿用错误的环境假设。
- **何时使用：** 在工具密集型工作开始前、已知坑点可能适用时，或刚确认某个操作问题今后仍可能重现时使用。
- **怎么用：** “运行项目工具前先使用 pitfalls；遇到新的环境问题时，先验证结论，再记录经验。”

</details>

## 安装

你需要 Node.js 22.20 或更高版本，以及 `npx`。

运行安装器，然后根据当前主要问题选择 Skills，并指定目标 agent 和安装范围：

```bash
npx skills add aigengame/skills
```

也可以直接安装一个 Skill，或让 Skills 在多个项目中可用：

```bash
# 安装一个 Skill
npx skills add aigengame/skills --skill entropy-review

# 跨项目安装
npx skills add aigengame/skills --global
```

如需安装指定版本，请在仓库来源后追加 [release tag](https://github.com/aigengame/skills/releases)，例如 `aigengame/skills#v0.1.0`。

Skills 不会自动更新。未指定 release tag 时，可以运行 `npx skills update`；加上 `--project` 或 `--global` 可直接选择范围。通过 release tag 安装的版本会固定在该 tag，需要升级时请安装新的 tag。

## 使用 Skill

先说明当前最需要解决的问题，再选择对应板块，指出要使用的 Skill 和期望结果，并提供相关证据、约束和项目决策。

每个 Skill 条目中的“怎么用”都可以作为起点。如果新证据改变了问题重心，就重新选择。如果你的 agent 提供 Skill 命令或选择器，也可以直接使用，不必在自然语言中点名。

## 获取帮助和反馈

如需报告缺陷、询问用法或提议可复用的 Skill，请使用 [GitHub Issues](https://github.com/aigengame/skills/issues)。请附上 Skill 名称、目标 agent、预期结果和实际情况。

## 参与贡献

如果你想改进现有 Skill，或提出新的可复用 Skill，请阅读 [CONTRIBUTING.md](../CONTRIBUTING.md)，了解仓库范围、验证、审查和发布规则。

## 许可证

本仓库采用 [MIT License](../LICENSE)。
