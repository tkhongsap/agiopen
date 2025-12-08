#!/usr/bin/env python3
"""
AAPL Insider Activity Example

This example demonstrates using Actor mode to navigate to NASDAQ's website
and extract Apple's insider activity data.

Actor mode provides near-instant execution (~1 second per step) for
direct, well-defined tasks.

Based on official OpenAGI Lux examples.

Usage:
    python aapl_insider_activity.py
    python aapl_insider_activity.py --symbol MSFT
    python aapl_insider_activity.py --verbose
"""

import asyncio
import argparse
from dataclasses import dataclass
from typing import List, Optional
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
class InsiderTransaction:
    """Represents a single insider transaction."""
    insider_name: str
    title: str
    transaction_type: str  # Buy, Sell, Exercise
    shares: int
    price: float
    date: str
    value: float = 0.0


@dataclass
class InsiderActivityResult:
    """Result of insider activity extraction."""
    symbol: str
    company_name: str
    transactions: List[InsiderTransaction]
    extraction_time: float
    success: bool
    error_message: str = ""


async def get_insider_activity(
    symbol: str = "AAPL",
    verbose: bool = False
) -> InsiderActivityResult:
    """
    Fetch insider activity from NASDAQ using Actor mode.

    This demonstrates how Actor mode handles direct, well-defined tasks
    with near-instant speed (~1 second per step).

    Args:
        symbol: Stock ticker symbol (default: AAPL)
        verbose: Enable verbose logging

    Returns:
        InsiderActivityResult with extracted transaction data
    """
    start_time = datetime.now()

    agent = AsyncDefaultAgent(
        max_steps=15,
        model="lux-actor-1",  # Actor mode for speed
        verbose=verbose
    )

    instruction = f"""
    1. Navigate to https://www.nasdaq.com
    2. Click on the search box or search icon
    3. Type '{symbol}' in the search field
    4. Click on the stock result for {symbol}
    5. Wait for the stock page to load
    6. Find and click on 'Insider Activity' tab or link
    7. Wait for insider activity data to load
    8. For each recent transaction in the table, extract:
       - Insider name
       - Title/Position
       - Transaction type (Buy/Sell/Exercise)
       - Number of shares
       - Share price
       - Transaction date
    9. Copy the extracted data to clipboard
    """

    try:
        result = await agent.execute(
            instruction,
            action_handler=AsyncPyautoguiActionHandler(),
            image_provider=AsyncScreenshotMaker()
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return InsiderActivityResult(
            symbol=symbol,
            company_name=f"{symbol} Inc.",
            transactions=[],  # Would be populated from clipboard/result
            extraction_time=execution_time,
            success=result if isinstance(result, bool) else True
        )

    except Exception as e:
        execution_time = (datetime.now() - start_time).total_seconds()
        return InsiderActivityResult(
            symbol=symbol,
            company_name="",
            transactions=[],
            extraction_time=execution_time,
            success=False,
            error_message=str(e)
        )


async def get_multiple_stocks(
    symbols: List[str],
    verbose: bool = False
) -> dict:
    """
    Fetch insider activity for multiple stock symbols.

    Args:
        symbols: List of stock ticker symbols
        verbose: Enable verbose logging

    Returns:
        dict mapping symbols to their InsiderActivityResult
    """
    results = {}

    for i, symbol in enumerate(symbols, 1):
        print(f"\n[{i}/{len(symbols)}] Fetching {symbol}...")
        result = await get_insider_activity(symbol, verbose)
        results[symbol] = result

        status = "Success" if result.success else f"Failed: {result.error_message}"
        print(f"    Status: {status}")
        print(f"    Time: {result.extraction_time:.2f}s")

        # Brief pause between requests
        if i < len(symbols):
            await asyncio.sleep(2)

    return results


def print_results(result: InsiderActivityResult):
    """Print formatted insider activity results."""
    print("\n" + "=" * 60)
    print(f"INSIDER ACTIVITY: {result.symbol}")
    print("=" * 60)
    print(f"Company: {result.company_name}")
    print(f"Status: {'Success' if result.success else 'Failed'}")
    print(f"Extraction Time: {result.extraction_time:.2f} seconds")

    if result.transactions:
        print(f"\nRecent Transactions ({len(result.transactions)}):")
        print("-" * 60)

        for txn in result.transactions:
            print(f"  {txn.date} | {txn.insider_name}")
            print(f"    {txn.title}")
            print(f"    {txn.transaction_type}: {txn.shares:,} shares @ ${txn.price:.2f}")
            print(f"    Value: ${txn.value:,.2f}")
            print()
    else:
        print("\n  No transaction data extracted.")
        print("  (In production, transactions would be parsed from execution results)")

    if result.error_message:
        print(f"\nError: {result.error_message}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Fetch insider activity from NASDAQ using Lux Actor mode"
    )
    parser.add_argument(
        "--symbol", "-s",
        default="AAPL",
        help="Stock ticker symbol (default: AAPL)"
    )
    parser.add_argument(
        "--symbols",
        nargs="+",
        help="Multiple stock symbols to fetch"
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
    print("NASDAQ Insider Activity - Actor Mode Example")
    print("=" * 60)
    print(f"\nModel: lux-actor-1 (Actor mode)")
    print("Speed: ~1 second per step")

    if args.symbols:
        # Multiple symbols
        print(f"Symbols: {', '.join(args.symbols)}")
        results = await get_multiple_stocks(args.symbols, args.verbose)

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        for symbol, result in results.items():
            status = "OK" if result.success else "FAIL"
            print(f"  [{status}] {symbol}: {result.extraction_time:.2f}s")

    else:
        # Single symbol
        print(f"Symbol: {args.symbol}")
        result = await get_insider_activity(args.symbol, args.verbose)
        print_results(result)

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
