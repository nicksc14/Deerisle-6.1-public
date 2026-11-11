# BS KeyRoom — 模组完整指南 (Mod Guide)

> **版本覆盖:** v1.0.8+  
> **数据来源:** [BS-KeyRoom Official Wiki](https://github.com/cjcarw/BS-KeyRoom/wiki) (8 篇页面完整抓取, 2026-03-13 更新)  
> **本地路径:** `$profile/BS_KeyRoom/`  
> **生成日期:** 2026-07-14

---

## ⚠️ AI 编辑规则 (Claude Rules — READ FIRST)

**任何对 `profiles/BS_KeyRoom/` 下文件的编辑操作，必须遵循以下规则：**

1. **编辑前必须先 Review 本文件** — 充分理解 BS KeyRoom 模组的架构、参数含义和跨文件关联后再动手。
2. **JSON 格式严格校验** — BS KeyRoom 对 JSON 语法极其敏感，一个逗号或引号的错误会导致服务器崩溃。编辑后必须用 JSON 验证器（如 jsonlint.com）检查。
3. **`BS_KeyRoom_Cooldowns.json` 绝对不可手动编辑** — 这是模组自动管理的运行时状态文件。
4. **坐标参数禁止手动输入** — `x/y/z`、`building_x/y/z`、`door_indices` 必须由游戏内 `BS_DoorLocker` 管理工具生成。容器的 `position` 和 `orientation` 需要通过 DayZ Editor 或 VPP Admin Tools 的 `getpos` 命令获取。
5. **保持文件关联一致性** — 修改 `BS_KeyRoom_ItemNames.json` 中的 ClassName 时，同步检查所有 DoorConfig 中引用的 `keycard_class_name`/`keycard_class_names`；修改 `BS_KeyRoom_Settings.json` 中的 Global LootPool 名称时，同步检查所有 DoorConfig 中的 `lootPoolName` 引用。
6. **`debug_build` 上线必须置 0** — 编辑完成后若曾设为 1 进行测试，必须在提交前重置为 0。
7. **新增 DoorConfig 的 `Location_Name` 必须唯一** — 重复的名称会导致冷却追踪冲突。
8. **参数名区分大小写** — JSON key 必须与官方文档完全一致。

---

## 目录 (Table of Contents)

1. [模组概述](#1-模组概述)
2. [安装指南](#2-安装指南)
3. [初始设置与文件结构](#3-初始设置与文件结构)
4. [门配置 (Door Configuration)](#4-门配置-door-configuration)
5. [高级战利品系统 (Advanced Loot System)](#5-高级战利品系统-advanced-loot-system)
6. [AI 生成系统 (AI Spawning System)](#6-ai-生成系统-ai-spawning-system)
7. [载具生成系统 (Vehicle Spawning System)](#7-载具生成系统-vehicle-spawning-system)
8. [钥匙与门禁卡配置](#8-钥匙与门禁卡配置)
9. [主设置文件 (BS_KeyRoom_Settings.json)](#9-主设置文件-bs_keyroom_settingsjson)
10. [管理员命令与快捷键](#10-管理员命令与快捷键)
11. [当前项目配置快照](#11-当前项目配置快照)
12. [常见陷阱与最佳实践](#12-常见陷阱与最佳实践)

---

## 1. 模组概述

**BS KeyRoom** 是一个 DayZ 服务器的钥匙门系统模组。它允许管理员创建需要特定钥匙/门禁卡才能打开的上锁房间，房间内可以生成：
- **战利品容器** (可配置固定掉落、随机池、LBmaster 预设)
- **AI 防守者** (原版僵尸/动物 + Expansion AI 士兵)
- **载具奖励** (打开门后临时生成，关门后自动删除)
- **可破解的箱子** (Bastardos Hacked Crates 集成)

**核心特性：**
- 所有配置均为纯 JSON 文件，无需重打包 PBO
- 支持热重载（`!kcreload` 管理员命令）
- 权重的随机选择系统（spawnChance 控制概率）
- 支持 Expansion Mod、LBmaster Rework、Bastardos Hacked Crates 集成
- 管理员 GUI 面板（按 `K` 键）

---

## 2. 安装指南

### 2.1 前提条件
- 一台正常运行的 DayZ 服务器 (PC)
- FTP 或文件管理器访问权限
- 服务器启动脚本访问权限

### 2.2 安装步骤

1. **订阅模组** — Steam Workshop 订阅 `@BS_KeyRoom`
2. **上传文件** — 将本地 `!Workshop\@BS_KeyRoom` 文件夹上传到服务器根目录
3. **添加启动参数** — 在 `-mod=` 中加入 `@BS_KeyRoom;`
   ```
   DayZServer_x64.exe -config=serverdz.cfg -port=2302 "-mod=@CF;@BS_KeyRoom;"
   ```
4. **生成默认配置** — 首次启动服务器后，模组会在 `$profile/BS_KeyRoom/` 下自动创建所有配置文件

### 2.3 可选依赖

| 模组 | 收益 |
|------|------|
| **DayZ-Expansion** | 更丰富的全局通知系统（Expansion Notifications 格式） |
| **CFTools / GameLabs** | 玩家交互日志输出到外部服务 |
| **LBmaster Rework** | 容器内使用 LBmaster 战利品预设 |
| **Bastardos Hacked Crates** | 门打开时生成可破解的箱子 |

### 2.4 故障排除

| 问题 | 解决方案 |
|------|----------|
| 配置文件未生成 | 确认模组正确加载，检查 `adm.log` |
| 门不响应门禁卡 | 确认 `debug_build` 为 0（上线模式）且门配置正确生成 |
| 服务器启动崩溃 | 用 [jsonlint.com](https://jsonlint.com) 检查 JSON 语法错误 |

---

## 3. 初始设置与文件结构

### 3.1 文件夹结构

```
$profile/
└── BS_KeyRoom/
    ├── DoorConfigs/                      ← 每个门一个 JSON 文件
    │   └── GreenMontainRedKeycard.json   ← 自动生成的示例
    ├── logs/                             ← 详细调试/管理员日志
    ├── BS_KeyRoom_Settings.json          ← 全局设置 & 全局战利品池
    ├── BS_KeyRoom_ItemNames.json         ← 钥匙/门禁卡名称、描述、使用次数
    ├── BS_KeyRoom_Cooldowns.json         ← 活跃门的冷却状态（自动管理，勿动！）
    └── admins.txt                        ← 管理员 Steam64ID
```

> ⚠️ **绝对不要手动编辑 `BS_KeyRoom_Cooldowns.json`。** 此文件由模组自动管理，用于在服务器重启之间持久化门状态。

### 3.2 初始配置三步骤

#### ① 设置管理员 (`admins.txt`)
- 每行一个 Steam64ID
- 通过 [steamid.io](https://steamid.io/) 查询
- 示例：
  ```
  YOUR_STEAM64_ID
  YOUR_STEAM64_ID
  ```

#### ② 查看主设置 (`BS_KeyRoom_Settings.json`)
关键设置：
| 设置 | 值 | 说明 |
|------|-----|------|
| `debug_build` | `1` | 启用在游戏内管理工具 (`BS_DoorLocker`)，上线必须为 `0` |
| `admin_log` | `1` | 写入详细玩家交互日志到 `logs/` 文件夹 |
| `showDoorTimerText` | `1` | 显示"Door closing in Xm Xs"给看着门的玩家 |

#### ③ 理解钥匙配置 (`BS_KeyRoom_ItemNames.json`)
无需立即修改，但需要知道位置。详见 [第 8 节](#8-钥匙与门禁卡配置)。

> ⚠️ **当前项目状态:** `admins.txt` 为空（无管理员 Steam64ID 填写），意味着没有人可以使用 `!kcreload` 命令或按 `K` 打开管理面板。在添加管理员之前，所有配置修改后都需要重启服务器才能生效。

---

## 4. 门配置 (Door Configuration)

每个受 BS KeyRoom 控制的门都必须有一个单独的 `.json` 文件存放在 `BS_KeyRoom/DoorConfigs/` 中。

### 4.1 使用管理工具自动创建配置（最快方式）

**步骤：**
1. 在 `BS_KeyRoom_Settings.json` 中设 `debug_build` 为 `1`
2. 以管理员身份生成物品 `BS_DoorLocker`
3. 对准目标门，按住鼠标左键，触发动作 "Setup Keycard Door"
4. 新的 `.json` 文件会生成在 `DoorConfigs/` 中，预填了建筑坐标、门位置和门索引

> 生成文件后，停止服务器，编辑填充战利品/计时器等内容，再重启。

### 4.2 完整参数参考

#### 📍 核心识别参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `x`, `y`, `z` | Float | 门的世界坐标。**由管理工具生成，不要手动编辑。** |
| `building_x`, `building_y`, `building_z` | Float | 建筑的世界坐标。**由管理工具生成，不要手动编辑。** |
| `door_indices` | Array | 此配置控制的建筑门索引列表。一个门禁卡可以同时打开多扇门。 |
| `linked_doors` | Array | 其他门配置的 `Location_Name` 列表。当此门打开时，所有链接的门同时打开。适用于双门入口。 |
| `Location_Name` | String | **唯一**标识符，用于日志和冷却追踪。在所有门 JSON 文件中必须唯一。 |
| `BuildingClassName` | String | 建筑的 classname。由管理工具自动获取。 |

#### 🔑 钥匙/门禁卡设置

| 参数 | 类型 | 说明 |
|------|------|------|
| `keycard_class_name` | String | **单个**需求的物品 classname。向后兼容。 |
| `keycard_class_names` | Array | **(v1.0.8+)** 可以开此门的 classname 列表。若玩家携带**任意一个**即可开门。若和 `keycard_class_name` 同时设置，此参数优先。例: `["BS_Key_Red", "BS_Key_Master"]` |
| `showRequiredKeys` | 0/1 | `1` = 显示所需钥匙名称给玩家（如 "Requires Red Keycard"）。`0` = 显示通用消息（适合神秘/硬核服务器） |
| `sound_accept` | String | 成功解锁时播放的 SoundSet。留 `""` 则无声。默认 `"Sound_Door_Accepted"` |
| `sound_deny` | String | 无有效钥匙的玩家靠近时播放的 SoundSet。留 `""` 则无声。默认 `"Sound_Door_Denied"` |

#### 🚪 门行为

| 参数 | 类型 | 说明 |
|------|------|------|
| `unlockOnly` | 0/1 | `1` = 门禁卡仅解锁门，玩家需要手动开门。`0` = 自动开门 |
| `use_continuous_action` | 0/1 | `1` = 使用"按住"动作而非单按（需要 `BS_ActionOpenDoorContinuous`） |
| `reputationReward` | Int | 打开门的玩家获得声望点数。设 `0` 禁用 |

#### 📢 公告与警报

| 参数 | 类型 | 说明 |
|------|------|------|
| `use_announcement` | 0/1 | `1` = 门禁卡使用时发送全服公告 |
| `announcement_title` | String | 公告标题（如 `"ALERT"`） |
| `announcement_text` | String | 公告正文 |
| `announcement_color_rgba` | String | Expansion 通知颜色格式 `"Alpha,Red,Green,Blue"` (0-255)。仅 Expansion 加载时有效 |
| `use_alarm` | 0/1 | `1` = 在门位置播放循环警报声 |
| `alarm_sound` | String | 警报 SoundSet classname（如 `"Alarm_Military"`） |
| `alarm_duration` | Int | 警报播放总时长（秒） |
| `alarm_loop_delay` | Float | 每次警报声循环之间的秒数。越小越频繁 |

#### ⏱️ 计时器

| 参数 | 类型 | 说明 |
|------|------|------|
| `min_unlock_time` | Int | 门禁卡使用后到门打开的最短秒数 |
| `max_unlock_time` | Int | 最长秒数。在 min 和 max 之间随机选择 |
| `min_restock_time` | Int | 门保持打开的最短秒数，之后自动关闭和清除战利品 |
| `max_restock_time` | Int | 最长秒数。在 min 和 max 之间随机选择 |

#### 📦 战利品与容器

| 参数 | 类型 | 说明 |
|------|------|------|
| `containers_only` | 0/1 | `1` = 容器在服务器启动时永久生成。门始终锁定且不能用门禁卡打开。用于持久化战利品房间 |
| `min_containers_to_spawn` | Int | 从 `containers` 数组中选择的最少容器数。设 `-1` 总是生成全部定义的容器 |
| `max_containers_to_spawn` | Int | 最多生成容器数 |

#### 🛡️ 安全与重启持久化

| 参数 | 类型 | 说明 |
|------|------|------|
| `persistCooldownOnRestart` | 0/1 | `1` = 门开关/冷却状态在服务器重启后正确恢复。**强烈建议保持 `1`** |
| `delay_close_if_player_nearby` | 0/1 | `1` = 若 `safety_teleport_radius` 内有存活的玩家，门不会关闭。每 60 秒重新检查直到区域清空 |
| `use_safety_teleport` | 0/1 | `1` = 门关闭前检查房间内是否有玩家，将其传送出去避免被困 |
| `safety_teleport_radius` | Float | 安全传送扫描的半径（从建筑中心起算，米） |
| `use_custom_teleport_points` | 0/1 | `1` = 将玩家传送到 `custom_teleport_points` 中的指定点而非随机附近位置 |
| `custom_teleport_points` | Array | `"X Z Y"` 世界坐标列表（注意 DayZ 轴顺序）。每次随机选择一个点 |

#### 🤖 AI 防守者

| 参数 | 类型 | 说明 |
|------|------|------|
| `aiToSpawnOnOpen` | Array | 门打开时生成的 AI 实体配置列表（详见第 6 节） |
| `min_ai_to_spawn` | Int | 列表中生成的最少 AI 数。`-1` 生成全部 |
| `max_ai_to_spawn` | Int | 最多 AI 数。`-1` 生成全部 |

#### 🚗 载具

| 参数 | 类型 | 说明 |
|------|------|------|
| `vehiclesToSpawn` | Array | 门打开时生成的载具配置列表（详见第 7 节） |
| `min_vehicles_to_spawn` | Int | 列表中最少载具数。`-1` 生成全部 |
| `max_vehicles_to_spawn` | Int | 最多载具数。`-1` 生成全部 |

#### 🔗 模组集成 — Bastardos Hacked Crates

| 参数 | 类型 | 说明 |
|------|------|------|
| `spawn_hacked_crate` | 0/1 | `1` = 门打开时生成可破解箱子 |
| `hacked_crate_classname` | String | 可破解箱子的 classname |
| `hacked_crate_position` | String | 世界坐标 `"X Y Z"` |
| `hacked_crate_orientation` | String | 朝向 `"Pitch Yaw Roll"` |
| `hacked_crate_config_id` | String | Hacked Crates 模组配置中的 `ConfigUniqueID` |

### 4.3 最小配置示例

```json
{
    "x": 3689.39,
    "y": 5985.54,
    "z": 403.74,
    "building_x": 3686.41,
    "building_y": 5982.14,
    "building_z": 407.67,
    "door_indices": [0],
    "Location_Name": "GreenMountain_Main_Barracks",
    "BuildingClassName": "Land_Mil_Barracks5",
    "keycard_class_name": "BS_keycard_lab_red",
    "min_restock_time": 300,
    "max_restock_time": 300,
    "min_containers_to_spawn": 2,
    "max_containers_to_spawn": 2,
    "persistCooldownOnRestart": 1,
    "containers": [],
    "doorSpecificLootPools": []
}
```

---

## 5. 高级战利品系统 (Advanced Loot System)

此系统是 BS KeyRoom 最强大的功能。通过两个数组在每个门 JSON 文件中配置：`doorSpecificLootPools` 和 `containers`。

### 5.1 容器的选择机制

门级别的两个参数控制生成容器数量：

| 参数 | 说明 |
|------|------|
| `min_containers_to_spawn` | 最少容器数，`-1` = 总是生成全部 |
| `max_containers_to_spawn` | 最多容器数 |

系统基于每个容器的 `spawnChance` 进行**加权随机选择**。`spawnChance: 1.0` 的容器被选中的概率是 `0.1` 的十倍。省略 `spawnChance` 默认为 `1.0`。

### 5.2 战利品池 (Loot Pools)

战利品池是一个可复用的命名物品列表，可定义在两个位置：
- **全局池** — 在 `BS_KeyRoom_Settings.json` 的 `lootPools` 中。所有门可用。适合通用层级。
- **门专属池** — 在某门 JSON 的 `doorSpecificLootPools` 中。仅该门的容器可用。适合独有奖励。

#### 池结构

```json
{
    "lootPoolName": "Military_Weapons_HighTier",
    "rewards": [
        {
            "name": "M4A1",
            "chanceToSpawn": 0.5,
            "quantityMin": 1,
            "quantityMax": 1,
            "attachments": [
                { "name": "M4_RISHndgrd", "quantity": 1 },
                { "name": "Mag_STANAG_30Rnd", "quantity": 30 }
            ]
        }
    ]
}
```

#### 奖励物品参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | String | 物品的 `className` |
| `chanceToSpawn` | Float | 相对**权重** — 非百分比。越大相对池内其他物品越可能被选中。例：`1.0` 的物品被选中几率是 `0.5` 的两倍 |
| `quantityMin` | Int | 最少生成数量（弹药、食物、弹匣有用） |
| `quantityMax` | Int | 最多数量。在 min 和 max 间随机 |
| `attachments` | Array | 生成时附带的物品（见附件系统） |

### 5.3 附件系统 (Attachment System)

三种模式可自由组合和嵌套：

#### 直接附件 — 总是附带
```json
{
    "name": "M4A1",
    "attachments": [
        { "name": "Mag_STANAG_30Rnd", "quantity": 30 },
        { "name": "M4_RISHndgrd", "quantity": 1 }
    ]
}
```

#### 随机附件 — `name` 为空，`random_names` 从中随机选一
```json
{
    "name": "M4A1",
    "attachments": [
        { "name": "Mag_STANAG_30Rnd", "quantity": 30 },
        { "name": "", "random_names": ["ACOGOptic", "M68Optic", "BUISOptic"] }
    ]
}
```

#### 嵌套附件 — 附件也可有自己的附件，任意深度
```json
{
    "name": "SNAFUKivaari_Tan_GUN",
    "attachments": [
        { "name": "", "random_names": ["ACOGOptic", "M68Optic"],
          "attachments": [
              { "name": "Battery9V", "quantity": 1 }
          ]
        }
    ]
}
```

### 5.4 容器坐标的获取

> ⚠️ **错误坐标会导致容器生成在墙内、飘在空中或地图下方。**
> `BS_DoorLocker` 管理工具只创建门配置 — 它不放置容器。

**推荐方法：**
- **DayZ Editor** — 离线模式工具，可放置物体并导出坐标
- **VPP Admin Tools** 或 **Community Online Tools** — 游戏内管理员模组，有 `getpos` 命令

**坐标格式：**
| JSON 字段 | 轴 | 说明 |
|-----------|-----|------|
| `position` | [X, Y, Z] | Y = 地面以上高度 |
| `orientation` | [Yaw, Pitch, Roll] | Yaw = 左右旋转 |

**步骤：**
1. 在离线模式加载地图，或用管理员工具连接到服务器
2. 飞/传送到门禁卡房间位置
3. 生成要使用的容器 `className`（如 `BS_Guncase`）
4. 移动和旋转直到看起来正确 — 不穿墙、不悬空
5. 使用工具的检查器或 `getpos` 命令复制 Position 和 Orientation

### 5.5 容器配置完整参考

#### 基础参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `referenceName` | String | — | 唯一名称，用于日志 |
| `className` | String | — | 实体 classname（如 `BS_Guncase`, `BS_Box1_Black`） |
| `position` | Array | — | 世界坐标 `[X, Y, Z]` |
| `orientation` | Array | — | 旋转 `[Yaw, Pitch, Roll]` |
| `spawnChance` | Float | `1.0` | 加权概率 |
| `objectScale` | Float | `1.0` | 视觉比例。`0.75`=75%大小，仅影响外观不影响碰撞体 |

#### 容器锁参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `requiredItem` | String | `""` | 若设置，生成的容器（必须是 `BS_Storage_Base`）被锁定，需要此物品 classname 来打开 |
| `unlockTime` | Float | `0` | 使用 `requiredItem` 解锁容器需要的按住秒数 |
| `consumeItem` | 0/1 | `0` | `1` = 解锁容器使用的物品被消耗/销毁 |

#### 战利品方法参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `useFixedLoot` | 0/1 | `0` | `1` = 启用 `fixedItems` 中的保证物品 |
| `fixedItems` | Array | `[]` | 保证掉落的物品列表（方法 A） |
| `lootPoolName` | String | `""` | 从中抽随机物品的单个池名（方法 B） |
| `randomLootPools` | Array | `[]` | 多个池名列表。行为取决于 `spawnFromAllPools`（方法 B2） |
| `spawnFromAllPools` | 0/1 | `0` | `0` = 随机选一个池。`1` = 从所有列出的池合并抽取 |
| `lootMin` | Int | `0` | 最少随机物品数 |
| `lootMax` | Int | `0` | 最多随机物品数 |
| `preventDuplicateLoot` | 0/1 | `0` | `1` = 同一物品 classname 在容器中只能出现一次 |

#### LBmaster 集成参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `lb_preset_name` | String | `""` | LBmaster Rework 预设名。若设置，绕过了整个内部战利品系统 |

#### 替换容器参数

| 参数 | 替换的对应字段 |
|------|----------------|
| `replacementChance` | — (0.0~1.0，替换概率) |
| `replacementClassName` | `className` |
| `replacementUseFixedLoot` | `useFixedLoot` |
| `replacementFixedItems` | `fixedItems` |
| `replacementLootPoolName` | `lootPoolName` |
| `replacementRandomLootPools` | `randomLootPools` |
| `replacementLootMin` | `lootMin` |
| `replacementLootMax` | `lootMax` |
| `replacementPreventDuplicateLoot` | `preventDuplicateLoot` |
| `replacement_lb_preset_name` | `lb_preset_name` |

#### 固定物品参数 (Method A)

| 参数 | 类型 | 说明 |
|------|------|------|
| `name` | String | 物品 classname |
| `quantity` | Int | 非可堆叠物品：生成这么多件。可堆叠物品：见下方百分比 |
| `quantityMinPercent` | Float | 仅对可堆叠物品：以最大容量的分数表示的最小填充量 (`0.5` = 50%) |
| `quantityMaxPercent` | Float | 最大填充分数。在 min 和 max percent 间随机 |
| `attachments` | Array | 附件（使用相同的嵌套系统，见 5.3） |

### 5.6 四种战利品方法

#### 方法 A — 保证掉落 (`useFixedLoot` + `fixedItems`)
`fixedItems` 中的物品**总是**生成，且附加在任何随机池的额外物品之上：

```json
{
    "referenceName": "Medical_Crate",
    "className": "BS_Box1_White",
    "useFixedLoot": 1,
    "fixedItems": [
        { "name": "BandageDressing", "quantity": 4 },
        { "name": "SalineBag", "quantity": 1 }
    ],
    "lootPoolName": "Global_HighTier_Medical",
    "lootMin": 0,
    "lootMax": 2
}
```

#### 方法 B — 单池随机战利品
```json
{
    "lootPoolName": "Military_Weapons_HighTier",
    "lootMin": 1,
    "lootMax": 3
}
```

#### 方法 B2 — 多池随机战利品
`spawnFromAllPools: 0` — 随机选一个池：
```json
{
    "randomLootPools": ["Global_Military_Weapons_T4", "Global_Military_Gear_T4"],
    "spawnFromAllPools": 0,
    "lootMin": 1,
    "lootMax": 2
}
```

`spawnFromAllPools: 1` — 所有池合并为一个大池：
```json
{
    "randomLootPools": ["Global_Military_Weapons_T4", "Global_Military_Gear_T4"],
    "spawnFromAllPools": 1,
    "lootMin": 2,
    "lootMax": 4
}
```

#### 方法 C — LBmaster Rework 集成
```json
{
    "lb_preset_name": "Full_SNAFU_M4_Kit"
}
```
> `lb_preset_name` 必须与 LBmaster 配置中的 `preset_name` **完全匹配**（区分大小写）。

#### 方法 D — 替换容器
一个基础容器有概率被更稀有的容器替换（玩家看不到原始容器生成）：

```json
{
    "referenceName": "Tools_or_Rare_Gun",
    "className": "BS_Box1_White",
    "lootPoolName": "Global_Industrial_Tools",
    "lootMin": 3,
    "lootMax": 5,
    "replacementChance": 0.10,
    "replacementClassName": "BS_Guncase_Black",
    "replacementLootPoolName": "Global_Military_Weapons_T4",
    "replacementLootMin": 1,
    "replacementLootMax": 1
}
```
- **90%** → 白箱子 + 3-5 个随机工业工具
- **10%** → 黑枪柜 + 1-2 个 T4 武器

---

## 6. AI 生成系统 (AI Spawning System)

> 从 **v1.0.8+** 开始可用

当玩家使用门禁卡成功开门时：
1. 系统读取 `aiToSpawnOnOpen` 和 `min_ai_to_spawn` / `max_ai_to_spawn`
2. 执行基于各 AI `spawnChance` 的**加权随机选择**
3. 选中的 AI 实体生成在定义的世界坐标
4. **AI 被击杀后不会重生** — 只在下次门被解锁时再次生成
5. 门冷却结束后关闭时，所有存活的 AI 自动清除

### 6.1 AI 条目参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `referenceName` | String | `"AI_Spawn"` | 唯一名称，用于日志 |
| `className` | String | `"ZmbM_PatrolNormal_Autumn"` | 实体 classname。原版直接使用 classname。Expansion AI 使用管道格式（见下文） |
| `position` | Array | `[0, 0, 0]` | 世界坐标 `[X, Y, Z]` |
| `orientation` | Array | `[0, 0, 0]` | 旋转 `[Yaw, Pitch, Roll]` |
| `spawnChance` | Float | `1.0` | 此 AI 被选中的加权概率 |

### 6.2 门级别 AI 参数

| 参数 | 说明 |
|------|------|
| `min_ai_to_spawn` | 最少生成数。`-1` = 总是全部生成 |
| `max_ai_to_spawn` | 最多生成数。`-1` = 总是全部生成 |

### 6.3 Expansion AI — className 管道格式

```
"className": "AI_Class|LoadoutFile|FactionName"
```

| 部分 | 说明 |
|------|------|
| `AI_Class` | 基础实体类（如 `eAI_SurvivorM_Mirek`, `eAI_SurvivorF_Eva`） |
| `LoadoutFile` | `$profile:/ExpansionMod/Loadouts/` 中的装备 JSON 文件名 — **不含** `.json` 后缀 |
| `FactionName` | Expansion AI 阵营名（如 `Mercenaries`, `Raiders`, `Guards`） |

> ⚠️ 三部分全部写在同一行 `className` 中，用 `|` 分隔。没有单独的 loadout 或 faction 字段。

> ⚠️ Expansion AI 需要加载 **DayZ-Expansion-AI** 模组。若未加载，管道格式被忽略且实体会生成失败。

### 6.4 示例

**纯原版僵尸：**
```json
{
    "aiToSpawnOnOpen": [
        { "referenceName": "Guard_1", "className": "ZmbM_PatrolNormal_Autumn",
          "position": [1320.5, 290.0, 9285.0], "orientation": [0, 0, 0], "spawnChance": 1.0 },
        { "referenceName": "Guard_2", "className": "ZmbF_JournalistNormal_White",
          "position": [1325.0, 290.0, 9290.0], "orientation": [90, 0, 0], "spawnChance": 0.5 }
    ],
    "min_ai_to_spawn": -1,
    "max_ai_to_spawn": -1
}
```

**Expansion AI + 装备 + 阵营：**
```json
{
    "aiToSpawnOnOpen": [
        { "referenceName": "Elite_Commander", "className": "eAI_SurvivorM_Mirek|Guards_Tier3|Raiders",
          "position": [1322.0, 290.5, 9287.0], "orientation": [0, 0, 0], "spawnChance": 1.0 },
        { "referenceName": "Silent_Sniper", "className": "eAI_SurvivorF_Eva|Sniper_Loadout|Mercenaries",
          "position": [1330.0, 295.0, 9288.0], "orientation": [45, 0, 0], "spawnChance": 0.3 }
    ],
    "min_ai_to_spawn": 1,
    "max_ai_to_spawn": 2
}
```

**混合 — 僵尸 + Expansion AI + 动物：**
```json
{
    "aiToSpawnOnOpen": [
        { "referenceName": "Zombie_Grunt", "className": "ZmbM_PatrolNormal_Autumn",
          "position": [1318.0, 290.0, 9283.0], "spawnChance": 1.0 },
        { "referenceName": "Expansion_Guard", "className": "eAI_SurvivorM_Mirek|HumanLoadout|Mercenaries",
          "position": [1322.0, 290.0, 9287.0], "spawnChance": 0.5 },
        { "referenceName": "Bear_Surprise", "className": "Animal_UrsusArctos",
          "position": [1326.0, 290.0, 9292.0], "spawnChance": 0.1 }
    ],
    "min_ai_to_spawn": 1,
    "max_ai_to_spawn": 2
}
```

### 6.5 Expansion 阵营说明

常用内置阵营名：`Guards`, `Mercenaries`, `Raiders`, `Police`, `Military`

自定义阵营定义在 `$profile:/ExpansionMod/AI/Factions/`。使用文件夹名作为管道字符串中的 faction 值。

同一门事件生成的所有 AI 被自动放入**同一组**，故无论指定哪个阵营，它们之间都会相互协调。

---

## 7. 载具生成系统 (Vehicle Spawning System)

> 载具与门事件绑定。关门后自动删除。**不要用此系统做永久载具生成** — 使用专门的载具生成模组。

### 7.1 载具条目参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `referenceName` | String | 唯一名称，用于日志 |
| `className` | String | 载具实体 classname（如 `OffroadHatchback`, `ExpansionMh6`） |
| `position` | Array | 世界坐标 `[X, Y, Z]` |
| `orientation` | Array | 旋转 `[Yaw, Pitch, Roll]` |
| `spawnChance` | Float | 加权概率 |
| `fuel` | Float | 燃油量（最大容量的分数）：`0.0`=空, `1.0`=满, `-1`=默认(0) |
| `useDebugAttachments` | Bool | `1` = 调用 `OnDebugSpawn()` 自动附加默认部件。快速设置时使用 |
| `attachments` | Array | 手动附加的零件列表。每项有 `name` (classname) 和 `quantity`。仅在 `useDebugAttachments` 为 `0` 时使用 |

### 7.2 门级别载具参数

| 参数 | 说明 |
|------|------|
| `min_vehicles_to_spawn` | 最少载具数。`-1` = 生成全部 |
| `max_vehicles_to_spawn` | 最多载具数。`-1` = 生成全部 |

### 7.3 示例

**高价值门 + 载具奖励：**
```json
{
    "vehiclesToSpawn": [
        { "referenceName": "Jackpot_Helicopter", "className": "ExpansionMh6",
          "position": [3670.0, 402.5, 5990.0], "spawnChance": 0.15, "fuel": 1.0, "useDebugAttachments": 1 },
        { "referenceName": "Standard_Car", "className": "OffroadHatchback",
          "position": [3672.0, 402.0, 5994.0], "spawnChance": 1.0, "fuel": 0.6, "useDebugAttachments": 0,
          "attachments": [
              { "name": "HatchbackHood_Black", "quantity": 1 },
              { "name": "CarBattery", "quantity": 1 },
              { "name": "SparkPlug", "quantity": 1 }
          ]}
    ],
    "min_vehicles_to_spawn": 1,
    "max_vehicles_to_spawn": 1
}
```

> **提示：** 先使用 `useDebugAttachments: true` 验证载具能正常生成和驾驶，然后切换为手动附件以精确控制零件。

---

## 8. 钥匙与门禁卡配置

**文件位置:** `$profile/BS_KeyRoom/BS_KeyRoom_ItemNames.json`

此文件可以自定义任何钥匙或门禁卡物品的**游戏内显示名称、描述和使用次数** — 无需重打包 PBO。

### 8.1 结构

```json
{
    "KeyCardEntries": [
        {
            "ClassName": "BS_keycard_lab_red",
            "DisplayAndDescription": "Red Laboratory Keycard|Grants access to restricted military zones. Single use.",
            "MaxUses": 1
        }
    ]
}
```

### 8.2 参数参考

| 参数 | 类型 | 说明 |
|------|------|------|
| `ClassName` | String | 物品的精确 classname（区分大小写） |
| `DisplayAndDescription` | String | 显示名称和描述，用管道符 `|` 分隔。格式: `"显示名称|描述文本。"` |
| `MaxUses` | Int | 控制物品可使用次数（见下表） |

### 8.3 MaxUses 详解

| 值 | 行为 | 名称中显示 |
|----|------|-----------|
| `1` | **一次性。** 使用后销毁 | `[1/1]` |
| `> 1` (如 `5`) | **多次使用。** 计数器倒数。最后一次销毁 | `[4/5]` → `[3/5]` → … |
| `-1` | **无限次。** 永不销毁 | `[∞]` |
| `0` | **隐藏一次性。** 使用一次后消耗，但不显示计数器 | *(隐藏)* |

### 8.4 注意事项

- 仅在此文件中列出的物品会被自定义。未列出的使用其 PBO 默认值。
- 编辑后**不需要重启服务器**，使用 `!kcreload` 命令即可。
- `DisplayAndDescription` 使用单个管道符 `|` 分隔。不要在名称或描述文本中使用 `|`。

---

## 9. 主设置文件 (BS_KeyRoom_Settings.json)

**文件位置:** `$profile/BS_KeyRoom/BS_KeyRoom_Settings.json`

### 9.1 全局参数

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `debug_build` | 0/1 | `0` | **关键。** `1` = 启用在游戏内 `BS_DoorLocker` 管理工具。**上线公服必须为 `0`** |
| `admin_log` | 0/1 | `0` | `1` = 写入详细玩家交互日志到 `logs/` 文件夹 |
| `showDoorTimerText` | 0/1 | `1` | `1` = 玩家看着已打开的门时显示关门倒计时 |
| `enableRandomContainerRespawn` | 0/1 | `0` | 遗留/实验功能。保持默认 `0` |
| `maxRandomContainers` | Int | `50` | 遗留/实验功能。保持默认 |

### 9.2 全局战利品池 (`lootPools`)

`lootPools` 数组是一个命名物品列表库，**任何门**都可以按名称引用，避免在几十个门配置中重复相同的物品列表。

| 使用全局池的场景 | 使用门专属池的场景 |
|------------------|--------------------|
| 多个门共享相同的战利品层级 | 单个门有独有奖励 |
| 想在单一位置更新多个门的战利品 | 想一个门的战利品完全隔离 |
| 通用分类（医疗、民用、军用 T1-T4） | 地点专属主题战利品 |

在门配置中引用全局池：
```json
{
    "referenceName": "Weapons_Crate",
    "className": "BS_Box4_Green",
    "lootPoolName": "Global_Military_T3",
    "lootMin": 1,
    "lootMax": 2
}
```

### 9.3 不重启应用更改

编辑后可通过 `!kcreload` 在线重载（需要 Steam64ID 在 `admins.txt` 中）。

### 9.4 游戏内管理菜单编辑全局设置

`K` → 打开 BS KeyRoom 管理面板 → **General** 标签 → "GLOBAL MOD SETTINGS" 区域：

| 菜单复选框 | JSON 字段 |
|-----------|-----------|
| `DebugBuild` | `debug_build` |
| `AdminLog` | `admin_log` |
| `ShowDoorTimer` | `showDoorTimerText` |

修改后点击 **Save** 写回 `BS_KeyRoom_Settings.json`，立即生效无需重启。

---

## 10. 管理员命令与快捷键

| 操作 | 方式 | 说明 |
|------|------|------|
| 打开管理面板 | 按 **`K`** 键 | 打开完整 BS KeyRoom 管理 GUI。仅 `admins.txt` 中的玩家有效 |
| 热重载配置 | 聊天输入 **`!kcreload`** | 从磁盘重载所有门配置和设置，无需重启服务器 |
| 创建门配置 | `BS_DoorLocker` + 瞄准门按住左键 | 需要 `debug_build: 1` |

> ⚠️ **当前项目状态:** `admins.txt` 为空文件。所有管理员功能（K 键面板、`!kcreload`）目前不可用。配置修改后必须手动重启服务器。建议将服务器管理员的 Steam64ID 填入此文件。

---

## 11. 当前项目配置快照

### 11.1 目录状态

| 文件 | 状态 |
|------|------|
| `BS_KeyRoom_Settings.json` | 已配置，2 个全局战利品池 (`Military_Default`, `Medical_Default`)，`debug_build: 0`, `enableRandomContainerRespawn: 1` |
| `BS_KeyRoom_ItemNames.json` | 已配置，62 个钥匙/门禁卡条目（覆盖了所有 BS_Key/BS_bluekey/BS_greenkey/BS_redkey/BS_yellowkey/keycard_lab/BS_New_* 系列） |
| `admins.txt` | **空文件** — 无管理员 Steam64ID |
| `DoorConfigs/GreenMontainRedKeycard.json` | 已配置的示例门（Green Mountain 军营，红卡，3 个容器，3 个门专属战利品池） |
| `logs/` | 空目录 |
| `BS_KeyRoom_Cooldowns.json` | 未生成（服务器首次启动后才会创建） |

### 11.2 现有门配置摘要 — GreenMontainRedKeycard

| 设置 | 值 |
|------|-----|
| 建筑 | `Land_Mil_Barracks5` (Green Mountain) |
| 位置 | [3689.40, 5985.54, 403.75] |
| 门索引 | [0, 1, 2, 3] — 控制四个门 |
| 所需钥匙 | `BS_keycard_lab_red`（红卡，单次使用） |
| 开门时间 | 0 秒（门禁卡使用后立即开门） |
| 房间持续时间 | 70 秒 |
| 公告 | ✅ 启用 ("Red Keycard" / "A red keycard has been activated at Green Mountain.")，橙色 |
| 警报 | ✅ 启用 (`Alarm_Military`, 45 秒) |
| 安全传送 | ✅ 半径 30m |
| 玩家附近延迟关门 | ✅ 启用 |
| 容器数 | 2-3 (加权随机) / 3 个容器全部 spawnChance 1.0 |
| AI 防守者 | ❌ 无 |
| 载具 | ❌ 无 |
| 可破解箱子 | ❌ 未启用 |

**3 个容器：**
1. **BOX1** (`BS_Box1_Black`): 固定物品（9件）+ 随机池 `Vest`（1-1 件）
2. **Guncase1** (`BS_Guncase`): 随机池 `Weapons1`（2-2 件，无重复）
3. **Box2** (`BS_Box4_Green`): 固定物品（4件含 FAL+附件+毒气手雷+培根）+ 随机池 `Explosives`（2-2 件，无重复）

**3 个门专属战利品池：**
- `Weapons1`: SVD_Wooden(0.5权重) + M4A1(0.5权重)，各带附件
- `Vest`: 5种 PlateCarrier 变体 (各 0.2 权重) + PressVest + PoliceVest
- `Explosives`: Plastic_Explosive(0.5) + ImprovisedExplosive(0.25) + ClaymoreMine(0.25)

**2 个全局战利品池：**
- `Military_Default`: AKM(1.0权重, 带弹匣) + PlateCarrierVest(0.5)
- `Medical_Default`: BandageDressing(1.0权重, 5-10个) + Morphine(0.8, 2-4个)

### 11.3 既有问题与待改进项

1. **`admins.txt` 为空** — 没有管理员可以使用 `!kcreload` 或 K 键面板。必须填入 Steam64ID。
2. **`persistCooldownOnRestart` 为 `0`** — GreenMountain 门的冷却状态在服务器重启后丢失。文档强烈建议设为 `1`。
3. **`enableRandomContainerRespawn` 为 `1`** — 文档标注为遗留/实验功能，建议保持 `0`。
4. **现有门配置路径引用 `BS_KeyRoom/`** — 需确认服务器 `$profile` 路径是否对应该目录。

---

## 12. 常见陷阱与最佳实践

### 12.1 JSON 陷阱

1. **坐标字段不要手动编辑** — `x/y/z`, `building_x/y/z`, `door_indices` 必须由 `BS_DoorLocker` 生成
2. **`Location_Name` 必须全局唯一** — 重复会导致冷却追踪冲突
3. **容器的 `position` / `orientation`** 需要单独获取（DayZ Editor 或 VPP Admin Tools 的 `getpos`）
4. **`DisplayAndDescription` 中的管道符** — 使用单个 `|` 分隔，但不能在名称或描述文本中再使用 `|`
5. **Expansion AI className 三部分** — 全部写在同一行的 `"className": "Class|Loadout|Faction"` 中

### 12.2 运行时陷阱

1. **`debug_build: 1`** 上线服务器是安全风险 — 玩家可能滥用 `BS_DoorLocker`
2. **`!kcreload`** 只在 Steam64ID 在 `admins.txt` 中时可用
3. **载具与门事件绑定** — 门关闭时载具自动删除，不要用于永久载具
4. **AI 不会重生** — 被击杀后只在下一次门解锁时才重新生成
5. **Expansion AI 需要加载 DayZ-Expansion-AI 模组**

### 12.3 编辑最佳实践

1. **先离线编辑，再部署** — 在本地用 JSON 验证器检查，然后上传
2. **善用全局战利品池** — 共享的层级（Military T1-T4、Medical、Civilian）放在 `BS_KeyRoom_Settings.json` 中统一管理
3. **门专属池仅用于独有奖励** — 特定位置才出的稀有物品放门专属池
4. **使用管理面板实时测试** — K 键 GUI 可以不重启调整全局设置
5. **编辑后运行 `!kcreload`** — 避免频繁重启服务器
6. **为 `persistCooldownOnRestart` 保持 `1`** — 防止重启后门状态混乱

---

## 附录: Wiki 页面索引

以下 8 个页面已全部抓取并整合到本文档中：

| 编号 | 页面 | 内容 |
|------|------|------|
| 0 | Installation | 安装步骤、可选依赖、故障排除 |
| 1 | Initial Setup | 文件结构、admins.txt/K键/!kcreload管理命令 |
| 2 | Door Configuration | 门 JSON 完整参数参考、最小示例 |
| 3 | Advanced Loot System | 战利品池、附件系统、四种战利品方法、替换容器 |
| 4 | AI Spawning System | 原版僵尸/Expansion AI/动物/阵营配置 |
| 5 | Vehicle Spawning System | 载具生成、附件、燃油、坐标获取 |
| 6 | Keys and Keycards Configuration | ItemNames.json 结构、MaxUses 机制 |
| 7 | Main Settings (BS_KeyRoom_Settings.json) | 全局参数、全局战利品池、管理菜单操作 |

---

> **本文档是 BS KeyRoom 模组的权威参考。任何编辑 `profiles/BS_KeyRoom/` 下文件的操作，必须先 review 本文档。**
