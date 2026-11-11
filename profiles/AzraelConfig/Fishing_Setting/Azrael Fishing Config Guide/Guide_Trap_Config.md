# Azrael Fishing Mod
# TRAP Config Guide

**Config path:** `$profile:\AzraelConfig\Fishing_Setting\Trap_Config.json`  
**Guide version:** `1.0`  

---

## About this config

**RU:**  
Этот конфиг содержит настройки ловушек: сеть и ловушка из бутылки. Настраивается список вылавливаемой рыбы и другие параметры.

**EN:**  
This config contains trap settings: the net and the bottle trap. It configures the list of catchable fish and other parameters.

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

# 1. ============ TRAP CONFIG

### `cfg_AzraelTrapList`
`array` 

RU: Список ловушек.   
EN: List of traps.

---

### `TrapClassname`
`classname`

RU: Класснейм ловушки, для которой применяются параметры.   
EN: Trap classname to which the parameters apply.

---

### `TrapNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `ChanceSea`
`float` · default: `0.5` · range: `0.0–1.0`
### `ChancePond`
`float` · default: `0.5` · range: `0.0–1.0`

RU: Вероятность попытки поймать рыбу в зависимости от типа воды.
EN: Chance to attempt catching fish depending on water type.

---

### `ChanceBaitLoss`
`float` · default: `0.01` · range: `0.0–1.0`

RU: Вероятность потери приманки при попытке поймать рыбу.
EN: Chance to lose bait when attempting to catch fish.

---

### `FishChanceModifier`
`float` · default: `1.0` · range: `0.0–1.0`

RU: Множитель шанса появления рыбы, указанного в Fish_Config.json.
EN: Multiplier for the fish spawn chance specified in Fish_Config.json.

---

### `SafeTimer`
`float` · default: `300.0`

RU: Время, через которое начнутся попытки поймать рыбу, после того как вы положили/поменяли приманку. Предотвращает слишком быструю ловлю. Значение в секундах (300 сек = 5 мин)
EN: Time after placing/changing bait before attempts to catch fish begin. Prevents catching fish too quickly. Value in seconds (300 sec = 5 min).

---

### `WaitTimeMin`
`float` · default: `40.0`
### `WaitTimeMax`
`float` · default: `60.0`

RU: Мин. и макс. время между попытками поймать рыбу. Значение в секундах.
EN: Min. and max. time between attempts to catch fish. Value in seconds.

---

### `MinDistanceToPlayers`
`float` · default: `15.0`

RU: Минимальная дистанция в метрах до ближайшего игрока для возможности поймать рыбу.
EN: Minimum distance in meters to the nearest player required to catch fish.

---

### `DamageAfterCatching`
`float` · default: `5.0`

RU: Урон, наносимый ловушке, после того как рыба поймана.
EN: Damage dealt to the trap after a fish is caught.

---

### `FishList`
`array classname`

RU: Список класснеймов рыб, которые загружают настройки из Fish_Config.json (обязательно нахождение указанной рыбы в конфиге для рыбы) и могут быть пойманы этой ловушкой. Тип воды соотносится с подходящей для нее рыбой автоматически. ВАЖНО: параметр IsActive из Fish_Config.json игнорируется для ловушек.
EN: List of fish classnames that load settings from Fish_Config.json (the specified fish must exist in the fish config) and can be caught by this trap. Water type is matched to the suitable fish automatically. IMPORTANT: the IsActive parameter from Fish_Config.json is ignored for traps.
