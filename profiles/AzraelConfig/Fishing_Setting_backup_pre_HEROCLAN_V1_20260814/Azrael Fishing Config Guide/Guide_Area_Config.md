# Azrael Fishing Mod
# AREA Config Guide

**Config path:** `$profile:\AzraelConfig\Fishing_Setting\Area_Config.json`  
**Guide version:** `1.0`  

---

## About this config

**RU:**  
Этот конфиг содержит настройки специальных зон, в которых можно переписать шансы появления/сигнала для необходимой рыбы или предметов.

**EN:**  
This config contains settings for special zones where you can override spawn and signal chances for specific fish or items.

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

# 1. ============ AREA CONFIG

### `cfg_AzraelAreaList`
`array` 

RU: Список специальных зон.   
EN: List of special zones.

---

### `AreaName`
`string`

RU: Уникальное название зоны. Только латиница, без пробелов.   
EN: Unique zone name. Latin characters only, no spaces.

---

### `AreaNote`
`string`

RU: Текстовое поле для заметок. Не используется нигде.  
EN: Text field for notes. Not used anywhere.

---

### `IsActive`
`bool` · default: `1` · range: `0-1`

RU: Включить/выключить появление данной зоны.
EN: Enable/disable this zone.

---

### `Area_X`
`float`
### `Area_Z`
`float` 

RU: Начальные координаты зоны. Если AreaRadius больше 0, то координаты будут центром зоны. Иначе (при AreaRadius = 0) Area_X/Area_Z и будут первой вершиной зоны-параллелепипеда.
EN: Starting zone coordinates. If AreaRadius is greater than 0, these coordinates will be the center of the zone. Otherwise (when AreaRadius = 0), Area_X/Area_Z will be the first vertex of the box-shaped zone.

---

### `Area_X2`
`float`
### `Area_Z2`
`float` 

RU: Координаты второй вершины зоны-параллелепипеда (при AreaRadius = 0).
EN: Coordinates of the second vertex of the box-shaped zone (when AreaRadius = 0).

---

### `AreaRadius`
`float`

RU: Радиус зоны (цилиндра) в метрах. Если равен 0, то форма зоны сменится на параллелепипед с вершинами.
EN: Zone radius (cylinder) in meters. If set to 0, the zone shape switches to a box using vertices.

---

### `OverrideFishList`
`array` 

RU: Список рыбы, шансы появления/клева которой нужно изменить.   
EN: List of fish whose spawn/bite signal chances should be overridden.

---

### `FishClassname`
`classname`

RU: Класснейм рыбы, для которой буду перезаписаны параметры.   
EN: Fish classname whose parameters will be overridden.

---

### `OverrideChance`
`float`
### `OverrideChanceSignal`
`float`

RU: Обновленные значения шансов появления/сигнала. Подробнее о параметрах в FISH Config Guide.
EN: Updated spawn/signal chance values. See FISH Config Guide for details.

---

### `OverrideJunkList`
`array` 

RU: Список предметов, шансы появления/сигнала которых нужно изменить.   
EN: List of items whose spawn/signal chances should be overridden.

---

### `JunkClassname`
`classname`

RU: Класснейм предмета, для которого буду перезаписаны параметры.   
EN: Item classname whose parameters will be overridden.

---

### `OverrideChanceJunkSea`
`float`
### `OverrideChanceJunkPond`
`float`
### `OverrideChanceSignal`
`float`

RU: Обновленные значения шансов появления/сигнала. Подробнее о параметрах в JUNK Config Guide.
EN: Updated spawn/signal chance values. See JUNK Config Guide for details.
