# DeerIsle 6.1 — Expansion Market 配置基线与变更日志

> **长期交接文档 / 后续操作前必读**  
> 此文件是本服务器 Expansion Market 的持续维护入口。以后无论切换模型、任务或对话，在修改市场配置前都必须先读本文件；完成任何价格、库存、买卖权限、物品增删或交易商调整后，必须同步更新“当前基线”和文末“变更日志”。

- 基线审计日期：2026-08-11（Asia/Shanghai）
- 审计范围：`profiles/ExpansionMod` 与 `mpmissions/empty.deerisle/expansion`
- 本次审计结果：只创建本文档，**未修改任何市场 JSON、交易商 JSON、区域 JSON 或 `.map` 文件**。
- 重要提醒：`traderzones/*.json` 中的 `Stock` 是运行期数据，会随交易和服务器保存而变化；本文记录的是 2026-08-11 的静态快照。

> **当前基线2026-10-02（第二次调价）：** 普通/黑市非载具按首次原价60%，黑市整车原包价50%百万取整；分级回收，各普通商品仍可买，黑市仅购买，零回收商品禁止出售，车辆配件0价隐藏。所有商店交易无声望门槛，积分/稀有度/死亡损失保持；ATM初始200万。价格、权限及声望静态验证PASS，部署待验。本段覆盖此前原20%/100%回收政策，完整记录见文末。

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
| `LargeVehicles` | 当前为空 | `ExpansionLHD`不存在，已于2026-08-29从活动配置退役。 |
| `VehicleKeys` | `ExpansionCarKey` | 载具钥匙 classname。 |
| `MaxSZVehicleParkingTime` | 1800 | 安全区载具停放时间。 |
| `SZVehicleParkingTicketFine` | 0 | 停车罚款。 |
| `SZVehicleParkingFineUseKey` | 1 | 停车罚款相关钥匙设置。 |
| `DisallowUnpersisted` | 0 | 未持久化物品未被全局禁止交易。 |
| `DisableClientSellTransactionDetails` | 0 | 客户端显示出售交易详情。 |

`NetworkCategories` 当前为空；该字段属于运行/网络生成数据，不应人工维护。

载具生成点：

- 陆地：2 个，约位于 `(5649.727539, 28.734999, 5417.433594)` 与 `(13400.003, 12.965, 9877.509)`。
- 空中：1 个，约位于 `(13419.766, 12.965, 9876.791)`。
- 水上：2 个，约位于 `(5217.702, 0.444, 9317.313)` 与 `(7773.341, 0.563, 6891.502)`。
- 火车：0 个。

## 4. 本服 Market 初始分类审计（历史，非当前基线）

本节177/3228/16组重复等数字是重建初期快照，不得用作当前活动基线。当前基线请以本文18.35节和`Project Manage/Market System Rebuild/MARKET-REBUILD-HANDOFF.md`为准：166 Market、3648 Item、5338 Variant、35 Trader、9 Zone、12362 Stock、211 JSON，当前验证器为0 warning/0 error。

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
- 分类权限引用总数（无后缀按 Expansion 默认模式 1 计）：模式 0 = 29，模式 1 = 88，模式 2 = 27，模式 3 = 21。手动物品模式 0/1/2/3 为 26/48/17/63。
- 所有 Trader 当前均无声望、阵营或任务限制。

下表中“分类模式”按 `0/1/2/3` 统计；“手动物品”也是相同顺序：

| Trader 文件 | 显示名/用途 | 货币 | 分类模式 0/1/2/3 | 手动物品 0/1/2/3 |
|---|---|---|---:|---:|
| `Aircraft.json` | Aircraft | Hryvnia | 0/0/0/2 | 2/1/0/1 |
| `AJW.json` | AJW武器商人 | Hryvnia | 0/5/2/1 | 0/0/0/0 |
| `AP_Armor.json` | 高级护甲商人 | Bitcoin | 14/0/0/0 | 0/0/0/0 |
| `AP_Rookie.json` | 新手区护甲商人 | Hryvnia | 0/7/2/0 | 0/0/0/0 |
| `Attachments.json` | Attachments | Hryvnia | 0/5/0/0 | 0/40/0/1 |
| `Better_Cars.json` | 高端载具商人空壳（待 Carpack） | Bitcoin | 0/0/0/2 | 0/0/0/1 |
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
| `MagLoader.json` | 装弹器&消音器 | Bitcoin | 2/2/0/0 | 0/0/0/0 |
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

截至 2026-08-23，`mpmissions/empty.deerisle/expansion/traders` 中共有 5 个 `.map` 文件、28 个实体放置。每行基本格式：

```text
<Trader实体类>.<Traders配置文件基名>|<位置>|<朝向>|<装备>
```

所有 28 个放置引用都能找到对应 Trader JSON，且都位于至少一个 TraderZone 内。

| `.map` 文件 | 主要绑定 |
|---|---|
| `42.map` | `MagLoader`、`Better_Cars`、`BIG_GUNS`、`AP_Armor`、`Defibrillator` |
| `AP_WEAR.map` | `AP_WEAR` |
| `QPK_Materials.map` | `QPK_Materials` |
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
| `42.json` | 黑市 | `(13383.530, 12.910, 9865.882)` | 250 | 100% | -1（回退全局） | 372 |
| `AP_WEAR.json` | AP WEAR 服装商人 | `(3460.711, 34.494, 6429.530)` | 1 | 100% | -1 | 485 |
| `Boat_Trader_Rookie.json` | 船只商人 | `(7786, 1, 6831)` | 200 | 100% | -1 | 233 |
| `Boat_Trader_Spire.json` | 船只商人 | `(5223.367, 1.571, 9303.166)` | 200 | 100% | -1 | 233 |
| `QPK_Materials.json` | QPK 制作材料商人 | `(5623.563, 28.735, 5394.646)` | 1 | 100% | -1 | 6 |
| `Rookie_Trader.json` | 物资交易中心 | `(5630, 28.740, 5392.5)` | 200 | 100% | 30% | 5,049 |
| `Waldoboro.json` | 高级武器商人 | `(9557.933, 0, 8937.799)` | 200 | 100% | -1 | 1,119 |
| `WestBrook.json` | 高级护甲商人 | `(3445, 0, 6424)` | 200 | 100% | -1 | 2,964 |
| `World.json` | World Trader Zone | `(7500, 0, 7500)` | 15000 | 100% | -1 | 1,872 |

实际最近区域映射：

- `42.map` 的交易商 → `42.json`。
- `AP_WEAR.map` → `AP_WEAR.json`；专用区半径 1 米，避免捕获 3.995 米外的 `FOG_Trader`。
- `QPK_Materials.map` → `QPK_Materials.json`；专用区半径 1 米，避免捕获 2.710 米外的 `Clothing`。
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

3. **3 种大口径弹药曾低于唯一比特币面值。**  
   这是历史问题，已收口。`gcgn_ammo_408chey` 和 `gcgn_ammo_50cal` 已迁入 Hryvnia `Snafu_Ammo`，固定价 1,000，由 `Rookie_Snafu` 以模式 2 只回收；不再经过 `BIG_GUNS` 比特币购买路径。`snafu_ammo_145cal` 也已随爆炸物/大口径市场收口处理。

4. **16 组重复 classname 会触发官方 Market 配置错误。**  
   官方 `ExpansionMarketCategory.CheckDuplicate` 会拒绝后加载的重复项，并记录 MarketCfgError。12 组参数相同，主要造成日志错误和分类缺项风险；以下 4 组参数不同，加载先后还会改变最终有效配置：

   - `expansionbiggyrocopter`：32,000,000 固定价 vs 1,000,000–2,000,000 动态价。
   - `expansiongyrocopter`：22,000,000 固定价 vs 500,000–1,000,000 动态价。
   - `expansionmh6`：102,000,000 固定价 vs 1,500,000–3,000,000 动态价。
   - `expansionhydraulichoses`：0 vs 54,045。

### 9.2 确认运营意图后处理

1. **7 个已放置 Trader 商品配置为可买卖，但库存阈值是 `0 / 0`。**  
   `nbcbootsgray`、`nbcjacketgray`、`nbcpantsgray`、`gasmask`、`gp5gasmask`、`nbcglovesgray`、`nbchoodgray` 当前模式均为 1，但 `MaxStockThreshold = 0`。官方逻辑不会把 `0 / 0` 识别为静态库存，购买库存也无法建立；实际效果更接近只回收。若它们是稀有战利品，应明确改为模式 2；若希望可购买，应设置正数库存阈值。

2. **18 个 Variant 由多个父条目或同一父条目重复声明。**  
   主要集中在 FOG 服装/护甲以及 LandCruiser 门变体。官方加载器会拒绝后续 Variant 归属，并不是无害的记录重复。**状态：已于 2026-08-12 20:27 修复**；15 个跨父级项已归并到唯一语义父项，3 个同父项重复值已去重。

3. **`expansion_ammo_taser` 的 1 Hryvnia 占位价已解决。**  
   当前活动 `Ammo.json` 固定价为 500 Hryvnia，`SellPricePercent=5`；`Weapons` Trader 为模式 1，玩家可购买并低价回收。该项不再是遗留项。

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

