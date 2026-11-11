#!/usr/bin/env python3
"""
CJ Black Card → BSHC "Black" Category Migration Script
Reads CJ LootChests_V106.json, generates BSHC loot pool entries.
"""
import json, copy
from pathlib import Path

# === Config ===
CJ_PATH = str(Path(__file__).resolve().parent.parent / 'CJ_LootChests/LootChests_V106.json')
BSHC_LOOT_PATH = str(Path(__file__).resolve().parent.parent / 'Bastardo_HC/loot_pools.json')
BSHC_CRATES_PATH = str(Path(__file__).resolve().parent.parent / 'Bastardo_HC/BS_Dynamic_crates.json')

# Weapons to EXCLUDE (user decision)
EXCLUDE_WEAPONS = {
    'SNAFU_MK4716Gun',       # 75rd drum
    'Snafu_ScarH_Black_GUN', # 100rd drum
    'SNSA58_Gun',            # Drum mag
    'TTC_MRAD',              # .338 Lapua
    'TTC_Beowulf',           # .50 Beowulf
    'SNAFUP90',              # 50rd mag
}

# CJ attachments that are structural (stock, handguard) — always spawn
STRUCTURAL_KEYWORDS = ['stock', 'bttstck', 'hndgrd', 'handguard', 'rail', 'hg', 'hbar',
                       'cylinder', 'barrel', 'chamber', 'buttstock', 'ris', 'lv']

# CJ attachments that are accessories — random spawn
ACCESSORY_KEYWORDS = ['suppressor', 'sil', 'grip', 'bipod', 'light', 'tac', 'fgk',
                      'tllr', 'sadar', 'tacgrip', 'foregrip', 'afg', 'comp']

def is_structural(att_name):
    """Determine if a CJ attachment is structural (always spawns) vs accessory (random)"""
    name_lower = att_name.lower()
    for kw in STRUCTURAL_KEYWORDS:
        if kw in name_lower:
            return True
    return False

def is_accessory(att_name):
    """Determine if a CJ attachment is an accessory"""
    name_lower = att_name.lower()
    for kw in ACCESSORY_KEYWORDS:
        if kw in name_lower:
            return True
    return False

def make_bshc_attachment(name, probability=1.0, quantity_min=-1, quantity_max=-1,
                          spawn_count_min=1, spawn_count_max=1, health=-1.0,
                          variants=None, nested_attachments=None):
    """Create a standard BSHC attachment dict"""
    att = {
        "name": name,
        "variants": variants or [],
        "attachments": nested_attachments or [],
        "probability": probability,
        "health": health,
        "quantity_min": quantity_min,
        "quantity_max": quantity_max,
        "spawn_count_min": spawn_count_min,
        "spawn_count_max": spawn_count_max
    }
    return att

def make_bshc_item(item_name, probability=1.0, health_lvl=0.8,
                    quantity_min=-1, quantity_max=-1, spawn_count_min=1, spawn_count_max=1,
                    attachments=None):
    """Create a standard BSHC item dict"""
    return {
        "item_name": item_name,
        "attachments": attachments or [],
        "probability": probability,
        "quantity_min": quantity_min,
        "quantity_max": quantity_max,
        "health_lvl": health_lvl,
        "spawn_count_min": spawn_count_min,
        "spawn_count_max": spawn_count_max
    }

def translate_cj_preset_to_bshc(preset):
    """Convert a CJ LC_predefined_* weapon preset to BSHC item with attachments"""
    weapon = preset['weapon']
    magazine = preset.get('magazine', '')
    optic = preset.get('optic', '')
    optic_battery = preset.get('opticbattery', 0)
    cj_attachments = preset.get('attachments', [])

    # Filter out empty string attachments
    cj_attachments = [a for a in cj_attachments if a and a.strip()]

    bshc_attachments = []

    # 1. Magazine (always, probability 1.0)
    if magazine and magazine.strip():
        bshc_attachments.append(make_bshc_attachment(magazine, probability=1.0))

    # 2. Sort CJ attachments into structural vs accessory
    structural = []
    accessory = []
    for att in cj_attachments:
        if is_structural(att):
            structural.append(att)
        elif is_accessory(att):
            accessory.append(att)
        else:
            # Unknown type — treat as structural (likely a weapon-specific part)
            structural.append(att)

    # Structural attachments: probability 1.0
    for att in structural:
        bshc_attachments.append(make_bshc_attachment(att, probability=1.0))

    # Accessory attachments: probability 0.4
    for att in accessory:
        bshc_attachments.append(make_bshc_attachment(att, probability=0.4))

    # 3. Optic (probability 0.5)
    if optic and optic.strip():
        optic_attachments = []
        if optic_battery == 1:
            optic_attachments.append(make_bshc_attachment("Battery9V", probability=1.0))
        bshc_attachments.append(make_bshc_attachment(
            optic, probability=0.5, nested_attachments=optic_attachments
        ))

    return make_bshc_item(weapon, attachments=bshc_attachments)

