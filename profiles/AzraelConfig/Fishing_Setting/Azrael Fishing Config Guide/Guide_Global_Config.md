# Azrael Fishing Mod
# GLOBAL Config Guide

**Config path:** `$profile:\AzraelConfig\Fishing_Setting\Global_Config.json`  
**Guide version:** `1.0`  

---

## About this config

**RU:**  
Этот конфиг содержит глобальные и основные настройки мода. Он позволяет менять общую сложность рыбалки, мини-игры, поломки снастей, ловли мусора и других механик без глубокого редактирования отдельных рыб, приманок и зон.

**EN:**  
This config contains global and basic mod settings. It allows you to adjust the overall difficulty of fishing, the mini-game, equipment breaking, trash catching, and other mechanics without deeply editing individual fish, baits, or zones.

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

# 1. ============ GLOBAL CONFIG

### `EnableDebugPrint`
`bool` · default: `0` · range: `0-1`

RU: Включить/выключить вывод технической информации в лог. НЕ РЕКОМЕНДУЕТСЯ МЕНЯТЬ ЗНАЧЕНИЕ.   
EN: Enable/disable technical information output to the log. CHANGING THIS VALUE IS NOT RECOMMENDED.

---

### `CanRodOverload`
`bool` · default: `1` · range: `0-1`

RU: Включить/выключить механику перегрузки и максимального веса для удочки и снастей.  
EN: Enable/disable overload and maximum weight mechanics for the rod and gear.

---

### `DisableCraftVanillaRodImprovised`
`bool` · default: `1` · range: `0-1`

RU: Включить/выключить крафт ванильной самодельной удочки. ВНИМАНИЕ: если параметр выключен, то отключается крафт НОВОЙ самодельной удочки и наоборот. НЕ РЕКОМЕНДУЕТСЯ МЕНЯТЬ ЗНАЧЕНИЕ.   
EN: Enable/disable crafting of the vanilla improvised fishing rod. WARNING: if this parameter is disabled, crafting of the NEW improvised rod is disabled, and vice versa. CHANGING THIS VALUE IS NOT RECOMMENDED.

---

### `FindNewFishIfChanceZero`
`bool` · default: `1` · range: `0-1`

RU: Включить/выключить повторный поиск рыбы, если предыдущий поиск не дал результатов. НЕ РЕКОМЕНДУЕТСЯ МЕНЯТЬ ЗНАЧЕНИЕ. 
EN: Enable/disable searching for a new fish if the previous search found nothing. CHANGING THIS VALUE IS NOT RECOMMENDED.

---

### `FindNewFIshIfChanceZeroCycleCount`
`int` · default: `3` · range: `1–20`

RU: Количество "холостых" циклов перед новым поиском рыбы при включенном параметре FindNewFishIfChanceZero. Увеличение значения может сделать рыбалку более долгой при низком клеве. 
EN: Number of "empty" cycles before searching for a new fish when FindNewFishIfChanceZero is enabled. Increasing this value can make fishing take longer when bite activity is low.

---

### `FindNewFIshIfChanceZeroCycleCount`
`int` · default: `3` · range: `1–20`

RU: Количество "холостых" циклов перед новым поиском рыбы при включенном параметре FindNewFishIfChanceZero. Увеличение значения может сделать рыбалку более долгой при низком клеве. 
EN: Number of "empty" cycles before searching for a new fish when FindNewFishIfChanceZero is enabled. Increasing this value can make fishing take longer when bite activity is low.

---

# 2. ============ DEFAULT BASE PARAMETERS

### `Default_CatchProgressSpeedUp`
`float` · default: `2.0` · range: `0.1–10.0`

RU: Базовая скорость увеличения прогресса при вытягивании рыбы (мини-игра), так же зависит от настроек рыбы, удочки, снастей. Увеличение значения сделает вытягивание рыбы более быстрым. 
EN: Base progress increase speed while pulling fish (mini-game); also depends on fish, rod, and gear settings. Increasing this value makes pulling fish faster.

---

### `Default_CatchProgressSpeedDown`
`float` · default: `1.5` · range: `0.1–10.0`

RU: Базовая скорость потери прогресса вытягивания рыбы (мини-игра), так же зависит от настроек рыбы, удочки, снастей. Увеличение значения сделает вытягивание рыбы более сложным. 
EN: Base progress loss speed while pulling fish (mini-game); also depends on fish, rod, and gear settings. Increasing this value makes pulling fish harder.

---

### `Default_PullReelSpeed`
`float` · default: `2.0` · range: `0.1–10.0`

