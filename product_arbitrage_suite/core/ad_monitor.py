"""Monitor and analyze ads from Facebook Ad Library."""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json


class AdMonitor:
    """Monitor ads to find proven winners."""

    def __init__(self, min_days_running: int = 14):
        """
        Initialize ad monitor.

        Args:
            min_days_running: Minimum days an ad must be running to consider
        """
        self.min_days_running = min_days_running
        self.tracked_ads = []

    def is_winner(self, ad_data: Dict) -> bool:
        """
        Determine if an ad is a "winner" based on running time.

        Args:
            ad_data: Ad data dictionary with 'days_running' field

        Returns:
            True if ad meets criteria
        """
        days_running = ad_data.get('days_running', 0)
        return days_running >= self.min_days_running

    def analyze_ad(self, ad_data: Dict) -> Dict:
        """
        Analyze an ad to extract key insights.

        Args:
            ad_data: Ad data dictionary

        Returns:
            Analysis results
        """
        analysis = {
            'is_winner': self.is_winner(ad_data),
            'days_running': ad_data.get('days_running', 0),
            'niche': self._detect_niche(ad_data),
            'price_point': self._extract_price(ad_data),
            'copy_structure': self._analyze_copy_structure(ad_data),
            'landing_page': ad_data.get('landing_page_url', ''),
            'ad_creative': ad_data.get('creative_url', ''),
        }

        return analysis

    def _detect_niche(self, ad_data: Dict) -> str:
        """Detect product niche from ad data."""
        # Common niche keywords
        niche_keywords = {
            'sleep': ['sleep', 'insomnia', 'rest', 'tired', 'exhausted'],
            'productivity': ['productivity', 'focus', 'efficiency', 'time management'],
            'fitness': ['fitness', 'workout', 'weight loss', 'muscle', 'exercise'],
            'money': ['money', 'income', 'wealth', 'financial', 'investing'],
            'relationships': ['relationship', 'dating', 'marriage', 'love'],
            'business': ['business', 'entrepreneur', 'startup', 'sales'],
        }

        ad_copy = ad_data.get('ad_copy', '').lower()

        for niche, keywords in niche_keywords.items():
            if any(keyword in ad_copy for keyword in keywords):
                return niche

        return 'unknown'

    def _extract_price(self, ad_data: Dict) -> Optional[float]:
        """Extract price from ad copy or landing page."""
        import re

        text = ad_data.get('ad_copy', '') + ' ' + ad_data.get('landing_page_text', '')

        # Look for price patterns
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',
            r'€(\d+(?:\.\d{2})?)',
            r'£(\d+(?:\.\d{2})?)',
        ]

        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                return float(match.group(1))

        return None

    def _analyze_copy_structure(self, ad_data: Dict) -> Dict:
        """Analyze the structure of ad copy."""
        ad_copy = ad_data.get('ad_copy', '')

        return {
            'has_hook': any(word in ad_copy.lower() for word in ['how', 'secret', 'discover', 'learn']),
            'has_urgency': any(word in ad_copy.lower() for word in ['now', 'today', 'limited', 'urgent']),
            'has_proof': any(word in ad_copy.lower() for word in ['proof', 'results', 'success', 'testimonial']),
            'has_cta': any(word in ad_copy.lower() for word in ['click', 'get', 'download', 'buy', 'order']),
            'length': len(ad_copy),
        }

    def find_winning_ads(
        self,
        niche: str,
        country: str = "US",
        max_results: int = 10
    ) -> List[Dict]:
        """
        Find winning ads in a specific niche.

        Args:
            niche: Product niche to search
            country: Target country
            max_results: Maximum number of ads to return

        Returns:
            List of winning ad data
        """
        print(f"\n🔍 Finding Winning Ads")
        print(f"   Niche: {niche}")
        print(f"   Country: {country}")
        print(f"   Criteria: Running {self.min_days_running}+ days")
        print(f"\n   📱 Manual Process:")
        print(f"   1. Visit: https://www.facebook.com/ads/library")
        print(f"   2. Search: '{niche}' keywords")
        print(f"   3. Filter: Active ads in {country}")
        print(f"   4. Check 'Started Running' dates")
        print(f"   5. Select ads running {self.min_days_running}+ days")
        print(f"   6. Note: landing page URL, price, copy structure")

        # Return template for manual data entry
        return [
            {
                'template': True,
                'niche': niche,
                'country': country,
                'ad_copy': '',
                'landing_page_url': '',
                'days_running': 0,
                'creative_url': '',
                'instructions': 'Fill in data from Facebook Ad Library search'
            }
        ]

    def save_ad_data(self, ad_data: Dict, filepath: str):
        """
        Save ad data to file.

        Args:
            ad_data: Ad data to save
            filepath: Path to save file
        """
        with open(filepath, 'w') as f:
            json.dump(ad_data, f, indent=2)

        print(f"✓ Saved ad data to {filepath}")

    def load_ad_data(self, filepath: str) -> Dict:
        """
        Load ad data from file.

        Args:
            filepath: Path to load file

        Returns:
            Ad data dictionary
        """
        with open(filepath, 'r') as f:
            return json.load(f)
