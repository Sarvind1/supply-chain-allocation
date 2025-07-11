#!/bin/bash
# Run allocation tests with different data sizes

echo "=== Testing Simple Network ==="
python -m src.main \
    --products data/dummy/products_small.csv \
    --nodes data/dummy/nodes_simple.csv \
    --edges data/dummy/node-node_simple.csv \
    --output results/simple_allocation.json

echo "\n=== Testing Complex Network ==="
python -m src.main \
    --products data/dummy/products_medium.csv \
    --nodes data/dummy/nodes_complex.csv \
    --edges data/dummy/node-node_complex.csv \
    --output results/complex_allocation.json

echo "\n=== Testing Large Scale ==="
python -m src.main \
    --products data/dummy/products_large.csv \
    --nodes data/dummy/nodes_complex.csv \
    --edges data/dummy/node-node_complex.csv \
    --output results/large_allocation.json

echo "\nAll tests completed. Check results/ directory for outputs."