RU: Базовая скорость вращения катушки (движения рамки захвата в мини-игре), так же зависит от настроек рыбы, удочки, снастей. Увеличение значения может облегчить захват рыбы в мини-игре, но нарушить баланс. Рекомендуется менять выборочно для определенных снастей/удочек/рыбы в соответствующих конфигах. 
EN: Base reel rotation speed (catch frame movement in the mini-game); also depends on fish, rod, and gear settings. Increasing this value can make catching fish in the mini-game easier, but may break balance. It is recommended to change it selectively for specific gear/rods/fish in the corresponding configs.

---

### `Default_GlobalFishChanceModifier`
`float` · default: `1.0` · range: `0.1–2.0`

RU: Глобальный множитель шанса появления для всех рыб, так же зависит от настроек конкретной рыбы в Fish_Config.json. Увеличение значения облегчает рыбалку. Не рекомендуется значительных изменений, может нарушить баланс. 
EN: Global fish spawn chance multiplier for all fish; also depends on the specific fish settings in Fish_Config.json. Increasing this value makes fishing easier. Major changes are not recommended, as they may break balance.

---

### `Default_GlobalSignalChanceModifier`
`float` · default: `1.0` · range: `0.1–2.0`

RU: Глобальный множитель шанса клева для всех рыб, так же зависит от настроек конкретной рыбы в Fish_Config.json. Увеличение значения облегчает и ускоряет рыбалку. Не рекомендуется значительных изменений, может нарушить баланс. 
EN: Global bite chance multiplier for all fish; also depends on the specific fish settings in Fish_Config.json. Increasing this value makes fishing easier and faster. Major changes are not recommended, as they may break balance.

---

### `Default_FishSpeedMin`
`float` · default: `1.0` · range: `0.1–10.0`
### `Default_FishSpeedMax`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Глобальный множитель минимальной и максимальной скорости перемещения иконки рыбы в мини-игре, так же зависит от настроек конкретной рыбы в Fish_Config.json. Уменьшение значения облегчает вытягивание рыбы.
EN: Global multiplier for the minimum and maximum movement speed of the fish icon in the mini-game; also depends on the specific fish settings in Fish_Config.json. Lowering this value makes pulling fish easier.

---

### `Default_FishPauseMin`
`float` · default: `1.0` · range: `0.1–10.0`
### `Default_FishPauseMax`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Глобальный множитель минимальной и максимальной задержки между перемещениями иконки рыбы в мини-игре, так же зависит от настроек конкретной рыбы в Fish_Config.json. Уменьшение значения облегчает вытягивание рыбы. Значение в секундах.
EN: Global multiplier for the minimum and maximum delay between fish icon movements in the mini-game; also depends on the specific fish settings in Fish_Config.json. Lowering this value makes pulling fish easier. Value in seconds.

---

### `Default_FishPathMin`
`float` · default: `1.0` · range: `0.01–1.0`
### `Default_FishPathMax`
`float` · default: `1.0` · range: `0.01–1.0`

RU: Глобальный множитель минимальной и максимальной длины "пути" перемещения иконки рыбы в мини-игре, так же зависит от настроек конкретной рыбы в Fish_Config.json. Уменьшение значения облегчает вытягивание рыбы.
EN: Global multiplier for the minimum and maximum movement "path" length of the fish icon in the mini-game; also depends on the specific fish settings in Fish_Config.json. Lowering this value makes pulling fish easier.

---

### `Default_FishFilletQualityMin`
`float` · default: `0.4` · range: `0.01–1.0`
### `Default_FishFilletQualityMax`
`float` · default: `1.0` · range: `0.01–1.0`

RU: Минимальное и максимальное ограничение количества филе для каждого куска при разделке при минимальном и максимальном размере рыбы. НЕ РЕКОМЕНДУЕТСЯ МЕНЯТЬ ЗНАЧЕНИЕ.   
EN: Minimum and maximum fillet quantity limit for each piece when cutting fish of minimum and maximum size. CHANGING THIS VALUE IS NOT RECOMMENDED.

---

### `Default_LineDescreaseFailureMin`
`float` · default: `10.0` · range: `0.1–100.0`
### `Default_LineDescreaseFailureMax`
`float` · default: `20.0` · range: `0.1–100.0`

RU: Минимальное и максимальное значение, на которое уменьшается количество лески, когда она порвалась (перегруз). 
EN: Minimum and maximum amount by which the line quantity is decreased when it breaks (overload).

---

