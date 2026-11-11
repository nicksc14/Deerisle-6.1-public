# Expansion Quest P1/P2 完整修正规格

**日期：** 2026-08-03  
**状态：** 用户已批准设计，待实施  
**范围：** DeerIsle 新手任务链 P1/P2；不处理 P3 NPC 文件名/模型问题

## 目标

修复新手任务链中会造成提前解锁、奖励不兼容、错误引导和任务语义失真的 P1/P2 问题，并在服务器一次性回归测试前完成静态配置验证。

## 已核验依据

- Expansion 源码 `ExpansionQuestModule.c` 会逐项统计 `PreQuestIDs`，只有全部前置任务完成才显示后续任务，因此多个前置是 AND 关系。
- 916 的 Treasure Objective 固定生成原版 `M4A1`，附件为 `M4_OEBttstck`、`M4_PlasticHndgrd`、`M4_CarryHandleOptic`。
- 本地已加载 M4 配置明确将 `Mag_STANAG_60Rnd` 加入 `M4A1_Base` 的 `magazines[]`；`SNAFU_CMAG60556_Black` 不在该兼容列表中。
- `SNAFU_FGKAC_Grip` 的配置说明和插槽表明它只用于 SNAFU Modular Picatinny rail，不兼容 916 的原版 M4A1。
- `TerjeFirstAidKitIndividual_Black` 是 10 次容量 IFAK，具备止血和手术能力；强度位于 907 的 `TerjeSurgicalKit` 与 914 的 20 次 AFAK 之间。
- `SNAFUMDARRIF_Black` 的本地显示名为 `MDAR Rifle Black`。
- 坐标差值确认 NPC 3 到墓地、Camp Eagle 到 Stonington 均为西南方向。

## 设计

### 1. 任务链与解锁

- 913 保持 `PreQuestIDs: [910]`。
- 916 从 `[910]` 改为 `[913]`。
- 917 从 `[910]` 改为 `[916]`。
- 918 从 `[910]` 改为 `[911, 912, 913, 914, 915, 916, 917]`。
- 902 保持 `[911, 912, 913, 914, 915, 916, 917, 918]`。

结果：910 后可并行处理 911–915；寻宝任务按 913→916→917 推进；完成 911–917 后才开放高价值 918；完成 918 后才满足 902 的全部前置。

### 2. P1 文本修正

- 901 完成描述和 904 接取描述：墓地方向由“北边”改为“西南方向”。
- 909 完成描述和 910 接取描述：Camp Eagle/Eagle 港到 Stonington 的路线由“往东”改为“往西南”。
- 918 完成描述：地牢数量由 17 改为 18；“每个箱子都掉下一级钥匙”改为“副本箱有概率产出后续阶段钥匙”，不再承诺必掉。

### 3. P2 奖励修正

- 909：`Ammo_762x54` ×100 改为 `Ammo_762x39` ×100，与 901 获得的 SKS 立即兼容；同步更新完成描述。
- 911：`SNAFU_FGKAC_Grip` ×1 改为 `TerjeFirstAidKitIndividual_Black` ×1；同步将完成描述改为 IFAK 的正确用途，不再提握把。
- 912：`SNAFU_CMAG60556_Black` ×2 改为 `Mag_STANAG_60Rnd` ×2；同步将完成描述改为原版 60 发 STANAG 弹匣。

奖励数量、Chance、DamagePercent、HealthPercent、QuestID 和其他 Reward 字段保持不变。

### 4. 目标半径

- `Objective_911_CityMutants.json` 的 Target `MaxDistance` 从 `1500.0` 改为 `500.0`。
- 中心坐标、击杀数 15、感染者 classname、Travel Objective 和其他计数条件不变。

### 5. 奖励与任务语义

- 902 完成描述把“满配 M4”改为实际奖励“黑色 MDAR 步枪”，M1A 和其他装备描述保持一致。
- 1211 的接取、进行中、完成描述与 `ObjectiveText` 明确：玩家抵达标记区域后任务自动完成，`CJ_Key4` 与 `CJ_Key6` 由任务奖励系统发放；不存在地面预放钥匙，也无需返回 NPC。

### 6. HANDOFF 同步

- 第 9 节把全部 P1/P2 条目标为“配置已验证”或“已实施、待配置验证”，以实际验证结果为准。
- 第 13 节同步新的解锁顺序、911 半径、奖励兼容和 1211 文本测试重点。
- 第 14 节追加一条完整变更日志，记录涉及文件、修改前后、依据、验证结果和回滚方式。
- 第 15 节移除已经完成的 P1/P2 首要行动，保留服务器回归测试和 P3 后续事项。

## 预计修改文件

- `ExpansionMod/Quests/Quests/Quest_901_StarterGear.json`
- `ExpansionMod/Quests/Quests/Quest_904_Cemetery.json`
- `ExpansionMod/Quests/Quests/Quest_909_CampEagle.json`
- `ExpansionMod/Quests/Quests/Quest_910_BigCity.json`
- `ExpansionMod/Quests/Quests/Quest_911_CityMutants.json`
- `ExpansionMod/Quests/Quests/Quest_912_RenegadeOutpost.json`
- `ExpansionMod/Quests/Quests/Quest_916_FactoryStash.json`
- `ExpansionMod/Quests/Quests/Quest_917_GroundCache.json`
- `ExpansionMod/Quests/Quests/Quest_918_HighRise.json`
- `ExpansionMod/Quests/Quests/Quest_902_EliteGear.json`
- `ExpansionMod/Quests/Quests/Quest_1211_SouthHeaven_Key.json`
- `ExpansionMod/Quests/Objectives/Target/Objective_911_CityMutants.json`
- `ExpansionMod/Quests/HANDOFF.md`

913 与相关 Objective 只参与验证，不需要修改。

## 静态验证

1. 先以断言检查确认旧的错误值仍存在，使测试在修改前失败。
2. 修改后解析全部 60 Quest、73 Objective、6 NPC JSON。
3. 断言上述 P1/P2 的新值和新文本全部存在，旧的错误类名、方向、数量和措辞不存在于相关字段。
4. 建立 Quest ID 集合，验证所有 `PreQuestIDs` 存在且依赖图无环。
5. 按 `ObjectiveType + ID` 验证所有 Quest Objective 引用唯一存在。
6. 验证所有 Quest 保留三段描述，所有 Reward 必要字段完整。
7. 从本地配置再次验证新增 classname 存在，并确认 `Mag_STANAG_60Rnd` 与原版 M4A1 的兼容补丁仍在加载配置中。
8. 确认文件数量和 ConfigVersion 均未变化，并检查差异只涉及批准范围。

## 服务器回归测试

- 910 后最初只开放 911–915；完成 913 后开放 916，完成 916 后开放 917。
- 918 在 911–917 全部完成前不可接取；完成后才开放。
- 911 在距目标中心 500 米内击杀 15 只目标感染者可计数，区域外击杀不计数。
- 909 的 7.62×39 弹药可直接供 SKS 使用。
- 911 正常发放 IFAK；912 的两只原版 60 发 STANAG 可装入 916 获得的 M4A1。
- 902 文本与实际 MDAR 奖励一致。
- 1211 到达区域后自动完成并发放两把钥匙，无需寻找地面物品或返回 NPC。

## 回滚

仅反向恢复上述字段和文本，不覆盖目标文件中既有的其他用户改动；`HANDOFF.md` 追加“已回滚”日志，不删除历史记录。
