# HANDOFF — DeerIsle 6.1 Expansion Market 结构修复与武器护甲经济重构

> 交接日期：2026-08-12（Asia/Shanghai）  
> 当前阶段：结构修复已落地；统一定价、材料回购商人和最终迁区尚待实施  
> 适用项目根目录：`D:\OneDrive\Deerisle 6.1`  
> 本文件用途：让新的 agent 在不依赖既往对话的情况下恢复上下文、核验现状并继续市场重构。

## 0. 接手者先做什么

按以下顺序读取，不要直接从旧 Market JSON 开始猜设计：

1. 本 HANDOFF。
2. `D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\EXPANSION_MARKET_GUIDE.md`，尤其第 2、7、10、11、12 节。
3. `D:\OneDrive\Deerisle 6.1\Project Manage\合成系统-装备分级与经济基准.md`，尤其第 2—7、10、12—14 节。
4. `D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_MIGRATION.csv`。
5. 本次机器可读报告：`D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\Market_Backup\2026-08-12_structural_repair\REPAIR_REPORT.json`。
6. 再读取当前实际 `Market`、`Traders`、`.map` 和 `traderzones` 文件。运行期实际文件始终优先于文档快照。

重要版本提示：`EXPANSION_MARKET_GUIDE.md` 第 4—6 节记录的是 2026-08-11 的历史审计基线；第 12 节和当前磁盘 JSON 才是结构修复后的状态。不要把“177 个 Market、16 组独立重复、13,428 条库存”误当成当前状态。

## 1. 项目目标与已冻结的用户决策

服务器已统一 AP_EQUIPMENT、FOG、MMG 三个护甲模组，以及 TTC、SNAFU、AJW 三个武器模组的同类数值。市场重构的目标是让经济价格、买卖权限和商人位置与这套数值分阶、A1—A6 合成递进一致，避免玩家因某个模组的旧价格或单一最优解而放弃其他模组。

以下规则已经由用户明确确认，应视为硬约束：

1. 所有普通护甲最终统一到 WestBrook 护甲商人区交易；所有普通枪械最终统一到 Waldoboro 武器商人区交易。普通高等级枪械/护甲不再放在 42 区使用比特币售卖。
2. 所有比特币商品对玩家都是 buy only，即 Trader 模式 `0`；不能出售给比特币商人。
3. 自动随主商品生成、但不应单独显示或单独计价的附件使用模式 `3`，可以保持零价 Market 依赖。主商品的比特币价格仍应是 1,000,000 的整数倍，避免不足一枚比特币却消耗一整枚的问题。
4. Expansion Market 的物品定义是全局定义。车辆、飞机或不同商人可以引用同一 classname，不需要为每个商人复制定义。
5. 因副本递进而禁止 NPC/野外直接获得、但允许玩家回收变现的门槛物品应为 sell only（模式 `2`），不能用 `0/0` 库存伪装禁售。
6. TraderZone 运行期库存必须按 Expansion 逻辑修复，停服、备份、精确处理；禁止为了调价直接清空整个 `Stock`。
7. 无活动 Trader 分类引用、无手动物品引用、也不是 `SpawnAttachments` 依赖的定义，应移出活动 `Market` 到备份目录，不直接删除。
8. 所有后续 Expansion Market 修改，无论价格、权限、物品增删、Trader、TraderZone 或 `.map`，都必须同步写入 `EXPANSION_MARKET_GUIDE.md` 的当前状态和变更日志。

## 2. Expansion Market 在本服的实际结构

```text
D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\
├─ Market\*.json / <模组子目录>\*.json
│  └─ 全局物品定义、价格、库存阈值、SellPricePercent、附件和 Variants
├─ Traders\*.json
│  └─ Trader 分类、单品覆盖、0/1/2/3 权限和结算货币
├─ Market_Backup\
│  └─ 活动 Market 之外的备份与归档；Expansion 不会加载
└─ EXPANSION_MARKET_GUIDE.md

D:\OneDrive\Deerisle 6.1\mpmissions\empty.deerisle\expansion\
├─ settings\MarketSettings.json
├─ traders\*.map
│  └─ 实体/NPC 放置并绑定 Traders 配置基名
└─ traderzones\*.json
   └─ 区域价格倍率和运行期 Stock
```