- `Project Manage\Market System Rebuild\analysis\EXPANSION_MARKET_REBUILD_ANALYSIS.ipynb`：已执行的 312 条受管装备交叉审计。
- `Project Manage\Market System Rebuild\analysis\EXPANSION_MARKET_REBUILD_CROSSWALK.csv`：classname、A1—A6、模组、family、当前价格、Trader 权限和可达性逐条映射。

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
| 3 个低于比特币最小面值的弹药 | 已解决 | GCGN 两种弹药已迁入 Hryvnia `Snafu_Ammo` 且 Mode 2 只回收；不再走 BIG_GUNS 比特币路径 |
| 16 组重复 classname | 不会自然解决 | 车辆/部件重复项需独立清理，否则继续触发 MarketCfgError |
| 7 个 NBC/面具 `0/0` 但模式 1 | 必须在重构解决 | 这是跨阶门槛物资，应明确模式 2 或 3，不能恢复 NPC 新库存 |
| 18 个多父级/重复 Variant | 已解决 | 15 个跨父级归并、3 个同父项重复去重；不改价格、库存阈值和 Trader 权限 |
| Taser 弹药售价 1 | 已解决 | 当前固定价 500 Hryvnia、5% 回收，`Weapons` Mode 1 |
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
| 2026-08-12 20:27 | Codex | 复核 Expansion 官方源码/Wiki，消除 18 个 Variant 重复归属 | 5 个活动 Market JSON；新增隔离工作区、官方源码基线和只读校验器 | FOG Shirt/Pants/JPC2/Ghillie，LandCruiser 门 | 18 个后续声明会报错→0 个重复 Variant | 价格/库存/Trader/Zone 未改；212 个 JSON、5991 条 Variant、12030 个 Zone 键全量校验 0 错误/0 警告 |
| 2026-08-12 20:58 | Codex | 在隔离目录建立候选经济账本 v1 | 新增 13 材料 CSV、312 装备 CSV、公式工作簿、生成器、方法说明和摘要；更新 README/Guide/HANDOFF | 260 武器、49 护甲、3 受管弹匣及 13 种合成材料 | 无活动 Market/Trader/Zone/Settings/map 变更 | 候选值尚未获准上线；5 个工作表公式/视觉验证通过，4 项受管账本安全不变量通过；外围附件/弹匣/弹药仍待接入 |
| 2026-08-12 22:33 | Codex | 用 active types/config/官方源码建立外围候选价并接入套利审计 | 新增外围生成器、classname 证据、外围账本、套利生成器/审计；更新核心生成器、工作簿、README/方法/Guide/HANDOFF | 870 外围 classname；46 弹药、37 弹药盒、289 弹匣、498 附件类 | 无活动 Market/Trader/Zone/Settings/map 变更 | blocked/projectile review=0；donor 12,000→8,500；2,444 审计行正收益闭环 0；8-sheet 公式/视觉验证通过 |
| 2026-08-13 | Codex | 将 Market 重构临时工件、分析表、工具和临时官方源码集中到 Project Manage | 新建 `Project Manage\Market System Rebuild`；迁移 workspace、3 个分析工件、HANDOFF、预览 PNG 和冻结源码；修复工具与文档路径 | 项目文件组织，不涉及 classname/Trader/Zone | 旧散落路径与 `/private/tmp` 依赖→统一项目目录；无活动 Market/Trader/Zone/Settings/map 变更 | 迁移后重跑生成器、2,444 条套利审计与 212 JSON 校验；详细操作见 `Project Manage\Market System Rebuild\MARKET-REBUILD-HANDOFF.md` |
| 2026-08-13 10:16 | Codex | 完成候选经济 C1 用户审核包与保守首发建议 | 新增 C1 决策 CSV、异常 CSV、summary JSON、审核 MD、8-sheet XLSX 和生成器；更新 README/Guide/HANDOFF | 13 材料、312 受管装备、870 外围；52 个 TTC Mode 3 部件 | 候选建议 `QPK_FAR` 150,000→100,000；受管 `212/100`→`138/174`；外围 `741/77/52`→`521/201/144/HOLD 4`；无活动配置变更 | 15 项决定仍为 PENDING；645 个异常 classname；8/8 sheet 视觉通过、公式错误 0、XLSX ZIP 完整；活动配置仍 0 warnings/0 errors |
| 2026-08-13 10:36 | Codex | 冻结“玩法获取优先、黑市高价回收货币”原则并纠正 C1 方向 | 新增原则文档；更新 README、C1 报告、Guide、HANDOFF | A1—A6 获取渠道、`QPK_FAR`、普通商人和黑市 | 撤回 `QPK_FAR=100,000` 和“A1—A3 全部正常买卖”建议；C1 v1 改为历史审计 | A6 一次结算约 2 FAR；旧价整包材料理论回收 322,749.60，原活动配置未改 |
| 2026-08-13 10:52 | Codex | 读取声望商店项目并复核 AP/SNAFU 当前实际迁移状态 | 新增状态核查报告；更新原则、README、Guide、HANDOFF | A3—A6、AP、SNAFU、AP_Armor、BIG_GUNS | 冻结 A3—A4 高价直购例外；当时 A6 声望直购口径仍待后续决定；无活动配置变更 | AP_Armor/BIG_GUNS 仍在 42；35 个可见 AP、14 个 SNAFU classname 仍由黑市出售，候选重定价未上线 |
| 2026-08-13 11:05 | Codex | 冻结 A6 成品回收权限并明确 AP/SNAFU 原子修复安排 | 更新原则报告、状态报告、Guide、HANDOFF | A6 成品枪械、AP、SNAFU、AP_Armor、BIG_GUNS | A6 改为 NPC 永不直售、玩家可低额回收，声望不得绕过禁购；无活动配置变更 | AP/SNAFU 仍待一次性迁移；AP 高阶护甲直售规则待用户确认 |
| 2026-08-13 11:12 | Codex | 冻结 AP 终局护甲规则并生成 AP/SNAFU 逐 classname 权限矩阵 | 新增生成器、155 条 CSV、报告和摘要；更新原则/状态/README/Guide/HANDOFF | AP 25、SNAFU 130 条受管成品 | A6 枪械和终局护甲固定 NPC 禁售、玩家低价回收；无活动配置变更 | 149 条 active types 精确命中、155 条 config 精确命中、阻塞 0；104 条普通买卖、51 条只回收，价格仍待建模 |
| 2026-08-13 11:20 | Codex | 登记 AP WEAR/AWEAR 服装独立 NPC 遗留项 | 更新 Guide、HANDOFF | `AWEAR_types_*` 服装、未来独立 Trader/NPC | 本轮不纳入市场修改 | 当时 NPC 位置未定；该历史待办已于 2026-08-23 解决，见 18.27 |
| 2026-08-13 13:35 | Codex | 重新整理市场重构完整推进逻辑和遗留项目 | 新增当前路线图；更新 README、Guide、HANDOFF | 13 材料、312 受管装备、870 外围、42 黑市、声望、AP WEAR | 明确先补完整权限矩阵，再建价格、staging、验证和原子上线；无活动配置变更 | AP/SNAFU 155 条已完成；剩余 157 条受管装备及 870 条外围仍需权限复核 |
| 2026-08-13 14:05 | Codex | 冻结全目录 types 前置核对、黑市延期和删档写入要求 | 更新路线图、原则、状态、README、Guide、HANDOFF | 159 个 types 文件快照；AP/SNAFU 与 42 迁移边界 | 当前只重构普通市场；仅迁出 42 中应属普通体系的 A1—A6 枪械/护甲，其他黑市不动 | A6 仍为 NPC 禁售、玩家低额回收；活动 Market/Trader/Zone/types 未改；下一步生成逐 classname types 差异报告 |
| 2026-08-13 14:29 | Codex | 完成全目录 types / Market 交叉核对 v1 | 新增根节点扫描工具、2 份合同、5 份报告；更新 README/路线图/Guide/HANDOFF | 16,830 active classname、4 个 FOG 新增项、31 个 active 重复项、2 个无扩展名 Market 文件 | 159 个文件名快照→163 个根节点 CE 文件；无活动配置变更 | 23 个重复项 CE 参数冲突；AJW 旧弹匣确认排除；Dune Shield 留待黑市阶段；下一步裁决 35 个 classname |
| 2026-08-13 15:49 | Codex | 应用四项用户裁决并生成剩余 157 条权限矩阵 | 新增决策合同、生成器、权限/重复/FOG/清理报告与备份；修改 `FOG/FOG_Misc.json`、Bastardo loot、两份 Hardline、README/路线图/Guide/HANDOFF | 4 个 FOG 新类、AJW 旧 M82 弹匣、6 个 Terje Radiation 药品、157 条 AJW/TTC/FOG/MMG 受管装备、31 个 types 重名项 | 三枚 FOG Big Patch 加入唯一父项 Variant，唯一 Variant `5991→5994`；AJW 活动引用改为现行类；两份 Hardline 各删除 6 个未加载辐射药品键；Trader/Zone/types 未改 | 157 条目标模式 `106/51`、classname 阻塞 0；31 项纠正为 28 个清理候选/2 个有意覆盖/1 个大小写碰撞；活动 Market 0 warnings/0 errors |
| 2026-08-13 16:18 | Codex | 完成 870 条外围逐 classname v2 权限复核与统一合同 | 新增 AJW、SNAFU、TTC+原版/Expansion 三组专项生成器/合同/报告及统一生成器、CSV、MD、summary；更新 README/路线图/Guide/HANDOFF | AJW 265、SNAFU 261、TTC 189、原版/Expansion 155；52 个 TTC 结构件；BIG_GUNS 漏表 14 项 | 旧 v1 候选 `741/77/52` → v2 审查建议 `Mode 1/2/3/HOLD=572/205/15/78`；52 个 TTC 结构件由旧 Mode 3 纠正为 HOLD | 未修改活动 Market/Trader/Zone/types；权限和价格均未获上线批准；发现 SNAFU 旧类、Expansion .338 projectile 与战略小容量弹匣等账本问题 |
| 2026-08-13 16:20 | Codex | 完成 AP Variant、隐藏附件和完整护甲范围专项审查 | 新增 77 行 AP 结构计划与专项报告；更新 README/路线图/Guide/HANDOFF | 646 个活动 AP classname、29 家族/114 个成品护甲、6 个 mode 3 部件、AP 1.6 新增 13 项 | 原 25 代表项矩阵→发现 4 个漏家族/13 条；绿色终局头盔黑附件继承、6B43 mode 0 漏算和 9 个跨基类 Variant 已定位 | 未修改活动配置；77 条均有 active types/config 证据；原“11 条冲突路径”不得继续当精确 classname 数 |
| 2026-08-13 16:42 | Codex | 展开并冻结 AP 114 条、建立 SNAFU 旧类替换计划并补 BIG_GUNS 14 项 | 新增 AP v3/v4 生成器、合同、报告和 summary；SNAFU 旧类 CSV/MD；BIG_GUNS 生成器/CSV/MD；更新 README/路线图/Guide/HANDOFF | AP 29 家族/114 条；SNAFU 10 个 HOLD/179 个活动引用；BIG_GUNS 3 枪+8匣+3弹药 | AP 当前精确 `mode0/mode2/无路径=22/68/24`，v4目标`mode1/2=76/38`；旧 SNAFU 9 项有替代、1 项无替代；BIG_GUNS 12条只回收建议、2条HOLD | 未修改活动配置；四个 AP 漏家族冻结为 Kevlar-mid A2、其余三家族 A5；AP v4 HOLD=0、证据阻塞0 |
| 2026-08-13 17:08 | Codex | 合并完整权限范围并生成规范执行视图 | 新增全局生成器、1,285 行 CSV、MD 与 summary；更新 README、路线图、Guide、HANDOFF | 受管成品 404、外围/支持物 881；SNAFU 9 个旧类原子替换 | 原始建议 `839/351/15/80`；旧类按计划去重后的 1,279 条规范执行视图为 `840/353/15/71`；A5 共 96 | 历史 v1 快照；已被 18:20 的 global v2 取代，禁止用于 staging |
| 2026-08-13 18:20 | Codex | 应用用户五组决策、清理高置信 types 并建立 global v2 | 新增/重生成 AP 来源、玩法缺口、SNAFU Mod_Edit、旧枪审计、外围 v3、受管 v3 与全局 v2 工件；更新 README、路线图、Guide、HANDOFF；备份并修改 5 个活动 types | 1,279 个规范 classname；865 条外围；114 条 AP；129 条 SNAFU 受管；31 条来源登记；27 个 types classname | A5 全部禁售低回收；普通 SNAFU 配件高价直购低价回收；目标权限 `928/266/15/70`；删除 28 个重复 XML 节点，活动碰撞 31→4 | Market/Trader/Zone/价格未改；116 个 active types 可解析；活动 Market 仍为 172/3164/5994/32/7/12030/212、0 warnings/errors |
| 2026-08-13 20:22 | Codex | 补齐 AP-150/MMG 范围、冻结 Workbench 与 34 节点计划，建立 global/source/price v3 | 新增 AP-150、AP 内部基准、MMG 四色、global v3、source v3、price v3、Workbench/canonical 工件；更新 README/路线图/Guide/HANDOFF | 1,296 个规范 classname；49 条来源登记；314 制作 + 742 拆解；AP 两组各 13 项；MMG 四色 | 权限 `934/277/15/70`，A5=94/A6=43；价格 1,226 公式 + 70 HOLD；普通配件高价直购/低回收，终局禁售/低回收，无来源不用 NPC 补洞 | 本阶段未修改活动 Market/Trader/Zone/Workbench/价格/地图/声望；NPC 具体价仍为 0 |
| 2026-08-13 20:45 | Codex | 完成 13 种 QPK 材料经济输入事实审计 | 新增材料审计生成器、CSV、MD、summary；更新 README/路线图/Guide/HANDOFF | 13 种材料；312/314 制作配方；1,713 输入条目；1,409 拆解产出条目 | 范围和结构事实已冻结；旧周发行数字撤回为历史锚；正式材料价仍为 0 | 13/13 Mod_Edit 类证据；active types/Market/Trader/Zone/global v3 路径均为 0；未修改活动配置或 price v3 |
| 2026-08-13 21:05 | Codex | 完成 11 种输入专用 QPK 材料真实玩法来源审计 | 新增来源审计生成器、CSV、MD、summary；更新 README/路线图/Guide/HANDOFF | 11 种材料；CJ、SearchForLoot、Key6/7/8/103/200—204 | 11/11 有 CJ 可达主路径、完整零来源为 0；可量化运行时周供应项为 0，正式价格仍为 0 | SFL 在 DayZ 1.29 下挂运行兼容门禁；Key7/8 为未引用补充路线；未修改活动配置或 price v3 |
| 2026-08-13 21:25 | Codex | 完成 13 种 QPK 材料供应规划情景审计 | 新增供应规划生成器、CSV、MD、summary；更新 README/路线图/Guide/HANDOFF | 13 种材料；CJ、SFL、Workbench 拆解、异常重启 | 用户确认 4h/6day/42week 规划情景；不等于 runtime/telemetry，正式价格仍为 0 | 13/13 CJ；SFL 4 项与拆解 2 项运行验证 0；无去重控制器部署证据；未修改活动配置或 price v3 |
| 2026-08-13 21:45 | Codex | 同步 QPK 当前 CJ vs v4 待批需求偏差审计 | 更新 README/路线图/Guide/HANDOFF；登记已冻结生成器、CSV、MD、summary 及 SHA | 13 种 QPK；12 项 v4 候选目标 + `QPK_Calibrator` 无目标 | v4 仍为 `DESIGN_POLICY_NOT_RUNTIME_CONFIG`；六核心 P2P 允许/NPC 售卖与回收禁止；正式价格仍为 0 | init 低 capture 前三 0.166227%/0.497719%/0.559037%，仅为偏差门槛而非玩家实得；Bolts/MetalParts 拆解未并入 CJ；未修改活动配置 |
| 2026-08-13 22:00 | Codex | 同步 QPK Calibrator 消耗、供应与治理审计 | 更新 README/路线图/Guide/HANDOFF；登记生成器、CSV、MD、summary 及 SHA | 314 制作、295 条 A2–A6、294 条一次性消耗、1 个 MMG 例外、742 拆解 | 可维护里程碑工具为推荐未批准；v4 无目标；正式价格仍为 0 | 三项用户决策待定；未修改 Workbench、Mod_Edit、CJ、任务或活动市场 |
| 2026-08-14 00:31 | Codex | 退役 MJO/ALE/BZ，并清空 42 旧比特币车辆目录 | 修改/移出 32 个活动文件；新增备份、清理工具、32 行文件合同、959 行 classname 排除合同、报告与 summary | MJO 148；ALE/BZ 残留；旧车辆 21 分类、207 Item、602 Variant、809 classname | 172→151 Market；3164→2895 Item；5994→5306 Variant；12030→11091 Zone 键；`Better_Cars` 保留空壳，Carpack 未加入 | 两次预检均在写入前安全中止；最终 `--check` 与全量 Market 校验 PASS，0 warning/error；32 份备份可恢复 |
| 2026-08-14 09:18 | Codex | 核清全局活动 Market 与 price v3 的真实覆盖边界 | 新增覆盖生成器、8,152 行 CSV、中文报告和 summary；更新四份共同文档 | 活动 8,082 唯一 classname；price v3 1,296 | 活动命中 1,226：1,156 公式待数字 + 70 HOLD；范围外 6,856；合同未进活动 70；live 数值 0 | 纠正“price v3 等于全服全部商品”的错误前提；只读审计，活动配置未改；`--check` PASS |
| 2026-08-14 10:52 | Codex | 一次性收口战斗 Market 结构和 SNAFU 弃用类 | 修改 Market/Trader/Zone/Hardline/CJ/Loadout/spawnable/Workbench；新增两套备份和两支可复验工具 | AP 同色附件/功能 Variant；20 个缺定义；42 AP/SNAFU；14 个弃用 SNAFU classname | AP/SNAFU 目标商品迁出42；21个大口径对象迁入普通SNAFU；14旧类→13规范类；Workbench 314/742→312/737 | 全量 148 Market、2,887 Item、5,293 Variant、32 Trader、7 Zone、11,055 Stock、188 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true` |
| 2026-08-14 11:36 | Codex | 非战斗第一批、钓鱼骨架、AP WEAR/QPK 独立商人和 CarPack 替换 | 修改 41 个普通 Market、13 个 Hryvnia Trader、Fishing/Better_Cars/42/World；新增 AP WEAR/QPK/CarPack Market 与 2 个 Trader | 普通 709 Item；AP WEAR 485；QPK 普通材料 6；CarPack 11 车/72 随车件 | 普通商品回收5%；鱼类数字不动；核心QPK/Calibrator不进NPC；CarPack维持旧车价 | 159 Market、3,461 Item、5,293 Variant、34 Trader、7 Zone、11,629 Stock、201 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true` |
| 2026-08-14 17:51 | Codex | DF COLLECTION 51件回收价格分阶下调 | 修改 `Market/DF_Collection.json`，复用非战斗施工工具和备份/staging | 51 Item；7个旧价格档 | 5,000不变；10,000/20,000/35,000/50,000/75,000/100,000依次改为9,800/19,200/32,550/45,000/63,750/80,000；仍为Mode 2只回收 | 精确映射PASS；爆炸物引用0；159 Market、3,544 Item、5,299 Variant、34 Trader、7 Zone、11,708 Stock、201 JSON，0 warning/error |
| 2026-08-17 10:22 | Codex | 合并 AP 旧 Bitcoin 分类、补齐 AP/SNAFU 受管定义并清理 42 残留 | 3 个 Market、2 个 Trader、3 个 Zone、2 份 Hardline；6 个旧 AP Market 文件退出加载 | AP 114、SNAFU 129；42 普通 AP/SNAFU；Black Retext 3 分类 | AP/SNAFU 目标定义与权限全覆盖；旧 AP 文件 6→0；42 普通键→0；Black Retext 不变 | 专项 PASS；153 Market、3,572 Item、5,317 Variant、34 Trader、7 Zone、11,774 Stock、195 JSON，0 warning/error |
| 2026-08-17 14:30 | Codex | 收口 42 除颤器商人，把普通维修工具迁往中心商人只回收 | 修改 `Defibrillator.json`、`Components.json`、`Weapons.json`、`42.json`；新建 2 个 Market | `defibrillator`、`electronicrepairkit`、`weaponcleaningkit` | 除颤器保持 42 Mode 0/40,000；两工具迁 Components/Weapons Mode 2，40,000×5%=2,000 满状态回收上限 | `DEFIBRILLATOR_MIGRATION_VALID=true`；155 Market、3,572 Item、5,317 Variant、34 Trader、7 Zone、11,772 Stock、197 JSON，0 warning/error |
| 2026-08-17 15:44 | Codex | 按 Mod_Edit 实际属性统一调整 42 黑市 MMG/蝙蝠宝贝/追踪者装备 | 8 个 Market JSON | 73 Item；MMG 5套、Admin、Set_Baby、hNz | 72 件改价；MMG五套81M–84M/套，Admin26M，蝙蝠宝贝40M，hNz组23M；Mode 0不变 | `BLACK_MARKET_MODEDIT_REPRICE_VALID=true`；全量数量不变，0 warning/error |
| 2026-08-17 22:48 | Codex | 将 BRTX 约 5% 操控强化和 MagLoader 实际功能纳入黑市定价 | 4 个 Market JSON | 220 把 BRTX；3 种 MagLoader | Scar-H/Kivaari/Alligator 3M/5M/12M→4M/8M/15M；Loader 4M/6M/8M→3M/5M/8M | `BRTX_MAGLOADER_REPRICE_VALID=true`；222 Item仅价格字段改变；155 Market、3,572 Item、5,317 Variant，0 warning/error |
| 2026-08-18 09:35 | Codex | 将 DMT 最低标准 FLIR 档接入 CDS 所在黑市 NPC | 新建 1 Market；修改 1 Trader、2 Zone | 6 个 `DMT_FLIR_*`；`MagLoader` Trader | 历史方案为主物品内部值25M/Mode 0/库存1/随附9V电池，递归结算实际占用26 BTC；现已由18.36取代 | `DMT_STANDARD_FLIR_BLACKMARKET_VALID=true`；156 Market、3,578 Item、5,317 Variant、11,784 Stock，0 warning/error |
| 2026-08-18 16:01 | Codex | 接入 Inedia T1/T2 医疗商品 | 新建 6 Market；修改 2 Trader、3 Zone、2 Hardline | T1 15身份；T2 14身份 | T1中心Hryvnia Mode1/5%回收；T2黑市Bitcoin Mode0；T3排除 | `INEDIA_MARKET_CONTRACT_VALID=true`；162 Market、3,599 Item、5,325 Variant、11,842 Stock，0 warning/error |
| 2026-08-23 | Codex | 落地 AP WEAR/QPK 独立 NPC 与专用 TraderZone | 新建 2 map、2 Zone；同步 HANDOFF/路线图/全局索引 | AP WEAR 485；QPK 普通材料 6 | Mirek NPC；Zone 半径 1 米隔离相邻旧 Trader；价格与权限不变 | 162 Market、3,599 Item、5,325 Variant、34 Trader、9 Zone、12,333 Stock、206 JSON，0 warning/error |
| 2026-08-23 | Codex | 调整中心 Vehicles/P2P、车辆刷新点和 Trader 外观 | 修改 2 map、P2PTrader_1、MarketSettings；同步文档 | 27 名人形 Market Trader、1 名 P2P、2 套外观、1 个陆地刷新点 | 除 Vehicle_Parts Seth 外全部 Mirek；Fishing 渔业套装；Spire 补鞋 | 类型/坐标/Zone/刷新选择专项 PASS；全量数量不变，0 warning/error |
| 2026-08-24 | Codex | 重构容器/MMG Storage并统一全市场无限库存 | 新建MMG Storage Market与可重复执行工具；修改容器、帐篷、Building/Components Trader、7个Zone及HM Secure重复奖励 | 7063个可购identity；2492个可见父项+77个递归依赖父项；3种Safe；24个MMG套件 | 所有可购商品原生1/1静态库存；Safe/MMG仅回收；容器三分类只归BuildingSupplies | 165 Market、3618 Item、5338 Variant、35 Trader、9 Zone、12367 Stock、210 JSON；0 warning/error；待重启/RPT/UI实测 |
| 2026-08-24 | Codex | 接入 HEROCLAN 黑市特攻 Duck/Rabbit 服装 | 新建 Set_Duck/Set_Rabbit Market；AP_Armor 增加两条 Mode 0 分类 | Duck 6、Rabbit 27，共33个公开服装类 | 对应部位与 Bat Baby 同价；同部位各颜色同价；Bitcoin只购买 | 167 Market、3651 Item、5338 Variant、35 Trader、9 Zone、12367 Stock、212 JSON；0 warning/error；待PBO/重启/RPT/UI实测 |
| 2026-08-24 | Codex | 落地 HP CRAFTER 中心 Mirek 商人 | 修改 `ROOKIE_TRADER.map`；同步 Guide/HANDOFF/路线图/总索引 | 1个NPC、既有8件HP CRAFTER商品 | 复用中心Zone；不新增Zone/价格/权限/库存；工作坊外观 | NPC唯一、距中心20.199米、最近旧NPC 16.717米；全量167/3651/5338/35/9/12367/212静态通过 |
| 2026-08-25 | Codex | 将 BRTX 三种独立扩容弹匣接入 42 黑市 | 修改3个Market、2个Zone、2份Hardline；复用`BIG_GUNS` | Kivaari 35、SCAR-H 150、Alligator 20 | 实付10/6/20枚BTC；内部价10M/6M/20M法币等值，分别高于对应枪械25%/50%/33.3%；Mode 0只购、1/1库存 | 全量166/3649/5338/35/9/12363/211，0 warning/error；四个BRTX PBO与实机兼容性待验 |

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
7. 玩家主要通过探索、战利品、副本、任务、合成、拆解和玩家交易获得物品；普通商人不得成为跳过成长玩法的快捷入口。
8. 黑市可以提供远强于原版的装备和附件，但应以高价格、只买不卖的方式承担货币回收作用；稀缺物品价值不能直接等同于 NPC 现金回收价。
9. 制作核算价值、NPC 回收现金和黑市购买价格必须分别定价。A5/A6 核心材料不得仅因稀有就获得高额回收价，高阶活动也不得变成稳定印钞途径。
10. A3—A4 成品枪械可作为高价直接购买例外；A6 成品枪械不得由任何 NPC 直接卖给玩家，声望、任务和有限供应也不能绕过该禁购规则。玩家可以向 NPC 出售 A6 成品，但只能获得受控的低额残值。
11. AP 的 A6/终局成品护甲与 A6 成品枪械执行同一规则：NPC 禁售、玩家可低价回收、声望或任务不能形成直购例外。
12. 每次改商店物品前必须按 XML 根节点全量扫描 `Deerisle 6.1` 内 types/spawnabletypes，不能依赖文件名；并区分 `cfgeconomycore.xml` 活动注册、未注册更新候选和历史副本，与 Market、上一版清单和模组 config 交叉确认，不得自动上架所有 types classname。
13. 所有 Market/Trader 修改必须沿用当前文件与 Expansion 官方代码结构：Market `m_Version=12`、Trader `m_Version=13`、原有字段/数组层级、分类模式、全局 classname 唯一、Variant 单父归属和 `SpawnAttachments` 语义均不得变形。
14. 当前重构只处理普通市场。A1—A6 枪械/护甲归入 WestBrook/Waldoboro；A6 仍只回收。黑市商品、删换和价格以后独立处理，本轮仅迁出 AP/SNAFU 等普通装备旧路径。
15. 本次服务器删档。候选先在 workspace 验证，批准后必须写入 `Deerisle 6.1` 真实 Market、Trader、TraderZone、任务地图和必要设置，而不是只保留 staging。
16. A5 成品与 A6 执行相同购买权限：NPC 禁售、玩家可低价回收，声望不得形成直购例外；A5 与 A6 的具体回收额仍应按阶段和经济风险分别计算。
17. 普通外围配件原则上允许高价直购、低价回收；高容量弹匣、重口径资源和终局战略附件按逐 classname 合同只回收或 HOLD，不能因名称属于“配件”就整类开放。

