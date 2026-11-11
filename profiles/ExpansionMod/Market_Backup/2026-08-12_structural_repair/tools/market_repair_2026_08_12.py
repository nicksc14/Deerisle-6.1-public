from __future__ import annotations

import csv
import json
import shutil
from collections import defaultdict
from pathlib import Path


PROFILE = Path(r"D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod")
MISSION = Path(r"D:\OneDrive\Deerisle 6.1\mpmissions\empty.deerisle\expansion")
MARKET = PROFILE / "Market"
TRADERS = PROFILE / "Traders"
ZONES = MISSION / "traderzones"
BACKUP = PROFILE / "Market_Backup" / "2026-08-12_structural_repair"
PRE = BACKUP / "pre_change"
ARCHIVE = BACKUP / "archived_market_definitions"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def backup(path: Path) -> None:
    if path.is_relative_to(PROFILE):
        rel = Path("profiles_ExpansionMod") / path.relative_to(PROFILE)
    else:
        rel = Path("mpmissions_empty.deerisle_expansion") / path.relative_to(MISSION)
    target = PRE / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target)


def save_changed(path: Path, data) -> None:
    backup(path)
    write(path, data)


if BACKUP.exists():
    raise SystemExit(f"Refusing to rerun: backup/output directory already exists: {BACKUP}")
BACKUP.mkdir(parents=True)

report: dict[str, object] = {
    "date": "2026-08-12",
    "trader_changes": [],
    "market_changes": [],
    "archived": {},
    "traderzones": {},
}

# 1. Bitcoin traders: visible goods are buy-only (0); bundled dependencies are hidden (3).
trader_category_replacements = {
    "AP_Armor.json": {
        "Bitcoin-AP-Helmet-Parts:0": "Bitcoin-AP-Helmet-Parts:3",
    },
    "Better_Cars.json": {
        "Bitcoin_Batteries:3": "Batteries:3",
        "Bitcoin_Vehicle_Parts:3": "Vehicle_Parts:3",
    },
    "MagLoader.json": {
        "Bitcoin_CDS_Suppressor": "Bitcoin_CDS_Suppressor:0",
        "Bitcoin_CDS_Supp_Special": "Bitcoin_CDS_Supp_Special:0",
    },
}
for trader_name, replacements in trader_category_replacements.items():
    path = TRADERS / trader_name
    data = load(path)
    old_categories = list(data["Categories"])
    new_categories = [replacements.get(category, category) for category in old_categories]
    missing = sorted(set(replacements) - set(old_categories))
    if missing:
        raise AssertionError(f"Expected categories missing in {trader_name}: {missing}")
    data["Categories"] = new_categories
    save_changed(path, data)
    report["trader_changes"].append({"file": trader_name, "category_replacements": replacements})

# 2. Explicit sell-only NBC families. All variants are overridden as well.
nbc_by_trader = {
    "Clothing.json": [
        "nbcbootsgray", "nbcbootsyellow", "nbcbootswhite",
        "nbcjacketgray", "nbcjacketyellow", "nbcjacketwhite",
        "nbcpantsgray", "nbcpantsyellow", "nbcpantswhite",
    ],
    "Clothing_Accessories.json": [
        "nbcglovesgray", "nbcglovesyellow",
        "nbchoodgray", "nbchoodyellow", "nbchoodwhite",
        "gasmask", "gp5gasmask",
    ],
}
for trader_name, classnames in nbc_by_trader.items():
    path = TRADERS / trader_name
    data = load(path)
    items = data.setdefault("Items", {})
    for classname in classnames:
        items[classname] = 2
    save_changed(path, data)
    report["trader_changes"].append({"file": trader_name, "sell_only_items": classnames})

nbc_bases = {
    "Boots_And_Shoes.json": "nbcbootsgray",
    "Coats_And_Jackets.json": "nbcjacketgray",
    "Pants_And_Shorts.json": "nbcpantsgray",
    "Gloves.json": "nbcglovesgray",
    "Hats_And_Hoods.json": "nbchoodgray",
    "Masks.json": ("gasmask", "gp5gasmask"),
}
for market_name, targets in nbc_bases.items():
    targets = (targets,) if isinstance(targets, str) else targets
    path = MARKET / market_name
    data = load(path)
    found = []
    for item in data["Items"]:
        if item["ClassName"].lower() in targets:
            if item["MaxStockThreshold"] != 0 or item["MinStockThreshold"] != 0:
                raise AssertionError(f"NBC item was not 0/0 as expected: {market_name}:{item['ClassName']}")
            item["MaxStockThreshold"] = 100
            item["MinStockThreshold"] = 1
            found.append(item["ClassName"].lower())
    if set(found) != set(targets):
        raise AssertionError(f"NBC targets missing from {market_name}: {set(targets) - set(found)}")
    save_changed(path, data)
    report["market_changes"].append({"file": market_name, "normal_stock_sell_only_bases": found})

