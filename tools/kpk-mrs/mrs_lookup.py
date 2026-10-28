#!/usr/bin/env python3
"""
Khyber Pakhtunkhwa Market Rate System (KPK MRS) Lookup CLI & API
Official Finance Department, Government of Khyber Pakhtunkhwa (MRS-2025 1st Bi-Annual)
Website: https://www.finance.gkp.pk/articles/info-desk/market-rate-system
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Optional

INDEX_PATH = os.path.join(os.path.dirname(__file__), "kpk_mrs_2025_index.json")

def load_index() -> dict:
    if not os.path.exists(INDEX_PATH):
        raise FileNotFoundError(f"KPK MRS index not found at {INDEX_PATH}")
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def lookup_mrs(
    code: Optional[str] = None,
    query: Optional[str] = None,
    chapter: Optional[str] = None,
    district: Optional[str] = None,
    limit: int = 10
) -> List[Dict]:
    data = load_index()
    items = data["items"]
    district_factors = data["district_factors"]
    
    factor = 1.00
    if district:
        dist_key = district.strip().upper()
        if dist_key in district_factors:
            factor = district_factors[dist_key]
        else:
            for k, v in district_factors.items():
                if dist_key in k:
                    factor = v
                    dist_key = k
                    break

    results = []
    for it in items:
        if code and code.lower() in it["code"].lower():
            res = dict(it)
            res["district"] = district or "Peshawar (Base)"
            res["district_factor"] = factor
            res["adjusted_composite_rate"] = round(it["rate_metric_composite"] * factor, 2)
            res["adjusted_labour_rate"] = round(it["rate_metric_labour"] * factor, 2)
            results.append(res)
            continue
            
        if chapter and it["chapter"] != str(chapter).zfill(2):
            continue
            
        if query:
            q_terms = query.lower().split()
            desc = it["description"].lower()
            if all(term in desc for term in q_terms):
                res = dict(it)
                res["district"] = district or "Peshawar (Base)"
                res["district_factor"] = factor
                res["adjusted_composite_rate"] = round(it["rate_metric_composite"] * factor, 2)
                res["adjusted_labour_rate"] = round(it["rate_metric_labour"] * factor, 2)
                results.append(res)
                if len(results) >= limit:
                    break

    return results

def main():
    parser = argparse.ArgumentParser(description="Query KPK MRS 2025 official rates.")
    parser.add_argument("--code", type=str, help="MRS Item code (e.g. 19-25, 06-08-b)")
    parser.add_argument("--query", type=str, help="Search keywords in item description (e.g. gabion, pitching)")
    parser.add_argument("--chapter", type=str, help="Chapter number (e.g. 03, 06, 17, 19)")
    parser.add_argument("--district", type=str, help="District name to apply location factor (e.g. Swat, Chitral, Abbottabad)")
    parser.add_argument("--limit", type=int, default=10, help="Max results to display")
    
    args = parser.parse_args()
    
    if not (args.code or args.query or args.chapter):
        parser.print_help()
        sys.exit(1)
        
    res = lookup_mrs(code=args.code, query=args.query, chapter=args.chapter, district=args.district, limit=args.limit)
    
    if not res:
        print("No matching MRS items found.")
        return
        
    print(f"\nFound {len(res)} matching item(s) from KPK MRS-2025 (1st Bi-Annual):")
    print("=" * 80)
    for it in res:
        print(f"Item Code : {it['code']} (Chapter {it['chapter']}) | Page {it['page']}")
        print(f"Desc      : {it['description']}")
        print(f"Unit      : {it['unit']}")
        print(f"Base Rate : Labour: PKR {it['rate_metric_labour']:,.2f} | Composite: PKR {it['rate_metric_composite']:,.2f}")
        if it.get("district_factor", 1.0) != 1.0:
            print(f"District  : {it['district']} (Factor: {it['district_factor']})")
            print(f"Adj Rate  : Labour: PKR {it['adjusted_labour_rate']:,.2f} | Composite: PKR {it['adjusted_composite_rate']:,.2f}")
        print("-" * 80)

if __name__ == "__main__":
    main()
