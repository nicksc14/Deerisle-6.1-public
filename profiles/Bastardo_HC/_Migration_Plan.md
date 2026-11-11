# BSHC Loot Pool 迁移推进方案

> **目标:** 将 CJ LootChests 6 级副本战利品表完整迁移至 BSHC `loot_pools.json`
> **原则:** Standard 基线 + Advanced 降权分离 | 保留全部武器变种 | 弹匣固定/附件随机 | 不动 Default*

---

## 迁移全景图

CJ 端 6 个副本等级 → BSHC 6 个 Category，按稀有度从高到低推进：

| Phase | Category 名 | CJ 来源事件 | CJ 武器表 | 预估武器 Item 数 | 预估 Pool 数 |
|-------|------------|------------|----------|:---:|:---:|
| **P1** | `Nightmare` | ArcticTemple (Key103) | AJW_Sniper (25) + HERO (12) | ~37 | 5 |
| **P2** | `Red` | Oilrig4 + ShiLuo (Key204) | AJW_Sniper (25) + HERO (12) | ~37 | 5 |
| **P3** | `Green` | Oilrig1/2/3 (Key202) | TTC_Sniper(16) + SNAFU_Sniper(24) + AJW_Sniper(25) | ~65 | 5 |
| **P4** | `Blue` | ParisBunker + Subway (Key201) | AJW_Rifiles(45) + SNAFU_DMR(15) + TTC_DMR(17) | ~77 | 5 |
| **P5** | `Black` | Lance (Key200) | Police(9) + SNAFU_Rifiles(36) + TTC_Rifiles(24) + SNAFU_DMR(15) + TTC_DMR(17) | ~101 | 5 |
| **P6** | `Yellow` | 无 CJ 独占事件 | 设计为 Blue+Red 过渡桥 | ~50 | 4 |

> **P1 Nightmare 已完成 Sample v2** → 当前可直接进入审核

---

## 每 Phase 产出物

每个 Phase 产出 **一个完整、独立可合并的 Category**，包含：

1. **`_[CategoryName]_phase.json`** — 仅该 Category 的 JSON（不含 AllDefinedCategories 外层包裹），可直接粘贴进 `loot_pools.json`
2. **Phase 审核卡** — 列出 CJ 源表→BSHC Pool 的映射表、武器数量、稀有度参数、与上一 Phase 的差异

---

## Phase 推进规则

### 每条审核卡包含以下检查项：

- [ ] CJ 武器预设 **全部** 保留（无遗漏变种）
- [ ] 弹匣 attachment `probability: 1.0`，其余附件 `0.3~0.7`
- [ ] CJ 同槽位多选附件 → `variants[]`
- [ ] CJ 重复权重 → BSHC `probability` 相对权重
- [ ] CJ `|0.x` 后缀 → BSHC `probability` 绝对百分比
- [ ] Standard 事件 → 主基线 Pool (probability ≥ 0.8)
- [ ] Advanced 独占内容 → 独立降权 Pool (probability ≤ 0.3)
- [ ] Category 名称使用描述性英文（如 `Nightmare`, `Red`, `Green`…）

### 推进流程：

```
提出 Phase N 审核卡 → 用户审批 → 生成 _[Category]_phase.json → 用户确认 → 合并入 loot_pools.json → 下一 Phase
```

---

## P1: Nightmare（当前进行中）

### CJ 源

| 事件 | 箱子数 | 武器表 | 弹药/收藏品/贵重品 |
|------|:---:|------|------|
| ArcticTemple_Standard | 81 | AJW_Sniper (25) | SNAFU_Ammo, Ammo_TTC, SNAFU_Ammo_High_Cali, Collection_Common→Legendary→All, BitCoin, Gold |
| ArcticTemple_Advanced | 27 | HERO (12) | SNAFU_Ammo_High_Cali, Collection_Legendary, BitCoin(×2), Gold |

### BSHC Pool 设计

