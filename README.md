# Supply Chain Allocation Engine

A flexible inventory allocation engine using graph-based supply chain networks to optimize product distribution across warehouses and fulfillment centers. Supports cost-based optimization with configurable evaluation methods and comprehensive analytics.

## Features

- **Graph-Based Network**: Model complex supply chain networks with ports, warehouses, and fulfillment centers
- **Flexible Evaluation**: Pluggable evaluator system supporting fixed costs, cluster-based pricing, and custom logic
- **Performance Optimization**: Built-in memoization for evaluator results to handle large product catalogs
- **CM3 Optimization**: Allocates products to maximize Contribution Margin per dollar of cost
- **Comprehensive Testing**: Batch testing framework with dummy data of varying complexity
- **Analytics & Visualization**: Built-in scripts for analyzing results and visualizing network topology
- **Pydantic Validation**: Type-safe data handling with automatic validation

## Tech Stack

- **Python 3.8+** - Language
- **Pydantic** - Data validation and modeling
- **NetworkX** - Graph algorithms and network analysis
- **Pandas** - Data manipulation and analysis
- **Click** - CLI interface
- **Matplotlib** - Network visualization
- **Pytest** - Testing framework

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/supply-chain-allocation.git
cd supply-chain-allocation

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

Run allocation with example data:

```bash
python -m src.main \
    --products data/examples/products.csv \
    --nodes data/examples/nodes.csv \
    --edges data/examples/node-node.csv \
    --output allocation_results.json
```

View results:
```bash
python scripts/analyze_results.py allocation_results.json
```

## Usage Examples

### Simple Network Test

```bash
python -m src.main \
    --products data/dummy/products_small.csv \
    --nodes data/dummy/nodes_simple.csv \
    --edges data/dummy/node-node_simple.csv \
    --output results/simple_test.json
```

### Complex Network Test

```bash
python -m src.main \
    --products data/dummy/products_large.csv \
    --nodes data/dummy/nodes_complex.csv \
    --edges data/dummy/node-node_complex.csv \
    --output results/complex_test.json
```

### Batch Testing

Run multiple test scenarios and compare results:

```bash
python scripts/batch_test.py
```

### Analyze Results

```bash
# Analyze single result file
python scripts/analyze_results.py results/complex_test.json

# Analyze all results in directory
python scripts/analyze_results.py results/
```

### Visualize Network

```bash
python scripts/visualize_network.py --nodes data/examples/nodes.csv \
                                     --edges data/examples/node-node.csv
```

### Generate Custom Test Data

```bash
python scripts/generate_test_data.py --num-products 100 --network complex
```

## Project Structure

```
supply-chain-allocation/
├── src/
│   ├── allocation/        # Allocation algorithm and path evaluation
│   ├── evaluators/        # Cost/feasibility evaluation methods
│   ├── graph/             # Network graph construction and pathfinding
│   ├── models/            # Pydantic data models
│   ├── utils/             # CSV loading and utility functions
│   └── main.py            # CLI entry point
├── data/
│   ├── examples/          # Example CSV files
│   └── dummy/             # Test datasets of various sizes
├── scripts/
│   ├── analyze_results.py # Results analysis and reporting
│   ├── batch_test.py      # Batch testing framework
│   ├── generate_test_data.py  # Test data generation
│   └── visualize_network.py   # Network visualization
├── tests/                 # Unit and integration tests
├── config/
│   └── evaluators.json    # Evaluator configuration
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project metadata
└── README.md             # This file
```

## Data Format

### Products CSV

```csv
sku,origin,volume,weight,category,hazmat
SKU001,Port_Shanghai,100,2500,ELEC,0
SKU002,Port_LA,50,1000,TOYS,0
```

### Nodes CSV

```csv
node_id,node_type,cluster,cost_method,feasibility_method,node_group
warehouse_1,warehouse,US_West,wh_cost,1,group_a
fc_1,fulfillment_center,US_West,0,1,group_a
```

### Node-Node CSV

```csv
from_node,to_node,shipping_time,cost,capacity
Port_Shanghai,warehouse_1,15,1200,5000
warehouse_1,fc_1,3,100,10000
```

## Key Concepts

### CM3 Score

The allocation engine optimizes for CM3 (Contribution Margin 3):

```
CM3 Score = Contribution Margin / Total Cost
```

Higher CM3 scores indicate better margin relative to shipping costs.

### Allocation Process

1. **Path Finding**: Identifies all feasible paths from origin to available destinations
2. **Path Evaluation**: Calculates cost, lead time, and feasibility for each path
3. **Path Selection**: Chooses path with highest CM3 score (or lowest cost if specified)
4. **Result Recording**: Saves allocation decision with cost and timing metrics

### Evaluators

Pluggable evaluation methods support:

- **Fixed costs** - Static pricing (method: "100")
- **No cost** - Free operations (method: "0")
- **Cluster-based** - Cluster pair pricing ("cluster_costs")
- **Warehouse cost** - Per-warehouse rates ("wh_cost")
- **Custom** - User-defined evaluation logic

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=src

# Run specific test file
pytest tests/test_allocation.py -v
```

### Code Style

```bash
# Format code with Black
black src/ scripts/

# Type checking with mypy
mypy src/
```

### Environment Setup

Copy `.env.example` to `.env` if you need to configure runtime behavior:

```bash
cp .env.example .env
```

## Performance Considerations

- **Memoization**: Evaluator results are cached to avoid redundant calculations
- **Path Finding**: Uses NetworkX algorithms optimized for medium-size networks (up to ~100 nodes)
- **Large Products**: For >1000 SKUs, consider splitting into batches

## Output Format

Results are saved as JSON with the following structure:

```json
[
  {
    "sku": "SKU001",
    "chunk_id": "chunk-uuid",
    "origin": "Port_Shanghai",
    "selected_path": ["Port_Shanghai", "warehouse_1", "fc_1"],
    "total_cost": 1350.0,
    "total_lead_time": 18,
    "cm3_score": 0.742,
    "feasible": true
  }
]
```

## Configuration

Edit `config/evaluators.json` to customize evaluation methods:

```json
{
  "default_evaluator": "SimpleEvaluator",
  "evaluators": {
    "SimpleEvaluator": {
      "type": "simple",
      "config": {}
    }
  }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing Guidelines

- Add tests for new features in `tests/`
- Maintain test coverage above 80%
- Run the full test suite before submitting PRs

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Version**: 0.1.0  
**Last Updated**: 2026-04-10