### 12.2 本轮已经实际应用的修改

- `AP_Armor.json`：`Bitcoin-AP-Helmet-Parts:0` → `Bitcoin-AP-Helmet-Parts:3`。AP 头盔附件继续保持零价依赖，但不再作为可见免费商品。
- `MagLoader.json`：两个比特币消音器分类补全 `:0`，所有可见比特币商品现均为 buy only。比特币消音器的 `SellPricePercent` 从 `0.2` 修正为 `20.0`；虽然模式 `0` 会阻止实际回售，数值本身仍保持语义正确。普通 `Muzzles.json` 中相同的两处 `0.2` 笔误也同步改为 `20.0`。
- `Better_Cars.json`：隐藏依赖由重复的 `Bitcoin_Batteries` / `Bitcoin_Vehicle_Parts` 改为唯一全局分类 `Batteries:3` / `Vehicle_Parts:3`。共享的 `expansionhydraulichoses` 定义改为零价，继续只作为隐藏随车依赖。
- NBC/防毒系列：7 个独立 Market 父项的库存阈值由 `0/0` 改为 `1/100`；灰/黄/白变体共 16 个 classname 在 `Clothing.json` 或 `Clothing_Accessories.json` 中显式设为模式 `2`。玩家不能从 NPC 购买，但可向对应商人出售。
- 16 组独立 classname 重复全部归并，当前活动 Market 的独立重复数为 `0`。
- 49 个无交易/依赖路径的独立定义已归档；另外归档了 15 个重复副本。活动 Market 文件由 177 个变为 172 个；该次结构修复结束时含 3164 个独立定义和 6009 条 Variant 记录。
- Variant 归属修复移除 18 条重复声明后为 5991 条；2026-08-13 新增 3 个经确认的 FOG Big Patch 唯一 Variant，当前记录为 5994 条，唯一 Variant 也为 5994，多父级/同父重复数为 0。
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

- 已新增 `Project Manage\Market System Rebuild\analysis\EXPANSION_MARKET_REBUILD_MIGRATION.csv`，为 312 条受管装备记录目标区域、目标 Trader、目标货币和迁移状态。
- 护甲目标区为 `WestBrook`，枪械目标区为 `Waldoboro`，结算货币统一为 `expansionbanknotehryvnia`。
- 本轮**没有**立即删除 42 区的 `AP_Armor` / `BIG_GUNS` 放置或切走其分类。原因是统一 A1—A6 价格表和最终买卖权限尚未定稿；现在半迁移会造成商品缺失、旧比特币价在 Hryvnia 商人出现，或同一物品多币种并存。
- 正式切换必须作为一次原子变更完成：确定统一价格 → 修改 Market → 修改目标护甲/武器 Trader → 移除 42 区普通装备引用/放置 → 精确处理受影响 Zone 库存 → 完整验证。

### 12.5 仍会影响后续重构的问题

- 13 种材料、312 条受管装备和 870 个外围 classname 的候选账本已生成，2,444 条套利/转换路径无正收益闭环；但所有数字仍缺 wipe telemetry 和用户审批，不能写入活动 Market。
- 13 种合成材料的新回收商人仍未创建。旧 Mode `2`、单位回购价、周发行估算和监控线已由玩法获取优先原则撤回，只作历史锚。13/13 均有 CJ 配置路径，4h/6day/42week 规划情景已建立，但它不是 runtime/telemetry；当前尚需真实供应证据、内部价值、核心/普通回收策略和材料周发行预算。
- 18 个 Variant 重复归属已解决；该项已从后续经济账本阻塞项移除。
- Taser 弹药已以 500 Hryvnia/5% 回收写入活动 Market；GCGN 两种大口径弹药已迁入 Hryvnia `Snafu_Ammo` 并以 Mode 2 只回收。这三项不再是遗留项；当前只剩 `DisallowUnpersisted=0` 需独立安全策略决定。
- 42 区普通高阶武器/护甲仍临时维持旧市场，直到统一价格和商人权限可以原子切换。这是有意的过渡状态，不是最终方案。

### 12.6 备份、报告与恢复

- 完整变更前备份、归档定义和机器可读报告：`D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod\Market_Backup\2026-08-12_structural_repair\`
- 详细统计：上述目录内 `REPAIR_REPORT.json`。
- 第一次校验因未识别 `FOG\...` / `Snafu\...` 子目录分类而中止，已从逐文件备份完整恢复后重新执行；诊断快照保留在 `2026-08-12_structural_repair_failed_partial`，不位于活动 Market 内，也不会被 Expansion 加载。
- 当前验证（2026-08-14 17:51）：159 个活动 Market JSON、34 个 Trader JSON、7 个 TraderZone JSON和 1 个 MarketSettings JSON，共 201 个 JSON 均可解析；3,544 个独立定义、5,299 条唯一 Variant、11,708 个 TraderZone 键均通过只读校验；Trader 分类/单品引用完整；`SpawnAttachments` 引用完整；5 个比特币 Trader 的可见/隐藏权限均只使用模式 0/3；独立 classname 重复、Variant 多父级/重复和动态库存超限均为 0。DF COLLECTION 51 件仍为Mode 2只回收，并按5,000至80,000七档执行。

## 13. 2026-08-12 Expansion 官方源码复核与 Variant 归属修复

### 13.1 官方基线

- 官方仓库：`salutesh/DayZ-Expansion-Scripts`，`experimental` 分支。
- 本次浅克隆和源码审计 commit：`6dacd00f6d943ebbd99e0cf1baad93f470d96419`。
- 已逐段核对 `ExpansionMarketCategory.c`、`ExpansionMarketItem.c`、`ExpansionMarketTrader.c`、`ExpansionMarketTraderZone.c`、`ExpansionMarketSettings.c`、`ExpansionMarketModule.c`、`ExpansionTraderBase.c` 和对应 Market Wiki。
- 审计笔记：`Project Manage\Market System Rebuild\workspace\official_market_source_baseline.md`。
- 实现上 Variant 第二次被父项遇到时会进入 `MarketCfgError` 并跳过；跨文件枚举没有可依赖的经济优先级。

### 13.2 实际 Market 变更

本轮只修复 Variant 声明。没有改动价格、库存阈值、`SellPricePercent`、`SpawnAttachments`、Trader、TraderZone、MarketSettings 或 `.map`。

- `Market\FOG\FOG_Shirts.json`：`fog_crye_g2_shirt_mc` 仅保留在 G2 父项，从错误的 G3 父项移除。
- `Market\FOG\FOG_Pants.json`：`fog_pants_crye_g2_blue` / `dtg` / `wtg` 仅保留在原先先加载的 G2 父项，避免改变当前有效经济行为。
- `Market\FOG\FOG_Vests.json`：11 个 JPC2 颜色从 JPC 父项移除，仅保留在 `FOG_Vest_JPC2_ColorBase` 家族对应的 JPC2 父项。本地 FOG 模组 `config.cpp` 已确认 JPC 与 JPC2 为两个独立类继承系。
- `Market\FOG\Fog_Ghillies.json`：移除 `fog_ghilliehood_mcbrowns` 的同父项第二次声明。
- `Market\Bitcoin-MBM_LandCruiser100_Parts.json`：移除 `mbm_landcruiser_doors_codriver_green` 和 `mbm_landcruiser_doors_driver_blue` 各自的同父项第二次声明。

共移除 18 条重复声明：15 条跨父级，3 条同父项内重复。

### 13.3 备份与验证

- 修改前备份：`profiles\ExpansionMod\Market_Backup\2026-08-12_variant_parent_repair\pre_change\`。
- 可复用只读校验器：`Project Manage\Market System Rebuild\workspace\tools\validate_active_market_v1.py`。
- 服务器进程检查：未发现 DayZServer / DayZ_x64 / DZSA / Omega / BEC 匹配进程。
- 校验结果：`ACTIVE_MARKET_VALID=true`，`errors=0`，`warnings=0`。
- 未完成项：服务器启动 RPT、客户端 UI、买卖和附件生成实机验收。

## 14. 2026-08-12 候选经济账本 v1

### 14.1 状态与工件

状态固定为 `CANDIDATE_NOT_APPROVED_FOR_LIVE_MARKET`。候选账本现统一位于 `Project Manage\Market System Rebuild\workspace`，没有改动活动 Market、Trader、TraderZone、MarketSettings 或 `.map`。

- 13 种材料：`contracts\material_unit_buyback_v1.csv`
- 312 条受管装备：`contracts\managed_equipment_candidate_ledger_v1.csv`
- 870 个唯一外围 classname：`contracts\peripheral_candidate_ledger_v1.csv`
- 外围 classname 证据：`contracts\peripheral_classname_evidence_v1.csv`
- 2,444 条套利/转换路径：`reports\four_path_arbitrage_audit_v1.csv`
- 8-sheet 公式工作簿：`outputs\expansion_market_candidate_ledger_v1.xlsx`
- 生成器：`tools\build_candidate_ledger_v1.mjs`
- 外围与套利生成器：`tools\build_peripheral_candidate_v1.py`、`tools\build_arbitrage_audit_v1.py`
- 输入 hash、汇总和不变量：`reports\economy_candidate_summary_v1.json`
- 方法、公式、例外和限制：`reports\economy_candidate_methodology_v1.md`

### 14.2 材料单位回购候选值

| ClassName | Hryvnia/单位 | ClassName | Hryvnia/单位 |
|---|---:|---|---:|
| `QPK_Bolts` | 300 | `QPK_Cloth_Aramid` | 2,000 |
| `QPK_MetalParts` | 1,000 | `QPK_WeaponParts` | 4,000 |
| `QPK_Calibrator` | 5,000 | `QPK_MilitaryCable` | 5,000 |
| `QPK_Poxeram` | 6,000 | `QPK_MilitaryBoard` | 10,000 |
| `QPK_PowerFilter` | 20,000 | `QPK_GyroScope` | 35,000 |
| `QPK_FlashStorage` | 55,000 | `QPK_Virtex` | 90,000 |
| `QPK_FAR` | 150,000 |  |  |

本节下表只是2026-08-12候选账本的历史快照，现已撤回，不是当前方案。2026-08-14 Market端只给6种普通QPK材料设置12,000—100,000直购/2%回收；六种核心和Calibrator仍无NPC路径。上述售价不是制作内部价值。

### 14.3 受管装备候选规则

- 312/312 已映射：260 武器、49 护甲、3 受管弹匣。
- 完整成本包含 full-chain 材料、外部 donor、`制作秒数 × 50` 和 `工具损耗百分点 × 2,000`；full-chain 已包含 Calibrator 与阶段核心，不重复计价。
- A1—A4 共 212 条，候选 Mode `1`；NPC 高库存最低售价按家族成本与功能系数 `×1.35`，低库存最高售价 `×1.60`，`SellPricePercent=40`。
- A5—A6/停产项共 100 条，候选 Mode `2`；NPC 回购基准为家族成本 `×0.65` 向下取整到 500，`SellPricePercent=100`。
- 同 `balance_family`、同功能纯皮肤同价；武器按经济带/角色/口径/容量修正，护甲按防护、总容量和角色双轴修正。
- `AJW_Mag_M14_30rnd` 的外部 donor `AJW_Mag_M14_20rnd` 已改为从外围账本读取 P2P 参考价 `8,500`，不再使用临时 `12,000`；停产的 `AP_vest_dcs_3_mc` 仍用现役 A5 护甲完整成本中位数 140,000 作为回收底座并强制 Mode `2`。

### 14.4 验证与限制

- 312 条候选记录完整；同家族同分组价格离散为 0。
- 每个 classname 的最高 NPC 回购价均低于自身完整成本。
- 每个 Mode `1` classname 的 NPC 最低售价均高于自身完整成本和拆解材料价值。
- 870 个外围 classname 的 blocked 证据数为 0，projectile / `CfgVehicles.Resources` 待审核数为 0。其中候选 Mode `1/2/3` 为 `741/77/52`。
- 2,444 条审计中计算 1,929 条可执行路径，515 条因候选权限或 loose-ammo 未上架而不存在；可重复正收益闭环为 0。
- 工作簿 8 个 sheet 已完成公式错误扫描和视觉核验，未发现 `#REF!`、`#DIV/0!`、`#VALUE!`、`#NAME?` 或 `#N/A`。
- 活动 Market 复验仍为 `ACTIVE_MARKET_VALID=true`、0 错误、0 警告。
- 当前没有 wipe 后真实供应、P2P 成交、库存积压、玩家持币与货币沉没数据；所有 Hryvnia 数字都是候选值。
- 外围价、权限和套利算术已建立，但仍缺 wipe telemetry、用户审批和 RPT/UI/交易实机验收；C1 审核包已生成，七类 staging 门禁完成前不得生成完整候选 Market/Trader JSON，更不能覆盖活动配置。

### 14.5 外围 classname 与代码取证规则

- 精确 classname 先查 `cfgeconomycore.xml` 实际注册的 115 个 active types 和 13 个 active spawnabletypes，再查 AJW/SNAFU/TTC 解包 `config.cpp`。
- Expansion 物品使用冻结的 `experimental@6dacd00f6d943ebbd99e0cf1baad93f470d96419` 配置与 Market 实现源码。
- active types 证明 CE 拼写和生成政策；不在 types 里不代表 Trader-only / craft-only classname 必然无效，此时需 config 或官方源码证据。
- Market 现有小写名与 types/config 规范大小写并存；候选表同时保留 `market_classname` 和 `canonical_classname`。
- 弹药盒不能按空盒定价；必须解析 `CfgVehicles.Resources` 的 loose-ammo classname 和 quantity。Market 文件名只是初级线索，`CfgVehicles + Resources` 优先判定为弹药盒。

### 14.6 四路径与外围转换审计

- 受管四路径固定为：直接卖材料、合成后卖成品、拆解后卖材料、NPC 买入后拆解。
- NPC 买入路径依官方 `FindPriceOfPurchaseInternal` 递归计算最多 3 层 `SpawnAttachments`；出售路径依 `FindAttachmentsSellPriceEx` 处理弹匣内子弹和实体附件。
- 外围转换另查直接买入回售、弹药盒拆包回售和买弹药填满弹匣后卖出。`NO_ROUTE` 表示权限或 loose-ammo Market 缺失使该重复转换不存在，不是将未知收益当成 0。

## 15. 2026-08-13 项目文件集中管理

