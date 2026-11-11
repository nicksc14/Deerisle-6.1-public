# Azrael Fishing Mod
# FISH Config Guide

**Config path:** `$profile:\AzraelConfig\Fishing_Setting\Fish_Config.json`  
**Guide version:** `1.0`  

---

## About this config

**RU:**  
Этот конфиг содержит основные настройки для морской и пресноводной рыбы, их поведения в мини-игре, шансы появления и клева, подходящих снастей.

**EN:**  
This config contains main settings for sea and freshwater fish, their mini-game behavior, spawn and bite chances, and compatible gear.

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

# 1. ============ FISH CONFIG

### `cfg_AzraelFishList_SEA`
`array` 
### `cfg_AzraelFishList_POND`
`array` 

RU: Списки морской и пресноводной рыбы. Ваша рыба будет вылавливаться в море или в предах/реках/озерах в зависимости от того, в какой из этих списков вы ее пропишите.   
EN: Lists of sea and freshwater fish. Your fish will be caught in the sea or in ponds/rivers/lakes depending on which list you add it to.

---

### `FishClassname`
`classname`

RU: Класснейм рыбы, для которой применяются следующие параметры.   
EN: Fish classname to which the following parameters apply.

---

### `FishNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `IsActive`
`bool` · default: `1` · range: `0-1`

RU: Включить/выключить возможность ловить данную рыбу удочкой. ВНИМАНИЕ: не влияет на возможность поймать рыбу в ловушку, если она прописана в ней. 
EN: Enable/disable catching this fish with a fishing rod. WARNING: this does not affect the ability to catch this fish in a trap if it is listed there.

---

### `FishRarity`
`int` · default: `0` · range: `0–3`

RU: Редкость: количество звезд на экране мини-игры, когда вы поймали рыбу. Не влияет на геймплей. 
EN: Rarity: number of stars shown on the mini-game screen when you catch this fish. Does not affect gameplay.

---

### `ChanceFish`
`float` · default: -- · range: `0.0–1.0`

RU: Шанса появления рыбы. Попытка происходит один раз при забрасывании удочки. (В DLC RealFisher шанс устанавливается для каждого часа)
EN: Fish spawn chance. The attempt is made once when casting the rod. (In the RealFisher DLC the chance is set for every hour)

---

### `ChanceSignal`
`float` · default: -- · range: `0.0–1.0`

RU: Шанса клева рыбы. Попытка происходит каждый цикл (прокручивание колесика прогресса) один раз. (В DLC RealFisher шанс устанавливается для каждого часа)
EN: Fish bite chance. The attempt is made once every cycle (progress wheel rotation). (In the RealFisher DLC the chance is set for every hour)

---

### DLC RealFisher ### `DeepMin`
`float` · default: -- · range: `0.0–100.0`
### DLC RealFisher ### `DeepMax`
`float` · default: -- · range: `0.0–100.0`

RU: Мин. и макс. глубина, на которой можно поймать рыбу. Доступно только в DLC RealFisher.
EN: Min. and max. depth at which fish can be caught. Available only in the DLC RealFisher.

---

### DLC RealFisher ### `AddToBook`
`bool` · default: `1` · range: `0-1`

RU: Если включено, то рыба будет добавлена в книгу-справочник со всей информацией. Доступно только в DLC RealFisher.
EN: If enabled, the fish will be added to the reference book with all relevant information. Only available in the RealFisher DLC.

---

### `HookList`
`array string`

RU: Список крючков, которые позволяют ловить данную рыбу.
EN: List of hooks that allow this fish to be caught.

---

### `BaitList`
`array string`
format: `"classname|fish_chance_modifier|signal_chance_modifier"`
example: `"AP_fishing_bait_meat|1.35|1.20"`

RU: Список приманок, которые позволяют ловить данную рыбу. Так же указывается множитель шанса появления либо клева для данной рыбы. Это позволяет тонко настроить предпочтения каждой рыбы по приманкам. Важно: Empty - обозначает шансы для ловли без приманки (пустой крючок, блесна).
EN: List of baits that allow this fish to be caught. Also specifies the spawn or bite chance modifier for this fish. This allows fine-tuning each fish's bait preferences. Important: Empty defines chances for fishing without bait (empty hook, lure).

---

### `SignalDurationMin`
`float` · default: `1.0` · range: `0.5–5.0`
### `SignalDurationMax`
`float` · default: `2.0` · range: `0.5–5.0`

RU: Мин. и макс. длительность сигнала (всплеска воды), когда рыба поймалась схватила крючок, за это время вам необходимо успеть подсечь рыбу (отпустить ЛКМ), иначе рыба уйдет и к удочке/снастям применится модификатор Loss. Не рекомендуется ставить слишком низкие значение, это может сделать рыбалку слишком сложной. Значение в секундах.
EN: Min. and max. signal duration (water splash) when the fish bites the hook. During this time, you must hook the fish (release LMB), otherwise the fish will escape and the Loss modifier will be applied to the rod/gear. Very low values are not recommended, as they can make fishing too difficult. Value in seconds.