| Pool | 基线来源 | probability | min~max | 内容 |
|------|---------|:---:|:---:|------|
| `Nightmare_Weapons` | Standard | 1.0 | 1~2 | 25 把 AJW Sniper（弹匣固定，其余随机） |
| `Nightmare_Weapons_Rare` | Advanced | 0.25 | 0~1 | 12 把 HERO（25% 概率出现） |
| `Nightmare_Ammo` | Standard | 1.0 | 2~4 | 高口径+标准弹药 |
| `Nightmare_Collectibles` | Standard | 0.8 | 2~5 | Common→Legendary 全梯度 (35 项) |
| `Nightmare_Valuables` | Standard | 0.7 | 1~2 | 金条+矿机+噩梦钥匙 |

### 当前状态

**✅ Sample v2 已完成** → 文件: `_Nightmare_migration_sample.json`

待确认事项：
- 附件随机概率范围 (目前 suppressor 0.5 / optic 0.7 / stock 0.5) 是否合适？
- HERO 池 `probability: 0.25` 是否反映你预期的稀有度？
- 是否需要添加 `Nightmare_Gear`（装备/配件）池？（当前 CJ Nightmare 无此表）

---

## P2: Red

### CJ 源

| 事件 | 箱子数 | 武器表 | 其他 |
|------|:---:|------|------|
| Oilrig4_Standard | 63 | AJW_Sniper (25) | SNAFU_Ammo, Ammo_TTC, SNAFU_Ammo_High_Cali, Collection_Common→Legendary, BitCoin_Low, Gold |
| ShiLuo_Standard | 15 | AJW_Sniper (25) | 同上 |
| Oilrig4_Advanced | 21 | HERO (12) | BitCoin(标准), SNAFU_Ammo_High_Cali, Gold, Collection_Legendary |
| ShiLuo_Advanced | 3 | HERO (12) | 同上 |

### BSHC Pool 设计

| Pool | 基线 | probability | min~max | 内容 |
|------|------|:---:|:---:|------|
| `Red_Weapons` | Standard | 1.0 | 1~2 | 25 把 AJW Sniper |
| `Red_Weapons_Rare` | Advanced | 0.2 | 0~1 | 12 把 HERO（20%, 比 Nightmare 低 5%） |
| `Red_Ammo` | Standard | 1.0 | 2~4 | 高口径+标准 |
| `Red_Collectibles` | Standard | 0.8 | 2~4 | Common→Legendary（与 Nightmare 相同梯度） |
| `Red_Valuables` | Standard | 0.7 | 1~2 | BitCoin_Low(非标准BitCoin) + Gold + CJKeyNightmare |

### 与 Nightmare 的差异

| 维度 | Nightmare | Red | 原因 |
|------|-----------|-----|------|
| HERO 出现率 | 25% | 20% | CJ Advanced:Standard 比例 Nightmare=25% vs Red=24/(63+15)≈24% |
| 收藏品数量 | 2~5 | 2~4 | Red 无 Collection_All 表 |
| Bitcoin 类型 | 标准 BitCoin | BitCoin_Low | CJ Red 用 LC_Table_BitCoin_Low |
| 下级钥匙 | CJKeyNightmare | (无, Red 是顶层的下一级) | — |

---

## P3: Green

### CJ 源

| 事件 | 箱子数 | 武器表 | 其他 |
|------|:---:|------|------|
| Oilrig1/2/3_Standard | 16+16+16=48 | TTC_Sniper(16) + SNAFU_Sniper(24) + AJW_Sniper(25) | SNAFU_Ammo, Ammo_TTC, Collection_Common→Epic, SNAFU_Mags, Gold |

> Green 无 Advanced 事件 → 不需要分离稀有池

### BSHC Pool 设计

| Pool | probability | min~max | 内容 |
|------|:---:|:---:|------|
| `Green_Weapons` | 1.0 | 1~2 | 65 把狙击武器 (TTC+SNAFU+AJW 全保留) |
| `Green_Ammo` | 1.0 | 2~4 | 标准+高级弹药 |
| `Green_Magazines` | 0.8 | 1~3 | SNAFU 系列弹匣 |
| `Green_Collectibles` | 0.7 | 1~3 | Common→Epic（无 Legendary） |
| `Green_Valuables` | 0.6 | 1~2 | Gold + CJKeyYellow |

---

## P4: Blue

### CJ 源

