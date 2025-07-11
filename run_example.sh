#!/bin/bash
# Run example allocation

echo "Running supply chain allocation example..."

python -m src.main \
    --products data/examples/products.csv \
    --nodes data/examples/nodes.csv \
    --edges data/examples/node-node.csv \
    --output allocation_results.json

echo "\nResults saved to allocation_results.json"