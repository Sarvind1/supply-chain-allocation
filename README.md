# Supply Chain Allocation Engine

A flexible inventory allocation engine using graph-based supply chain network with Pydantic validation and memoization.

## Features
- 🔗 Graph-based supply chain network
- ✅ Pydantic data validation
- 🚀 Memoized evaluators for performance
- 📊 CM3-optimized allocation
- 🔧 Configurable evaluation methods
- 📈 Comprehensive analytics and visualization

## Quick Start

### Installation
```bash
# Clone the repository
git clone https://github.com/Sarvind1/supply-chain-allocation.git
cd supply-chain-allocation

# Install dependencies
pip install -r requirements.txt
```

### Run Basic Example
```bash
# Simple network
python -m src.main \
    --products data/examples/products.csv \
    --nodes data/examples/nodes.csv \
    --edges data/examples/node-node.csv \
    --output allocation_results.json
```

### Run with Test Data
```bash
# Small test (10 products, simple network)
python -m src.main \
    --products data/dummy/products_small.csv \
    --nodes data/dummy/nodes_simple.csv \
    --edges data/dummy/node-node_simple.csv \
    --output results/test_small.json

# Large test (50 products, complex network)
python -m src.main \
    --products data/dummy/products_large.csv \
    --nodes data/dummy/nodes_complex.csv \
    --edges data/dummy/node-node_complex.csv \
    --output results/test_large.json
```

## Available Test Data

### Products Data
- `products_small.csv` - 10 SKUs for quick testing
- `products_medium.csv` - 25 SKUs for moderate testing  
- `products_large.csv` - 50 SKUs across 10 categories (ELEC, HOME, TOYS, etc.)

### Network Configurations
- **Simple Network**: 1 port → 1 warehouse → 1 FC (5 nodes total)
- **Complex Network**: 3 ports → 9 warehouses → 4 FCs (23 nodes total)

### Supporting Data
- `shipping_times.csv` - Transit times between clusters
- `warehouse_rates.csv` - Storage costs by warehouse
- `ocean_rates.csv` - Shipping rates by port pairs
- `hazmat_rules.csv` - Hazardous material restrictions

## Analysis Tools

### Batch Testing
```bash
# Run multiple test scenarios
python scripts/batch_test.py
```

### Results Analysis
```bash
# Analyze specific result
python scripts/analyze_results.py results/test_large.json

# Analyze all results in directory
python scripts/analyze_results.py
```

### Network Visualization
```bash
# Visualize network structure
python scripts/visualize_network.py
```

### Generate More Test Data
```bash
# Generate custom sized datasets
python scripts/generate_test_data.py
```

## Project Structure
```
├── src/
│   ├── models/       # Pydantic data models
│   ├── graph/        # Network graph engine
│   ├── evaluators/   # Cost/feasibility/LT evaluators
│   ├── allocation/   # Allocation algorithm
│   └── main.py       # Entry point
├── data/
│   ├── examples/     # Basic example files
│   └── dummy/        # Test datasets
├── scripts/          # Utility scripts
├── results/          # Output directory
└── tests/            # Unit tests
```

## Key Concepts

### CM3 Score
The allocation engine optimizes for CM3 (Contribution Margin) score:
```
CM3 Score = Contribution Margin / Total Cost
```

### Path Evaluation
Each path is evaluated for:
1. **Total Cost**: Sum of all node and edge costs
2. **Lead Time**: Sum of all transit times
3. **Feasibility**: All segments must be feasible

### Memoization
Evaluator results are cached based on input parameters for performance.

## Development

### Run Tests
```bash
pytest tests/
```

### Code Style
```bash
black src/
mypy src/
```

## License
MIT License - see LICENSE file for details.