- 项目唯一入口：`Project Manage\Market System Rebuild\MARKET-REBUILD-HANDOFF.md`。
- 临时工具、候选合同、报告和输出：`Project Manage\Market System Rebuild\workspace\`。
- 312 条分析、crosswalk 和迁移控制表：`Project Manage\Market System Rebuild\analysis\`。
- 冻结官方源码：`Project Manage\Market System Rebuild\sources\DayZ-Expansion-Scripts-experimental-6dacd00f\`。
- 工作簿视觉核验 PNG：`Project Manage\Market System Rebuild\workspace\previews\`。
- 原 `Economy_Rework\expansion_market_economy_v1`、`profiles\ExpansionMod\EXPANSION_MARKET_REBUILD_*` 和 Project Manage 根目录旧 HANDOFF 已迁走，不保留重复副本。
- 活动配置、运行期 TraderZone、Market 备份和本 Guide 保留原位；它们不是临时工件，不应搬入项目目录。
- 迁移后的所有生成器会从脚本位置寻找项目根目录，显式读取同级 `analysis` / `sources`，并把预览写到 workspace；后续不得重新硬编码旧路径或 `/private/tmp`。

## 16. 2026-08-13 候选经济 C1 审核

### 16.1 审核包状态

- 状态：`C1_REVIEW_V1_SUPERSEDED_BY_ACQUISITION_FIRST_PRINCIPLE`；C1 v1 仅保留历史审计，本轮没有生成 staging，也没有修改活动 Market、Trader、TraderZone、MarketSettings 或 `.map`。
- 决策入口：`Project Manage\Market System Rebuild\workspace\contracts\candidate_review_decisions_v1.csv`，以及审核工作簿“决策矩阵”sheet。
- 15 项用户决定均保持 `PENDING`；其中 7 项阻塞 staging：`QPK_FAR`、A4 权限、外围 Mode `2→1`、外围 Mode `3→1`、4 个无路径条目、52 个 TTC Mode 3 部件、25 个高价值外围。

### 16.2 保守首发建议

- 本小节以下 C1 v1 建议只作历史记录，不再是现行建议。`QPK_FAR=100,000` 已撤回，制作价值和 NPC 回收现金必须拆开。
- “A1—A3 全部允许玩家向商人购买和出售”的整阶段规则已暂停；C1 v2 必须按真实获取渠道和玩法影响逐组判断。
- 外围建议首发 Mode `1/2/3/HOLD` 为 `521/201/144/4`。124 条当前 Mode 2 弹匣先保留 Mode 2；92 条当前 Mode 3 弹药/弹匣先保留 Mode 3；4 条无当前 Trader 路径的记录保持 HOLD。
- 415 条外围候选最低价至少上涨 10 倍，46 条至少下降 50%；价格切换只能绑定 wipe 或明确补偿的原子变更，不建议 mid-wipe 直接套用。

### 16.3 Classname 与 Mode 3 风险

- 312 条受管装备与 870 个外围 classname 继续沿用 active types、active spawnabletypes、模组 `config.cpp` 和冻结 Expansion 官方源码交叉证据；本审核未改写 classname。
- 旧 C1 v1 曾把 52 个 TTC 结构件列为 Mode `3`；v2 已全部纠正为 HOLD。52/52 在当前活动 Market 中都没有 `SpawnAttachments` 父引用，不能被描述为会自动随主商品生成；上线前必须逐项进行装配、Trader UI 可见性和出售行为实测。
- 42 区 11 条 AP/BIG_GUNS 普通高阶装备只有在 WestBrook/Waldoboro Hryvnia sell-only、42 区引用移除和 Zone 精确维护同时执行时才可迁移；Bitcoin 与 Hryvnia 不得直接做价格倍率比较。

### 16.4 验证与下一步

- C1 审核工作簿共 8 个 sheet；公式错误扫描为 0，8/8 sheet 已视觉核验，XLSX ZIP 完整。
- 异常明细合并为 645 个 classname；原 2,444 条套利/转换审计仍为 0 个正收益闭环。
- 活动配置复验仍为 `ACTIVE_MARKET_VALID=true`、0 warnings、0 errors。
- 下一步由用户填写/确认决策矩阵。七类 staging 门禁解除后，才在 `workspace\staging` 生成隔离候选 JSON，并重新执行 classname、权限、币种、附件、Variant、Trader 引用和套利全检。

### 16.5 玩法获取优先原则对 C1 的修正

- 玩家主要通过副本、探索、事件、合成、拆解和玩家交易取得装备；商店只解决必要补给或承担明确的经济作用。
- 黑市出售高性能、超原版属性装备，是高成本体验选择和货币回收渠道，不是普遍获取方式，也不应成为反向套现地点。
- A6 一次结算预计给 2 个 `QPK_FAR`。旧 150,000 回收价下，FAR 可换 300,000、整包材料约 `322,749.60` Hryvnia；此前 100,000 情景下整包仍约 `222,749.60`。虽然不是单件 100 万，但仍可能把终局玩法变成高额货币发行源。
- 下一步不是继续微调 FAR 单价，而是先分别建立制作核算价值、普通商人直购价和 NPC 回收价，再按活动频率与货币消耗确定是否允许核心材料回收。黑市售价延期到独立阶段设计，不阻塞当前普通市场重构。
- C1 v1 CSV/XLSX 不得进入 staging。现行硬约束见 `Project Manage\Market System Rebuild\workspace\reports\acquisition_first_economy_principle_v1.md`。

## 17. 2026-08-13 声望商店与 AP/SNAFU 当前状态

- 已读取独立 `ReputationMarketSystem` 项目。当前实现可让购买同时消耗 Expansion 货币和 Hardline 声望，并配置购买后最低剩余声望；纯声望购买、独立贡献点和商店界面声望价格显示尚未实现。
- A3—A4 可以在普通武器区域作为高价直购例外。A6 成品枪械不进入任何 NPC 直购，声望、任务或限量条件也不能作为例外；玩家可以卖给 NPC，但只能获得低额残值。
- AP 的 A6/终局成品护甲适用相同规则，不再保留 42 黑市直购例外。
- 声望系统可以用于 A3—A4 高价商品，或 A6 相关服务、材料、图纸与任务入口；若需要消费型声望，应考虑独立贡献点，避免购买后长期声望降级。
- AP/SNAFU 目标分类已在 2026-08-14 10:52 一次性迁出 42，并写入首批 Hryvnia 价格/权限；`AP_Armor` 的 8 个非 AP 分类和 `BIG_GUNS` 的 3 个黑色重贴图分类有意保留。
- 21 个 SNAFU 大口径对象已按武器/弹匣/弹药进入普通 SNAFU Market；A6/无来源对象继续禁止 NPC 购买，只允许低额回收或保持隔离。
- AP 同色附件、功能 Variant、20 个缺失 Market 定义和 14 个 SNAFU 弃用 classname 均已收口。旧状态报告只作历史证据。
- A6 枪械和 AP A6/终局护甲的禁购规则已经确认。本次规则补充没有修改 Market、Trader、TraderZone、地图或声望模组。
- 旧 `ap_snafu_managed_permission_matrix_v2.csv` 的 AP 25 条只是代表项，SNAFU 130 条也包含旧/新枪名重叠；AP 当前为 29 家族/114 个精确 classname，目标 mode 1=76、mode 2=38；SNAFU 当前权威是 v3 的 129 个规范 classname。两组均无 classname 证据阻塞。
- AP v4 已确认当前 AP_Armor mode 0 的 22 个精确护甲 classname 全部与目标禁购规则冲突；BIG_GUNS 14 项另有逐项迁移合同。该数字取代旧“11 条代表项”统计，但价格、Trader、Zone 和获取路径未准备完整前仍不得原地半迁移。
- AP WEAR（types 名为 `AWEAR_types_*`）的 485 件 Market 与独立 Trader 当时已建立；NPC/Zone 遗留已于 2026-08-23 解决，现行状态见 18.27。

## 18. 2026-08-13 当前唯一推进顺序

完整路线图见 `Project Manage\Market System Rebuild\workspace\reports\current_project_roadmap_2026-08-13.md`。后续按以下依赖顺序推进：

1. 全目录 types v1 审计、人工分类和高置信清理已完成：27 个 classname/28 个 XML 节点带备份移除，活动重名/碰撞由 31 降至 4。剩余中置信项和 MMG 大小写身份不得顺手处理。
2. 当前权威完整范围是 global v3：1,296 个规范 classname、受管 409、外围/支持物 887，目标 `934/277/15/70`，A5=94/A6=43。source v3 登记 49 项，单独阻止无来源物品通过 NPC 直售补洞。
3. 战斗市场首批 Hryvnia 数值和权限已写入；下一步是非战斗普通市场（食品、药品、工具、建材、普通服装、普通车辆零件）的简单分层定价。Workbench 清理弃用/重复配方后当前为 312 制作 + 737 拆解；旧 314/742 只作迁移前基线。
4. 当前全量 Market/Trader 已同步隔离 staging；继续严格排除爆炸物、退役模组和黑市独立商品。
5. 完成静态检查、套利、diff、RPT/UI/交易实测和 wipe 初始状态检查。
6. 用户批准后写入 `Deerisle 6.1` 真实运行路径，停服备份并原子上线，再按 7/14/30/45 天 telemetry 小步调价。

不可倒序：权限决定价格公式和库存路线，价格决定 Market/Trader JSON，完整 staging 才能计算 Zone 差异并安全移除 42 旧路径。

历史提醒：本节记录时 AP WEAR/AWEAR 与 QPK 尚缺 NPC；该项已于 2026-08-23 解决，现行状态见 18.27。CarPack 实车与其他运行验收仍未完成。

### 18.1 types v1 审计结果

- 当前全目录共 164 个 CE 文件：任务目录 139、历史快照 25；活动注册为 116 个 types 和 13 个 spawnabletypes。
- 清理后 active types 共 16,840 个不区分大小写的唯一键、16,844 条定义；116 个活动路径全部存在且可解析。27 个高置信 classname/28 个重复节点已从 5 个活动文件移除，修改前完整文件保存在项目备份目录。
- 当前只剩 4 个重名/碰撞：`AJW_Mag_CZP09_20Rnd` 是中置信度单独决策，`Defibrillator` 和 `WoodenLog` 是有意覆盖，MMG 大小写碰撞等待运行时类清单；本轮不得继续扩删。
- 4 个 FOG 新 classname 均由当前 `config.bin` 精确证实。三个 Big Patch 已纳入 `FOG_Misc` 的现有父项 Variant；`FOG_GPNVG_GSGM_Tan` 是独立 97° 四目夜视仪且没有玩法来源，补来源前不加入 Trader。
- AJW 旧类 `AJW_Barret50_Magazine_10rnd` 已从活动 Bastardo 掉落和两份 Hardline 引用中替换为 `AJW_Mag_M82_10rnd`；未注册/No Use/备份文件保留证据。6 个 Terje Radiation 药品因模组未加载已从两份 Hardline 删除。2 个 Dune Shield 继续留待黑市阶段。
- 官方源码 `ExpansionMarketSettings.LoadCategories` 只递归读取 `.json`；无扩展名的 `Market\Dune_Shield` 和 `Market\Helicopters` 当前均不加载。Dune Shield 属未来黑市范围，本轮只登记。
- 剩余 157 条受管装备矩阵目标为普通买卖 106、只回收 51，classname 阻塞 0；A5 与两个升级弹匣的只回收方向已经冻结。19 条没有活动 Market 全局定义，正式生成前必须先补正确父项/分类。
- 完整报告：`types_crosscheck_report_v1.md`、`types_duplicate_resolution_v1.md`、`fog_new_items_resolution_v1.md`、`remaining_managed_permission_matrix_v2.md`。

### 18.2 外围权限结果

- 870 条 v2 与 `572/205/15/78` 只保留为历史复核。当前 v3 为 865 个规范 classname：AJW `213/38/0/14`；SNAFU 专项本体 255 项为 `201/47/7/0`，统一表补入缺 Market 定义的 Black Gevar 后为 256 项 `201/48/7/0`；TTC `107/30/0/52`；原版/Expansion `139/6/8/2`。总计 `Mode 1/2/3/HOLD=660/122/15/68`。
- 15 个 Mode 3 中，SNAFU 7 种弹药由 Expansion `AddDefaultAttachments()` 根据弹匣 `ammoItems` 在运行时形成真实依赖；原版/Expansion 8 个弹匣有活动 `SpawnAttachments` 父引用。HOLD 不能用 Mode 3 冒充禁用。
- 52 个 TTC 结构件全部 HOLD：6 个枪管/机匣有制作/拆解用途，其余 46 个先做装配/UI/出售实测。52/52 无活动 Market 父引用。
- SNAFU 已按 `Custom Mods/Mod_Edit/SNAFU Weapons` 验证真实类：普通配件高价直购、低价回收；107 个弹匣中 69 个普通直购、38 个高容量/重口径战略弹匣只回收。弃用类通过独立原子动作处理，不计入 256 个规范范围。
- AJW 14 个 HOLD 主要是无战利品/制作/随枪来源的高容量弹匣及两个异常/彩蛋瞄具；先补玩法来源，再考虑低价回收。
- 本节权限方向已由用户确认，但没有批准具体价格、库存或声望条件，也没有把权限写入活动 Market、Trader 或 TraderZone。完整合同为 `workspace\contracts\peripheral_permission_matrix_v3.csv`。

### 18.3 AP Variant、隐藏附件与完整护甲范围

- AP 活动 Market 共 15 个分类、168 个独立 Item、478 个 Variant、646 个唯一 classname；646/646 均有 active types 与当前解包 config 精确证据。
- 完整 AP 护甲范围不是原矩阵的 25 个代表项，而是 29 个功能家族、114 个精确 classname。Kevlar-mid、6B43-full、6B45H、6B46H 四家族共 13 条已在 v4 通过兼容层和分级设计完成分类。
- `ap_helm_altyn_green`、`ap_helm_vulkan_green` 当前作为黑色成品头盔的 Variant，会继承黑色 `SpawnAttachments`。候选结构必须把两个绿色头盔拆为完整 Item，并分别绑定绿色 visor/barmit；6 个终局头盔部件继续 mode 3。
- 9 个跨 config 基类 Variant 中，LSHZ-HC、6B46H、suhar-new 共 5 条具有插槽/容量/重量等功能差异，必须拆成独立家族；holster/sheath 4 条在同价同权限且功能一致时可继续作 Variant。
- `AP_vest_6b43_sand` 与 `AP_vest_6b43_full_sand` 当前仍由 AP_Armor mode 0 出售；v4 精确确认 AP mode 0 冲突共 22 条，原“11 条冲突购买路径”代表项数字已废止。
- active AP Equipment types 另有 49 个类未进 Market，其中 AP 1.6 更新新增 13 条。types 只证明 classname 有效，不自动授权 NPC 上架。
- 本节当时 AP WEAR 的 8 个 active types 文件共 485 个 classname、Market 命中 0；后续已建立 485 件 Market/独立 Trader，并于 2026-08-23 完成 NPC/Zone，见 18.19 与 18.27。
- 本次只生成 `workspace\contracts\ap_variant_hidden_resolution_plan_v1.csv` 和 `workspace\reports\ap_variant_hidden_review_v1.md`，未修改活动配置。

### 18.4 AP v3 展开、SNAFU 旧类与 BIG_GUNS 漏表

- AP v3/v4 已把 29 个功能家族展开为 114 个唯一 classname，types/config 证据阻塞 0。当前实际为 AP_Armor mode 0 共 22、AP_Rookie mode 2 共 68、无路径 24；v4 已将四个漏家族全部分级，目标为 mode 1=76、mode 2=38、HOLD=0，22 个 mode 0 现均为明确禁购冲突。
- 护甲兼容层、`armor_upgrade_route_v1.json` 与 `recipe_profiles_v2_proposal.json` 交叉证明：Kevlar-mid 为 S 档/A2；6B43-full、6B45H、6B46H 为 H 档/A5。三者不是 H+，附件容量 48/52/42，也不满足 A6 大容量条件。9 个 A5 classname 中 4 个已有活动可拾取 AI 配装来源；真实来源缺口为 5 个沙色/冬季类。
- SNAFU 外围 9 个弃用类均有源码替代，另有 5 组弃用枪类；`SNAFUMPX_Grip` 是有效 scope=2 类且有 CJ 来源，不是弃用类。15 条独立动作记录中包含 14 条弃用替换和 1 条 MPX 握把保留/重分类；必须按各系统原子执行，不能机械字符串替换制造重复权重。
- `SNAFU_SR3Vikhr_Supp` 是普通专用配件，不是此前误判的终局高耐久消音器；普通配件按高价直购、低价回收。60/100 发等高容量弹匣仍是战略例外，不因“配件可以买卖”自动开放。
- BIG_GUNS 漏表 14 项全部有 active types/config 证据：3 个 M200 A6 成品归受管合同，8 个弹匣和 3 种重弹药归终局支持合同。12 项已有玩法路由，建议 mode 2；`GCGN_M200` 与 `SNAFU_M200Green` 无真实非商店获取路由，保持 HOLD。
- 本阶段全部为工作区合同，未修改 42 黑市商品、价格或任何活动配置。

### 18.5 全局权限范围合同

- 当前权威总表是 global v3：1,296 个不区分大小写的唯一规范 classname，受管成品 409、外围/支持物 887；目标普通高价买卖 934、只允许玩家低价回收 277、真实内部依赖 15、HOLD 70。
- 全局范围内 A5 共 94 个、A6 共 43 个；A5/A6 均已确认 NPC 禁售、玩家低价回收。权限确认不等于解决玩法来源，也不等于价格或库存已经批准。
- 旧 global v1 的 1,285 原始行、`839/351/15/80` 和 1,279 规范视图 `840/353/15/71` 只作历史审计，禁止作为 staging 输入。
- 总表保留逐物品当前权限、目标区域/Trader/货币、获取缺口、旧类原子动作和规范执行字段。4 个当前没有 Trader 路径的 Expansion 烟雾弹明确标记为待映射，未凭经验分配商人。
- 15 条 SNAFU 独立动作记录必须与规范主表同步消费；4 个 `PENDING_ROUTE_MAPPING` 必须阻止生成真实 Trader 路径。
- 完整工件：`workspace\tools\build_global_permission_scope_v3.py`、`workspace\contracts\global_permission_scope_v3.csv`、`workspace\reports\global_permission_scope_v3.md` 与 summary JSON。本次合并未修改活动 Market/Trader/Zone。

### 18.6 玩法来源与当前执行门禁

- `gameplay_acquisition_gap_registry_v3.csv` 共 49 项：33 个核心缺口、13 个 Market-only、3 个类语义待确认。没有玩法来源的物品不得通过 NPC 直售补洞。
- 没有玩法来源的物品继续 HOLD 或不加入 Trader，交由独立玩法来源项目处理；不得通过无限 NPC 库存制造来源。
- 当前可继续做价格和 staging 设计，但不能直接写活动配置：15 条 SNAFU 原子动作、19 个缺 Market 定义项、AP Variant/同色附件、TraderZone 差异、价格和库存必须形成同一份可验证候选。
- 本节当时 AP WEAR/AWEAR 独立 NPC 与黑市重构仍是后置项目；AP WEAR 的 Market/Trader/NPC/Zone 后续已完成，见 18.19 与 18.27。

### 18.7 普通市场价格模型 v3

- 价格模型已经给 global v3 的 1,296 个规范 classname 分配处理通道：1,226 个需要价格或内部组件价值，70 个 HOLD 不生成价格。当前完成的是公式和输入门禁，不是最终 Hryvnia 数值。
- Mode 1 使用高价便利溢价，并按单件绝对回收上限反推 `SellPricePercent`；Mode 2 回收额取内部价值比例、单件绝对上限和周发行预算/预计回收数量三者最低；A5/A6 没有直购公式。
- 15 个 Mode 3 内部依赖会参与父商品递归购买/回收估值，不能用零价隐藏替代。满弹匣、弹药盒拆包、三层附件递归和不同容量 Variant 都是强制套利门禁。
- 旧 v1/v2 数字只作审计参考；BIG_GUNS 的 Bitcoin 值完全排除。AP 内部价值 13 项已有待重基比较锚，尚需当前材料/替代成本。
- 完整工件：`normal_market_price_parameters_v3.csv`、`normal_market_price_readiness_v3.csv`、`normal_market_price_model_v3.md` 与 summary。黑市价格明确不在本模型范围。

### 18.8 隔离 staging 原子计划 v1

- 未来施工已拆为 34 个有向无环节点，并区分“可以生成候选”的 build 依赖和“允许上线”的 activation 依赖；当前没有生成或修改活动 JSON。
- 计划只精确迁出 42 的 6 个 AP 分类和 `BitCoin_Snafu_Sniper:0`。AP_Armor/BIG_GUNS NPC、地图行、8 个非 AP 分类和 3 个枪皮肤分类都不在删除范围。
- 19 个原缺 Market 定义项按 7 个目标文件分批；Black Gevar 是后来发现的第 20 项，单独建完整 Item 后再设只回收。
- 42 的 41 个 AP classname 中，22 个高阶护甲、6 个头盔内部件和另外 13 个耳机/成品头盔/修理工具/防破片裤均已有权限证据；后 13 项已并入 global v3，仍只能按精确合同迁移，不能整类操作。
- 生成器对 46 个未来受影响活动文件做前后 SHA 保护，依赖无环和覆盖数量断言均通过。完整工件为 `canonical_market_staging_plan_v1.csv/.md` 与对应生成器。

### 18.9 AP-150 范围补漏与 Workbench manifest

- staging 审查曾发现 42/AP_Armor 有 13 个真实玩家物品未进入历史 global v2：6 个主动降噪耳机为 Mode 1 高价直购/低价回收；4 个 H+/A6 成品头盔、护甲维修套件和两条防破片裤为 Mode 2。这 13 项现已并入 global v3。
- 结构应为 10 个完整 Item + 3 个颜色 Variant；两个绿色终局头盔必须拆成完整 Item并绑定同色附件。13 项只允许精确迁往 WestBrook/AP_Rookie，不授权修改其他黑市商品。
- 13 项中 2 个有活动来源，5 个 Mode 2 核心物和 6 个耳机没有非商店来源。这 11 项已并入 source registry v3；普通耳机即使允许昂贵直购，也应补长期玩法来源。
- global v3 已在历史 v2 的 1,279 条上并入上述 13 项和 MMG 四色，当前总数是 1,296，price readiness v3 也已同步重建。
- Workbench 正确口径是 314 个制作配方块 + 742 个拆解配方块；旧说法“742 个结果”错误。制作产出 314、拆解产出条目 1,414、全部产出 1,728。
- `mmg_gp_nvg_black` 是旧 313 个制作配方末尾追加的第 314 条，旧 313 条逐对象未变。MMG 四色现已进入 global v3 为 A6 Mode 2；black 有制作来源，tan/green/grey 缺来源，四色均无拆解配方。
- Workbench 仍引用 5 个弃用 SNAFU classname：制作成品 3 处、拆解目标 5 处；必须与既有 SNAFU 原子迁移同批修复。

### 18.10 当前 v3 权威范围与价格输入

- 当前唯一权威权限合同已升级为 global v3：1,296 个唯一规范 classname，受管 409、外围/支持 887，`Mode 1/2/3/HOLD=934/277/15/70`，A5=94、A6=43。global v2 的 1,279 条仅保留为历史已知基线。
- AP-150 范围补漏 13 项已并入 v3：6 个耳机 Mode 1；4 个 A6 头盔、修甲包和 2 条防破片裤 Mode 2。其中 11 项没有非商店来源。
- 另一组 AP 内部价值 13 项是 4 件 A2 Kevlar-mid + 9 件 A5 6B43 Full/6B45H/6B46H 背心，与 AP-150 集合完全不相交。临时内部锚为 A2 40,000，A5 三家族分别 183,000/184,000/182,000；只是待按当前材料/替代成本重基的比较值，不是 NPC 价格。
- MMG GP NVG black/tan/green/grey 四色已并入 v3 为 A6 Mode 2：NPC 禁售、玩家低价回收。black 有唯一 Workbench 制作路径；tan/green/grey 无来源；`Chance=0` Loadout 不算产出。四色均无拆解配方，当前不自动创建新拆解经济路径。
- 玩法来源 v3 的 49 项是历史基线。无来源事实与商店权限分开判断：适合普通商店供给的 A1—A4/普通配件可以高价直购、低价回收；A5/A6 和战略物仍禁止直购。Mode 1 直购不算野外、任务或合成来源。
- 本节原314/742是当时审计快照；当前活动Workbench为374条制作/755条拆解。HP_Crafter 3.2.1继承3.1动态名册，当前数量不是PBO精确硬合同；canonical staging的34个DAG节点仍仅属历史价格工件。
- price v3 覆盖 1,296 项：1,226 项已分配公式，70 项 HOLD；47 个参数中 5 项工作区证据就绪，但 NPC 具体 Hryvnia 数值仍为 0。普通配件高价直购、低价回收；A5/A6/终局装备禁止 NPC 直售、只给受周发行预算和绝对上限约束的低残值。
- 13 种材料的范围、配方用量和当前无 Market 路径事实已完成审计；13/13 均有 CJ 配置路径，用户确认的 42 窗口规划情景也已建立。下一步取得真实重启/RPT/PBO/玩家取得证据，处理 SFL、Workbench 拆解和异常重启去重门禁，再冻结核心/普通回收策略、材料周发行预算和内部单位价值。价格门禁通过后才生成隔离 staging。
- CJ-v4 偏差审计已明确 12 项待批候选目标与 `QPK_Calibrator` 无目标的分界。v4 未获用户批准、未进入 runtime；capture 比例只是当前 CJ 配置内容相对候选目标的偏差门槛，不是玩家实得。六种阶段核心已有交易硬规则：P2P 允许，NPC 售卖和回收禁止。
- Calibrator当前事实：374条制作中314条正式制造/升级配方使用`Destroy=1`每次销毁1个，41条纯颜色转换不要求；`mmg_gp_nvg_black`已要求Calibrator，不再是例外；755条拆解无目标也无产出。旧可维护工具提案未获批准；玩法供应、内部价值和NPC政策仍待运行数据。
- 本阶段当时没有修改活动 Market、Trader、TraderZone、Workbench、Hardline、地图、声望或价格。AP WEAR/AWEAR 的后置施工已在 18.19 与 18.27 完成；现行门禁为重启实测。

### 18.11 13 种材料经济输入审计

- 旧材料合同的 13 个 classname 范围本身没有错：它与当前 314 个制作配方中出现的全部 13 种 `QPK_` 材料精确一致。312 个制作配方使用 QPK，合计 1,713 个输入条目、字面需求数量 4,762。
- Workbench 拆解共有 1,409 个 QPK 产出条目，满耐久字面上限 1,962。仅 `QPK_Bolts` 和 `QPK_MetalParts` 会由拆解产出，且均开启 `ScaleYieldByTargetHealth=1`；1,962 是满耐久上限，不是玩家必得量。其余 11 种在 Workbench 中只是输入。
- 13/13 均有 Mod_Edit 精确 class 声明，但当前 115 个 active types、151 个递归 Market v12、32 个 Trader v13、7 个 TraderZone v6 中的定义、路由和库存键全部为 0，也不在 global v3 的 1,296 个商品 classname 范围内。
- 旧理论周发行 1,329,196.84、核心材料 1,026,643.46、`QPK_FAR` 605,769.30 一律撤回为 `CANDIDATE_NO_WIPE_TELEMETRY` 历史锚，不得作为内部价值或 NPC 回收价输入。13 种材料正式价仍为 0。
- price v3 可消费已冻结的 classname/配方用量/拆解关系；11 种输入专用材料的来源路径已查清，但在以下门禁解决前仍不得输出价格：材料内部单位价值；六种核心与七种普通/支持材料的 NPC 回收策略；材料层周发行预算；可信周供应和玩家保留/回售比例。
- 工件为 `build_material_economy_input_audit_v1.py`、`material_economy_input_audit_v1.csv`、对应 MD 和 summary JSON。本审计未修改 Market、Trader、TraderZone、types、Workbench、price v3 或任何正式价格。

### 18.12 11 种输入专用 QPK 材料玩法来源审计

- 11/11 均有当前 CJ 宝箱配置的可达主路径，完整材料零来源为 0。CJ 作者页确认宝箱只在 server restart 时生成并填充一次，打开后本次运行不会补货；因此当前只能冻结每次重启结构模型，不能把结构期望或绝对槽上限冒充玩家周取得量。
- 本节原“各1个SearchForLoot入口”是旧21池快照。当前SFL已迁移为105个Tier1—4/Unique池，`QPK_Bolts`、`QPK_MetalParts`、`QPK_WeaponParts`、`QPK_Cloth_Aramid`各有5个类别节点，但运行验证仍为0；Tier5—9解析、DayZ 1.29兼容和实际加载证据均未解除。四项继续挂`SFL_COMPATIBILITY_RUNTIME_GATE`，不能按5个节点直接换算供应。
- `CJ_Key7`、`CJ_Key8` 对应的 T5/T6 补充路线没有任何活动 `LootDropOnDeath` 引用，影响 7 种材料，但 7 种材料仍各有独立 CJ 主路径。两条缺口登记给玩法 Agent，不得计入当前供应，也不应通过 NPC 直售补洞。
- 本来源审计阶段可量化运行时周供应项为 0，只保留 CJ 每次重启结构模型。后续 42 窗口规划情景不能反向当作 telemetry。正式材料内部价值和 NPC 价格继续为 0；下一步输入为真实重启次数、三种可堆叠材料的 CJ 数量实机结果、钥匙/路线/开箱完成率、玩家保留/回售比例，以及 SFL Improved 实际加载和运行证据。
- 工件为 `build_qpk_input_only_gameplay_source_audit_v1.py`、`qpk_input_only_gameplay_source_audit_v1.csv`、对应 MD 和 summary JSON。当前生成器仍写死旧314/742 Workbench基线；修复并按374/755重生成前，报告只作历史快照。本审计未修改 Market、Trader、TraderZone、types、CJ、SearchForLoot、AI、任务、Workbench、price v3 或任何正式价格。

### 18.13 13 种 QPK 材料供应规划情景审计

- 规划输入来自 `Deerisle/Economy_Rework/design/operational_inputs_v2.json`：4 小时/窗口、6 窗口/天、42 窗口/周。它是用户确认的运营规划，不是 runtime 配置、重启日志或玩家实得 telemetry。
- 13/13 均有 CJ 配置路径。Bolts 为 12.253742 实例/重启、514.657150/42 窗口；MetalParts 为 4.507070/重启、189.296954/42 窗口；FlashStorage 约 1,156.895319/42 窗口，FAR 约 252.762343/42 窗口。它们是按箱数、随机槽和权重推导的配置内容期望，不是玩家实际获得量。
- Workbench拆解数量是旧审计快照；当前两套QPK生成器仍被314/742硬基线拦截，需先按374/755重生成。SFL当前四种基础材料各有5个Tier类别节点，运行验证仍为0；节点数不是单次搜索概率。
- 当前没有异常重启去重控制器的部署证据；`settlement_controller_v1` 明确标记为 `DESIGN_ONLY / NOT_DEPLOYABLE`。额外重启 `E` 会把 CJ 配置模型放大为 `每重启模型 × (42+E)`，不得假定设计控制器已经上线。
- 当前项目没有 RPT、启动日志或 modlist 可解除 SFL、Workbench、控制器和实际供应门禁。正式内部价值与 NPC 价格继续为 0。
- 工件为 `build_qpk_material_supply_planning_scenario_audit_v1.py`、`qpk_material_supply_planning_scenario_audit_v1.csv`、对应 MD 和 summary JSON。本审计未修改 CJ、SearchForLoot、Workbench、Market、types、price v3 或任何正式价格。

### 18.14 QPK 当前 CJ vs v4 待批需求偏差审计

- `reward_lane_policy_v4` 是 `DESIGN_POLICY_NOT_RUNTIME_CONFIG`，其规划段为 `CALIBRATION_SCENARIO_NOT_RUNTIME_APPROVAL`。它是当前待用户审批的设计候选，不是已批准政策、runtime 配置或价格权威。
- 13 种材料中 12 种有 v4 候选周目标；`QPK_Calibrator` 没有 v4 目标。`NO_V4_TARGET` 不等于目标 0，也不授权用当前 CJ 数字反推目标。
- init 数量模型下最低 capture 前三是 `QPK_FlashStorage` 0.166227%（当前 CJ/候选目标 601.585566×）、`QPK_MilitaryCable` 0.497719%（200.916490×）、`QPK_Poxeram` 0.559037%（178.879033×）。数值越低只表示玩家只需获取当前 CJ 可达内容的更小部分，就会达到待批候选目标；它不是已观测玩家获取率，更不是玩家实得量。init/full-stack 两套模型在堆叠语义实测前必须并存。
- A1—A6 六种核心的交易硬规则来自已确认的 `operational_inputs_v2.json`，而不是 v4 候选数值推导：玩家间交易允许，NPC 直售禁止，NPC 回收禁止。
- `QPK_Bolts` 和 `QPK_MetalParts` 的拆解供应不并入 CJ capture 分母。配置中有 712/697 个拆解配方，每配方各执行 1 次且满耐久时的字面量为 1,096/866；实际配方加载、每周执行次数和耐久缩放未有 PBO/RPT/telemetry 证据。
- 本审计生成的内部价值和 NPC 价格数量都是 0。当前正式内部价值、NPC 售价和 NPC 回收价继续为 0。
- 工件为 `build_qpk_cj_vs_v4_demand_deviation_audit_v1.py`、`qpk_cj_vs_v4_demand_deviation_audit_v1.csv`、对应 MD 和 summary JSON。下一步是请用户审批/驳回 v4 候选基线，单独决定 Calibrator 的目标治理，并用真实重启、PBO/RPT、堆叠、开箱与玩家保留数据替代理论 CJ 分母。本审计未修改活动 CJ、Workbench、Market、Trader、TraderZone、types、price v3 或 v4 设计文件。

### 18.15 QPK Calibrator 消耗、供应与治理审计（2026-08-13历史快照）

本节下方314/742、294条和MMG例外是当时审计过程，已被后续活动配置覆盖。当前口径为376制作/757拆解、314条正式制造/升级消耗Calibrator、41条纯颜色转换不消耗，`mmg_gp_nvg_black`已要求Calibrator；不得用本节旧数字回滚。

- 当前共有 314 条制作配方，A2–A6 共 295 条。其中 294 条的 Calibrator 用量都为 1 个，并统一设置 `Destroy=1 / Changehealth=0 / MinHealth01=0.25`，所以它现在是每次制作直接销毁 1 个的一次性消耗品。A1 的 17 条配方不要求它。
- 唯一 A2–A6 例外是 `mmg_gp_nvg_black`：该 A6 配方消耗原版 NVG 与 A1–A6 六种阶段核心，却不要求 Calibrator。现有证据无法证明这是有意免除还是遗漏，修改前必须由用户明确决定。
- 742 条拆解配方中，Calibrator 作为拆解目标和产出均为 0，当前不存在 Workbench 回流。
- 旧 `recipe_profiles_v2_proposal.json` 将其设计为不可堆叠、`Destroy=0 / Changehealth=-2 / MinHealth01=0.05` 的可维护工具，与现行 294 条 `Destroy=1` 配方冲突。“可维护的阶段里程碑工具”是本次审计的**推荐但未批准**方向，不是当前运行事实，也不是已获授权的施工方案。
- v4 仍没有 Calibrator 目标；CJ 42 窗口 init/full-stack 178.346126/1783.461261 与 v4 制作实现敏感性都只是规划情景，不是玩家实得或正式周需求。
- 用户只需先决定三项：是否批准可维护工具方向；MMG 全景夜视仪是否统一要求 Calibrator；是否确认 NPC 不出售、不回收，只保留玩法获取与 P2P。批准后还需把 Mod_Edit、294 条配方、MMG 例外、CJ/任务供应和 PBO/RPT/UI/耐久测试作为一个原子候选，不能只改单个 JSON 字段。
- 工件为 `build_qpk_calibrator_governance_audit_v1.py`、`qpk_calibrator_governance_audit_v1.csv`、对应 MD 和 summary JSON。正式内部价值、NPC 售价和 NPC 回收价继续为 0；本审计未修改 Workbench、Mod_Edit、CJ、任务、Market、Trader、TraderZone、types、price v3 或 v4 设计文件。

### 18.16 退役模组与 42 旧比特币车辆清理

- `MJO Fish` 共退役 148 个 Market classname。`Fish.json` 是混合分类，精确删除 53 个 MJO 父项及 86 个 Variant，保留 10 个原版鱼类；`Fishing.json` 仅删除 9 个 MJO 工具/鱼饵，保留 4 个原版物品。原版 `Fish`/`Fishing` Trader 路由没有删除。
- `ALECarLock` 在当前 6.1 没有 Market/Trader/Zone，只清理 mission Hardline 的 1 条残留；`BZ Garage` 没有 Market/Trader/Zone，清理两份 Hardline、`cfgeconomycore.xml` 注册和专用 types 文件。Expansion 原生 `ExpansionCarKey`、`ExpansionCodeLock` 未动。
- 42 `Better_Cars` 退役 21 个旧车辆/配件分类，涉及 207 个独立 Item、602 个 Variant、809 个唯一 classname；对应 21 个 Market JSON 已移出活动目录，精确清理 652 个 Zone 键。共享车辆部件定义和未被用户明确要求卸载的旧车辆模组其他玩法引用没有越界删除。
- `Better_Cars` NPC/Trader 外壳保留，只剩 `Batteries:3`、`Vehicle_Parts:3` 和手动 `glowplug:3`。Carpack 只是已登记的未来替换方向，本轮没有新增车型、零件、价格、`SpawnAttachments` 或库存。
- 本轮 32 个活动文件全部备份到 `workspace/backups/2026-08-14_mod_retirement_market_cleanup/`。32 行逐文件合同记录变更前后 SHA；959 行 classname 排除合同用于阻止下游重新生成退役商品。
- 当前静态基线为 151 Market、2,895 独立 Item、5,306 唯一 Variant、32 Trader、7 Zone、11,091 Stock 键、191 活动 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`。global/price v3 与退役集合交集为 0；canonical staging v1 的活动文件哈希已改变，生成候选前必须重基。
- 2026-08-24 追加退役 `MBM_2000FORD350`、`MBM_JLTV`、`MBM_LANDCRUISE100`、`MBM_MERCEDESSPRINTER`、`MBM_PORCHE918SPYDER` 和 `NAMANTH_BOXTRUCK`。活动 Market/Trader/TraderZone 的相关 classname 复核仍为 0，因此本轮不重复删 Market 文件或 Zone 库存。
- 这 6 组旧 types 文件已从 mission `cfgeconomycore.xml` 取消挂载，但原文件均保留在 `vehicles_ce`。`benz_types.xml` 中的 5 个非退役 `JGC_G63W463*` 条目已原参数拆到并挂载 `JGC_G63W463_types.xml`，避免误伤 G63。
- 两份 Hardline 各删除 453 键，Inedia/NoCarDamage 各删除 86 项，MPG CarFellingTrees2 删除 107 项。差异合同、XML/JSON、125 份 CE 挂载闭包及 Market 全量校验均静态通过；备份为 `Project Manage/Backups/VEHICLE-MOD-RETIREMENT-20260824-PRE/`，完整重启/RPT/商人 UI/世界验收待执行。