一次交易的有效链条是：

```text
Market 物品定义
  → Traders 分类/单品权限及货币
  → traders/*.map 放置与绑定
  → 最近的 TraderZone 库存池和倍率
  → 玩家交易并写回 Stock
```

核心参数口径：

- `MinPriceThreshold`：高库存端的最低购买价格。
- `MaxPriceThreshold`：低库存端的最高购买价格。
- `MinStockThreshold` / `MaxStockThreshold`：动态库存价格曲线阈值；相等且大于 0 表示静态库存。
- `SellPricePercent` 使用 0—100 百分数，`20` 才是 20%，`0.2` 是 0.2%。
- Trader 权限：`0` buy only；`1` buy/sell；`2` sell only；`3` hidden。
- Trader `Items` 单品覆盖优先于 `Categories` 分类权限。
- `InitStockPercent` 只在区域缺少该库存键时初始化，不是每次启动重置。
- `Stock` 可能为 Variant 单独存键；Variant 继承父定义的价格和库存阈值。

## 3. 本轮已经完成并写入实际配置的内容

### 3.1 比特币商店

- `Traders\AP_Armor.json`：`Bitcoin-AP-Helmet-Parts:0` 改为 `Bitcoin-AP-Helmet-Parts:3`。AP 头盔附件继续作为零价随附依赖，但不再显示为免费商品。
- `Traders\MagLoader.json`：`Bitcoin_CDS_Suppressor` 和 `Bitcoin_CDS_Supp_Special` 补为模式 `:0`。
- `Market\Bitcoin_CDS_Suppressor.json`、`Market\Bitcoin_CDS_Supp_Special.json`：共 4 个父定义的 `SellPricePercent` 从 `0.2` 改为 `20.0`。
- `Market\Muzzles.json`：`ak_suppressor`、`m4_suppressor` 的同类笔误从 `0.2` 改为 `20.0`。
- 当前 5 个使用 `hm_plus_bitcoin` 的 Trader，其可见/隐藏权限仅使用模式 0/3。

### 3.2 车辆、飞机与重复 classname

- `Traders\Better_Cars.json` 的隐藏依赖从 `Bitcoin_Batteries:3`、`Bitcoin_Vehicle_Parts:3` 改为唯一全局分类 `Batteries:3`、`Vehicle_Parts:3`。
- `Market\Vehicle_Parts.json` 中 `expansionhydraulichoses` 调整为零价隐藏依赖。
- 原来的 16 组独立 classname 重复全部归并；当前活动 Market 的独立重复数量为 `0`。
- `Bitcoin_Batteries.json`、`Bitcoin_Vehicle_Parts.json`、`Bitcoin-Helicopters.json` 已移出活动 Market。

### 3.3 NBC 与防毒门槛物品

7 个独立父定义的库存从 `0/0` 改为动态 `MinStockThreshold=1`、`MaxStockThreshold=100`：

- `nbcbootsgray`
- `nbcjacketgray`
- `nbcpantsgray`
- `nbcglovesgray`
- `nbchoodgray`
- `gasmask`
- `gp5gasmask`

包含灰/黄/白变体在内，共 16 个 classname 已在 `Traders\Clothing.json` 或 `Traders\Clothing_Accessories.json` 中显式覆盖为模式 `2`。它们不能从 NPC 购买，但可以卖给对应 NPC。

### 3.4 无路径定义归档

- 49 个无交易/依赖路径的独立定义已归档。
- 另外归档 15 个重复副本。
- 整文件归档：`Bitcoin_Batteries.json`、`Bitcoin_Vehicle_Parts.json`、`Bitcoin-Helicopters.json`、`Pelts.json`、`Sweaters_And_Hoodies.json`。
- 局部归档：`Ammo.json` 19 项、`Helicopters.json` 3 项、`Launchers.json` 2 项、`Liquids.json` 1 项、`Magazines.json` 9 项。
- 原始 JSON 对象都保留在 `Market_Backup\2026-08-12_structural_repair\archived_market_definitions`，可按 classname 恢复。

### 3.5 TraderZone 精确维护