### `Default_RodFullLoadSpeed`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Базовый множитель скорости увеличения нагрузки на удочку и снасти при перегрузе (мини-игра), когда рыба находится В рамке захвата.
EN: Base multiplier for load increase speed on the rod and gear during overload (mini-game), when the fish is INSIDE the catch frame.

---

### `Default_RodFullUnloadSpeed`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Базовый множитель скорости уменьшения нагрузки на удочку и снасти при перегрузе (мини-игра), когда рыба находится ВНЕ рамки захвата.
EN: Base multiplier for load decrease speed on the rod and gear during overload (mini-game), when the fish is OUTSIDE the catch frame.

---

### `Default_CatchFrameSize`
`float` · default: `110.0` · range: `30.0–300.0`

RU: Базовый размер рамки захвата рыбы в мини-игре, так же зависит от настроек рыбы, удочки, снастей. Увеличение значения может значительно облегчить вытягивание рыбы.
EN: Base catch frame size in the mini-game; also depends on fish, rod, and gear settings. Increasing this value can make pulling fish much easier.

---

### `Default_SafeFishReleaseTime`
`float` · default: `5.0` · range: `0.0–100.0`

RU: Время, позволяющее вам завершить мини-игру с минимальными потерями (если вы поняли, что не сможете вытянуть попавшуюся рыбу), к снастям применятся модификаторы Loss. По окончанию времени прерывание рыбалки засчитывается как сорвавшаяся рыба, к снастям применяются модификаторы Failure. В интерфейсе: тонкая голубая полоска-таймер. Увеличьте значение для упрощения рыбалки. Значение в секундах.
EN: Time that allows you to end the mini-game with minimal losses (if you realize you cannot pull the hooked fish). Loss modifiers will be applied to the gear. After this time ends, interrupting fishing counts as a failed fish escape, and Failure modifiers are applied to the gear. In the UI: thin blue timer bar. Increase this value to make fishing easier. Value in seconds.

---

### `Default_FishingMaxTime`
`float` · default: `20.0` · range: `5.0–500.0`

RU: Максимальное время для процесса вытягивания рыбы в мини-игре. Таймер включается после окончания таймера Default_SafeFishReleaseTime. По окончанию таймера рыба сорвется, к снастям применяются модификаторы Failure. В интерфейсе: тонкая красная полоска-таймер, появится после окончания таймера Default_SafeFishReleaseTime. Увеличьте значение для упрощения рыбалки. Значение в секундах.
EN: Maximum time for the fish pulling process in the mini-game. The timer starts after Default_SafeFishReleaseTime ends. When the timer expires, the fish escapes and Failure modifiers are applied to the gear. In the UI: thin red timer bar, appears after Default_SafeFishReleaseTime ends. Increase this value to make fishing easier. Value in seconds.

---

### `Default_JunkSpeedMinModifier`
`float` · default: `1.0` · range: `0.1–10.0`
### `Default_JunkSpeedMaxModifier`
`float` · default: `2.0` · range: `0.1–10.0`

RU: Базовая минимальная и максимальная скорость перемещения иконки предмета (мусора) в мини-игре, так же зависит от настроек конкретного предмета в Junk_Config.json. Увеличение значения усложняет вытягивание предмета.
EN: Base minimum and maximum movement speed of the item (junk) icon in the mini-game; also depends on the specific item settings in Junk_Config.json. Increasing this value makes pulling the item harder.

---

### `Default_JunkPauseMinModifier`
`float` · default: `1.0` · range: `0.1–10.0`
### `Default_JunkPauseMaxModifier`
`float` · default: `2.0` · range: `0.1–10.0`

RU: Базовая минимальная и максимальная задержка при перемещении иконки предмета (мусора) в мини-игре, так же зависит от настроек конкретного предмета в Junk_Config.json. Увеличение значения облегчает вытягивание предмета. Значение в секундах.
EN: Base minimum and maximum delay between item (junk) icon movements in the mini-game; also depends on the specific item settings in Junk_Config.json. Increasing this value makes pulling the item easier. Value in seconds.

---

### `Default_JunkPathMinModifier`
`float` · default: `0.2` · range: `0.01–1.0`
### `Default_JunkPathMaxModifier`
`float` · default: `0.4` · range: `0.01–1.0`

RU: Базовая минимальная и максимальная длина "пути" перемещения иконки предмета (мусора) в мини-игре, так же зависит от настроек конкретного предмета в Junk_Config.json. Увеличение значения усложняет вытягивание предмета.
EN: Base minimum and maximum movement "path" length of the item (junk) icon in the mini-game; also depends on the specific item settings in Junk_Config.json. Increasing this value makes pulling the item harder.

---
