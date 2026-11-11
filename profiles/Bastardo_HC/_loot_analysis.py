#!/usr/bin/env python3
"""
BSHC Loot Probability & Market Value Analysis
Analyzes expected items and sell value per dynamic crate difficulty.
"""
import json, os, random, glob
from pathlib import Path
from collections import defaultdict

# === Load BSHC loot pools ===
with open(str(Path(__file__).resolve().parent.parent / 'Bastardo_HC/loot_pools.json')) as f:
    loot_data = json.load(f)

# === Load BSHC dynamic crates ===
with open(str(Path(__file__).resolve().parent.parent / 'Bastardo_HC/BS_Dynamic_crates.json')) as f:
    crates = json.load(f)

# === Build Market Price Database ===
market_dir = str(Path(__file__).resolve().parent.parent / 'ExpansionMod/Market')
price_db = {}

def load_market_file(filepath):
    try:
        with open(filepath) as f:
            data = json.load(f)
        if 'Items' in data:
            for item in data['Items']:
                cn = item.get('ClassName', '').lower()
                # Also store SpawnAttachments for price lookup
                atts = item.get('SpawnAttachments', [])
                min_price = item.get('MinPriceThreshold', 0)
                max_price = item.get('MaxPriceThreshold', 0)
                sell_pct = item.get('SellPricePercent', -1.0)
                # Sell price: if SellPricePercent > 0, use that % of min price
                # Otherwise typical sell is ~50% of buy price (min)
                if sell_pct > 0:
                    sell_price = min_price * sell_pct / 100.0
                else:
                    sell_price = min_price * 0.5  # default sell is 50% of min
                price_db[cn] = {
                    'min_buy': min_price,
                    'max_buy': max_price,
                    'sell': int(sell_price),
                    'attachments': [a.lower() for a in atts]
                }
    except:
        pass

# Load ALL market JSON files
for root, dirs, files in os.walk(market_dir):
    for fname in files:
        if fname.endswith('.json'):
            load_market_file(os.path.join(root, fname))

print(f"Market price database: {len(price_db)} items loaded")

# === Loot Simulation Engine ===
SIMULATIONS = 50000

def weighted_choice(choices, key='probability'):
    """Weighted random selection from list of dicts"""
    if not choices:
        return None
    total = sum(c.get(key, 0) for c in choices)
    if total <= 0:
        return random.choice(choices)
    r = random.random() * total
    cumulative = 0
    for c in choices:
        cumulative += c.get(key, 0)
        if r <= cumulative:
            return c
    return choices[-1]

def count_item_and_attachments(item):
    """Recursively count an item and all its attachments. Returns (count, list_of_names)."""
    names = [item['item_name']]
    count = 1
    spawn_count = max(item.get('spawn_count_min', 1), item.get('spawn_count_max', 1))
    count = spawn_count  # overwrite base count with spawn_count

    for att in item.get('attachments', []):
        # Attachment probability uses absolute percentage (0.0-1.0)
        prob = att.get('probability', 1.0)
        if random.random() < prob:
            # Check variants
            if att.get('variants'):
                all_options = [att['name']] + att['variants']
                chosen_name = random.choice(all_options)
            else:
                chosen_name = att['name']

            att_spawn_count = max(att.get('spawn_count_min', 1), att.get('spawn_count_max', 1))
            names.append(chosen_name)
            count += att_spawn_count

            # Recursively count nested attachments
            for nested in att.get('attachments', []):
                nprob = nested.get('probability', 1.0)
                if random.random() < nprob:
                    nspawn = max(nested.get('spawn_count_min', 1), nested.get('spawn_count_max', 1))
                    names.append(nested['name'])
                    count += nspawn
    return count, names

def simulate_pool(pool):
    """Simulate one pool selection. Returns (item_count, item_names)."""
    total_items = 0
    all_names = []

    # Guaranteed items always spawn
    for item in pool.get('guaranteed_items', []):
        c, names = count_item_and_attachments(item)
        total_items += c
        all_names.extend(names)

    # Random items
    items_list = pool.get('items', [])
    if items_list:
        min_n = pool.get('min_items', 1)
        max_n = pool.get('max_items', 1)
        n = random.randint(min_n, max_n)

        if n > 0:
            # Weighted random selection without replacement
            available = list(items_list)
            for _ in range(n):
                if not available:
                    break
                chosen = weighted_choice(available)
                if chosen is None:
                    break
                c, names = count_item_and_attachments(chosen)
                total_items += c
                all_names.extend(names)
                available.remove(chosen)

    return total_items, all_names

def simulate_category(category_name):
    """Simulate one category: pick a pool, generate items. Returns (item_count, item_names)."""
    pools = loot_data['AllDefinedCategories'].get(category_name, [])
    if not pools:
        return 0, []

    chosen_pool = weighted_choice(pools)
    if chosen_pool is None:
        return 0, []

    return simulate_pool(chosen_pool)

def simulate_crate(categories):
    """Simulate one crate opening with multiple categories. Returns (item_count, item_names)."""
    total_items = 0
    all_names = []
    for cat in categories:
        c, names = simulate_category(cat)
        total_items += c
        all_names.extend(names)
    return total_items, all_names

def lookup_price(item_name):
    """Look up market sell price for an item."""
    key = item_name.lower()
    if key in price_db:
        return price_db[key]['sell']
    return 0

# === Run Simulations ===
print(f"\nRunning {SIMULATIONS} simulations per crate...\n")