### 18.17 全局活动 Market 价格覆盖边界

- 当前 151 个 Market 文件包含 2,895 个独立 Item 和 5,306 条 Variant 记录，去重后为 8,082 个活动 classname。Variant 继承父项价格，因此 8,082 不是 8,082 个独立价格字段，但它是必须审计的完整可交易身份范围。
- price v3 的 1,296 项只覆盖普通市场受管成品和已审查外围支持物，不等于全服全部 Market。它当前命中 1,226 个活动 classname：1,156 个已分配公式但正式数字被阻塞，70 个 HOLD 不得输出价格；活动覆盖率为 15.169512%。
- 6,856 个活动 classname 尚未进入 price v3，集中包含黑市重贴图、FOG/MMG/AP 外观与服装附件、共享车辆零件、原版服装/旗帜等。它们必须先逐类决定维持旧价、纳入重算或退役/后置，不能自动套用 A1—A6 武器护甲公式。
- 另有 70 个 price v3 classname 尚未进入活动 Market（Mode 1=45、Mode 2=25），必须先按 Item/Variant/Trader 正确结构补定义，不能仅写价格。
- 当前生成的 NPC 具体数值和活动价格写入均为 0。现阶段可以开始建立隔离数值候选，但不能直接批量调整 live；还需冻结材料内部价值、NPC 周回收预算、预计回售量、A1—A4 便利倍率、配件/弹匣/弹药倍率，并完成满弹匣、弹药盒和递归附件套利测试。
- 完整逐 classname 证据为 `global_market_price_coverage_audit_v1.csv`，对应生成器、中文报告和 summary 均在 Market System Rebuild 工作区。本审计未修改活动 Market、Trader、TraderZone 或价格。

