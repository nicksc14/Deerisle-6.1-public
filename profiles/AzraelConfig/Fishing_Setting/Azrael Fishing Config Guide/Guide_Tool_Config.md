# Azrael Fishing Mod
# TOOL Config Guide

**Config path:** `$profile:\AzraelConfig\Fishing_Setting\Tools_Config.json`  
**Guide version:** `1.0`  

---

## About this config

**RU:**  
Этот конфиг содержит настройки снаряжения: удочки, катушки, лески, крючки, приманки.

**EN:**  
This config contains equipment settings: rods, reels, lines, hooks, and baits.

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

# 1. ============ TOOLS CONFIG


# 1.0 ----- Basic parameters

### `ProgressSpeedUpModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель скорости увеличения прогресса при вытягивании рыбы (мини-игра), так же зависит от глобальных настроек, рыбы, других снастей. Увеличение значения сделает вытягивание рыбы более быстрым. 
EN: Progress increase speed multiplier while pulling fish (mini-game); also depends on global settings, fish, and other gear. Increasing this value makes pulling fish faster.

---

### `ProgressSpeedDownModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель скорости снижения прогресса вытягивания рыбы (мини-игра), так же зависит от глобальных настроек, рыбы, других снастей. Увеличение значения сделает вытягивание рыбы более сложным. 
EN: Progress decrease speed multiplier while pulling fish (mini-game); also depends on global settings, fish, and other gear. Increasing this value makes pulling fish harder.

---

### `ReelSpeedModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель скорости вращения катушки (движения рамки захвата в мини-игре), так же зависит от глобальных настроек, рыбы, других снастей. Увеличение значения может облегчить захват рыбы в мини-игре.
EN: Reel rotation speed multiplier (catch frame movement in the mini-game); also depends on global settings, fish, and other gear. Increasing this value can make catching fish in the mini-game easier.

---

### `LoadWeightMax`
`float` 

RU: Максимальная нагрузка. При превышении нагрузки может сломаться. Значение в килограммах.
EN: Maximum load. If the load is exceeded, the item may break. Value in kilograms.

---

### `LoadSpeedModifier`
`float` 

RU: Множитель скорости увеличения нагрузки (мини-игра), когда рыба находится в рамке захвата. Увеличение значения усложняет вытягивание рыбы на перегрузе.
EN: Load increase speed multiplier (mini-game) when the fish is inside the catch frame. Increasing this value makes pulling overloaded fish harder.

---

### `DamageLoss`
`float` 

RU: Урон инструменту, в случае если рыба ушла: когда вы отменили вытягивание во время безопасного таймера, или когда упустили сигнал рыбы.
EN: Damage to the tool when the fish is lost: when you cancel pulling during the safe timer, or when you miss the fish signal.

---

### `DamageFailure`
`float` 

RU: Урон инструменту, в случае если рыба сорвалась: когда процесс вытягивания достиг нуля, когда вы отменили вытягивание (мини-игру) после завершение безопасного таймера.
EN: Damage to the tool when the fish escapes: when the pulling progress reaches zero, or when you cancel pulling (mini-game) after the safe timer has ended.

---

### `DamageSuccess`
`float` 

RU: Урон инструменту, когда вы успешно поймали рыбу.
EN: Damage to the tool when you successfully catch a fish.

---

### `FrameSizeModifier`
`float` · default: `1.0` · range: `0.1–10.0`

RU: Множитель размера рамки захвата рыбы в мини-игре, так же зависит от глобальных настроек, удочки, снастей. Увеличение значения может значительно облегчить вытягивание рыбы.
EN: Catch frame size multiplier in the mini-game; also depends on global settings, rod, and gear. Increasing this value can make pulling fish much easier.




# 1.1 ----- Rods

### `cfg_AzraelRodList`
`array` 

RU: Список с удочками и их параметрами.   
EN: List of fishing rods and their parameters.

---

### `RodClassname`
`classname`

RU: Класснейм удочки.   
EN: Rod classname.

---

### `RodNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `RequiredReel`
`bool` · default: `1` · range: `0-1`

RU: Включить/выключить необходимость рыболовной катушки для ловли. В случае отсутствия катушки будут использоваться параметры NoReel из cfg_AzraelReelList. НЕ РЕКОМЕНДУЕТСЯ МЕНЯТЬ ЗНАЧЕНИЕ ПО УМОЛЧАНИЮ.
EN: Enable/disable the requirement for a fishing reel. If there is no reel, the NoReel parameters from cfg_AzraelReelList will be used. CHANGING THE DEFAULT VALUE IS NOT RECOMMENDED.

