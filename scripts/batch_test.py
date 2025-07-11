#!/usr/bin/env python3
"""Run batch allocation tests with different configurations."""

import subprocess
import time
from pathlib import Path
import json


def run_allocation(products, nodes, edges, output):
    """Run allocation and measure time."""
    start_time = time.time()
    
    cmd = [
        "python", "-m", "src.main",
        "--products", products,
        "--nodes", nodes,
        "--edges", edges,
        "--output", output
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.time() - start_time
    
    return {
        "success": result.returncode == 0,
        "elapsed_time": elapsed,
        "stdout": result.stdout,
        "stderr": result.stderr
    }


def main():
    """Run batch tests."""
    tests = [
        {
            "name": "Simple Network - Small Products",
            "products": "data/dummy/products_small.csv",
            "nodes": "data/dummy/nodes_simple.csv",
            "edges": "data/dummy/node-node_simple.csv",
            "output": "results/batch_simple_small.json"
        },
        {
            "name": "Simple Network - Medium Products",
            "products": "data/dummy/products_medium.csv",
            "nodes": "data/dummy/nodes_simple.csv",
            "edges": "data/dummy/node-node_simple.csv",
            "output": "results/batch_simple_medium.json"
        },
        {
            "name": "Complex Network - Small Products",
            "products": "data/dummy/products_small.csv",
            "nodes": "data/dummy/nodes_complex.csv",
            "edges": "data/dummy/node-node_complex.csv",
            "output": "results/batch_complex_small.json"
        },
        {
            "name": "Complex Network - Medium Products",
            "products": "data/dummy/products_medium.csv",
            "nodes": "data/dummy/nodes_complex.csv",
            "edges": "data/dummy/node-node_complex.csv",
            "output": "results/batch_complex_medium.json"
        },
        {
            "name": "Complex Network - Large Products",
            "products": "data/dummy/products_large.csv",
            "nodes": "data/dummy/nodes_complex.csv",
            "edges": "data/dummy/node-node_complex.csv",
            "output": "results/batch_complex_large.json"
        }
    ]
    
    print("Starting batch allocation tests...\n")
    
    results = []
    for test in tests:
        print(f"Running: {test['name']}...")
        result = run_allocation(
            test["products"],
            test["nodes"],
            test["edges"],
            test["output"]
        )
        
        if result["success"]:
            print(f"  ✓ Completed in {result['elapsed_time']:.2f} seconds")
        else:
            print(f"  ✗ Failed: {result['stderr']}")
        
        results.append({
            "test": test["name"],
            "success": result["success"],
            "elapsed_time": result["elapsed_time"]
        })
    
    # Save batch results
    with open("results/batch_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nBatch Test Summary:")
    print("="*50)
    for r in results:
        status = "✓" if r["success"] else "✗"
        print(f"{status} {r['test']}: {r['elapsed_time']:.2f}s")
    
    total_time = sum(r["elapsed_time"] for r in results)
    success_count = sum(1 for r in results if r["success"])
    print(f"\nTotal: {success_count}/{len(results)} successful, {total_time:.2f}s total time")


if __name__ == "__main__":
    main()