#!/usr/bin/env python3
"""
Example: Market Research

Analyze market opportunities before building anything.
"""

from product_arbitrage_suite import MarketAnalyzer

def main():
    analyzer = MarketAnalyzer()

    print("="*60)
    print("EXAMPLE 1: Analyze specific niche in target market")
    print("="*60)

    # Analyze sleep niche in French market
    analysis = analyzer.analyze_gap(
        niche="sleep",
        target_market="french"
    )

    print("\n" + "="*60)
    print("EXAMPLE 2: Compare opportunities across markets")
    print("="*60)

    # Compare sleep opportunity across all markets
    opportunities = analyzer.compare_markets(niche="sleep")

    print("\n" + "="*60)
    print("EXAMPLE 3: Get niche suggestions for a market")
    print("="*60)

    # What niches work best in Italian market?
    suggestions = analyzer.suggest_niches(target_market="italian")

    print("\n" + "="*60)
    print("EXAMPLE 4: Revenue estimation")
    print("="*60)

    # Estimate potential revenue
    revenue = analyzer.estimate_revenue(
        price=27,           # Product price
        daily_budget=30,    # Daily ad spend
        cpa=8.18,          # Cost per acquisition
        conversion_rate=0.03  # 3% conversion rate
    )


if __name__ == "__main__":
    main()