操作前已确认没有 DayZ/DZSA/Omega/BEC 服务器进程运行，并备份 7 个 TraderZone。没有清空任何区域。

| Zone | 修改前 | 修改后 | 移除过期键 | 移除 NBC 键以重初始化 | 动态库存截顶 |
|---|---:|---:|---:|---:|---:|
| `42.json` | 649 | 637 | 12 | 0 | 0 |
| `Boat_Trader_Rookie.json` | 239 | 233 | 6 | 0 | 0 |
| `Boat_Trader_Spire.json` | 239 | 233 | 6 | 0 | 4 |
| `Rookie_Trader.json` | 5997 | 5132 | 849 | 16 | 1469 |
| `Waldoboro.json` | 1081 | 1067 | 14 | 0 | 0 |
| `WestBrook.json` | 2897 | 2897 | 0 | 0 | 0 |
| `World.json` | 2326 | 1831 | 495 | 0 | 0 |
| **合计** | **13,428** | **12,030** | **1382** | **16** | **1473** |

1473 条截顶包括独立父 classname 和在 TraderZone 单独存储、继承父阈值的 Variant；此前审计中的 569 只统计父项，不是完整口径。

## 4. 当前验证基线

结构修复后已验证：

- 活动 Market JSON：172 个。
- 独立 Market 定义：3164 个。
- Variant 记录：6009 条。
- 独立 classname 重复：0。
- Trader JSON：32 个。
- TraderZone JSON：7 个。
- 加上 `MarketSettings.json`，共 212 个活动 JSON 全部可解析。
- 所有 Trader 分类引用均能解析到活动 Market 文件，包括 `FOG\...`、`Snafu\...` 子目录路径。
- 312 条受管装备迁移清单全部得到目标区域和 Trader，没有 `PENDING_REVIEW`：

| 目标区域 / Trader | 数量 |
|---|---:|
| Waldoboro / `AJW` | 56 |
| Waldoboro / `Rookie_Snafu` | 130 |
| Waldoboro / `TTC` | 77 |
| WestBrook / `AP_Rookie` | 25 |
| WestBrook / `FOG_Trader` | 20 |
| WestBrook / `MMG` | 4 |
| **合计** | **312** |

以上是静态配置验证。尚无本轮修复后的服务器启动 RPT、客户端 Market UI、买卖交易和自动附件生成实机验收记录，因此不要把静态通过描述成已经线上实测通过。

## 5. 有意保留的过渡状态

以下不是遗漏，而是为了避免半迁移造成缺货、双币种或错误价格而暂时保留：

- `AP_Armor` 和 `BIG_GUNS` 仍放置在 42 区并保持旧比特币市场。
- 部分高阶普通枪械/护甲仍在旧比特币分类中。
- 312 条迁移清单已建立，但价格、目标权限、目标分类和 42 区移除尚未同时切换。

最终迁区必须作为一次原子变更完成：冻结统一价格和权限 → 修改 Market → 修改 WestBrook/Waldoboro Trader → 移除 42 区普通枪械/护甲引用及必要的实体放置 → 精确处理受影响 Zone 库存 → 静态验证 → RPT/UI/交易实测。

不要先把 `AP_Armor` / `BIG_GUNS` 从 `42.map` 删除，也不要把旧比特币价格分类直接挂到 Hryvnia Trader。

## 6. 仍未完成且会影响重构的问题

按优先级排列：

1. 统一价格尚未生成。必须基于 A1—A6、武器经济带、护甲防护/容量双轴、材料机会成本和附件功能定价，不能简单按旧价平均或中位数。
2. 13 种合成材料的新回收商人尚未创建，sell-only 权限、单位回购价、发行预算与膨胀护栏均待设计。
3. 18 个多父级 Variant 尚未归并。它们不会造成独立 classname 加载冲突，但可能让同一皮肤继承多个父价格/库存，必须在生成最终价格文件之前处理。
4. Taser 弹药价格 `1` 尚未修复。
5. GCGN 两项不足 1 枚比特币面值的旧商品仍需处理；SNAFU 14.5 弹药可随通用弹药重构一起处理。
6. `MarketSettings.json` 的 `DisallowUnpersisted=0` 仍需作为独立安全策略决定。
7. 当前合成系统正式冻结合同仍有 314/742 与旧 313/742 manifest 的差异；新增项是 `mmg_gp_nvg_black`。市场价格生成应以当前 314/742 实际配置为起点，但上线前仍需重新冻结正式 manifest/hash。
8. 本轮 Market 修复和未来重构都仍需要实机验收。

