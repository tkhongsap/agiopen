#!/usr/bin/env python3
"""
Nike Shopping Example

This example demonstrates using Actor mode to browse and shop on Nike.com.
Actor mode provides near-instant execution (~1 second per step) for
e-commerce automation tasks.

Based on official OpenAGI Lux examples.

Usage:
    python nike_shopping.py --product "running shoes" --size 10
    python nike_shopping.py --product "basketball shoes" --size 11 --color black
    python nike_shopping.py --product "air max" --size 9 --add-to-cart
    python nike_shopping.py --verbose
"""

import asyncio
import argparse
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from oagi import AsyncDefaultAgent, AsyncPyautoguiActionHandler, AsyncScreenshotMaker
except ImportError:
    print("Error: oagi package not installed. Run: pip install oagi")
    sys.exit(1)


@dataclass
class ShoppingConfig:
    """Configuration for Nike shopping automation."""
    product_query: str
    size: str
    color: Optional[str] = None
    gender: Optional[str] = None  # Men, Women, Kids
    max_price: Optional[float] = None
    add_to_cart: bool = False
    checkout: bool = False


@dataclass
class ProductInfo:
    """Information about a Nike product."""
    name: str
    price: float
    color: str
    available_sizes: List[str]
    in_stock: bool = True
    url: Optional[str] = None


@dataclass
class ShoppingResult:
    """Result of Nike shopping automation."""
    success: bool
    product_found: bool
    size_available: bool
    added_to_cart: bool
    execution_time: float
    product: Optional[ProductInfo] = None
    error_message: str = ""


