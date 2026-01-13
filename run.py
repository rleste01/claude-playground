#!/usr/bin/env python3
"""
Product Arbitrage Suite - Main CLI Interface

Simple command-line interface for running the product arbitrage automation.
"""

import argparse
import sys
import os
from product_arbitrage_suite import ProductArbitrageOrchestrator, MarketAnalyzer


def print_banner():
    """Print ASCII banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║        PRODUCT ARBITRAGE SUITE                                ║
║        Translation Arbitrage Automation                       ║
║                                                               ║
║        Find → Clone → Translate → Launch → Profit             ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def cmd_full(args):
    """Run full automation pipeline."""
    orchestrator = ProductArbitrageOrchestrator(args.config)

    # YouTube videos are now optional - will auto-discover if not provided
    if not args.youtube_videos:
        print("ℹ️  No YouTube videos provided - will auto-discover videos")

    orchestrator.full_automation(
        niche=args.niche,
        funnel_url=args.funnel_url,
        youtube_videos=args.youtube_videos,
        target_market=args.target_market,
        dialect=args.dialect,
        output_dir=args.output
    )


def cmd_quick_clone(args):
    """Quick clone a funnel to new topic/market."""
    orchestrator = ProductArbitrageOrchestrator(args.config)

    orchestrator.quick_clone(
        funnel_url=args.funnel_url,
        new_topic=args.topic,
        target_market=args.target_market,
        output_dir=args.output
    )


def cmd_research(args):
    """Research and create product content only."""
    orchestrator = ProductArbitrageOrchestrator(args.config)

    # YouTube videos are now optional - will auto-discover if not provided
    if not args.youtube_videos:
        print("ℹ️  No YouTube videos provided - will auto-discover videos")

    orchestrator.research_only(
        topic=args.topic,
        youtube_videos=args.youtube_videos,
        output_path=args.output
    )


def cmd_market_analysis(args):
    """Analyze market opportunities."""
    analyzer = MarketAnalyzer()

    if args.niche:
        if args.compare:
            analyzer.compare_markets(args.niche)
        else:
            analyzer.analyze_gap(args.niche, args.target_market)
    else:
        analyzer.suggest_niches(args.target_market)


def main():
    """Main CLI entry point."""
    print_banner()

    parser = argparse.ArgumentParser(
        description="Product Arbitrage Suite - Automate info product cloning and translation"
    )

    parser.add_argument(
        '--config',
        default='config.yaml',
        help='Path to config file (default: config.yaml)'
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # FULL AUTOMATION
    full_parser = subparsers.add_parser(
        'full',
        help='Full automation: funnel → product → translation → landing page'
    )
    full_parser.add_argument('--niche', required=True, help='Product niche/topic')
    full_parser.add_argument('--funnel-url', required=True, help='Winning funnel URL to clone')
    full_parser.add_argument(
        '--youtube-videos',
        nargs='+',
        required=False,
        help='YouTube video URLs for research (optional - will auto-discover if not provided)'
    )
    full_parser.add_argument(
        '--target-market',
        default='french',
        help='Target market language (default: french)'
    )
    full_parser.add_argument(
        '--dialect',
        help='Specific dialect (e.g., brazilian, latin_american, canadian)'
    )
    full_parser.add_argument('--output', default='./output', help='Output directory')
    full_parser.set_defaults(func=cmd_full)

    # QUICK CLONE
    clone_parser = subparsers.add_parser(
        'clone',
        help='Quick clone: Recreate funnel only (no product generation)'
    )
    clone_parser.add_argument('--funnel-url', required=True, help='Funnel URL to clone')
    clone_parser.add_argument('--topic', required=True, help='New topic to adapt for')
    clone_parser.add_argument(
        '--target-market',
        default='french',
        help='Target market (default: french)'
    )
    clone_parser.add_argument('--output', default='./output', help='Output directory')
    clone_parser.set_defaults(func=cmd_quick_clone)

    # RESEARCH ONLY
    research_parser = subparsers.add_parser(
        'research',
        help='Research and generate product content only'
    )
    research_parser.add_argument('--topic', required=True, help='Product topic')
    research_parser.add_argument(
        '--youtube-videos',
        nargs='+',
        required=False,
        help='YouTube video URLs (optional - will auto-discover if not provided)'
    )
    research_parser.add_argument(
        '--output',
        default='./output/product.md',
        help='Output file path'
    )
    research_parser.set_defaults(func=cmd_research)

    # MARKET ANALYSIS
    market_parser = subparsers.add_parser(
        'market',
        help='Analyze market opportunities'
    )
    market_parser.add_argument('--niche', help='Specific niche to analyze')
    market_parser.add_argument(
        '--target-market',
        default='french',
        help='Target market (default: french)'
    )
    market_parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare opportunity across all markets'
    )
    market_parser.set_defaults(func=cmd_market_analysis)

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n⚠️  WARNING: ANTHROPIC_API_KEY not set!")
        print("   Export your API key: export ANTHROPIC_API_KEY=your_key_here")
        print("   Get a key at: https://console.anthropic.com/\n")
        sys.exit(1)

    # Run command
    args.func(args)


if __name__ == '__main__':
    main()