---

### `ChanceModifier`
`float` · default: `1.0`

RU: Множитель, влияющий на шанс появления рыбы.
EN: Multiplier that affects fish spawn chance.




# 1.2 ----- Reels

### `cfg_AzraelReelList`
`array` 

RU: Список с рыболовными катушками и их параметрами.   
EN: List of fishing reels and their parameters.

---

### `ReelClassname`
`classname`

RU: Класснейм рыболовной катушки. "NoReel" - используется для загрузки параметров для удочки, для которой отключена необходимость катушки.  
EN: Fishing reel classname. "NoReel" is used to load parameters for a rod that does not require a reel.

---

### `ReelNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### Basic Parameters
RU: Остальные параметры описаны в разделе 1.0. 
EN: The remaining parameters are described in section 1.0.




# 1.3 ----- Lines

### `cfg_AzraelLineList`
`array` 

RU: Список с рыболовными лесками и их параметрами.   
EN: List of fishing lines and their parameters.

---

### `LineClassname`
`classname`

RU: Класснейм рыболовной лески.
EN: Fishing line classname.

---

### `LineNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `DescreaseChanceFailure`
`float` · default: `1.0` · range: `0.0-1.0`

RU: Шанс порвать леску, когда рыба сорвалась (Failure). Если леска порвалась - крючок тоже исчезает.
EN: Chance for the line to break when the fish escapes (Failure). If the line breaks, the hook also disappears.

---

### Basic Parameters
RU: Остальные параметры описаны в разделе 1.0. 
EN: The remaining parameters are described in section 1.0.




# 1.4 ----- Hook

### `cfg_AzraelHookList`
`array` 

RU: Список с рыболовными крючками и их параметрами.   
EN: List of fishing hooks and their parameters.

---

### `HookClassname`
`classname`

RU: Класснейм рыболовного крючка.
EN: Fishing hook classname.

---

### `HookNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `JunkChance`
`float` · default: `0.5` · range: `0.0-1.0`

RU: Шанс, что вместо рыбы будет попытка выловить мусор/предметы из конфига Junk_Config.json.
EN: Chance that, instead of fish, there will be an attempt to catch junk/items from Junk_Config.json.

---

### `ChanceModifierFish`
`float` · default: `1.0`
### `ChanceModifierJunk`
`float` · default: `1.0`

RU: Множители, влияющие на шанс появления рыбы и мусора.
EN: Multipliers that affect fish and junk spawn chances.

---

### Basic Parameters
RU: Остальные параметры описаны в разделе 1.0. 
EN: The remaining parameters are described in section 1.0.



# 1.5 ----- Bait

### `cfg_AzraelBaitList`
`array` 

RU: Список с рыболовными приманками/наживками и их параметрами.   
EN: List of fishing baits/lures and their parameters.

---

### `BaitClassname`
`classname`

RU: Класснейм рыболовной наживки.
EN: Fishing bait classname.

---

### `BaitNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `ChanceModifier`
`float` · default: `1.0`

RU: Множитель, влияющий на шанс появления рыбы.
EN: Multiplier that affects fish spawn chance.

---

### `ChanceSignalModifier`
`float` · default: `1.0`

RU: Множитель, влияющий на шанс клева (сигнала) рыбы.
EN: Multiplier that affects fish bite (signal) chance.

---

### `LossChanceSuccess`
`float` · default: `1.0` · range: `0.0-1.0`

RU: Шанс удаления приманки, когда рыба поймана.
EN: Chance to remove the bait when the fish is caught.

---

### `LossChanceFailure`
`float` · default: `1.0` · range: `0.0-1.0`

RU: Шанс удаления приманки, в случае если рыба сорвалась.
EN: Chance to remove the bait if the fish escapes.

---

### `LossChanceSignalMiss`
`float` · default: `0.7` · range: `0.0-1.0`

RU: Шанс удаления приманки, когда ушла, после того как вы упустили сигнал или завершили мини-игру до завершение безопасного таймера.
EN: Chance to remove the bait when the fish gets away after you miss the signal or end the mini-game before the safe timer ends.

---

### Basic Parameters
RU: Остальные параметры описаны в разделе 1.0. 
EN: The remaining parameters are described in section 1.0.

---

