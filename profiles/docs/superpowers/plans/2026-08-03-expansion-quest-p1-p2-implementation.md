# Expansion Quest P1/P2 完整修正实施计划

> **For Codex:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在不覆盖现有用户改动的前提下，完成已批准的新手任务链 P1/P2 修正，并通过全量 JSON、依赖图、Objective 引用和奖励兼容性静态验证。

**Architecture:** 只修改现有 Quest/Objective JSON 的批准字段，并同步维护 `HANDOFF.md`。修改前先运行目标状态断言确认失败；修改后复用同一断言并执行全量结构验证。所有文件使用窄范围 `apply_patch`，不使用 JSON 重序列化工具。

**Tech Stack:** DayZ Expansion Quest JSON v22、Objective JSON v28、`jq`、`rg`、Python 3 只用于跨文件依赖图和引用验证、Git 只用于只读差异检查。

---

## Task 1：保护现有工作区并建立失败基线

**Files:**

- Read: `ExpansionMod/Quests/Quests/Quest_901_StarterGear.json`
- Read: `ExpansionMod/Quests/Quests/Quest_904_Cemetery.json`
- Read: `ExpansionMod/Quests/Quests/Quest_909_CampEagle.json`
- Read: `ExpansionMod/Quests/Quests/Quest_910_BigCity.json`
- Read: `ExpansionMod/Quests/Quests/Quest_911_CityMutants.json`
- Read: `ExpansionMod/Quests/Quests/Quest_912_RenegadeOutpost.json`
- Read: `ExpansionMod/Quests/Quests/Quest_916_FactoryStash.json`
- Read: `ExpansionMod/Quests/Quests/Quest_917_GroundCache.json`
- Read: `ExpansionMod/Quests/Quests/Quest_918_HighRise.json`
- Read: `ExpansionMod/Quests/Quests/Quest_902_EliteGear.json`
- Read: `ExpansionMod/Quests/Quests/Quest_1211_SouthHeaven_Key.json`
- Read: `ExpansionMod/Quests/Objectives/Target/Objective_911_CityMutants.json`
- Read: `ExpansionMod/Quests/HANDOFF.md`

**Step 1：记录目标文件 Git 状态和现有未暂存差异**

Run: `git status --short -- <target paths>` and `git diff -- <target paths>`

Expected: 多个文件为 `A`/`AM`，差异属于用户现有工作；后续只叠加批准字段。

**Step 2：运行目标状态断言**

使用 `jq -e` 检查以下期望状态：

```text
916.PreQuestIDs == [913]
917.PreQuestIDs == [916]
918.PreQuestIDs == [911,912,913,914,915,916,917]
909 rewards contains Ammo_762x39 and not Ammo_762x54
911 rewards contains TerjeFirstAidKitIndividual_Black and not SNAFU_FGKAC_Grip
912 rewards contains Mag_STANAG_60Rnd and not SNAFU_CMAG60556_Black
Objective 2:911 MaxDistance == 500
```

Expected: 非零退出；至少一项仍为旧值，证明测试能捕捉当前问题。

**Step 3：不提交 Quest 文件**

Reason: 这些文件在首个规格提交前已含大量用户暂存/未暂存改动；对它们执行路径提交会把既有内容一并纳入，超出本次授权。实施完成后保留工作树差异供用户统一测试。

## Task 2：修正任务链和 P1 路线/副本文本

**Files:**

- Modify: `ExpansionMod/Quests/Quests/Quest_901_StarterGear.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_904_Cemetery.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_909_CampEagle.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_910_BigCity.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_916_FactoryStash.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_917_GroundCache.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_918_HighRise.json`

**Step 1：修正墓地方向**

- 901 `Descriptions[2]`：`北边的墓地` → `西南方向的墓地`。
- 904 `Descriptions[0]`：`北边的墓地` → `西南方向的墓地`。

**Step 2：修正 Camp Eagle 到 Stonington 方向**

- 909 `Descriptions[2]`：`从Eagle港往东出海` → `从Eagle港往西南方向出海`。
- 910 `Descriptions[0]`：同样改为西南方向。

**Step 3：修正寻宝依赖**

```json
// Quest 916
"PreQuestIDs": [913]

// Quest 917
"PreQuestIDs": [916]

// Quest 918
"PreQuestIDs": [911, 912, 913, 914, 915, 916, 917]
```

保持 913 和 902 不变。

**Step 4：修正 918 完成描述**

把 17 个副本改为 18 个；把必掉下一颜色钥匙改为副本箱有概率产出后续阶段钥匙；保留“新城全部任务完成”和推荐信衔接语义。

**Step 5：解析本任务文件**

Run: `jq empty <seven modified quest files>`

Expected: 退出码 0，无输出。

## Task 3：修正 P2 奖励与 911 半径

**Files:**

- Modify: `ExpansionMod/Quests/Quests/Quest_909_CampEagle.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_911_CityMutants.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_912_RenegadeOutpost.json`
- Modify: `ExpansionMod/Quests/Objectives/Target/Objective_911_CityMutants.json`

**Step 1：修正 909 弹药路径**