# 3. Correct 0.2% typo to 20%. Bitcoin goods remain non-sellable through trader mode 0.
sell_percent_files = {
    "Bitcoin_CDS_Suppressor.json": 2,
    "Bitcoin_CDS_Supp_Special.json": 2,
    "Muzzles.json": 2,
}
for market_name, expected_count in sell_percent_files.items():
    path = MARKET / market_name
    data = load(path)
    changed = []
    for item in data["Items"]:
        if item.get("SellPricePercent") == 0.2:
            item["SellPricePercent"] = 20.0
            changed.append(item["ClassName"])
    if len(changed) != expected_count:
        raise AssertionError(f"Expected {expected_count} 0.2 entries in {market_name}, found {len(changed)}")
    save_changed(path, data)
    report["market_changes"].append({"file": market_name, "sell_percent_20": changed})

# 4. Keep one global zero-price definition for shared bundled vehicle dependencies.
vehicle_parts_path = MARKET / "Vehicle_Parts.json"
vehicle_parts = load(vehicle_parts_path)
hydraulic = [item for item in vehicle_parts["Items"] if item["ClassName"].lower() == "expansionhydraulichoses"]
if len(hydraulic) != 1:
    raise AssertionError("Expected exactly one expansionhydraulichoses definition")
hydraulic[0]["MaxPriceThreshold"] = 0
hydraulic[0]["MinPriceThreshold"] = 0
hydraulic[0]["SellPricePercent"] = -1.0
save_changed(vehicle_parts_path, vehicle_parts)
report["market_changes"].append({"file": "Vehicle_Parts.json", "zero_price_dependency": "expansionhydraulichoses"})

# 5. Archive whole duplicate/unreferenced files outside Market so Expansion does not load them.
whole_files = [
    "Bitcoin_Batteries.json",
    "Bitcoin_Vehicle_Parts.json",
    "Bitcoin-Helicopters.json",
    "Pelts.json",
    "Sweaters_And_Hoodies.json",
]
for market_name in whole_files:
    source = MARKET / market_name
    backup(source)
    target = ARCHIVE / "whole_files" / market_name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))
report["archived"]["whole_files"] = whole_files

# 6. Archive only the independent definitions that have no trader/category/manual/spawn path.
partial_targets = {
    "Ammo.json": {
        "ammo_12gapellets", "ammo_12gaslug", "ammo_22", "ammo_308win",
        "ammo_308wintracer", "ammo_357", "ammo_380", "ammo_40mm_explosive",
        "ammo_45acp", "ammo_556x45", "ammo_556x45tracer", "ammo_762x39",
        "ammo_762x39tracer", "ammo_762x54", "ammo_762x54tracer", "ammo_9x19",
        "ammo_9x39", "ammo_9x39ap", "ammo_flare",
    },
    "Helicopters.json": {"expansionmh6", "expansionuh1h", "expansionmerlin"},
    "Launchers.json": {"flaregun", "m79"},
    "Liquids.json": {"engineoil"},
    "Magazines.json": {
        "mag_akm_drum75rnd", "mag_akm_palm30rnd", "mag_cmag_10rnd",
        "mag_cmag_20rnd", "mag_cmag_30rnd", "mag_cmag_40rnd",
        "mag_mp5_15rnd", "mag_stanag_60rnd", "mag_stanagcoupled_30rnd",
    },
}
partial_archive_report = {}
for market_name, targets in partial_targets.items():
    path = MARKET / market_name
    data = load(path)
    archived_items = [item for item in data["Items"] if item["ClassName"].lower() in targets]
    found = {item["ClassName"].lower() for item in archived_items}
    if found != targets:
        raise AssertionError(f"Archive targets missing from {market_name}: {targets - found}")
    data["Items"] = [item for item in data["Items"] if item["ClassName"].lower() not in targets]
    archive_data = {key: value for key, value in data.items() if key != "Items"}
    archive_data["DisplayName"] = f"[ARCHIVE 2026-08-12] {archive_data.get('DisplayName', market_name)}"
    archive_data["Items"] = archived_items
    save_changed(path, data)
    write(ARCHIVE / "partial_files" / market_name, archive_data)
    partial_archive_report[market_name] = sorted(found)
report["archived"]["partial_files"] = partial_archive_report

