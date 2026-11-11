# MPG_Spawner 1.4 完整文档

> **来源:** [https://docs.mpg-dayz.ru/spawner/](https://docs.mpg-dayz.ru/spawner/)
> **爬取日期:** 2026/06/22
> **文档语言:** 俄文原文已翻译为中文，关键字段名保留英文以便对照代码
> **本服务器适用:** 所有 Deerisle 副本（巴黎堡垒、恶魔岛、石螺、北极神庙、地下监狱、玑迷、水牢、隧道、海峡、山谷、Oilrig4、Lab、海上航母、Lance、海下航母、Milo、SEUG、地铁）共 18 个副本均由本模组驱动

---

## 目录

1. [简介与功能概览](#1-简介与功能概览)
2. [安装方式](#2-安装方式)
3. [模组主配置 (`Config.json`)](#3-模组主配置-configjson)
4. [触发点配置 (`Points/*.json`)](#4-触发点配置-pointsjson)
   - [4.1 标识与调试](#41-标识与调试字段)
   - [4.2 通知系统](#42-通知系统)
   - [4.3 触发器依赖与联动](#43-触发器依赖与联动)
   - [4.4 触发器几何形状与位置](#44-触发器几何形状与位置)
   - [4.5 时序参数（延迟/冷却/排班）](#45-时序参数延迟冷却排班)
   - [4.6 清理与去活逻辑](#46-清理与去活逻辑)
   - [4.7 生成位置与生成参数](#47-生成位置与生成参数)
   - [4.8 生成列表 `spawnList`（核心）](#48-生成列表-spawnlist核心)
   - [4.9 死尸清理时间](#49-死尸清理时间)
   - [4.10 地图建筑 mapping](#410-地图建筑-mappingdata)
5. [与其它 Spawn 模组的功能对比](#5-与其它-spawn-模组的功能对比)
6. [实用调参速查](#6-实用调参速查)
7. [代码编辑规范（强制遵守）](#7-代码编辑规范强制遵守)

---

## 1. 简介与功能概览

**MPG_Spawner** 是一款**纯服务端模组**，通过 JSON 配置文件灵活定义"非标准刷新点"，可同时管理**动物**和**僵尸（感染者）**的刷新。

### 主要功能

- ✅ 同时正确处理动物与僵尸
- ✅ 可加载多个配置文件（每个文件管理一组触发器）
- ✅ 触发器可视化（需配套客户端模组 `@MPG_spawn_zone`）
- ✅ 进入触发器时弹出通知
- ✅ 离开/生成完成时弹出通知
- ✅ 触发器之间可设置"依赖关系"（必须先触发 A 才能激活 B）
- ✅ 可"或"逻辑依赖（A 或 B 触发后即激活 C）
- ✅ 触发器自动贴地放置
- ✅ 触发器形状支持：**球体 / 圆柱 / 长方体**（可水平旋转）
- ✅ 首次触发延迟、进入后延迟生成
- ✅ 按"游戏内时间"排班（如 8 点～18 点生效）
- ✅ 单个触发器内多个生成点
- ✅ 独立日志文件 + 日志归档
- ✅ 单触发器独立调试开关
- ✅ 最小/最大生成数量
- ✅ 玩家停留期间可循环重生
- ✅ 可旋转生成体
- ✅ 可设定生命周期（lifetime）和血量
- ✅ 单触发器活体数量上限
- ✅ 自定义动物/僵尸死亡后清除时间
- ✅ 每个 classname 设置独立生成几率
- ✅ 最小生成距离（避免在玩家脸上刷出）
- ✅ 已停用的触发器可被其它触发器激活
- ✅ 玩家离场或排班时间结束时清空所有生成体
- ✅ 灵活的 mapping（场景建筑）添加/删除
- ✅ **可生成战利品（loot）**，并设置 lifetime、弹匣装填、水量、食物腐败、损耗等

---

## 2. 安装方式

服务端模组——**客户端无需安装**。从 Steam 创意工坊下载放入服务器启动行即可。

> 首次启动服务器时模组会自动生成 JSON 配置文件，之后再去编辑。

---

## 3. 模组主配置 `Config.json`

位置：`profiles/MPG_Spawner/Config.json`

```jsonc
{
    "configVersion": 4,
    "documentation": "https://docs.mpg-dayz.ru/spawner/",
    "isModDisabled": 0,
    "isDebugEnabled": 0,
    "pointsConfigs": [ "1_ParisBunker", "2_Alcatraz", ... ],
    "admins": [ "YOUR_STEAM64_ID", "YOUR_STEAM64_ID" ]
}
```

| 字段 | 含义 |
| --- | --- |
| `configVersion` | 配置版本号。**服务字段，不要手动改**，更新模组时自动维护。 |
| `documentation` | 文档链接，服务字段。 |
| `isModDisabled` | 整模启用/禁用开关。`0`=启用，`1`=禁用。 |
| `isDebugEnabled` | 调试开关。开启后日志会输出大量调试信息，对所有触发点生效。 |
| `pointsConfigs` | **关键字段**。数组，列出 `Points/` 文件夹下要加载的 JSON 文件名（不带 `.json` 后缀）。本服务器列出了 18 个副本配置。 |
| `admins` 1.4 | 管理员 SteamID64 列表，允许使用管理指令。 |

---

## 4. 触发点配置 `Points/*.json`

> **命名建议**：文件名以 ID 起始数字开头，如 `1_myTriggers.json`（容纳 ID 1-499）、`500_myOtherTriggers.json`、`1000_myMoreTriggers.json`。便于管理 pointId 命名空间。

### 4.1 标识与调试字段

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `pointId` | int | **触发器唯一 ID**，不能重复，可任意整数（上限 `2147483647`）。 |
| `isDebugEnabled` | 0/1 | 单触发器调试开关，开后日志详细输出该触发器全过程。 |
| `isDisabled` | 0/1 | 初始禁用。**⚠ 禁用后将完全不与玩家交互**：不显示通知、不工作 mapping（除 startup 一次性 mapping）、不生成。 |
| `showVisualisation` | 0/1 | 显示半透明触发器形状（需要客户端模组 `@MPG_spawn_zone`，调试用）。 |

### 4.2 通知系统

| 字段 | 说明 |
| --- | --- |
| `notificationTitle` | 触发点名称（在日志/通知头部使用），如 `"Точка 3"` 或 `"巴黎堡垒"`。 |
| `notificationTextEnter` | 玩家进入触发器时显示的文本。**只要点未禁用，必定推送**。留空 `""` 即关闭。 |
| `notificationTextExit` | 玩家离开触发器时显示。留空关闭。 |
| `notificationTextSpawn` | 生成体出现时全场内玩家收到。**支持词形变化占位符**。 |
| `notificationTextWin` | 触发器内所有生成体被击杀时显示。 |
| `notificationTime` | 通知显示秒数。 |
| `notificationIcon` | 通知图标，可使用游戏内已注册的 icon set 或图片路径。 |

#### 通知文本的占位符（俄语词形变化用，中文可忽略复杂句法）

- 分隔符 `;`：第一部分是带占位符的主文本，后续为词形变体。
- `%1` = 生成数量；`%2`-`%5` = 后续词形变体。
- 词干和词尾用 `|` 分隔：`"волк||а|ов"` → (1, 2, 5) → `волк, волка, волков`。

中文情境下一般用简单文案即可：`"notificationTextSpawn": "警告：附近出现敌人！"`。

```jsonc
"notificationIcon": "set:dayz_inventory image:electricity",
"notificationIcon": "set:dayz_inventory image:woodcrate",
"notificationIcon": "set:dayz_gui image:iconSkull"
```

### 4.3 触发器依赖与联动

| 字段 | 说明 |
| --- | --- |
| `triggerDependencies` | 当前触发器所依赖的其它触发器 ID 列表。**只有列表中所有触发器都已触发，当前才会激活**。 |
| `triggerDependenciesAnyOf` | `1` 时，将 `triggerDependencies` 改为"或"逻辑——只要其中**任意一个**触发即激活。 |
| `triggersToEnableOnEnter` | 当前触发器被玩家进入时，激活的其它触发器 ID 列表。 |
| `triggersToEnableOnFirstSpawn` | 当前触发器**首次生成**生效时激活的其它 ID 列表。 |
| `triggersToEnableOnWin` | 当前触发器内所有生成体被击杀时激活的其它 ID。 |
| `triggersToEnableOnLeave` | 所有玩家离开当前触发器后激活的其它 ID。 |

> 典型用法：实现"必须先击杀外圈僵尸 → 才解锁内圈 boss 区域"、"多个入口任一进入即开启整个副本"。

### 4.4 触发器几何形状与位置

| 字段 | 说明 |
| --- | --- |
| `triggerPosition` | 触发器坐标 `"x y z"` 或 `"x y z\|yaw 0 0"`（仅水平旋转）。若 y=0.0，自动贴地。 |
| `triggerDebugColor` | 调试可视颜色：`blue`(默认)/`green`/`red`/`yellow`。 |
| `triggerRadius` | 触发器半径（米）。可写区间 `"5.5-20.0"`，每次服务器重启随机。 **⚠ 不要超过 500 m**，否则多玩家同时进入时服务器压力骤增。 |
| `triggerHeight` | 高度（米）。`"0"` = 球形；指定数值 = 圆柱/长方体。支持 `"2.5-5.6"` 区间。 |
| `triggerWidthX` | 长方体 X 轴长度。指定后变为长方体。支持区间。 |
| `triggerWidthY` | 长方体 Y 轴长度。**同时指定 X、Y 时，`triggerRadius` 被忽略**，触发器变成长方体。 |

> **⚠ 禁忌**：不要让触发器互相嵌套（"套娃"）或大面积重叠，DayZ 引擎会因无法正确判定玩家归属而显著加重服务器负载。

### 4.5 时序参数（延迟/冷却/排班）

| 字段 | 说明 |
| --- | --- |
| `triggerFirstDelay` | 服务器启动后**首次触发**前的等待秒数。**官方建议 180-300 秒以上**——给玩家逃离危险区的时间，也减轻服务器开服压力。支持区间 `"300-900"`。 |
| `triggerCooldown` | 两次触发间冷却秒数。支持区间 `"2400-3600"`（每次随机），使重生时间难以预测。 |
| `triggerSafeDistance` | 进入触发器时，生成体距离玩家的**最小距离**（米）。仅在玩家"进入"时生效。如果 > `spawnRadius + 1m` 则该参数被忽略（防止服务器在不可达坐标上尝试 spawn）。 |
| `triggerEnterDelay` | 玩家**首次**进入触发器到生成发生之间的延迟秒数（仅对第一个进入者）。 |
| `triggerWorkingTime` | 按**游戏内时间**排班。`"0-24"` 全天，`"8-18"` 仅 8 点到 18 点生效。 |

### 4.6 清理与去活逻辑

| 字段 | 说明 |
| --- | --- |
| `triggerCleanupImmersive` 1.3 | `1` 时，移除生成体不是凭空消失——先"杀死"，2 秒后尸体消失（让死亡动画完成播放）。 |
| `triggerCleanupOnLeave` | `1` 时，最后一个玩家离开触发器后清空所有生成体和战利品（玩家已捡的不删）。 |
| `triggerCleanupOnLunchTime` | `1` 时，按 `triggerWorkingTime` 排班结束时清空所有生成体。 |
| `triggerCleanupDelay` | 清理操作的延迟秒数（仅 `OnLeave` 或 `OnLunchTime` 触发时生效）。 |
| `triggerInactiveResetDelay` 1.4 | 不活跃秒数。当生成体在指定时间内未受到任何伤害（玩家进了又走没打），触发器重置回服务器启动时的状态、生成体被移除。**很适合放在多怪场景，避免玩家'踩一下就跑'造成的资源积压**。 |
| `triggerDisableOnWin` | `1` = 全部击杀后永久停用该触发器。 |
| `triggerDisableOnLeave` | `1` = 玩家全部离开后永久停用。 |

### 4.7 生成位置与生成参数

| 字段 | 说明 |
| --- | --- |
| `spawnPositions` | 生成点坐标数组。格式同 `triggerPosition`：`"x y z"` 或 `"x y z\|yaw 0 0"`。y=0 = 贴地。**一个触发器可有多个生成点**。 |
| `spawnRadius` | 围绕每个 `spawnPositions` 坐标的生成半径。`0.0` = 精确点位；`>0` = 半径内随机。**⚠ 半径太小 + 数量太大会导致生成体相互卡住、服务器负载升高**。 |
| `spawnMin` | 单次触发最少生成数量。可为 `0`（即不生成）。 |
| `spawnMax` | 单次触发最大生成数量。不要 < 1。 |
| `spawnCountLimit` | 全局活体上限（无视 min/max），达到后不再生成，直到当前生成体被击杀。`0` = 无上限。 |
| `spawnLoopInside` | `1` = 玩家在触发器内时允许循环重生；`0` = 必须离开后再进才能触发。 |
| `spawnQueueDelay` 1.4 | 列表中各元素的**生成间隔（毫秒）**。如 `1000` = 每秒生成 1 个（10 只熊 = 10 秒分批刷出）。**不影响** firstDelay/cooldown/enterDelay。 |

### 4.8 生成列表 `spawnList`（核心）

> **核心字段**。支持 **动物、僵尸、战利品** 混合刷新。

#### 参数语法

```
"classname | 生成几率 | lifetime | 数量 | 血量 | 食物状态"
```

| 位置 | 参数 | 取值 |
| --- | --- | --- |
| 1 | classname | DayZ 物品类名 |
| 2 | 生成几率 | `0.0-1.0`（0.7 = 70%） |
| 3 | lifetime | 经济寿命秒数 |
| 4 | 数量 | 弹匣弹数/水量/食物份数等 |
| 5 | 血量 | 见特殊取值 |
| 6 | 食物状态 | 见特殊取值 |

#### 特殊取值

| 数值 | 含义 |
| --- | --- |
| `-3` | 关闭（使用经济系统默认值） |
| `-2` | 完全随机（0-100%；食物状态= Pristine/Worn/Damaged/Badly Damaged/Ruined 五档随机；食物腐败= 腐烂/烘干/生鲜三档随机） |
| `-1` | 最大值（食物=新鲜，其他=100%） |
| `0-100` | 百分比区间，区间内随机 |

> **动物 / 僵尸只生效：生成几率、lifetime、血量**。数量、食物状态对它们无意义。
> 缺省参数等价于 `-3`，可省略尾部。

#### 实战示例

```jsonc
"spawnList": [
    // 基础写法 — 默认 100% 几率
    "ZmbM_ConstrWorkerNormal_Beige",
    "Animal_UrsusArctos",

    // 70% 几率刷出该女僵尸
    "ZmbF_MechanicNormal_Beige | 0.7",

    // 30% 几率刷狼
    "Animal_CanisLupus_Grey | 0.3",

    // 熊：100% 几率，血量 0.1%~1%（即 3-8 HP，残血秒杀型）
    "Animal_UrsusArctos | 1 | -3 | -3 | 0.1-1",

    // 重度损坏 + 腐烂的苹果
    "Apple | 1 | -3 | -3 | 30-30 | 30-30",

    // 全随机水瓶（除 lifetime 外）
    "WaterBottle | 1 | -2 | -2 | -2 | -2",

    // 50%几率弹匣 / 120秒lifetime / 9-18发 / 重度损坏到磨损
    "Mag_AK101_30Rnd | 0.5 | 120 | 30-60 | 10-67",

    // 武器 — 只有最后一个状态生效（武器无"数量"概念）
    "AKM | 1 | -3 | -2 | -1"
]
```

### 4.9 死尸清理时间

| 字段 | 说明 |
| --- | --- |
| `clearDeathAnimals` | 动物尸体保留秒数。 |
| `clearDeathZombies` | 僵尸尸体保留秒数。 |

### 4.10 地图建筑 `mappingData`

为副本动态添加/移除建筑物（如临时围墙、灯塔、宝箱）。

#### 事件标志位

- `addOnStartup` — 服务器启动时添加
- `addOnEnter` — 玩家首次进入时添加
- `addOnFirstSpawn` — 首次生成发生时添加
- `addOnWin` — 击杀全部生成体时添加
- `addDelay` — 添加延迟（秒）
- `removeOnEnter` / `removeOnFirstSpawn` / `removeOnWin` — 对应事件触发时移除
- `removeDelay` — 移除延迟（秒）
- `mappingObjects` — 对象数组，**完全兼容 DayZ-Editor 导出的 vanilla json 格式**

> ⚠ **同事件冲突**：不能在同一事件上同时"添加+移除"，否则不会移除。
> ⚠ 仅支持 classname 物体，**不能放 .p3d 文件**。

#### 示例（节选）

```jsonc
"mappingData": [
    {
        "addOnStartup": 1,
        "addOnFirstSpawn": 0,
        "addOnWin": 0,
        "addDelay": 0.0,
        "removeOnFirstSpawn": 1,
        "removeDelay": 0.0,
        "mappingObjects": [
            {
                "name": "Land_Sawmill_Illuminanttower",
                "pos": [2185.56, 208.08, 5444.35],
                "ypr": [74.0, 0.0, 0.0],
                "scale": 1,
                "enableCEPersistency": 0
            }
        ]
    },
    {
        "addOnWin": 1,
        "mappingObjects": [
            {
                "name": "SeaChest",
                "pos": [2111.29, 197.57, 5439.36],
                "ypr": [0, 0, 0],
                "scale": 1.0,
                "enableCEPersistency": 0
            }
        ]
    }
]
```

第一段：开服时就放灯塔，**首次生成时移除**。
第二段：**通关后**奖励一个 SeaChest 宝箱。

---

## 5. 与其它 Spawn 模组的功能对比

| 功能 | ZombieSpawnTool | SpawnerBubaku | **MPG_Spawner** |
| --- | --- | --- | --- |
| 动物 & 僵尸都正确处理 | 🔲 | 🔲 | 🟩 |
| 多配置文件 | 🔲 | 🟨 (随机选一) | 🟩 |
| 触发器可视化调试 | 🔲 | 🔲 | 🟩 |
| 进入通知 | 🔲 | 🟨 (仅 debug) | 🟩 |
| 出/生成通知 | 🔲 | 🔲 | 🟩 |
| 触发器依赖关系 | 🔲 | 🟩 | 🟩 |
| 自动贴地 | 🟩 | 🔲 | 🟩 |
| 圆柱触发器 | 🔲 | 🟩 | 🟩 |
| 长方体触发器 | 🔲 | 🟩 | 🟩 |
| 重启随机大小 | 🔲 | 🔲 | 🟩 |
| 随机首次延迟 | 🔲 | 🔲 | 🟩 |
| 随机冷却 | 🔲 | 🔲 | 🟩 |
| 首次触发延迟 | 🟩 | 🔲 | 🟩 |
| 进入后延迟 | 🔲 | 🔲 | 🟩 |
| 按游戏时间排班 | 🔲 | 🟩 | 🟩 |
| 多生成点 | 🟩 | 🔲 | 🟩 |
| 独立日志/归档 | 🔲 | 🟩 | 🟩 |
| 单触发器 debug | 🔲 | 🔲 | 🟩 |
| 击杀僵尸后掉落 | 🟩 | 🔲 | 🟨 (用 mapping/联动触发器) |
| 击杀动物后掉落 | 🔲 | 🔲 | 🟨 (用 mapping/联动触发器) |
| min/max 生成数量 | 🟩 | 🔲 | 🟩 |
| 玩家停留时重生 | 🟩 | 🔲 | 🟩 |
| 生成体旋转 | 🔲 | 🟩 | 🟩 |
| 活体上限 | 🔲 | 🟩 | 🟩 |
| 僵尸死亡掉落配置 | 🔲 | 🟩 | 🔲 |
| 僵尸服装配置 | 🟩 | 🔲 | 🔲 |
| 死亡尸体清除时间 | 🔲 | 🔲 | 🟩 |
| 每 classname 几率 | 🔲 | 🟨 | 🟩 |
| 玩家最小生成距离 | 🟩 | 🟨 | 🟩 |
| "或"依赖逻辑 | 🔲 | 🔲 | 🟩 |
| 可激活已停用触发器 | 🔲 | 🔲 | 🟩 |
| 击杀后停用触发器 | 🔲 | 🔲 | 🟩 |
| 离开后停用触发器 | 🔲 | 🔲 | 🟩 |
| 离场清空生成体 | 🔲 | 🔲 | 🟩 |
| 排班结束清空 | 🔲 | 🔲 | 🟩 |
| Mapping 启动添加 | 🔲 | 🔲 | 🟩 |
| Mapping 进入添/删 | 🔲 | 🔲 | 🟩 |
| Mapping 胜利添/删 | 🔲 | 🔲 | 🟩 |
| Mapping 首生成添/删 | 🔲 | 🔲 | 🟩 |
| Mapping 延迟 | 🔲 | 🔲 | 🟩 |
| 战利品 + 血量/lifetime/数量 | 🔲 | 🔲 | 🟩 |
| 列表分批生成（队列延迟） | 🔲 | 🔲 | 🟩 |
| 沉浸式去尸（先杀再清） | 🔲 | 🔲 | 🟩 |

**结论**：MPG_Spawner 在动态副本编排能力上**全面领先**两款竞品，这也是本服选它驱动 18 个副本的原因。

---

## 6. 实用调参速查

### 6.1 想"提高副本难度"

| 改这里 | 效果 |
| --- | --- |
| 增加 `spawnMin` / `spawnMax` | 单次生成数量↑ |
| 增加 `spawnCountLimit` | 同时活体上限↑（副本压力↑） |
| 降低 `triggerCooldown` 下限 | 重生更快 |
| 在 `spawnList` 中加入更强的 classname | 火力↑ |
| 启用 `spawnLoopInside: 1` | 玩家停留期间持续刷新 |
| `triggerSafeDistance` 设小 | 怪物贴脸生成更突然 |

### 6.2 想"降低服务器负载"

| 改这里 | 效果 |
| --- | --- |
| 增加 `spawnQueueDelay`（如 500-1000ms） | 分批刷出，避免瞬时尖峰 |
| 启用 `triggerInactiveResetDelay` | 防止玩家踩一下就跑造成的资源沉积 |
| 启用 `triggerCleanupOnLeave: 1` + 合适 `triggerCleanupDelay` | 玩家走后释放怪物 |
| `triggerFirstDelay` 设为 180-300s 以上 | 减轻开服后压力 |
| 减小 `triggerRadius`，避免 >500m | 避免大半径下大量玩家在内 |
| 不让多个触发器嵌套/重叠 | 引擎不会反复判定 |

### 6.3 想"实现剧情/解锁式副本"

- 用 `triggerDependencies` + `triggersToEnableOnWin` 串成**线性章节**。
- 用 `triggerDependenciesAnyOf: 1` 做**多入口副本**。
- 用 `mappingData.addOnWin` 在通关后投放奖励箱。
- 用 `triggersToEnableOnFirstSpawn` 触发"敌人出现 → 锁门"机制。

### 6.4 想"做战利品房间（无僵尸）"

- `spawnList` 全部填战利品 classname，写法 `"AKM | 0.3 | -3 | -2 | -1"`。
- 启用 `triggerCleanupOnLeave: 1` 防止玩家屯刷。
- 配合 `triggerCooldown` 设大冷却（如 1800-3600s）做"几小时刷新一次的彩蛋房"。

### 6.5 想"白天/夜晚不同的副本"

用 `triggerWorkingTime`：
- 夜晚版本副本：`"triggerWorkingTime": "20-6"`（晚 8 点～早 6 点）
- 白天版本副本：`"triggerWorkingTime": "6-20"`

可在同一坐标布置两个不同 `pointId` 的触发器、错开排班即可。

---

## 附录：本服 18 个副本配置文件

详见 `Config.json` 中的 `pointsConfigs`：

```
1_ParisBunker           — 巴黎堡垒
2_Alcatraz              — 恶魔岛
3_ShiLuo                — 石螺
4_ArcticTemple          — 北极神庙
5_UGPrison              — 地下监狱
6_JiMi                  — 玑迷
7_ShuiLao               — 水牢
8_Tunnel                — 隧道
9_HaiXia                — 海峡
10_Valley               — 山谷
11_Oilrig4              — 海上石油平台
12_Lab                  — 实验室
13_HeliCarrierSurface   — 海上航母（甲板）
14_Lance                — Lance
15_HeliCarrierUnder     — 海下航母（舱内）
16_Milo                 — Milo
17_SEUG                 — SEUG
18_Subway               — 地铁
```

每个副本独立一个 JSON 文件，统一放在 `profiles/MPG_Spawner/Points/` 文件夹下。要调整某副本的丧尸刷新机制，直接编辑对应文件即可。

---

## 7. 代码编辑规范（强制遵守）

以下规则适用于对 `profiles/MPG_Spawner/Points/*.json` 文件的任何修改。**违反任一条即视为无效修改，必须回滚重做。**

### 7.1 字段完整性

- **禁止删除任何字段。** 每个 pointId 对象在文件中定义的所有字段必须完整保留。当前每个 pointId 包含 32 个字段（从 `pointId` 到 `mappingData`），一个都不能少。
- **禁止跳行、漏行。** 修改时只替换目标字段的值，不删除、不插入、不重排任何行。
- **禁止新增字段。** 除 `spawnList` 条目外，不得向 pointId 对象添加文档未记载的字段。

### 7.2 允许修改的字段（白名单）

| 字段 | 说明 | 修改约束 |
|---|---|---|
| `spawnList` | 生成实体 classname 数组 | 仅使用 `"classname"` 裸字符串，**禁止**使用 `"classname\|几率"` 管道语法。用重复列出控制权重。 |
| `spawnMin` | 单次最小生成数量 | 整数。多 spawnPositions 时按位置数等比例缩放 |
| `spawnMax` | 单次最大生成数量 | 整数。同上缩放 |
| `spawnCountLimit` | 活体上限 | 整数。同上缩放 |

**禁止修改的字段（黑名单）**：

`pointId`, `isDebugEnabled`, `isDisabled`, `showVisualisation`, 所有 `notification*` 字段, `triggerDependencies*`, `triggersToEnable*`, `triggerPosition`, `triggerDebugColor`, `triggerRadius`, `triggerHeight`, `triggerWidth*`, `triggerFirstDelay`, `triggerCooldown`, `triggerSafeDistance`, `triggerEnterDelay`, `triggerCleanup*`, `triggerInactiveResetDelay`, `triggerWorkingTime`, `triggerDisable*`, `spawnPositions`, `spawnRadius`, `spawnLoopInside`, `spawnQueueDelay`, `clearDeath*`, `mappingData`

> **特别强调**：`triggerFirstDelay`（服务器启动后等待 navmesh 加载）和 `triggerCooldown`（防止同一副本内重复刷新）**绝对不能改动**。它们由服务器管理员按全局经验值设定，不在难度调整范围内。

### 7.3 格式规范

- **缩进**：4 空格。与源文件严格一致，禁止使用 Tab、2 空格或任何其他缩进。
- **JSON 合法性**：修改后文件必须能通过 `json.load()` 解析，不允许尾逗号、缺失引号等语法错误。
- **文件末尾**：必须有一个换行符 `\n`。
- **编码**：UTF-8 without BOM。

### 7.4 multi-spawnPos 缩放规则

当一个 pointId 的 `spawnPositions` 数组包含多个坐标时，`spawnMin`、`spawnMax`、`spawnCountLimit` 必须按位置数量等比例缩放：

```
修改后的值 = 梯队基准值 × spawnPositions 数量
```

例如：黄卡基准 `spawnMin=7, spawnMax=12, limit=24`，某触发点有 3 个 spawnPositions → 设为 `21, 36, 72`。

### 7.5 spawnList 编写规则

#### 7.5.1 基本规则：裸 classname（默认 100% 几率）

每个条目为纯字符串 `"ZmbM_ClassName"`。不写管道参数时，MPG 默认该条目的"生成几率"为 `1.0`（即 100%——每次被选中必定生成）。

**权重通过重复控制**：若某 classname 需 3 倍出现概率，将其列出 3 次。条目顺序不影响选择概率。

#### 7.5.2 管道语法：精确控制单实体几率（`|` 分隔符）

MPG 支持通过 `|` 为每条目附加参数，语法为：

```
"classname | 生成几率 | lifetime | 数量 | 血量 | 食物状态"
```

| 位置 | 参数 | 类型 | 说明 |
|:---:|---|---|---|
| 1 | classname | string | DayZ 实体类名 |
| 2 | **生成几率** | `0.0 ~ 1.0` | 该条目被选中后的**实际生成通过率**。`0.08` = 8% |
| 3 | lifetime | int / `-3` | 经济寿命（秒），`-3`=使用默认 |
| 4 | 数量 | int / `-3` | 对动物/僵尸无意义，省略 |
| 5 | 血量 | `-3`/`-2`/`-1`/`0-100` | `-3`=使用 Inedia 设置 |
| 6 | 食物状态 | `-3`/`-2`/`-1`/`0-100` | 对动物/僵尸无意义 |

> 对动物/僵尸只生效：**生成几率、lifetime、血量**。其余参数设为 `-3` 或省略。

#### 7.5.3 生成几率的底层机制（关键）

MPG 每生成一个实体时执行以下流程：

1. 从 `spawnList` 数组中**随机选一个条目**
2. 对该条目投骰子，比对 `生成几率`（默认 `1.0` = 100%）
3. **投过了** → 以该 classname 生成此实体
4. **没投过** → 重新随机选一个条目，重复步骤 2
5. 所有条目都连续没投过 → **此生成槽位浪费，实际生成数可能少于 `spawnMin`**

**核心含义**：`| 0.08` 不是"该 classname 占 8% 权重"，而是"每当该条目被抽中时，只有 8% 的概率真正生成它"。

这意味着：
- 一个 spawnList 包含 27 条裸 classname（各 100%）+ 1 条 `"NYFreezingMutant | 0.08"`
- 每轮抽到 FreezingMutant 的概率 ≈ 1/28 ≈ 3.6%
- 抽到后只有 8% 通过率 → **有效生成概率 ≈ 3.6% × 8% ≈ 0.29%**
- 以 spawnMax=14 计算：期望值 ≈ 14 × 0.29% = 0.04 只/次
- **95%+ 的触发器激活中不会出现该实体，偶尔出现 1 只**

#### 7.5.4 管道语法的使用约束

- **允许使用的场景**：需要将某个强力实体（如 NYFreezingMutant）的生成频率精确控制在"偶尔 1 只"级别时，使用 `| 极低几率`（如 `0.05 ~ 0.10`）。
- **禁止使用的场景**：常规填充型丧尸和普通特技丧尸仍然使用裸 classname + 重复列出来控制权重，不得滥用管道语法。
- **强制汇报**：**每次计划使用管道语法前，必须先向用户解释：① 原因（为什么需要精确控制）② 目标几率 ③ 预期效果（期望生成次数 + 出现概率），经用户确认后方可执行。**
- **禁止使用不在 `zmb_types.xml` 或模组中注册的 classname**。

#### 7.5.5 示例对比

```jsonc
// 常规写法 — 27 条裸 classname，各 100% 几率，权重靠重复控制
"spawnList": [
    "SMCS_Snork_Hard",
    "SMCS_Snork_Hard",          // 出现 2 次 = 2 倍权重
    "AP_zmb_kamikaze",
    "AP_zmb_kamikaze",
    "AP_zmb_kamikaze"            // 出现 3 次 = 3 倍权重
]

// 精确几率控制 — Freezing 仅 1 条，但 | 0.08 限制其通过率
"spawnList": [
    "SMCS_Snork_Hard",
    "SMCS_Snork_Hard",
    "AP_zmb_kamikaze",
    "AP_zmb_kamikaze",
    "AP_zmb_kamikaze",
    "NYFreezingMutant | 0.08"    // 选中后仅 8% 概率真正生成
]
```

### 7.6 修改前检查清单

- [ ] 已用 `Read` 工具完整读取目标文件，确认其当前结构和所有字段值
- [ ] 明确该副本所属梯队（黑/蓝/绿/黄/红/噩梦）及其对应的 spawnList 模板和数字基准
- [ ] 确认每个 pointId 的 `spawnPositions` 数量，需要缩放的点已计算缩放系数
- [ ] 修改后已用 Python `json.load()` 验证 JSON 合法性
- [ ] 已逐 pointId 验证 `spawnMin/spawnMax/spawnCountLimit` 值 = 基准 × 缩放系数
- [ ] 已逐 pointId 验证 `spawnList` 内容与模板完全一致（长度 + 每个条目）
- [ ] 已抽查 `triggerFirstDelay`、`triggerCooldown`、`triggerPosition` 确认未被修改

### 7.7 禁止行为

- ❌ 用手工逐行编辑替代 Python `json.load/dump` 批量修改（手工易出错、易漏字段）
- ❌ 修改后不验证直接提交
- ❌ 跨梯队混用 spawnList 模板
- ❌ 修改白名单之外的任何字段
- ❌ 改动文件缩进风格
- ❌ 删除或注释掉任何 field
- ❌ 未经用户确认擅自使用 `|` 管道几率语法（见 7.5.4 强制汇报规则）