# === Load CJ Data ===
print("Loading CJ LootChests config...")
with open(CJ_PATH) as f:
    cj = json.load(f)

# Build lookups
presets = {}
for p in cj.get('LCPredefinedWeapons', []):
    presets[p['defname']] = p

tables = {}
for t in cj.get('LootCategories', []):
    tables[t['name']] = t['Loot']

# Black card weapon tables
black_weapon_tables = [
    "LC_Table_Weapons_Police",
    "LC_Table_Weapons_SNAFU_Rifiles",
    "LC_Table_Weapons_TTC_Rifiles",
    "LC_Table_Weapons_SNAFU_DMR",
    "LC_Table_Weapons_TTC_DMR"
]

# === Translate Weapons ===
print("Translating CJ weapon presets → BSHC items...")
black_weapons = []
excluded = []
skipped_no_preset = []
stats = {'with_mag': 0, 'with_optic': 0, 'with_battery': 0, 'structural_atts': 0, 'accessory_atts': 0}

for table_name in black_weapon_tables:
    if table_name not in tables:
        print(f"  WARNING: {table_name} not found!")
        continue

    for entry in tables[table_name]:
        if entry in presets:
            preset = presets[entry]
            weapon_name = preset['weapon']

            # Check exclusion list
            if weapon_name in EXCLUDE_WEAPONS:
                excluded.append(weapon_name)
                continue

            bshc_item = translate_cj_preset_to_bshc(preset)
            black_weapons.append(bshc_item)

            # Stats
            for att in bshc_item['attachments']:
                if 'Mag' in att['name'] or 'mag' in att['name'] or 'Rnd' in att['name']:
                    stats['with_mag'] += 1
                if 'Optic' in att['name'] or 'optic' in att['name'] or 'Holo' in att['name'] or 'HAMR' in att['name'] or 'Elcan' in att['name'] or 'ACOG' in att['name'] or 'BugBuster' in att['name'] or 'Aimpoint' in att['name'] or 'HuntingOptic' in att['name']:
                    stats['with_optic'] += 1
                if att['attachments']:  # has nested attachments (battery)
                    stats['with_battery'] += 1
        else:
            skipped_no_preset.append(entry)
            print(f"  WARNING: {entry} has no preset definition! Treating as raw classname.")
            # Treat as raw weapon classname with no attachments
            black_weapons.append(make_bshc_item(entry))

print(f"\n  Weapons translated: {len(black_weapons)}")
print(f"  Excluded: {len(excluded)} — {excluded}")
print(f"  No preset (raw classname): {len(skipped_no_preset)}")
print(f"  Stats: {stats}")

# === Black_Weapons Pool ===
black_weapons_pool = {
    "pool_name": "Black_Weapons",
    "probability": 1.0,
    "min_items": 1,
    "max_items": 2,
    "guaranteed_items": [],
    "items": black_weapons
}

# === Black_Ammo Pool ===
black_ammo_pool = {
    "pool_name": "Black_Ammo",
    "probability": 0.8,
    "min_items": 2,
    "max_items": 4,
    "guaranteed_items": [],
    "items": [
        make_bshc_item("Ammo_762x54", spawn_count_min=1, spawn_count_max=2),
        make_bshc_item("Ammo_308Win", spawn_count_min=1, spawn_count_max=2),
        make_bshc_item("Ammo_556x45", spawn_count_min=1, spawn_count_max=2),
    ]
}

