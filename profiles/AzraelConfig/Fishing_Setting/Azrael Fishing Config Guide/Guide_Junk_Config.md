# Azrael Fishing Mod
# JUNK Config Guide

**Config path:** `$profile:\AzraelConfig\Fishing_Setting\Junk_Config.json`  
**Guide version:** `1.0`  

---

## About this config

**RU:**  
Этот конфиг содержит основные настройки для мусора/предметов, которые вы так же можете вытащить из воды, их поведения в мини-игре, шансы появления и сигнала, количества и состояния.

**EN:**  
This config contains main settings for junk/items that can also be pulled out of the water, their mini-game behavior, spawn and signal chances, quantity, and condition.

---

## Before editing

- Always make a backup before editing.
- Do not delete parameter names.
- Do not remove commas.
- Do not change the JSON structure unless you know what you are doing.
- Use a dot for decimal values: `1.5`, not `1,5`.
- Bool-style values use `0 / 1`.
- If the server does not start after editing, check the last changed parameter first.

---

## Value types

| Type | Meaning | Example |
|---|---|---|
| `int` 		| Whole number | `10` |
| `float` 		| Decimal number | `2.5` |
| `bool` 		| Disabled / enabled value | `0 / 1` |
| `string` 		| Text value in quotes | `"any text 123"` |
| `array` 		| List of values or objects | `[ ... ]` |
| `classname` 	| DayZ classname | `"AP_FishingRod_Pro"` |

---

# 1. ============ JUNK CONFIG

### `cfg_AzraelJunkList`
`array` 

RU: Список мусора/предметов, который может быть пойман в зависимости от настроек ваших снастей.   
EN: List of junk/items that can be caught depending on your gear settings.

---

### `JunkClassname`
`classname`

RU: Класснейм предмета, для которого применяются следующие параметры.   
EN: Item classname to which the following parameters apply.

---

### `JunkNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `IsActive`
`bool` · default: `1` · range: `0-1`

RU: Включить/выключить возможность ловить данный предмет удочкой.
EN: Enable/disable catching this item with a fishing rod.

---

### `JunkRarity`
`int` · default: `0` · range: `0–3`

RU: Редкость: количество звезд на экране мини-игры, когда вы поймали этот предмет. Не влияет на геймплей. 
EN: Rarity: number of stars shown on the mini-game screen when you catch this item. Does not affect gameplay.

---

### `ChanceSea`
`float` · default: -- · range: `0.0–1.0`

RU: Шанса появления появления предмета в море.
EN: Item spawn chance in the sea.

---

### `ChancePond`
`float` · default: -- · range: `0.0–1.0`

RU: Шанса появления появления предмета в пресной воде.
EN: Item spawn chance in freshwater.

---

### `SignalChance`
`float` · default: -- · range: `0.0–1.0`

RU: Шанса появления сигнала (всплеска). Попытка происходит каждый цикл (прокручивание колесика прогресса) один раз.
EN: Signal (splash) chance. The attempt is made once every cycle (progress wheel rotation).

---

### DLC RealFisher ### `DeepMin`
`float` · default: -- · range: `0.0–100.0`
### DLC RealFisher ### `DeepMax`
`float` · default: -- · range: `0.0–100.0`

RU: Мин. и макс. глубина, на которой можно поймать предмет. Доступно только в DLC RealFisher.
EN: Min. and max. depth at which item can be caught. Available only in the DLC RealFisher.

---

### `SignalDurationMin`
`float` · default: `2.0` · range: `0.5–5.0`
### `SignalDurationMax`
`float` · default: `4.0` · range: `0.5–5.0`

RU: Мин. и макс. длительность сигнала (всплеска воды), когда предмет зацепился за крючок, за это время вам необходимо успеть подсечь его (отпустить ЛКМ), иначе предмет потеряется и к удочке/снастям применится модификатор Loss. Не рекомендуется ставить слишком низкие значение, это может сделать процесс слишком сложным. Значение в секундах.
EN: Min. and max. signal duration (water splash) when the item hooks onto the hook. During this time, you must hook it (release LMB), otherwise the item will be lost and the Loss modifier will be applied to the rod/gear. Very low values are not recommended, as they can make the process too difficult. Value in seconds.

---

### `QuantityInPercent`
`bool` · default: `1` · range: `0-1`

RU: Указывать ли quantity в процентах. Если выключено, то нужно указывать Quantiy в целых значениях.
EN: Whether quantity should be specified as a percentage. If disabled, Quantity must be specified as whole values.

---

### `QuantiyMin`
`float` · default: `0.1` · range: `0.0–1.0`
### `QuantiyMax`
`float` · default: `1.0` · range: `0.0–1.0`

RU: Мин. и макс. "количество" (quantity) предмета в стаке.
EN: Min. and max. item "quantity" in the stack.

---

### `HealthMin`
`float` · default: `0.1` · range: `0.0–1.0`
### `HealthMax`
`float` · default: `0.4` · range: `0.0–1.0`

RU: Мин. и макс. здоровье предмета в процентах.
EN: Min. and max. item health percentage.

---

### `DurabilityMin`
### `DurabilityMax`

RU: Параметр не используется в данный момент.
EN: This parameter is not currently used.

---

### `RodFullLoadModifier`
`float` · default: `1.0` · range: `0.0–10.0`

RU: Множитель нагрузки на удочку и снасти (мини-игра), когда предмет находится в рамке захвата. Пример: при значении 2.0 предмет весом в 5 кг будет создавать нагрузку на удочку, будто он весит 10 кг.
EN: Load multiplier applied to the rod and gear (mini-game) when the item is inside the catch frame. Example: with value 2.0, an item weighing 5 kg will load the rod as if it weighed 10 kg.

---

### `RodFullLoadSpeedModifier`
`float` · default: `1.0` · range: `0.0–10.0`

RU: Множитель скорости увеличения нагрузки на удочку и снасти (мини-игра), когда предмет находится в рамке захвата. Увеличение значения усложняет вытягивание предмета на перегрузе.
EN: Load increase speed multiplier for the rod and gear (mini-game) when the item is inside the catch frame. Increasing this value makes pulling overloaded items harder.

---

### `PullSpeedUpModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель скорости увеличения прогресса при вытягивании предмета (мини-игра), так же зависит от глобальных настроек, удочки, снастей. Увеличение значения сделает вытягивание предмета более быстрым. 
EN: Progress increase speed multiplier while pulling an item (mini-game); also depends on global settings, rod, and gear. Increasing this value makes pulling the item faster.

---

### `PullSpeedDownModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель скорости снижения прогресса вытягивания предмета (мини-игра), так же зависит от глобальных настроек, удочки, снастей. Увеличение значения сделает вытягивание предмета более сложным. 
EN: Progress decrease speed multiplier while pulling an item (mini-game); also depends on global settings, rod, and gear. Increasing this value makes pulling the item harder.

---

### `FrameSizeModifier`
`float` · default: `1.0` · range: `0.1–300.0`

RU: Множитель размера рамки захвата предмета в мини-игре, так же зависит от глобальных настроек, удочки, снастей. Увеличение значения может значительно облегчить вытягивание предмета.
EN: Catch frame size multiplier for the item in the mini-game; also depends on global settings, rod, and gear. Increasing this value can make pulling the item much easier.