### 18.18 2026-08-14 战斗市场活动收口

- 战斗装备已按简单统一规则写入：普通商品高价直购、5%低回收；A5/A6、战略弹匣和终局支持物禁止 NPC 直售，只给固定低额回收；爆炸物完全不进入 Market。
- AP/SNAFU 已从 42 精确迁出，黑市其他分类未改；20 个缺失定义已补齐；AP 同色头盔附件与功能 Variant 已修正。
- 14 个经 SNAFU Mod_Edit 源码确认的弃用 classname 已原子迁移到 13 个规范类，涉及的 Market/Trader/Zone/Hardline/CJ/Loadout/spawnable/Workbench 已同步；旧类活动引用为 0。
- 当前静态基线：148 Market、2,887 独立 Item、5,293 唯一 Variant、32 Trader、7 Zone、11,055 Stock、188 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`。当前 Workbench 为 312 制作、737 拆解。
- 当前 Market/Trader 全量 180 个加载 JSON 已同步到 `workspace/staging/combat_market_price_v1`；另镜像 5 个不会被加载的压缩包/无扩展名文件。旧 74 文件快照、旧 candidate CSV、314/742 manifest 和 09:18 覆盖数字均是变更前历史证据。
- 下一步不是继续分析战斗价格，而是做服务器 RPT/UI/买卖/同色附件/满弹套利验收，并开始非战斗普通商品的简单分层定价。

### 18.19 2026-08-14 非战斗第一批与独立商人施工

- 41 个普通非战斗分类共709个Item已按“旧价乘5后分品类限幅”的简单规则写入：食品饮料上限10,000、服装30,000、医疗40,000、生存/建材工具50,000、车辆零件80,000 Hryvnia；玩家回收统一5%，13个Hryvnia Trader对应分类为Mode 1。
- 钓鱼 Trader 已恢复为 `Fish:2` 与 `Fishing:1`。原版鱼类/鱼肉只回收，渔具可买卖；本轮没有修改 `Fish.json`/`Fishing.json` 数值。新钓鱼模组 classname 与鱼种难度表到位后再定最终价格，MJO旧类不得恢复。**这是 2026-08-14 当时状态，现行高激励基线见第 18.26 节。**
- AP WEAR 以8份活动types为依据建立8分类/485 Item及独立Trader，价格12,000—25,000、回收5%。QPK独立Trader只含6种普通材料，价格12,000—100,000、回收2%；六种阶段核心和 `QPK_Calibrator` 不进入NPC。**这是 2026-08-14 当时状态；两个 NPC 与独立 Zone 已于 2026-08-23 写入，见 18.27。**
- 42 `Better_Cars`已用11辆CarPack近似替代旧车；当时沿用旧车5M—35M内部值，当前完整包价已由18.36调整为8/20/32/45 BTC。72个精确types部件继续作为Mode 3随车件。classname静态门禁通过，但本地缺完整CarPack config，必须做RPT、购买生成及附件槽位实测。
- 本批没有修改制作/拆解。此前SNAFU规范迁移造成Workbench由历史314/742变为当前312/737，12个AJW与3个SNAFU无来源高容量弹匣已经集中登记给制作Agent；这些战略弹匣不得因无来源改成 NPC 直售，但普通商品可按自身商店定位单独判断。
- 当前静态基线由本节取代18.18末尾旧快照：159 Market、3,461独立Item、5,293唯一Variant、34 Trader、7 Zone、11,629 Stock、201 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`。

### 18.20 2026-08-17 AP/SNAFU 普通市场文件收口

- 官方 Wiki 与 `experimental@6dacd00f6d943ebbd99e0cf1baad93f470d96419` 再确认：Market identity 只能定义一次；Trader 单品权限覆盖分类权限；Mode 3 仅用于隐藏随附件；Zone Stock 不替代权限。
- 6 个旧 `Bitcoin-AP-*` 分类的内容已合并到 `AP-Helmet-Rookie.json` / `Ap-vest-Rookie.json`，旧文件退出加载。AP 114/114、SNAFU 129/129 个受管 classname 均为唯一 Market identity 并匹配普通商人目标模式。
- 42 Zone 已删除 19 个残留 AP 和 22 个普通 SNAFU Stock 键；WestBrook/Waldoboro 已补齐目标键。Black Retext 三分类仍由 `BIG_GUNS` 使用 Bitcoin buy-only，未改商品和价格。
- 本次规范的 24 件 SNAFU 武器均有当前 Workbench 合成结果；`SG552_Gun`、`SNAFUSR3_Vikhr` 只有 Mod_Edit config+合成来源而没有 active types，因此没有擅自补 CE。`SG552_Gun` 已在两份 Hardline 明确登记 rarity 5。
- 本次 AP 范围确认 46 个精确 classname 没有野外、合成、活动或可拾取 AI 的直接来源：Mode 1 普通商品19、Mode 2 成品23、Mode 3 Vulkan隐藏件4。完整名单写在 HANDOFF 的 2026-08-17 10:22 记录，交玩法来源 Agent；普通商品是否直购按商店定位判断，A5/A6 禁直购不变。
- 当前静态基线：153 Market、3,572 Item、5,317 Variant、8,772 去重 identity、34 Trader、7 Zone、11,774 Stock、195 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`。工具和22文件备份分别为 `apply_ap_snafu_market_completion_v1.py` 与 `2026-08-17_ap_snafu_market_completion_v1_pre_apply`。

### 18.21 2026-08-17 42 除颤器与维修工具迁移

- 42 `Defibrillator` 仍只接受 Bitcoin，`defibrillator` 保持 Mode 0 和 40,000 原价。
- `electronicrepairkit` 改由中心 `Components` 回收，`weaponcleaningkit` 改由中心 `Weapons` 回收；两个分类都是 Mode 2，玩家不能购买。
- 两工具基准价 40,000、`SellPricePercent=5.0`，满状态单件最高回收 2,000 Hryvnia。42 Zone 旧库存键已删，Rookie Zone 键存在。
- CarPack 本轮完全不改，继续列为实车测试遗留；CDS 普通/特殊消音器因只有外观差异而统一价格。
- MMG 和其他黑市装备下一步必须对照 `Custom Mods/Mod_Edit` 对应 `config.cpp` 的实际防护、容量、耐久及功能参数；物品无非商店来源时，是否禁止直购仍按其商店定位判断。
- 当前静态基线：155 Market、3,572 Item、5,317 Variant、8,772 identity、34 Trader、7 Zone、11,772 Stock、197 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`。

### 18.22 2026-08-17 42 Mod_Edit 装备价格重算

- 五套 MMG 无损装备的 Mod_Edit 属性一致：99,999 耐久，护甲/头盔弹道伤害系数 0.1，衣裤腰带 150 格、背包 300 格、小配件 50 格。统一价格为护甲/背包 15M、头盔 12M、衣裤腰带 8M、小配件 3M，整套 81M–84M。
- MMG Admin 五件均为 `scope=2` 玩家物品，只是 Admin 外观，不是管理工具。按 150/300 格与继承防护设为 1M/3M/6M/10M 档，整套 26M。
- 蝙蝠宝贝耐久 1,000,000，护甲弹道伤害系数 0.1，整套价 40M；追踪者背包组耐久 999,999，300+60+40 格，价格 15M+5M+3M=23M。
- 73 件继续由 `AP_Armor` 以 Mode 0 出售，全部价格是 1 BTC 整数倍。Trader/Zone/库存/classname 未改。
- CarPack 和 CDS 消音器按用户要求未改。Black Retext/MagLoader 在当时未有足够功能证据，本节当时保留现价；后续已由 18.23 根据用户确认性能和 MagLoader 活动配置完成调价。
- 备份为 `workspace\backups\2026-08-17_42_modedit_equipment_reprice_v1_pre_apply`；验证 `BLACK_MARKET_MODEDIT_REPRICE_VALID=true`、`ACTIVE_MARKET_VALID=true`，0 warning/error。

### 18.23 2026-08-17 BRTX 与 MagLoader 功能定价

- BRTX 是黑市商店专属的特殊皮肤强化枪；用户确认相对原型约有 5% 摇摆/后座改善。它们应有性能溢价，但不能伪装成大幅属性跃迁。
- 89 把 Scar-H 为 4M，84 把 `.338` Kivaari 为 8M，47 把重口径 Alligator 为 15M Bitcoin。三类继续由 `BIG_GUNS:0` 只购买，库存上下限均为 1。
- 活动 `MagLoaderBoxConfig*.json` 确认三档每发装/退弹时间为 0.5/0.35/0.2 秒，耗电为 3/2/1，单次损耗约 1.0%/0.9%/0.8%。价格为 3M/5M/8M，仍由 `MagLoader:0` 只购买。
- 220 把 BRTX 和 3 种 MagLoader 的 active types 均为 nominal 0；这是符合商品定位的黑市专属来源，不因无野外/合成来源自动禁止直购。
- 本轮只改 222 个 Item 的 `MaxPriceThreshold/MinPriceThreshold`；classname、顺序、附件、库存、Trader、Zone、CarPack 和 CDS 均未改。备份为 `workspace\backups\2026-08-17_42_brtx_magloader_reprice_v1_pre_apply`。

### 18.24 2026-08-18 DMT 标准 FLIR 接入黑市

- 仅接入最低标准档：`DMT_FLIR_Rangefinder`、`DMT_FLIR_StarlightOptic`、`DMT_FLIR_KazuarOptic`、`DMT_FLIR_HuntingOptic`、`DMT_FLIR_ACOGOptic`、`DMT_FLIR_ACOGOptic_6x`。不包含进阶 AI 与赞助档。
- 6件标准档功能相同：150米视线内活体热高亮，无骨骼显示。最初主物品内部值25M并随附电池，递归结算会占用26 BTC；当前已由18.36调整为35 BTC且不带电池。
- 新分类`Bitcoin_DMT_Standard_FLIR`由`MagLoader` Trader以Mode 0加载，与CDS消音器共用同一NPC和`hm_plus_bitcoin`货币。Market/42/World库存路径仍为1，但当前六件`SpawnAttachments=[]`。
- 这 6 件既有 active types/Hardline/Mod_Edit 证据，也已有 A6 Workbench 和 CJ 奖励路线。本轮保留原玩法来源；用户的黑市直购决策取代文档原“仅 A6 候选”建议。
- 备份：`workspace\backups\2026-08-18_dmt_standard_flir_blackmarket_v1_pre_apply`。验证：`DMT_STANDARD_FLIR_BLACKMARKET_VALID=true`、`ACTIVE_MARKET_VALID=true`，0 warning/error。

### 18.25 2026-08-18 Inedia T1/T2 医疗商品接入

- 中心 `Medicals` 新增 T1 药片、工具、空容器 3 分类，共 15 个商品身份。使用 Hryvnia，Trader Mode 1，单价 75,000—300,000，`SellPricePercent=5`。
- 42 `Defibrillator`调整为高级医疗与电气器材商人，新增T2对应3分类，共14个T2商品身份。使用Bitcoin、Trader Mode 0、禁止玩家回售；最初1M—5M内部价已由18.36调整为2—8 BTC，除颤器另为3 BTC。
- 容器使用白色 Item + 黑色/迷彩 Variant，`SpawnAttachments=[]`；T1/T2 分别写入正确 Zone，World 同步。两份 Hardline 精确设为 T1 rarity 4、T2 rarity 5。
- T3、`InediaInfectedAI_Calcium` 和旧 `HEROCLAN_AdvInedia_*` 未进入 Market。当时用户确认2.0 PBO已打包，但后续RPT证明该包因重复类启动失败；现行源码为2.0.2，尚无新PBO、双端部署或运行证明。29个Market商品身份仍是静态配置事实，实际可用性依赖2.0.2通过打包、RPT和药效/姿态验收。
- 备份：`workspace\backups\2026-08-18_inedia_t1_t2_market_v1_pre_apply`。验证：29 个身份唯一、路由/权限/声望一致，`ACTIVE_MARKET_VALID=true`，0 warning/error。

### 18.26 2026-08-18 AP Fishing 高激励基线与当前指导收口

- AP Fishing 当前权威事实是高激励版：71 种完整鱼由 `Fish:2` 只回收；T0/T4、鱼片和 Quest 专属类不进 Market。
- T1 全套可买卖且回收 15%；T2 竿/轮 Mode 2 只回收，线/钩有限买卖且回收 15%；T3 全套 Mode 2 只回收；8种AP鱼饵 Mode 0 只购买。《渔夫之书》已从Market完整移除，改由1301 Quest接取时免费发放。
- `apply_ap_fishing_market_v1.py` 已同步当前价格和权限，`--check` 会验证 71 鱼、25 Item/31 identity、6 个 Mode 2、8 个 Mode 0 及 T0/T4/鱼片/图鉴排除。
- 本节当时静态基线为 162 Market、3,599 Item、5,325 Variant、34 Trader、7 Zone、11,842 Stock 键、204 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`；现行基线见 18.27。
- 当前未完成的是重启后 UI/买卖/鱼体状态入账与包含通勤成本的小时收益验收，不是“等待新鱼种或首次定价”。
- 本次只同步文档和验证工具，没有修改活动 Market/Trader/TraderZone，且按用户要求未建立备份。

### 18.27 2026-08-23 AP WEAR/QPK 独立 NPC 与 TraderZone

- `AP_WEAR.map` 使用 `ExpansionTraderMirek.AP_WEAR`，位置 `(3460.710693, 34.494152, 6429.529785)`，朝向 `(170.469818, 0, 0)`；专用 Zone 含 485 个 AP WEAR 库存键。
- `QPK_Materials.map` 使用 `ExpansionTraderMirek.QPK_Materials`，位置 `(5623.562500, 28.734995, 5394.646484)`，朝向 `(130.091507, 0, 0)`；专用 Zone 仅含 6 个普通材料库存键，核心材料与 `QPK_Calibrator` 继续排除。
- 两个点均位于原有 200 米交易区内。Expansion 源码按覆盖区中心距离最近者绑定 TraderZone，因此两个专用 Zone 采用 1 米半径，使新 NPC 在中心距离 0 时精确绑定，同时不捕获最近 3.995/2.710 米外的旧 NPC。
- Market 商品、价格、回收比例和 Trader Mode 均未改变；初始库存均为各 Item 的 `MaxStockThreshold=1`。
- 本节当时静态基线：162 Market、3,599 Item、5,325 Variant、34 Trader、9 Zone、12,333 Stock 键、206 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`；现行基线见 18.29。
- 当前门禁：服务器完整重启后检查 RPT、NPC 模型/站位/朝向、UI、Hryvnia 扣款、买卖方向与库存持久化。静态通过不等于实机通过。

### 18.28 2026-08-23 中心车辆/P2P 与商人外观调整

