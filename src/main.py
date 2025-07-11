"""Main entry point for supply chain allocation."""

import click
from pathlib import Path
import json

from .models import NetworkGraph
from .utils import load_products, load_nodes, load_edges, validate_network_integrity
from .graph import NetworkBuilder
from .evaluators import create_evaluator, load_evaluator_config
from .allocation import Allocator


@click.command()
@click.option('--products', type=click.Path(exists=True), required=True, help='Products CSV file')
@click.option('--nodes', type=click.Path(exists=True), required=True, help='Nodes CSV file')
@click.option('--edges', type=click.Path(exists=True), required=True, help='Node-Node CSV file')
@click.option('--config', type=click.Path(), default='config/evaluators.json', help='Evaluator config')
@click.option('--output', type=click.Path(), default='allocation_results.json', help='Output file')
def main(products, nodes, edges, config, output):
    """Run supply chain allocation."""
    click.echo("Loading data...")
    
    # Load CSV data
    products_data = load_products(Path(products))
    nodes_data = load_nodes(Path(nodes))
    edges_data = load_edges(Path(edges))
    
    # Validate network integrity
    validate_network_integrity(nodes_data, edges_data)
    
    click.echo(f"Loaded {len(products_data)} products, {len(nodes_data)} nodes, {len(edges_data)} edges")
    
    # Build network graph
    click.echo("Building network graph...")
    builder = NetworkBuilder()
    graph = builder.build(nodes_data, edges_data)
    builder.validate_connectivity()
    
    stats = builder.get_stats()
    click.echo(f"Network stats: {stats}")
    
    # Load evaluator configuration
    click.echo("Loading evaluator configuration...")
    evaluator_config = load_evaluator_config(Path(config))
    evaluator = create_evaluator(evaluator_config)
    
    # Create allocator
    allocator = Allocator(builder, evaluator)
    
    # Allocate products
    click.echo("Running allocation...")
    results = allocator.allocate_products(products_data)
    
    click.echo(f"Allocated {len(results)} products")
    
    # Save results
    output_data = [result.dict() for result in results]
    with open(output, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)
    
    click.echo(f"Results saved to {output}")
    
    # Print summary
    total_cost = sum(r.total_cost for r in results)
    avg_lead_time = sum(r.total_lead_time for r in results) / len(results) if results else 0
    
    click.echo("\nAllocation Summary:")
    click.echo(f"  Total products allocated: {len(results)}")
    click.echo(f"  Total cost: ${total_cost:,.2f}")
    click.echo(f"  Average lead time: {avg_lead_time:.1f} days")
    
    # Show cache stats
    if hasattr(evaluator.evaluate, 'cache_stats'):
        stats = evaluator.evaluate.cache_stats()
        click.echo(f"\nCache performance: {stats}")


if __name__ == "__main__":
    main()