把 Reward classname `Ammo_762x54` 改为 `Ammo_762x39`，Amount 保持 100；完成描述补充该弹药可供当前 SKS 使用。

**Step 2：修正 911 中阶医疗奖励**

把 `SNAFU_FGKAC_Grip` 改为 `TerjeFirstAidKitIndividual_Black`，Amount 保持 1；完成描述改为 IFAK 的 10 次容量、止血/手术用途，不再提握把。

**Step 3：修正 912 M4 弹匣**

把 `SNAFU_CMAG60556_Black` 改为 `Mag_STANAG_60Rnd`，Amount 保持 2；完成描述改为“两只原版 60 发 STANAG 弹匣”。

**Step 4：收紧 911 Target 范围**

把 `MaxDistance: 1500.0` 改为 `500.0`；其他字段不变。

**Step 5：运行奖励断言**

Run: `jq -e` 检查三个新 classname、三个 Amount、旧 classname 不存在、`MaxDistance == 500`。

Expected: 退出码 0。

## Task 4：修正 902 与 1211 的真实机制文本

**Files:**

- Modify: `ExpansionMod/Quests/Quests/Quest_902_EliteGear.json`
- Modify: `ExpansionMod/Quests/Quests/Quest_1211_SouthHeaven_Key.json`

**Step 1：修正 902 奖励名称**

`Descriptions[2]` 的“满配M4加M1A”改为“满配黑色MDAR步枪加M1A”，其余毕业装备和 1211 引导保持不变。

**Step 2：重写 1211 三阶段描述**

- 接取：说明抵达 T4 标记区域后任务自动完成，两把钥匙由任务系统发放。
- 进行中：说明无需寻找地面物品，也无需返回 NPC。
- 完成：明确已发放 `CJ_Key4` 和 `CJ_Key6`，分别用于传送/撤离与 T4 战利品箱。
- `ObjectiveText`：同时写明取得 `CJ_Key4` 与 `CJ_Key6`。

**Step 3：验证结构与机制字段未变**

Run: `jq -e` 检查 `Autocomplete == 1`、Reward classnames 仍为 `CJ_Key4`/`CJ_Key6`、Objective 仍复用 `ObjectiveType 3 + ID 1202`。

Expected: 退出码 0。

## Task 5：同步 HANDOFF

**Files:**

- Modify: `ExpansionMod/Quests/HANDOFF.md`

**Step 1：更新第 9 节状态**

把全部 P1/P2 项更新为“配置已验证”，内容写成实际实施结果；P3 保持待确认。

**Step 2：更新第 13 节回归测试重点**

写入 910 后 911–915、913→916→917、918 全前置、911 500 米、IFAK、原版 60 发 STANAG、902 MDAR 文本和 1211 系统奖励测试。

**Step 3：追加第 14 节变更日志**

记录日期 2026-08-03、执行者 Codex、状态、所有涉及文件/ID、修改前后、源码/配置依据、静态验证结果、服务器待测项和字段级回滚方式。

**Step 4：更新第 15 节**

移除已完成的 P1/P2 实施行动；把一次性服务器回归测试列为首要行动，P3 保持后续。

## Task 6：全量静态验证与差异审查

**Files:**

- Verify: `ExpansionMod/Quests/Quests/*.json`
- Verify: `ExpansionMod/Quests/Objectives/**/*.json`
- Verify: `ExpansionMod/Quests/NPCs/*.json`
- Verify: all modified files

**Step 1：全量 JSON 解析与计数**

Run: `find ... -name '*.json' -print0 | xargs -0 -n1 jq empty`

Expected: 全部退出码 0；数量仍为 60 Quest、73 Objective、6 NPC。

**Step 2：运行目标状态断言**

复用 Task 1 的断言，并增加方向、18 个副本、概率措辞、MDAR 和 1211 三阶段文本检查。

Expected: 退出码 0；旧错误值不再存在于目标字段。

**Step 3：验证依赖图和 Objective 引用**

用 Python 只读加载 JSON：

- Quest ID 唯一；所有 `PreQuestIDs` 存在；DFS 无循环。
- 所有 Quest Objective 引用能按 `(ObjectiveType, ID)` 唯一解析。
- 每个 Quest 有三段 `Descriptions`；Reward 必要字段完整。
- ConfigVersion 仍为 Quest 22、Objective 28、NPC 6。

Expected: 输出验证摘要，无错误并以 0 退出。

**Step 4：验证新增 classname 和兼容依据**

Run: `rg` 检查 Terje IFAK 定义、M4A1 的 `Mag_STANAG_60Rnd` 兼容补丁、MDAR displayName。

Expected: 三项均命中本地已加载配置。

**Step 5：审查最终差异**

Run: `git diff -- <modified paths>` and `git diff --check -- <modified paths>`

Expected: 无空白错误；只出现批准字段、文本和 `HANDOFF.md` 维护内容；不覆盖既有无关差异。

**Step 6：交付服务器测试清单**

报告静态验证结果、修改文件和仍需实际服务器验证的行为；不把静态通过称为“服务器已验证”。