- 中心 `Vehicles` 使用 `ExpansionTraderMirek`，新位置 `(5636.599121, 28.758051, 5406.565430)`、朝向 `(133.008041, 0, 0)`；对应中心陆地购车刷新点为 `(5649.727539, 28.734999, 5417.433594)`、朝向 `(-51.679569, 0, 0)`，两者距离约 17.043 米。
- P2P 继续使用 AI 商人功能族，只把人物从 `ExpansionP2PTraderAIIrena` 换为 `ExpansionP2PTraderAIMirek`；新位置 `(5614.329102, 29.201323, 5407.729004)`、朝向 `(94.577873, 0, 0)`。
- 本节调整完成时有 27 名人形 Market Trader，其中 26 名为 Mirek，唯一允许的例外是中心 `ExpansionTraderSeth.Vehicle_Parts`。加入 HP CRAFTER 后当前为 27 Mirek + 1 Seth，见 18.32；P2P 也为 AI Mirek，兑换机和 Quest NPC 不属于本规则。
- Fishing 外观为橄榄色圆边帽、黄色雨衣、绿色工装裤、绿色涉水靴、黄色工作手套和绿色防水包；Spire Boat Trader 已补绿色 MMG 靴。
- 本次没有改变商品、价格、权限或库存。静态门禁全部通过；仍需重启后检查人物外观、P2P/Market 交互、车辆落点和碰撞空间。

### 18.29 2026-08-23 HP CRAFTER 基础工作台商店

- 新建 `HP_Crafter\HP_Crafter_Workstations.json` 与 `Traders\HP_Crafter.json`，上架 KIT 和 7 个专用附件。货币为 Hryvnia，分类 Mode 0 只购买，不允许玩家回售。
- KIT/铁砧/台钳固定价为 15,000/10,000/10,000；钻床/砂轮机 7,500；电烙铁 5,000；锉刀/注油壶 2,500。全部使用 `1/1` 静态库存和固定价格。
- 仅售 `HP_Crafter_Kit`，不直接出售其部署结果 `HP_Crafter` 或不可拆公共台 `HP_Crafter_Static`。8 件均有当前源码 `scope=2` 与 active types 精确证据。
- 当前 374/755 配方只使用铁砧与台钳；另外 5 个附件虽然能挂入工作台，但当前不影响配方解锁。商店保留完整附件系列，后续文案不得误导玩家必须买齐。
- 8 个库存键写入既有中心 `Rookie_Trader` Zone。`ExpansionTraderMirek.HP_Crafter` 已放置于 `(5649.829590, 28.782780, 5396.346680)`、朝向 `(-134.847641, 0, 0)`，使用工作坊外观并复用现有 Zone，不建立独立 TraderZone。
- 本节当时静态基线：163 Market、3,607 Item、5,325 Variant、35 Trader、9 Zone、12,341 Stock、208 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`；现行基线和 NPC 落地状态见 18.32。当前仍无服务器重启、RPT、UI 或购买/部署实机证明。

### 18.30 2026-08-24 MBM Dune Buggy 接入中心 Vehicles

- 当前出售 Yamaha 的 `Vehicles` Trader 新增 `MBM_DuneBuggy:0`；货币仍为 Hryvnia，只允许购买。专用轮胎在该 Trader 使用 Mode 3，只作为随车附件隐藏。
- 活动 types/CE 注册精确类为 `MBM_DuneBuggy` 与 `MBM_DuneBuggy_wheel`，均无地图 CE 刷新；Hardline rarity 4 已存在。
- 整车基础价 140,000，轮胎 7,500。交付包含 4 轮、电瓶、散热器和火花塞；按 Expansion 递归附件计价，理论完整结算为 181,500—182,500。两个木箱槽不附赠木箱。
- 价格定位依据：作者声明该车为 AWD、300 格并有两个木箱槽；当前活动 Yamaha 为 30,000，普通 Cars 基础价约 40,000—640,000。Dune Buggy 高于 UAZ/Offroad 基础档、低于 Bus/Land Rover，并仍需实机确认驾驶性能和附件槽。
- 两个库存键已加入中心 `Rookie_Trader` Zone；没有新增 NPC/Zone，也没有改变中心陆地车辆刷新点。
- 本节落地时静态基线：164 Market、3,609 Item、5,325 Variant、35 Trader、9 Zone、12,343 Stock、209 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`；现行基线见 18.31。重启后必须验证 RPT、结算价、附件、启动和刷新点碰撞。

### 18.31 2026-08-24 容器/MMG Storage 与全市场无限库存

- Expansion 当前配置没有可用的“定时补货间隔”字段；源码确认 `MinStockThreshold` 与 `MaxStockThreshold` 为相同正数时属于静态库存，购买不会扣减 Zone 库存。本服统一使用 `1/1`，不新增模组无法读取的字段。
- MMG Admin五件退市后，全部Trader当前有效权限中共有7,091个可购identity，对应2,520个可见父项；递归`SpawnAttachments`另涉及77个依赖父项，合计2,597个Market父项均为`1/1`。7个受影响Zone的静态键保持为1。
- `Containers.json` 固定价为 35,000—95,000，`Tents.json` 固定价为 90,000—450,000；便携容器回收 5%，部署型容器回收 3%。帐篷同功能颜色已改为 Variant，避免重复独立定义。
- Expansion Safe Mini/Medium/Large 名义价为 200,000/450,000/900,000、回收比例 3%，仅在 `BuildingSupplies.Items` 以 Mode 2 接收；玩家满状态回收额分别为 6,000/13,500/27,000，NPC 不售卖。
- 新建 `MMG_Storage.json`，覆盖 HM Secure 奖励池内 24 个 MMG Storage KIT；名义价 80,000—400,000、回收 10%，`MMG_Storage:2` 仅回收。实际满状态回收范围为 8,000—40,000。
- `Containers:1`、`Tents:1`、`MMG_Storage:2` 只保留在 `BuildingSupplies`，`Components` 不再重复显示。复用已有 BuildingSupplies NPC，因此不需要新 Trader 或新坐标待办。
- 本节落地时静态基线为167/3651/5338/8874/35/9/12367/212；已被18.33的MMG Admin退市状态取代。容器/库存合同本身仍幂等通过；尚需完整重启后验证RPT、连续购买不减库存、Safe/MMG只出现回收方向及实际入账，并验证黑市护甲PBO与商品。

### 18.32 2026-08-24 HP CRAFTER 中心 NPC 坐标落地

- `ROOKIE_TRADER.map` 新增 `ExpansionTraderMirek.HP_Crafter`，位置 `(5649.829590, 28.782780, 5396.346680)`、朝向 `(-134.847641, 0, 0)`。用户提供的 `SurvivorM_Mirek` 通过 Expansion 对应 Trader 实体类实现，不能直接使用普通 Survivor 类替代商人实体。
- 外观为橙色施工头盔、焊接面罩、棕色飞行夹克、米色工装裤、黑色低帮登山鞋和黄色工作手套；均为活动原版有效 classname，不携带武器。
- NPC 距中心 Zone 中心 20.199 米，明确位于 200 米半径内；距 QPK 1 米专用 Zone 中心 26.322 米，不会误绑定。最近既有 Market NPC 为 Vehicles，距离约 16.717 米。
- Trader v13、8 个 Market Item、中心 8 个 Stock 键和 `1/1` 静态库存保持不变；没有新增专用 TraderZone，也没有改变商品、价格、权限、配方或 PBO。
- 当前Market商人已无待提供坐标项。本节落地时静态基线为167/3651/5338/35/9/12367/212，现行基线见18.33；完整重启后检查RPT、人物站位/朝向、服装槽位、交易UI、Hryvnia扣款、KIT部署和附件挂载。

### 18.33 2026-08-25 MMG Admin退市后的当前基线

- 原始`MMG_*_admin`五件套已从活动Market分类、`AP_Armor`路由及42/World共10个Stock键移除；CE、Hardline、JPC源码和`ZZSA_MMG_*`赞助类保留。
- 当前活动购买引用为0；其他五套MMG重贴图继续保留。该退市只完成配置与静态验证，尚无重启、RPT、Trader UI或购买回归证据。
- 当前静态基线：166 Market、3,646 Item、5,338 Variant、8,869 identity、35 Trader、9 Zone、12,357 Stock、211 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`。
- 当前无限库存合同：7,091个可购identity、2,520个可见父项、77个递归依赖父项，共2,597个静态父项；`apply_container_market_rebuild_v1.py`为`files_to_write=0`。

本节基线已被18.34新增三种BRTX弹匣后的状态取代；MMG Admin退市合同本身保持不变。

### 18.34 2026-08-25 BRTX 三种扩容弹匣接入 42 黑市

- 深链任务 `01a00f3f-2906-70d1-ba23-b82dc728ea4e` 新增 `BRTX_Kivaari_35Mag_Vanta`、`BRTX_ScarH_150RND_Drum`、`BRTX_Alligator_20rdMag`。活动 types 均为 `nominal=0/min=0`，不自然刷新。
- 三者分别加入现有 `Bitcoin-Black_Retext_Kivaari/ScarH/ALigator`。Market内部固定价为10M / 6M / 20M法币等值；`HM_Plus_Bitcoin`面额为1M，因此实际支付10 / 6 / 20枚BTC。对应枪械实付8 / 4 / 15枚BTC，弹匣溢价为25% / 50% / 33.3%。`QuantityPercent=-1`，购买时生成完整35/150/20发弹匣。
- `BIG_GUNS` 已用 Mode 0 引用三个分类，因此无需新建 Trader 或分类路由；42/World Zone 各增加三个 Stock=1 键，维持 Expansion 原生 `1/1` 静态无限库存。42 Zone 禁售，不能向该商人回售。
- 两份 Hardline 按对应 BRTX 枪械当前 rarity 写入；保留 Alligator profiles/runtime 的既有 7/8 差异。当前静态基线为166 Market、3,649 Item、5,338 Variant、8,872 identity、35 Trader、9 Zone、12,363 Stock、211 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`；库存合同为7,094/2,523/77/2,600，`files_to_write=0`。
- 本轮没有新建备份。四个 BRTX PBO 尚未构建、签名或双端部署；完整重启后必须检查 RPT、价格/库存、35/150/20 实际装填量、只兼容对应 BRTX 枪且不兼容原 SNAFU 枪，以及拆弹后是否存在可重复收益。

### 18.35 2026-08-25 《渔夫之书》退出Market并改由Quest发放