# 7. Validate active Market uniqueness and collect valid stock keys/limits.
definitions: dict[str, list[tuple[str, dict]]] = defaultdict(list)
stock_limits: dict[str, list[tuple[int, int]]] = defaultdict(list)
for path in MARKET.rglob("*.json"):
    data = load(path)
    for item in data.get("Items", []):
        base = item["ClassName"].lower()
        definitions[base].append((str(path.relative_to(MARKET)), item))
        max_stock = int(item.get("MaxStockThreshold", 0))
        min_stock = int(item.get("MinStockThreshold", 0))
        stock_limits[base].append((min_stock, max_stock))
        for variant in item.get("Variants", []):
            stock_limits[variant.lower()].append((min_stock, max_stock))

duplicates = {name: rows for name, rows in definitions.items() if len(rows) > 1}
if duplicates:
    raise AssertionError(f"Independent ClassName duplicates remain: {sorted(duplicates)}")
valid_stock_keys = set(stock_limits)

# Verify every trader category points to an active category file stem.
active_category_names = {
    path.relative_to(MARKET).with_suffix("").as_posix().lower()
    for path in MARKET.rglob("*.json")
}
missing_categories = []
for path in TRADERS.glob("*.json"):
    data = load(path)
    for raw in data.get("Categories", []):
        category = raw.rsplit(":", 1)[0].replace("\\", "/").lower()
        if category not in active_category_names:
            missing_categories.append((path.name, raw))
if missing_categories:
    raise AssertionError(f"Trader category references missing after archive: {missing_categories}")

# 8. Precise TraderZone cleanup: preserve valid stocks, remove obsolete keys,
#    clamp only dynamic stocks above current max, and reinitialize only NBC families.
nbc_reinit = {name.lower() for names in nbc_by_trader.values() for name in names}
for zone_path in sorted(ZONES.glob("*.json")):
    zone = load(zone_path)
    stock = zone.get("Stock", {})
    new_stock = {}
    removed_orphans = []
    removed_nbc = []
    clamped = []
    normalized_negative = []
    for raw_name, raw_value in stock.items():
        name = raw_name.lower()
        if name in nbc_reinit:
            removed_nbc.append(raw_name)
            continue
        if name not in valid_stock_keys:
            removed_orphans.append(raw_name)
            continue
        value = raw_value
        limits = stock_limits[name]
        dynamic_maxima = [maximum for minimum, maximum in limits if maximum > minimum]
        if isinstance(value, (int, float)) and value < 0:
            normalized_negative.append((raw_name, value, 0))
            value = 0
        if dynamic_maxima and isinstance(value, (int, float)):
            maximum = max(dynamic_maxima)
            if value > maximum:
                clamped.append((raw_name, value, maximum))
                value = maximum
        new_stock[raw_name] = value
    zone["Stock"] = new_stock
    if removed_orphans or removed_nbc or clamped or normalized_negative:
        save_changed(zone_path, zone)
    report["traderzones"][zone_path.name] = {
        "before": len(stock),
        "after": len(new_stock),
        "removed_orphans": len(removed_orphans),
        "removed_nbc_for_reinit": len(removed_nbc),
        "clamped_dynamic_over_max": len(clamped),
        "normalized_negative": len(normalized_negative),
    }

# 9. Durable armor/weapon relocation manifest. Prices and cutover remain pending.
crosswalk = PROFILE / "EXPANSION_MARKET_REBUILD_CROSSWALK.csv"
migration_csv = PROFILE / "EXPANSION_MARKET_REBUILD_MIGRATION.csv"
backup(crosswalk)
with crosswalk.open("r", encoding="utf-8-sig", newline="") as source:
    rows = list(csv.DictReader(source))
    fieldnames = list(rows[0]) + [
        "target_area", "target_trader", "target_currency",
        "planned_permission", "planned_price_status", "migration_status",
    ]
trader_map = {
    "AP": "AP_Rookie",
    "FOG": "FOG_Trader",
    "MMG": "MMG",
    "TTC": "TTC",
    "SNAFU": "Rookie_Snafu",
    "AJW": "AJW",
}
for row in rows:
    is_armor = row.get("item_kind", "").lower() == "armor"
    row["target_area"] = "WestBrook" if is_armor else "Waldoboro"
    row["target_trader"] = trader_map.get(row.get("source_mod", ""), "PENDING_REVIEW")
    row["target_currency"] = "expansionbanknotehryvnia"
    row["planned_permission"] = "standard area trade; progression exceptions require explicit override"
    row["planned_price_status"] = "pending unified tier price table"
    row["migration_status"] = "pending atomic price-and-trader cutover"
with migration_csv.open("w", encoding="utf-8-sig", newline="") as target:
    writer = csv.DictWriter(target, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
report["migration_manifest"] = {"file": migration_csv.name, "rows": len(rows)}

write(BACKUP / "REPAIR_REPORT.json", report)
print(json.dumps(report, ensure_ascii=False, indent=2))
