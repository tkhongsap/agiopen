#!/usr/bin/env python3
"""
Amazon Product Search Example

This example demonstrates using the TaskerAgent framework to automate
product searching and data extraction on Amazon.com.

Based on the official oagi-lux-samples repository pattern.

Usage:
    python amazon_product_search.py \
        --product "wireless headphones" \
        --sort-by "best-sellers" \
        --max-products 10 \
        --output products.json
"""

import asyncio
import argparse
import json
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from oagi import TaskerAgent
    from oagi import AsyncPyautoguiActionHandler, AsyncScreenshotMaker
except ImportError:
    print("Error: oagi package not installed. Run: pip install oagi")
    sys.exit(1)


@dataclass
class SearchConfig:
    """Configuration for Amazon product search."""
    product_name: str
    sort_by: str = "relevance"  # relevance, price-low-high, price-high-low, best-sellers, rating
    max_products: int = 10
    min_rating: Optional[float] = None  # e.g., 4.0
    max_price: Optional[float] = None
    prime_only: bool = False
    output_file: Optional[str] = None


@dataclass
class ProductInfo:
    """Extracted product information."""
    name: str
    price: str
    rating: Optional[str] = None
    review_count: Optional[str] = None
    url: Optional[str] = None
    is_prime: bool = False
    is_bestseller: bool = False


@dataclass
class SearchResult:
    """Result of product search operation."""
    success: bool
    products: List[ProductInfo] = field(default_factory=list)
    search_query: str = ""
    total_results: Optional[int] = None
    execution_time: float = 0.0
    errors: List[str] = field(default_factory=list)


async def search_amazon_products(config: SearchConfig, verbose: bool = False) -> SearchResult:
    """
    Search for products on Amazon using TaskerAgent.

    Args:
        config: SearchConfig with search parameters
        verbose: Enable verbose logging

    Returns:
        SearchResult with found products
    """
    # Initialize TaskerAgent
    tasker = TaskerAgent(
        max_steps=30,
        model="lux-tasker-1",
        retry_on_failure=True,
        max_retries=3,
        timeout_per_step=30,
        verbose=verbose
    )

    # Build sort parameter
    sort_mapping = {
        "relevance": "relevanceblender",
        "price-low-high": "price-asc-rank",
        "price-high-low": "price-desc-rank",
        "best-sellers": "bestsellers",
        "rating": "review-rank",
        "newest": "date-desc-rank"
    }
    sort_param = sort_mapping.get(config.sort_by, "relevanceblender")

    # Build filter steps
    filter_steps = []
    if config.prime_only:
        filter_steps.append("Check the 'Prime' filter checkbox on the left sidebar")
    if config.min_rating:
        filter_steps.append(f"Click on '{config.min_rating} Stars & Up' in the Customer Reviews filter")
    if config.max_price:
        filter_steps.append(f"Enter '{config.max_price}' in the Max price field and apply filter")

    # Define the step-by-step task sequence
    steps = [
        # Navigation
        "Navigate to https://www.amazon.com",
        "Wait for the page to fully load",

        # Search
        f"Click on the search box at the top of the page",
        f"Type '{config.product_name}' in the search box",
        "Click the search button or press Enter",
        "Wait for search results to load",

        # Sorting
        f"Click on the 'Sort by' dropdown",
        f"Select '{config.sort_by.replace('-', ' ').title()}' from the dropdown options",
        "Wait for results to update",

        # Apply filters (if any)
        *filter_steps,

        # Data extraction
        f"For each of the top {config.max_products} products in the results, extract:",
        "  - Product name/title",
        "  - Price",
        "  - Star rating",
        "  - Number of reviews",
        "  - Whether it has Prime badge",
        "  - Whether it's a Best Seller",

        # Copy data
        "Select and copy all extracted product data to clipboard",
    ]

    # Execute the task
    result = await tasker.execute(
        steps=steps,
        action_handler=AsyncPyautoguiActionHandler(),
        image_provider=AsyncScreenshotMaker(),
    )

    return SearchResult(
        success=result.success,
        products=[],  # Would be populated from clipboard data
        search_query=config.product_name,
        execution_time=result.execution_time,
        errors=result.errors if hasattr(result, 'errors') else []
    )