async def shop_nike(
    config: ShoppingConfig,
    verbose: bool = False
) -> ShoppingResult:
    """
    Browse and shop on Nike.com using Actor mode.

    This demonstrates Actor mode handling e-commerce workflows
    with product filtering and cart operations.

    Args:
        config: ShoppingConfig with shopping parameters
        verbose: Enable verbose logging

    Returns:
        ShoppingResult with shopping outcome
    """
    start_time = datetime.now()

    agent = AsyncDefaultAgent(
        max_steps=30,
        model="lux-actor-1",  # Actor mode for speed
        verbose=verbose
    )

    # Build filter list
    filters = []
    if config.gender:
        filters.append(f"Select gender: {config.gender}")
    if config.color:
        filters.append(f"Select color: {config.color}")
    if config.max_price:
        filters.append(f"Set max price: ${config.max_price:.2f}")

    filter_instructions = "\n       ".join(filters) if filters else "No additional filters"

    instruction = f"""
    1. Navigate to https://www.nike.com
    2. Click on the search icon or search bar
    3. Type '{config.product_query}' in the search field
    4. Press Enter or click search
    5. Wait for search results to load
    6. Apply filters:
       {filter_instructions}
    7. Click on the first product in the results
    8. Wait for product page to load completely
    9. Note the product name and price
    10. Click on size selector
    11. Select size: {config.size}
    12. Verify size {config.size} is available
    """

    if config.add_to_cart:
        instruction += """
    13. Click 'Add to Bag' button
    14. Wait for confirmation
    15. Verify item was added to cart (check cart icon or popup)
    """

    if config.checkout:
        instruction += """
    16. Click on cart icon
    17. Click 'Checkout' button
    18. Wait for checkout page to load
    """

    try:
        result = await agent.execute(
            instruction,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker()
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return ShoppingResult(
            success=result if isinstance(result, bool) else True,
            product_found=True,   # Would be determined from execution
            size_available=True,  # Would be determined from execution
            added_to_cart=config.add_to_cart,
            execution_time=execution_time
        )

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return ShoppingResult(
            success=False,
            product_found=False,
            size_available=False,
            added_to_cart=False,
            execution_time=execution_time,
            error_message=str(e)
        )


async def check_product_availability(
    product_url: str,
    size: str,
    verbose: bool = False
) -> ShoppingResult:
    """
    Check availability of a specific Nike product.

    Args:
        product_url: Direct URL to Nike product page
        size: Size to check availability for
        verbose: Enable verbose logging

    Returns:
        ShoppingResult with availability info
    """
    start_time = datetime.now()

    agent = AsyncDefaultAgent(
        max_steps=15,
        model="lux-actor-1",
        verbose=verbose
    )

    instruction = f"""
    1. Navigate to {product_url}
    2. Wait for product page to load
    3. Note the product name and current price
    4. Look at the size selector
    5. Check if size {size} is available (not grayed out)
    6. Note all available sizes
    7. Check if 'Add to Bag' button is active
    """

    try:
        result = await agent.execute(
            instruction,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker()
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return ShoppingResult(
            success=result if isinstance(result, bool) else True,
            product_found=True,
            size_available=True,  # Would be determined from execution
            added_to_cart=False,
            execution_time=execution_time
        )

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return ShoppingResult(
            success=False,
            product_found=False,
            size_available=False,
            added_to_cart=False,
            execution_time=execution_time,
            error_message=str(e)
        )


async def compare_products(
    products: List[str],
    size: str,
    verbose: bool = False
) -> dict:
    """
    Compare multiple Nike products.

    Args:
        products: List of product search queries
        size: Size to check for all products
        verbose: Enable verbose logging

    Returns:
        dict mapping product queries to ShoppingResult
    """
    results = {}

    for i, product in enumerate(products, 1):
        print(f"\n[{i}/{len(products)}] Searching: {product}")

        config = ShoppingConfig(
            product_query=product,
            size=size,
            add_to_cart=False
        )

        result = await shop_nike(config, verbose)
        results[product] = result

        status = "Found" if result.product_found else "Not Found"
        print(f"    Status: {status}")
        print(f"    Time: {result.execution_time:.2f}s")

        if i < len(products):
            await asyncio.sleep(2)

    return results


def print_results(result: ShoppingResult, config: ShoppingConfig):
    """Print formatted shopping results."""
    print("\n" + "=" * 60)
    print("NIKE SHOPPING RESULTS")
    print("=" * 60)

    print(f"\nSearch: {config.product_query}")
    print(f"Size: {config.size}")
    if config.color:
        print(f"Color: {config.color}")
    if config.max_price:
        print(f"Max Price: ${config.max_price:.2f}")

    print(f"\nStatus:")
    print(f"  Success: {'Yes' if result.success else 'No'}")
    print(f"  Product Found: {'Yes' if result.product_found else 'No'}")
    print(f"  Size Available: {'Yes' if result.size_available else 'No'}")
    print(f"  Added to Cart: {'Yes' if result.added_to_cart else 'No'}")
    print(f"  Execution Time: {result.execution_time:.2f} seconds")

    if result.product:
        print(f"\nProduct Details:")
        print(f"  Name: {result.product.name}")
        print(f"  Price: ${result.product.price:.2f}")
        print(f"  Color: {result.product.color}")
        print(f"  In Stock: {'Yes' if result.product.in_stock else 'No'}")

    if result.error_message:
        print(f"\nError: {result.error_message}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Browse and shop on Nike.com using Lux Actor mode"
    )
    parser.add_argument(
        "--product", "-p",
        default="running shoes",
        help="Product to search for (default: 'running shoes')"
    )
    parser.add_argument(
        "--size", "-s",
        default="10",
        help="Shoe size (default: 10)"
    )
    parser.add_argument(
        "--color", "-c",
        help="Preferred color"
    )
    parser.add_argument(
        "--gender", "-g",
        choices=["Men", "Women", "Kids"],
        help="Gender category"
    )
    parser.add_argument(
        "--max-price",
        type=float,
        help="Maximum price filter"
    )
    parser.add_argument(
        "--add-to-cart",
        action="store_true",
        help="Add product to cart"
    )
    parser.add_argument(
        "--checkout",
        action="store_true",
        help="Proceed to checkout (requires --add-to-cart)"
    )
    parser.add_argument(
        "--compare",
        nargs="+",
        help="Compare multiple products"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()


async def main():
    """Main entry point."""
    args = parse_args()

    print("=" * 60)
    print("Nike Shopping - Actor Mode Example")
    print("=" * 60)
    print(f"\nModel: lux-actor-1 (Actor mode)")
    print("Speed: ~1 second per step")

    if args.compare:
        # Compare multiple products
        print(f"\nComparing {len(args.compare)} products...")
        results = await compare_products(args.compare, args.size, args.verbose)

        print("\n" + "=" * 60)
        print("COMPARISON SUMMARY")
        print("=" * 60)
        for product, result in results.items():
            status = "OK" if result.success else "FAIL"
            print(f"  [{status}] {product}")

    else:
        # Single product search
        config = ShoppingConfig(
            product_query=args.product,
            size=args.size,
            color=args.color,
            gender=args.gender,
            max_price=args.max_price,
            add_to_cart=args.add_to_cart,
            checkout=args.checkout and args.add_to_cart
        )

        print(f"\nSearching for: {config.product_query}")
        result = await shop_nike(config, args.verbose)
        print_results(result, config)

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