---

### `QualityMin`
`float` · default: `0.1` · range: `0.0–1.0`
### `QualityMax`
`float` · default: `1.0` · range: `0.0–1.0`

RU: Мин. и макс. "количество" рыбы. Влияет на вес и количество получаемого мяса при разделке. НЕ РЕКОМЕНДУЕТСЯ МЕНЯТЬ ЗНАЧЕНИЕ. 
EN: Min. and max. fish "quantity". Affects weight and the amount of meat received when cutting the fish. CHANGING THIS VALUE IS NOT RECOMMENDED.

---

### `RodFullLoadModifier`
`float` · default: `1.0` · range: `0.0–10.0`

RU: Множитель нагрузки на удочку и снасти (мини-игра), когда рыба находится в рамке захвата. Пример: при значении 2.0 рыба весом в 5 кг будет создавать нагрузку на удочку, будто она весит 10 кг. Повзоляет более детально настроить поведение рыбы.
EN: Load multiplier applied to the rod and gear (mini-game) when the fish is inside the catch frame. Example: with value 2.0, a 5 kg fish will load the rod as if it weighed 10 kg. Allows more detailed tuning of fish behavior.

---

### `RodFullLoadSpeedModifier`
`float` · default: `1.0` · range: `0.0–10.0`

RU: Множитель скорости увеличения нагрузки на удочку и снасти (мини-игра), когда рыба находится в рамке захвата. Увеличение значения усложняет вытягивание рыбы на перегрузе.
EN: Load increase speed multiplier for the rod and gear (mini-game) when the fish is inside the catch frame. Increasing this value makes pulling overloaded fish harder.

---

### `FrameSizeModifier`
`float` · default: `1.0` · range: `0.1–300.0`

RU: Множитель размера рамки захвата рыбы в мини-игре, так же зависит от глобальных настроек, удочки, снастей. Увеличение значения может значительно облегчить вытягивание рыбы.
EN: Catch frame size multiplier in the mini-game; also depends on global settings, rod, and gear. Increasing this value can make pulling fish much easier.

---

### `PullSpeedUpModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель скорости увеличения прогресса при вытягивании рыбы (мини-игра), так же зависит от глобальных настроек, удочки, снастей. Увеличение значения сделает вытягивание рыбы более быстрым. 
EN: Progress increase speed multiplier while pulling fish (mini-game); also depends on global settings, rod, and gear. Increasing this value makes pulling fish faster.

---

### `PullSpeedDownModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель скорости снижения прогресса вытягивания рыбы (мини-игра), так же зависит от глобальных настроек, удочки, снастей. Увеличение значения сделает вытягивание рыбы более сложным. 
EN: Progress decrease speed multiplier while pulling fish (mini-game); also depends on global settings, rod, and gear. Increasing this value makes pulling fish harder.

---

### `FishSpeedMinModifier`
`float` · default: `1.0` · range: `0.1–10.0`
### `FishSpeedMaxModifier`
`float` · default: `2.0` · range: `0.1–10.0`

RU: Минимальная и максимальная скорость перемещения иконки рыбы в мини-игре, так же зависит от глобальных настроек. Увеличение значения усложняет вытягивание рыбы.
EN: Minimum and maximum movement speed of the fish icon in the mini-game; also depends on global settings. Increasing this value makes pulling fish harder.

---

### `FishPauseMinModifier`
`float` · default: `1.0` · range: `0.1–10.0`
### `FishPauseMaxModifier`
`float` · default: `2.0` · range: `0.1–10.0`

RU: Минимальная и максимальная задержка при перемещении иконки рыбы в мини-игре, так же зависит от настроек конкретной рыбы в Fish_Config.json. Увеличение значения облегчает вытягивание рыбы. Значение в секундах.
EN: Minimum and maximum delay between fish icon movements in the mini-game; also depends on the specific fish settings in Fish_Config.json. Increasing this value makes pulling fish easier. Value in seconds.

---

### `FishPathMinModifier`
`float` · default: `0.2` · range: `0.01–1.0`
### `FishPathMaxModifier`
`float` · default: `0.4` · range: `0.01–1.0`

RU: Базовая минимальная и максимальная длина "пути" перемещения иконки рыбы в мини-игре, так же зависит от настроек конкретной рыбы в Fish_Config.json. Увеличение значения усложняет вытягивание рыбы.
EN: Base minimum and maximum movement "path" length of the fish icon in the mini-game; also depends on the specific fish settings in Fish_Config.json. Increasing this value makes pulling fish harder.

