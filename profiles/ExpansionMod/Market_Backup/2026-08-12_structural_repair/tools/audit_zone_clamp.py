import json
from collections import defaultdict, Counter
from pathlib import Path

P = Path(r"D:\OneDrive\Deerisle 6.1\profiles\ExpansionMod")
M = P / "Market"
Z = Path(r"D:\OneDrive\Deerisle 6.1\mpmissions\empty.deerisle\expansion\traderzones")
B = P / "Market_Backup" / "2026-08-12_structural_repair" / "pre_change" / "mpmissions_empty.deerisle_expansion" / "traderzones"

base = {}
variant = defaultdict(list)
for path in M.rglob("*.json"):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    for item in data.get("Items", []):
        name = item["ClassName"].lower()
        base[name] = item
        for name2 in item.get("Variants", []):
            variant[name2.lower()].append(item)

for zone in sorted(Z.glob("*.json")):
    old_path = B / zone.name
    if not old_path.exists():
        continue
    old = json.loads(old_path.read_text(encoding="utf-8-sig"))["Stock"]
    new = json.loads(zone.read_text(encoding="utf-8-sig"))["Stock"]
    decreased = [(k, v, new[k]) for k, v in old.items() if k in new and new[k] < v]
    kinds = Counter("base" if k.lower() in base else "variant" if k.lower() in variant else "unknown" for k, _, _ in decreased)
    print(zone.name, len(decreased), dict(kinds))
    if zone.name == "Rookie_Trader.json":
        deltas = Counter()
        examples = defaultdict(list)
        for k, oldv, newv in decreased:
            key = k.lower()
            item = base.get(key)
            kind = "base"
            if not item:
                parents = variant.get(key, [])
                item = parents[0] if parents else None
                kind = "variant"
            if item:
                signature = (kind, item.get("MinStockThreshold"), item.get("MaxStockThreshold"), oldv, newv)
            else:
                signature = (kind, None, None, oldv, newv)
            deltas[signature] += 1
            if len(examples[signature]) < 3:
                examples[signature].append(k)
        for sig, count in deltas.most_common(20):
            print(" ", count, sig, examples[sig])

print("ACTIVE_MARKET_FILES", len(list(M.rglob("*.json"))))
print("ACTIVE_BASE_DEFINITIONS", len(base))
print("ACTIVE_VARIANT_RECORDS", sum(len(v) for v in variant.values()))
all_independent = defaultdict(list)
for path in M.rglob("*.json"):
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    for item in data.get("Items", []):
        all_independent[item["ClassName"].lower()].append(str(path.relative_to(M)))
dupes = {k: v for k, v in all_independent.items() if len(v) > 1}
print("INDEPENDENT_DUPLICATES", len(dupes))
print("ZONE_STOCK_TOTAL", sum(len(json.loads(p.read_text(encoding="utf-8-sig"))["Stock"]) for p in Z.glob("*.json")))
