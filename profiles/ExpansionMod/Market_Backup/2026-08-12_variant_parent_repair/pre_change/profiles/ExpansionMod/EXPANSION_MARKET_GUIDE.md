# DeerIsle 6.1 — Expansion Market 配置基线与变更日志

> **长期交接文档 / 后续操作前必读**  
> 此文件是本服务器 Expansion Market 的持续维护入口。以后无论切换模型、任务或对话，在修改市场配置前都必须先读本文件；完成任何价格、库存、买卖权限、物品增删或交易商调整后，必须同步更新“当前基线”和文末“变更日志”。

- 基线审计日期：2026-08-11（Asia/Shanghai）
- 审计范围：`profiles/ExpansionMod` 与 `mpmissions/empty.deerisle/expansion`
- 本次审计结果：只创建本文档，**未修改任何市场 JSON、交易商 JSON、区域 JSON 或 `.map` 文件**。
- 重要提醒：`traderzones/*.json` 中的 `Stock` 是运行期数据，会随交易和服务器保存而变化；本文记录的是 2026-08-11 的静态快照。

## 1. 官方资料与本服路径

官方入口：

- [The Market System](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-The-Market-System)
- [General Market Settings](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-General-Market-Settings)
- [Market Categories Settings](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Market-Categories-Settings)
- [Trader Settings](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Trader-Settings)
- [Market TraderZones Settings](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Market-TraderZones-Settings)
- [Adding a new Item](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Adding-a-new-Item-to-the-market)
- [Adding a new Category](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Adding-a-new-Category-to-the-market)
- [Trader Entities and NPCs](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Setting-up-Trader-Entities-and-NPCs)
- [Custom Market Currencies](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Setting-up-Custom-Market-Currencies)
- [Static Stock](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-How-to-make-the-Stock-Static)
- [Common Mistakes](https://github.com/salutesh/DayZ-Expansion-Scripts/wiki/%5BServer-Hosting%5D-Market-Common-Mistakes)

本服实际文件结构：

```text
D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\
├─ Market\                         # 物品目录、价格、库存阈值、物品级出售比例
│  ├─ *.json
│  └─ <模组子目录>\*.json          # 会递归加载
├─ Traders\                        # 交易商可见目录、买卖权限、结算货币
│  └─ *.json
└─ EXPANSION_MARKET_GUIDE.md       # 本文档

D:\OneDrive\Deerisle 6.1\mpmissions\empty.deerisle\expansion\
├─ settings\MarketSettings.json    # 全局市场/ATM/载具生成点设置
├─ traders\*.map                   # NPC/实体放置与 Trader 配置绑定
└─ traderzones\*.json              # 交易区域、区域价格倍率、实时库存
```

## 2. 系统怎样运作

一次交易由四层配置共同决定：

```text
Market/*.json（物品定义、价格和库存阈值）
        ↓ 被 Categories 或 Items 引用
Traders/*.json（该交易商是否展示、允许买/卖、使用什么货币）
        ↓ 由文件名基名绑定
traders/*.map（在地图放置 NPC/实体并绑定 Trader 配置）
        ↓ 必须位于某个区域内
traderzones/*.json（选择该位置的库存池及区域买卖倍率）
        ↓
玩家交易；库存写回对应 TraderZone 的 Stock
```

### 2.1 价格和库存

- `MinPriceThreshold`：库存高时的最低购买价格。
- `MaxPriceThreshold`：库存低时的最高购买价格。
- `MinStockThreshold`：低库存端阈值。
- `MaxStockThreshold`：高库存端阈值。
- 动态库存时，购买价不是简单线性插值；当前官方实现使用 6 次幂曲线，使价格随库存从高到低由 `MinPriceThreshold` 向 `MaxPriceThreshold` 上升。
- 玩家购买会减少区域库存，出售会增加区域库存；静态库存和部分食物状态例外。
- `MinStockThreshold == MaxStockThreshold > 0` 表示静态/无限库存；本服静态库存统一为 `1 / 1`。
- `MinPriceThreshold == MaxPriceThreshold` 表示静态价格。
- `InitStockPercent` 只用于：新建区域库存文件，或该区域 `Stock` 中缺少某个物品记录时的初始化。它不是每次启动都重置库存。
- 若要让某个动态库存物品重新按 `InitStockPercent` 初始化，应在服务器停止后，仅删除对应 TraderZone `Stock` 中该 class 的记录并重启。不要为“调价格”顺手清空整个库存文件。

购买价的概念式：

```text
物品库存曲线价格 × TraderZone.BuyPricePercent / 100
```

出售比例优先级：

```text
物品 SellPricePercent（>= 0）
  > TraderZone.SellPricePercent（>= 0）
  > MarketSettings.SellPricePercent
```

最终出售金额还会受物品状态、剩余数量/容量及食物状态影响。当前官方逻辑中的状态倍率为：Pristine 100%、Worn 75%、Damaged 50%、Badly Damaged 25%、Ruined 0%；部分消耗品还按剩余量折算。

> **版本差异提醒：** 官方 Wiki 的旧示例曾把 `SellPricePercent` 描述成 0.0–1.0，但当前 Expansion 源码和本服配置使用 **0–100 的百分数**，计算时除以 100。本服后续修改必须按当前格式理解，例如 `20` = 20%，而 `0.2` = 0.2%。

### 2.2 Market 分类文件参数

| 参数 | 含义与维护规则 |
|---|---|
| `m_Version` | Expansion 内部配置版本，禁止手动修改。 |
| `DisplayName` | 市场 UI 分类名，可用本地化键。 |
| `Icon` / `Color` | 分类图标与颜色。 |
| `IsExchange` | `1` 表示此分类中的物品作为货币/兑换项。 |
| `InitStockPercent` | 缺失库存项首次初始化时，占最大库存的百分比。 |
| `Items[].ClassName` | DayZ/模组物品 classname，通常不区分大小写，但建议保持原写法。 |
| `MinPriceThreshold` / `MaxPriceThreshold` | 高库存最低价 / 低库存最高价。应满足 MinPrice ≤ MaxPrice。 |
| `MinStockThreshold` / `MaxStockThreshold` | 库存价格曲线的低/高端阈值。应满足 MinStock ≤ MaxStock。 |
| `SellPricePercent` | 物品级出售比例；`-1` 表示继续使用区域或全局值。 |
| `QuantityPercent` | 买入生成物品时的容量/数量百分比；`-1` 等同 100%。 |
| `SpawnAttachments` | 购买主物品时随附生成的默认附件。附件也必须存在于市场定义中，并通常以权限 `3` 隐藏。 |
| `Variants` | 与主条目共享市场配置的变体 classname；若某变体另有独立 `Items` 定义，则独立定义覆盖。 |

### 2.3 Trader 买卖权限

`Traders/*.json` 的 `Categories` 引用 `Market` 分类文件的相对名，不带 `.json`；子目录用路径表示。可加 `:<模式>`：

| 模式 | 含义 |
|---:|---|
| `0` | 玩家只能从交易商购买，不能卖给交易商。 |
| `1` | 玩家可以买，也可以卖。未写后缀时按此模式理解。 |
| `2` | 玩家只能卖给交易商，不能购买。 |
| `3` | 对玩家隐藏，常用于默认附件、变体或仅作为内部依赖。 |

`Items` 可对单个 classname 手动指定模式，并且优先于 `Categories`。因此调整“能否买卖”时，必须同时检查分类引用和手动物品覆盖，不能只改 Market 分类文件。

Trader 还可设置 `Currencies`、声望范围、阵营及任务要求。本服所有 32 个 Trader 配置的声望范围均为 `0..2147483647`，阵营为空，任务要求为 `-1`，当前没有实际门槛。

### 2.4 TraderZone 选择

交易商必须位于至少一个 TraderZone 中。若同时位于多个区域，当前官方实现会在所有包含该交易商位置的区域中，选择**区域中心距离交易商最近**的一个。因此本服半径 15000 的 `World.json` 是兜底区，本地小区域会覆盖它。

## 3. 本服当前全局设置

文件：`mpmissions/empty.deerisle/expansion/settings/MarketSettings.json`

| 设置 | 当前值 | 说明 |
|---|---:|---|
| `m_Version` | 17 | 禁止手动修改。 |
| `MarketSystemEnabled` | 1 | 市场启用。 |
| `ATMSystemEnabled` | 1 | ATM 启用。 |
| `SellPricePercent` | 20 | 全局兜底出售比例 20%。 |
| `Currencies` | `expansionbanknotehryvnia` | ATM 主货币。 |
| `MaxDepositMoney` | 100,000,000 | 玩家最大存款。 |
| `DefaultDepositMoney` | 10,000 | 玩家默认存款。 |
| `ATMPlayerTransferEnabled` | 1 | 玩家转账启用。 |
| `ATMPartyLockerEnabled` | 1 | 队伍金库启用。 |
| `MaxPartyDepositMoney` | 1,000,000,000 | 队伍最大存款。 |
| `UseWholeMapForATMPlayerList` | 1 | ATM 玩家列表使用全地图。 |
| `NetworkBatchSize` | 100 | 市场网络同步批大小。 |
| `MaxVehicleDistanceToTrader` | 200 | 普通载具交易距离。 |
| `MaxLargeVehicleDistanceToTrader` | 800 | 大型载具交易距离。 |
| `LargeVehicles` | `expansionlhd` | 大型载具列表。 |
| `VehicleKeys` | `ExpansionCarKey` | 载具钥匙 classname。 |
| `MaxSZVehicleParkingTime` | 1800 | 安全区载具停放时间。 |
| `SZVehicleParkingTicketFine` | 0 | 停车罚款。 |
| `SZVehicleParkingFineUseKey` | 1 | 停车罚款相关钥匙设置。 |
| `DisallowUnpersisted` | 0 | 未持久化物品未被全局禁止交易。 |
| `DisableClientSellTransactionDetails` | 0 | 客户端显示出售交易详情。 |

`NetworkCategories` 当前为空；该字段属于运行/网络生成数据，不应人工维护。

载具生成点：

- 陆地：2 个，约位于 `(5641.939, 27.996, 5430.872)` 与 `(13400.003, 12.965, 9877.509)`。
- 空中：1 个，约位于 `(13419.766, 12.965, 9876.791)`。
- 水上：2 个，约位于 `(5217.702, 0.444, 9317.313)` 与 `(7773.341, 0.563, 6891.502)`。
- 火车：0 个。

## 4. 本服 Market 分类基线

扫描结果：

- Market JSON：177 个，全部可解析。
- 物品定义：3228 条，3212 个唯一 classname。
- 重复 classname：16 组。
- 静态价格：1991 条。
- 正数静态库存：1931 条，全部使用 `1 / 1`；另有 9 条 `0 / 0` 库存定义，不属于静态库存。
- 物品级 `SellPricePercent` 覆盖：1948 条。
- 价格阈值倒置：0 条；库存阈值倒置：0 条。
- 所有分类 `m_Version`：12。
- `InitStockPercent`：75%（103 个文件）、100%（73 个文件）、78%（仅 `Fish.json`）。

按目录/模组家族统计：

| 家族 | 文件 | 条目 | 静态价格 | 静态库存 | 物品出售比例覆盖 |
|---|---:|---:|---:|---:|---:|
| 基础/其他 | 76 | 1266 | 256 | 416 | 175 |
| AJW | 8 | 345 | 344 | 5 | 345 |
| AP | 9 | 151 | 151 | 151 | 151 |
| Bitcoin | 36 | 476 | 476 | 468 | 418 |
| FOG | 10 | 214 | 214 | 211 | 214 |
| MMG | 9 | 234 | 234 | 232 | 171 |
| NamantH | 2 | 21 | 21 | 21 | 21 |
| Snafu | 10 | 324 | 98 | 230 | 282 |
| TTC | 17 | 197 | 197 | 197 | 171 |

当前 `SellPricePercent` 分布：

```text
-1:1280, 0.2:6, 1:13, 3:86, 4:3, 5:569, 6:6, 7:42,
8:58, 9:72, 10:654, 15:3, 20:37, 25:17, 30:15, 35:12,
40:11, 50:6, 75:283, 80:1, 100:54
```

其中 6 条 `0.2` 按当前代码代表 **0.2%**，不是 20%；这是后续价格审查的高优先级检查项，但本次没有擅自修改。

### 4.1 货币定义

`Market/Exchange.json`：`IsExchange = 1`，4 种兑换项均为静态价格/静态库存。

| Classname | 固定价值 | 出售比例 |
|---|---:|---:|
| `expansionbanknotehryvnia` | 1 | 100% |
| `expansiongoldbar` | 3,000 | 100% |
| `expansiongoldnugget` | 1,500 | 100% |
| `hm_plus_bitcoin` | 1,000,000 | 80% |

ATM 使用 `expansionbanknotehryvnia`。部分高级交易商直接使用 `hm_plus_bitcoin` 结算。

### 4.2 重复 classname

这些 classname 在多个独立 Market 条目中有定义，加载顺序可能影响最终生效项；在改价前必须先确认所有定义：

| Classname | 重复文件 |
|---|---|
| `battery9v` | `Batteries.json`; `Bitcoin_Batteries.json` |
| `carbattery` | `Batteries.json`; `Bitcoin_Batteries.json` |
| `carradiator` | `Bitcoin_Vehicle_Parts.json`; `Vehicle_Parts.json` |
| `expansion_mh6_door_1_1` | `Bitcoin_Vehicle_Parts.json`; `Vehicle_Parts.json` |
| `expansion_mh6_door_1_2` | 同上 |
| `expansion_mh6_door_2_1` | 同上 |
| `expansion_mh6_door_2_2` | 同上 |
| `expansionbiggyrocopter` | `Bitcoin-Helicopters.json`; `Helicopters.json` |
| `expansiongyrocopter` | `Bitcoin-Helicopters.json`; `Helicopters.json` |
| `expansionhelicopterbattery` | `Batteries.json`; `Bitcoin_Batteries.json` |
| `expansionhydraulichoses` | `Bitcoin_Vehicle_Parts.json`; `Vehicle_Parts.json` |
| `expansionigniterplug` | `Bitcoin_Vehicle_Parts.json`; `Vehicle_Parts.json` |
| `expansionmh6` | `Bitcoin-Helicopters.json`; `Helicopters.json` |
| `headlighth7` | `Bitcoin_Vehicle_Parts.json`; `Vehicle_Parts.json` |
| `sparkplug` | `Bitcoin_Vehicle_Parts.json`; `Vehicle_Parts.json` |
| `truckbattery` | `Batteries.json`; `Bitcoin_Batteries.json` |

### 4.3 未被 Trader 分类引用的文件

以下 8 个 Market 分类文件没有出现在任何 Trader 的 `Categories` 中：

```text
Ammo.json
Bitcoin-Helicopters.json
Helicopters.json
Launchers.json
Liquids.json
Magazines.json
Pelts.json
Sweaters_And_Hoodies.json
```

综合 `Categories`、Trader 手动 `Items` 和 `Variants` 检查后，共有 49 条物品定义当前无法通过已配置交易商路径到达。删除前仍须检查它们是否作为 `SpawnAttachments`、其他脚本依赖或未来备用配置使用，不能仅凭“未引用”直接删除。

交叉引用结果：

- Trader 引用不存在的 Market 分类：0。
- Trader 手动物品引用不存在的 Market 定义/变体：0。

## 5. 本服 Trader 基线

- Trader JSON：32 个，全部可解析，全部 `m_Version = 13`。
- 分类权限引用总数：模式 0 = 39，模式 1 = 90，模式 2 = 27，模式 3 = 30。
- 所有 Trader 当前均无声望、阵营或任务限制。

下表中“分类模式”按 `0/1/2/3` 统计；“手动物品”也是相同顺序：

| Trader 文件 | 显示名/用途 | 货币 | 分类模式 0/1/2/3 | 手动物品 0/1/2/3 |
|---|---|---|---:|---:|
| `Aircraft.json` | Aircraft | Hryvnia | 0/0/0/2 | 2/1/0/1 |
| `AJW.json` | AJW武器商人 | Hryvnia | 0/5/2/1 | 0/0/0/0 |
| `AP_Armor.json` | 高级护甲商人 | Bitcoin | 14/0/0/0 | 0/0/0/0 |
| `AP_Rookie.json` | 新手区护甲商人 | Hryvnia | 0/7/2/0 | 0/0/0/0 |
| `Attachments.json` | Attachments | Hryvnia | 0/5/0/0 | 0/40/0/1 |
| `Better_Cars.json` | 高端载具商人 | Bitcoin | 11/0/0/12 | 0/0/0/4 |
| `BIG_GUNS.json` | 高级步枪商人 | Bitcoin | 4/0/0/0 | 0/0/0/0 |
| `Bitcoin_Mining.json` | 区块链商人 | Hryvnia | 1/0/0/0 | 0/0/0/0 |
| `Boats.json` | Boats | Hryvnia | 0/1/0/2 | 0/0/0/0 |
| `BuildingSupplies.json` | Building Supplies | Hryvnia | 0/8/0/0 | 2/0/0/0 |
| `Clothing_Accessories.json` | Clothing Accessories | Hryvnia | 0/13/0/0 | 0/0/0/1 |
| `Clothing.json` | Clothing | Hryvnia | 0/6/0/0 | 0/0/0/0 |
| `Components.json` | Components | Hryvnia | 0/9/0/0 | 1/0/0/6 |
| `Consumables.json` | Consumables | Hryvnia | 0/0/6/0 | 0/0/0/0 |
| `Defibrillator.json` | 高级电气道具商人 | Bitcoin | 1/0/0/0 | 0/0/0/0 |
| `DF_Collection.json` | 稀有收藏品商人 | Hryvnia | 0/0/1/0 | 0/0/0/0 |
| `DNA.json` | DNA卡房物资商 | Hryvnia | 1/0/0/0 | 0/0/1/0 |
| `Event.json` | Event | Hryvnia | 0/1/0/0 | 0/0/0/0 |
| `Exchange.json` | Exchange | Hryvnia | 0/1/0/0 | 0/0/0/0 |
| `Exchanger.json` | 货币交换机 | Hryvnia | 0/0/1/0 | 0/1/0/1 |
| `Fishing.json` | Fishing | Hryvnia | 1/0/1/0 | 0/0/0/0 |
| `FOG_Trader.json` | FOG装备 | Hryvnia | 0/8/2/0 | 0/0/0/0 |
| `MagLoader.json` | 装弹器&消音器 | Bitcoin | 1/2/0/0 | 0/0/0/0 |
| `Medicals.json` | Medicals | Hryvnia | 2/0/0/0 | 0/0/0/0 |
| `MMG.json` | MMG装备商人 | Hryvnia | 0/2/1/0 | 0/0/0/0 |
| `Rookie_Snafu.json` | 新手区SNAFU武器商人 | Hryvnia | 0/7/2/1 | 0/0/0/0 |
| `Special.json` | Special | Hryvnia | 0/1/0/0 | 5/6/0/0 |
| `Spraycans.json` | Spraycans | Hryvnia | 0/1/0/0 | 0/0/0/0 |
| `TTC.json` | TTC武器商人 | Hryvnia | 0/5/7/5 | 0/0/0/0 |
| `Vehicle_Parts.json` | Vehicle Parts | Hryvnia | 0/0/0/1 | 1/0/0/3 |
| `Vehicles.json` | Vehicles | Hryvnia | 2/0/0/2 | 4/0/0/0 |
| `Weapons.json` | Weapons | Hryvnia | 1/8/2/4 | 11/0/0/49 |

注：表中 Hryvnia 指 `expansionbanknotehryvnia`，Bitcoin 指 `hm_plus_bitcoin`。

## 6. Trader 放置与区域基线

### 6.1 放置文件

`mpmissions/empty.deerisle/expansion/traders` 中共有 3 个 `.map` 文件、26 个实体放置。每行基本格式：

```text
<Trader实体类>.<Traders配置文件基名>|<位置>|<朝向>|<装备>
```

所有 26 个放置引用都能找到对应 Trader JSON，且都位于至少一个 TraderZone 内。

| `.map` 文件 | 主要绑定 |
|---|---|
| `42.map` | `MagLoader`、`Better_Cars`、`BIG_GUNS`、`AP_Armor`、`Defibrillator` |
| `ROOKIE_TRADER.map` | `BuildingSupplies`、`Clothing`、`Clothing_Accessories`、`Fishing`、`Medicals`、`Consumables`、`Components`、`Weapons`、`Vehicles`、`Vehicle_Parts`、`Exchanger`、`Bitcoin_Mining`、`DF_Collection` |
| `World.map` | 两个 `Boats`，以及 `Rookie_Snafu`、`TTC`、`AJW`、`AP_Rookie`、`FOG_Trader`、`MMG` |

未在现有 `.map` 放置中找到的 Trader 配置：

```text
Aircraft.json
Attachments.json
DNA.json
Event.json
Exchange.json
Special.json
Spraycans.json
```

它们可能是备用配置，也可能由其他模组/脚本动态生成实体；在当前检查范围内不能确认其实际 NPC 已启用。注意 `Exchanger.json` 已放置，而 `Exchange.json` 没有找到放置。

### 6.2 TraderZone 快照

| 区域文件 | 显示名 | 中心 | 半径 | 买入倍率 | 区域出售比例 | Stock 条目 |
|---|---|---|---:|---:|---:|---:|
| `42.json` | 黑市 | `(13383.530, 12.910, 9865.882)` | 250 | 100% | -1（回退全局） | 649 |
| `Boat_Trader_Rookie.json` | 船只商人 | `(7786, 1, 6831)` | 200 | 100% | -1 | 239 |
| `Boat_Trader_Spire.json` | 船只商人 | `(5223.367, 1.571, 9303.166)` | 200 | 100% | -1 | 239 |
| `Rookie_Trader.json` | 物资交易中心 | `(5630, 28.740, 5392.5)` | 200 | 100% | 30% | 5997 |
| `Waldoboro.json` | 高级武器商人 | `(9557.933, 0, 8937.799)` | 200 | 100% | -1 | 1081 |
| `WestBrook.json` | 高级护甲商人 | `(3445, 0, 6424)` | 200 | 100% | -1 | 2897 |
| `World.json` | World Trader Zone | `(7500, 0, 7500)` | 15000 | 100% | -1 | 2326 |

实际最近区域映射：

- `42.map` 的交易商 → `42.json`。
- `ROOKIE_TRADER.map` 的交易商 → `Rookie_Trader.json`。
- Waldoboro 的 `Rookie_Snafu/TTC/AJW` → `Waldoboro.json`。
- WestBrook 的 `AP_Rookie/FOG_Trader/MMG` → `WestBrook.json`。
- 两个船商 → 各自的 Boat TraderZone。
- `World.json` 覆盖全图，但因中心更远，只作为兜底。

## 7. 后续修改标准流程

### 7.1 修改价格

1. 搜索 classname 的全部独立定义和变体：

   ```powershell
   rg -n -i '"ClassName"\s*:\s*"目标ClassName"|"目标ClassName"' 'D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\Market'
   ```

2. 确认是否存在重复独立定义；若有，明确哪个 Trader/分类正在使用。
3. 在对应 `Market/*.json` 修改 `MinPriceThreshold` 与 `MaxPriceThreshold`。
4. 若希望固定价格，两者设为相同值；若希望动态价格，保持 `MinPriceThreshold ≤ MaxPriceThreshold`。
5. 不要因为调价而修改 TraderZone `Stock`，除非明确要重置库存。
6. 解析全部 JSON、复核引用，并登记变更日志。

### 7.2 修改可以买/卖的属性

1. 找出目标 Market 分类。
2. 检查所有 `Traders/*.json` 中该分类的 `Categories` 模式。
3. 同时检查 Trader `Items` 是否对该 classname 有覆盖；`Items` 优先。
4. 按需求使用模式 0/1/2/3。
5. 若物品是主物品默认附件或仅内部使用，通常保留市场定义并使用模式 3，而不是直接删除。

### 7.3 新增市场物品

1. 确认准确 classname、来源模组及依赖附件。
2. 优先放入语义正确的现有分类；如需新分类，创建新的 `Market/<名称>.json`。
3. 设置价格、库存阈值、出售比例、数量、附件和变体。
4. 至少在一个目标 Trader 的 `Categories` 或 `Items` 中引用并设置权限，否则物品不会形成可用交易路径。
5. `SpawnAttachments` 中的附件也要有 Market 定义，并确保目标 Trader 可访问，通常为模式 3。
6. 对已存在的 TraderZone，新增物品的缺失库存项会按分类 `InitStockPercent` 初始化。
7. 检查 classname 重复、所有 JSON 解析及交叉引用，然后记录日志。

### 7.4 删除市场物品

1. 搜索该 classname 的独立定义、`Variants`、`SpawnAttachments` 和 Trader 手动 `Items`。
2. 先解除 Trader 展示/权限引用，再删除 Market 定义。
3. 确认没有作为其他商品默认附件、变体或脚本依赖。
4. TraderZone 的旧 `Stock` 条目通常可由系统维护；若要人工清理，必须停服、备份并精确删除单项，不能批量清空。
5. 解析全部 JSON并登记日志。

### 7.5 每次修改的最低验证清单

- [ ] 修改前已停止服务器或确认配置文件不会被运行中的服务器回写。
- [ ] 已备份所有将修改的文件。
- [ ] `m_Version` 未手动更改。
- [ ] `NetworkCategories` 未手动维护。
- [ ] 全部 Market、Trader、TraderZone、MarketSettings JSON 可解析。
- [ ] `MinPriceThreshold ≤ MaxPriceThreshold`。
- [ ] `MinStockThreshold ≤ MaxStockThreshold`。
- [ ] 没有意外新增重复 classname。
- [ ] Trader 分类引用均存在。
- [ ] Trader 手动 Items 均能在 Market 定义或 Variants 中找到。
- [ ] 新物品至少有一个有效交易商路径和正确权限。
- [ ] 默认附件/变体依赖可用。
- [ ] 已在本文“变更日志”记录修改内容、前后值和验证结果。

## 8. 当前待关注事项

1. 6 条 `SellPricePercent = 0.2` 按当前实现仅为 0.2%，需要在未来定价任务中逐项确认是否原本想写 20%。
2. 16 组重复 classname 可能让改价只改到其中一份；相关物品必须全局搜索后再操作。
3. 8 个未被 Trader 分类引用的文件、49 条无法通过现有交易路径到达的定义，需按实际运营意图决定保留、接入或删除。
4. 7 个 Trader JSON 未发现静态 `.map` 放置；可能是备用或动态生成，不能直接判定为废弃。
5. `Rookie_Trader.json` 的区域出售比例是 30%，会覆盖全局 20%；其他当前区域为 `-1`，通常回退到全局 20%，但物品级非负值仍有最高优先级。

## 9. 2026-08-12 全市场异常审计

本节记录 2026-08-12 的专项审计结论。本轮只分析和记录，未修改任何 Market、Trader、TraderZone、MarketSettings 或 `.map` 配置。

### 9.1 建议优先解决

1. **3 个 AP 高级头盔附件可免费购买。**  
   `ap_altyn_visor_black`、`ap_vulkan_barmit_black`、`ap_vulkan_visor_black` 在 `Bitcoin-AP-Helmet-Parts.json` 中价格为 0，而 `AP_Armor.json` 对该分类使用模式 0。它们不是单纯隐藏附件，而是可见、可购买、不可出售。建议按运营意图改为模式 3，或设置真实价格。

2. **4 个比特币消音器出售后实际无法获得货币。**  
   `cds_sodapipsi_suppressor`、`cds_teddy_suppressor_pink`、`cds_suppressor_ak_01`、`cds_suppressor_m4_camo925` 的价格均为 5,000,000，`SellPricePercent = 0.2`，账面回收价仅 10,000。`MagLoader` 只接受面值 1,000,000 的 `hm_plus_bitcoin`，官方 `SpawnMoney` 无法生成不足 1 枚的实物货币，因此玩家出售物品后实物付款为 0。若原意是 20%，应写 `20`，并确认出售额能被 Trader 的货币面值精确支付。

3. **3 种大口径弹药标价低于唯一比特币面值。**  
   `gcgn_ammo_408chey` 和 `gcgn_ammo_50cal` 标价 50,000，`snafu_ammo_145cal` 标价 200,000；它们在 `BIG_GUNS` 以模式 0 出售，而 Trader 只接受面值 1,000,000 的比特币。官方购买逻辑会拿取 1 枚足以覆盖价格的大面值货币，再使用该 Trader 接受的货币找零；当前没有小面值，因此实际扣除 1,000,000，无法返还 950,000 或 800,000。

4. **16 组重复 classname 会触发官方 Market 配置错误。**  
   官方 `ExpansionMarketCategory.CheckDuplicate` 会拒绝后加载的重复项，并记录 MarketCfgError。12 组参数相同，主要造成日志错误和分类缺项风险；以下 4 组参数不同，加载先后还会改变最终有效配置：

   - `expansionbiggyrocopter`：32,000,000 固定价 vs 1,000,000–2,000,000 动态价。
   - `expansiongyrocopter`：22,000,000 固定价 vs 500,000–1,000,000 动态价。
   - `expansionmh6`：102,000,000 固定价 vs 1,500,000–3,000,000 动态价。
   - `expansionhydraulichoses`：0 vs 54,045。

### 9.2 确认运营意图后处理

1. **7 个已放置 Trader 商品配置为可买卖，但库存阈值是 `0 / 0`。**  
   `nbcbootsgray`、`nbcjacketgray`、`nbcpantsgray`、`gasmask`、`gp5gasmask`、`nbcglovesgray`、`nbchoodgray` 当前模式均为 1，但 `MaxStockThreshold = 0`。官方逻辑不会把 `0 / 0` 识别为静态库存，购买库存也无法建立；实际效果更接近只回收。若它们是稀有战利品，应明确改为模式 2；若希望可购买，应设置正数库存阈值。

2. **18 个 Variant 由多个父条目重复声明。**  
   主要集中在 FOG 服装/护甲以及两个 LandCruiser 门变体。它们的父条目参数当前一致，经济影响较低，但官方加载器会拒绝后续 Variant 归属，建议在整理对应分类时修正。

3. **`expansion_ammo_taser` 固定购买价仅为 1 Hryvnia。**  
   该物品由已放置的 `Weapons` Trader 手动设为模式 0。不能仅凭价格判定为错误，但它显著低于其他弹药，应确认是否为占位价或刻意免费化。

4. **市场整体以固定价和无限库存为主。**  
   3228 条定义中，1931 条（59.8%）为正数静态库存，1991 条（61.7%）为静态价格。这不属于配置错误，但意味着本服 Market 更接近固定价商店，而不是强库存驱动的动态市场。

5. **`DisallowUnpersisted = 0`。**  
   当前允许未完成持久化的物品参与交易。没有证据证明本服已发生利用，但若服务器希望加强复制品/回档交易防护，应单独评估是否改为 1。

### 9.3 维护性问题，暂不建议优先动

- 7 个 TraderZone 合计 13,428 条 `Stock` 记录，其中 1297 条（9.7%）已不属于当前 Market 独立定义或 Variants：`Rookie_Trader.json` 804 条、`World.json` 471 条，其余区域共 22 条。
- 569 条动态库存（4.2%）高于当前 `MaxStockThreshold`，其中 565 条在 `Rookie_Trader.json`。官方运行逻辑会按当前上限处理，主要风险是文件膨胀、旧配置残留和排障困难。
- 49 条 Market 定义没有当前有效交易路径，7 个 Trader JSON 没有找到静态 `.map` 放置。这些可能是备用或脚本动态使用项，不能直接删除。

### 9.4 建议处理顺序

1. 零价 AP 附件。
2. 比特币消音器的 `0.2` 出售比例和零实付问题。
3. 三种低于比特币面值的弹药价格。
4. 7 个 `0 / 0` 库存商品的实际买卖意图。
5. 16 组重复 classname 和 18 个多父级 Variant。
6. 最后在停服、备份后清理孤儿库存和确认无路径配置。

## 10. 2026-08-12 市场重构需求与影响分析

本节承接 `D:\OneDrive\Deerisle 6.1\Project Manage\合成系统-装备分级与经济基准.md`。本轮只建立重构方案、交叉表和验证口径，未修改任何 Market、Trader、TraderZone、MarketSettings 或 `.map` 配置。

配套可复核文件：

- `EXPANSION_MARKET_REBUILD_ANALYSIS.ipynb`：已执行的 312 条受管装备交叉审计。
- `EXPANSION_MARKET_REBUILD_CROSSWALK.csv`：classname、A1—A6、模组、family、当前价格、Trader 权限和可达性逐条映射。

### 10.1 重构目标

1. AP/FOG/MMG 护甲不再按模组来源定价，改按 A1—A6、防护带、确认总容量和角色定价。
2. TTC/SNAFU/AJW 武器不再按模组来源定价，改按 A1—A6、战斗角色、口径、持续火力、弹匣和附件完整度定价。
3. 同一 `balance_family` 的纯皮肤原则上同价，Variant 只继承一个父条目。
4. 附件、弹匣和弹药按功能与适配层级定价，不能继续沿用“整个 SNAFU 配件 400、AJ 配件数千至数十万”等模组独立价表。
5. 新增材料回收商人，让玩家出售多余合成材料，但将其设计成受控的货币出口，避免与成品回购叠加造成经济膨胀。
6. A5/A6、阶段核心和终局递进物资继续以副本、合成和 P2P 为主，不重新开放无限 NPC 售卖库存。

### 10.2 当前 Market 与受管名册的交叉结果

- 正式受管名册：312 条（260 武器、49 护甲、3 弹匣；不含 Hammer/Shovel 和后来新增的 MMG 全景 NVG）。
- 当前有 Market 独立定义或 Variant 映射：263 条；另有 49 条受管结果目前没有 Market 定义。这里的“49 条”与旧审计中的“49 条 Market 定义无交易路径”是两个不同集合，后续不能混淆。
- 263 条均能通过当前已放置 Trader 到达。
- 玩家当前可从 NPC 购买的受管结果仅 20 条。
- 玩家当前可出售给 NPC 的受管结果有 252 条。新增材料回购后，必须避免“成品回购 + 材料回购”形成双重货币增发。
- 有 1 条受管结果命中多个 Market 父级/定义，后续生成新分类时必须消除多父级 Variant。

当前同阶跨模组价格差异非常大，证明不能只做百分比平移：

- A6 武器：AJW 当前中位价约 83,000；TTC 约 65,000；SNAFU 约 10,000,000，SNAFU 同阶最低 50,000、最高 15,000,000。
- A6 护甲：AP 两件均约 5,000,000；FOG 三件约 13,000—30,700。
- A3 护甲：AP 中位价约 150,000；FOG 约 30,700；MMG 约 22,000。
- 附件也没有统一口径：SNAFU 大量配件固定 400；TTC 常见配件约 400—5,000；AJ 光学和附件约 3,000—200,000。

### 10.3 推荐的新结构

建议以一份可生成的“经济账本”为唯一价格源，再生成 Expansion JSON；不要继续直接在六套模组文件中各自手工定价。

```text
受管装备名册 / family / A1—A6
        +
合成完整成本 / donor / 拆解返还
        +
武器角色、护甲防护与容量、附件功能
        ↓
统一经济账本（每个 classname 的权限、基础价、NPC 回收价、库存策略）
        ↓
Market\Rework\*.json + Traders\*.json
        ↓
重复项、套利、货币面值、Trader 可达性、JSON/RPT/实机验证
```

建议的逻辑分类：

- `Rework\Weapons_A1` 至 `Weapons_A6`，A6 再区分 Horde / AI Heavy / Strategic。
- `Rework\Armor_A1` 至 `Armor_A6`，同时保留防护带、容量和突击/后勤角色字段于经济账本。
- `Rework\Optics`、`Suppressors`、`Magazines`、`Ammo`、`WeaponParts`，按功能和适配层级而不是模组拆价。
- `Rework\Materials_Common`：Bolts、Cloth、Metal、WeaponParts、Calibrator、Cable、Poxeram。
- `Rework\Materials_Core`：Board、PowerFilter、GyroScope、FlashStorage、Virtex、FAR。
- 只作为成品默认附件或内部依赖的条目保留 Market 定义，但 Trader 使用模式 3。

### 10.4 权限与价格原则

1. 材料商人使用模式 2（玩家只能卖给 NPC），不向玩家无限出售材料。
2. 材料按“1 单位”定价。官方出售逻辑会读取堆叠数量并逐单位计算；仍须用 1/5/满堆三组自定义 QPK 实物完成烟雾测试。
3. 材料分类建议 `SellPricePercent = 100`，直接把 `Min/MaxPriceThreshold` 作为明确的单位回收价，避免再次发生 `0.2` 被误解为 20% 的双参数错误。
4. Expansion 原生 Market 没有可靠的每日回收额度。动态库存可以降低价格，但模式 2 不会通过玩家购买自然消耗库存；因此不能把 `MaxStockThreshold` 当作每日硬上限。
5. 成品完整成本 `C` 必须包含材料单位价、阶段核心、Calibrator、工具损耗、工时和 donor。
6. NPC 售价必须高于 `C`，避免商店挤掉合成路线；A5/A6 原则上不提供无限 NPC 售卖。
7. NPC 成品回收价必须低于 `C`，并与“直接卖材料”和“拆解后卖材料”两条路径共同做闭环审计。
8. 同 family 纯皮肤同价；配件包、弹匣、耐久或数值确有差异时才允许加价。
9. 高级护甲不能只按防护单轴；Redut H+/42 与 Wardrum Full H/126 必须作为不同终局路线定价。
10. A6 Strategic 至少按 FAR 3 / 1.5 RGE 核算，不能与普通 A6 平价。

### 10.5 旧问题在重构中的去留

| 旧问题 | 重构结果判断 | 必须采取的动作 |
|---|---|---|
| 3 个 AP 零价头盔附件 | 仅部分自然解决 | 必须把 AP 附件也纳入新账本；仅改 312 条成品不会触及它们 |
| 4 个比特币消音器 `0.2%` 且零实付 | 不会自然解决 | 独立修正 MagLoader/Bitcoin 消音器价格、比例和面值 |
| 3 个低于比特币最小面值的弹药 | 部分解决 | SNAFU 14.5 可随弹药重构处理；两种 GCGN 弹药仍需 BIG_GUNS 专项 |
| 16 组重复 classname | 不会自然解决 | 车辆/部件重复项需独立清理，否则继续触发 MarketCfgError |
| 7 个 NBC/面具 `0/0` 但模式 1 | 必须在重构解决 | 这是跨阶门槛物资，应明确模式 2 或 3，不能恢复 NPC 新库存 |
| 18 个多父级 Variant | 部分解决 | FOG 项从 family 源重新生成并去重；LandCruiser 门仍需独立处理 |
| Taser 弹药售价 1 | 不会自然解决 | 纳入通用弹药专项审计 |
| TraderZone 历史库存 | 不会因改价消失 | 下档停服备份后初始化新库存，避免历史门槛物资重新进入市场 |
| 49 条无现行交易路径定义 | 可能重新分配但不会自动消失 | 新 JSON 生成后再次做可达性审计 |
| `DisallowUnpersisted = 0` | 不会自然解决 | 作为独立安全策略决定 |

### 10.6 推荐实施顺序

1. 重新冻结当前 314/742 合成合同，并将 MMG 全景 NVG 纳入正式 manifest。
2. 冻结 Market 重构范围和 NPC 权限矩阵：哪些阶可买、可卖、P2P-only、隐藏。
3. 建立 13 种材料的单位回收价与每周 NPC 货币发行预算；阶段核心单独定价。
4. 从 312 条受管名册生成武器/护甲统一账本，再补入 MMG 全景 NVG、所有皮肤 family、附件、弹匣和弹药。
5. 先在副本配置副本或隔离目录生成新 Market/Trader JSON，不覆盖运行文件。
6. 运行重复 classname、Variant、附件依赖、货币面值、权限可达性和四类套利检查。
7. 在新档停服窗口备份旧配置与 TraderZone，替换配置并初始化库存。
8. 完成 RPT、UI、1/5/满堆材料出售、带附件成品出售、比特币找零和新库存实机验收。
9. wipe 后按 7/14/30/45 天观察材料发行、货币增发、P2P 成交和阶段到达速度，再小步调价。

### 10.7 重构成败的最小指标

- NPC 材料回购的 Hryvnia 发行量/活跃玩家/周。
- NPC 总回购发行量与服务器主要货币回收量之比。
- 各材料 NPC 售出单位数、P2P 成交量及成交中位数。
- A1—A6 的玩家到达时间与当前 3/7/14/21/30/45 天目标差异。
- 同 stage、同 family、同功能附件的价格离散度；纯皮肤应为 0。
- “卖材料、合成后卖成品、拆解后卖材料、NPC 买入后拆解”四条路径的最高净收益；任何可重复正收益闭环均不得上线。

当前缺少 wipe 后实测供应与成交数据，因此本轮可以确定分类、公式、权限与安全线，但不应把任何拍脑袋的 Hryvnia 数字写成最终正式价格。

## 11. 变更日志

后续每次修改必须追加一行；若一次操作较复杂，可在表格后另建带日期的小节写完整明细。

| 日期时间 | 操作人/模型 | 需求与范围 | 修改文件 | Classname / 分类 / Trader | 修改前 → 修改后 | 验证与备注 |
|---|---|---|---|---|---|---|
| 2026-08-11 | Codex | 建立 Expansion Market 机制说明与本服配置基线 | 新增 `EXPANSION_MARKET_GUIDE.md` | 全局审计 | 无市场配置变更 | 177 Market、32 Trader、7 Zone、3 map/26 放置均完成解析与交叉核对 |
| 2026-08-12 | Codex | 全市场异常、货币面值、权限与库存专项审计 | 更新 `EXPANSION_MARKET_GUIDE.md` | 全局审计 | 无市场配置变更 | 记录 4 类优先问题、运营确认项与维护性问题；相关 JSON 仍保持原样 |
| 2026-08-12 | Codex | 将 A1—A6 合成分级、六模组统一定价和材料商人需求映射到 Market 重构 | 更新指南；新增 `EXPANSION_MARKET_REBUILD_ANALYSIS.ipynb` 与 `EXPANSION_MARKET_REBUILD_CROSSWALK.csv` | 312 条受管装备、13 种材料、旧异常矩阵 | 无市场配置变更 | 263 条有 Market 映射、20 条可买、252 条可卖；记录重构结构、权限原则、实施顺序与指标 |
| 2026-08-12 | Codex | 落实市场结构修复，并固化枪械/护甲重构规则 | 25 个 Market/Trader 源文件、7 个 TraderZone；新增迁移清单与备份 | 比特币商店、NBC、车辆/飞机依赖、重复定义、无引用定义、区域库存 | 见第 12 节 | 212 个活动 JSON 全部可解析；独立 classname 重复数 16 → 0；库存 13,428 → 12,030，未清空任何区域 |

### 复杂变更记录模板

```markdown
### YYYY-MM-DD HH:mm — <任务标题>

- 用户目标：
- 修改文件：
- 涉及 classname / 分类 / Trader / Zone：
- 修改前：
- 修改后：
- 修改理由与价格逻辑：
- 是否重置区域库存：否 / 是（列出精确条目和备份）
- 验证：JSON 解析 / 阈值 / 重复项 / Trader 引用 / 附件与变体 / 实机验证
- 备份位置或版本标识：
- 未决问题：
```

## 12. 2026-08-12 市场结构修复与重构决策

### 12.1 已确认的长期规则

1. AP / FOG / MMG 的普通护甲最终统一在 WestBrook 护甲商人区交易；TTC / SNAFU / AJW 的普通枪械最终统一在 Waldoboro 武器商人区交易。不得再仅因装备等级较高，就把普通枪械或护甲放到 42 区并使用比特币结算。
2. 所有以 `hm_plus_bitcoin` 结算且向玩家显示的商品必须是模式 `0`（buy only）；自动随主商品生成但不应单独显示的附件使用模式 `3`。零价隐藏附件只参与生成完整物品，不代表玩家可免费购买。
3. Market 物品定义是全局的。同一 classname 只保留一个独立定义；车辆商人和飞机商人可共同引用该定义，不得为每个商人复制一份类别文件。
4. 因副本/事件递进而禁止商人出售、但允许玩家回收变现的物品使用模式 `2`（sell only），不得再用 `0/0` 库存伪装成禁售。
5. TraderZone 是运行期库存，不因改价自动重置。维修时必须停服、先备份、按当前有效定义精确删除过期键或截顶异常动态库存，禁止直接清空整个 `Stock`。
6. 无活动分类引用、无手动物品引用且不是 `SpawnAttachments` 依赖的独立定义，移出活动 `Market` 并放入 `Market_Backup`；不得直接删除。

### 12.2 本轮已经实际应用的修改

- `AP_Armor.json`：`Bitcoin-AP-Helmet-Parts:0` → `Bitcoin-AP-Helmet-Parts:3`。AP 头盔附件继续保持零价依赖，但不再作为可见免费商品。
- `MagLoader.json`：两个比特币消音器分类补全 `:0`，所有可见比特币商品现均为 buy only。比特币消音器的 `SellPricePercent` 从 `0.2` 修正为 `20.0`；虽然模式 `0` 会阻止实际回售，数值本身仍保持语义正确。普通 `Muzzles.json` 中相同的两处 `0.2` 笔误也同步改为 `20.0`。
- `Better_Cars.json`：隐藏依赖由重复的 `Bitcoin_Batteries` / `Bitcoin_Vehicle_Parts` 改为唯一全局分类 `Batteries:3` / `Vehicle_Parts:3`。共享的 `expansionhydraulichoses` 定义改为零价，继续只作为隐藏随车依赖。
- NBC/防毒系列：7 个独立 Market 父项的库存阈值由 `0/0` 改为 `1/100`；灰/黄/白变体共 16 个 classname 在 `Clothing.json` 或 `Clothing_Accessories.json` 中显式设为模式 `2`。玩家不能从 NPC 购买，但可向对应商人出售。
- 16 组独立 classname 重复全部归并，当前活动 Market 的独立重复数为 `0`。
- 49 个无交易/依赖路径的独立定义已归档；另外归档了 15 个重复副本。活动 Market 文件由 177 个变为 172 个，当前含 3164 个独立定义和 6009 条 Variant 记录。
- 整文件归档：`Bitcoin_Batteries.json`、`Bitcoin_Vehicle_Parts.json`、`Bitcoin-Helicopters.json`、`Pelts.json`、`Sweaters_And_Hoodies.json`。
- 局部归档：`Ammo.json` 19 项、`Helicopters.json` 3 项、`Launchers.json` 2 项、`Liquids.json` 1 项、`Magazines.json` 9 项。原始对象完整保存在备份分类文件中，可按 classname 恢复。

### 12.3 TraderZone 精确清理结果

服务器进程确认未运行后，先备份 7 个区域文件，再按修复后的活动 Market 建立大小写不敏感的有效 classname/Variant 集合：

| Zone | 修改前 | 修改后 | 过期键移除 | NBC 重初始化键 | 动态库存截顶 |
|---|---:|---:|---:|---:|---:|
| 42 | 649 | 637 | 12 | 0 | 0 |
| Boat_Trader_Rookie | 239 | 233 | 6 | 0 | 0 |
| Boat_Trader_Spire | 239 | 233 | 6 | 0 | 4 |
| Rookie_Trader | 5997 | 5132 | 849 | 16 | 1469 |
| Waldoboro | 1081 | 1067 | 14 | 0 | 0 |
| WestBrook | 2897 | 2897 | 0 | 0 | 0 |
| World | 2326 | 1831 | 495 | 0 | 0 |
| **合计** | **13,428** | **12,030** | **1382** | **16** | **1473** |

此前第 9 节的“569 条动态库存超上限”只覆盖独立父 classname，并未完整统计 TraderZone 中单独保存、但继承父阈值的 Variant 库存键。本轮按运行时继承关系复核后的正确处理数是 1473。有效库存没有被重置；只删除失去活动定义的键、16 个需要按新库存规则初始化的 NBC 键，并把动态库存高于当前上限的数值截到上限。

### 12.4 枪械/护甲迁区的当前状态

- 已新增 `EXPANSION_MARKET_REBUILD_MIGRATION.csv`，为 312 条受管装备记录目标区域、目标 Trader、目标货币和迁移状态。
- 护甲目标区为 `WestBrook`，枪械目标区为 `Waldoboro`，结算货币统一为 `expansionbanknotehryvnia`。
- 本轮**没有**立即删除 42 区的 `AP_Armor` / `BIG_GUNS` 放置或切走其分类。原因是统一 A1—A6 价格表和最终买卖权限尚未定稿；现在半迁移会造成商品缺失、旧比特币价在 Hryvnia 商人出现，或同一物品多币种并存。
- 正式切换必须作为一次原子变更完成：确定统一价格 → 修改 Market → 修改目标护甲/武器 Trader → 移除 42 区普通装备引用/放置 → 精确处理受影响 Zone 库存 → 完整验证。

### 12.5 仍会影响后续重构的问题

- 统一价格尚未生成。需要基于 A1—A6、武器经济带、附件功能系数和材料机会成本建立价格表，不能沿用各模组旧价中位数。
- 13 种合成材料的新回收商人、sell-only 权限、回购价和发行量护栏尚未落地；这是控制新档货币膨胀的核心工作。
- 18 个多父级 Variant 尚未归并。它们不会造成独立 classname 加载冲突，但会让同一皮肤可能继承多个价格/库存父项，必须在生成最终价格文件前解决。
- Taser 弹药价格 `1`、GCGN 两项不足一枚比特币的旧价格、`DisallowUnpersisted=0` 仍是独立遗留项；不会因六模组重新定价自动消失。
- 42 区普通高阶武器/护甲仍临时维持旧市场，直到统一价格和商人权限可以原子切换。这是有意的过渡状态，不是最终方案。

### 12.6 备份、报告与恢复

- 完整变更前备份、归档定义和机器可读报告：`D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\Market_Backup\2026-08-12_structural_repair\`
- 详细统计：上述目录内 `REPAIR_REPORT.json`。
- 第一次校验因未识别 `FOG\...` / `Snafu\...` 子目录分类而中止，已从逐文件备份完整恢复后重新执行；诊断快照保留在 `2026-08-12_structural_repair_failed_partial`，不位于活动 Market 内，也不会被 Expansion 加载。
- 当前验证：172 个活动 Market JSON、32 个 Trader JSON、7 个 TraderZone JSON 和 1 个 MarketSettings JSON，共 212 个 JSON 均可解析；Trader 分类引用完整；5 个比特币 Trader 的可见/隐藏权限均只使用模式 0/3；独立 classname 重复数为 0。

---

**给后续模型/对话的固定指令：** 先读取本文件，再读取本次涉及的实际 JSON；不要只依赖本文的快照。所有修改要同时更新实际配置和本文件的当前基线/变更日志。若运行期文件与本文不一致，以实际文件为准，并在完成核对后修正文档。