for crate in crates:
    config_id = crate['ConfigUniqueID']
    categories = crate.get('LootCategoriesToUse', [])
    countdown = crate.get('CountdownTime', 0)

    results = []
    for _ in range(SIMULATIONS):
        count, names = simulate_crate(categories)
        total_value = sum(lookup_price(n) for n in names)
        results.append({
            'count': count,
            'value': total_value,
            'names': names
        })

    counts = [r['count'] for r in results]
    values = [r['value'] for r in results]

    avg_count = sum(counts) / len(counts)
    avg_value = sum(values) / len(values)

    # Percentiles
    sorted_vals = sorted(values)
    p10 = sorted_vals[int(len(sorted_vals) * 0.1)]
    p25 = sorted_vals[int(len(sorted_vals) * 0.25)]
    p50 = sorted_vals[int(len(sorted_vals) * 0.5)]
    p75 = sorted_vals[int(len(sorted_vals) * 0.75)]
    p90 = sorted_vals[int(len(sorted_vals) * 0.9)]
    p95 = sorted_vals[int(len(sorted_vals) * 0.95)]
    p99 = sorted_vals[int(len(sorted_vals) * 0.99)]
    min_v = min(values)
    max_v = max(values)

    # Most common items
    from collections import Counter
    all_item_names = []
    for r in results:
        all_item_names.extend(r['names'])
    top_items = Counter(all_item_names).most_common(20)

    # Count how often each item appears per crate
    item_freq = {}
    for r in results:
        for n in set(r['names']):
            item_freq[n] = item_freq.get(n, 0) + 1

    # Top items with frequency and price
    top_with_prices = []
    for name, freq in Counter(all_item_names).most_common(20):
        price = lookup_price(name)
        freq_pct = freq / SIMULATIONS * 100
        if price > 0:
            top_with_prices.append((name, freq_pct, price))
        else:
            top_with_prices.append((name, freq_pct, 0))

    print(f"{'='*80}")
    print(f"📦 {config_id}")
    print(f"   Categories: {categories}")
    print(f"   Countdown: {countdown}s")
    print(f"{'─'*80}")
    print(f"   📊 物品数量统计:")
    sorted_counts = sorted(counts)
    p50_c = sorted_counts[int(len(sorted_counts) * 0.5)]
    p95_c = sorted_counts[int(len(sorted_counts) * 0.95)]
    print(f"      平均: {avg_count:.1f} 件")
    print(f"      P50:  {p50_c} 件 | P95: {p95_c} 件")
    print(f"      范围: {min(counts)} - {max(counts)} 件")
    print(f"{'─'*80}")
    print(f"   💰 售出价值统计 (Expansion Market):")
    print(f"      平均: {avg_value:,.0f} ₽")
    print(f"      P10:  {p10:,.0f} ₽")
    print(f"      P25:  {p25:,.0f} ₽")
    print(f"      P50:  {p50:,.0f} ₽ (中位数)")
    print(f"      P75:  {p75:,.0f} ₽")
    print(f"      P90:  {p90:,.0f} ₽")
    print(f"      P95:  {p95:,.0f} ₽")
    print(f"      P99:  {p99:,.0f} ₽")
    print(f"      最小: {min(values):,.0f} | 最大: {max(values):,.0f} ₽")
    print(f"{'─'*80}")
    # Category-level breakdown
    print(f"   📋 各 Category 贡献:")
    for cat in categories:
        cat_results = []
        for _ in range(10000):
            c, names = simulate_category(cat)
            cat_results.append({'count': c, 'value': sum(lookup_price(n) for n in names)})
        cat_avg_count = sum(r['count'] for r in cat_results) / len(cat_results)
        cat_avg_value = sum(r['value'] for r in cat_results) / len(cat_results)
        print(f"      {cat:<30} 平均 {cat_avg_count:5.1f} 件 | 价值 {cat_avg_value:>8,.0f} ₽")
    print(f"{'─'*80}")
    print(f"   🎯 最常出现物品 (占比 + 售价):")
    for name, freq_pct, price in top_with_prices[:15]:
        bar = '█' * int(freq_pct / 2)
        price_str = f"{price:,}₽" if price > 0 else "无价格"
        print(f"      {name:<45} {freq_pct:5.1f}% {bar} {price_str}")

    print()

# === Summary Comparison ===
print(f"\n{'='*80}")
print(f"📊 三种难度对比总结")
print(f"{'='*80}")

summary_data = []
for crate in crates:
    config_id = crate['ConfigUniqueID']
    categories = crate.get('LootCategoriesToUse', [])
    results = []
    for _ in range(SIMULATIONS):
        count, names = simulate_crate(categories)
        total_value = sum(lookup_price(n) for n in names)
        results.append({'count': count, 'value': total_value})

    counts = [r['count'] for r in results]
    values = [r['value'] for r in results]
    sorted_vals = sorted(values)

    avg_count = sum(counts) / len(counts)
    avg_value = sum(values) / len(values)

    print(f"\n  {config_id}:")
    print(f"    物品: 平均 {avg_count:.1f} 件 | 价值: 平均 {avg_value:,.0f} ₽ | P50 {sorted_vals[len(sorted_vals)//2]:,.0f} ₽")

print()
print("⚠️  注意: 售价基于 Expansion Market MinPriceThreshold × 50% (默认卖出比例)")
print("  实际游戏中价格会受市场供需、服务器设定影响")
print(f"  模拟次数: {SIMULATIONS} 次/箱子")
