# InediaInfectedAI 配置文件完全参考手册

> **来源:** [InediaInfectedAI Wiki](https://github.com/ysaroka/InediaInfectedAI/wiki) — Description + Configuration Guide + FAQ + Pain System Guide + Medicine Guide
> **抓取日期:** 2026-07-08
> **配置文件位置:** `%DayZserverDir%/profiles/Inedia/InediaInfectedAIConfig.json`
> **管理员配置:** `%DayZserverDir%/profiles/Inedia/InediaAdminsConfig.json`

---

## 目录

- [1. 配置系统基础规则](#1-配置系统基础规则)
- [2. 快速入门检查清单](#2-快速入门检查清单)
- [3. Zombies 参数](#3-zombies-参数)
  - [3.1 Groups（组）](#31-zombiesgroups)
  - [3.2 CustomIrritants（自定义刺激物）](#32-zombiescustomirritants)
  - [3.3 ThrowingProjectiles（投掷物定义）](#33-zombiesthrowingprojectiles)
  - [3.4 BreakingDoors（破门）](#34-zombiesbreakingdoors)
  - [3.5 AttackPlayers（攻击玩家）](#35-zombiesattackplayers)
  - [3.6 AttackAnimals（攻击动物）](#36-zombiesattackanimals)
  - [3.7 FriendlyNPC（友好NPC）](#37-zombiesfriendlynpc)
  - [3.8 Search（搜索模式）](#38-zombiessearch)
  - [3.9 Speed（速度）](#39-zombiesspeed)
  - [3.10 Smells（气味）](#310-zombiessmells)
  - [3.11 UpJump / DownJump / StuckJump（跳跃）](#311-zombiesupjump--downjump--stuckjump)
  - [3.12 FallHandler（坠落伤害）](#312-zombiesfallhandler)
  - [3.13 InjuryHandler（受伤系统）](#313-zombiesinjuryhandler)
  - [3.14 AttackCar（攻击车辆）](#314-zombiesattackcar)
  - [3.15 React（反应系统）](#315-zombiesreact)
  - [3.16 DamageToPlayer（对玩家伤害）](#316-zombiesdamagetoplayer)
  - [3.17 DamageToZombie（对僵尸伤害）](#317-zombiesdamagetozombie)
  - [3.18 MeleeAttacksDodge（近战闪避）](#318-zombiesmeleeattacksdodge)
  - [3.19 JumpAttack（跳跃攻击）](#319-zombiesjumpattack)
  - [3.20 Blood（血液系统）](#320-zombiesblood)
  - [3.21 ResistContaminatedEffect（抗毒区）](#321-zombiesresistcontaminatedeffect)
  - [3.22 AllowCrawling / RespawnInCrawling（爬行）](#322-zombiesallowcrawling--respawnincrawling)
  - [3.23 Scream（尖叫）](#323-zombiesscream)
  - [3.24 SearchBody（搜索尸体）](#324-zombiessearchbody)
  - [3.25 Butchering（屠宰）](#325-zombiesbutchering)
  - [3.26 CanBeBackstabbed（背刺）](#326-zombiescanbebackstabbed)
  - [3.27 VisionRangeMultiplier（视野倍率）](#327-zombiesvisionrangemultiplier)
  - [3.28 Size（体型）](#328-zombiessize)
  - [3.29 ThrowingProjectilesHandler（投掷物绑定）](#329-zombiesthrowingprojectileshandler)
  - [3.30 RangeAttacksHandler（远程攻击）](#330-zombiesrangeattackshandler)
  - [3.31 DiseasesToPlayer（疾病传播）](#331-zombiesdiseasestoplayer)
  - [3.32 CameraShakeToPlayer（镜头震动）](#332-zombiescamerashaketoplayer)
  - [3.33 PainToPlayer（疼痛系统-僵尸侧）](#333-zombiespaintoplayer)
  - [3.34 StunToPlayer（眩晕）](#334-zombiesstuntoplayer)
  - [3.35 DisarmToPlayer（缴械）](#335-zombiesdisarmtoplayer)
  - [3.36 FastAttackToPlayerChancePercent（快速攻击）](#336-zombiesfastattacktoplayerchancepercent)
  - [3.37 LongVision（长视野）](#337-zombieslongvision)
  - [3.38 ReturnToSpawn（返回出生点）](#338-zombiesreturntospawn)
- [4. Players 参数](#4-players-参数)
- [5. Vehicles 参数](#5-vehicles-参数)
- [6. 全局参数](#6-全局参数)
- [7. Inedia 疼痛系统详解](#7-inedia-疼痛系统详解)
  - [7.1 系统概述](#71-系统概述)
  - [7.2 疼痛等级与减益表](#72-疼痛等级与减益表)
  - [7.3 骨折系统](#73-骨折系统)
  - [7.4 深度伤口系统](#74-深度伤口系统)
  - [7.5 子弹伤系统](#75-子弹伤系统)
  - [7.6 内出血系统](#76-内出血系统)
  - [7.7 护甲与疼痛防护](#77-护甲与疼痛防护)
- [8. Inedia 医疗系统详解](#8-inedia-医疗系统详解)
  - [8.1 模组新增药物](#81-模组新增药物)
  - [8.2 原版物品的疼痛/医疗属性](#82-原版物品的疼痛医疗属性)
  - [8.3 自定义药物属性](#83-自定义药物属性)
  - [8.4 自定义医疗工具属性](#84-自定义医疗工具属性)
  - [8.5 脚本 API 方法](#85-脚本-api-方法)
- [9. 核心机制深度解析](#9-核心机制深度解析)
  - [9.1 血液与流血系统](#91-血液与流血系统)
  - [9.2 气味系统](#92-气味系统)
  - [9.3 Inedia 长视野](#93-inedia-长视野)
  - [9.4 感染者受伤与减益系统](#94-感染者受伤与减益系统)
  - [9.5 车辆攻击逻辑](#95-车辆攻击逻辑)
  - [9.6 投掷物系统配置指南](#96-投掷物系统配置指南)
  - [9.7 格挡穿透机制](#97-格挡穿透机制)
  - [9.8 天气对机制的影响](#98-天气对机制的影响)
  - [9.9 原版刺激物与 Inedia 刺激物的关系](#99-原版刺激物与-inedia-刺激物的关系)
  - [9.10 消音器机制](#910-消音器机制)
  - [9.11 水中感染者的处理](#911-水中感染者的处理)
- [10. 常见问题排查](#10-常见问题排查)
- [11. 管理员命令快速参考](#11-管理员命令快速参考)
- [12. 模组兼容性](#12-模组兼容性)

---

## 1. 配置系统基础规则

### 参数作用域

- **ANY** `Zombies.*` 参数（除了 `Zombies.Groups`、`Zombies.CustomIrritants`、`Zombies.ThrowingProjectiles` 这三个配置列表）都可以按**具体类名**、**基类名**、**组名**或 `all` 来设置。
- 部分参数（参数说明中会标注）也可以为**动物**或**幸存者**配置。为幸存者配置时使用特殊类名 `"SurvivorBase"`。
- 如果参数说明中没有指定适用于哪些生物，则该参数**仅对感染者生效**，不适用于幸存者或动物。
- 僵尸类名**不区分大小写**。

### 优先级规则（从高到低）

1. **具体类名** (exact class) — 最高优先级
2. **基类名** (base class) — 如 `ZmbM_SoldierNormal_Base`
3. **组名** (group) — 按字母顺序检查（或按 `!`/`~` 优先级符号）
4. **`all`** — 最低优先级，始终存在（即使从配置中删除也会使用硬编码默认值）

### 组优先级控制

在 `Zombies.Groups` 的组名中使用特殊符号调整优先级：
- `!` 前缀 — **最高优先级**（最先匹配）
- `~` 前缀 — **最低优先级**（最后匹配），多个 `~` 叠加表示更低优先级（如 `~~Group1` 比 `~Group2` 优先级更低）
- 无特殊符号 — 按 ASCII 字母顺序处理（大写字母优先于小写字母）

### 配置文件更新

- 模组更新后**无需更新配置文件**。缺失的参数会使用默认值。
- `SaveConfigAfterInit` 参数设为 `1` 可自动将缺失参数写入配置文件。
- 使用 `/ireload` 命令可在游戏中重载配置而无需重启服务器。

---

## 2. 快速入门检查清单

**新装模组时必须做的事：**

1. **添加管理员 SteamID** 到 `InediaAdminsConfig.json`（字符串格式）。这是**最关键的一步**——管理员登录时会收到配置错误通知，可消除 99% 的配置排错问题。
2. 验证配置文件 JSON 格式：[jsonlint.com](https://jsonlint.com)
3. 检查服务器崩溃日志：`%DayZserverDir%/profiles/crash_*.log`（JSON 验证器无法检测参数类型不匹配）
4. 如需恢复某个默认值，查看[默认配置文件](https://github.com/ysaroka/InediaInfectedAI/wiki/Default-configuration-file)

**⚠️ 搜索模式 (`SearchHandlerIsActive`) 是核心：** 许多功能（破门、光/声反应、气味、尖叫、长视野）都依赖搜索模式。不要禁用此参数。

---

## 3. Zombies 参数

### 3.1 Zombies.Groups

**类型:** 全局列表（不对应单个生物）

定义可在其他配置参数中引用的僵尸/动物分组。支持嵌套。

**默认分组:**

| 组名 | 类型 | 说明 |
|------|------|------|
| `city` | 感染者 | 城市僵尸 |
| `villagers` | 感染者 | 村民僵尸 |
| `industrial` | 感染者 | 工业区僵尸 |
| `military` | 感染者 | 军事僵尸 |
| `police` | 感染者 | 警察僵尸 |
| `prisoners` | 感染者 | 囚犯僵尸 |
| `firefighters` | 感染者 | 消防员僵尸 |
| `medics` | 感染者 | 医疗僵尸 |
| `hunters` | 感染者 | 猎人僵尸 |
| `fishermen` | 感染者 | 渔民僵尸 |
| `priests` | 感染者 | 牧师僵尸 |
| `lowstr` | 特殊 | 低力量快速配置 |
| `lowdef` | 特殊 | 低防御快速配置 |
| `mediumstr` | 特殊 | 中力量快速配置 |
| `mediumdef` | 特殊 | 中防御快速配置 |
| `highstr` | 特殊 | 高力量快速配置 |
| `highdef` | 特殊 | 高防御快速配置 |
| `bears` | 动物 | 熊 |
| `wolves` | 动物 | 狼 |

**重要说明:**
- 组支持嵌套（最大深度 10 层）
- 组内类名不区分大小写，支持基类
- 建议为覆盖面大的组（如层级组）从一开始就设置低优先级（`~~`），避免与小型选择性组冲突

---

### 3.2 Zombies.CustomIrritants

**类型:** 全局列表

定义自定义刺激物（来自其他模组的可开关物品）。必要条件：物品必须是 `ItemBase` 的后代，且通过 `ComponentEnergyManager` 运作。

**JSON 结构:**
```json
"Zombies": {
    "CustomIrritants": {
        "irritant_name": {
            "Classes": ["Class1", "Class2"],
            "RadiusOutdoorDay": 0.0,
            "RadiusOutdoorNight": 25.0,
            "RadiusIndoorDay": 0.0,
            "RadiusIndoorNight": 5.0,
            "Type": 0,
            "Priority": 1
        }
    }
}
```

| 字段 | 说明 |
|------|------|
| `Classes` | 关联的物品类名列表，支持基类，不区分大小写 |
| `RadiusOutdoorDay` | 白天室外刺激半径 |
| `RadiusOutdoorNight` | 夜晚室外刺激半径 |
| `RadiusIndoorDay` | 白天室内刺激半径 |
| `RadiusIndoorNight` | 夜晚室内刺激半径 |
| `Type` | `0` = 视觉刺激物, `1` = 噪音刺激物 |
| `Priority` | 整数，优先级。数值越高，僵尸越优先响应 |

**原版刺激物默认优先级参考:**
- 777: 枪声、爆炸物、烟花、加油站爆炸、玩家脚步/语音/坠落、僵尸尖叫
- 4: 篝火、聚光灯、车灯、车喇叭、引擎声、发电机、门声
- 3: 路焰、火炬、便携燃气灯、烟雾弹
- 2: 手电筒、厨房计时器、闹钟
- 1: 化学灯、尸体倒地声

---

### 3.3 Zombies.ThrowingProjectiles

**类型:** 全局列表

定义投掷物及其参数，可绑定到特定类型感染者。

**JSON 结构:**
```json
"ThrowingProjectiles": {
    "ProjectileName": {
        "ItemClasses": ["Item1", "Item2"],
        "Parameters": {
            "HavingProjectileChancePercent": 100,
            "InitialSpeed": 20,
            "AccuracySpread": 0.05,
            "TargetHealthDamage": -1,
            "TargetShockDamage": -1,
            "TargetStaminaDamage": -1,
            "TargetBloodDamage": 0,
            "TargetBleedingChancePercent": -1,
            "TargetStunChancePercent": -1,
            "TargetPainMultiplier": 1,
            "TargetBreakChanceMultiplier": 1,
            "TargetDeepWoundChanceMultiplier": 0.5,
            "TargetArmsPainDisarmMultiplier": 0.3,
            "ThrowConditionAmountOfProjectiles": 1,
            "ThrowConditionThrowChancePercent": 100,
            "ThrowConditionCooldownSeconds": 5,
            "ThrowConditionZombieTargetDistanceMax": 50,
            "ThrowConditionZombieTargetDistanceMin": 0,
            "ThrowConditionZombieTargetVerticalDistanceMax": 25,
            "ThrowConditionZombieTargetVerticalDistanceMin": -25,
            "ThrowConditionZombieTargetHorizontalDistanceMax": 25,
            "ThrowConditionZombieTargetHorizontalDistanceMin": 0,
            "ThrowConditionGroundTargetDistanceMax": 100,
            "ThrowConditionGroundTargetDistanceMin": 0,
            "ThrowConditionTargetInWater": 0,
            "DestroyProjectileAfterSeconds": 10,
            "DeleteProjectileAfterSeconds": 60,
            "ActivateGrenadeAfterSeconds": 0,
            "EnableSpawner": 1
        }
    }
}
```

**投掷物参数说明:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `HavingProjectileChancePercent` | 100 | 感染者生成时拥有此投掷物的概率(%) |
| `InitialSpeed` | 20 | 初速度(m/s)，决定投掷距离。不能超过50 |
| `AccuracySpread` | 0.05 | 精准度扩散(0~1)，实际偏移 = 距离 × 此值 |
| `TargetHealthDamage` | -1 | 健康伤害(0~100)。-1=根据武器重量自动计算 |
| `TargetShockDamage` | -1 | 冲击伤害(0~100)。-1=根据武器重量自动计算 |
| `TargetStaminaDamage` | -1 | 体力伤害(%)。-1=自动计算 |
| `TargetBloodDamage` | 0 | 失血伤害(%)。100% = 从满血到濒危 |
| `TargetBleedingChancePercent` | -1 | 造成流血概率(%)。-1=根据武器类型自动决定 |
| `TargetStunChancePercent` | -1 | 造成眩晕概率(%)。-1=自动计算 |
| `TargetPainMultiplier` | 1 | 疼痛倍率（Inedia疼痛系统）。0=禁用疼痛 |
| `TargetBreakChanceMultiplier` | 1 | 骨折概率倍率。0=禁用 |
| `TargetDeepWoundChanceMultiplier` | 0.5 | 深度伤口概率倍率 |
| `TargetArmsPainDisarmMultiplier` | 0.3 | 缴械概率倍率 |
| `ThrowConditionAmountOfProjectiles` | 1 | 每次投掷的数量 |
| `ThrowConditionThrowChancePercent` | 100 | 投掷概率(%) |
| `ThrowConditionCooldownSeconds` | 5 | 投掷冷却时间(秒) |
| `ThrowConditionZombieTargetDistanceMax` | 50 | 投掷最大水平距离 |
| `ThrowConditionZombieTargetDistanceMin` | 0 | 投掷最小水平距离 |
| `ThrowConditionZombieTargetVerticalDistanceMax` | 25 | 最大垂直距离 |
| `ThrowConditionZombieTargetVerticalDistanceMin` | -25 | 最小垂直距离（从高向低投需为负值） |
| `ThrowConditionZombieTargetHorizontalDistanceMax` | 25 | 最大水平距离 |
| `ThrowConditionZombieTargetHorizontalDistanceMin` | 0 | 最小水平距离 |
| `ThrowConditionGroundTargetDistanceMax` | 100 | 目标离地最大距离 |
| `ThrowConditionGroundTargetDistanceMin` | 0 | 目标离地最小距离（>0 = 仅当玩家在障碍物上时投掷） |
| `ThrowConditionTargetInWater` | 0 | 目标在水中时投掷(1=启用) |
| `DestroyProjectileAfterSeconds` | 10 | 投出后摧毁的时间(秒)。-1=不摧毁 |
| `DeleteProjectileAfterSeconds` | 60 | 投出后删除的时间(秒) |
| `ActivateGrenadeAfterSeconds` | 0 | 手榴弹激活延迟(秒) |
| `EnableSpawner` | 1 | 启用在世界中生成此投掷物供感染者拾取 |

---

### 3.4 Zombies.BreakingDoors*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `BreakingDoorsHandlerIsActive` | 0/1 | 1 | 破门系统总开关 |
| `BreakingDoorsRestrictedDoors` | object | 见配置 | 禁止被破坏的门列表（如钥匙卡门、保险库门等）。支持：DNA Keycards, Custom Keycards, KeyCard-Rooms, Banov, DeerIsle, Sakhal |
| `BreakingDoorsDestroyAfterOpenChancePercent` | 0~100 | all:30 | 门被打开后被摧毁的概率(%) |
| `BreakingDoorsOpenChancePercent` | 0~100 | all:30 | 单次攻击打开门的概率(%) |
| `BreakingDoorsOpenLockPickChancePercent` | 0~100 | all:5 | 撬锁打开门的概率(%) |
| `BreakingDoorsLossInterestAfterHitChancePercent` | 0~100 | all:5 | 攻击门后失去兴趣的概率(%) |
| `BreakingDoorsLossInterestAfterHitLockPickChancePercent` | 0~100 | all:25 | 攻击被撬锁的门后失去兴趣的概率(%) |
| `BreakingDoorsCrawlersChanceMultiplier` | 0~∞ | all:0 | 爬行僵尸破门概率倍率。0=爬行僵尸不能破门 |

---

### 3.5 Zombies.AttackPlayers*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `AttackPlayersUnconsciousHandlerIsActive` | 0/1 | 0 | 攻击昏迷玩家系统开关 |
| `AttackPlayersUnconsciousHitsLimit` | >=0 | all:5 | 玩家昏迷时感染者的攻击次数上限。目的：防止玩家利用昏迷无敌躲避威胁 |

---

### 3.6 Zombies.AttackAnimals*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `AttackAnimalsHandlerIsActive` | 0/1 | 1 | 攻击动物系统总开关 |
| `AttackAnimalsWildBoar` | 0/1 | 1 | 攻击野猪 |
| `AttackAnimalsPig` | 0/1 | 1 | 攻击猪 |
| `AttackAnimalsSheep` | 0/1 | 1 | 攻击羊 |
| `AttackAnimalsDeer` | 0/1 | 1 | 攻击鹿 |
| `AttackAnimalsRoeDeer` | 0/1 | 1 | 攻击狍子 |
| `AttackAnimalsGoat` | 0/1 | 1 | 攻击山羊 |
| `AttackAnimalsCow` | 0/1 | 1 | 攻击牛 |
| `AttackAnimalsCustom` | object | all:0 | 自定义动物敌对关系配置（用于模组动物） |

---

### 3.7 Zombies.FriendlyNPC

定义对感染者友好的NPC列表（感染者不会攻击的NPC类型）。

⚠️ 注意：此参数只让感染者对NPC友好，NPC可能仍会攻击感染者。需要在对应NPC模组中将NPC配置为对感染者友好（如 Expansion-AI 中将 bot 加入 "Shamans" 派系）。

**可对动物配置**——使动物对指定NPC友好。

---

### 3.8 Zombies.Search*

搜索模式是 InediaInfectedAI 的核心，许多功能（破门、光/声反应、气味、尖叫、长视野）都依赖它。**不要禁用 `SearchHandlerIsActive`。**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `SearchHandlerIsActive` | 0/1 | 1 | 搜索模式总开关。⭐核心参数 |
| `SearchSphereRadiusIncreaseEverySeconds` | float | 0.2 | 搜索球半径每秒增长速度 |
| `SearchSphereDistanceToRadiusMultiplier` | float | 0.3 | 距离到搜索球半径的倍率 |
| `SearchSphereRadiusMin` | float | 0 | 搜索球最小半径 |
| `SearchSphereRadiusMax` | float | 50 | 搜索球最大半径 |
| `SearchSphereRadiusBurst` | float | 60 | 突发搜索球半径（被刺激时） |

---

### 3.9 Zombies.Speed*

控制感染者在不同模式下的移动速度。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `SpeedHandlerIsActive` | 0/1 | 1 | 速度系统开关 |
| `SpeedMinimumInCalmMode` | float | 0 | 平静模式最低速度 |
| `SpeedLimitInCalmMode` | float | 3 | 平静模式速度上限 (0~3) |
| `SpeedMultiplierInCalmMode` | float | 1 | 平静模式速度倍率 |
| `SpeedMinimumInSearchMode` | float | 0 | 搜索模式最低速度 |
| `SpeedLimitInSearchMode` | float | 3 | 搜索模式速度上限 |
| `SpeedMultiplierInSearchMode` | float | 1 | 搜索模式速度倍率 |
| `SpeedMinimumInChaseMode` | float | 0 | 追击模式最低速度 |
| `SpeedLimitInChaseMode` | float | 3 | 追击模式速度上限 (0~3) |
| `SpeedMultiplierInChaseMode` | float | 1 | 追击模式速度倍率 |
| `SpeedNoLimitsFromDistanceMeters` | float | 0 | 超过此距离后无视速度限制 |

**速度值参考:** `1` = 步行, `2.1` = 慢跑, `3` = 冲刺。原版感染者不支持高于3的速度。

**速度降幅不生效的前提条件：**
- `DamageToPlayerHandlerIsActive` 被禁用时，伤害降幅不工作
- `SpeedHandlerIsActive` 被禁用时，速度降幅不工作

---

### 3.10 Zombies.Smells*

感染者气味追踪机制。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `SmellsHandlerIsActive` | 0/1 | 1 | 气味系统开关（僵尸侧） |
| `SmellsSphereRadius` | float | 2 | 气味感知球半径（可通过天气缩小：雨/雾） |
| `SmellsAllowStealthKills` | 0/1 | 1 | 允许在气味感知范围内潜行击杀 |
| `SmellsLossInterestAfterReactionForSeconds` | float | 0 | 对气味失去兴趣的时间(秒)。0=永不失去兴趣 |

详见 [9.2 气味系统详解](#92-气味系统)。

---

### 3.11 Zombies.UpJump / DownJump / StuckJump*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `UpJumpHandlerIsActive` | 0/1 | 0 | 向上跳跃系统开关 |
| `UpJumpHeightMax` | float | 1.8 | 最大向上跳跃高度(米) |
| `UpJumpImpulseDamageChancePercent` | 0~100 | 50 | 跳跃时造成冲击伤害的概率(%) |
| `UpJumpChancePercent` | 0~100 | 100 | 跳跃概率(%) |
| `UpJumpCooldownSeconds` | float | 0 | 跳跃冷却时间(秒) |
| `DownJumpHandlerIsActive` | 0/1 | 0 | 向下跳跃系统开关 |
| `DownJumpHeightMax` | float | 30 | 最大向下跳跃高度(米) |
| `StuckJumpHandlerIsActive` | 0/1 | 0 | 卡住跳跃开关。⚠️强烈建议开启——允许感染者跳出卡住位置并到达原版导航网格无法覆盖的区域 |

**⚠️ 重要说明：** 以上跳跃机制仅适用于 Inedia 新增的跳跃行为，不影响原版感染者翻越/攀爬行为（原版行为无法通过这些设置配置或禁用）。

---

### 3.12 Zombies.FallHandler*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `FallHandlerIsActive` | 0/1 | 0 | 坠落伤害系统开关 |
| `FallHandlerLegBreakHeightMin` | float | 3 | 腿部骨折最小高度(米) |
| `FallHandlerLegBreakHeightMax` | float | 15 | 腿部骨折最大高度(米) |
| `FallHandlerDeathHeightMin` | float | 10 | 坠落致死最小高度(米) |
| `FallHandlerDeathHeightMax` | float | 20 | 坠落致死最大高度(米) |

---

### 3.13 Zombies.InjuryHandler*

感染者/动物受伤后获得减益的系统。**适用于感染者和动物。**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `InjuryHandlerIsActive` | 0/1 | 1(对非boss) | 受伤系统总开关 |
| `InjuryHandlerInjuryOnExplosiveDamageChancePercent` | 0~100 | 100 | 爆炸伤害导致受伤的概率(%) |
| `InjuryHandlerDamageThresholdToInjuryArm` | float | 30 | 手臂受伤所需累积伤害阈值 |
| `InjuryHandlerRestoreInjuredArmAfterSeconds` | float | 0 | 手臂恢复时间(秒)。0=永不恢复 |
| `InjuryHandlerInjuredOneArmAttackMultiplier` | 0~∞ | 0.5 | 单手受伤攻击倍率 |
| `InjuryHandlerInjuredBothArmsAttackMultiplier` | 0~∞ | 0.2 | 双手受伤攻击倍率 |
| `InjuryHandlerInjuredOneArmBreakingDoorChanceMultiplier` | 0~∞ | 0.5 | 单手受伤破门概率倍率 |
| `InjuryHandlerInjuredBothArmsBreakingDoorChanceMultiplier` | 0~∞ | 0 | 双手受伤破门概率倍率 |
| `InjuryHandlerInjuredOneArmStunChanceMultiplier` | 0~∞ | 0.5 | 单手受伤眩晕概率倍率 |
| `InjuryHandlerInjuredBothArmsStunChanceMultiplier` | 0~∞ | 0 | 双手受伤眩晕概率倍率 |
| `InjuryHandlerInjuredOneArmPainMultiplier` | 0~∞ | 0.5 | 单手受伤造成疼痛倍率 |
| `InjuryHandlerInjuredBothArmsPainMultiplier` | 0~∞ | 0 | 双手受伤造成疼痛倍率 |
| `InjuryHandlerInjuredOneArmBleedingChanceMultiplier` | 0~∞ | 0.5 | 单手受伤造成流血概率倍率 |
| `InjuryHandlerInjuredBothArmsBleedingChanceMultiplier` | 0~∞ | 0 | 双手受伤造成流血概率倍率 |
| `InjuryHandlerDamageThresholdToInjuryLeg` | float | 30 | 腿部受伤所需累积伤害阈值（动物可用） |
| `InjuryHandlerRestoreInjuredLegAfterSeconds` | float | 0(AnimalBase:900) | 腿部恢复时间(秒)。0=永不恢复（动物可用） |
| `InjuryHandlerInjuredOneLegSpeedLimit` | 0~3 | 2.1 | 单腿受伤速度上限 |
| `InjuryHandlerInjuredBothLegsSpeedLimit` | 0~3 | 1 | 双腿受伤速度上限 |
| `InjuryHandlerInjuredOneLegJumpHeightMultiplier` | 0~∞ | 0.5 | 单腿受伤跳跃高度倍率 |
| `InjuryHandlerInjuredBothLegsJumpHeightMultiplier` | 0~∞ | 0 | 双腿受伤跳跃高度倍率 |
| `InjuryHandlerSpawnWithInjuredOneArmChancePercent` | 0~100 | 0 | 生成时单臂受伤概率(%) |
| `InjuryHandlerSpawnWithInjuredBothArmsChancePercent` | 0~100 | 0 | 生成时双臂受伤概率(%) |
| `InjuryHandlerSpawnWithInjuredOneLegChancePercent` | 0~100 | 0 | 生成时单腿受伤概率(%) |
| `InjuryHandlerSpawnWithInjuredBothLegsChancePercent` | 0~100 | 0 | 生成时双腿受伤概率(%) |

详见 [9.4 感染者受伤与减益系统详解](#94-感染者受伤与减益系统)。

---

### 3.14 Zombies.AttackCar*

控制感染者/动物攻击车辆的各方面。**所有 AttackCar 参数可对动物配置（`bears`、`wolves`）。**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `AttackCarHandlerIsActive` | 0/1 | 1 | 攻击车辆系统总开关。禁用后所有 AttackCar 功能失效 |
| `AttackCarPlayersIsActive` | 0/1 | 1 | 是否攻击车内玩家（动物可用） |
| `AttackCarPlayersDistanceMeters` | float | 2 | 攻击玩家距离(米)。需突破车窗 |
| `AttackCarElementsIsActive` | 0/1 | 1(wolves:0) | 是否攻击车辆部件（动物可用） |
| `AttackCarElementsDistanceMeters` | float | 2 | 攻击车辆部件距离(米) |
| `AttackCarElementsGlobalDamageMultiplier` | 0~∞ | 1(bears:3) | 攻击车辆部件的全局伤害倍率 |
| `AttackCarElementsByCollisionsIsActive` | 0/1 | 1 | 碰撞伤害开关（动物可用） |
| `AttackCarElementsByCollisionsGlobalDamageMultiplier` | 0~∞ | 1 | 碰撞伤害全局倍率（动物/玩家可用） |
| `AttackCarElementsMultiplierByCarClassId` | object | all:1 | 按车辆类ID设置伤害倍率。可对特定车辆类降低伤害（如坦克设0） |
| `AttackCarWindowDamagePercent` | 0~100 | 25 | 单次攻击对车窗伤害(%) |
| `AttackCarDoorDamagePercent` | 0~100 | 20 | 单次攻击对车门伤害(%) |
| `AttackCarDoorChancePercent` | 0~100 | 60 | 攻击玩家时伤害车门的概率(%) |
| `AttackCarRadiatorDamagePercent` | 0~100 | 10 | 单次攻击对散热器伤害(%) |
| `AttackCarCarBatteryDamagePercent` | 0~100 | 10 | 单次攻击对电池伤害(%) |
| `AttackCarPlugDamagePercent` | 0~100 | 25 | 单次攻击对火花塞伤害(%) |
| `AttackCarEngineDamagePercent` | 0~100 | 10 | 单次攻击对引擎伤害(%) |
| `AttackCarLightsDamagePercent` | 0~100 | 50 | 单次攻击对车灯伤害(%) |
| `AttackCarFenderDamagePercent` | 0~100 | 10 | 单次攻击对挡泥板伤害(%) |
| `AttackCarBumperDamagePercent` | 0~100 | 10 | 单次攻击对保险杠伤害(%) |
| `AttackCarHoodDamagePercent` | 0~100 | 10 | 单次攻击对引擎盖伤害(%) |
| `AttackCarFuelTankDamagePercent` | 0~100 | 5 | 单次攻击对油箱伤害(%) |

**伤害计算公式:**
- 攻击伤害: `AttackCar#ELEMENT#DamagePercent × AttackCarElementsGlobalDamageMultiplier × AttackCarElementsMultiplierByCarClassId`
- 碰撞伤害: `AttackCar#ELEMENT#DamagePercent × 0.05 × ZombieDamageReceivedInHP × AttackCarElementsByCollisionsGlobalDamageMultiplier × AttackCarElementsMultiplierByCarClassId`

详见 [9.5 车辆攻击逻辑详解](#95-车辆攻击逻辑)。

---

### 3.15 Zombies.React*

控制感染者对各种刺激物的反应和摧毁行为。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ReactHandlerIsActive` | 0/1 | 1 | 反应系统总开关。⚠️禁用会影响脚步声/枪声反应 |
| `ReactBehindVisualMultiplier` | 0~1 | 0.2 | 刺激物在背后的视觉倍率 |
| `ReactBehindNoiseMultiplier` | 0~1 | 0.6 | 刺激物在背后的噪音倍率 |

**视觉刺激物反应:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ReactFireplaceVisual` | 1 | 夜间对篝火的反应 |
| `ReactFireplaceDayVisual` | 1 | 白天对篝火(烟/噼啪声)的反应 |
| `ReactFlashlightsVisual` | 1 | 夜间对手电筒/头灯/武器手电的反应 |
| `ReactHeadtorchRedVisual` | 1 | 对红色头灯的反应 |
| `ReactRoadflareVisual` | 1 | 对路焰的反应 |
| `ReactChemlightVisual` | 1 | 对化学灯的反应 |
| `ReactChemlightRedVisual` | 1 | 对红色化学灯的反应 |
| `ReactPortableGasLampVisual` | 1 | 对便携燃气灯的反应 |
| `ReactFlammablesVisual` | 1 | 对可燃物的反应 |
| `ReactSpotlightVisual` | 1 | 对聚光灯的反应 |
| `ReactCarLightVisual` | 1 | 对车灯的反应 |
| `ReactSmokeGrenadeVisual` | 1 | 对烟雾弹的反应 |

**噪音刺激物反应:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ReactRoadflareNoise` | 1 | 对路焰噪音的反应 |
| `ReactPowerGeneratorNoise` | 1 | 对发电机噪音的反应 |
| `ReactCarHornNoise` | 1 | 对车喇叭的反应 |
| `ReactAlarmClockNoise` | 1 | 对闹钟的反应 |
| `ReactKitchenTimerNoise` | 1 | 对厨房计时器的反应 |
| `ReactFuelStationNoise` | 1 | 对加油站爆炸的反应 |
| `ReactFireworksNoise` | 1 | 对烟花的反应 |
| `ReactExplosiveItemNoise` | 1 | 对爆炸物的反应 |
| `ReactCarEngineNoise` | 1 | 对引擎噪音的反应 |
| `ReactScreamNoise` | 1 | 对僵尸尖叫的反应 |
| `ReactWeaponShotNoise` | 1 | 对枪声的反应 |

**玩家噪音反应（分白天/夜晚）:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ReactFootstepsJogDayNoise` / `ReactFootstepsJogNightNoise` | 1 | 慢跑脚步声 |
| `ReactFootstepsCrouchSprintDayNoise` / `ReactFootstepsCrouchSprintNightNoise` | 0.7 | 蹲伏冲刺脚步声 |
| `ReactFootstepsSprintDayNoise` / `ReactFootstepsSprintNightNoise` | 1 | 冲刺脚步声 |
| `ReactDoorsDayNoise` / `ReactDoorsNightNoise` | 1 | 开关门声 |
| `ReactPlayerFallDayNoise` / `ReactPlayerFallNightNoise` | 1 | 玩家坠落声 |
| `ReactBodyfallDayNoise` / `ReactBodyfallNightNoise` | 0.5 | 僵尸尸体倒地声 |
| `ReactBodyfallBackstabDayNoise` / `ReactBodyfallBackstabNightNoise` | 0 | 背刺击杀倒地声 |
| `ReactSymptomsDayNoise` / `ReactSymptomsNightNoise` | 1 | 玩家症状声(咳嗽/喷嚏/呕吐等) |
| `ReactVoiceWhisperDayNoise` / `ReactVoiceWhisperNightNoise` | 1 | 耳语音 |
| `ReactVoiceTalkDayNoise` / `ReactVoiceTalkNightNoise` | 1 | 普通说话声 |
| `ReactVoiceShoutDayNoise` / `ReactVoiceShoutNightNoise` | 1 | 喊叫声 |
| `ReactMiningLightDayNoise` / `ReactMiningLightNightNoise` | 1 | 轻采矿噪音 |
| `ReactMiningHardDayNoise` / `ReactMiningHardNightNoise` | 1 | 重采矿噪音 |
| `ReactBuildingDayNoise` / `ReactBuildingNightNoise` | 1 | 建筑噪音 |
| `ReactSawPlanksDayNoise` / `ReactSawPlanksNightNoise` | 1 | 锯木板噪音 |
| `ReactVanillaMindstateChange` | 1 | 原版心智状态变化反应 |

**刺激物摧毁行为 (ReactAndDestroy*):**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ReactAndDestroyFlashlightsVisual` | 1 | 摧毁手电筒 |
| `ReactAndDestroyHeadtorchRedVisual` | 1 | 摧毁红色头灯 |
| `ReactAndDestroyRoadflareVisual` | 1 | 摧毁路焰 |
| `ReactAndDestroyRoadflareNoise` | 1 | 摧毁路焰(噪音) |
| `ReactAndDestroyChemlightVisual` | 1 | 摧毁化学灯 |
| `ReactAndDestroyChemlightRedVisual` | 1 | 摧毁红色化学灯 |
| `ReactAndDestroyPortableGasLampVisual` | 1 | 摧毁便携燃气灯 |
| `ReactAndDestroyFlammablesVisual` | 0.5 | 摧毁可燃物 |
| `ReactAndDestroySpotlightVisual` | 0.25 | 摧毁聚光灯 |
| `ReactAndDestroyFireplaceVisual` | 0.25 | 摧毁篝火 |
| `ReactAndDestroyFireplaceDayVisual` | 0.25 | 白天摧毁篝火 |
| `ReactAndDestroyCarLightVisual` | 1 | 摧毁车灯 |
| `ReactAndDestroyFireworksNoise` | 0.25 | 摧毁烟花 |
| `ReactAndDestroyPowerGeneratorNoise` | 0.1 | 摧毁发电机 |
| `ReactAndDestroyAlarmClockNoise` | 1 | 摧毁闹钟 |
| `ReactAndDestroyKitchenTimerNoise` | 1 | 摧毁计时器 |
| `ReactAndDestroySmokeGrenadeVisual` | 0.5 | 摧毁烟雾弹 |

**自定义刺激物反应:**

| 参数 | 说明 |
|------|------|
| `ReactCustomIrritants` | 定义每种自定义刺激物对于不同感染者的 `React`(反应) 和 `Destroy`(摧毁) 行为 |

详见 [9.9 原版刺激物与 Inedia 刺激物的关系](#99-原版刺激物与-inedia-刺激物的关系)。

---

### 3.16 Zombies.DamageToPlayer*

控制感染者对玩家的各类伤害。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DamageToPlayerHandlerIsActive` | 0/1 | 1 | 伤害系统总开关 |
| `DamageToPlayerHealthMultiplier` | 0~∞ | 1.2(low/med/high:递增) | 健康伤害倍率 |
| `DamageToPlayerShockMultiplier` | 0~∞ | 1.2(low/med/high:递增) | 冲击伤害倍率 |
| `DamageToPlayerStaminaPercent` | 0~100 | 12(low/med/high:递增) | 体力伤害(%) |
| `DamageToPlayerBloodPercent` | 0~100 | 0 | 失血伤害(%) |
| `DamageToPlayerBleedingHandlerIsActive` | 0/1 | 1 | 流血系统开关 |
| `DamageToPlayerBleedingChancePercent` | 0~100 | 10(low/med/high:递增) | 造成流血概率(%) |
| `DamageToPlayerInBlockHealthMultiplier` | 0~∞ | 0.6 | 格挡时健康伤害倍率 |
| `DamageToPlayerInBlockShockMultiplier` | 0~∞ | 0.6 | 格挡时冲击伤害倍率 |
| `DamageToPlayerInBlockStaminaPercent` | 0~100 | 6 | 格挡时体力伤害(%) |
| `DamageToPlayerInBlockBloodPercent` | 0~100 | 0 | 格挡时失血伤害(%) |
| `DamageToPlayerInBlockBleedingChancePercent` | 0~100 | 5 | 格挡时流血概率(%) |

---

### 3.17 Zombies.DamageToZombie*

控制感染者受到的伤害和防御。**可对动物和玩家(`SurvivorBase`)配置。**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DamageToZombieHandlerIsActive` | 0/1 | 1 | 僵尸伤害系统总开关 |
| `DamageToZombieHealthPoints` | >=-1 | -1 | 生命值。-1=使用原版HP(100)。特殊Boss单独设值 |
| `DamageToZombieHealthPointsLeg` | >=-1 | -1 | 腿部生命值。-1=使用 `DamageToZombieHealthPoints` 的值 |
| `DamageToZombieHeadMeleeMultiplier` | 0~∞ | 1.5 | 近战爆头伤害倍率 |
| `DamageToZombieHeadRangeMultiplier` | 0~∞ | 1 | 远程爆头伤害倍率 |
| `DamageToZombieBodyMeleeMultiplier` | 0~∞ | 0.8 | 近战身体伤害倍率 |
| `DamageToZombieBodyRangeMultiplier` | 0~∞ | 1(根据防御组变化) | 远程身体伤害倍率 |
| `DamageToZombieFromCarsMultiplier` | 0~∞ | 1 | 车辆撞击伤害倍率 |
| `DamageToZombieFromExplosionsMultiplier` | 0~∞ | 1 | 爆炸伤害倍率 |
| `DamageToZombieFromHotItemsHp` | float | 10 | 热物品(如燃烧)造成的HP伤害 |
| `DamageToZombieBodyPartsPiercingIsActive` | 0/1 | 1 | 子弹穿透多部位伤害。0=仅计入首次命中 |
| `DamageToZombieAlwaysKillOnBackstab` | 0/1 | 1 | 背刺必定击杀。0=按实际伤害计算 |

**冲击眩晕系统:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DamageToZombieShockToStunHandlerIsActive` | 0/1 | 1(Boss:0) | 冲击眩晕系统开关。0=使用原版眩晕机制 |
| `DamageToZombieShockToStunLightHeavyAnimationThresholdMeleeHeavy` | float | 0 | 近战重击触发重眩晕动画的冲击伤害阈值 |
| `DamageToZombieShockToStunLightHeavyAnimationThresholdRange` | float | 200 | 远程触发重眩晕动画的冲击伤害阈值 |
| `DamageToZombieShockToStunThresholdMeleeHeavy` | float | 0 | 近战重击造成眩晕的最低冲击阈值。0=总是眩晕 |
| `DamageToZombieShockToStunThresholdRange` | float | 0 | 远程造成眩晕的最低冲击阈值。0=总是眩晕 |
| `DamageToZombieShockToStunFromButtstockHit` | -1/0/1/2 | 2 | 枪托打击眩晕动画。-1=自动/0=无/1=轻/2=重 |
| `DamageToZombieShockToStunCumulativeDamage` | 0/1 | 1 | 累积冲击伤害（0.1秒内累积计算） |
| `DamageToZombieShockToStunCumulativeDamageTimeFrameSeconds` | float | 0.1 | 累积伤害时间窗口(秒) |
| `DamageToZombieShockToStunIgnoreMeleeHitChancePercent` | 0~100 | 0 | 忽略近战重眩晕概率(%) |
| `DamageToZombieShockToStunIgnoreRangedHitChancePercent` | 0~100 | 0 | 忽略远程重眩晕概率(%) |
| `DamageToZombieShockToStunImmunityAfterMeleeHitSeconds` | float | 0 | 近战重眩晕后的免疫时间(秒) |
| `DamageToZombieShockToStunImmunityAfterRangedHitSeconds` | float | 0 | 远程重眩晕后的免疫时间(秒) |

**武器伤害倍率:**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DamageToZombieWeaponsMultipliers` | object | all:1 | 按武器/弹药类型设置伤害倍率。可指定武器类名或弹药类名，武器优先于弹药 |

**常用原版弹药类名参考（区分大小写，不支持基类）:**
`MeleeFist`, `MeleeFist_Heavy`, `FirearmHit_Pistol`, `FirearmHit_Rifle`, `FirearmHit_Rifle_Bayonet`, `FinisherHit`, `FinisherHitNeck`, `Bullet_762x54`, `Bullet_762x54Tracer`, `Bullet_308Win`, `Bullet_308WinTracer`, `Bullet_762x39`, `Bullet_762x39Tracer`, `Bullet_556x45`, `Bullet_556x45Tracer`, `Bullet_545x39`, `Bullet_9x39`, `Bullet_9x39AP`, `Bullet_357`, `Bullet_45ACP`, `Bullet_9x19`, `Bullet_380`, `Bullet_22`, `Bullet_12GaugePellets`, `Bullet_12GaugeSlug`, `Bullet_12GaugeRubberSlug`, `Bullet_ImprovisedBolt_1`, `Bullet_ImprovisedBolt_2`, `Bullet_HuntingBolt`, `Bullet_Flare`, `Bullet_FlareRed`, `Bullet_FlareGreen`, `Bullet_FlareBlue`

---

### 3.18 Zombies.MeleeAttacksDodge*

感染者近战闪避——在玩家正面时会短暂减速以躲避精确爆头。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `MeleeAttacksDodgeHandlerIsActive` | 0/1 | 1 | 近战闪避系统开关 |
| `MeleeAttacksDodgeChance` | 0~100 | 50 | 闪避概率(%) |
| `MeleeAttacksDodgeCooldownSeconds` | >=3 | 10 | 闪避冷却时间(秒) |

---

### 3.19 Zombies.JumpAttack*

感染者跳跃攻击——冲向玩家并尝试眩晕和击倒。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `JumpAttackHandlerIsActive` | 0/1 | 1 | 跳跃攻击系统开关 |
| `JumpAttackChance` | 0~100 | 20 | 跳跃攻击概率(%) |
| `JumpAttackCooldownSeconds` | >=3 | 45 | 跳跃攻击冷却时间(秒) |

---

### 3.20 Zombies.Blood*

感染者/动物的血液和流血系统。**可对动物和玩家(`SurvivorBase`)配置。**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `BloodHandlerIsActive` | 0/1 | 1(Boss/特殊:0) | 血液系统总开关。0=使用原版(无流血) |
| `BloodVolumeMl` | >=0 | 0 | 血量(ml)。0=根据体重自动计算(体重kg×0.07)（动物可用） |
| `BloodLossRateMinMl` | float | 5 | 最小流血速率(ml/秒)（动物可用） |
| `BloodLossRateMaxMl` | float | 60 | 最大流血速率(ml/秒)（动物可用） |
| `BloodLossRateRegenMl` | float | 0.2 | 流血速率回复(ml/秒)（动物可用） |
| `BloodOnExplosiveDamageChancePercent` | 0~100 | 50 | 爆炸伤害导致流血概率(%)（动物可用） |
| `BloodSplatParticlesIsActive` | 0/1 | 1 | 血液飞溅粒子开关（动物/玩家可用） |
| `BloodTrailParticlesIsActive` | 0/1 | 1 | 血迹拖尾粒子开关（动物/玩家可用） |
| `BloodPoolParticlesIsActive` | 0/1 | 1 | 血泊粒子开关（动物/玩家可用）。坡度>15°不生成 |

详见 [9.1 血液与流血系统详解](#91-血液与流血系统)。

---

### 3.21 Zombies.ResistContaminatedEffect*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ResistContaminatedEffectHandlerIsActive` | 0/1 | 1 | 抗毒区系统开关。0=由其他模组处理（动物/玩家可用） |
| `ResistContaminatedEffect` | 0/1 | 0(NBC僵尸:1) | 对毒区的免疫开关。1=免疫毒区伤害 |

---

### 3.22 Zombies.AllowCrawling / RespawnInCrawling*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `AllowCrawling` | 0/1 | 1 | 允许玩家打残感染者腿部使其爬行 |
| `RespawnInCrawlingChancePercent` | 0~100 | 0 | 感染者生成时处于爬行状态的概率(%) |

---

### 3.23 Zombies.Scream*

感染者尖叫吸引同伴的系统。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ScreamHandlerIsActive` | 0/1 | 1 | 尖叫系统开关 |
| `ScreamAttractsZombiesInRadius` | float | 50(军官:120) | 尖叫吸引半径(米) |
| `ScreamChancePercent` | 0~100 | 25(军官:100) | 发现玩家时尖叫的概率(%)。不尖叫=沉默攻击 |
| `ScreamCooldownSeconds` | float | 60 | 尖叫冷却时间(秒) |
| `ScreamNearbyInfectedSilenceSeconds` | float | 60 | 附近感染者被尖叫沉默的时间(秒) |

---

### 3.24 Zombies.SearchBody*

玩家搜索感染者尸体获取物品的系统。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `SearchBodyToViewCargo` | 0/1 | 0 | 是否需要搜索才能查看尸体物品。0=直接查看 |
| `SearchBodyToViewCargoSeconds` | float | 1 | 搜索所需时间(秒) |
| `SearchBodyExtendLootingToPlayersInRadiusMeters` | float | 100 | 搜索尸体效果延伸给附近玩家的距离(米) |
| `SearchBodyOnlyEmptyHands` | 0/1 | 0 | 是否必须空手才能搜索 |
| `SearchBodyWithoutGlovesBloodyHandsChancePercent` | 0~100 | 0 | 不戴手套搜索导致血手的概率(%) |
| `SearchBodyWithoutMaskVomitChancePercent` | 0~100 | 10 | 不戴面具搜索导致呕吐的概率(%) |

---

### 3.25 Zombies.Butchering*

感染者尸体屠宰系统。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CanBeButchered` | 0/1 | 1 | 是否可被屠宰 |
| `ButcheringSeconds` | float | 20 | 屠宰所需时间(秒) |
| `ButcheringWithoutGlovesBloodyHandsChancePercent` | 0~100 | 100 | 不戴手套屠宰导致血手的概率(%) |
| `ButcheringWithoutMaskVomitChancePercent` | 0~100 | 50 | 不戴面具屠宰导致呕吐的概率(%) |
| `ItemsAfterButchering` | array | 骨头/布条/内脏/人肉等 | 屠宰后掉落的物品列表（见下方） |

**ItemsAfterButchering 条目结构:**
```json
{
    "ClassId": "Bone",
    "DropChancePercent": 100,
    "QuantityInStackFromPercent": 16,
    "QuantityInStackToPercent": 84,
    "ConditionFrom": 2,
    "ConditionTo": 3,
    "Foodstages": []
}
```
- `ClassId` — 物品类名
- `DropChancePercent` — 掉落概率(%)
- `QuantityInStackFromPercent` / `QuantityInStackToPercent` — 堆叠数量范围(占最大堆叠的%)
- `ConditionFrom` / `ConditionTo` — 物品状态范围
- `Foodstages` — 食物阶段（用于肉类，如 `[6]`=腐烂）

---

### 3.26 Zombies.CanBeBackstabbed*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CanBeBackstabbedHandlerIsActive` | 0/1 | 0 | 背刺系统自定义开关 |
| `CanBeBackstabbed` | 0/1 | 1 | 是否允许被背刺 |

---

### 3.27 Zombies.VisionRangeMultiplier*

影响原版感染者对玩家的可见度倍率。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `VisionRangeMultiplierDay` | 0~∞ | 2 | 白天视野倍率（原版=1） |
| `VisionRangeMultiplierNight` | 0~∞ | 0.8 | 夜晚视野倍率（原版=1） |

---

### 3.28 Zombies.Size*

感染者的随机体型系统。默认关闭。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `SizeHandlerIsActive` | 0/1 | 0 | 体型系统开关 |
| `SizeFromMultiplier` | float | 0.9 | 体型最小倍率 |
| `SizeToMultiplier` | float | 1.1 | 体型最大倍率 |
| `SizeDamageScalingIsActive` | 0/1 | 0 | 体型影响伤害开关 |
| `SizeBloodVolumeScalingIsActive` | 0/1 | 1 | 体型影响血量开关 |
| `SizeSpeedMultiplierScalingIsActive` | 0/1 | 1 | 体型影响速度开关 |

---

### 3.29 Zombies.ThrowingProjectilesHandler*

控制投掷物系统全局行为和绑定。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ThrowingProjectilesHandlerIsActive` | 0/1 | 1 | 投掷系统总开关。⚠️禁用也会禁用玩家投掷物伤害 |
| `ThrowingProjectilesHandlerDamageMultiplier` | 0~∞ | 0.5 | 所有投掷物对玩家/生物伤害倍率（动物/玩家可用） |
| `ThrowingProjectilesHandlerVehiclesDamageMultiplier` | 0~∞ | 0.5 | 所有投掷物对车辆伤害倍率。0=完全禁用（动物/玩家可用） |
| `ThrowingProjectilesHandlerThrowForceMultiplier` | 0~∞ | 默认不配=1 | 投掷力度(初速度)倍率 |
| `ThrowingProjectilesHandlerSpreadMultiplier` | 0~∞ | 默认不配=1 | 投掷扩散(精准度)倍率 |
| `ThrowingProjectilesHandlerProjectilesList` | object | 按组配置 | 将 `ThrowingProjectiles` 中定义的投掷物绑定到各组感染者 |

**ThrowingProjectilesHandlerProjectilesList 示例:**
```json
"ThrowingProjectilesHandlerProjectilesList": {
    "all": [],
    "military": ["GarbageIfPlayerOnObstacle", "MilitaryProjectile"],
    "police": ["GarbageIfPlayerOnObstacle", "PoliceProjectile"],
    "medics": ["GarbageIfPlayerOnObstacle", "MedicsProjectile"]
}
```

详见 [9.6 投掷物系统配置指南](#96-投掷物系统配置指南)。

---

### 3.30 Zombies.RangeAttacksHandler*

感染者远程攻击系统（用于替代/补充投掷物系统）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `RangeAttacksHandlerIsActive` | 0/1 | 0 | 远程攻击系统开关 |
| `RangeAttacksHandlerZombiePlayerDistance` | float | 2 | 远程攻击距离(米) |
| `RangeAttacksHandlerPlayerOnObstacleHeight` | float | 0.5 | 玩家在障碍物上的高度阈值(米) |

---

### 3.31 Zombies.DiseasesToPlayer*

感染者传播疾病给玩家的系统。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DiseasesToPlayerHandlerIsActive` | 0/1 | 1 | 疾病传播系统开关 |
| `DiseasesToPlayerAgents` | object | 按组配置 | 每种生物可传播的病原体配置 |

**DiseasesToPlayerAgents 条目结构:**
```json
{
    "AgentId": 64,
    "AddChance": 10,
    "AddChanceInBlock": 5,
    "AddAmount": 10,
    "AddAmountInBlock": 5,
    "AddAmountNoMoreThan": 50,
    "AddOnlyIfBleeding": 1
}
```
- `AgentId` — 病原体ID
- `AddChance` — 添加病原体概率(%)
- `AddChanceInBlock` — 格挡时添加概率(%)
- `AddAmount` — 添加量
- `AddAmountInBlock` — 格挡时添加量
- `AddAmountNoMoreThan` — 总量上限
- `AddOnlyIfBleeding` — 仅流血时添加(0/1)

---

### 3.32 Zombies.CameraShakeToPlayer*

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `CameraShakeToPlayerIntensity` | 0~∞ | 0 | 受到攻击时镜头震动强度。0=禁用 |

---

### 3.33 Zombies.PainToPlayer*

Inedia 疼痛系统的僵尸侧配置。**可对动物和玩家(`SurvivorBase`)配置。**

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `PainToPlayerHandlerIsActive` | 0/1 | 1 | 疼痛系统僵尸侧开关。0=对特定生物不造成疼痛 |
| `PainToPlayerHeadMultiplier` | 0~∞ | 1(0.8~1.2) | 头部疼痛倍率 |
| `PainToPlayerHeadInBlockMultiplier` | 0~∞ | 0.6 | 格挡时头部疼痛倍率 |
| `PainToPlayerArmsMultiplier` | 0~∞ | 1.2 | 手臂疼痛倍率 |
| `PainToPlayerArmsInBlockMultiplier` | 0~∞ | 0.6 | 格挡时手臂疼痛倍率 |
| `PainToPlayerArmsDisarmMultiplier` | 0~∞ | 0.3 | 手臂受伤缴械倍率 |
| `PainToPlayerArmsInBlockDisarmMultiplier` | 0~∞ | 0.15 | 格挡时缴械倍率 |
| `PainToPlayerLegsMultiplier` | 0~∞ | 1.2 | 腿部疼痛倍率 |
| `PainToPlayerLegsInBlockMultiplier` | 0~∞ | 0.6 | 格挡时腿部疼痛倍率 |
| `PainToPlayerTorsoMultiplier` | 0~∞ | 1.2 | 躯干疼痛倍率 |
| `PainToPlayerTorsoInBlockMultiplier` | 0~∞ | 0.6 | 格挡时躯干疼痛倍率 |
| `PainToPlayerLimbsBreakChancesMultiplier` | 0~∞ | 1 | 骨折概率倍率 |
| `PainToPlayerLimbsDeepWoundChancesMultiplier` | 0~∞ | 1 | 深度伤口概率倍率 |

---

### 3.34 Zombies.StunToPlayer*

玩家被感染者击中时眩晕的概率。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `StunToPlayerChancePercent` | 0~100 | 25(low/med/high:递增) | 普通攻击眩晕概率(%) |
| `StunToPlayerInBlockChancePercent` | 0~100 | 12.5 | 格挡时眩晕概率(%) |

---

### 3.35 Zombies.DisarmToPlayer*

感染者击落玩家武器的概率。默认关闭。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DisarmToPlayerChancePercent` | 0~100 | 0 | 普通攻击缴械概率(%) |
| `DisarmToPlayerInBlockChancePercent` | 0~100 | 0 | 格挡时缴械概率(%) |

> **注意:** 不要与 `PainToPlayerArms*DisarmMultiplier` 混淆——后者仅在手臂受伤时通过 Inedia 疼痛系统生效。

---

### 3.36 Zombies.FastAttackToPlayerChancePercent

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `FastAttackToPlayerChancePercent` | 0~100 | 100 | 快速攻击概率(%) |

---

### 3.37 Zombies.LongVision*

**Inedia 长视野（Long Vision）系统。** 允许处于搜索模式的感染者看到远超原版 40m 极限的距离。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `LongVisionHandlerIsActive` | 0/1 | 1 | 长视野系统总开关。0=完全禁用 |
| `LongVisionMetersInSearchModeDay` | float | 120 | 白天搜索模式视野距离(米) |
| `LongVisionMetersInSearchModeNight` | float | 120 | 夜晚搜索模式视野距离(米) |
| `LongVisionMetersInCalmModeDay` | float | 0 | 白天平静模式视野距离(米)。⚠️默认关闭，启用前测试性能 |
| `LongVisionMetersInCalmModeNight` | float | 0 | 夜晚平静模式视野距离(米) |
| `LongVisionPersistAfterIrritationSeconds` | float | 300 | 搜索模式结束后长视野持续的时间(秒) |
| `LongVisionAllowIgnoreWeather` | 0/1 | 0 | 无视天气影响(雨/雪/雾)。默认继承天气影响 |
| `LongVisionVisualAcuity*` | 0~100 | 见下方 | 不同玩家姿态下的视觉敏锐度(%) |

详见 [9.3 Inedia 长视野详解](#93-inedia-长视野)。

---

### 3.38 Zombies.ReturnToSpawn*

感染者搜索模式结束后返回出生区域的机制。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `ReturnToSpawnHandlerIsActive` | 0/1 | 1 | 返回出生点系统开关 |

---

## 4. Players 参数

所有 `Players.*` 参数定义在配置文件的 `"Players"` 顶级节点下。

### 气味系统

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `SmellsHandlerIsActive` | 0/1 | 1 | 玩家气味系统总开关 |
| `SmellLifetimeSeconds` | float | 120 | 气味存留时间(秒)。受天气影响缩短 |
| `SmellsCountOnMapLimit` | int | 1000 | 地图上气味数量上限。超过后移除最旧气味。若性能有问题可降低此值 |
| `SmellRadiusDefault` | float | 见配置 | 健康玩家气味半径(米) |
| `SmellRadiusWounded` | float | 见配置 | 受伤玩家气味半径(米) |
| `SmellRadiusBandaged` | float | 见配置 | 包扎后玩家气味半径(米) |

### 脚步噪音

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `FootstepsNoiseHandlerIsActive` | 0/1 | 1 | 脚步噪音系统开关 |

### 搜索尸体（玩家侧）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `SearchBodyToViewCargo` | 0/1 | 0 | 0=直接查看/1=需搜索 |
| `SearchBodyToViewCargoSeconds` | float | 1 | 搜索时间(秒) |
| `SearchBodyExtendLootingToPlayersInRadiusMeters` | float | 100 | 延伸拾取距离(米) |
| `SearchBodyOnlyEmptyHands` | 0/1 | 0 | 必须空手搜索 |

### 静音开门

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `QuietDoorOpeningMechanicIsActive` | 0/1 | 1 | 静音开关门系统开关 |
| `QuietDoorOpeningMechanicDisabledForOpening` | 0/1 | 1 | 1=仅静音关门有效/0=开关门都可静音 |
| `QuietDoorOpeningMechanicSeconds` | float | 3 | 静音操作持续时间(秒) |
| `QuietDoorOpeningMechanicRestrictedBuildings` | array | 见配置 | 禁止静音开关门的建筑列表（钥匙卡门/保险库等） |
| `DisableVanillaDoorNoiseSystem` | 0/1 | 1 | 禁用原版门噪音系统 |

### 伤害分布

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `OverrideGetHitComponentChances` | 0/1 | 1 | 覆盖原版肢体伤害分布。0=使用原版系统 |

### 疼痛与受伤系统 (Inedia Pain System)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `PainSystemIsActive` | 0/1 | 0 | ⭐疼痛系统总开关。0=完全禁用整个疼痛系统（包括减益和所有伤型） |
| `PainSystemNotificationsType` | 0/1/2 | 2 | 疼痛通知类型。0=禁用/1=聊天/2=弹窗 |
| `ShowPainBadges` | 0/1 | 0 | 显示疼痛徽章图标 |
| `ShowPainBlur` | 0/1 | 0 | 显示疼痛模糊效果 |
| `ShowMedicationInfo` | 0/1 | 0 | 显示药物信息 |
| `PainHealingRatePerSecondPercent` | float | 0.5 | 疼痛恢复速率(%/秒)(默认0.1) |
| `HealthDrainWithOverPainedLimbPerSecondPercent` | float | 0.1 | 过度疼痛肢体导致的健康流失(%/秒) |

**疼痛倍率（各种来源）:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `VehicleCrashPainMultiplier` | 0.5 | 车辆撞击疼痛倍率 |
| `VehicleCollisionsPainMultiplier` | 0.5 | 车辆碰撞疼痛倍率 |
| `FallPainMultiplier` | 0.5 | 坠落疼痛倍率 |
| `ExplosionsPainMultiplier` | 0.5 | 爆炸疼痛倍率 |

**疼痛效果开关:**

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `UnconsciousWhenOverPainedHeadReceivingHits` | 0 | 头部过度疼痛时昏迷 |
| `CrouchWhenOverPainedTorsoReceivingHits` | 0 | 躯干过度疼痛时强制蹲伏 |
| `ArmsLowerWhenAimingWithPainedArms` | 0 | 手臂疼痛瞄准时手臂下垂 |
| `ArmsLowerWhenOverPainedArmsReceivingHits` | 0 | 手臂过度疼痛时下垂 |
| `ArmsPainShockDamageActions` | all:1 | 手臂疼痛动作冲击伤害 |
| `ArmsPainUnrestrainItems` | 见配置 | 手臂疼痛时挣脱束缚物品的阈值 |
| `AuditoryHallucinationsWithPainedHead` | 0 | 头部过度疼痛幻听 |
| `VomitWithPainedHead` | 1 | 头部疼痛呕吐 |
| `TinnitusWhenHeadReceivingHits` | 0 | 头部受击耳鸣 |
| `BlurWhenHeadReceivingHits` | 1 | 头部受击视线模糊 |
| `SoundAttenuationWhenHeadReceivingHits` | 0 | 头部受击环境声衰减 |
| `MovementCoordinationImpairmentWhenHeadReceivingHits` | 0 | 头部受击运动协调障碍(减速20秒) |
| `PainArmsWhenHitWithoutGloves` | 0 | 不戴手套攻击导致手臂疼痛 |
| `ShockIfRunsWithPainedLegs` | 0 | 腿部疼痛时跑步受冲击 |
| `ShockIfAttackingWithPainedArms` | 0 | 手臂疼痛时攻击受冲击 |
| `DisableStaminaRegenWhenTorsoPainDurationSeconds` | float | 躯干疼痛时禁用体力恢复的秒数 |
| `WeaponSwayWhenHeadReceivingHits` | 0/1 | 头部受击武器摇晃 |

### 骨折系统 (LimbsBreak)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `LimbsBreakSystemIsActive` | 0/1 | 0 | 骨折系统总开关。0=使用原版骨折机制 |
| `LimbsBreakPainThresholdPercent` | 0~100 | 30 | 骨折所需疼痛阈值(%) |
| `HeadBreakDurationSeconds` | >=0 | 1800 | 头骨骨折持续时间(秒)。0=禁用 |
| `ArmsBreakDurationSeconds` | >=0 | 1800 | 手臂骨折持续时间(秒)。0=禁用 |
| `LegsBreakDurationSeconds` | >=0 | 1800 | 腿部骨折持续时间(秒)。0=禁用 |
| `TorsoBreakDurationSeconds` | >=0 | 1800 | 肋骨骨折持续时间(秒)。0=禁用 |
| `LimbsBreakFromFalls` | 0/1 | 0 | 坠落导致骨折 |
| `LegsBreakFromTraps` | 0/1 | 0 | 捕兽夹导致腿部骨折 |
| `UnconsciousWhenHeadBreak` | 0/1 | 0 | 头骨骨折昏迷 |
| `LimbsBreakIgnoreAmmoList` | array | [] | 不触发骨折的弹药列表（如电击枪弹） |

### 深度伤口系统 (LimbsDeepWound)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `LimbsDeepWoundSystemIsActive` | 0/1 | 0 | 深度伤口系统总开关 |
| `HeadDeepWoundDurationSeconds` | >=0 | 1800 | 头部深度伤口持续(秒)。0=禁用 |
| `ArmsDeepWoundDurationSeconds` | >=0 | 1800 | 手臂深度伤口持续(秒)。0=禁用 |
| `LegsDeepWoundDurationSeconds` | >=0 | 1800 | 腿部深度伤口持续(秒)。0=禁用 |
| `TorsoDeepWoundDurationSeconds` | >=0 | 1800 | 躯干深度伤口持续(秒)。0=禁用 |
| `LimbsDeepWoundVanillaCutBleedRateMultiplier` | 0~1 | 0.1 | 原版切伤流血倍率（在深度伤口上下文中降低） |
| `LimbsDeepWoundFromFalls` | 0/1 | 0 | 坠落导致深度伤口 |
| `LegsDeepWoundFromTraps` | 0/1 | 0 | 捕兽夹导致腿部深度伤口 |

### 子弹伤系统 (LimbsBullet)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `LimbsBulletSystemIsActive` | 0/1 | 0 | 子弹伤系统开关 |
| `LimbsBulletTimeToSecondStageSeconds` | >=-1 | 7200 | 进入第二阶段的时间(秒)。-1=禁用 |

### 内出血系统 (InternalBleeding)

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `InternalBleedingSystemIsActive` | 0/1 | 0 | 内出血系统开关 |
| `InternalBleedingBloodLossRateMl` | >=0 | 2 | 内出血速率(ml/秒) |

### 通知和噪音

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `DestroyedDoorNotificationType` | 0/1/2 | 2 | 被破坏门通知类型。0=禁用/1=聊天/2=弹窗 |
| `NoiseMultiplierDay` | 0~∞ | 1 | 白天玩家原版噪音倍率 |
| `NoiseMultiplierNight` | 0~∞ | 1 | 夜晚玩家原版噪音倍率 |
| `NoiseMultiplierCrouchDay` | 0~∞ | 1 | 白天蹲伏噪音倍率 |
| `NoiseMultiplierCrouchNight` | 0~∞ | 1 | 夜晚蹲伏噪音倍率 |
| `NoiseMultiplierLadderDay` | 0~∞ | 0.2 | 白天爬梯噪音倍率（降低因原版爬梯噪音=跑步噪音） |
| `NoiseMultiplierLadderNight` | 0~∞ | 0.2 | 夜晚爬梯噪音倍率 |

### 伪装服

| 参数 | 说明 |
|------|------|
| `CamoClothingVisibilityMultipliers` | 定义伪装服列表及可见度倍率。0=感染者完全无法发现该玩家。多个伪装服倍率相乘 |

### 呕吐防护

| 参数 | 说明 |
|------|------|
| `HeadgearItemsWithVomitProtection` | 定义哪些头部装备提供呕吐防护。默认：摩托车头盔=防护，面具=防护（剔除特定不防护面具） |

---

## 5. Vehicles 参数

| 参数 | 说明 |
|------|------|
| `Vehicles.Noise` | 按车辆类配置引擎噪音吸引僵尸的半径 |
| `Vehicles.Noise.RpmIdleMeters` | 怠速时吸引半径(米)，默认40 |
| `Vehicles.Noise.RpmMaxMeters` | 最大转速时吸引半径(米)，默认120 |
| `Vehicles.CollisionsSoundThreshold` | 碰撞声音阈值速度(km/h)。低于此速度=轻微声，高于=巨大声。0=禁用碰撞声 |
| `Vehicles.CollisionsSpeedReductionMultiplier` | 碰撞减速倍率(0~∞)。0=无减速，1=真实物理减速，<1=减速减少，>1=减速增加 |
| `Vehicles.CollisionsDamageSpeedThresholdKmH` | 车辆开始受碰撞伤害的最低速度(km/h)。低于此速度=无伤害 |

**车辆降速公式:**
```
vehicleSpeedAfterCollision = (vehicleWeight - targetWeight) × speedBefore / (vehicleWeight + targetWeight)
实际降速 = (vehicleSpeedAfterCollision - speedBefore) × CollisionsSpeedReductionMultiplier
```

---

## 6. 全局参数

顶级配置参数（不在 Zombies/Players/Vehicles 节点下）。

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `LossInterestToIrritantAfterSeconds` | float | 120 | 感染者无法到达刺激物后失去兴趣的时间(秒)。全局参数 |
| `LightInHouseMultiplier` | 0~∞ | 0.2 | 室内发光物品的范围倍率 |
| `SoundInHouseMultiplier` | 0~∞ | 0.5 | 室内噪音物品的范围倍率 |
| `SuppressorShotCooldownSeconds` | >=0 | 5 | 消音器射击冷却时间(秒)。在此期间再次射击会被听到。0=禁用此机制 |
| `SuppressorShotOverfireDistanceMeters` | >=0 | 80 | 消音器连续射击(频率>SuppressorShotCooldownSeconds)的可被听到距离(米) |
| `BloodParticlesLimit` | >=0 | 1000 | 客户端血液粒子最大数量。超过后移除旧粒子 |
| `BloodParticleDurationSeconds` | >=0 | 600 | 血液粒子存留时间(秒)。前2/3时间不变,后1/3时间渐隐。0=禁用 Inedia 血液粒子系统（恢复原版/模组粒子系统） |
| `SaveConfigAfterInit` | 0/1 | 0 | 服务器启动后将缺失参数自动写入配置文件。⚠️使用前建议备份 |

---

## 7. Inedia 疼痛系统详解

### 7.1 系统概述

Inedia 疼痛系统是模组的核心特色功能。当角色肢体受到冲击伤害(Shock Damage)时，会产生疼痛(Pain)并获得相应减益(Debuff)。疼痛是系统的基石——疼痛越强，减益越严重。各类伤型（骨折、深度伤口、子弹伤）本身几乎不产生减益，但它们会影响疼痛水平，从而加重疼痛相关的减益。如果没有疼痛（如使用止痛药后），这些伤型就不会造成减益。

**系统禁用层级:**
- `Players.PainSystemIsActive` = 0 → 完全禁用整个疼痛系统（包括所有减益和伤型）
- `Zombies.PainToPlayerHandlerIsActive` = 0 对特定生物 → 仅禁用特定生物造成的疼痛
- `Zombies.PainToPlayer#LIMB#Multiplier` = 0 → 禁用特定肢体的疼痛
- `Players.LimbsBreakSystemIsActive` = 0 → 仅禁用骨折，保留其他
- `Players.LimbsDeepWoundSystemIsActive` = 0 → 仅禁用深度伤口，保留其他
- `Players.LimbsBulletSystemIsActive` = 0 → 仅禁用子弹伤，保留其他
- `Players.InternalBleedingSystemIsActive` = 0 → 仅禁用内出血，保留其他

每个肢体疼痛百分比 0%~100%，通过 `PainHealingRatePerSecondPercent` 参数自然恢复（默认 0.1%/秒）。受角色护甲影响——头盔和防弹衣在 PvE 服务器上也有意义。

### 7.2 疼痛等级与减益表

疼痛分为 3 级：**黄色**(轻度)、**橙色**(中度)、**红色**(重度)。

#### 手臂疼痛减益

| 等级 | 症状 |
|------|------|
| 黄色 (≥1%) | 近战攻击速度 -15%、武器摇晃增加 |
| 橙色 (≥30%) | 攻击速度 -30%、武器摇晃严重增加、瞄准时手臂下垂 |
| 红色 (≥50%) | 攻击速度 -50%、失去背刺能力、无法攀爬超过 1.5m 的障碍、无法挣脱束缚 |

- 手臂疼痛超过 10% 时，生物攻击手臂有概率缴械（由 `PainToPlayerArms*DisarmMultiplier` 控制）
- 不戴手套空手攻击会导致手臂疼痛（由 `PainArmsWhenHitWithoutGloves` 控制）
- 卧倒时手臂减益不适用

#### 腿部疼痛减益

| 等级 | 症状 |
|------|------|
| 黄色 (≥1%) | 移动速度降低 |
| 橙色 (≥30%) | 严重减速、冲刺消耗更多体力 |
| 红色 (≥50%) | 无法冲刺、无法跳跃、移动极慢 |

#### 躯干疼痛减益

| 等级 | 症状 |
|------|------|
| 黄色 (≥1%) | 体力消耗轻微增加 |
| 橙色 (≥30%) | 体力大幅重置、10 秒内体力不恢复 |
| 红色 (≥50%) | 强制蹲伏、严重体力惩罚 |

#### 头部疼痛减益

| 等级 | 症状 |
|------|------|
| 黄色 (≥1%) | 视野轻微模糊 |
| 橙色 (≥30%) | 视野模糊加重、可能呕吐 |
| 红色 (≥50%) | 严重模糊、幻听、可能失去意识 |

**头部额外效果（单次头部冲击伤害≥5时触发，最多每60秒一次）:**
- 耳鸣（`TinnitusWhenHeadReceivingHits`）
- 视线模糊持续 2.5~10 秒（`BlurWhenHeadReceivingHits`）
- 环境声衰减 70%（`SoundAttenuationWhenHeadReceivingHits`）
- 武器摇晃持续 3.75~15 秒（`WeaponSwayWhenHeadReceivingHits`）
- 严重减速持续 5~20 秒（`MovementCoordinationImpairmentWhenHeadReceivingHits`）
- 这些持续时间取决于头部防护和受到的伤害量

头部疼痛造成的模糊效果是其他肢体的3倍。

### 7.3 骨折系统

当受到足够冲击伤害时，肢体可能骨折。骨折将疼痛锁定在 ≥80%。

**骨折概率公式:** `0.03125 × 2^(LimbPainPercent / 10)`

骨折后可通过夹板（Splint/Splint Kit）稳定。稳定后：
- 骨折不再造成减益
- 骨折恢复速率翻倍
- 疼痛可以降低到 80% 以下
- 头骨骨折稳定后不会因昏迷机制失去意识

**骷髅骨折特殊机制：** 头骨骨折后每秒有 0.2% 概率失去意识（除非使用 Splint Kit 稳定）。7 秒前会有视线模糊和声音衰减的警告。休息姿势不会失去意识。此机制由 `UnconsciousWhenHeadBreak` 控制。

### 7.4 深度伤口系统

受到足够伤害时产生深度伤口。深度伤口导致持续流血，可通过止血敷料(Hemostatic Dressing)或原版绷带处理。

绷带有不同效果等级：
- 专业止血敷料(Hemostatic Dressing)：恢复倍率 ×3
- 原版绷带(Bandage Dressing)：恢复倍率 ×1.5, 持续 600s
- 布条(Rag/Bandana)：恢复倍率 ×1.2, 持续 600s
- 缝纫包(Sewing Kit)：恢复倍率 ×1.25, 持续 600s（但降低伤口恢复速度 ×0.25）

**无效绷带：** 当伤口需要专业敷料但使用了普通绷带时，绷带图标显示为灰色半透明（"无效"状态），恢复效果降低。

### 7.5 子弹伤系统

枪支伤害到未受保护的身体部位时产生子弹伤。子弹伤分为两个阶段：
- 第一阶段：子弹仍在体内，有持续额外负面影响
- 第二阶段（`LimbsBulletTimeToSecondStageSeconds` 后，默认 7200 秒）：子弹被组织包裹，负面影响降低

子弹伤需要手术工具(Surgical Kit)配合刀具取出。手术持续时间和成功率可通过脚本方法 `InediaInfectedAI_Restrictions.GetSurgeryDurationAndSuccessChance()` 定制。

### 7.6 内出血系统

受到枪伤或穿刺武器伤害到躯干时可能产生内出血。内出血导致持续失血，速率由 `InternalBleedingBloodLossRateMl` 设定。

内出血由原版弹药配置 `CfgAmmo Ammo DamageApplied bleedThreshold` 决定触发概率。

口服 Tranexam 药片可临时加速内出血恢复。

### 7.7 护甲与疼痛防护

Inedia 疼痛系统构建在原版 `Shock` 和 `Blood` 伤害之上。在 `config.cpp` 中增加护甲对这两种伤害的防护即可增加对疼痛系统的防护。

**示例：自定义护甲**
```cpp
// 近战疼痛防护 80%，深度伤口概率 0%
class CfgVehicles {
    class YourClothingItem {
        class GlobalArmor {
            class Melee {
                class Shock { damage = 0.2; };   // 仅受20%冲击伤害→20%疼痛
                class Blood { damage = 0.0; };    // 0%失血→深度伤口概率0%
            };
            class Projectile {
                class Shock { damage = 0.6; };    // 60%冲击伤害
                class Blood { damage = 0.1; };    // 10%深度伤口概率
            };
        };
    };
};
```

**⚠️ 重要：** 对于子弹伤害，Blood 防御倍率不能超过 0.5（即 `damage=0.5`）。因为超过 50% 的失血伤害在计算深度伤口概率时被视为 100%。这是为了防止子弹因距离衰减后打中无防护角色却不产生深度伤口。

---

## 8. Inedia 医疗系统详解

### 8.1 模组新增药物

`types.xml` 和服务器配置文件位于模组根目录的 `types/` 文件夹中。

| 药物 | 效果 |
|------|------|
| **Tramadol 片** | 强力止痛药。降低所有肢体的疼痛水平。过量服用会产生呕吐副作用 |
| **Tranexam 片** | 加速深度伤口和内出血恢复（再生 ×2），持续 300s |
| **Sorbifer Durules 片** | 再生血液。强力补血剂 |
| **Metoclopramide 片** | 止吐药。抑制呕吐反射 |
| **Calcium Hydroxyapatite 胶囊** | 加速骨折恢复（再生 ×2），持续 300s |
| **Surgical Kit** | 手术工具包。从肢体中取出子弹和碎片。需配合刀具使用。5次使用次数 |
| **Splint Kit** | 专业夹板套件。稳定骨折，恢复速度 ×3 |
| **Hemostatic Dressing** | 止血敷料。闭合深度伤口，再生 ×3。4次使用次数。恢复时间=1800/(1×3)=600s |

### 8.2 原版物品的疼痛/医疗属性

| 物品 | 效果 |
|------|------|
| **吗啡 (Morphine)** | 强效止痛。完全消除疼痛症状（但不治疗骨折/深度伤口本身） |
| **止痛药/可待因 (Painkillers/Codeine)** | 中等止痛。减少疼痛水平 |
| **伏特加 (Vodka)** | 弱效止痛（液体消耗品） |
| **缝纫包 (Sewing Kit)** | 闭合深度伤口 |
| **绷带 (Bandage Dressing)** | 闭合深度伤口 |
| **布条/头巾 (Rags/Bandanas)** | 闭合深度伤口 |
| **夹板 (Splint)** | 稳定骨折 |
| **任何原版刀具（非手工制）** | 手术辅助工具 |
| **小型急救包** | 存储医疗用品 |
| **急救箱** | 存储医疗用品 |

### 8.3 自定义药物属性

通过修改模组的 `config.cpp` 可为任何物品添加 Inedia 药物属性。需将 InediaInfectedAI 添加为依赖。

**使物品成为止痛药:**
```cpp
class YourEdibleItem {
    class InediaInfectedAI_Medicine {
        PainKillerLevel = 2;  // 1=弱, 2=中, 3=强
        PainKillerDurationSeconds = 300;
        ShowTips = 1;         // 使用前显示属性提示
    };
};
```

**使物品成为补血物品:**
```cpp
class YourBloodItem {
    class InediaInfectedAI_Medicine {
        BloodRegenMultiplier = 10;   // 10倍于默认恢复速率
        BloodRegenDurationSeconds = 60;
        ShowTips = 1;
    };
};
```

**组合属性:**
```cpp
class YourHybridItem {
    class InediaInfectedAI_Medicine {
        PainKillerLevel = 3;
        PainKillerDurationSeconds = 120;
        BloodRegenMultiplier = 5;
        BloodRegenDurationSeconds = 60;
        ShowTips = 1;
    };
};
```

**液体物品（根据体积计算持续时间）:**
```cpp
class YourLiquidItem {
    class InediaInfectedAI_Medicine {
        PainKillerLevel = 1;
        PainKillerDurationSeconds = 120;  // 1升=120秒, 0.5升=60秒
    };
};
```

**全套药物属性参数:**

| 参数 | 说明 |
|------|------|
| `PainKillerLevel` | 止痛等级 1~3 |
| `PainKillerDurationSeconds` | 止痛持续时间(秒) |
| `BloodRegenMultiplier` | 血液再生倍率 |
| `BloodRegenDurationSeconds` | 血液再生持续时间(秒) |
| `DeepWoundHealMultiplier` | 深度伤口愈合倍率 |
| `DeepWoundHealDurationSeconds` | 深度伤口愈合持续时间(秒) |
| `BreakHealMultiplier` | 骨折愈合倍率 |
| `BreakHealDurationSeconds` | 骨折愈合持续时间(秒) |
| `InternalBleedingStopMultiplier` | 内出血停止倍率 |
| `InternalBleedingStopDurationSeconds` | 内出血停止持续时间(秒) |
| `VomitReflexBlock` | 阻止呕吐反射(0/1) |
| `ShowTips` | 显示提示(0/1) |
| `RemoveAllActionsExceptInedia` | 移除所有非 Inedia 动作(0/1) |

**消耗规则：** 消耗多个同类物品时，影响更大的效果会替换影响较小的（比较 `Duration × Multiplier`）。

### 8.4 自定义医疗工具属性

使物品成为伤型处理工具：

```cpp
class YourMedicalTool {
    class InediaInfectedAI_Medicine {
        // 骨折相关
        SplintFractureStabilization = 1;   // 稳定骨折
        SplintHealMultiplier = 3;           // 骨折愈合倍率
        SplintDurationSeconds = 1800;       // 夹板持续时间

        // 深度伤口相关
        CloseDeepWound = 1;                 // 闭合深度伤口
        CloseDeepWoundHealMultiplier = 3;   // 深度伤口愈合倍率
        CloseDeepWoundDurationSeconds = 1800;

        // 手术相关
        SurgeryTool = 1;                    // 手术工具标记
    };
};
```

**附加到 Inedia 医疗槽位:**
```cpp
class YourMedicalItem {
    class InediaInfectedAI_Medicine {
        // 对于非附件物品（药品）添加 InventorySlot 关联
    };
};
```

### 8.5 脚本 API 方法

以下辅助方法可在自己的模组中覆写以连接技能系统：

**影响手术/包扎的成功率和持续时间:**
```cpp
// 返回 {duration, successChance}
InediaInfectedAI_Restrictions.GetSurgeryDurationAndSuccessChance(
    PlayerBase player, string limb, float baseDuration, float baseSuccessChance)

InediaInfectedAI_Restrictions.GetCloseDeepWoundDurationAndSuccessChance(
    PlayerBase player, string limb, float baseDuration, float baseSuccessChance, not_iint item)

InediaInfectedAI_Restrictions.GetSplintFractureStabilizationDurationAndSuccessChance(
    PlayerBase player, string limb, float baseDuration, float baseSuccessChance, not_iint item)
```

**控制不同等级止痛药的激活条件:**
```cpp
bool InediaInfectedAI_Restrictions.IsWeakPainKillerActivated(PlayerBase player)
bool InediaInfectedAI_Restrictions.IsMediumPainKillerActivated(PlayerBase player)
bool InediaInfectedAI_Restrictions.IsStrongPainKillerActivated(PlayerBase player)
```

**直接操作疼痛系统:**
```cpp
// 为肢体增加/减少疼痛 (value 可正可负)
player.InediaInfectedAI_GetPainManager().AddPainPercentForLimb("Head", -10.0);
player.InediaInfectedAI_GetPainManager().AddPainPercentForLimb("RightArm", -10.0);

// 直接停用骨折
player.InediaInfectedAI_GetPainManager().DeactivateBreakForLimb("RightLeg");

// 直接停用深度伤口
player.InediaInfectedAI_GetPainManager().DeactivateDeepWoundForLimb("Torso");
```

**修改玩家气味半径:**
```cpp
// 覆写此方法实现自定义气味逻辑（如技能/卫生系统）
float InediaInfectedAI_Restrictions.SmellsSystem_ModifyPlayerSmellRadius(
    PlayerBase player, float baseRadius)
```

**触发感染者搜索模式（用于自定义模组）:**
```cpp
// 在指定位置触发感染者搜索模式
InediaInfectedAI_IrritantsManager.ModMassSearchActivation(
    vector position, float radius, int irritantType, float priority)
// irritantType: 0=视觉, 1=噪音
// ⚠️ 不建议过于频繁调用（5~10秒一次足够），因为内部使用原版声音系统，高频率大范围调用会影响性能
```

---

## 9. 核心机制深度解析

### 9.1 血液与流血系统

感染者和动物在此模组中有血液系统，可因流血而死亡。与玩家不同，生物只有一个流血速率参数。

**初始血量:** `WeightKG × 0.07`
- 普通感染者: ~5000 ml
- 熊: ~11000 ml
- 鹿: ~14000 ml
- 牛: ~40000 ml

**流血速率公式:**
```
BleedingRatePerSecond = (DamageTakenHealth × DamageTakenBlood) × BleedingCoef
```
- `BleedingCoef`: 近战=0.0025, 其他=0.005
- `DamageTakenBlood` 从原版弹药配置 (`CfgAmmo #AMMO# DamageApplied bleedThreshold`) 中获取，受护甲和距离影响
- `DamageToZombie*Multiplier` 防御参数不影响计算中使用的伤害值
- 头部伤害使流血概率 3 倍提升

**流血速率边界:**
- 低于 `BloodLossRateMinMl` → 设为 `BloodLossRateMinMl`
- 高于 `BloodLossRateMaxMl` → 设为 `BloodLossRateMaxMl`
- 每秒减少 `BloodLossRateRegenMl`（默认 0.2 ml，即伤口在愈合）

**示例:**
CZ75 手枪对感染者造成 30 Health + 100 Blood 伤害:
1. 初始流血速率 = `30 × 100 × 0.005 = 15 ml/sec`
2. 紧接着再中一枪 30 Health: `15 + (30 × 100 × 0.005) = 30 ml/sec`
3. 伤口愈合时间 = `30 / 0.2 = 150 秒`

**失血效果阈值:**
| 生物类型 | >20% 失血 | >30% 失血 | >40% 失血 |
|----------|-----------|-----------|-----------|
| 感染者 | 不能快跑 | 只能步行/不能跳/不能破门/攻击力减半 | 死亡 |
| 动物 | - | 切换为小跑(玩家可追上) | 死亡 |

**注:** 减速降幅需要 `DamageToPlayerHandlerIsActive` 和 `SpeedHandlerIsActive` 开启。

### 9.2 气味系统

气味系统让感染者能通过气味持续追踪玩家。

**气味生成周期:** 每 10 秒，玩家生成一个气味。
- 气味半径: `SmellRadiusDefault`(健康) / `SmellRadiusWounded`(受伤) / `SmellRadiusBandaged`(包扎)
- 气味存留: `SmellLifetimeSeconds`（默认 120s）
- 气味随风移动
- 天气影响：雨/雾按强度等比缩小气味半径

**感染者检测周期:** 每 10 秒，检查是否有气味与检测球相交。
- 检测球半径: `SmellsSphereRadius`（默认 2m），受天气影响缩小
- 检测到气味 → 感染者进入搜索模式 → 向气味源与玩家连线上的某点移动
- 目标点偏移由 `SmellsChaseMultiplier` 控制

**特殊规则:**
- 玩家在建筑内不会生成新气味，但旧气味保持活跃
- `SmellsAllowStealthKills` = 1 时，潜行击杀不受气味干扰
- `SmellsLossInterestAfterReactionForSeconds` 设定反应后的忽略期（大检测球时有用）
- `SmellsCountOnMapLimit` 设定全图气味上限（默认 1000，性能有问题时可降低）

**性能提示:** 如果用户将检测球或气味半径设得很大（如 500m），可能导致性能下降。可启用 `SmellsDisableVanillaIrritationSound` 来缓解。

**自定义气味逻辑:** 覆写 `InediaInfectedAI_Restrictions.SmellsSystem_ModifyPlayerSmellRadius()` 方法实现基于技能/卫生系统的气味半径变化。

### 9.3 Inedia 长视野

此机制让处于搜索模式的感染者可以看到远超原版 40m 极限的距离（默认 120m），旨在防止玩家远距离骚扰感染者后安全搜刮。

**工作原理:**
- 每 **10 秒**，感染者检查前方 **120m** 内是否有**移动中的玩家**
- 静止不动的玩家**不会被**此机制发现（除非已被追击）
- 检测概率取决于玩家**姿态/移动速度/追击状态**，**不受距离影响**

**检测概率（由 `LongVisionVisualAcuity*` 参数控制）:**

| 状态 | 默认概率 |
|------|----------|
| 追击中 | 100% |
| 冲刺/慢跑 | 较高概率 |
| 步行 | 中等概率 |
| 蹲伏移动 | 较低概率 |
| 卧倒/静止 | 0% |

**额外影响因素:**
- `LongVisionAllowIgnoreWeather` = 1 → 感染者无视雨/雪/雾
- `LongVisionPersistAfterIrritationSeconds` → 搜索结束后长视野继续有效的时间（默认 300s/5min）
- 平静模式下默认不启用（`LongVisionMetersInCalmMode*` = 0），可为 Boss 单独开启

**战术意义:** 一旦激怒感染者，它们会在 5 分钟内保持高度警觉。不能骚扰-脱离-再回来。规则很简单——不要激怒感染者。

### 9.4 感染者受伤与减益系统

当感染者肢体受到足够累积伤害时产生受伤及减益。对动物也适用（简化版）。

**受伤判定:**
- 手臂累积伤害 > `InjuryHandlerDamageThresholdToInjuryArm`（默认 30 HP）
- 腿部累积伤害 > `InjuryHandlerDamageThresholdToInjuryLeg`（默认 30 HP）
- 仅使用原始原版伤害值，不受 `DamageToZombie*Multiplier` 防御参数和原版 `TransferToGlobalCoef` 倍率影响

**手臂受伤减益:**
- 单手受伤: 攻击力 ×0.5, 破门概率 ×0.5, 眩晕概率 ×0.5, 疼痛 ×0.5, 流血概率 ×0.5
- 双手受伤: 攻击力 ×0.2, 破门概率 0, 眩晕概率 0, 疼痛 0, 流血概率 0

**腿部受伤减益:**
- 单腿受伤: 速度限制 2.1(慢跑), 跳跃高度 ×0.5
- 双腿受伤: 速度限制 1(步行), 跳跃高度 0(不能跳)

**注意:** 减益生效前提条件同血液系统：
- 伤害降幅需要 `DamageToPlayerHandlerIsActive` 开启
- 流血概率降幅需要 `DamageToPlayerBleedingHandlerIsActive` 开启
- 速度降幅需要 `SpeedHandlerIsActive` 开启

**Boss/突变体处理:**
- 方式一：设置 `InjuryHandlerIsActive` = 0 对该生物完全禁用受伤系统
- 方式二：将 `InjuryHandlerDamageThresholdToInjury(Arm/Leg)` 提高到很大值（如 500/1000 HP）

### 9.5 车辆攻击逻辑

车辆受到的伤害分为两种类型：

**碰撞伤害 (Collision damage):**
1. 伤害随机分配给车辆部件
2. **先**攻击保护性部件（保险杠、挡泥板、引擎盖）
3. 保护性部件完全损毁后才攻击重要部件（引擎、散热器、电池、火花塞、油箱等）
4. 车门在碰撞中不被伤害（既非保护性也非重要部件），但车门在玩家保护中起关键作用（见下）

**生物攻击伤害 (Entity strike damage):**
1. 生物在 `AttackCarPlayersDistanceMeters` 范围内搜索玩家
2. 找到玩家 + 路径上无车门 → 直接攻击玩家
3. 有车门 + 车窗玻璃 → 先攻击玻璃，再攻击车门和玩家
4. 车门未被摧毁 → 有 `AttackCarDoorChancePercent`% 概率伤害被重定向到车门
5. 车门被摧毁 → 100% 概率玩家受伤
6. 周围无玩家 → 攻击 `AttackCarElementsDistanceMeters` 范围内的车辆部件（按碰撞逻辑先保护性后重要部件）

### 9.6 投掷物系统配置指南

**配置流程:**

1. **定义投掷物** — 在 `Zombies.ThrowingProjectiles` 中配置每个项目（如同给感染者配备武器）
2. **绑定到感染者** — 在 `Zombies.ThrowingProjectilesHandlerProjectilesList` 中为各组感染者绑定投掷物
3. **（可选）全局调整** — 使用 `ThrowingProjectilesHandlerDamageMultiplier` / `ThrowForceMultiplier` / `SpreadMultiplier` 全局影响所有投掷物

**内置投掷物一览:**

| 投掷物 | 用途 |
|--------|------|
| `GarbageIfPlayerOnObstacle` | 玩家在障碍物上时投掷杂物（树枝+石头） |
| `GarbageIfPlayerNonObstacle` | 无障碍时通用投掷 |
| `GarbageIfPlayerInWater` | 玩家在水中时投掷（不默认绑定任何感染者） |
| `FlashGrenade` | 闪光弹 |
| `HEGrenade` | 高爆手雷(RGD5/M67) |
| `GasGrenade` | 毒气手雷 |
| `MilitaryProjectile` | 军事感染者投掷（头盔/刺刀/水壶/望远镜等） |
| `PoliceProjectile` | 警察感染者投掷（手枪/霰弹枪/刀等） |
| `MedicsProjectile` | 医疗感染者投掷（瓶/刀/滤罐/消毒剂等） |
| `CityProjectile` | 城市感染者投掷（瓶/棒球棍/管钳/手电筒等） |
| `VillagersProjectile` | 村民感染者投掷（农具/刀/斧头等） |
| `FirefightersProjectile` | 消防员感染者投掷（头盔/消防斧等） |
| `FishermenProjectile` | 渔民感染者投掷（刀/鱼竿/铲子等） |
| `HuntersProjectile` | 猎人感染者投掷（刀/水壶/望远镜等） |
| `IndustrialProjectile` | 工业感染者投掷（管钳/扳手/锤子/锯等） |

**⚠️ 硬编码限制:**
- 感染者不能在 3 秒内投掷两次
- 目标距离不能超过 50m（节省服务器 FPS，减少射线检测）
- 只能在追击模式下投掷（否则看不到目标）
- 投掷物伤害不是"感染者伤害"，不受本模组伤害倍率影响（故意为之避免与 Virus Z 等传播状态的模组冲突）

**玩家投掷物伤害:** 玩家投掷的手雷等投掷物会对感染者/动物/其他玩家造成伤害（此功能由 `ThrowingProjectilesHandlerIsActive` 控制）。

**仅允许玩家而禁止感染者投掷:**
```json
"ThrowingProjectilesHandlerIsActive": {
    "all": 0,
    "SurvivorBase": 1
}
```

### 9.7 格挡穿透机制

**核心理解:** 格挡穿透动画不代表穿透了生命伤害——它可能由格挡中的冲击伤害、流血概率或疼痛伤害触发。

**默认行为:**
- 感染者确实穿透格挡，但所有伤害/冲击/疼痛伤害减半
- 状态效果（眩晕、流血）概率也减半
- 这种动画是必要的——没有它，`PlayerBase.EEHitBy()` 不会返回造成伤害所需的参数值

**触发条件（满足任一即触发）:**
1. `DamageToPlayerInBlockHealthMultiplier` > 0 → 有格挡健康伤害
2. `DamageToPlayerInBlockShockMultiplier` > 0 → 有格挡冲击伤害
3. `DamageToPlayerInBlockBleedingChancePercent` > 0 → 有格挡流血概率
4. `PainToPlayer#LIMB#InBlockMultiplier` > 0 → 有格挡疼痛伤害

**⚠️ 重要:** 无论角色是否受伤，格挡穿透动画都会损坏衣物。要禁用衣物损坏，必须按上面条件完全禁用格挡穿透动画。

**如何完全禁用:** 设置 `DamageToPlayerHandlerIsActive` = 0，但会失去所有与此参数相关的伤害控制功能。

### 9.8 天气对机制的影响

**下雨:**
- 降低噪音刺激物效果（降低到原有效果的一定比例，受雨强影响）
- 缩小气味检测球半径和气味半径
- 减弱长视野检测（除非 `LongVisionAllowIgnoreWeather` = 1）

**降雪 (DayZ 1.26 引入):**
- 效果同下雨

**雾:**
- 降低视觉刺激物效果
- 缩小气味检测球半径和气味半径
- 减弱长视野检测（除非 `LongVisionAllowIgnoreWeather` = 1）

**风:**
- 每 10 秒将所有气味向风向移动
- 影响气味的实际传播方向

**⚠️ 重要:** 不同因素对同一刺激物的影响是**相乘**而非相加。例如：雨降低噪音至 40%，雪降低至 70%，则最终效果 = 40% × 70% = 28%。

### 9.9 原版刺激物与 Inedia 刺激物的关系

感染者有**两种**切换到搜索模式的方式：
1. **原版机制** — 通过心智状态变化(CALM→ALERTED/DISTURBED)触发
2. **Inedia 机制** — 通过 Inedia 的 `React*` 参数触发

**为什么会同时存在？**

一些 `React*` 参数与原版机制重叠（如 `ReactWeaponShotNoise` 与枪声）。调整 Inedia 参数似乎不生效是因为原版刺激物仍在起作用。

Inedia 刺激物的引入原因是：当感染者已处于 MINDSTATE_ALERTED 状态时，原版机制无法继续处理新的脚步噪音等刺激并改变搜索目标。Inedia 刺激物允许独立于原版心智状态改变感染者目标。

**如何让 Inedia 刺激物参数有实际意义:**
使用 `ReactVanillaMindstateChange` 限制原版搜索模式激活半径。例如：
```json
"ReactVanillaMindstateChange": {
    "all": 50   // 仅50m内通过原版机制切换搜索模式
}
```
这样 50m 以外的感染者只能通过 Inedia 刺激物进入搜索模式，使得 `React*` 参数有真正的配置空间。

⚠️ 不建议将 `ReactVanillaMindstateChange` 设为低于 0.3。

### 9.10 消音器机制

**原版累积刺激机制:** 原版中，感染者有一个累积刺激量表。过于频繁地射击（即使带消音器）也会触发表满。每 5 秒射一枪就不会有问题。

**Inedia 消音器机制:** 如果消音武器射击频率高于 `SuppressorShotCooldownSeconds`（默认 5s），感染者会听到射击声。
- 设置为 0 可禁用此机制
- 设置为 0.3 时，单发消音射击不会被听到，但连发/点射会被听到
- `SuppressorShotOverfireDistanceMeters`（默认 80m）设定连发射击的可听距离

**MKII 和 AS VAL:** 游戏中最安静的武器，刺激量表上升最慢。但如果像机枪一样快速连射，它们同样会引起反应。

### 9.11 水中感染者的处理

默认情况下，感染者可在水面和水下构建路径（通过 game config 实现，不能在 Inedia 配置中关闭）。

**禁用水中行走的方法:**
1. 创建含以下 `config.cpp` 的模组：
```cpp
class CfgPatches { ... };
class CfgWorlds {
    class CAWorld {
        class DefaultWaterGeometry {
            allowInsanityForAI = 0;
        };
    };
};
```
2. 或使用 [此模组](https://steamcommunity.com/sharedfiles/filedetails/?id=3119213010)（允许重新打包）

**禁用水中行走后:** 将 `GarbageIfPlayerInWater` 投掷物绑定到感染者，防止玩家在水中安全射击。

---

## 10. 常见问题排查

### 配置文件被忽略
1. 用 [jsonlint.com](https://jsonlint.com) 验证 JSON 格式
2. 检查 `crash_*.log`（在线验证器检测不到参数类型不匹配）
3. 添加 SteamID 到管理员配置——管理员登录时自动收到配置错误通知

### 安装模组后僵尸无敌
可能原因：其他模组将感染者 MaxHP 设为极大值（如 1000000），Inedia 生成时将 HP 设为最大值。解决方案：
- 方案一：用 Inedia 的 `DamageToZombieHealthPoints` 直接设 HP（推荐）
- 方案二：禁用 Inedia 伤害处理器 → 使用原版僵尸伤害

### 服务器 FPS 下降
1. 裸测试：仅 InediaInfectedAI + 管理模组 + 服务器 wipe
2. Inedia 对"损坏的服务器"很敏感——其他模组的全局变量破坏可能导致 Inedia 参数随机化（如气味半径被设为 1km）
3. 通常 wipe 服务器能解决
4. 检查是否设置了过大的气味检测球半径或玩家气味半径

### Boss/突变体流血致死
- 方案一：`BloodHandlerIsActive` = 0（完全禁用流血，但无血溅/血泊效果）
- 方案二：`BloodVolumeMl` = 极高值（如 1000000）→ 流血但不死
- 方案三：`BloodLossRateMaxMl` = 低值（如 5~10）→ 流血很慢

### Boss/突变体受攻击/速度减益
- 方案一：`InjuryHandlerIsActive` = 0
- 方案二：`InjuryHandlerDamageThresholdToInjury(Arm/Leg)` = 高值（如 500/1000）

### 钥匙卡门被感染者破坏或静音开门
Inedia 支持以下钥匙卡模组的自动排除：DNA Keycards, Custom Keycards, KeyCard-Rooms, Banov, DeerIsle, Sakhal。

其他模组需要手动配置：
- 破坏排除：`BreakingDoorsRestrictedDoors` 添加建筑类名
- 静音开门排除：`QuietDoorOpeningMechanicRestrictedBuildings` 添加建筑类名

### 感染者对消音器射击反应过度
1. 区分是 Inedia 刺激物还是原版刺激物触发（参见 [9.9](#99-原版刺激物与-inedia-刺激物的关系)）
2. 调整 `ReactVanillaMindstateChange` 限制原版搜索半径
3. 调整 `SuppressorShotCooldownSeconds` 控制消音器机制

### 让感染者对玩家噪音不那么敏感
- 调整 `Players.NoiseMultiplier*`（原版噪音倍率，仅影响原版噪音）
- 调整 `Zombies.ReactFootsteps*`（Inedia 脚步声反应，独立于原版）
- 使用 `ReactHandlerIsActive` = 0 禁用所有 Inedia 刺激物反应（但保留了原版反应）

### PVEZ 等伤害修改模组冲突
Inedia 影响玩家对玩家的伤害（如受伤手臂的玩家拳击伤害降低）。冲突会导致玩家无法被击杀等问题。

解决方案：对 `SurvivorBase` 类禁用 `DamageToPlayerHandlerIsActive`。

---

## 11. 管理员命令快速参考

配置文件: `%DayZserverDir%/profiles/Inedia/InediaAdminsConfig.json`

SteamID 必须是**字符串**格式。

| 命令 | 功能 |
|------|------|
| `/ireload` | 重载配置文件，无需重启服务器 |
| `/idebug dmg` | 伤害调试模式 |
| `/idebug irr` | 刺激物调试模式 |
| `/idebug search` | 搜索球可视化（仅 DayZDiag） |
| `/idebug smells` | 气味可视化（仅 DayZDiag） |
| `/idebug stop` | 停止所有调试器 |
| `/ihide [player]` | 隐藏模式（生物看不到/听不到玩家） |
| `/igm [player]` | 上帝模式（无敌） |
| `/iheal [player]` | 治愈玩家（包括 Inedia 特殊debuff） |
| `/irep [player]` | 修复所有物品到完好 |
| `/iday` / `/inight` | 切换白天/夜晚 |
| `/irain <0-100>` | 设置降雨强度(%) |
| `/isnow <0-100>` | 设置降雪强度(%) |
| `/iwind <0-20>` | 设置风速(m/s) |
| `/izmb [距离] [数量]` | 生成随机低等级感染者 |
| `/izmbm [距离] [数量]` | 生成医疗感染者 |
| `/izmbs [距离] [数量]` | 生成军事感染者 |
| `/iwolf [距离] [数量]` | 生成狼 |
| `/ibear [距离] [数量]` | 生成熊 |
| `/iclear [半径]` | 清除范围内所有生物/物品/车辆 |

---

## 12. 模组兼容性

InediaInfectedAI 支持与以下模组的自动兼容：

| 模组 | 兼容类型 |
|------|----------|
| DNA Keycards | 钥匙卡门保护（自动排除） |
| Custom Keycards | 钥匙卡门保护（自动排除） |
| KeyCard-Rooms | 钥匙卡门保护（自动排除） |
| Banov | 地图门保护（自动排除） |
| DeerIsle | 地图门保护（自动排除） |
| Sakhal | 地图门保护（自动排除 Land_WarheadStorage_Main 全部门） |
| PvZ / PvZ DarkHorde | 有专门的兼容性指南 |
| Syberia Project (1.0) | 有专门的兼容性指南 |
| TerjeMods (Syberia 2.0) | 有专门的兼容性指南 |
| DayZ-Expansion-AI | 通过 FriendlyNPC 参数协调 |

对于 TerjeMods/Syberia 2.0 的医学系统兼容性，请参考官方 Wiki 专门的兼容性页面。

---

> **版权声明:** InediaInfectedAI 由 [johnkind](https://steamcommunity.com/id/johnkind/) 开发。
> 本文档内容来源于 [官方 GitHub Wiki](https://github.com/ysaroka/InediaInfectedAI/wiki)，仅供本服务器配置参考使用。
> 抓取日期: 2026-07-08 | 包含页面: Description, Configuration Guide, FAQ, Pain System Guide, Medicine Guide
