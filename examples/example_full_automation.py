#!/usr/bin/env python3
"""
Example: Full Automation Pipeline

This example shows how to run the complete pipeline from finding a winning
funnel to launching in a new market.
"""

from product_arbitrage_suite import ProductArbitrageOrchestrator

def main():
    # Initialize orchestrator
    orchestrator = ProductArbitrageOrchestrator(config_path="../config.yaml")

    # Define your inputs
    niche = "fix sleep naturally"
    funnel_url = "https://example.com/sleep-fix-landing-page"  # Replace with real URL

    # YouTube videos for research (find 4 high-view videos on the topic)
    youtube_videos = [
        "https://www.youtube.com/watch?v=EXAMPLE1",  # Replace with real URLs
        "https://www.youtube.com/watch?v=EXAMPLE2",
        "https://www.youtube.com/watch?v=EXAMPLE3",
        "https://www.youtube.com/watch?v=EXAMPLE4",
    ]

    target_market = "french"  # or german, spanish, italian, portuguese
    output_dir = "./output/sleep_fix_french"

    # Run full automation
    results = orchestrator.full_automation(
        niche=niche,
        funnel_url=funnel_url,
        youtube_videos=youtube_videos,
        target_market=target_market,
        output_dir=output_dir
    )

    print("\n✅ Complete! Check output directory for all assets.")
    print(f"📂 {output_dir}")


if __name__ == "__main__":
    main()
