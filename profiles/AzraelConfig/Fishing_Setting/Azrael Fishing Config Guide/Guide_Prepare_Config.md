# Azrael Fishing Mod
# PREPARE Config Guide

**Config path:** `$profile:\AzraelConfig\Fishing_Setting\Prepare_Config.json`  
**Guide version:** `1.0`  

---

## About this config

**RU:**  
Этот конфиг содержит основные настройки для разделки рыбы и инструментов.

**EN:**  
This config contains the main settings for fish preparation and tools.

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

# 1. ============ PREPARE CONFIG

### `cfg_AzraelPrepareKnifeList`
`array` 

RU: Список инструментов, с помощью которых возможна разделка рыбы, а так же их параметры.   
EN: List of tools that can be used to prepare fish, as well as their parameters.

---

### `KnifeClassname`
`classname`

RU: Класснейм ножа, который доступен для разделки.   
EN: Classname of the knife that can be used for preparation.

---

### `PrepareTimeModifier`
`float` · default: 1.0

RU: Множитель времени разделки. Чем выше значение - тем ДОЛЬШЕ этот нож будет разделывать рыбу. 
EN: Preparation time multiplier. The higher the value, the LONGER this knife will take to prepare the fish.

---

### `ToolDamageModifier`
`float` · default: 1.0

RU: Урон инструменту после разделки. 
EN: Damage applied to the tool after preparation.

---


### `cfg_AzraelPrepareList`
`array` 

RU: Список рыбы и параметров разделки для нее.   
EN: List of fish and their preparation parameters.

---

### `FishClassname`
`classname`

RU: Класснейм рыбы, для которой применятся параметры.   
EN: Classname of the fish to which these parameters are applied.

---

### `PrepareNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `PrepareTimeSec`
`float`

RU: Время, необходимое для разделки этой рыбы по умолчанию. 
EN: Default time required to prepare this fish.

---

### `PrepareToolDamage`
`float` 

RU: Урон инструменту после разделки для этой рыбы по умолчанию. 
EN: Default tool damage after preparing this fish.

---


### `cfg_PrepareItemsList`
`array` 

RU: Список мяса, костей, других предметов, получаемых при разделке рыбы.   
EN: List of meat, bones, and other items received when preparing fish.

---

### `ItemClassname`
`classname`

RU: Класснейм предмета/мяса/костей.   
EN: Classname of the item/meat/bones.

---

### `ItemChance`
`float` · default: -- · range: `0.0–1.0`

RU: Шанс получения предмета при разделке. 
EN: Chance to receive this item when preparing fish.

---

### `SpawnAttemptMin`
`int` · default: `1` · range: `1–20`
### `SpawnAttemptMax`
`int` · default: `1` · range: `1–20`

RU: Количество попыток заспавнить данные предмет (например при мин. значении 1, макс. значении 3, вы получить от 1 до 3 предметов с этими настройками). 
EN: Number of attempts to spawn this item (for example, with min. value 1 and max. value 3, you will receive from 1 to 3 items with these settings).

---

### `InsertSalmonella`
`bool` · default: `1` · range: `0-1`

RU: Получит ли мясо заражение сальмонеллой после разделки. 
EN: Whether the meat will receive salmonella contamination after preparation.

---

### `BloodyHands`
`bool` · default: `1` · range: `0-1`

RU: Может ли получение этого предмета испачкать руки игрока в крови. 
EN: Whether receiving this item can make the player's hands bloody.

---

### `QuantityInPercent`
`bool` · default: `1` · range: `0-1`

RU: Учитывать ли значение QuantityMin и QuantityMax как процентное в формате где 0.0 - 0%, а 1.0 - 100%. Если отключено, то QuantityMin и QuantityMax должны быть указаны как целые точные значения quantity предмета.
EN: Whether QuantityMin and QuantityMax should be treated as percentage values, where 0.0 = 0% and 1.0 = 100%. If disabled, QuantityMin and QuantityMax must be set as exact whole quantity values for the item.

---

### `QuantityMin`
`float` · default: `-2.0`
### `QuantityMax`
`float` · default: `-2.0`

RU: Мин. и макс. количество предмета. Установите -2.0 для автоматического расчета количества мяса в зависимости от размера и веса рыбы. 
EN: Minimum and maximum item quantity. Set to -2.0 to automatically calculate the meat quantity based on fish size and weight.

---

### `HealthMin`
`float` · default: `1.0` · range: `0.0–1.0`
### `HealthMax`
`float` · default: `1.0` · range: `0.0–1.0`

RU: Мин. и макс. состояние здоровья предмета. 
EN: Minimum and maximum item health condition.