| 事件 | 箱子数 | 武器表 | 其他 |
|------|:---:|------|------|
| ParisBunker + Subway | 7+8=15 | AJW_Rifiles(45) + SNAFU_DMR(15) + TTC_DMR(17) | SNAFU_Ammo, Ammo_TTC, Collection_Common+Rare, SNAFU_Attachments, Gold |

> Blue 无 Advanced 事件

### BSHC Pool 设计

| Pool | probability | min~max | 内容 |
|------|:---:|:---:|------|
| `Blue_Weapons` | 1.0 | 1~2 | 77 把步枪/DMR (AJW+SNAFU+TTC 全保留) |
| `Blue_Ammo` | 1.0 | 2~4 | 标准+高级 |
| `Blue_Attachments` | 0.7 | 1~2 | SNAFU 配件 |
| `Blue_Collectibles` | 0.6 | 1~3 | Common+Rare |
| `Blue_Valuables` | 0.5 | 1~2 | Gold + CJKeyGreen |

---

## P5: Black

### CJ 源

| 事件 | 箱子数 | 武器表 | 其他 |
|------|:---:|------|------|
| Lance | 8 | Police(9) + SNAFU_Rifiles(36) + TTC_Rifiles(24) + SNAFU_DMR(15) + TTC_DMR(17) | SNAFU_Ammo, Collection_Common, Medical, Gold |

> Black 无 Advanced 事件

### BSHC Pool 设计

| Pool | probability | min~max | 内容 |
|------|:---:|:---:|------|
| `Black_Weapons` | 1.0 | 1~2 | 101 把武器 (5 表全保留) |
| `Black_Ammo` | 1.0 | 2~3 | SNAFU 标准弹药 |
| `Black_Collectibles` | 0.5 | 1~2 | Common only |
| `Black_Medical` | 0.6 | 1~2 | 复用 DefaultMedical 内容 |
| `Black_Valuables` | 0.4 | 1~2 | Gold + CJKeyBlue |

---

## P6: Yellow（设计桥）

Yellow 在 CJ 中无独占事件（仅作为钥匙在 Green 箱中产出）。设计为 **Blue → Red 的过渡桥**：

- 武器：Blue 武器池的精选子集 + Red 低概率稀有武器
- 弹药：Blue 与 Red 混合
- 收藏品：Common→Epic
- 无 Advanced 分离（本来就是桥接层）

| Pool | probability | min~max | 内容 |
|------|:---:|:---:|------|
| `Yellow_Weapons` | 1.0 | 1 | 精选 ~50 把 |
| `Yellow_Weapons_Rare` | 0.15 | 0~1 | Red 狙击武器低概率 |
| `Yellow_Ammo` | 1.0 | 2~3 | 混合弹药 |
| `Yellow_Valuables` | 0.5 | 1~2 | Gold + CJKeyRed |

---

## P7: 收尾集成

1. 将 6 个 Category 合并写入 `loot_pools.json`（紧跟现有 Default* 之后）
2. 更新 `BS_Dynamic_crates.json` / `BS_Static_crates.json` 中对应 Crate 的 `LootCategoriesToUse`
3. JSON 语法校验
4. 提醒用户 `!hcreload`

---

## 审批节点

| 节点 | 审批内容 | 产出物 |
|------|---------|--------|
| **N1** ← 当前 | P1 Nightmare Sample v2 审核 | `_Nightmare_migration_sample.json` |
| **N2** | P1 完整版 → 合并 | 完整的 Nightmare Category JSON |
| **N3** | P2 Red 审核卡 | Red 武器列表 + 稀有度参数 |
| **N4** | P2 完整版 → 合并 | 完整的 Red Category JSON |
| ... | 后续 Phase 各一次审核 | ... |
| **N-final** | P7 集成审核 | 完整 loot_pools.json diff |

---

## 下一步

请审核 **P1 Nightmare Sample v2** (`_Nightmare_migration_sample.json`)，确认：
1. 武器变种完整无误？
2. 附件概率（suppressor 0.5 / optic 0.7 / stock 0.5）OK？
3. HERO Rare Pool probability 0.25 OK？
4. 是否需要额外 Pool（如 Gear/Medical）？

确认后我立即生成完整的 Nightmare Category（补全所有 25+12 把武器）并合并入 `loot_pools.json`。