# === Black_Medical Pool ===
# Curated selection from CJ's 48-entry medical table + some key Terje items
black_medical_items = [
    ("FirstAidKit", 1.0), ("BandageDressing", 1.0), ("Morphine", 0.8),
    ("Epinephrine", 0.6), ("TetracyclineAntibiotics", 0.6), ("CharcoalTablets", 0.5),
    ("SalineBag", 0.5), ("BloodBagEmpty", 0.3), ("StartKitIV", 0.3),
    ("AntiChemInjector", 0.4), ("PurificationTablets", 0.4), ("Heatpack", 0.3),
    ("PainkillerTablets", 0.5), ("VitaminBottle", 0.4),
    ("TerjeBandageHemostatic", 0.5), ("TerjeSurgicalKit", 0.3),
    ("TerjeInjectorPropital", 0.3), ("TerjeInjectorZivirol", 0.2),
]

black_medical_pool = {
    "pool_name": "Black_Medical",
    "probability": 0.6,
    "min_items": 1,
    "max_items": 3,
    "guaranteed_items": [],
    "items": [make_bshc_item(name, probability=prob) for name, prob in black_medical_items]
}

# === Black_Collectibles Pool ===
# CJ uses |probability suffix — map to BSHC
collectible_items = []
cj_collection = tables.get("LC_Table_Collection_Common", [])
for entry in cj_collection:
    if '|' in entry:
        item_name, prob_str = entry.split('|', 1)
        prob = float(prob_str)
    else:
        item_name = entry
        prob = 1.0
    collectible_items.append(make_bshc_item(item_name.strip(), probability=prob))

black_collectibles_pool = {
    "pool_name": "Black_Collectibles",
    "probability": 0.5,
    "min_items": 1,
    "max_items": 3,
    "guaranteed_items": [],
    "items": collectible_items
}

# === Black_Valuables Pool ===
black_valuables_pool = {
    "pool_name": "Black_Valuables",
    "probability": 0.5,
    "min_items": 1,
    "max_items": 2,
    "guaranteed_items": [],
    "items": [
        make_bshc_item("ExpansionGoldBar", probability=1.0),
        make_bshc_item("ExpansionGoldNugget", probability=0.5),
        make_bshc_item("CJ_Key201", probability=0.3),
    ]
}

# === Assemble Black Category ===
black_category = [
    black_weapons_pool,
    black_ammo_pool,
    black_medical_pool,
    black_collectibles_pool,
    black_valuables_pool,
]

# === Write to loot_pools.json ===
print("\nLoading existing loot_pools.json...")
with open(BSHC_LOOT_PATH) as f:
    loot_data = json.load(f)

# Insert Black category after Red (before IslandHeaven)
new_categories = {}
inserted = False
for cat_name, pools in loot_data['AllDefinedCategories'].items():
    new_categories[cat_name] = pools
    if cat_name == 'Red' and not inserted:
        new_categories['Black'] = black_category
        inserted = True

if not inserted:
    # Fallback: add at end
    new_categories['Black'] = black_category

loot_data['AllDefinedCategories'] = new_categories

print(f"Writing updated loot_pools.json ({len(new_categories)} categories)...")
with open(BSHC_LOOT_PATH, 'w') as f:
    json.dump(loot_data, f, indent=4)

# === Update BS_Dynamic_crates.json ===
print("\nLoading BS_Dynamic_crates.json...")
with open(BSHC_CRATES_PATH) as f:
    crates = json.load(f)

for crate in crates:
    if crate['ConfigUniqueID'] == 'BSHC_Dynamic_Hard':
        old_cats = crate['LootCategoriesToUse']
        crate['LootCategoriesToUse'] = ['IslandHeaven', 'Black']
        print(f"  Updated BSHC_Dynamic_Hard: {old_cats} → {crate['LootCategoriesToUse']}")
        break
else:
    print("  WARNING: BSHC_Dynamic_Hard not found!")

with open(BSHC_CRATES_PATH, 'w') as f:
    json.dump(crates, f, indent=4)

print("\n=== Migration Complete ===")
print(f"Black category: {len(black_category)} pools")
print(f"  Black_Weapons: {len(black_weapons)} items")
print(f"  Black_Ammo: {len(black_ammo_pool['items'])} items")
print(f"  Black_Medical: {len(black_medical_pool['items'])} items")
print(f"  Black_Collectibles: {len(black_collectibles_pool['items'])} items")
print(f"  Black_Valuables: {len(black_valuables_pool['items'])} items")
print(f"\nExcluded weapons ({len(excluded)}):")
for w in excluded:
    print(f"  - {w}")
