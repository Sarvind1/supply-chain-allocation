#!/usr/bin/env python3
"""Analyze allocation results."""

import json
import pandas as pd
from pathlib import Path
from collections import Counter, defaultdict
import sys

sys.path.append(str(Path(__file__).parent.parent))


def analyze_allocation_results(results_file):
    """Analyze and summarize allocation results."""
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    if not results:
        print("No results to analyze")
        return
    
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(results)
    
    print(f"\n{'='*60}")
    print(f"ALLOCATION RESULTS ANALYSIS: {results_file}")
    print(f"{'='*60}")
    
    # Basic statistics
    print(f"\nBasic Statistics:")
    print(f"  Total SKUs allocated: {len(df)}")
    print(f"  Total cost: ${df['total_cost'].sum():,.2f}")
    print(f"  Average cost per SKU: ${df['total_cost'].mean():,.2f}")
    print(f"  Average lead time: {df['total_lead_time'].mean():.1f} days")
    print(f"  Average CM3 score: {df['cm3_score'].mean():.3f}")
    
    # Path analysis
    print(f"\nPath Analysis:")
    path_counts = Counter([' -> '.join(path) for path in df['selected_path']])
    print(f"  Unique paths used: {len(path_counts)}")
    print(f"\n  Top 5 most used paths:")
    for path, count in path_counts.most_common(5):
        print(f"    {path}: {count} SKUs")
    
    # Destination analysis
    print(f"\nDestination Analysis:")
    destinations = Counter([path[-1] for path in df['selected_path']])
    for dest, count in destinations.most_common():
        print(f"  {dest}: {count} SKUs")
    
    # Cost breakdown by path length
    print(f"\nCost by Path Length:")
    df['path_length'] = df['selected_path'].apply(len)
    cost_by_length = df.groupby('path_length')['total_cost'].agg(['mean', 'sum', 'count'])
    for length, row in cost_by_length.iterrows():
        print(f"  {length} nodes: ${row['mean']:,.2f} avg, ${row['sum']:,.2f} total ({row['count']} SKUs)")
    
    # Lead time distribution
    print(f"\nLead Time Distribution:")
    lt_bins = [0, 10, 20, 30, 40, 50, 100]
    lt_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '50+']}
    df['lt_bin'] = pd.cut(df['total_lead_time'], bins=lt_bins, labels=lt_labels)
    lt_dist = df['lt_bin'].value_counts().sort_index()
    for bin_name, count in lt_dist.items():
        print(f"  {bin_name} days: {count} SKUs ({count/len(df)*100:.1f}%)")
    
    # Performance metrics
    print(f"\nPerformance Metrics:")
    high_cm3 = df[df['cm3_score'] > df['cm3_score'].quantile(0.75)]
    print(f"  High CM3 score SKUs (top 25%): {len(high_cm3)}")
    print(f"  Average cost for high CM3: ${high_cm3['total_cost'].mean():,.2f}")
    
    # Export summary
    summary_file = Path(results_file).with_suffix('.summary.txt')
    with open(summary_file, 'w') as f:
        f.write(f"Allocation Summary for {results_file}\n")
        f.write(f"{'='*50}\n")
        f.write(f"Total SKUs: {len(df)}\n")
        f.write(f"Total Cost: ${df['total_cost'].sum():,.2f}\n")
        f.write(f"Average Lead Time: {df['total_lead_time'].mean():.1f} days\n")
        f.write(f"Unique Paths: {len(path_counts)}\n")
    
    print(f"\nSummary saved to {summary_file}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        analyze_allocation_results(sys.argv[1])
    else:
        # Analyze all result files
        for results_file in Path("results").glob("*.json"):
            if "summary" not in str(results_file):
                analyze_allocation_results(results_file)