async def search_multiple_products(
    products: List[str],
    config: SearchConfig,
    verbose: bool = False
) -> dict:
    """
    Search for multiple products sequentially.

    Args:
        products: List of product names to search
        config: Base SearchConfig (product_name will be overwritten)
        verbose: Enable verbose logging

    Returns:
        dict mapping product names to their SearchResults
    """
    results = {}

    for i, product in enumerate(products, 1):
        print(f"\nSearching {i}/{len(products)}: {product}")

        # Create config for this product
        product_config = SearchConfig(
            product_name=product,
            sort_by=config.sort_by,
            max_products=config.max_products,
            min_rating=config.min_rating,
            max_price=config.max_price,
            prime_only=config.prime_only
        )

        try:
            result = await search_amazon_products(product_config, verbose)
            results[product] = result
            print(f"  Status: {'Success' if result.success else 'Failed'}")
        except Exception as e:
            print(f"  Error: {e}")
            results[product] = SearchResult(
                success=False,
                search_query=product,
                errors=[str(e)]
            )

        # Brief pause between searches
        if i < len(products):
            await asyncio.sleep(2)

    return results


def export_results(results: SearchResult, output_file: str):
    """Export search results to JSON file."""
    data = {
        "search_query": results.search_query,
        "success": results.success,
        "total_results": results.total_results,
        "execution_time": results.execution_time,
        "timestamp": datetime.now().isoformat(),
        "products": [
            {
                "name": p.name,
                "price": p.price,
                "rating": p.rating,
                "review_count": p.review_count,
                "url": p.url,
                "is_prime": p.is_prime,
                "is_bestseller": p.is_bestseller
            }
            for p in results.products
        ],
        "errors": results.errors
    }

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"\nResults exported to: {output_file}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Search Amazon products using Lux TaskerAgent"
    )
    parser.add_argument("--product", required=True, help="Product name to search")
    parser.add_argument("--sort-by", default="relevance",
                        choices=["relevance", "price-low-high", "price-high-low",
                                 "best-sellers", "rating", "newest"],
                        help="Sort order for results")
    parser.add_argument("--max-products", type=int, default=10,
                        help="Maximum number of products to extract")
    parser.add_argument("--min-rating", type=float, help="Minimum star rating filter")
    parser.add_argument("--max-price", type=float, help="Maximum price filter")
    parser.add_argument("--prime-only", action="store_true", help="Only show Prime items")
    parser.add_argument("--output", help="Output JSON file path")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    # Create search configuration
    config = SearchConfig(
        product_name=args.product,
        sort_by=args.sort_by,
        max_products=args.max_products,
        min_rating=args.min_rating,
        max_price=args.max_price,
        prime_only=args.prime_only,
        output_file=args.output
    )

    print("=" * 60)
    print("Amazon Product Search - TaskerAgent Example")
    print("=" * 60)
    print(f"\nSearching for: {config.product_name}")
    print(f"Sort by: {config.sort_by}")
    print(f"Max products: {config.max_products}")
    if config.min_rating:
        print(f"Min rating: {config.min_rating} stars")
    if config.max_price:
        print(f"Max price: ${config.max_price}")
    if config.prime_only:
        print("Prime only: Yes")
    print("")

    # Execute search
    result = await search_amazon_products(config, verbose=args.verbose)

    # Print results
    print("\n" + "=" * 60)
    print("SEARCH RESULT")
    print("=" * 60)
    print(f"Success: {result.success}")
    print(f"Products found: {len(result.products)}")
    print(f"Time: {result.execution_time:.2f} seconds")

    if result.products:
        print("\nProducts:")
        for i, product in enumerate(result.products, 1):
            print(f"  {i}. {product.name}")
            print(f"     Price: {product.price}")
            if product.rating:
                print(f"     Rating: {product.rating} ({product.review_count} reviews)")

    if result.errors:
        print(f"\nErrors: {result.errors}")

    # Export if output file specified
    if config.output_file:
        export_results(result, config.output_file)

    return 0 if result.success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