## 7. 下一位 agent 推荐推进顺序

### 阶段 A：重新审计并冻结输入

1. 确认服务器停止，重新读取本 HANDOFF、Market 指南和经济基准。
2. 解析当前 172 个 Market、32 个 Trader、3 个 `.map`、7 个 TraderZone 以及合成 314/742 配方，不依赖旧笔记输出。
3. 冻结 312 条受管装备名册，并把新增 MMG 全景 NVG 及所有需要统一定价的附件、弹匣、弹药纳入外围账本。
4. 在价格生成前解决 18 个多父级 Variant，保留可恢复备份并更新指南。

### 阶段 B：建立经济账本

1. 先定义 13 种材料的“单单位”回购价和每周 NPC Hryvnia 发行预算。
2. 计算每件成品完整成本：材料、阶段核心、Calibrator、工具损耗、工时、donor。
3. 给武器按 A1—A6 和经济带定价；给护甲按防护与总容量双轴定价。
4. 同 family 的纯皮肤同价；功能、弹匣、附件包、耐久或容量确有差异时才允许加价。
5. 检查四条套利路径：直接卖材料、合成后卖成品、拆解后卖材料、NPC 买入后拆解。任何可重复正收益闭环都不能上线。

### 阶段 C：在隔离目录生成候选配置

1. 不直接覆盖活动 Market；先在 `Economy_Rework` 或新建隔离 staging 目录生成候选 Market/Trader 文件。
2. 使用 `EXPANSION_MARKET_REBUILD_MIGRATION.csv` 作为 312 条迁区控制表。
3. 新材料商人采用模式 `2`；材料分类建议 `SellPricePercent=100`，将 Min/Max 直接作为明确单位回购价。
4. 对只作为随附依赖的物品保持 Market 定义，并在 Trader 中使用模式 `3`。
5. 比特币商品价格必须为 1,000,000 整数倍，所有可见商品模式 `0`。

### 阶段 D：候选配置验证

至少检查：

- 所有 JSON 可解析、版本字段未被擅自修改。
- `MinPriceThreshold <= MaxPriceThreshold`、`MinStockThreshold <= MaxStockThreshold`。
- 独立 classname 重复为 0。
- Variant 不存在多父级歧义。
- 所有 Trader 分类、单品覆盖、SpawnAttachments 和 Variants 引用有效。
- 每个已放置 Trader 都落在正确 TraderZone。
- 每件普通枪械/护甲只在预期区域和货币下可达。
- 门槛物品不可从 NPC 购买；材料只可售出。
- 比特币面值和隐藏附件不会产生少于一枚仍扣一枚、免费附件可见等问题。
- 四类经济闭环全部无正收益。

### 阶段 E：原子切换与实机验收

1. 停服并备份所有将改动的 Market、Trader、`.map`、TraderZone 和指南。
2. 一次性应用价格、权限、分类和放置变更。
3. TraderZone 只精确删除受新阈值/身份影响的库存键；不要清空整个 Stock。
4. 启动后检查 RPT 的 MarketCfgError、缺失 classname、重复定义和附件生成错误。
5. 实机检查 WestBrook/Waldoboro/42 的商品、币种、价格和买卖按钮。
6. 对材料做 1 单位、5 单位、满堆出售；对成品做带附件出售；对比特币商品做整数面值支付；对车辆/AP 头盔做附件自动生成。
7. 将结果、失败项和修复继续写入 Market 指南及本 HANDOFF 的后续交接版本。

## 8. 关键工件、备份和恢复路径

