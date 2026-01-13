"""Main orchestrator for automating the product arbitrage process."""

from typing import Dict, List, Optional
import os
import yaml
from .core.ad_monitor import AdMonitor
from .core.funnel_analyzer import FunnelAnalyzer
from .core.content_generator import ContentGenerator
from .core.translator import Translator
from .core.landing_page_builder import LandingPageBuilder
from .core.market_analyzer import MarketAnalyzer
from .utils.ai_helper import AIHelper


class ProductArbitrageOrchestrator:
    """Orchestrates the entire product arbitrage automation process."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize orchestrator.

        Args:
            config_path: Path to configuration file
        """
        # Load config
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        else:
            self.config = self._default_config()

        # Initialize modules
        self.ai_helper = AIHelper()
        self.ad_monitor = AdMonitor(
            min_days_running=self.config['ad_monitoring']['min_days_running']
        )
        self.funnel_analyzer = FunnelAnalyzer(self.ai_helper)
        self.content_generator = ContentGenerator(self.ai_helper)
        self.translator = Translator(self.ai_helper)
        self.landing_page_builder = LandingPageBuilder()
        self.market_analyzer = MarketAnalyzer()

    def _default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'ad_monitoring': {'min_days_running': 14},
            'target_markets': [
                {'language': 'french', 'price_multiplier': 0.9}
            ],
            'automation': {
                'auto_translate': True,
                'auto_generate_content': True,
                'auto_create_landing_page': True,
                'require_human_review': True,
            }
        }

    def full_automation(
        self,
        niche: str,
        funnel_url: str,
        youtube_videos: List[str],
        target_market: str = "french",
        output_dir: str = "./output"
    ) -> Dict:
        """
        Complete end-to-end automation.

        Args:
            niche: Product niche
            funnel_url: URL of winning funnel to copy
            youtube_videos: List of YouTube URLs for research
            target_market: Target market/language
            output_dir: Output directory

        Returns:
            Dictionary with all generated assets
        """
        print("\n" + "="*70)
        print("🚀 PRODUCT ARBITRAGE AUTOMATION - FULL PIPELINE")
        print("="*70)

        os.makedirs(output_dir, exist_ok=True)

        assets = {
            'niche': niche,
            'target_market': target_market,
            'funnel_url': funnel_url,
        }

        # STEP 1: Market Analysis
        print("\n📊 STEP 1: Market Analysis")
        market_gap = self.market_analyzer.analyze_gap(niche, target_market)
        assets['market_analysis'] = market_gap

        # STEP 2: Analyze Winning Funnel
        print("\n\n🔍 STEP 2: Analyze Winning Funnel")
        funnel_analysis = self.funnel_analyzer.analyze_funnel(funnel_url)
        assets['funnel_analysis'] = funnel_analysis

        # STEP 3: Create Product Content
        print("\n\n✍️  STEP 3: Generate Product Content")
        product_content = self.content_generator.create_from_youtube(
            topic=niche,
            video_urls=youtube_videos,
            output_path=os.path.join(output_dir, f"{niche.replace(' ', '_')}_product.pdf")
        )
        assets['product_content'] = product_content

        # STEP 4: Create Funnel Blueprint
        print("\n\n🔧 STEP 4: Create Funnel Blueprint (English)")
        funnel_blueprint = self.funnel_analyzer.recreate_funnel_blueprint(
            funnel_analysis,
            new_topic=niche,
            language="english"
        )
        assets['funnel_blueprint_en'] = funnel_blueprint

        # STEP 5: Translate Everything
        if self.config['automation']['auto_translate']:
            print(f"\n\n🌍 STEP 5: Translate to {target_market.title()}")

            # Translate funnel
            translated_funnel = self.translator.translate_funnel(
                funnel_blueprint,
                target_market
            )
            assets['funnel_blueprint_translated'] = translated_funnel

            # Translate product content
            translated_product = self.translator.translate_product_content(
                product_content,
                target_market
            )

            # Save translated product
            translated_path = os.path.join(
                output_dir,
                f"{niche.replace(' ', '_')}_product_{target_market}.md"
            )
            with open(translated_path, 'w', encoding='utf-8') as f:
                f.write(translated_product)

            assets['product_content_translated'] = translated_product

            # Generate testimonials in target language
            print(f"   Generating testimonials in {target_market}...")
            testimonials = self.ai_helper.generate_testimonials(
                niche,
                num_testimonials=5,
                language=target_market
            )
            assets['testimonials'] = testimonials

        # STEP 6: Build Landing Page
        if self.config['automation']['auto_create_landing_page']:
            print("\n\n🏗️  STEP 6: Build Landing Page")

            landing_page_path = os.path.join(output_dir, "landing_page.html")

            html = self.landing_page_builder.build_page(
                funnel_blueprint=assets.get('funnel_blueprint_translated', funnel_blueprint),
                testimonials=assets.get('testimonials', []),
                output_path=landing_page_path
            )

            assets['landing_page'] = landing_page_path

            # Generate Lovable prompt
            print("\n   Generating Lovable.ai prompt...")
            lovable_prompt = self.landing_page_builder.generate_lovable_prompt(
                assets.get('funnel_blueprint_translated', funnel_blueprint)
            )

            lovable_path = os.path.join(output_dir, "lovable_prompt.txt")
            with open(lovable_path, 'w', encoding='utf-8') as f:
                f.write(lovable_prompt)

            assets['lovable_prompt'] = lovable_path

        # STEP 7: Summary & Next Steps
        print("\n\n" + "="*70)
        print("✅ AUTOMATION COMPLETE!")
        print("="*70)

        self._print_summary(assets, output_dir)

        # Save summary
        summary_path = os.path.join(output_dir, "summary.yaml")
        with open(summary_path, 'w') as f:
            yaml.dump(assets, f, default_flow_style=False)

        print(f"\n📄 Full summary saved to: {summary_path}")

        return assets

    def _print_summary(self, assets: Dict, output_dir: str):
        """Print summary of generated assets."""

        print(f"\n📦 Generated Assets (in {output_dir}):")
        print(f"   ✓ Market analysis")
        print(f"   ✓ Funnel blueprint")
        print(f"   ✓ Product content (English + {assets['target_market']})")
        print(f"   ✓ Landing page HTML")
        print(f"   ✓ Lovable.ai prompt")
        print(f"   ✓ Testimonials ({len(assets.get('testimonials', []))})")

        print(f"\n📋 Next Steps:")
        print(f"   1. Review all generated content")
        print(f"   2. Polish translation (hire on Upwork for ~$40)")
        print(f"   3. Convert markdown to PDF (use Notion or Pandoc)")
        print(f"   4. Build landing page (use Lovable.ai with prompt)")
        print(f"   5. Set up Stripe checkout")
        print(f"   6. Launch ads on Facebook")

        if 'market_analysis' in assets:
            opportunity_score = assets['market_analysis'].get('opportunity_score', 0)
            print(f"\n💡 Market Opportunity: {opportunity_score}/10")

        print(f"\n🚀 Time to market: ~6 hours")
        print(f"   - Content generation: DONE")
        print(f"   - Translation: DONE (needs polish)")
        print(f"   - Landing page: DONE (needs deployment)")
        print(f"   - Ready to launch ads!")

    def quick_clone(
        self,
        funnel_url: str,
        new_topic: str,
        target_market: str = "french",
        output_dir: str = "./output"
    ) -> Dict:
        """
        Quick clone: Recreate funnel only (no product generation).

        Args:
            funnel_url: Winning funnel URL
            new_topic: New topic to adapt for
            target_market: Target market
            output_dir: Output directory

        Returns:
            Generated assets
        """
        print(f"\n⚡ QUICK CLONE: {new_topic} → {target_market}")

        os.makedirs(output_dir, exist_ok=True)

        # Analyze funnel
        funnel_analysis = self.funnel_analyzer.analyze_funnel(funnel_url)

        # Create blueprint
        funnel_blueprint = self.funnel_analyzer.recreate_funnel_blueprint(
            funnel_analysis,
            new_topic=new_topic,
            language="english"
        )

        # Translate
        translated_funnel = self.translator.translate_funnel(
            funnel_blueprint,
            target_market
        )

        # Generate testimonials
        testimonials = self.ai_helper.generate_testimonials(
            new_topic,
            num_testimonials=5,
            language=target_market
        )

        # Build landing page
        landing_page_path = os.path.join(output_dir, "landing_page.html")
        self.landing_page_builder.build_page(
            funnel_blueprint=translated_funnel,
            testimonials=testimonials,
            output_path=landing_page_path
        )

        print(f"\n✅ Quick clone complete!")
        print(f"   Landing page: {landing_page_path}")
        print(f"   Next: Create product content and connect payment")

        return {
            'funnel_blueprint': translated_funnel,
            'testimonials': testimonials,
            'landing_page': landing_page_path,
        }

    def research_only(
        self,
        topic: str,
        youtube_videos: List[str],
        output_path: str = "./output/product.md"
    ) -> str:
        """
        Research and generate product content only.

        Args:
            topic: Product topic
            youtube_videos: YouTube URLs
            output_path: Output file path

        Returns:
            Generated content
        """
        print(f"\n📚 RESEARCH MODE: {topic}")

        content = self.content_generator.create_from_youtube(
            topic=topic,
            video_urls=youtube_videos,
            output_path=output_path
        )

        print(f"\n✅ Product content generated!")
        print(f"   File: {output_path}")

        return content