- `AP_fishing_book_guide`已从`Market/Fishing.json`商品定义、`Traders/Fishing.json` Mode 0权限和`traderzones/Rookie_Trader.json`库存键完整移除；Market不再购买或回收《渔夫之书》。
- `apply_ap_fishing_market_v1.py`同步改为永久排除图鉴，避免未来`--write`复跑把该书重新写回Market/Trader/Zone。工具`--check`通过：71鱼、25 Fishing Item/31 identity、6 Mode 2、8 Mode 0、T0/T4/鱼片/图鉴排除0偏差。
- 现行静态基线为166 Market、3,648 Item、5,338 Variant、35 Trader、9 Zone、12,362 Stock、211 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`。书籍改由1301“钓鱼之路 I：淡水大师”接取时免费发放；发书/保留与Trader UI仍待重启实测。
- 备份：`Project Manage/Backups/QUEST-NPC-FISHING-ROUTING-20260825-PRE/`。

### 18.36 2026-08-28 42 黑市整枚 Bitcoin 调价

- `hm_plus_bitcoin`在`Exchange.json`中的固定面额为1,000,000。本节完成时5个Bitcoin Trader共2,292个可见商品身份；现行数量见18.37。所有可见购买均按Expansion递归`SpawnAttachments`总价验证为1,000,000整数倍。
- 高级医疗：除颤器3 BTC；T2药片2/3 BTC；T2工具3/6 BTC；T2急救包/箱4/8 BTC。高级护甲六档由2/3/5/8/12/15调整为3/5/8/12/18/22 BTC。
- BRTX枪/扩容弹匣：Scar-H 6/9 BTC、Kivaari 12/15 BTC、Alligator 22/30 BTC；弹匣仍高于对应枪械。MagLoader三档5/8/12 BTC，普通和特殊CDS消音器统一8 BTC。
- 6件标准DMT FLIR统一35 BTC并将`SpawnAttachments`清空，不再随附低于一枚Bitcoin的`battery9v`。全局`Batteries`分类和Zone电池库存不受影响，玩家自行安装电池。
- 11辆CarPack保留现有完整轮胎、车门、车身件和电气附件。按当前递归附件最低价反算主车内部价后，完整包精确结算为8/20/32/45 BTC；主车的非整百万字段不是玩家最终支付价。
- 新增`workspace/tools/apply_black_market_bitcoin_reprice_v2.py`和`workspace/contracts/black_market_bitcoin_reprice_v2.json`；专项覆盖2,292个可见身份及11辆完整车辆，幂等复跑`files_changed=0`。旧`apply_noncombat_market_rebuild_v1.py`的CarPack生成价同步更新，避免复跑恢复旧价。
- 本轮调整21个Market JSON；Trader、TraderZone、types、Hardline和模组源码未改，也未新建备份。全量静态基线为166 Market、3,648 Item、5,338 Variant、35 Trader、9 Zone、12,362 Stock、211 JSON，0 warning/error，`ACTIVE_MARKET_VALID=true`；专项为`BLACK_MARKET_BITCOIN_REPRICE_V2_VALID=true`。
- 下一门禁：完整重启后检查RPT，并在5个42黑市NPC验证UI价、整枚扣币、禁止回售、DMT无电池，以及11辆车附件齐全且实际支付8/20/32/45 BTC。静态验证不能替代运行证明。

### 18.37 2026-08-28 T800 / REV-9 高级护甲接入

- 指定源码`lipesinoff_Rev9`的六个商品类加入`Market/T800_Rev9.json`，`AP_Armor`以Mode 0只购加载；42与World各有6个`Stock=1`键，CE为0/0/0且两份Hardline均为rarity 6。
- 固定价为躯干30、腿24、头盔18、面具12、手10、足10 BTC，整套104 BTC；无随附附件、不可回售，全部符合1,000,000整数倍合同。
- 原生Projectile/Melee/Infected传入系数0.2和FragGrenade 0.5已经高于现有普通黑市服装，因此没有继续降低伤害系数；仅把六件2,000耐久统一为800,000，并按部位补齐Terje melee/firearm。原有生化字段未扩大到头盔/面具。
- 当前静态基线为167 Market、3,654 Item、5,338 Variant、35 Trader、9 Zone、12,374 Stock、212 JSON，0 warning/error；Bitcoin专项为2,298个可见身份/11辆车且幂等通过。本轮未创建备份。
- 仍需重建/签名/双端部署`lipesinoff_Rev9` PBO，完整重启后用RPT、购买扣币、穿戴、容量、NVG槽及受控伤害验证；源码和JSON静态通过不等于实机生效。

### 18.38 2026-08-28 中心弹药退市、医疗/钉子调价与复活针来源

- `Weapons`、`Rookie_Snafu`、`TTC`、`AJW`四个Trader内共77个散装/盒装弹药身份统一为Mode 3；分类Mode与已有单品覆盖同时处理，弹匣保持原权限。
- 中心基础医疗21项改为10,000—250,000 Hryvnia固定价，Terje注射剂13项改为150,000—1,000,000；Inedia T1原75,000—300,000分层保持。`TerjeInjectorReanimatal`名义价1,000,000，但在`Medicals.Items`中为Mode 2，只允许回收、禁止购买；当前5%回收率对应满状态50,000。
- 复活针仍有四类活动来源：普通CE `nominal=3/min=1`；9份启用医疗空投各8%且最多1件；BTR最终巡逻`CombatMedical`池0.4；一次性Quest 902保证1件。旧Apache事件已禁用，`DNA_Keycards(No Use)`与Hardline稀有度不属于活动刷新来源。
- 本轮只取消商人直售，没有把普通CE改为0/0。若以后确定严格事件/任务专属，必须单独修改CE并经重启/RPT/落地掉落验证，不能仅靠Trader Mode宣称完成。
- 历史钉子规则已于2026-09-05废止：散装`Nail`按颗计价，不能沿用盒价100,000。当前估值Nail=100、NailBox=1,000、回收率均5%；BuildingSupplies和Components对两者均显式Mode 2，只回收且禁止购买。完好散钉每颗回收5，完整钉盒回收50。
- 新增`Project Manage/Market System Rebuild/workspace/tools/apply_center_progression_market_v1.py`并修正旧非战斗市场生成器的复跑边界。本轮未备份；全量静态基线仍为167/3654/5338/35/9/12374/212，0 warning/error，`ACTIVE_MARKET_VALID=true`。
- 下一门禁（2026-09-05钉子规则替代旧项）：完整重启后核对四名武器商人的弹药隐藏/弹匣保留、Medicals复活针只回收与全体药价，以及BuildingSupplies/Components两处散钉和盒钉均不可购买、回收金额符合按颗/按盒与耐久折算，并检查RPT。静态通过不等于实机通过。

### 18.39 2026-08-29 医疗回收降档、Inedia T1涨价与中心食品只回收

- `Medicals`加载5个分类/45个父商品。基础医疗21项和Terje注射剂13项购买售价不变，回收率5%→2.5%；复活针继续Mode 2只回收，满状态理论回收50,000→25,000。
- Inedia T1的6药片/3工具/2容器共11项售价精确提高50%，新范围112,500—450,000；回收率设为1.5%，使提价后的实际回收额仍比原始5%状态降低55%，而不是使用2.5%时只降低25%。
- 中心`Consumables`的果蔬、食品、肉类、饮料、HM食品五分类共111个身份，由Mode 1统一改为Mode 2。NPC不再出售，仍可回收；价格、Market库存、CE、狩猎、任务、空投和事件来源未改。
- 42黑市高级医疗不在本轮范围。两份施工工具已写入固定价格、回收率和权限保护合同，幂等复跑0变更。
- 全量静态基线保持167/3654/5338/35/9/12374/212，0 warning/error，`ACTIVE_MARKET_VALID=true`；未创建备份。完整重启后检查RPT、两档医疗回收率、Inedia新售价、复活针只回收及Consumables不可购买/可回收。

### 18.40 2026-08-29 常规船只完整价格提高10倍

- Rookie与Spire两处`Boats` NPC共用同一Trader/Market分类。五种常规低价船按`SpawnAttachments`递归完整包结算，而非只乘船体字段。
- 原版小艇及Black/Blue/Camo Variants完整价27,180→271,800；Utility Boat含TruckBattery+GlowPlug为29,000→290,000；JMC STAG黑/红/白含SparkPlug均为49,500→495,000 Hryvnia。最大递归阈值同样精确10倍。
- 共享SparkPlug、TruckBattery、GlowPlug价格未改，船体已反算；Variants、附件、`1/1`静态库存、Hryvnia、Trader/Zone、CE和钥匙Quest均保持。
- `ExpansionLHD`经用户确认在本服实际游戏内容中不存在，已从Market、两份Boat Zone、CE types、MarketSettings、VehicleSettings、两份Hardline和MPG车辆表共9处活动引用全部删除；备份历史不改。
- `apply_boat_market_price_v1.py`现强制LHD活动引用为0，幂等复跑0变更且`BOAT_MARKET_PRICE_V1_VALID=true`。退役后全量为167/3653/5338/35/9/12372/212、0 warning/error，未备份；完整重启后确认两处船商无LHD、RPT无缺类，并验证其余船价、附件和落点。

### 18.41 2026-08-30 A3+ 普通来源收口

- 新经济合同覆盖本 Guide 中所有历史“A3/A4 可高价直购”表述：普通 CE、普通 Hryvnia NPC 直购的最高阶段统一为 A2。A3+ 继续由 Workbench、钥匙副本、事件箱或明确的一次性任务提供；不是由把 TraderZone 库存归零来伪造权限。
- 以活动`profiles/WorkbenchCrafting/CraftingRecipes.json`的822条运行表生成624个 A3-A6结果，再补入12个活动挂载 types 中已验证的`.338/.50`终局补给。6份实际挂载 types 的374个正 `nominal/min` 节点已精确置为`0/0`，类定义、已受控来源及非 types 文件均保留。
- Hryvnia Trader 以`Items`覆盖`Categories`的官方规则逐 classname 加入/改写 Mode 2：AJW 66、AP_Rookie 21、FOG 20、MMG 6、Rookie_Snafu 146、TTC 87，合计346。已有 Mode 2/3不改；六件 DMT Standard FLIR 仍为 BTC Mode 0，不混入本轮。
- 为避免两把活动 CE 已识别`.50`变体失去来源，`LC_Table_Weapons_DUNGEON_MIX_A6`新增`LC_predefined_AJW_AK50_MD_Black`与`LC_predefined_AJW_M82_MD_Black`各4个相对权重，表总权重600→608，不增加 Key103 箱体数或单箱抽取次数。共享`LC_Table_Ammo_TTC`严格保持原7项；新建仅供`CJ_Key103`使用的`LC_Table_KEY103_A6_TERMINAL_AMMO`（原7项加6项终局补给），原位替换26次 Key103 的共享表抽取，故箱体数和抽取次数均不增加，且不会泄漏到低阶/公共路线。该两类 AJW 变体的运行 PBO resolved-config/弹匣兼容仍需RPT和实机确认。
- 施工工具及合同：`Project Manage/Market System Rebuild/workspace/tools/apply_a3plus_source_control_v1.py`、`workspace/contracts/a3plus_source_control_manifest_v1.json/csv`。备份：`Project Manage/Backups/CE-MARKET-A3PLUS-SOURCE-CONTROL-20260830-PRE/`。静态门禁为 A3PLUS_SOURCE_CONTROL_VALID、XML解析与全量`ACTIVE_MARKET_VALID=true`；尚未构建、部署或重启，不能写成实机通过。

---

### 18.42 2026-09-05 钉子止损及全量价格复核

- 当前Nail与NailBox均只回收，BuildingSupplies和Components分别显式Mode2；Supplies估值100/1000，回收5%，满耐久单颗5、60颗300、完整盒50。旧100000单颗和钉盒可购描述全部被此规则替代。两维护生成器及校验器已同步，避免旧价/跨商人购买入口复发。
- 三个TERRA High子代理完成167 Market文件价格分区审查，主线程复核发现MMG帐篷材料成本13450、满耐久回收30000的正收益闭环；活动Craft_Tent=true，尚未修复。4种BRTX弹匣因隐式满弹增加20,000/4,000/10,000/14,000，破坏整数BTC最终价，也尚未修复。不能依据结构校验通过宣称经济安全。
- 完整结论、公式、源码依据、待补62条弹药回售及3类MagLoader运行配置证据见`Project Manage/Market System Rebuild/workspace/reports/market_price_review_20260905.md`。下一步先确认上述两项修复，再做实际交易验收。
- 测试服同步Supplies.json、Traders/BuildingSupplies.json、Traders/Components.json至实际-profiles；不清库存、不需PBO，完整重启后核验两NPC禁购、单颗/整堆/整盒回收LOG。其他价格尚未改动。

### 18.43 2026-09-05 容器与BRTX修复已写入（覆盖18.42未修复状态）

- 普通Containers非Safe7父项、Tents6父项、Furnishings枪架1父项，共14父项/25变体展开身份，NPC仅出售不回收（Mode0+SellPricePercent0），原Min/Max价格各提高5倍。背包/衣物/炉灶/黑市特殊容器不改。BuildingSupplies显式逐项/变体防止旁路。
- MMG Storage/Expansion Safe共27身份继续Mode2、不开放购买、不涨价。仅MMG帐篷KIT回收从10%改2%，满耐久6000，低于商店材料13450；其他MMG与Safe回收率不变。
- BRTX五种独立弹匣QuantityPercent=0且无附件，购买仅一个空匣：Alligator20=30BTC、Kivaari10/25/35=12/12/15BTC、SCAR-H150=9BTC。空附件数组本身不能禁止默认填弹，必须保留QuantityPercent=0。
- 静态全量校验与14种错误注入通过，52个容器最终身份方向通过；BTC2298根已计算价格无非整数百万项，3类MagLoader类型未知仍待证据。
- 本轮上传Market的Containers、Tents、Furnishings、MMG_Storage、Bitcoin-Black_Retext_ALigator、Bitcoin-Black_Retext_Kivaari、Bitcoin-Black_Retext_ScarH七个JSON，加Traders/BuildingSupplies.json，共8文件。无需PBO、不得清库存，完整重启后实测价格/方向/空匣与扣币。详细价格和验证见Market Handoff本日末条。

### 18.44 2026-09-07 AP钓鱼收益优化

- 54种普通鱼满状态回收约上调小型50%/中型40%/大型25%，17种被动螯虾/奖杯/旧回收≥25000鱼保持，最高仍180000；全部只回收，75%回收率不变，基础价已反算。实际每条仍按数量、健康和食物状态折价。
- T1竿/轮/线/钩售价6000/4000/1500/750，整套12250；T2线/钩5000/2500。15%回收、无限直购保留；T2竿/轮与T3仍只回收；饵料和钓鱼箱保持原价。旧高激励价格表对应字段被本节替代。
- 用户LOG26条鱼实收18780，同期渔业采购23345；这是Market现金流，不是每小时或完整利润。详细统计与源码量纲解释见Market workspace/reports/ap_fishing_income_review_20260907.md及AP Fishing Handoff16.7。
- 仅上传Market/Fish.json、Market/Fishing.json；无PBO/Trader/Zone变动。专项与全量静态通过，完整重启后验证新价及鱼体折价，记录手钓/陷阱/任务各来源净收益。

### 18.45 2026-09-07 高级鱼饵包装补正

- 鱼价上涨与六件渔具降价保留。高级鱼饵1500/满组10粒；按管理员一包两组的实测描述，包装6000→2700，较两组单买3000优惠10%。PUBLIC未公开拆包动作，每组满10粒/合计20粒仍待实机确认，不能伪称源代码证明。
- 普通鱼饵价格和全部AP饵料仅购买/回收0/无限库存保持；包装不附带额外SpawnAttachments。兼容Hook/Jig价格与AP钩阶梯不一致暂只记录，未涨价。
- 生成器/专项测试同步，容量与4项包装故障注入通过。新增仅Fishing.json改变，累计上传Fish.json和Fishing.json，完整重启后核对组与包的扣款、内容数量和拒收。详见AP Fishing Handoff16.8及综合收入报告。

**给后续模型/对话的固定指令：** 先读取本文件，再读取本次涉及的实际 JSON；不要只依赖本文的快照。所有修改要同时更新实际配置和本文件的当前基线/变更日志。若运行期文件与本文不一致，以实际文件为准，并在完成核对后修正文档。

### 18.46 2026-09-09 TTC .338 拆盒套利定价修复

- `TTC_Ammo.json`中`ttc_ammo_338`回收比例100%→5%，保持1000/发基础价和5000/盒。源码一盒10发，满状态拆盒回收由10000降至500；相对5000买盒成本净亏4500。数量、库存和Trader权限未改。
- 当前本地TTC散弹/盒弹分类与单品均Mode 3隐藏依赖，与用户线上能直接成交的报告存在部署状态差异。隐藏依赖可参与附件交易；不得将本地静态修复写成服务器实测通过。
- 旧价格候选生成器固定保留`.338`修复，活动校验器加入10发回收额严格低于盒最低买价门禁。新价通过，原100%与零利润边界故障注入被拒绝；全量215 JSON、0 warning/error。未重生成旧staging，未改其他口径；`.50Beo/.50BMG`同型定价组合仍待专项确认。
- 仅同步`profiles/ExpansionMod/Market/TTC_Ammo.json`至真实服务器`-profiles`对应位置，无需PBO/客户端更新或清库存；完整重启，核对线上Trader权限及RPT/交易金额。五文件备份、修改清单及证据见Market HANDOFF的2026-09-09 TTC记录。

### 18.47 2026-09-09 盒装价差统一修复（静态通过）

- 四种散弹`ttc_ammo_50beo`、`ttc_ammo_50bmg`、`ajw_ammo_338`、`ammo_expansion_338`基础价保持1000，回收率100%→5%。四种盒价仍5000，拆盒回收分别1000/500/500/750，无正收益。之前TTC .338保持5%。
- Nail保持100/颗、5%回收=5；NailBox基础价1000保持，回收率5%→35%=350，与批准的70颗/盒一致。BuildingSupplies与Components均继续对两者显式Mode2只回收。此条取代旧记录“整盒回收50”；实际PBO拆盒数仍需部署后核实。
- 4份活动文件共5个比例字段改变，Trader/Zone/其他商品不变；价格候选生成器、两套钉子生成器、全量校验器及故障回归同步。全215 JSON无错误，5组弹药旧价及收支相等边界拒绝、钉子回收一致性/生成器恢复/原有经济门禁通过。
- 仅同步Market/TTC_Ammo.json、Market/AJ_Weapons_Ammo.json、Market/Ammo.json、Market/Supplies.json到真实服务器-profiles，完整重启查RPT和收款。无需PBO/客户端更新/清库存。本地已修，尚未部署或实机验收。备份和全部12文件清单见Market HANDOFF同日“盒装价差统一修复”。

### 2026-10-02 — 全市场20%价格、100%回收与双向交易（当前配置规则，运行待验）

- 用户最新授权覆盖历史黑市只购买、普通高阶仅回收、隐藏弹药以及5%回收等旧限制：现有商品均开放买卖，唯一例外是黑市车辆配件继续Mode 3隐藏。
- 普通商品Min/Max价格按修改前的20%四舍五入为整数，正价最低1、原0保留。Exchange的4种货币面值保留，避免改变纸币/金条/比特币结算价值；所有商品、全局及9个交易区SellPricePercent=100。
- 30个黑市非车辆/配件分类按20%后百万四舍五入，最低100万。11辆CarPack按原含附件总价8/20/32/45百万，调整为2/4/6/9百万。
- Bitcoin-CarPack-Parts的72个专用配件Min/Max价格设0。Better_Cars的Bitcoin-CarPack-Parts/Batteries/Vehicle_Parts分类及glowplug覆盖保持Mode 3，共296个隐藏配件身份；11个车本体保持Mode 1。共享电池/水箱等仍使用普通市场20%价格，其4100附件费用从车体内部价格扣除，确保最终整车报价整百万。不可仅用车体内部字段判断整车报价。
- 唯一原库存0/0的mmg_gp_nvg_black改为1/1，4色Variants继承；其他库存、Stock、NPC、货币、附件及准入条件保持。
- 3个gpt-6.1-sol子代理并行分区处理及审核。当前178 Market、3745独立Item、5338 Variant、35 Trader、9 Zone、12366 Stock键、223活动JSON；10055商人-商品关系中9759为双向、296为黑市隐藏车辆配件。
- 新规则验证PASS：备份SHA256、JSON重复键、价格公式、引用可达性、权限、完整车辆总价、其他字段及原字节格式通过。115个独立Item与Variant同名关系是原有合法价格覆盖，沿用官方AddVariants语义。旧validate_active_market_v1.py的经济合同仍要求过去的限制，当前77项报错均为旧规则冲突，不能复跑旧写入工具恢复旧价格/权限；旧规则工具未修改。
- 确认保留的价差：5种弹盒新价1000，拆成散弹可回收2000/3000/4000；钉子盒200，70钉可回收1400。100%仅基础回收比例，损坏、数量、食物状态及动态库存仍影响实际交易金额。
- 修改217个配置文件：178 Market、29 Trader、9 TraderZone、1 MarketSettings；另同步本HANDOFF和Guide，共219个原有文件。未打包、未修改模组源码。部署、重启、RPT和实机交易尚未验证。
- 备份/精确文件清单/本次只读验证脚本：`workspace/backups/all-market-20pct-100sell-20261002-004556/`，见`original/`、`changed-files.txt`、`verification.json`与`verify_current.py`。
- 本次依据：现有活动JSON、冻结Expansion开源源码，以及2026-10-02读取的官方Market Categories/Trader Settings Wiki；保留原版本及层级。


### 2026-10-02 — 玩家ATM初始余额200万

- 按用户要求，活动`mpmissions/empty.deerisle/expansion/settings/MarketSettings.json`的`DefaultDepositMoney`由10000改为2000000；只改变此配置字段，其他市场规则、ATM上限、库存和玩家存档保持。
- 本地Expansion源码`ExpansionMarketModule::CreateATMData`使用此值初始化新账户；不会覆盖已有玩家银行余额。
- JSON解析、单字段深比较和原字节格式验证通过；配置与两份维护说明原文件已备份于`workspace/backups/atm-initial-2000000-20261002-010159/original/`。
- 尚未部署、重启或实机验证。后续同步MarketSettings.json、完整重启，并用新创建的银行账户检查200万初始余额。


### 2026-10-02 — 第二次调价与全市场声望逻辑统一（当前规则）

- 用户批准新方案，并明确所有商店购买和回收均不设声望门槛，保留声望积分及其他用途。本记录覆盖同日此前原20%价格/100%回收的临时规则。
- 价格基准为首次调价前`all-market-20pct-100sell-20261002-004556/original`，不是当前价格：普通商品原60%整数四舍五入；黑市非载具原60%百万四舍五入最低100万；11辆CarPack按原含附件整车价50%百万取整，最终为400/1000/1600/2300万。
- 黑市专用72件配件保持0价、296个车辆配件关系Mode3隐藏；共享电池水箱等普通价不清零，从车体价扣除12300附件费用保证完整整车百万整数。Exchange四币面值原样，所有Zone BuyPricePercent=100避免折扣兑换套利。ATM初始2000000原样。
- 按用途配置差异回收：一般服装/普通枪甲/普通车件20，已查378个A3-A6枪甲10，枪械附件与弹匣15，常规消耗/工具15，散弹与纸/建材5，鱼75、DF80、QPK废品40、医疗2.5/InediaT1为1.5、工作台5、普通容器10及原0例外。渔具原14项0保留，其他10；Safe3、MMG帐篷kit2、nailbox35、nail5。全局与9 Zone默认回收15，各商品显式值优先。
- QPK材料按转换预算进一步降到Bolts1.5%、MetalParts1.4%、WeaponParts1.8%，其余3项2%；唯一可有价拆解的免费altyn visor及生成绿色variant独立购价1000，回收0。其他两个免费Vulkan附件0价/0回收且现FormalV3无转换引用。
- 所有普通商品仍可买；5个黑市所有可见主商品Mode0仅购买、禁止回收，避免BTC不足一枚的支付余数损失。普通回收0商品同样Mode0禁止零收益交货。源码递归10055关系=7343双向+2416仅买+296隐藏车配件，9759可见。
- 声望根因是实际读`$mission:expansion/settings/HardlineSettings.json`，profiles副本不覆盖；旧任务版开启购买/出售稀有度门槛而profiles关闭，默认稀有度和显式高稀有度导致商品要求不同。现仅把实际任务版`UseItemRarityForMarketPurchase/Sell`改0，profiles原0不动；35Trader准入无门槛，RMS只有未匹配示例，不生效。保留UseReputation、死亡损失、ItemRarity映射、HUD与所有其他声望字段。
- 3个gpt-6.1-sol子代理并行独立审计。178分类3745独立项5338 Variant/8968去重身份结构、价格、回收、整车、权限、声望、备份SHA256及非目标字段/字节验证PASS。转换核验8964非兑换直接买卖、1230可报价拆解、20可报价弹盒和钉盒通过；149拆解、687制作、17弹盒仍缺价/数量语义，明确UNKNOWN，不把单步通过当成全模组闭环证明。
- 修改197配置：177 Market（178审核，Exchange未变）、9 Trader、9 Zone、MarketSettings及实际Hardline各1；另更新HANDOFF/Guide共199原有文件，新增只读`audit_conversion_caps_60pct_v1.py`工具。不修改模组源码、配方、存档；不打包。
- 当前备份及验证在`workspace/backups/market-60pct-recovery-reputation-20261002-233511/`：original、changed-files.txt、verification.json、conversion-audit.json、reputation-audit.json；验证脚本verify_current.py可直接运行。旧定价writer/旧强制低回收与黑市仅购买经济校验不得回写旧规则。
- 以上仅本地静态结果。下一步同步精确配置文件、完整重启，核RPT与普通/黑市/车辆交易，并以低声望新账户复核买卖无门槛。零价车件Mode3是UI隐藏，不能宣传为绝对服务器单件交易禁令；未确认外部技能返料脚本不能当作当前行为。