| 文件/目录 | 用途 |
|---|---|
| `D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\EXPANSION_MARKET_GUIDE.md` | 长期机制说明、当前状态和唯一持续变更日志 |
| `D:\OneDrive\Deerisle 6.1\Project Manage\合成系统-装备分级与经济基准.md` | A1—A6、合成成本、材料与经济边界 |
| `D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_ANALYSIS.ipynb` | 2026-08-12 重构交叉审计；是历史快照，需按当前配置重跑/更新 |
| `D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_CROSSWALK.csv` | 312 条受管装备与修复前市场映射；历史基线 |
| `D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_MIGRATION.csv` | 312 条目标区域/Trader/货币迁移控制表 |
| `D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\Market_Backup\2026-08-12_structural_repair\` | 成功迁移前备份、归档对象、报告及使用过的审计脚本 |
| `...\2026-08-12_structural_repair\REPAIR_REPORT.json` | 本轮所有配置变更和 TraderZone 数量报告 |
| `...\2026-08-12_structural_repair_failed_partial\` | 第一次校验中止后的诊断快照；已恢复，不是活动配置 |

如需恢复本轮某一项，不要覆盖整个项目：从成功备份的 `pre_change` 中提取对应原文件，结合 `REPAIR_REPORT.json` 做单项反向变更。TraderZone 是运行期数据，恢复前必须停服并确认不会覆盖修复后的真实玩家交易库存。

## 9. 交接时的文件完整性指纹

以下 SHA-256 只用于确认接手时读取的是 2026-08-12 交接版本；后续正常修改后 hash 改变是预期行为：

```text
988909306075742CCF1D3FCE5076D72B3948284D6885BFEB98E612D764EFCFF1  profiles\ExpansionMod\EXPANSION_MARKET_GUIDE.md
727C86E16EABB1BDEC24CCBAAF5B80A79B9125E7B6D476A4C1428E37BBC2AC0D  profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_ANALYSIS.ipynb
03DDA9B3F0058915972A827EDA60C7D8C08AF7CE3B9CEFB128F722F75CAAF48A  profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_CROSSWALK.csv
C3F8D9AB1063661B1CC9AD4BB8CD6D0157338579E11197259FD7A13A31019FB8  profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_MIGRATION.csv
C3171CAE3673AEAA88EFE3349AD47E52B697C24A904C066F27FBCEFE53F9D20F  profiles\ExpansionMod\Market_Backup\2026-08-12_structural_repair\REPAIR_REPORT.json
9867B94B0F246493EF48A46648F492CEB3145748517F78CA585F78E7692FF952  Project Manage\合成系统-装备分级与经济基准.md
```

## 10. 不要做的事情

- 不要把 Market 指南第 4—6 节的旧数字当成当前状态。
- 不要删除备份目录或无引用定义；恢复价值已经明确。
- 不要为车辆商人和飞机商人重新复制相同 classname。
- 不要把 Market 中 `SellPricePercent=20` 误读为 20 倍或把 `0.2` 误读为 20%。
- 不要通过 `0/0` 库存控制买卖权限；用 Trader 模式 0/1/2/3。
- 不要因为调整价格而清空所有 TraderZone Stock。
- 不要在最终价格未冻结时先拆除 42 区普通高阶枪械/护甲商人。
- 不要把普通高阶枪械/护甲继续设计成比特币黑市专属。
- 不要在缺少发行预算时拍脑袋确定材料回购价格。
- 不要只验证 JSON 解析；必须验证引用、可达性、货币、权限、附件、Variant、库存和套利闭环。
- 不要完成市场修改后漏记 `EXPANSION_MARKET_GUIDE.md`。

## 11. 当前最合适的下一项任务

下一项工作应是：在不修改活动市场的前提下，基于 `合成系统-装备分级与经济基准.md` 和 312 条迁移清单，建立“13 种材料单位回购价 + A1—A6 武器/护甲统一价格 + 附件/弹匣/弹药功能价”的候选经济账本；同时先解决 18 个多父级 Variant。完成账本和套利审计后，再生成隔离的候选 Market/Trader JSON，最后安排原子切换。

---

接手者固定维护规则：开始前读本文件和 `EXPANSION_MARKET_GUIDE.md`；结束时把实际修改、验证、备份和仍未完成事项写回 Market 指南，并在需要再次跨任务交接时更新或新建带日期的 HANDOFF。
