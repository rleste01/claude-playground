#!/usr/bin/env python3
"""
Example: Quick Clone

Quick clone just recreates the funnel without generating product content.
Use this when you already have a product and just need a landing page.
"""

from product_arbitrage_suite import ProductArbitrageOrchestrator

def main():
    orchestrator = ProductArbitrageOrchestrator()

    # Clone a proven funnel to a new topic
    results = orchestrator.quick_clone(
        funnel_url="https://example.com/winning-funnel",
        new_topic="fix anxiety naturally",
        target_market="german",
        output_dir="./output/anxiety_german"
    )

    print(f"\n✅ Landing page created: {results['landing_page']}")
    print("Next steps:")
    print("1. Create your product content separately")
    print("2. Set up Stripe/payment processor")
    print("3. Deploy landing page")
    print("4. Launch ads!")


if __name__ == "__main__":
    main()
