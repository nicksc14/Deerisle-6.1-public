# BS Hacked Crate (BSHC) — 模组完整指南 (Mod Guide)

> **数据来源:** [BS-Hacked-Crate Official Wiki](https://github.com/cjcarw/BS-Hacked-Crate/wiki) (5 篇页面完整抓取, 2026-07-15 更新)  
> **本地路径:** `$profile/Bastardo_HC/`  
> **生成日期:** 2026-07-15

---

## ⚠️ AI 编辑规则 (Claude Rules — READ FIRST)

**任何对 `profiles/Bastardo_HC/` 下文件的编辑操作，必须遵循以下规则：**

1. **编辑前必须先 Review 本文件** — 充分理解 BSHC 模组的架构、参数含义和跨文件关联后再动手。
2. **JSON 格式严格校验** — BSHC 对 JSON 语法极其敏感，编辑后必须确认格式正确（逗号、引号、括号匹配）。
3. **`ConfigUniqueID` 必须唯一** — 在 `BS_Dynamic_crates.json` 和 `BS_Static_crates.json` 中，每个 Crate 配置的 `ConfigUniqueID` 不可重复，否则会导致行为未定义。
4. **坐标参数禁止手动输入** — `Position` 和 `Rotation` 必须通过 DayZ Editor 或 VPP Admin Tools 的 `getpos` 命令获取。
5. **`LootCategoriesToUse` 必须与 `loot_pools.json` 中的 `AllDefinedCategories` key 一致** — 引用不存在的 Category 会导致战利品不生成。
6. **`admins.txt` 使用 Steam64ID** — 每行一个 64 位 Steam ID，非 Steam 昵称或 32 位 ID。
7. **通知 Key 使用 `#STR_` 前缀** — 引用 `stringtable.xml` 中的本地化字符串；系统会自动根据 `ShowLocationInNotifications` 选择 `_Located` 后缀版本。
8. **编辑后提醒用户执行 `!hcreload`** — BSHC 支持热重载，无需重启服务器即可生效。

---

## 目录 (Table of Contents)

1. [模组概述](#1-模组概述)
2. [文件结构与快速启动](#2-文件结构与快速启动)
3. [全局设置 (BS_Global_settings.json)](#3-全局设置-bs_global_settingsjson)
4. [Crate 配置 (BS_Dynamic_crates.json & BS_Static_crates.json)](#4-crate-配置-bs_dynamic_cratesjson--bs_static_cratesjson)
   - [4.1 身份与生成逻辑](#41-身份与生成逻辑)
   - [4.2 计时器与生命周期](#42-计时器与生命周期)
   - [4.3 需求与安全检查](#43-需求与安全检查)
   - [4.4 地图标记](#44-地图标记)
   - [4.5 通知与本地化](#45-通知与本地化)
   - [4.6 AI 系统 (PvE)](#46-ai-系统-pve)
   - [4.7 战利品与交互](#47-战利品与交互)
   - [4.8 位置配置 (CrateLocations)](#48-位置配置-cratelocations)
   - [4.9 Expansion AI 高级支持](#49-expansion-ai-高级支持)
   - [4.10 状态标记颜色与持久化](#410-状态标记颜色与持久化)
5. [战利品系统 (loot_pools.json)](#5-战利品系统-loot_poolsjson)
   - [5.1 战利品选取逻辑](#51-战利品选取逻辑)
   - [5.2 Pool 设置](#52-pool-设置)
   - [5.3 Item 设置](#53-item-设置)
   - [5.4 Attachment 设置](#54-attachment-设置)
   - [5.5 配置示例](#55-配置示例)
   - [5.6 Pro-Tips](#56-pro-tips)
6. [通知系统](#6-通知系统)
7. [管理员命令与日志](#7-管理员命令与日志)
8. [当前项目配置快照](#8-当前项目配置快照)
9. [常见陷阱与最佳实践](#9-常见陷阱与最佳实践)

---

## 1. 模组概述

**Bastardos Hacked Crate (BSHC)** 是一个 DayZ 高级事件模组，引入类似 Rust 的"可破解箱子"机制。玩家需要:
1. 在地图上找到箱子位置
2. 启动破解序列 (Hacking Countdown)
3. 在倒计时期间抵御 AI 攻击波
4. 倒计时结束后打开箱子获取战利品

### 核心特性

- **混合事件系统:** 同时支持 **Static** (固定坐标) 和 **Dynamic** (随机从位置池选取) 两种生成模式
- **交互式破解:** 需要玩家主动交互启动实时倒计时，箱子上有视觉进度指示器
- **高级 AI 集成:**
  - 箱子生成时原地刷出 AI 守卫
  - 破解期间触发防御性 AI 攻击波
  - **Expansion AI 支持:** 可直接从 config 为 AI 守卫分配特定 Loadout
- **多地图系统集成:** 原生支持 DayZ Expansion Map、BasicMap、LBmaster Advanced Groups、VPP Map
- **实时标记更新:** 标记会动态显示 "Hacking... X%" 或 "Unlocked" 状态
- **强大的战利品系统:** 自定义权重战利品池，支持递归附件、数量控制、物品耐久度
- **LBmaster 集成:** 支持使用 LBmaster 战利品预设替代原生战利品系统
- **热重载:** `!hcreload` 命令即时重载所有配置，无需重启服务器

### 依赖

| 模组 | 必要性 | 用途 |
|------|--------|------|
| **CF (Community Framework)** | 必需 | 基础框架 |
| **DayZ Expansion** | 可选 | AI Loadouts + Expansion 地图标记 |
| **BasicMap** | 可选 | Basic 地图标记 |
| **ExpansionMap** | 可选 | Expansion 地图标记 |
| **LBAdvancedGroup** | 可选 | Advanced Groups 地图标记 + 战利品预设 |

---

## 2. 文件结构与快速启动

### 2.1 文件清单

所有配置文件位于服务器 `$profile/Bastardo_HC/` 目录下：

| 文件 | 用途 |
|------|------|
| `BS_Global_settings.json` | 服务器级别全局设置 (影响所有动态箱子) |
| `BS_Dynamic_crates.json` | 动态事件配置 (随机从位置池选取) |
| `BS_Static_crates.json` | 静态事件配置 (固定在 `StaticSpawns=1` 的坐标) |
| `loot_pools.json` | 战利品池定义 (按 Category 组织) |
| `admins.txt` | 管理员 Steam64ID 列表 (每行一个) |

### 2.2 快速启动

1. 安装模组到服务器和客户端
2. 首次启动服务器 → 模组自动在 `$profile/Bastardo_HC/` 生成默认配置文件
3. 编辑 JSON 文件自定义事件
4. 将管理员 Steam64ID 添加到 `admins.txt`
5. 在游戏内使用 `!hcreload` 热重载配置

---

## 3. 全局设置 (BS_Global_settings.json)

此文件控制模组服务器级别的通用行为，影响所有动态箱子。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ServerStartGracePeriod` | `int` | `5` | 服务器重启后等待多少分钟才开始生成逻辑 (给玩家登录时间) |
| `PeriodicTickIntervalSeconds` | `int` | `3600` | 服务器检查是否需要生成新箱子以补充地图的频率 (秒) |
| `MaxGlobalDynamicCrates` | `int` | `-1` | **全局硬限制:** 地图上所有类型动态箱子的最大总数。`-1` = 不限制 |

**当前项目配置:**
```json
{
    "ServerStartGracePeriod": 5,
    "PeriodicTickIntervalSeconds": 3600,
    "MaxGlobalDynamicCrates": -1
}
```

---

## 4. Crate 配置 (BS_Dynamic_crates.json & BS_Static_crates.json)

两个文件的结构完全相同，区别仅在于 `StaticSpawns` 字段的行为:
- `BS_Dynamic_crates.json`: `StaticSpawns = 0`，从 `CrateLocations` 中随机选取位置
- `BS_Static_crates.json`: `StaticSpawns = 1`，固定在 `CrateLocations` 中的指定位置生成

每个文件是一个 JSON 数组，包含多个 Crate 配置对象。

### 4.1 身份与生成逻辑

| 参数 | 类型 | 说明 |
|------|------|------|
| `ConfigUniqueID` | `String` | **必填。** 唯一标识符 (如 `"Tier1_Mil_Crate"`)。不可重复。 |
| `CrateType` | `String` | 箱子对象的 ClassName (如 `"BS_Hacked_Crate"`) |
| `ActiveCrateCount` | `int` | 此类型箱子在地图上保持活跃的目标数量 |
| `StaticSpawns` | `int` | `1` = 固定在坐标创建; `0` = 从 `CrateLocations` 随机选取 |
| `AutoRefresh` | `int` | `1` = 活跃数量低于目标时自动补充 |
| `RefreshInterval` | `int` | 此配置的刷新检查间隔 (秒) |

### 4.2 计时器与生命周期

| 参数 | 类型 | 说明 |
|------|------|------|
| `CountdownTime` | `int` | **破解持续时间:** 破解完成所需秒数 (如 `900` = 15 分钟) |
| `WarningTimeMinutes` | `int` | **预生成警报:** 箱子物理生成前提前多少分钟警告玩家。`0` = 立即生成 |
| `AutoDespawnTimeMinutes` | `int` | **清理:** 箱子被破解/搜刮后多少分钟自动删除 |
| `MaxLifetimeMinutes_NotTouched` | `int` | **过期事件:** 动态箱子无人交互的最大存活时间 (分钟)。`0` = 不限制 |

### 4.3 需求与安全检查

| 参数 | 类型 | 说明 |
|------|------|------|
| `MinPlayersToSpawnCrate` | `int` | 服务器最少在线玩家数才允许此箱子生成。`0` = 不限制 |
| `EnablePlayerNearbyCheck` | `int` | `1` = 玩家在指定半径内时阻止生成 |
| `PlayerNearbyCheckRadius` | `float` | 生成前检查玩家的距离 (米, 如 `15.0`) |
| `IgnorePlayerCheckOnWarnedSpawn` | `int` | `1` = 如果已发出预警 (`WarningTimeMinutes > 0`)，即使附近有玩家也强制生成 |

### 4.4 地图标记

支持多种地图系统的标记显示，带实时状态更新。

| 参数 | 类型 | 说明 |
|------|------|------|
| `UseExpansionMapMarker` | `int` | `1` = 启用 Expansion Mod 标记 |
| `UseAdvancedGroupsMapMarker` | `int` | `1` = 启用 LBmaster Advanced Groups 标记 |
| `UseBasicMapMarker` | `int` | `1` = 启用 BasicMap 标记 |
| `UseVPPMapMarker` | `int` | `1` = 启用 VPP Map 标记 |
| `ExpansionMarkerColor` | `String` | Expansion 标记 ARGB 颜色 (如 `"255,255,0,0"` = 红色) |
| `AdvancedGroupsMarkerColor` | `String` | AG 标记 ARGB 颜色 |
| `MarkerEnable2D` | `int` | `1` = 在 2D 地图 (M 键) 上显示 |
| `MarkerEnable3D` | `int` | `1` = 在 3D 世界中显示浮动图标 |
| `EnableMarkerHackingProgress` | `int` | `1` = 标记名称实时显示破解进度 (如 "Hacking 50%") |
| `EnableMarkerUnlockedStatus` | `int` | `1` = 破解完成后标记文本变为 "Unlocked" |

### 4.5 通知与本地化

| 参数 | 类型 | 说明 |
|------|------|------|
| `UseCrateNotifications` | `int` | **总开关:** `1` = 启用此箱子的所有通知 |
| `ShowLocationInNotifications` | `int` | `1` = 消息中包含位置名称; `0` = 仅通用消息 |
| `EnableSpawnNotification` | `int` | 箱子物理生成时通知 |
| `EnableStartNotification` | `int` | 破解开始时通知 |
| `EnableEndNotification` | `int` | 破解成功时通知 |
| `EnableDespawnNotification` | `int` | 箱子消失时通知 |
| `EnableMaxCrateNotification` | `int` | 全局限制阻止生成时通知 |
| `MaxCrateNotification_Key` | `String` | "达到限制"消息的 StringTable Key |

**本地化 Key (高级 — 仅在使用自定义 stringtable 时修改):**

系统有两套 Key：不带 `_Located` 的用于通用消息，带 `_Located` 的用于包含位置名称的消息。`ShowLocationInNotifications=1` 时自动使用 `_Located` 版本。

| Key | 对应消息 |
|-----|---------|
| `CrateSpawnNotification_Key` | 箱子生成 (无位置) |
| `CrateSpawnNotification_Key_Located` | 箱子生成 (含位置) |
| `CrateWarningNotification_Key` | 预生成警告 (无位置) |
| `CrateWarningNotification_Key_Located` | 预生成警告 (含位置) |
| `CrateStartNotification_Key` | 破解开始 (无位置) |
| `CrateStartNotification_Key_Located` | 破解开始 (含位置) |
| `CrateEndNotification_Key` | 破解完成 (无位置) |
| `CrateEndNotification_Key_Located` | 破解完成 (含位置) |
| `CrateDespawnNotification_Key` | 箱子消失 (无位置) |
| `CrateDespawnNotification_Key_Located` | 箱子消失 (含位置) |

默认 Key 格式: `#STR_BSHC_Notification_<Type>_Default` / `#STR_BSHC_Notification_<Type>_Located`

### 4.6 AI 系统 (PvE)

#### 初始守卫 (箱子生成时 / 破解开始时刷出)

| 参数 | 类型 | 说明 |
|------|------|------|
| `SpawnAIOnCrateSpawn` | `int` | `1` = 箱子出现时生成 AI 守卫 (看守上锁箱子) |
| `SpawnAIOnHackStart` | `int` | `1` = 破解开始时生成 AI |
| `AISpawnTypes` | `Array<String>` | 生成的 AI ClassName 列表 (如 `["ZmbM_SoldierNormal"]`) |
| `MinAIToSpawn` | `int` | 初始生成最小数量 |
| `MaxAIToSpawn` | `int` | 初始生成最大数量 |
| `AISpawnRadiusMin` | `float` | 初始生成距离箱子最小半径 (米) |
| `AISpawnRadiusMax` | `float` | 初始生成距离箱子最大半径 (米) |

#### 周期性攻击波 (倒计时期间)

| 参数 | 类型 | 说明 |
|------|------|------|
| `UseAIWaves` | `int` | `1` = 启用倒计时期间的攻击波 |
| `NumberOfAIWaves` | `int` | 攻击波总次数 |
| `TimeBetweenAIWavesSeconds` | `float` | 波次之间的间隔 (秒) |
| `AIWaveInitialDelaySeconds` | `float` | 第一次攻击波开始前的延迟 (秒) |
| `AIWaveSpawnTypes` | `Array<String>` | 攻击波的 AI ClassName 列表 |
| `MinAIToSpawnPerWave` | `int` | 每波最小生成数量 |
| `MaxAIToSpawnPerWave` | `int` | 每波最大生成数量 |
| `AIWaveSpawnRadiusMin` | `float` | 攻击波生成最小距离 (米) |
| `AIWaveSpawnRadiusMax` | `float` | 攻击波生成最大距离 (米) |

**注意:** 每个 Location 还可以配置独立的 `AISpawnPositions` 列表，用于指定 AI 的精确生成坐标。

### 4.7 战利品与交互

| 参数 | 类型 | 说明 |
|------|------|------|
| `LootCategoriesToUse` | `Array<String>` | 从 `loot_pools.json` 引用哪些 Category (如 `["DefaultArmaments", "DefaultMedical"]`) |
| `lb_preset_name` | `String` | **LBmaster 集成:** 如果填写此值，则使用 LBmaster 预设替代原生战利品系统。留空则使用 `LootCategoriesToUse` |
| `RequireAccessAction` | `int` | `1` = 破解后玩家需交互 ("Access Loot") 才能解锁; `0` = 破解后自动解锁 |

### 4.8 位置配置 (CrateLocations)

`CrateLocations` 是一个 JSON 数组，包含可能的生成点：

```json
{
    "Position": "x y z",
    "Rotation": "pitch yaw roll",
    "LocationName": "可读的位置名称 (用于通知)",
    "AISpawnPositions": []
}
```

| 字段 | 说明 |
|------|------|
| `Position` | DayZ 世界坐标，格式 `"X Y Z"` (空格分隔) |
| `Rotation` | 朝向，格式 `"Pitch Yaw Roll"` |
| `LocationName` | 位置名称，用于通知消息 |
| `AISpawnPositions` | 此位置专属的 AI 精确生成坐标列表 |

**重要:**
- `StaticSpawns=1` 时，使用 `CrateLocations` 的第一个 (通常唯一) 条目生成固定位置箱子。
- `StaticSpawns=0` 时，系统从 `CrateLocations` 中随机选取 `ActiveCrateCount` 个位置生成动态箱子。

### 4.9 Expansion AI 高级支持

可以在 `AISpawnTypes` 和 `AIWaveSpawnTypes` 中使用高级格式来指定 AI 的 Loadout 和 Faction:

**支持格式:**
- `ClassName|LoadoutName` — 指定 ClassName 和 Expansion Loadout
- `ClassName|loadout:LoadoutName,faction:FactionName` — 同时指定 Loadout 和 Faction

**示例:**
```json
"AIWaveSpawnTypes": [
    "ExpansionZombieBase|loadout:Tier4_Soldier,faction:West",
    "ZmbM_HermitSkinny_Beige"
]
```

### 4.10 状态标记颜色与持久化

| 参数 | 类型 | 说明 |
|------|------|------|
| `UseStateBasedMarkerColor` | `int` | `1` = 根据箱子状态自动切换标记颜色 |
| `MarkerColor_Idle` | `String` | 空闲状态 ARGB 颜色 (如 `"255,230,0,0"`) |
| `MarkerColor_Hacking` | `String` | 破解进行中 ARGB 颜色 (如 `"255,255,200,0"`) |
| `MarkerColor_Unlocked` | `String` | 已解锁状态 ARGB 颜色 (如 `"255,0,200,0"`) |
| `PersistActiveCrateOnRestart` | `int` | `1` = 服务器重启后保持活跃箱子状态 |

---

## 5. 战利品系统 (loot_pools.json)

战利品配置文件结构:

```json
{
    "AllDefinedCategories": {
        "CategoryName1": [ /* 战利品池数组 */ ],
        "CategoryName2": [ /* 战利品池数组 */ ]
    }
}
```

每个 `CategoryName` 对应 Crate 配置中 `LootCategoriesToUse` 引用的名称。

### 5.1 战利品选取逻辑

理解三级决策过程有助于正确配置战利品：

1. **Category 选择** → Crate 的 `LootCategoriesToUse` 列出要使用的所有 Category
2. **Pool 选择 (权重随机)** → 在每个 Category 内，根据 `probability` 权重从 Pool 列表中选一个 Pool
3. **Item 选取 (权重随机 + 保底)** → 选中 Pool 后:
   - `guaranteed_items` 中的物品 **必定生成**
   - `items` 中根据 `min_items`/`max_items` 随机选取 N 件，每件按自身 `probability` 权重决定是否被选中

### 5.2 Pool 设置

| 参数 | 类型 | 说明 |
|------|------|------|
| `pool_name` | `String` | Pool 描述名称 (如 `"M4_Special_Forces"`)，仅用于组织管理 |
| `probability` | `Float` | **选择权重。** 决定此 Pool 在同一 Category 内相对于其他 Pool 被选中的概率。越高越可能被选中 |
| `min_items` | `int` | 从 `items` 列表中随机选取的最小物品数 |
| `max_items` | `int` | 从 `items` 列表中随机选取的最大物品数 |
| `guaranteed_items` | `Array` | 如果此 Pool 被选中，**必定生成**的物品列表 |
| `items` | `Array` | 随机选取的物品池 (按 `min_items`～`max_items` 数量) |

### 5.3 Item 设置

| 参数 | 类型 | 说明 |
|------|------|------|
| `item_name` | `String` | 物品的精确 ClassName (如 `"M4A1"`, `"BakedBeansCan"`) |
| `probability` | `Float` | **选择权重。** 仅当物品在随机 `items` 列表中时使用。值越高越可能被选中 |
| `quantity_min` | `int` | 最小数量 (弹药数、水量、堆叠数)。设为 `-1` 表示满/默认 |
| `quantity_max` | `int` | 最大数量 |
| `health_lvl` | `Float` | 物品状况: `1.0` = 完好无损, `0.7` = 磨损, `0.5` = 损坏。设为 `-1.0` 表示随机/默认 |
| `spawn_count_min` | `int` | 此物品生成的最小份数 (如一次生成 3 个绷带)。默认 `1` |
| `spawn_count_max` | `int` | 此物品生成的最大份数 |
| `attachments` | `Array` | 附加到此物品上的附件列表 (见 §5.4) |

### 5.4 Attachment 设置

附件支持递归嵌套 (附件上再加附件，如光学瞄具里塞电池)。

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | `String` | 附件的 ClassName (如 `"PSO1Optic"`) |
| `probability` | `Float` | **百分比概率 (0.0～1.0):** `1.0` = 100% 必定出现; `0.5` = 50%; `0.1` = 10% |
| `variants` | `Array<String>` | 备选 ClassName 列表。如果提供，系统随机从 `name` 或 `variants` 中选一个 |
| `attachments` | `Array` | 嵌套附件列表 (如瞄具里放电池) |
| `health` | `Float` | 附件耐久度 (`0.0`～`1.0`)。设为 `-1.0` 表示随机/默认 |
| `quantity_min` | `int` | 附件最小数量 (如弹匣中的弹药数) |
| `quantity_max` | `int` | 附件最大数量 |
| `spawn_count_min` | `int` | 最小生成份数 |
| `spawn_count_max` | `int` | 最大生成份数 |

### 5.5 配置示例

#### 示例 1: "Survivalist" (基础)

一个简单的 Pool：保底给背包，随机给食物和饮水。

```json
{
    "pool_name": "Survival_Food_Pack",
    "guaranteed_items": [],
    "items": [
        {
            "item_name": "Pot",
            "attachments": [
                {
                    "name": "TacticalBaconCan",
                    "attachments": [],
                    "probability": 1.0,
                    "health": -1.0,
                    "quantity_min": -1,
                    "quantity_max": -1,
                    "spawn_count_min": 1,
                    "spawn_count_max": 2
                }
            ],
            "probability": 0.5,
            "quantity_min": -1,
            "quantity_max": -1,
            "health_lvl": -1.0,
            "spawn_count_min": 1,
            "spawn_count_max": 1
        },
        {
            "item_name": "Canteen",
            "attachments": [],
            "probability": 0.7,
            "quantity_min": -1,
            "quantity_max": -1,
            "health_lvl": -1.0,
            "spawn_count_min": 1,
            "spawn_count_max": 1
        }
    ],
    "min_items": 3,
    "max_items": 5,
    "probability": 0.6
}
```

#### 示例 2: "Field Medic" (中级)

展示 quantity 和嵌套附件的使用。保底给急救箱，内含固定数量的绷带和概率性的吗啡。

```json
{
    "pool_name": "Field_Medic_Crate",
    "guaranteed_items": [],
    "items": [
        {
            "item_name": "FirstAidKit",
            "attachments": [
                {
                    "name": "BandageDressing",
                    "probability": 1.0,
                    "health": -1.0,
                    "quantity_min": -1,
                    "quantity_max": -1,
                    "spawn_count_min": 2,
                    "spawn_count_max": 2
                },
                {
                    "name": "Morphine",
                    "probability": 0.8,
                    "health": -1.0,
                    "quantity_min": -1,
                    "quantity_max": -1,
                    "spawn_count_min": 1,
                    "spawn_count_max": 1
                }
            ],
            "probability": 1.0,
            "quantity_min": -1,
            "quantity_max": -1,
            "health_lvl": -1.0,
            "spawn_count_min": 1,
            "spawn_count_max": 1
        }
    ],
    "min_items": 2,
    "max_items": 4,
    "probability": 1.0
}
```

#### 示例 3: "Chad M4" (高级)

展示 **Variants** (随机瞄具) 和 **深度嵌套** (瞄具里放电池)。

```json
{
    "pool_name": "Tier4_M4_Setup",
    "guaranteed_items": [
        {
            "item_name": "PlateCarrierVest_Camo",
            "attachments": [
                {
                    "name": "PlateCarrierPouches_Camo",
                    "probability": 1.0,
                    "health": -1.0,
                    "quantity_min": -1,
                    "quantity_max": -1,
                    "spawn_count_min": 1,
                    "spawn_count_max": 1
                }
            ],
            "probability": 1.0,
            "quantity_min": -1,
            "quantity_max": -1,
            "health_lvl": 0.5,
            "spawn_count_min": 1,
            "spawn_count_max": 1
        }
    ],
    "items": [
        {
            "item_name": "M4A1",
            "attachments": [
                {
                    "name": "M4_T3NRDSOptic",
                    "variants": ["ACOGOptic", "StarlightOptic"],
                    "attachments": [
                        {
                            "name": "Battery9V",
                            "probability": 1.0,
                            "health": -1.0,
                            "quantity_min": 100,
                            "quantity_max": 100,
                            "spawn_count_min": 1,
                            "spawn_count_max": 1
                        }
                    ],
                    "probability": 1.0,
                    "health": -1.0,
                    "quantity_min": -1,
                    "quantity_max": -1,
                    "spawn_count_min": 1,
                    "spawn_count_max": 1
                },
                {
                    "name": "Mag_STANAG_30Rnd",
                    "probability": 1.0,
                    "health": -1.0,
                    "quantity_min": 30,
                    "quantity_max": 30,
                    "spawn_count_min": 1,
                    "spawn_count_max": 1
                }
            ],
            "probability": 1.0,
            "quantity_min": -1,
            "quantity_max": -1,
            "health_lvl": 0.9,
            "spawn_count_min": 1,
            "spawn_count_max": 1
        }
    ],
    "min_items": 1,
    "max_items": 1,
    "probability": 1.0
}
```

### 5.6 Pro-Tips

1. **用 Variants 增加多样性:** 与其为同一把枪创建 3 个不同条目(仅为了换瞄具)，不如在光学瞄具上使用 `variants` 数组。系统会从 `name` 和 `variants` 中随机选一个。

2. **嵌套能力极强:** 可以无限层嵌套。例如: `PlateCarrier → Pouches → Grenade inside Pouch`。只需在 Pouches 的定义中添加 `attachments` 数组即可。

3. **战利品 "派对":** 利用 `min_items`/`max_items` 控制数量，可以创建一个 "医疗派对" Pool — 从超大列表中随机选 5～10 件医疗物品，确保玩家获得可观战利品，而无需将每件物品定义为 "Guaranteed"。

4. **权重 vs. 百分比:**
   - **Pool & 随机 Item 使用"权重" (相对概率):** `100.0` 的权重比 `1.0` 高 100 倍被选中的可能性，但不保证一定选中。
   - **Attachment 使用"百分比" (绝对概率):** `1.0` = 100% 必定附上; `0.5` = 50% 概率。

5. **Category 引用必须精确:** `LootCategoriesToUse` 中的名称必须与 `loot_pools.json` 中 `AllDefinedCategories` 的 key 完全一致(大小写敏感)。

---

## 6. 通知系统

### 通知触发时机

| 时机 | Key 变量 | 说明 |
|------|---------|------|
| 预生成警告 | `CrateWarningNotification_Key` | `WarningTimeMinutes > 0` 时触发 |
| 箱子物理生成 | `CrateSpawnNotification_Key` | 箱子在地图上出现时 |
| 破解开始 | `CrateStartNotification_Key` | 玩家开始交互破解时 |
| 破解完成 | `CrateEndNotification_Key` | 倒计时结束/破解成功时 |
| 箱子消失 | `CrateDespawnNotification_Key` | 箱子被搜刮后自动清理时 |

### 位置感知

当 `ShowLocationInNotifications = 1` 时，系统自动使用带 `_Located` 后缀的 Key，并在消息中附加 `LocationName`。不需要为包含位置的消息单独编写模板 — 模组自动处理拼接。

### 自定义通知

如需自定义通知文本，修改 DSL 文件中对应的 `#STR_BSHC_Notification_*` StringTable 条目。

---

## 7. 管理员命令与日志

### 管理员设置

将 **Steam64ID** 逐行添加到 `$profile/Bastardo_HC/admins.txt`:

```
// Put the Steam64IDs of the administrators here, one per line.
YOUR_STEAM64_ID
YOUR_STEAM64_ID
```

### 命令

| 命令 | 说明 |
|------|------|
| **`!hcreload`** | 在游戏内聊天中执行，即时重载所有 JSON 配置（`Global` + `Static` + `Dynamic` + `Loot`），无需重启服务器 |

### 日志系统

模组内置详细日志系统，用于调试生成问题或配置错误。

**日志位置:** `$profile/Bastardo_HC/logs/`

**日志文件名格式:** `BSHC_MissionServer_Session_[Date].log`

**何时查看日志:**
- 箱子不生成
- 战利品不出现
- AI 不生成
- 配置热重载无效
- 任何与预期不符的行为

---

## 8. 当前项目配置快照

### 8.1 BS_Global_settings.json

```json
{
    "ServerStartGracePeriod": 5,
    "PeriodicTickIntervalSeconds": 3600,
    "MaxGlobalDynamicCrates": -1
}
```

### 8.2 BS_Static_crates.json — 当前事件

| ConfigUniqueID | 类型 | 位置 | 倒计时 | 战利品 |
|---------------|------|------|--------|--------|
| `DefaultStaticEvent_Example1` | Static | Zelenogorks | 900s (15min) | DefaultMedical |

### 8.3 BS_Dynamic_crates.json — 当前事件

| ConfigUniqueID | 类型 | 活跃数 | 倒计时 | 战利品 |
|---------------|------|--------|--------|--------|
| `DefaultDynamicEvent_Example1` | Dynamic | 2 | 900s (15min) | DefaultArmaments + DefaultMedical |

**动态位置池:** Airfield (4732, 338, 10350), VMC (4553, 317, 8352)

### 8.4 loot_pools.json — 当前 Category

| Category | Pool 数量 | 用途 |
|----------|----------|------|
| `DefaultMedical` | 1 (Field_Medic_Crate) | 急救物资 |
| `DefaultMisc` | 2 (Explosive_Party, Survival_Food_Pack) | 爆炸物 + 生存补给 |
| `DefaultArmaments` | 2 (Tier4_M4_Setup, AKM_Heavy_Setup) | M4A1 + AKM 全配件 |
| `DefaultSnipers` | 1 (Sniper_Ghillie_Pack) | SVD/Mosin + Ghillie |
| `DefaultBuilding` | 1 (Base_Builder_Starter) | 基地建材 |

---

## 9. 常见陷阱与最佳实践

### 陷阱速查

| 陷阱 | 后果 | 正确做法 |
|------|------|---------|
| `ConfigUniqueID` 重复 | 模组行为未定义，可能只加载其中一个配置 | 确保每个 Crate 配置使用唯一 ID |
| `LootCategoriesToUse` 引用不存在的 Category | 战利品不生成 | 引用的 Category 名必须与 `loot_pools.json` 中 key 严格一致 |
| `probability` 值混淆 | 战利品分配不符合预期 | Pool/Item 用权重(相对)，Attachment 用百分比(绝对 0.0～1.0) |
| Coordinates 手动输入 | 箱子生成在错误位置或地下 | 必须用 DayZ Editor 或 VPP Admin Tools 的 `getpos` 获取 |
| `lb_preset_name` 和 `LootCategoriesToUse` 同时配置 | 战利品行为不确定 | 要么用 LBmaster 预设 (`lb_preset_name`)，要么用原生系统 (`LootCategoriesToUse`) — `lb_preset_name` 优先级更高 |
| 修改配置后不执行 `!hcreload` | 修改不生效，直到下次重启 | 编辑后提醒用户执行 `!hcreload` 或在游戏内聊天中执行 |
| `WarningTimeMinutes` 设置但忘记配 `_Located` Key | 预警消息无位置信息 | 确保同时配置带 `_Located` 和不带的 Key 对 |
| `ActiveCrateCount` > `CrateLocations` 条目数 | 某些生成尝试失败 (无可用位置) | `ActiveCrateCount` ≤ 可用的 `CrateLocations` 条目数 |
| `MaxGlobalDynamicCrates` 设置过低 | 动态箱子无法生成 | 确保全局限制 ≥ 所有 Dynamic Config 的 `ActiveCrateCount` 之和 |

### 最佳实践

1. **分级配置:** 为不同难度创建独立的 Dynamic/Static 配置，使用描述性 `ConfigUniqueID` (如 `"T1_MilCamp"`, `"T4_NavalBase"`)
2. **测试前先减小范围:** 在 `admins.txt` 只添加自己的 ID，设置 `MinPlayersToSpawnCrate=0` 方便单独测试
3. **使用分类良好的 Category:** 按武器类型/用途组织战利品 Category，方便 Crate 配置复用
4. **AI 类型渐进式难度:** `AISpawnTypes` 用基础僵尸，`AIWaveSpawnTypes` 用更强力的变体
5. **保留默认配置作为模板:** 修改前备份默认 JSON 文件
6. **日志优先调试:** 遇到行为异常先检查 `$profile/Bastardo_HC/logs/`
7. **通知保持一致性:** 所有 Crate 配置使用相同的 `#STR_BSHC_*` Key 前缀，方便后续统一修改
