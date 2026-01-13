"""Analyze and recreate sales funnels."""

from typing import Dict, Optional
from ..utils.scraper import WebScraper
from ..utils.ai_helper import AIHelper


class FunnelAnalyzer:
    """Analyze sales funnels and extract key components."""

    def __init__(self, ai_helper: Optional[AIHelper] = None):
        """
        Initialize funnel analyzer.

        Args:
            ai_helper: AI helper instance for analysis
        """
        self.scraper = WebScraper()
        self.ai_helper = ai_helper or AIHelper()

    def analyze_funnel(self, url: str) -> Dict:
        """
        Analyze a complete sales funnel.

        Args:
            url: Landing page URL

        Returns:
            Funnel analysis dictionary
        """
        print(f"\n📊 Analyzing Funnel: {url}")

        # Fetch the page
        print("   Fetching page...")
        html = self.scraper.fetch_page(url)

        # Parse basic structure
        print("   Parsing structure...")
        parsed_data = self.scraper.parse_landing_page(html, url)

        # AI-powered analysis
        print("   AI analysis...")
        ai_analysis = self.ai_helper.analyze_funnel(html, url)

        # Combine results
        analysis = {
            'url': url,
            'parsed_data': parsed_data,
            'ai_analysis': ai_analysis,
            'components': self._extract_components(parsed_data),
            'structure': self._determine_structure(parsed_data),
        }

        print("   ✓ Analysis complete")

        return analysis

    def _extract_components(self, parsed_data: Dict) -> Dict:
        """
        Extract key funnel components.

        Args:
            parsed_data: Parsed page data

        Returns:
            Dictionary of components
        """
        return {
            'headline': parsed_data.get('headline', ''),
            'subheadline': parsed_data.get('subheadline', ''),
            'bullets': parsed_data.get('bullets', []),
            'cta': parsed_data.get('cta_text', ''),
            'price': parsed_data.get('price', ''),
            'social_proof': parsed_data.get('testimonials', []),
            'images': parsed_data.get('images', []),
        }

    def _determine_structure(self, parsed_data: Dict) -> str:
        """
        Determine funnel structure type.

        Args:
            parsed_data: Parsed page data

        Returns:
            Structure type description
        """
        has_long_copy = len(parsed_data.get('bullets', [])) > 5
        has_testimonials = len(parsed_data.get('testimonials', [])) > 0
        has_price = bool(parsed_data.get('price'))

        if has_long_copy and has_testimonials:
            return "long-form-sales-page"
        elif has_price and len(parsed_data.get('bullets', [])) <= 5:
            return "short-form-sales-page"
        elif not has_price:
            return "lead-capture-page"
        else:
            return "standard-sales-page"

    def recreate_funnel_blueprint(self, analysis: Dict, new_topic: str, language: str = "english") -> Dict:
        """
        Create a blueprint for recreating the funnel with a new topic.

        Args:
            analysis: Funnel analysis from analyze_funnel()
            new_topic: New topic to adapt for
            language: Target language

        Returns:
            Blueprint for new funnel
        """
        print(f"\n🔧 Creating Funnel Blueprint")
        print(f"   Original: {analysis['url']}")
        print(f"   New Topic: {new_topic}")
        print(f"   Language: {language}")

        components = analysis['components']

        # Use AI to recreate copy
        print("   Recreating headline...")
        new_headline = self.ai_helper.recreate_copy(
            components['headline'],
            new_topic,
            language if language != "english" else None
        )

        print("   Recreating bullets...")
        bullets_text = '\n'.join(f"- {b}" for b in components['bullets'])
        new_bullets = self.ai_helper.recreate_copy(
            bullets_text,
            new_topic,
            language if language != "english" else None
        )

        print("   Recreating CTA...")
        new_cta = self.ai_helper.recreate_copy(
            components['cta'],
            new_topic,
            language if language != "english" else None
        )

        blueprint = {
            'topic': new_topic,
            'language': language,
            'structure_type': analysis['structure'],
            'components': {
                'headline': new_headline,
                'subheadline': '',  # Could add subheadline recreation
                'bullets': new_bullets.split('\n'),
                'cta': new_cta,
                'price': components['price'],  # Keep same price or adjust
                'num_testimonials': len(components['social_proof']),
            },
            'original_url': analysis['url'],
        }

        print("   ✓ Blueprint created")

        return blueprint

    def get_funnel_screenshots(self, url: str, output_dir: str = "./screenshots") -> Dict[str, str]:
        """
        Take screenshots of funnel sections.

        Args:
            url: Funnel URL
            output_dir: Directory to save screenshots

        Returns:
            Dictionary mapping section names to file paths
        """
        import os

        os.makedirs(output_dir, exist_ok=True)

        screenshots = {}

        # Full page screenshot
        full_page_path = os.path.join(output_dir, "full_page.png")
        if self.scraper.screenshot_page(url, full_page_path):
            screenshots['full_page'] = full_page_path
            print(f"   ✓ Saved screenshot: {full_page_path}")

        return screenshots

    def compare_funnels(self, funnel_a: Dict, funnel_b: Dict) -> Dict:
        """
        Compare two funnels to identify similarities and differences.

        Args:
            funnel_a: First funnel analysis
            funnel_b: Second funnel analysis

        Returns:
            Comparison results
        """
        comparison = {
            'structure_match': funnel_a['structure'] == funnel_b['structure'],
            'same_structure_type': funnel_a['structure'],
            'price_difference': {
                'funnel_a': funnel_a['components']['price'],
                'funnel_b': funnel_b['components']['price'],
            },
            'bullet_count': {
                'funnel_a': len(funnel_a['components']['bullets']),
                'funnel_b': len(funnel_b['components']['bullets']),
            },
            'has_social_proof': {
                'funnel_a': len(funnel_a['components']['social_proof']) > 0,
                'funnel_b': len(funnel_b['components']['social_proof']) > 0,
            }
        }

        return comparison
